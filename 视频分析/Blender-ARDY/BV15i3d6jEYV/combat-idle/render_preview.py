"""Render the actual saved loop, front/side checks, and mesh contact metrics."""
import argparse
import json
from pathlib import Path
import sys
import bpy
import numpy as np
from mathutils import Vector

parser = argparse.ArgumentParser()
parser.add_argument('--artifacts', type=Path, required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out = args.artifacts.resolve()
bpy.ops.wm.open_mainfile(filepath=str(out/'ARDY_CombatIdle_Core28.blend'))
scene = bpy.context.scene
arm = bpy.data.objects['Armature']
mesh = bpy.data.objects['SK_ARDY_Core28']
unique_frames = scene.frame_end
ankles = {'left': 'LeftFoot', 'right': 'RightFoot'}
sole_ids = {side: [v.index for v in mesh.data.vertices
                  if v.co.z < 2.0 and (v.co.x > 0 if side=='left' else v.co.x < 0)] for side in ankles}
report = {'samples': [], 'root_motion': 'fixed independent root; pelvis has small sway'}
all_positions = []
for frame in range(1, unique_frames+2):
    scene.frame_set(frame)
    evaluated = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    world = np.array([(mesh.matrix_world @ v.co)[:] for v in evaluated.data.vertices])
    all_positions.append(world)
    if frame in (1,21,41,61,81):
        report['samples'].append({'frame': frame, 'mesh_min_height_cm': float(world[:,2].min()),
                                 'sole_min_height_cm': {side: float(world[ids,2].min()) for side,ids in sole_ids.items()}})
all_positions = np.array(all_positions)
report['mesh_endpoint_max_difference_cm'] = float(np.linalg.norm(all_positions[-1]-all_positions[0],axis=-1).max())
report['mesh_max_frame_displacement_cm'] = float(np.linalg.norm(np.diff(all_positions,axis=0),axis=-1).max())
report['sole_horizontal_drift_cm'] = {side: float(np.linalg.norm(all_positions[:,ids,:2]-all_positions[0,ids,:2],axis=-1).max()) for side,ids in sole_ids.items()}
report['sole_vertices'] = {side: len(ids) for side,ids in sole_ids.items()}
(out/'mesh-contact-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
assert all(-.02 <= h <= .05 for s in report['samples'] for h in s['sole_min_height_cm'].values()), 'Sole contact height failed'
assert report['mesh_endpoint_max_difference_cm'] < .001, 'Mesh loop endpoint differs'
assert max(report['sole_horizontal_drift_cm'].values()) < .01, 'Soles drift'

scene.render.resolution_x, scene.render.resolution_y = 768, 768
scene.render.resolution_percentage = 100
scene.frame_set(1)
camera = scene.camera
original_position, original_rotation = camera.location.copy(), camera.rotation_euler.copy()
for name, location in [('front',(0,-550,135)),('side',(550,0,135))]:
    camera.location = location
    camera.rotation_euler = (Vector((0,0,95))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath = str(out/f'check-{name}.png')
    bpy.ops.render.render(write_still=True)
camera.location, camera.rotation_euler = original_position, original_rotation
frames_dir = out/'preview-frames'
frames_dir.mkdir(exist_ok=True)
for frame in range(1, unique_frames+1):
    scene.frame_set(frame)
    scene.render.filepath = str(frames_dir/f'{frame:04d}.png')
    bpy.ops.render.render(write_still=True)
print('COMBAT_PREVIEW_RENDERED', json.dumps(report))
