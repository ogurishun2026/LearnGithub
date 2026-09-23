"""Import BVH, attach the upstream reference skin, audit, and export separate FBXs."""
import argparse
import json
import sys
from pathlib import Path

import addon_utils
import bpy
from mathutils import Matrix, Vector
import numpy as np

C = np.array([[1., 0, 0], [0, 0, -1], [0, 1, 0]])


def bone_audit(arm, reference):
    names = list(reference['names'])
    max_position, max_rotation = 0., 0.
    for i in range(len(reference['positions'])):
        bpy.context.scene.frame_set(i + 1)
        for j, name in enumerate(names):
            bone = arm.pose.bones[str(name)]
            actual = np.array(arm.matrix_world @ bone.matrix)
            expected = C @ reference['positions'][i, j] * 100
            max_position = max(max_position, float(np.linalg.norm(actual[:3, 3] - expected)))
            # BVH rest axes are carried by each Blender edit bone.
            rest = np.array(arm.data.bones[str(name)].matrix_local)
            deform_rotation = actual[:3, :3] @ rest[:3, :3].T
            max_rotation = max(max_rotation, float(np.max(np.abs(deform_rotation - C @ reference['rotations'][i, j] @ C.T))))
    if max_position > 0.01 or max_rotation > 1e-4:
        raise RuntimeError(f'Pose conversion failed: {max_position=} cm, {max_rotation=}')
    return {'max_joint_position_error_cm': max_position, 'max_rotation_matrix_error': max_rotation}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    out = args.artifacts.resolve()
    ref = np.load(out / 'source_reference.npz', allow_pickle=False)
    frames = len(ref['positions'])
    fps = int(ref['fps'])
    samples = [int(x) for x in np.linspace(1, frames, 5)]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 0.01
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, frames
    addon_utils.enable('io_anim_bvh', default_set=False)
    bpy.ops.import_anim.bvh(filepath=str(out / 'ARDY_CombatIdle_Core27.bvh'), global_scale=1,
                            frame_start=1, rotate_mode='QUATERNION', use_fps_scale=False,
                            update_scene_fps=True, update_scene_duration=True,
                            axis_forward='-Z', axis_up='Y')
    # Blender's BVH duration update adds an inclusive endpoint; retain the exact source sample count.
    scene.frame_start, scene.frame_end = 1, frames
    arm = bpy.context.object
    arm.name = 'Armature'
    arm.show_in_front = True
    # Verify standalone BVH import before adding the independent UE motion root.
    imported_error = 0.
    for frame in range(frames):
        scene.frame_set(frame + 1)
        for index, name in enumerate(ref['names'][1:], 1):
            actual = np.array(arm.matrix_world @ arm.pose.bones[str(name)].head)
            imported_error = max(imported_error, float(np.linalg.norm(actual - C @ ref['positions'][frame, index] * 100)))
    if imported_error > 0.01:
        raise RuntimeError(f'Standalone BVH import error: {imported_error} cm')
    imported_action = arm.animation_data.action
    arm.animation_data_clear()
    bpy.data.actions.remove(imported_action)
    bpy.ops.object.mode_set(mode='EDIT')
    shift = Vector(C @ ref['bind_rig_transform'][0, :3, 3] * 100)
    original = {b.name: (b.head.copy(), b.tail.copy()) for b in arm.data.edit_bones}
    for bone in arm.data.edit_bones:
        bone.use_connect = False
        bone.head = original[bone.name][0] + shift
        bone.tail = original[bone.name][1] + shift
    root = arm.data.edit_bones.new('root')
    root.head, root.tail = (0, 0, 0), (0, 0, 10)
    arm.data.edit_bones['pelvis'].parent = root
    bpy.ops.object.mode_set(mode='OBJECT')
    action = bpy.data.actions.new('ARDY_CombatIdle_Loop_v1')
    arm.animation_data_create().action = action
    action.use_fake_user = True
    previous_quaternions = {}
    for frame in range(frames):
        scene.frame_set(frame + 1)
        desired = {}
        for index, item in enumerate(ref['names']):
            name = str(item)
            bone = arm.pose.bones[name]
            matrix = Matrix((C @ ref['rotations'][frame, index] @ C.T).tolist()).to_4x4() @ bone.bone.matrix_local.to_3x3().to_4x4()
            matrix.translation = Vector(C @ ref['positions'][frame, index] * 100)
            desired[name] = matrix
            kwargs = {} if bone.parent is None else {'parent_matrix': desired[bone.parent.name], 'parent_matrix_local': bone.parent.bone.matrix_local}
            basis = bone.bone.convert_local_to_pose(matrix, bone.bone.matrix_local, invert=True, **kwargs)
            location, quaternion, scale = basis.decompose()
            if name in previous_quaternions and quaternion.dot(previous_quaternions[name]) < 0:
                quaternion.negate()
            previous_quaternions[name] = quaternion.copy()
            if max(abs(v - 1) for v in scale) > 1e-4:
                raise RuntimeError(f'Nonunit pose scale: {name}')
            bone.rotation_mode = 'QUATERNION'
            bone.location, bone.rotation_quaternion, bone.scale = location, quaternion, (1, 1, 1)
            bone.keyframe_insert(data_path='location', frame=frame + 1, group=name)
            bone.keyframe_insert(data_path='rotation_quaternion', frame=frame + 1, group=name)
    report = {'blender_version': bpy.app.version_string, 'bones': len(arm.data.bones),
              'source': 'ARDY Core27 + independent root; Hips renamed pelvis',
              'frame_range': [1, frames], 'fps': fps, 'unit_scale_m': 0.01,
              'hierarchy_root': arm.data.bones['pelvis'].parent.name,
              'bvh_import_max_joint_error_cm': imported_error, 'pose_audit': bone_audit(arm, ref)}
    if len(arm.data.bones) != 28 or arm.data.bones['pelvis'].parent.name != 'root':
        raise RuntimeError('Unexpected bone hierarchy')

    vertices = ref['bind_vertices'] @ C.T * 100
    mesh_data = bpy.data.meshes.new('ARDY_ReferenceSkin')
    mesh_data.from_pydata(vertices.tolist(), [], ref['faces'].tolist())
    mesh_data.update()
    mesh = bpy.data.objects.new('SK_ARDY_Core28', mesh_data)
    scene.collection.objects.link(mesh)
    for poly in mesh.data.polygons:
        poly.use_smooth = True
    mesh.parent = arm
    modifier = mesh.modifiers.new('ARDY skin', 'ARMATURE')
    modifier.object = arm
    weights = ref['lbs_weights'].copy()
    indices = ref['lbs_indices']
    # Only 18 reference vertices use five weights. Keep four and renormalize for this export.
    order = np.argsort(weights, axis=1)
    weights[np.arange(len(weights)), order[:, 0]] = 0
    weights /= weights.sum(axis=1, keepdims=True)
    for j, original in enumerate(ref['rig_joint_names']):
        name = 'pelvis' if str(original) == 'Hips' else str(original)
        group = mesh.vertex_groups.new(name=name)
        for vertex, slot in np.argwhere((indices == j) & (weights > 0)):
            group.add([int(vertex)], float(weights[vertex, slot]), 'ADD')
    report['skin'] = {'vertices': len(vertices), 'faces': len(ref['faces']),
                      'vertices_pruned_from_five_weights': int(((ref['lbs_weights'] > 1e-8).sum(axis=1) == 5).sum()),
                      'max_influences': max(len(v.groups) for v in mesh.data.vertices),
                      'unweighted_vertices': sum(len(v.groups) == 0 for v in mesh.data.vertices)}
    inverse_bind = np.linalg.inv(ref['bind_rig_transform'])
    homogeneous = np.concatenate([ref['bind_vertices'], np.ones((len(vertices), 1))], axis=1)
    max_skin_delta = 0.
    for frame in samples:
        scene.frame_set(frame)
        transforms = np.tile(np.eye(4), (27, 1, 1))
        transforms[:, :3, :3] = ref['rotations'][frame - 1, 1:]
        transforms[:, :3, 3] = ref['positions'][frame - 1, 1:]
        affine = transforms @ inverse_bind
        influences = np.einsum('vwij,vj->vwi', affine[indices, :3, :], homogeneous)
        expected = np.sum(influences * ref['lbs_weights'][:, :, None], axis=1)
        evaluated = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
        actual = np.array([v.co[:] for v in evaluated.data.vertices]) @ C / 100
        max_skin_delta = max(max_skin_delta, float(np.linalg.norm(actual - expected, axis=1).max()))
    report['skin']['max_vertex_difference_from_upstream_m'] = max_skin_delta
    if report['skin']['unweighted_vertices'] or report['skin']['max_influences'] > 4:
        raise RuntimeError('Invalid skin weights')

    def export(path, animation, include_mesh):
        bpy.ops.object.select_all(action='DESELECT')
        arm.select_set(True)
        mesh.select_set(include_mesh)
        bpy.context.view_layer.objects.active = arm
        bpy.ops.export_scene.fbx(filepath=str(path), use_selection=True, global_scale=1,
            apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', axis_forward='-Z', axis_up='Y',
            object_types={'ARMATURE', 'MESH'} if include_mesh else {'ARMATURE'},
            add_leaf_bones=False, use_armature_deform_only=True,
            bake_anim=animation, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False, bake_anim_force_startend_keying=True,
            bake_anim_step=1, bake_anim_simplify_factor=0, path_mode='AUTO')

    arm.animation_data.action = None
    for bone in arm.pose.bones:
        bone.matrix_basis.identity()
    bpy.context.view_layer.update()
    export(out / 'SK_ARDY_Core28.fbx', False, True)
    arm.animation_data.action = action
    scene.frame_set(1)
    # Include skin clusters so FBX carries the original T-pose bind matrices;
    # an armature-only file otherwise falls back to the currently posed node transforms.
    export(out / 'AN_ARDY_CombatIdle_Loop.fbx', True, True)

    # Review scene only; camera and floor are excluded from both FBX exports.
    material = bpy.data.materials.new('ARDY blue')
    material.diffuse_color = (0.12, 0.36, 0.62, 1)
    mesh.data.materials.append(material)
    bpy.ops.mesh.primitive_plane_add(size=1200, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = 'Preview_Floor'
    floor_material = bpy.data.materials.new('Floor')
    floor_material.diffuse_color = (0.55, 0.58, 0.63, 1)
    floor.data.materials.append(floor_material)
    bpy.ops.object.camera_add(location=(330, -490, 230))
    camera = bpy.context.object
    camera.rotation_euler = (Vector((0, 0, 95)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 245
    camera.data.clip_end = 5000
    scene.camera = camera
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'MATERIAL'
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.background_type = 'WORLD'
    scene.world = bpy.data.worlds.new('ARDY Preview World')
    scene.world.color = (0.8, 0.8, 0.8)
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.clip_end = 5000
            area.spaces.active.region_3d.view_distance = 430
            area.spaces.active.region_3d.view_location = Vector((0, 0, 100))
    # The last keyed pose duplicates frame 1 for FBX timing; viewport loops unique samples.
    scene.frame_end = frames - 1
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'ARDY_CombatIdle_Core28.blend'))
    for frame in samples:
        scene.frame_set(frame)
        scene.render.filepath = str(out / f'preview-{frame:02d}.png')
        bpy.ops.render.render(write_still=True)
    (out / 'blender-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('ARDY_BLENDER_EXPORT_OK', json.dumps(report))


if __name__ == '__main__':
    main()
