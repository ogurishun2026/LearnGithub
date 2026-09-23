# Portable conversion and Blender export

The scripts require an interpreter with ARDY, NumPy and SciPy installed. Blender scripts run with Blender's Python. Model weights are unnecessary when only converting a saved NPZ, but the installed Core27 skeleton and `skin_standard.npz` are required. Other skeletons (G1, SOMA, custom rigs) need a separate mapping and validation.

Use an empty output directory. Names must be simple ASCII slugs; user-facing labels may be Chinese in the report.

```powershell
# A moving, non-looping clip:
& $ArdyPython "$SkillRoot/scripts/prepare_motion.py" $WalkNpz --out "$RunDir/walk_export" --name Walk_v2 --root-mode planar
# A previously looped stationary clip, including one duplicate endpoint:
& $ArdyPython "$SkillRoot/scripts/prepare_motion.py" $IdleLoopNpz --out "$RunDir/idle_export" --name CombatIdle_v2 --root-mode fixed --loop

# Repeat these for the chosen output directory.
& $BlenderExe --background --factory-startup --python-exit-code 1 --python "$SkillRoot/scripts/build_blender.py" -- --artifacts $ExportDir
& $BlenderExe --background --factory-startup --python-exit-code 1 --python "$SkillRoot/scripts/verify_exports.py" -- --artifacts $ExportDir
& $BlenderExe --background --factory-startup --python-exit-code 1 --python "$SkillRoot/scripts/render_preview.py" -- --artifacts $ExportDir --contact-mode observe
```

`motion.json` carries the name, frames, FPS, root policy and explicit loop flag to the next stages. It removes the old demo's fixed 40/81-frame limits and CombatIdle filenames. Generated artifacts:

- `<name>.blend`: source reference skin with its own Action.
- `<name>.bvh`: Core27 animation, centimeter coordinate values.
- `SK_ARDY_Core28.fbx`: reference mesh and source Skeleton, no animation.
- `AN_<name>.fbx`: animation plus reference skin/bind matrices.
- `source_reference.npz`: conversion verification fixture with upstream skin; normally keep local.
- `blender-report.json`, `saved-export-report.json`, optional `mesh-contact-report.json`, previews.
- `LICENSE-ARDY.txt`, `NOTICE.txt`: carry upstream attribution with redistributed reference-skin artifacts.

Build scripts create their own scene in a fresh background process. Do not load over the user's unsaved interactive Blender scene. Existing global actions and other project assets are not inputs to these scripts.

In an existing meter-based Blender scene, BVH import Scale=.01, Forward=-Z, Up=Y, source FPS; in a centimeter-coordinate scene, Scale=1. Enable/install the BioVision importer if absent. Reset the frame range after import: the tested importer added an extra inclusive endpoint. A BVH is a bone animation, not automatic retargeting to another rig.

Weight pruning retains the four largest influences and normalizes. The reference skin's 18 five-influence vertices changed by about 2.5–2.6 mm in the two tested motions. The build rejects more than 1 cm sampled skin deviation as gross mismatch; that bound is not a visual-quality acceptance claim.

Preview conversion example (FFmpeg must be installed; use actual FPS):

```powershell
ffmpeg -framerate 20 -start_number 1 -i "$ExportDir/preview-frames/%04d.png" -c:v libx264 -crf 19 -pix_fmt yuv420p -movflags +faststart "$ExportDir/preview.mp4"
```

Scripts are intended for the reference human. Camera framing is estimated from root travel; review/correct it for unusual height, floor moves or fast motion. Ground/contact assumptions do not transfer automatically to a different character.
