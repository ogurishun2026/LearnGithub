"""Fresh-process reload and FBX round-trip checks; does not modify project assets."""
import argparse
import json
from pathlib import Path
import sys

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_blender import bone_audit


args_parser = argparse.ArgumentParser()
args_parser.add_argument('--artifacts', type=Path, required=True)
args = args_parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = args.artifacts.resolve()
reference = np.load(out / 'source_reference.npz', allow_pickle=False)
report = {}
bpy.ops.wm.open_mainfile(filepath=str(out / 'ARDY_CombatIdle_Core28.blend'))
report['blend_reload'] = bone_audit(bpy.data.objects['Armature'], reference)
loop_arm = bpy.data.objects['Armature']
root_frames = []
for frame in range(1, len(reference['positions']) + 1):
    bpy.context.scene.frame_set(frame)
    root_frames.append(np.array(loop_arm.matrix_world @ loop_arm.pose.bones['root'].matrix))
assert np.max(np.abs(np.array(root_frames)-root_frames[0])) < 1e-6, 'Idle root drifts'
assert np.max(np.abs(reference['positions'][-1]-reference['positions'][0])) < 1e-9
report['loop'] = {'root_max_matrix_drift': float(np.max(np.abs(np.array(root_frames)-root_frames[0]))),
                  'endpoint_joint_error_cm': float(np.max(np.abs(reference['positions'][-1]-reference['positions'][0]))*100),
                  'unique_frames': len(reference['positions'])-1, 'duplicate_endpoint_frame': len(reference['positions'])}
original_rest = {b.name: np.array(b.matrix_local) for b in bpy.data.objects['Armature'].data.bones}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 0.01
bpy.ops.import_scene.fbx(filepath=str(out / 'SK_ARDY_Core28.fbx'), use_anim=False)
arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
mesh = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
report['skeletal_fbx'] = {'bones': len(arm.data.bones), 'pelvis_parent': arm.data.bones['pelvis'].parent.name,
                          'armature_scale': list(arm.scale), 'mesh_height_cm': float(mesh.dimensions.z),
                          'mesh_vertices': len(mesh.data.vertices)}
assert report['skeletal_fbx']['bones'] == 28
assert report['skeletal_fbx']['pelvis_parent'] == 'root'
assert max(abs(v - 1) for v in arm.scale) < 1e-4
assert 185 < mesh.dimensions.z < 195
static_rest = {b.name: np.array(arm.matrix_world @ b.matrix_local) for b in arm.data.bones}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 0.01
bpy.context.scene.render.fps = 20
bpy.ops.import_scene.fbx(filepath=str(out / 'AN_ARDY_CombatIdle_Loop.fbx'), use_anim=True, anim_offset=0)
arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
print('ANIM_FRAME_RANGE', list(arm.animation_data.action.frame_range), 'SCENE_FPS', bpy.context.scene.render.fps, 'SCALE', list(arm.scale), flush=True)
print('ANIM_ARM_WORLD', [list(row) for row in arm.matrix_world], flush=True)
for name in ('root', 'pelvis', 'LeftArm', 'LeftHand'):
    imported_rest = np.array(arm.matrix_world @ arm.data.bones[name].matrix_local)
    print('REST_COMPARISON', name, 'static_vs_original', float(np.abs(static_rest[name] - original_rest[name]).max()),
          'anim_vs_static', float(np.abs(imported_rest - static_rest[name]).max()), flush=True)
for f in (1, 2, 20, 21, 39, 40, 41):
    bpy.context.scene.frame_set(f)
    print('ANIM_SAMPLE', f, list(arm.pose.bones['root'].head), list(arm.pose.bones['pelvis'].head), flush=True)
report['animation_fbx'] = {'bones': len(arm.data.bones), 'armature_scale': list(arm.scale),
                          'action': arm.animation_data.action.name,
                          'frame_range': list(arm.animation_data.action.frame_range),
                          'pose_audit': bone_audit(arm, reference)}
assert report['animation_fbx']['frame_range'] == [1, len(reference['positions'])]
report['status'] = 'pass'
report['unreal_import_status'] = 'not tested in Unreal; FBX round-trip checked in Blender only'
(out / 'saved-export-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('ARDY_SAVED_EXPORT_VERIFIED', json.dumps(report))
