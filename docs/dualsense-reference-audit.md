# DualSense shaded template — 0.18

Added **DualSense · Shaded / Dark** as an independent starting template. The gallery now has 28 visual families / 71 skins. Existing templates retain their identity, and retired Xelu models remain removed. The visual template can be driven by any browser-standard gamepad; selecting it does not change input-device selection or remap existing controls.

## Source audit

Reference: https://github.com/Hammy18/dualsense_overlay at `8ce4d80bf4260c7d3ccdea5469ec0651403579d1`. It is a fork of https://github.com/philipbry/dualsense_overlay. The fork contains README and CSS; the original repository contains a README. Neither repository nor the image host advertises a public license. **The user confirmed commercial customization/redistribution permission on 2026-11-14.** Attribution and that confirmation ship in `app/licenses/dualsense-artwork.txt`; this is not a claim of a public open-source license.

The CSS is an adapter for Gamepad Viewer's DS4 DOM. It is not a standalone input engine. It relies on eight PNGs at philipbry.github.io. Its README's alternate mapping reports a D-pad limitation and needs a separate virtual-controller configuration. That mapping is not imported. Static images and measured layout are adapted into Overlay Studio's existing universal input/rendering/export pipeline; upstream scripts and instructions are not executed.

The original source files, image hashes and dimensions are retained outside the shipped app under `reference-assets/dualsense-hammy18`. `tools/import-dualsense-reference.py` reproducibly generates the template pack and thumbnail from those images. `docs/dualsense-sprite-audit.json` records measurements and provenance. No asset from this template is mixed into another controller family.

## Implemented

- Original 794 × 639 dark housing and pink accents; original shell geometry, uniformly fitted to the shared output canvas.
- Separate 95px source caps over fixed source socket backgrounds. Radial travel is explicitly limited to 12 source pixels. That is a visual limit, not an upstream calibration value; the CSS does not supply one.
- Four source-alpha face-button shapes, all D-pad directions/diagonals, Create/Options, mirrored bumpers, independent analog triggers, physical PS emblem, touchpad and mute preview.
- Shared button-17 input provides **touchpad click when exposed by the browser**. Touch coordinates/gestures are not available through this mapping. Microphone mute is clearly marked **preview only**; no unsupported physical signal is invented.
- An optional button-17 press/release check is included in physical-input verification when the connected device exposes it. Required coverage is unchanged.
- Per-part and shell recoloring preserves source shading. A model-specific tone range prevents very dark source art from becoming flat color blocks. Shading detail is retained directly instead of converting photographic highlights into bright glyph outlines. Other families retain their original material path.
- Highlight compositing respects the alpha of supplied floating artwork; synthetic triggers without supplied floating art retain their existing rendering path.
- Existing artwork/text, dragging/placement, saved jobs, textures, patterns, finishes, input effects and all 18 anime presets use the existing common painter. PS-shaped Home artwork remains clipped to the physical PS silhouette, so detailed circular emblems have less room than on a round Home button.
- Customer HTML embeds the model and its layers. No Gamepad Viewer, remote CSS, image host, editor process or local bridge is required by the customer export.

## Verification

`dualsense-template-test.cjs` verifies gallery/apply/restore, 19 visual inputs, optional touchpad and preview-only mute, clean highlight alpha, exact release, five trigger depths, 16 stick directions/clicks, visible fixed rims, recolors, all 18 anime presets and standalone customer HTML with zero external asset requests. The existing input, layered-pack, retired-model, production and UI suites cover regression behavior. Release checks also compare packaged assets with tested files.

[Source appearance and input/recolor previews](dualsense-shaded-review.jpg)

## Limits requiring target review

The source raster is 794 × 639, with 54px face buttons and 95px sticks. It reads well at typical OBS sizes; large upscaling does not add real detail. Bright recolors can expose tonal steps already present in the dark 8-bit original. High-resolution layered originals would improve this ceiling. The source has blank face buttons rather than printed PlayStation symbols, which are deliberately retained.

Physical DualSense hardware, Home/touchpad availability on specific drivers, OBS/Streamlabs background input and target-GPU performance still require manual testing. The template does not implement adaptive-trigger force, touch gestures, haptics or a microphone-mute protocol.
