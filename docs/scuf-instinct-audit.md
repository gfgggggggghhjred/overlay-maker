# SCUF Instinct front artwork and branded presets

Source: user-supplied `SCUF_Xbox_Orange_Assets.zip`. The archive supplies 19 aligned RGBA layers, extraction masks, assembly and empty-shell PNGs, a raster-backed SVG and two visual references. No uploaded code is executed. Original files stay unchanged under `reference-assets/scuf-instinct/`.

## What the assets establish

The canvas is 2896 × 2172, enlarged 2× from a 1448 × 1086 native render. The source describes rendered/reconstructed artwork and approximate hidden recesses, not a dimensionally certified mesh or independently validated controller revision. Layer recomposition matches the supplied assembly within one channel level of alpha-compositing rounding. The import removes detached low-alpha background dust while preserving all pixels with alpha at least 128 and the source shoulder edge components. Source hashes and exact pivots are recorded in `scuf-instinct-audit.json`.

Both cap pivots remain `[798,752]` and `[1778,1126]`. Caps are isolated from the fixed orange rings and socket cups. Hidden wells come directly from the supplied uncapped layers, not synthetic fills. Full cap alpha fits its pivot-relative clipping radius. Visual travel is 45 source pixels with direct radial input; it is not a hardware calibration. The segmented D-pad remains one stationary source disc with four mutually exclusive directional masks sharing source pivot `[1112,1164]`; diagonals activate adjacent sectors.

## Inputs and deliberate limits

The template exposes 15 front input visualizations: A/B/X/Y, four D-pad directions, View/Back, Menu/Start, Home, both stick clicks, plus Share/Capture and mic mute previews. Axes follow the existing browser-standard mapping regardless of the physical controller brand.

Only 13 of these button/direction/click signals have established standard mappings. Share/Capture and mute remain **preview-only**, with explicit labels. Button 17 is not assumed to be the Xbox Share button; the existing optional touchpad mapping is unchanged. The green source indicator is static artwork, not controller connection or mute state.

The two shoulder sprites show visible portions only. They do not establish four complete independent LB/RB/LT/RT surfaces or rear paddles, so no such controls are fabricated. The gallery, editor and export panel label this model **Front preview** and describe its limitations. A complete customer-ready model still needs source-aligned individual shoulder/trigger layers, neutral/full-travel references, rear artwork where desired, and actual device input evidence. Physical controller and OBS/Streamlabs acceptance testing remain manual.

## EQDomain and SJD presets

Three gallery options remain independent: stock **Graphite / orange rings**, **EQDomain · gold / cyan**, and **SJD · gold / cyan**. The two requested branded versions use charcoal #3a424b, gold #d7b964 and cyan #30d9ee. Left ring and Home use gold; the segmented D-pad keeps its original gray material; the right ring and utility accents use cyan. Neutral rubber texture and familiar source legends remain. The indicator adopts cyan in the branded artwork without becoming a live status display.

Ring/indicator recoloring selects only colored material, retaining alpha, reflections and geometry. Matching hidden-well patches receive the same treatment, so cap travel cannot reveal an orange seam. Original source artwork is never overwritten. Text uses the included Rajdhani font, gold, on the clear right grip; EQDomain and SJD stay editable through the existing text controls. Palette dictionaries are copied per project. `wordmark` catalog metadata initializes existing project text/font/placement fields and requires no new saved-project format or export runtime.

`tools/import-scuf-instinct.py` regenerates model packages and audit metadata. `tools/capture-scuf-instinct.cjs` generates actual renderer thumbnails and review images with the included font.

## Source notice

User-supplied production resources. No public redistribution license or explicit restrictive license is included; this integration does not assert a new public artwork license or independently verify ownership. Original source notices are retained.

Native legend masks use an optional inset on this model so white control reflections do not become false outlined glyphs when recolored. Existing models omit the option and retain their previous masks. Renderer revision 12 embeds the same optional masking in customer HTML.

Verification suites: `scuf-instinct-test.cjs` covers 15 exposed visual inputs, release, highlight containment, 16 stick directions/clicks, fixed rings, complete cap alpha/pivots, visible source fidelity outside cap patches, anime presets and standalone controller/disconnect behavior. `scuf-instinct-presets-test.cjs` covers both wordmarks, clear control areas, source legend insets, fixed recolored rings, optional-input honesty, selection/save/default/Undo, included-font loading and single-selected-template offline export. Transparent source comparisons use premultiplied visible color plus alpha, avoiding false artwork failures from invisible RGB rounding.

The final source-fidelity check found that restoring a protected translucent socket layer with source-over increased its alpha. Restoration now replaces the masked contribution using complementary alpha, preserving the original socket-edge transparency. The existing shaded DualSense check passes with this correction.
