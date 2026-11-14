"""Prepare the supplied rendered Xbox layers without running their HTML.
Use the front reference for physical boundaries. Input remains browser-standard.
The owner confirmed commercial customization/redistribution permission on 2026-11-14.
"""
from pathlib import Path
import base64,hashlib,io,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
from raster_paths import mask_path

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'reference-assets/xbox-white-render';MODEL='XboxWhiteRender'
spec=json.loads((SOURCE/'layers.json').read_text());W,H=spec['canvas']['width'],spec['canvas']['height'];assert (W,H)==(2048,1664)
images={};rows={r['name']:r for r in spec['layers']};hashes={}
for name,row in rows.items():
 p=(SOURCE/row['file']).resolve();assert p.is_relative_to(SOURCE.resolve());im=Image.open(p).convert('RGBA');assert im.size==(W,H);assert list(im.getbbox())==row['bounds'];images[name]=im;hashes[row['file']]=hashlib.sha256(p.read_bytes()).hexdigest()
front=Image.open(SOURCE/'front-reference.png').convert('RGBA');body=images['body'];reference=np.array(front);bare=np.array(body)
composite=Image.new('RGBA',(W,H))
for row in spec['layers']:composite.alpha_composite(images[row['name']])
assert np.array_equal(np.array(composite),np.array(Image.open(SOURCE/'layered-preview.png').convert('RGBA')))
def url(im):
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def gray(a):return a[:,:,:3].mean(axis=2)
controls=[];sticks=[];layers={};audit=[];well_notes=[]
mapping={'a':'A','b':'B','x':'X','y':'Y','view':'Share','menu':'Options','xbox':'Home','left-bumper':'LB','right-bumper':'RB','left-trigger':'LT','right-trigger':'RT'}
for name,key in mapping.items():
 row=rows[name];x,y,right,bottom=row['bounds'];a=np.array(images[name].crop((x,y,right,bottom)));mask=a[:,:,3]>=128
 if name.endswith(('bumper','trigger')):
  # Keep the visible shoulder cutout; later opaque layers may cover its AA edge.
  later=spec['layers'][list(rows).index(name)+1:];visible=np.ones(mask.shape)
  for other in later:visible*=1-np.array(images[other['name']].crop((x,y,right,bottom)))[:,:,3]/255
  mask&=a[:,:,3]*visible>=128
 native=reference[y:bottom,x:right,:3][mask];normal='#'+''.join(f'{int(v):02x}' for v in np.median(native,axis=0))
 controls.append({'key':key,'tag':'path','attrs':{'d':mask_path(mask)},'matrix':[1,0,0,1,x,y],'bounds':[x,y,right-x,bottom-y],'fillRule':'evenodd','floating':False,'normal':normal,'layeredMaterial':True,'surfaceOnly':key!='Home','inkMode':'bright-mark' if key=='Home' else 'default','preserveColorInk':key in ['A','B','X','Y']})
 audit.append({'key':key,'bounds':row['bounds'],'sourceButton':row['button'],'visiblePixels':int(mask.sum())})
row=rows['d-pad'];x,y,right,bottom=row['bounds'];mask=np.array(images['d-pad'].crop((x,y,right,bottom)))[:,:,3]>=128;yy,xx=np.indices(mask.shape);dx=xx-(right-x)/2;dy=yy-(bottom-y)/2
for direction,sector in [('Up',(dy<0)&(abs(dy)>=abs(dx))),('Down',(dy>=0)&(abs(dy)>=abs(dx))),('Left',(dx<0)&(abs(dx)>abs(dy))),('Right',(dx>=0)&(abs(dx)>abs(dy)))]:
 controls.append({'key':'DPad_'+direction,'tag':'path','attrs':{'d':mask_path(mask&sector)},'matrix':[1,0,0,1,x,y],'bounds':[x,y,right-x,bottom-y],'fillRule':'evenodd','floating':False,'normal':'#4d4d4d','layeredMaterial':True,'surfaceOnly':True})
