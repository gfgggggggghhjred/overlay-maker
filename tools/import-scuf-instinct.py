"""Import aligned, user-supplied Instinct front artwork as data, not code.
No native 3D mesh, verified shoulder geometry or hardware mapping is supplied.
"""
from pathlib import Path
import base64, hashlib, io, json
import numpy as np
from PIL import Image
from scipy import ndimage
from raster_paths import mask_path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'reference-assets/scuf-instinct'
MODEL = 'ScufInstinctRender'
spec = json.loads((SOURCE / 'alignment.json').read_text())
W, H = spec['canvas']['width'], spec['canvas']['height']
assert (W, H) == (2896, 2172)
rows = {r['id']: r for r in spec['layers']}
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

assembled = Image.new('RGBA', (W, H))
for name in spec['layerOrder']:
    assembled.alpha_composite(images[name])
error = np.abs(np.array(assembled).astype(int) - np.array(Image.open(SOURCE/'Assembled_Controller.png')).astype(int))
assert error.max() <= 1, 'Layer order must reproduce the supplied assembly'
# Preserve the continuous body and its antialiasing, including detached shoulder
# edge pixels covered by the actual shoulder sprites. Remove only background dust.
body = np.array(images['body'])
keep = ndimage.binary_dilation(body[:, :, 3] >= 32, iterations=3)
for name in ['shoulder_left_visible', 'shoulder_right_visible']:
    keep |= np.array(images[name])[:, :, 3] > 0
removed = int(((body[:, :, 3] > 0) & ~keep).sum())
assert not np.any((body[:, :, 3] >= 128) & ~keep), 'Do not remove opaque source art'
body[~keep] = 0
images['body'] = Image.fromarray(body)
front, fixed = Image.new('RGBA', (W, H)), Image.new('RGBA', (W, H))
for name in spec['layerOrder']:
    front.alpha_composite(images[name])
    if name not in ['stick_left_cap', 'stick_right_cap']:
        fixed.alpha_composite(images[name])

def contour(name, mask=None):
    x, y, right, bottom = images[name].getbbox()
    pixels = np.array(images[name].crop((x, y, right, bottom)))
    visible = pixels[:, :, 3] >= 128
    if mask is not None:
        visible &= mask
    return {'tag': 'path', 'attrs': {'d': mask_path(visible)}, 'matrix': [1, 0, 0, 1, x, y],
            'bounds': [x, y, right-x, bottom-y], 'fillRule': 'evenodd'}

mapping = {**{'button_'+k: k for k in ['A', 'B', 'X', 'Y']}, 'button_view': 'Share',
           'button_menu': 'Options', 'button_home': 'Home', 'button_share': 'Capture', 'button_mute': 'M'}
controls = []
for name, key in mapping.items():
    shape = contour(name)
    controls.append({**shape, 'key': key, 'floating': False, 'normal': '#303236',
                     'layeredMaterial': True, 'surfaceOnly': False, 'inkInset': .92 if key=='Home' else .76})
# One stationary source disc; directional masks share the exact source pivot.
x, y, right, bottom = images['dpad_disc'].getbbox()
cx, cy = rows['dpad_disc']['pivot']
yy, xx = np.indices((bottom-y, right-x)); dx, dy = xx+x+.5-cx, yy+y+.5-cy
for direction, sector in [('Up', (dy<0)&(abs(dy)>=abs(dx))), ('Down', (dy>=0)&(abs(dy)>=abs(dx))),
                          ('Left', (dx<0)&(abs(dx)>abs(dy))), ('Right', (dx>=0)&(abs(dx)>abs(dy)))]:
    controls.append({**contour('dpad_disc', sector), 'key': 'DPad_'+direction, 'floating': False,
                     'normal': '#46484a', 'layeredMaterial': True, 'surfaceOnly': True})

