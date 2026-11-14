# Rendered white Xbox — asset integration and QC

Local candidate: **Xbox · Rendered / White & graphite**. The pack does not identify an exact Xbox hardware revision, so the template does not claim a Series/One/Elite revision. Existing controller artwork is retained in its own families. The gallery candidate contains 29 families / 74 skins.

## Supplied resources

`White_Xbox_Controller_Assets.zip` contains a 2048 × 1664 orthographic front reference, 17 transparent layer PNGs, a neutral layered preview, a measurement/input manifest and a small input-reference HTML page. It contains no editable 3D mesh or scene. The references were inspected as data; the HTML was not executed. Input indices are interpreted through Overlay Studio's existing standard Gamepad mapping.

The layers recompose **pixel-for-pixel** to the supplied layered preview. That preview differs from the full front reference: exported socket meshes reveal portions that the assembled housing should occlude. The physical front reference is therefore the appearance target for the app.

Original files remain unchanged in `reference-assets/xbox-white-render`, outside the shipped app assets. The importer records their SHA-256 hashes and measurements in `xbox-white-render-audit.json`.

## Corrections implemented

- Recovered each visible socket opening from the front reference and body layer. Kept the exposed reference rim fixed, reconstructed the hidden area under the cap and removed baked cap pixels. The large unoccluded socket disks in the supplied layered preview no longer cover the housing.
- Preserved the provided joint pivots, `[531,685]` and `[1277,979]`. They are not the image centers. Cap-fitting radii include every nontransparent cap pixel relative to those pivots; a half-width crop would truncate the lower cap edges.
- Used the reference HTML's 15-source-pixel travel as the visual range, with the existing radial input limit. This is not a claim of physical hardware calibration.
- Preserved the visible bumper/trigger cutouts, excluding later-layer occlusion at mask edges. These components illuminate in place; no hidden shoulder geometry or mechanical travel is invented.
- Added opt-in analog illumination blending over the original shoulder art, so very small trigger values do not pop abruptly into a different material. Neutral/release returns to original artwork.
- Preserved source surface shading without turning its specular highlights into noisy contrasting ink. Kept the original ABXY legend colors. The Xbox emblem uses a separate bright-mark mask and background sampling for legibility during activation.
- Corrected effect anchoring for attached triggers. RT comic effects use the real RT bounds rather than the default detached-trigger location. Existing floating-trigger bounds retain priority.
- Kept the original white housing, graphite shoulders/sticks and colored face legends as a coordinated finish. Added no monochrome default color variants. Existing per-part colors, logos/text, patterns, finishes, textures, themes and input effects remain available.
- Used the common lazy-loaded model pack, gallery, saved-job and standalone customer export systems. Customer output has no remote asset, reference-HTML or editor dependency.

## Verification

`xbox-render-test.cjs` checks all 17 visual inputs, highlight alpha, seven trigger depths including 0.5% onset, exact release, 16 stick directions/clicks, pivot preservation, complete cap coverage, fixed visible rim samples, exposed-recess white-gap checks, Xbox emblem contrast, attached RT effect bounds, all 18 anime themes, gallery selection, per-part settings restoration and self-contained customer export.

The neutral output has **zero significant changed pixels outside reconstructed cap footprints** compared with the fitted front-reference image. This is measured with an 8-level channel tolerance. Cap surfaces can differ slightly from the full render because the supplied isolated cap render has slightly different lighting.

The existing DualSense and Controller Layer Pack suites pass after the shared renderer changes. The complete local regression run passed **35/35 suites**; the syntax check passed **124 JavaScript files**. Windows packaging/target verification still follows reuse confirmation. Test controllers are simulated; these tests do not count as physical-controller verification in the production workflow.

[Neutral and simultaneous-input preview](xbox-white-render-review.jpg)

## Remaining checks and rights

The archive README explicitly says it includes no license or reuse grant. Commercial modification/redistribution confirmation for this Xbox pack is pending; the earlier DualSense confirmation does not establish rights to this separate artwork. Publication is on hold pending that factual confirmation.

A real-controller recording was not supplied. Home availability, full travel, pressure values, driver mapping and OBS/Streamlabs background input need target-machine acceptance testing. Shoulder cutouts cannot support accurate hidden-surface or mechanical animations without additional source artwork/geometry.

## Build metadata QC

The version-bump audit found that previous text replacement had also changed Node engine constraints in transitive lockfile entries. Those records now match the original dependency lock exactly; only the application package fields carry version 0.19.0. No dependency upgrade was introduced.

A standalone **internal** preview is prepared at `release/Xbox-Rendered-Internal-Preview.html`. It embeds the current renderer and assets for operator review. It is not a published customer handoff.

The managed QA browser rejects direct `file://` navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. That optional file-opening check could not be completed; no bypass was attempted. The embedded customer HTML passed rendering/export checks in the existing browser test context. Local-file opening and real-controller behavior still need verification on the operator’s Windows browser.
