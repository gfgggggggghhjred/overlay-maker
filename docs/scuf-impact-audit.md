# SCUF Impact front-preview integration

The supplied `SCUF_Impact_Preview_Quality (1).zip` is a raster layer pack, not a native 3D model. Its working canvas is 2860 × 2200, enlarged 2× from 1430 × 1100 source artwork. The import preserves the supplied neutral pearl finish, material shading, layer origins, control positions and original stick pivots. It does not claim native 2860-pixel render detail.

Original files are retained unchanged in `reference-assets/scuf-impact/`; they are reference material, not instructions to execute. `tools/import-scuf-impact.py` reproduces the app data and records source hashes in `scuf-impact-audit.json`. Manifest recomposition agrees with the supplied assembly to within one channel level (alpha-compositing rounding). The derived app artwork removes detached low-alpha background residue outside a three-pixel antialiasing band around the opaque shell; no opaque shell pixels are removed.

## Supported visualization

- Four face buttons, four D-pad directions including simultaneous diagonals, Share, Options, Home and touchpad click.
- Both movable stick caps and stick clicks. The source sockets, SCUF rim lettering and shell remain stationary. Neutral wells come from the uncapped source layers, avoiding duplicated caps.
- Standard browser-gamepad mapping, independent of the connected controller brand. Touchpad click uses button 17 where exposed; a generic Xbox-style pad cannot supply an additional touchpad input by itself.
- Existing per-button colors, shell customization, effects, presets, saved jobs and self-contained customer HTML use the shared renderer.

## Deliberate limitations

This template is labeled **Front preview** in the gallery and editor. The pack has only two thin shoulder fragments and no complete four-control shoulder set. They remain stationary source artwork; LB/RB/LT/RT are not fabricated or exposed as editable visual surfaces. Rear paddle artwork and independent paddle input are also absent. Physical shoulder/trigger inputs can still be inspected by the existing hardware audit, but are not visualized by this template.

To complete those surfaces, supply individually separated L1, R1, L2 and R2 layers aligned to the same front canvas, plus neutral and full-travel references (or the actual source model). Distinct rear paddles also require artwork and evidence of the input indices or mapped actions exposed by the device. Physical controller, OBS and Streamlabs testing remain manual release checks. The 36-source-pixel visual stick travel is conservative and has not been validated against a device recording.

## Source and use

User-supplied production artwork. The pack contains no public redistribution license or explicit restriction; no new public license is asserted by this integration. Original source notices are preserved. This audit does not independently verify third-party ownership.