for side in ['left','right']:
 row=rows[side+'-stick-cap'];x,y,right,bottom=row['bounds'];px,py=row['pivot'];cap=images[side+'-stick-cap'].crop((x,y,right,bottom));cap_a=np.array(cap)[:,:,3];ys,xs=np.nonzero(cap_a>0);radius=float(np.hypot(xs+x+.5-px,ys+y+.5-py).max()+2)
 socket=rows[side+'-stick-socket'];sx,sy,sr,sb=socket['bounds'];f=reference[sy:sb,sx:sr];b=bare[sy:sb,sx:sr]
 # The separately exported socket includes surfaces hidden by the housing.
 # Recover its true visible opening from the full front reference and body render.
 opening=(gray(f)<190)&(gray(b)>190)&(f[:,:,3]>128);labels,n=ndimage.label(opening);sizes=np.bincount(labels.ravel());sizes[0]=0;opening=ndimage.binary_fill_holes(labels==sizes.argmax());oy,ox=np.nonzero(opening)
 hole=Image.fromarray((opening*255).astype('uint8'));cup=Image.new('RGBA',(sr-sx,sb-sy),(38,38,38,255));cup.alpha_composite(images[side+'-stick-socket'].crop((sx,sy,sr,sb)))
 under=body.crop((sx,sy,sr,sb));under.paste(cup,(0,0),hole)
 # Preserve the reference's exposed rim. Replace only the baked cap footprint.
 remove=np.array(images[side+'-stick-cap'].crop((sx,sy,sr,sb)))[:,:,3]>0;remove=ndimage.binary_dilation(remove,iterations=2)
 well=front.crop((sx,sy,sr,sb));well.paste(under,(0,0),Image.fromarray((remove*255).astype('uint8')))
 # Supply a well patch covering the cap's complete bounds, while retaining origin.
 patch=front.copy();patch.paste(well,(sx,sy));well_crop=patch.crop((x,y,right,bottom))
 gy,gx=np.indices(opening.shape);cap_mask=np.array(images[side+'-stick-cap'].crop((sx,sy,sr,sb)))[:,:,3]>=128
 reveal=ndimage.binary_erosion(opening,iterations=3)&cap_mask&(np.hypot(gx+sx+.5-px,gy+sy+.5-py)>radius-13)
 locations=np.argwhere(reveal);reveal_samples=[[float(q[1]+sx+.5),float(q[0]+sy+.5)] for q in locations[::max(1,len(locations)//40)]]
 key=side+'Cap';well_key=side+'Well';layers[key]=url(cap);layers[well_key]=url(well_crop)
 rim=float(np.hypot(ox+sx+.5-px,oy+sy+.5-py).max()+1)
 visible_rim=opening&~ndimage.binary_dilation(np.array(images[side+'-stick-cap'].crop((sx,sy,sr,sb)))[:,:,3]>0,iterations=3)
 points=np.argwhere(visible_rim);samples=[[float(q[1]+sx+.5),float(q[0]+sy+.5)] for q in points[::max(1,len(points)//40)]]
 sticks.append({'center':[px,py],'rimSamples':samples,'revealSamples':reveal_samples,'capRadius':radius,'rimRadius':rim,'travel':45,'capImage':key,'wellImage':well_key,'layerBounds':[x,y,right-x,bottom-y]})
 well_notes.append({'side':side,'pivot':[px,py],'capRadius':radius,'visibleRimRadius':rim,'openingBounds':[int(ox.min()+sx),int(oy.min()+sy),int(ox.max()+sx+1),int(oy.max()+sy+1)],'removedCapPixels':int(remove.sum())})
record={'name':'White / graphite','width':W,'height':H,'cover':url(front),'modelLayers':layers,'modelGeometry':{'sourceWidth':W,'sourceHeight':H,'bodyBounds':[42,269,1965,1323],'controls':controls,'sticks':sticks,'protectedShapes':[],'floatArtwork':True,'layered':True,'analogOverlay':True,'spatialRemap':'canonical-positions'},
 'source':{'pack':'White_Xbox_Controller_Assets.zip','frontReferenceSHA256':hashlib.sha256((SOURCE/'front-reference.png').read_bytes()).hexdigest(),'manifestSHA256':hashlib.sha256((SOURCE/'layers.json').read_bytes()).hexdigest(),'permission':'Owner confirmed commercial customization and redistribution permission on 2026-11-14.'}}
gold_cyan={'baseColor':'#24282e','buttonBaseColor':'#18232b','accent':'#30d9ee','pressed':'#36dff3','buttonColors':{key:{'rest':rest,'pressed':pressed} for key,rest,pressed in [('LSB','#c9a951','#f2d98a'),('RSB','#2ac9df','#55eaff'),('DPad_Up','#c9a951','#f2d98a'),('DPad_Down','#c9a951','#f2d98a'),('DPad_Left','#c9a951','#f2d98a'),('DPad_Right','#c9a951','#f2d98a'),('Home','#d3b45e','#f5e2a1'),('Share','#2cb7ca','#55eaff'),('Options','#2cb7ca','#55eaff'),('LB','#28323b','#43e1f3'),('RB','#28323b','#43e1f3'),('LT','#b49345','#f2d98a'),('RT','#b49345','#f2d98a')]}}
pack={'White':record,'GoldCyan':{**record,'name':'Midnight / gold / cyan'}}
(ROOT/'app/controller-data'/f'{MODEL}.js').write_text('// User-supplied rendered Xbox layers; attribution and source audit: docs/xbox-white-render-audit.md.\nCONTROLLER_PACKS['+json.dumps(MODEL)+']='+json.dumps(pack,separators=(',',':'))+';\n')
thumb=front.copy();thumb.thumbnail((400,350));folder=ROOT/'app/controller-thumbnails'/MODEL;folder.mkdir(parents=True,exist_ok=True);thumb.save(folder/'White.png')
path=ROOT/'app/controller-catalog.js';catalog=json.loads(path.read_text().split('const CONTROLLER_CATALOG=')[1].strip().rstrip(';'));index=next((i for i,m in enumerate(catalog) if m['id']==MODEL),len(catalog));catalog=[m for m in catalog if m['id']!=MODEL]
catalog.append({'id':MODEL,'name':'Xbox · Rendered','collection':'Rendered controllers','defaultVariant':'White','variants':[{'id':'White','name':'White / graphite','thumbnail':f'controller-thumbnails/{MODEL}/White.png','controls':sorted({c['key'] for c in controls}|{'LSB','RSB'}),'labels':{'Home':'Xbox / Home','Share':'View / Back','Options':'Menu / Start'}},{'id':'GoldCyan','name':'Midnight / gold / cyan','thumbnail':f'controller-thumbnails/{MODEL}/GoldCyan.png','controls':sorted({c['key'] for c in controls}|{'LSB','RSB'}),'labels':{'Home':'Xbox / Home','Share':'View / Back','Options':'Menu / Start'},'palette':gold_cyan}]})
catalog.insert(index,catalog.pop())
path.write_text('// Visual templates are independent of the connected input device.\nconst CONTROLLER_CATALOG='+json.dumps(catalog,separators=(',',':'))+';\n')
(ROOT/'docs/xbox-white-render-audit.json').write_text(json.dumps({'inputSize':[W,H],'layeredPreviewPixelExact':True,'controls':audit,'wells':well_notes,'hashes':hashes,'visualStickTravel':{'sourcePixels':45,'previousSourcePixels':15,'note':'Expanded visual range; direct radial axes with no additional filtering or deadzone. Not hardware calibration.'},'shoulders':'Visible cutouts; masked illumination only. No hidden geometry or mechanical trigger animation invented.'},indent=2)+'\n')
print('Refresh thumbnails/private preview using tools/capture-xbox-render.cjs. Prepared Xbox white/graphite: front-reference geometry, reconstructed hidden wells, full pivot-relative caps and attached shoulder masks.')
