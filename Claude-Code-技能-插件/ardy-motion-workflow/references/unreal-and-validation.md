# Unreal handoff and evidence boundaries

Blender verification and UE import are separate stages. No generic Core28 export proves an Animation Sequence works on Manny. The bundled workflow has been exercised on Core27 walk and combat idle in Blender, not on a target UE character.

## Source import

For a first import, use a new task/version directory. Import `SK_ARDY_Core28.fbx` with Skeleton=None and animations disabled. Only reuse a source Skeleton whose bone names, parents and bind pose match the same contract. Preserve existing Manny and project Skeleton assets.

Import `AN_<name>.fbx` with that ARDY Skeleton, Import Animations enabled and Import Mesh disabled. Keep the existing reference pose and source sample rate; disable default 30 FPS resampling if applicable. Exact FBX/Interchange UI labels vary by UE version. Do not select Manny directly.

Check bone count 28, direct `root → pelvis`, scale, pose, duration and visible motion inside UE. Forty samples at 20 FPS have a 1.95-second key span; 80 unique loop samples plus duplicate endpoint have a 4-second span. Neither is missing a frame.

## Retargeting to Manny/Quinn or another rig

Create/use source and target IK Rigs and an IK Retargeter. Retarget Root is pelvis on both. The root-motion chain is **root → root**, never root → pelvis. Define compatible torso, neck/head, left/right arm, and left/right leg chains; review existing chain endpoints instead of assuming identical names mean identical semantics.

Typical bone correspondence:

| ARDY | Manny |
|---|---|
| Spine → Spine3 | spine_01 → spine_05 |
| Neck → Head | neck_01 → head |
| LeftShoulder / RightShoulder | clavicle_l / clavicle_r |
| LeftArm → LeftHand / RightArm → RightHand | upperarm_l → hand_l / upperarm_r → hand_r |
| LeftUpLeg → LeftFoot / RightUpLeg → RightFoot | thigh_l → foot_l / thigh_r → foot_r |
| LeftToeBase / RightToeBase | ball_l / ball_r |

Align the source T pose and target A/other pose, body facing and size. Preserve root travel for locomotion, and keep stationary idle root fixed. In UE versions exposing Root Motion operations, specify target_root=root and target_pelvis=pelvis and ensure the correct target rig/pose is active. Diagnose facing with hips/chest body orientation, not an individual bone's local axis.

Preview and export retargeted animation before using it in Sequencer or an Anim Blueprint. For movement-driven locomotion use an in-place animation; for root-driven locomotion configure Root Motion consistently with the Character/Montage setup. Do not apply the same displacement twice. Add a target-character fist pose when full finger chains exist and the motion calls for closed fists.

## Evidence to deliver

- Actual inputs/hashes, generation metadata, source versus processed NPZ, and deviations such as NF4.
- Fresh `.blend` reopen plus static/animated FBX reimport; bone hierarchy, scales, bind pose, frame range and pose comparisons.
- Foot skin/contact checks when relevant, root trajectory and loop checks, rendered multi-view frames and motion preview.
- UE import and target retarget reports/screenshots only if those stages actually ran; otherwise state them as untested.

Stop on wrong bone count, non-unit scale, root/pelvis cancellation, invalid rotations, backward limbs, obvious skin failure or wrong action. Fix the responsible stage. Preserve the upstream license for redistributed reference skin and do not upload model weights, environments or private caches merely because Git was requested.