layers, sticks = {}, []
for side in ['left', 'right']:
    name = 'stick_'+side+'_cap'
    x, y, right, bottom = images[name].getbbox()
    px, py = rows[name]['pivot']
    cap = images[name].crop((x, y, right, bottom))
    ys, xs = np.nonzero(np.array(cap)[:, :, 3] > 0)
    radius = float(np.hypot(xs+x+.5-px, ys+y+.5-py).max()+2)
    cap_key, well_key = side+'Cap', side+'Well'
    layers[cap_key] = url(cap)
    layers[well_key] = url(fixed.crop((x, y, right, bottom)))
    # Trace the visible fixed socket's actual alpha, rather than inventing a rim.
    socket = np.array(images['stick_'+side+'_socket'])[:, :, 3] >= 128
    sy, sx = np.nonzero(ndimage.binary_erosion(socket, iterations=4))
    distances = np.hypot(sx+.5-px, sy+.5-py)
    points = np.column_stack((sx[distances>182]+.5, sy[distances>182]+.5))
    samples = points[::max(1, len(points)//40)].tolist()
    rim = float(np.hypot(sx+.5-px, sy+.5-py).max()+4)
    sticks.append({'center': [px, py], 'capRadius': radius, 'rimRadius': rim, 'travel': 45,
                   'capImage': cap_key, 'wellImage': well_key, 'layerBounds': [x, y, right-x, bottom-y],
                   'rimSamples': samples})
protected = []
for name in ['stick_left_socket', 'stick_right_socket', 'dpad_socket', 'indicator_green']:
    protected.append({**contour(name), 'preserveColor': True})
x, y, right, bottom = front.getbbox()
record = {'name': 'Graphite / orange rings', 'width': W, 'height': H, 'cover': url(front), 'modelLayers': layers,
          'modelGeometry': {'sourceWidth': W, 'sourceHeight': H, 'bodyBounds': [x, y, right-x, bottom-y],
                            'controls': controls, 'sticks': sticks, 'protectedShapes': protected,
                            'floatArtwork': True, 'layered': True, 'analogOverlay': True,
                            'spatialRemap': 'canonical-positions'},
          'source': {'pack': 'SCUF_Xbox_Orange_Assets.zip', 'nativeRender': spec['nativeRender'],
                     'exportScale': spec['exportScale'], 'physicalInputVerified': False,
                     'limitations': 'Rendered/reconstructed front artwork; not dimensionally certified. No complete LB/RB/LT/RT or rear controls. Capture/mute are preview-only. LED is source artwork, not connection state.'}}
def branded_colors(image):
    pixels = np.array(image).copy()
    for name, color in [('stick_left_socket', '#d7b964'), ('stick_right_socket', '#30d9ee'), ('indicator_green', '#30d9ee')]:
        x, y, right, bottom = images[name].getbbox()
        region = pixels[y:bottom, x:right]
        rgb = region[:, :, :3].astype(float)
        # Select only the colored material, preserving white reflections, gray
        # rubber, alpha and all source geometry. Both front and hidden wells use
        # the same treatment so moving caps never reveal the stock orange again.
        if name == 'indicator_green':
            selected = (rgb[:, :, 1] > rgb[:, :, 0]*1.3) & (rgb[:, :, 1] > rgb[:, :, 2]*1.3)
        else:
            selected = (rgb[:, :, 0] > rgb[:, :, 1]*1.08) & (rgb[:, :, 1] > rgb[:, :, 2]*1.5) & (rgb[:, :, 0]-rgb[:, :, 2] > 50)
        target = np.array([int(color[i:i+2],16) for i in [1,3,5]])
        value = rgb.max(axis=2)/255
        region[:, :, :3][selected] = np.rint(value[:, :, None]*target)[selected]
    return Image.fromarray(pixels)

brand_front, brand_fixed = branded_colors(front), branded_colors(fixed)
brand_layers = dict(layers)
for side, stick in zip(['left','right'], sticks):
    x, y, w, h = stick['layerBounds']
    brand_layers[side+'Well'] = url(brand_fixed.crop((x,y,x+w,y+h)))
brand_palette = {'baseColor': '#3a424b', 'buttonBaseColor': '#ffffff', 'accent': '#d7b964', 'pressed': '#30d9ee',
    'buttonColors': {
        'LSB': {'rest': '#ffffff', 'pressed': '#d7b964'}, 'RSB': {'rest': '#ffffff', 'pressed': '#30d9ee'},
        'Home': {'rest': '#d7b964', 'pressed': '#f4d98a'},
        **{key: {'rest': '#245360', 'pressed': '#53e7f5'} for key in ['Share','Options','Capture','M']}}}
pack = {'Orange': record}
for brand in ['EQDomain','SJD']:
    pack[brand] = {**record, 'name': brand+' · gold / cyan', 'cover': url(brand_front), 'modelLayers': brand_layers}
(ROOT/'app/controller-data'/f'{MODEL}.js').write_text('// User-supplied Instinct front artwork; docs/scuf-instinct-audit.md.\nCONTROLLER_PACKS['+json.dumps(MODEL)+']='+json.dumps(pack, separators=(',', ':'))+';\n')
folder = ROOT/'app/controller-thumbnails'/MODEL
folder.mkdir(parents=True, exist_ok=True)
thumb = front.copy(); thumb.thumbnail((400, 297)); thumb.save(folder/'Orange.png')
path = ROOT/'app/controller-catalog.js'
catalog = json.loads(path.read_text().split('const CONTROLLER_CATALOG=')[1].strip().rstrip(';'))
index = next((i for i, m in enumerate(catalog) if m['id']==MODEL), len(catalog))
catalog = [m for m in catalog if m['id']!=MODEL]
variants = [{'id': 'Orange', 'name': record['name'], 'thumbnail': f'controller-thumbnails/{MODEL}/Orange.png',
        'controls': sorted({c['key'] for c in controls}|{'LSB','RSB'}),
        'labels': {'Home': 'Xbox / Home', 'Share': 'View / Back', 'Options': 'Menu / Start',
                   'Capture': 'Share / Capture (preview only)', 'M': 'Mic mute (preview only)'},
        'palette': {'baseColor': '#ffffff', 'buttonBaseColor': '#ffffff', 'accent': '#ff9d20', 'pressed': '#ffad36'}}]
for brand in ['EQDomain','SJD']:
    variants.append({**variants[0], 'id': brand, 'name': pack[brand]['name'],
        'thumbnail': f'controller-thumbnails/{MODEL}/{brand}.png', 'palette': brand_palette,
        'wordmark': {'text': brand, 'size': 240, 'x': 1260, 'y': 635, 'angle': 35,
                     'fontFamily': 'Rajdhani', 'fontWeight': 700, 'fontItalic': False}})
catalog.insert(index, {'id': MODEL, 'name': 'SCUF Instinct · Front preview', 'collection': 'Rendered controllers',
    'defaultVariant': 'Orange',
    'supportNote': 'Front preview: bumpers, triggers and rear paddles are not visualized. Share/Capture and mute are preview-only. The green indicator is artwork, not connection status.',
    'variants': variants})
path.write_text('// Visual templates are independent of the connected input device.\nconst CONTROLLER_CATALOG='+json.dumps(catalog, separators=(',', ':'))+';\n')
(ROOT/'docs/scuf-instinct-audit.json').write_text(json.dumps({'canvas': [W,H], 'nativeRender': spec['nativeRender'],
    'compositionMaximumRoundingError': int(error.max()), 'backgroundPixelsRemoved': removed, 'hashes': hashes,
    'controls': [c['key'] for c in controls], 'sticks': sticks, 'dpadPivot': rows['dpad_disc']['pivot'],
    'missingVisualControls': ['LB','RB','LT','RT','rear paddles'], 'previewOnly': ['Capture','M'],
    'physicalInputVerified': False}, indent=2)+'\n')
print(f'Prepared SCUF Instinct front preview: {len(controls)} source surfaces, two independent caps, fixed orange rings and explicit input limits.')
