"""Build the DualSense template from audited image sprites; no upstream code runs.
The user confirmed commercial customization/redistribution permission on 2026-11-14.
Run from any directory. Source image hashes and CSS measurements are recorded.
"""
from pathlib import Path
import base64, hashlib, io, json
import numpy as np
from PIL import Image, ImageDraw
from raster_paths import mask_path

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'reference-assets/dualsense-hammy18'
MODEL='DualSenseShaded'
for entry in json.loads((SOURCE/'assets-audit.json').read_text()):
    assert hashlib.sha256((SOURCE/entry['file']).read_bytes()).hexdigest()==entry['sha256'], 'Reference image changed: '+entry['file']
def png(im):
    out=io.BytesIO();im.save(out,format='PNG');return 'data:image/png;base64,'+base64.b64encode(out.getvalue()).decode()
def image(name): return Image.open(SOURCE/name).convert('RGBA')
cover=image('ZDjUbh0.png');controls=[];layers={};measured=[]
def control(key,im,x,y,floating=False,preserve=False):
    mask=np.array(im)[:,:,3]>=128;ys,xs=np.nonzero(mask)
    controls.append({'key':key,'tag':'path','attrs':{'d':mask_path(mask)},'matrix':[1,0,0,1,x,y],
        'bounds':[int(x+xs.min()),int(y+ys.min()),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)],
        'fillRule':'evenodd','floating':floating,'normal':'#282828','layeredMaterial':True,'preserveColorInk':preserve})
    measured.append({'key':key,'position':[x,y],'size':list(im.size),'shape':'source alpha >= 128'})
faces=image('HdHbA0t.png')
for key,sx,x,y in [('A',0,618,268),('B',54,677,211),('X',108,559,210),('Y',162,618,152)]:
    control(key,faces.crop((sx,0,sx+54,54)),x,y)
dpad=image('548MWGT.png')
for key,rect,x,y in [('Up',(0,0,44,58),127,171),('Down',(44,0,88,58),127,246),('Left',(88,0,145,44),82,216),('Right',(144,0,201,44),157,215)]:
    control('DPad_'+key,dpad.crop(rect),x,y)
arrows=image('PrAfLDQ.png')
control('Share',arrows.crop((0,0,23,37)),200,132)
control('Options',arrows.crop((23,0,46,37)),572,132)
bumper=image('wijYAzG.png');control('LB',bumper,90,98);control('RB',bumper.transpose(Image.Transpose.FLIP_LEFT_RIGHT),590,98)
triggers=image('KcAyIZw.png')
control('LT',triggers.crop((0,0,100,97)),100,0,True)
control('RT',triggers.crop((100,0,200,97)),593,0,True)
control('Touchpad',image('Gnd106J.png'),237,97,preserve=True)
# The physical PS button follows its raised emblem, not an invented circular button.
home_path='M18 0C25 1 34 4 36 9 39 13 39 21 35 24 32 26 29 25 27 24V11C27 9 24 8 24 11V42L18 40Z M15 24L5 28C-2 31-2 36 5 39 8 40 13 41 17 40V34C13 35 9 34 8 33 7 31 11 30 15 29Z M27 29C34 26 39 26 43 29 47 33 40 36 27 41V36L36 32C41 30 37 29 34 30L27 33Z'
controls.append({'key':'Home','tag':'path','attrs':{'d':home_path},'matrix':[1,0,0,1,374,318],'bounds':[374,318,45,48],'fillRule':'nonzero','floating':False,'normal':'#282828','layeredMaterial':True})
measured.append({'key':'Home','position':[374,318],'size':[45,48],'shape':'Curved mask following the raised PS emblem; retains its interior cutouts.'})
mute=Image.new('RGBA',(40,15));ImageDraw.Draw(mute).rounded_rectangle((0,0,39,14),radius=6,fill='white');control('M',mute,377,384)
sticks=[];cap=image('3sBwghP.png').crop((0,0,95,95))
for name,x in [('ls',222),('rs',477)]:
    layers[name+'Cap']=png(cap);layers[name+'Well']=png(cover.crop((x,294,x+95,389)))
    sticks.append({'center':[x+47.5,341.5],'capRadius':47.5,'rimRadius':51,'travel':12,
        'capImage':name+'Cap','wellImage':name+'Well','layerBounds':[x,294,95,95]})
