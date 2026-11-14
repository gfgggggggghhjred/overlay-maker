"""Import user-supplied SCUF front layers; no source scripts are executed.
The preview contains no complete shoulder/trigger geometry or native 3D file.
Original resources stay unmodified in reference-assets/scuf-impact.
"""
from pathlib import Path
import base64, hashlib, io, json
import numpy as np
from PIL import Image
from scipy import ndimage
from raster_paths import mask_path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'reference-assets/scuf-impact'
MODEL = 'ScufImpactRender'
spec = json.loads((SOURCE / 'alignment.json').read_text())
W, H = spec['canvas']['width'], spec['canvas']['height']
assert (W, H) == (2860, 2200)
rows = {row['id']: row for row in spec['layers']}
images, hashes = {}, {}
for name in spec['layerOrder']:
    file = (SOURCE / rows[name]['file']).resolve()
    assert file.is_relative_to(SOURCE.resolve())
    images[name] = Image.open(file).convert('RGBA')
    assert images[name].size == (W, H)
    hashes[rows[name]['file']] = hashlib.sha256(file.read_bytes()).hexdigest()

def url(im):
    buffer = io.BytesIO()
    im.save(buffer, format='PNG')
    return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

original = Image.new('RGBA', (W, H))
for name in spec['layerOrder']:
    original.alpha_composite(images[name])
error = np.abs(np.array(original).astype(int) - np.array(Image.open(SOURCE / 'Assembled_Controller.png')).astype(int))
assert error.max() <= 1, 'Supplied assembly does not match the layer manifest'
# Retain the continuous silhouette and its antialiased boundary, removing only
# low-alpha detached background residue. Never change RGB or opaque geometry.
body = np.array(images['body'])
labels, _ = ndimage.label(body[:, :, 3] >= 32)
sizes = np.bincount(labels.ravel()); sizes[0] = 0
keep = ndimage.binary_dilation(labels == sizes.argmax(), iterations=3)
removed = int(((body[:, :, 3] > 0) & ~keep).sum())
assert not np.any((body[:, :, 3] >= 32) & ~keep)
body[~keep] = 0
images['body'] = Image.fromarray(body)

front, fixed = Image.new('RGBA', (W, H)), Image.new('RGBA', (W, H))
for name in spec['layerOrder']:
    front.alpha_composite(images[name])
    if name not in ['stick_left_cap', 'stick_right_cap']:
        fixed.alpha_composite(images[name])

mapping = {'button_south': 'A', 'button_east': 'B', 'button_west': 'X', 'button_north': 'Y',
           'button_share': 'Share', 'button_options': 'Options', 'button_home': 'Home', 'touchpad': 'Touchpad',
           **{'dpad_' + d.lower(): 'DPad_' + d for d in ['Up', 'Down', 'Left', 'Right']}}
controls = []
for name, key in mapping.items():
    x, y, right, bottom = images[name].getbbox()
    pixels = np.array(images[name].crop((x, y, right, bottom)))
    mask = pixels[:, :, 3] >= 128
    normal = '#' + ''.join(f'{int(v):02x}' for v in np.median(pixels[:, :, :3][mask], axis=0))
    controls.append({'key': key, 'tag': 'path', 'attrs': {'d': mask_path(mask)},
                     'matrix': [1, 0, 0, 1, x, y], 'bounds': [x, y, right-x, bottom-y],
                     'fillRule': 'evenodd', 'floating': False, 'normal': normal,
                     'layeredMaterial': True, 'surfaceOnly': True})
