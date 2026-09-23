"""Fresh-process Blender and FBX checks against the selected motion contract."""
import argparse
import json
from pathlib import Path
import sys
import bpy
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_blender import bone_audit

parser = argparse.ArgumentParser()
parser.add_argument('--artifacts',type=Path,required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out = args.artifacts.resolve()
contract = json.loads((out/'motion.json').read_text(encoding='utf-8'))
reference = np.load(out/'source_reference.npz',allow_pickle=False)
name, frames, fps = contract['name'],contract['frames'],contract['fps']

def audit_structure(arm):
    expected = {str(n): (None if p<0 else str(reference['names'][p])) for n,p in zip(reference['names'],reference['parents'])}
    actual = {b.name: b.parent.name if b.parent else None for b in arm.data.bones}
    assert actual == expected, 'Bone names or parents differ'
    assert max(abs(v-1) for v in arm.scale)<1e-4, 'Non-unit armature scale'

def new_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = .01
    scene.render.fps = round(fps)
    scene.render.fps_base = round(fps)/fps

report = {}
bpy.ops.wm.open_mainfile(filepath=str(out/f'{name}.blend'))
arm = bpy.data.objects['Armature']
audit_structure(arm)
assert bpy.context.scene.frame_end == contract['playback_end']
report['blend_reload'] = bone_audit(arm,reference)
if contract['root_mode']=='fixed':
    roots = []
    for frame in range(1,frames+1):
        bpy.context.scene.frame_set(frame)
        roots.append(np.array(arm.matrix_world @ arm.pose.bones['root'].matrix))
    report['root_max_matrix_drift'] = float(np.max(np.abs(np.array(roots)-roots[0])))
    assert report['root_max_matrix_drift']<1e-6
if contract['loop']:
    report['endpoint_joint_error_cm'] = float(np.max(np.abs(reference['positions'][-1]-reference['positions'][0]))*100)
    assert report['endpoint_joint_error_cm']<.001

new_scene()
bpy.ops.import_scene.fbx(filepath=str(out/'SK_ARDY_Core28.fbx'),use_anim=False)
arm = next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
mesh = next(o for o in bpy.context.scene.objects if o.type=='MESH')
audit_structure(arm)
report['skeletal_fbx'] = {'bones':len(arm.data.bones),'height_cm':float(mesh.dimensions.z),'scale':list(arm.scale)}
expected_height = float(np.ptp(reference['bind_vertices'][:,1])*100)
assert abs(mesh.dimensions.z-expected_height)<.01
static_rest = {b.name:np.array(arm.matrix_world @ b.matrix_local) for b in arm.data.bones}

new_scene()
bpy.ops.import_scene.fbx(filepath=str(out/f'AN_{name}.fbx'),use_anim=True,anim_offset=0)
arm = next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
audit_structure(arm)
rest_error = max(float(np.abs(np.array(arm.matrix_world @ b.matrix_local)-static_rest[b.name]).max()) for b in arm.data.bones)
assert rest_error<.01, 'Animation FBX bind pose differs from static mesh'
frame_range = list(arm.animation_data.action.frame_range)
assert frame_range == [1,frames], frame_range
report['animation_fbx'] = {'frame_range':frame_range,'pose_audit':bone_audit(arm,reference),'bind_matrix_error':rest_error}
report['status'] = 'pass'
report['unreal_status'] = 'not tested; this report covers Blender and FBX round-trip only'
(out/'saved-export-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ARDY_SAVED_EXPORT_VERIFIED',json.dumps(report))
