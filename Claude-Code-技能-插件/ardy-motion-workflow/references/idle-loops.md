# Stationary idle loops and foot contact

Use this route only when the intended action stays in one location with both feet planted. It is unsuitable for footwork, walking, jumps, rolls or airborne attacks. A combat guard can keep open hands when the skeleton cannot close individual fingers; explain that limitation instead of claiming the prompt was fully realized.

Choose a stable generated segment after any initial transition. Judge pose and movement visually; one of three tested “standing guard” candidates traveled several meters sideways despite its text prompt. Preserve the raw sequence.

```powershell
& $ArdyPython "$SkillRoot/scripts/make_loop.py" $SelectedNpz --start 40 --stop 120 --frames 80 --out "$RunDir/processed/idle_loop.npz"
& $ArdyPython "$SkillRoot/scripts/prepare_motion.py" "$RunDir/processed/idle_loop.npz" --out "$RunDir/idle_export" --name CombatIdle_v2 --root-mode fixed --loop
```

`start` is zero-based; `stop` is exclusive. `frames` is the number of unique samples; the output adds a repeated endpoint. At 20 FPS, 80+1 samples span 4 seconds. Do not apply those indices to a shorter input. Reusing the example does not establish that a different clip has the same useful segment.

The helper fits two periodic harmonics to pelvis translation and local rotations in each joint's tangent space around a mean SO(3) rotation. This avoids Euler wraparound at 180°. It then solves both legs to fixed ankle targets, retains fixed foot orientation, and corrects ankle height against the **actual four-weight skinned sole**. Bone lengths remain fixed. Large turns are rejected; unreachable legs fail instead of stretching the mesh. Results are edited animation, not raw model output.

Root translation and rotation must be fixed for in-place idle; body breathing/sway remains in pelvis/spine. Setting a separate root to zero while leaving meters of travel in pelvis does not make a stationary clip. The helper is intended for already stationary candidates.

Run normal export verification and then:

```powershell
& $BlenderExe --background --factory-startup --python-exit-code 1 --python "$SkillRoot/scripts/render_preview.py" -- --artifacts "$RunDir/idle_export" --contact-mode planted
```

The planted check measures both feet's selected sole vertices, horizontal drift and floor height, plus full-mesh loop closure. Bone contact alone is insufficient: a previous clip had stable foot joints while one skin sole penetrated the floor by about 1 cm. Correct the source ankle target; lowering the display floor hides the problem.

Check values and actual frames at the start, quarter, middle, three-quarter and end, plus front/side views and repeated playback. Position closure alone does not prove velocity continuity or natural timing. Keep the duplicate endpoint in FBX for duration, but omit it from looping Blender preview playback. Fitting can attenuate motion; reject an effectively frozen or visibly wrong result even if all invariants pass.
