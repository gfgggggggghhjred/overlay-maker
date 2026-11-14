SCUF IMPACT — APPROVED-PREVIEW QUALITY EDITION

This replaces the earlier low-resolution-reference asset pack.
The shell, socket rings, recessed wells and visible shoulder fragments are
extracted directly from the selected approved preview. The face controls,
D-pad, thumbstick caps, menu buttons, home button and touchpad are newly rendered
to match that preview. No controls from the previous low-resolution pack are
reused.

FILES
Approved_Preview_Original.png — your exact selected preview, unchanged.
Assembled_Controller.png — assembled from the actual delivered layers.
layers/ — 19 transparent aligned PNG layers.
SCUF_Impact_Layers.svg — named editable raster-backed layer stack.
alignment.json — canvas size, drawing order and per-layer pivot coordinates.
masks/ — editable vector extraction contours, not vectorized controller art.

IMPORT
Every working PNG is 2860 x 2200. Place every layer at (0,0), without trimming
or independently centering parts. The controller is about 2500 pixels wide.
The source rendering is 1430 x 1100; exports are 2x Lanczos enlargements of that
higher-quality artwork, not native 2860-pixel renders. The original approved
preview retains its original dimensions and exact bytes.
Open the SVG in Inkscape while keeping the layers/ folder beside it. Its layers
reference the PNGs, so the SVG is not standalone and is not pure vector artwork.
JSON coordinates are full-canvas pixels with a top-left origin.

LAYER CONTENTS
Body; two sockets/rings; two thumbstick caps; four D-pad directions; four face
buttons; Share; Options; Home; touchpad; two visible shoulder-edge fragments.
Keep body, rings and sockets stationary while moving only the stick caps.
The original preview has empty sockets, so no old stick artwork remains below
the movable caps. Preserve the supplied draw order for correct assembly.

SCOPE
The visible shoulder fragments are not four complete L1/R1/L2/R2 controls.
Full shoulder/trigger geometry still requires clear additional views or the
source model. Movement limits, timing and input mapping remain unverified
without an input recording and a test in the consuming engine.
Static layer alignment, transparency and assembly were checked. This package
is artwork, not a new controller engine. No reuse-permission statement was
provided; this pack does not establish third-party rights.