layers, sticks = {}, []
for side in ['left', 'right']:
    name = 'stick_' + side + '_cap'
    x, y, right, bottom = images[name].getbbox()
    px, py = rows[name]['pivot']
    cap = images[name].crop((x, y, right, bottom))
    ys, xs = np.nonzero(np.array(cap)[:, :, 3] > 0)
    radius = float(np.hypot(xs+x+.5-px, ys+y+.5-py).max()+2)
    cap_key, well_key = side+'Cap', side+'Well'
    layers[cap_key], layers[well_key] = url(cap), url(fixed.crop((x, y, right, bottom)))
    # Socket and lettering remain in the fixed artwork. These points lie outside
    # the cap's entire permitted travel, for regression checks of the static rim.
    samples = [[px+220*np.cos(a), py+220*np.sin(a)] for a in np.arange(16)*np.pi/8]
    sticks.append({'center': [px, py], 'capRadius': radius, 'rimRadius': 245, 'travel': 36,
                   'capImage': cap_key, 'wellImage': well_key, 'layerBounds': [x, y, right-x, bottom-y],
                   'rimSamples': samples})
x, y, right, bottom = front.getbbox()
record = {'name': 'Original pearl · front preview', 'width': W, 'height': H, 'cover': url(front), 'modelLayers': layers,
          'modelGeometry': {'sourceWidth': W, 'sourceHeight': H, 'bodyBounds': [x, y, right-x, bottom-y],
                            'controls': controls, 'sticks': sticks, 'protectedShapes': [], 'floatArtwork': True,
                            'layered': True, 'analogOverlay': True, 'spatialRemap': 'canonical-positions'},
          'source': {'pack': 'SCUF_Impact_Preview_Quality (1).zip', 'sourceResolution': spec['sourceResolution'],
                     'exportScale': spec['exportScale'], 'inputVerified': False,
                     'limitations': 'Front artwork only. No complete LB/RB/LT/RT or rear paddle assets. Visual stick travel requires physical validation.'}}
(ROOT/'app/controller-data'/f'{MODEL}.js').write_text('// Supplied SCUF front artwork; see docs/scuf-impact-audit.md.\nCONTROLLER_PACKS['+json.dumps(MODEL)+']='+json.dumps({'Pearl': record}, separators=(',', ':'))+';\n')
folder = ROOT/'app/controller-thumbnails'/MODEL
folder.mkdir(parents=True, exist_ok=True)
thumb = front.copy(); thumb.thumbnail((400, 297)); thumb.save(folder/'Pearl.png')
path = ROOT/'app/controller-catalog.js'
catalog = json.loads(path.read_text().split('const CONTROLLER_CATALOG=')[1].strip().rstrip(';'))
catalog = [m for m in catalog if m['id'] != MODEL]
catalog.append({'id': MODEL, 'name': 'SCUF Impact · Front preview', 'collection': 'Rendered controllers',
                'defaultVariant': 'Pearl',
                'supportNote': 'Front preview: bumpers, triggers and rear paddles are not visualized. Complete shoulder artwork is still needed. Touchpad click requires browser button 17.',
                'variants': [{'id': 'Pearl', 'name': record['name'], 'thumbnail': f'controller-thumbnails/{MODEL}/Pearl.png',
                              'controls': sorted(set(mapping.values()) | {'LSB', 'RSB'}),
                              'labels': {'A': 'Cross / Bottom', 'B': 'Circle / Right', 'X': 'Square / Left', 'Y': 'Triangle / Top', 'Home': 'SCUF / Home'}}]})
path.write_text('// Visual templates are independent of the connected input device.\nconst CONTROLLER_CATALOG='+json.dumps(catalog, separators=(',', ':'))+';\n')
(ROOT/'docs/scuf-impact-audit.json').write_text(json.dumps({'sourceCanvas': [W, H], 'sourceResolution': spec['sourceResolution'],
    'compositionMaximumRoundingError': int(error.max()), 'detachedLowAlphaPixelsRemoved': removed,
    'controls': list(mapping.values()), 'hashes': hashes, 'sticks': sticks,
    'missingVisualControls': ['LB', 'RB', 'LT', 'RT', 'rear paddles'], 'hardwareVerified': False}, indent=2)+'\n')
print(f'Prepared independent SCUF front preview: {len(controls)} button surfaces, two sticks; removed {removed} detached low-alpha pixels.')
