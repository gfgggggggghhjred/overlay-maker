// Procedural theme artwork: no network, image downloads or external runtime dependencies.
// Kept as a factory so the same painter is embedded verbatim in exported overlays.
function createThemePainter(ctx, faces, shellMask, getLayout) {
 const artwork=createButtonArtworkPainter(),identity=createAnimeIdentityPainter(),layer=document.createElement('canvas');layer.width=1672;layer.height=941;
 const g=layer.getContext('2d'),pulse=document.createElement('canvas');pulse.width=1672;pulse.height=941;const pc=pulse.getContext('2d'),press=createPressEffectPainter(ctx,faces,shellMask,getLayout);
 let cacheKey='',lastTime=-Infinity,styleKey='',previous={},events=[];
 function shell(style,p){
  const key=JSON.stringify([style,p.baseColor,p.accent,p.pressed,shellMask.dataset.skin]);if(key===cacheKey)return;cacheKey=key;
  g.clearRect(0,0,1672,941);identity.shell(g,style,p);g.globalCompositeOperation='destination-in';g.drawImage(shellMask,0,0);g.globalCompositeOperation='source-over';
 }
 function button(key,style,p,state,time){artwork.draw(ctx,faces[key]?.themeFace||faces[key],key,style,p,state,time);}
 return {
  update(p,state,time){
   press.update(p,state,time);
   const key=(p.themeStyle||'none')+'|'+shellMask.dataset.skin,enabled=!!p.themeAbilityEffects&&p.themeStyle!=='none';
   if(key!==styleKey||time<lastTime||time-lastTime>1200||!enabled){events=[];previous={};if(styleKey)previous=Object.fromEntries(Object.entries(state).filter(([k])=>k!=='axes').map(([k,v])=>[k,{active:typeof v==='number'?v>.16:v===true}]));styleKey=key;}
   events=events.filter(e=>time-e.time<e.duration);lastTime=time;
   let edge=false,power=0;
   for(const k of new Set([...Object.keys(previous),...Object.keys(state)])){if(k==='axes')continue;const value=state[k];const threshold=['LT','RT'].includes(k)?(previous[k]?.active ? .08 : .16):.5,active=typeof value==='number'?value>threshold:value===true;if(enabled&&active&&!previous[k]?.active){edge=true;power=Math.max(power,typeof value==='number'?value:1);}previous[k]={active};}
   if(edge&&p.animationMode!=='still'){const duration={ninja:660,pirate:620,saiyan:760,soul:420,water:650,curse:940,hero:340,chainsaw:380,hunter:520,clover:450,duelist:520,gold:400,spy:360,occult:420,kaiju:280,assassin:220,uchiha:540,flame:480}[p.themeStyle]||600;events.push({time,power,duration});if(events.length>4)events.shift();}
  },
  shell(p,state,time){
   const style=p.themeStyle||'none',amount=p.themeIntensity??.7;if(style==='none'||amount===0)return;
   shell(style,p);ctx.save();ctx.globalAlpha=amount;ctx.drawImage(layer,0,0);ctx.restore();
   pc.clearRect(0,0,1672,941);
   if(p.themeAbilityEffects&&p.animationMode!=='still')for(const event of events){const age=lastTime-event.time;if(age>=0&&age<event.duration)identity.effect(pc,style,p,age/event.duration,event.power);}
   pc.globalCompositeOperation='destination-in';pc.drawImage(shellMask,0,0);pc.globalCompositeOperation='source-over';ctx.save();ctx.globalAlpha=amount*(p.animationMode==='reduced'?.5:.85);ctx.drawImage(pulse,0,0);ctx.restore();
  },
  bursts(p,time){
   press.draw(p,time);
  },
  controls(p,state,time){for(const key of ['A','B','X','Y'])button(key,p.buttonStyle,p,state,time);button('Home',p.homeStyle,p,state,time);},
  inspect:()=>({activeSignatureEvents:events.length,cachedPaths:identity.inspect().cachedPaths}),
  sample(c,kind,color){c.save();c.translate(32,32);c.strokeStyle=c.fillStyle=color;artwork.symbol(c,kind,23);c.restore();}
 };
}