thumbnail=cover.copy()
for x in [222,477]:thumbnail.alpha_composite(cap,(x,294))
thumbdir=ROOT/'app/controller-thumbnails'/MODEL;thumbdir.mkdir(parents=True,exist_ok=True)
thumbnail.thumbnail((400,350));thumbnail.save(thumbdir/'Dark.png')
geometry={'sourceWidth':794,'sourceHeight':639,'bodyBounds':[0,98,794,541],'controls':controls,'sticks':sticks,
    'protectedShapes':[],'floatArtwork':True,'layered':True,'materialRange':[3,65],'spatialRemap':'canonical-positions'}
provenance={'repository':'https://github.com/Hammy18/dualsense_overlay','commit':'8ce4d80bf4260c7d3ccdea5469ec0651403579d1',
    'upstream':'https://github.com/philipbry/dualsense_overlay','imageHost':'https://philipbry.github.io/',
    'permission':'User confirmed commercial customization and redistribution permission on 2026-11-14; upstream has no public license file.',
    'originalSHA256':hashlib.sha256((SOURCE/'ZDjUbh0.png').read_bytes()).hexdigest()}
core={'tag':'path','attrs':{'d':'M238 98Q397 85 556 98L558 258C585 282 594 315 588 350 584 392 570 430 536 439H258C224 430 210 392 206 350 200 315 209 282 236 258Z'},'matrix':[1,0,0,1,0,0],'preserveColor':True,'restoreSourceOnly':True}
labels={'A':'Cross / bottom face','B':'Circle / right face','X':'Square / left face','Y':'Triangle / top face','Share':'Create','Options':'Options','Home':'PS / Home','Touchpad':'Touchpad click (if exposed)','M':'Microphone mute (preview only)'}
def palette(shell,buttons,accent,rest):return {'baseColor':shell,'buttonBaseColor':buttons,'accent':accent,'pressed':accent,'buttonColors':{key:{'rest':color} for key,color in rest.items()}}
finishes=[('Dark','Original dark / rose',palette('#ffffff','#ffffff','#df4ba8',{})),
 ('Pearl','Pearl / charcoal',palette('#f3f0e8','#30343e','#de76ad',{'Touchpad':'#252b33','LT':'#454954','RT':'#454954','LB':'#454954','RB':'#454954','Home':'#a0a7b2','M':'#b75e89','A':'#3d607e','B':'#a34e61','X':'#855b86','Y':'#447969'})),
 ('Crimson','Crimson / graphite',palette('#b83b51','#282c34','#ec879e',{'Touchpad':'#1e242c','LT':'#4a4e58','RT':'#4a4e58','LB':'#4a4e58','RB':'#4a4e58','Home':'#aab0b9','M':'#cc7b94','A':'#b2677c','B':'#484d58','X':'#484d58','Y':'#484d58'}))]
pack={};variants=[]
for variant,title,colors in finishes:
    shape={**geometry,'protectedShapes':[] if variant=='Dark' else [core]}
    pack[variant]={'name':title,'width':794,'height':639,'cover':png(cover),'modelLayers':layers,'modelGeometry':shape,'source':provenance}
    item={'id':variant,'name':title,'thumbnail':f'controller-thumbnails/{MODEL}/{variant}.png','controls':sorted({c['key'] for c in controls}|{'LSB','RSB'}),'labels':labels}
    if colors:item['palette']=colors
    variants.append(item)
(ROOT/'app/controller-data'/f'{MODEL}.js').write_text('// Shaded DualSense artwork. User-confirmed reuse permission; attribution in app/licenses/dualsense-artwork.txt.\nCONTROLLER_PACKS['+json.dumps(MODEL)+']='+json.dumps(pack,separators=(',',':'))+';\n')
file=ROOT/'app/controller-catalog.js';catalog=json.loads(file.read_text().split('const CONTROLLER_CATALOG=')[1].strip().rstrip(';'));catalog=[m for m in catalog if m['id']!=MODEL]
catalog.append({'id':MODEL,'name':'DualSense · Shaded','collection':'Rendered controllers','defaultVariant':'Dark','variants':variants})
file.write_text('// Visual templates are independent of the connected input device.\nconst CONTROLLER_CATALOG='+json.dumps(catalog,separators=(',',':'))+';\n')
(ROOT/'docs/dualsense-sprite-audit.json').write_text(json.dumps({'source':provenance,'controls':measured,'sticks':sticks,'nativeSize':[794,639],'travelNote':'12 source pixels; explicit visual limit, not a device calibration or a value supplied by the CSS.'},indent=2)+'\n')
print('Prepared 3 DualSense finishes; refresh matching thumbnails with tools/capture-dualsense-palettes.cjs. Template: 17 source-aligned controls, 2 separate caps and stationary wells. Reuse permission confirmed by the user.')
