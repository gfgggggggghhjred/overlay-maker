// Costume and ability drawings for the existing anime collection.
// Pure Canvas paths; serialized with the same renderer into customer HTML.
function createAnimeIdentityPainter(){
 const TAU=Math.PI*2,paths=new Map();
 const path=d=>{if(!paths.has(d)){if(paths.size>=256)paths.delete(paths.keys().next().value);paths.set(d,new Path2D(d));}return paths.get(d);};
 const fill=(c,d,color)=>{c.fillStyle=color;c.fill(path(d),'evenodd');};
 const stroke=(c,d,color,width)=>{c.strokeStyle=color;c.lineWidth=width;c.stroke(path(d));};
 const disk=(c,x,y,r,color)=>{c.fillStyle=color;c.beginPath();c.arc(x,y,r,0,TAU);c.fill();};
 const line=(c,d,color,width=4)=>{c.strokeStyle=color;c.lineWidth=width;c.beginPath();d.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.stroke();};
 function star(c,x,y,r,color){c.fillStyle=color;c.beginPath();for(let i=0;i<10;i++){const a=i*Math.PI/5-Math.PI/2,d=i%2?r*.43:r;c.lineTo(x+Math.cos(a)*d,y+Math.sin(a)*d);}c.closePath();c.fill();}
 const known=new Set(['void','leaf-seal','straw-hat','hell-butterfly','hunter-mark','clover','millennium','ladybug','wise-pin','turbo-cat','kaiju-mask','round-glasses','sharingan','uchiha-fan','flame-guard','pull-cord','deku-mask','water-crest','spirit-blade','chimera']);
 function symbol(c,kind,r,phase=0){
  if(!known.has(kind))return false;c.save();c.scale(r,r);c.lineCap='round';c.lineJoin='round';
  if(kind==='void'){
   const halo=c.createRadialGradient(0,0,.03,0,0,.94);halo.addColorStop(0,'#ffffff');halo.addColorStop(.12,'#e8deff');halo.addColorStop(.29,'#ae85e2');halo.addColorStop(.55,'#443363');halo.addColorStop(1,'#241c3b');c.fillStyle=halo;c.beginPath();c.arc(0,0,.94,0,TAU);c.fill();
   for(let i=0;i<6;i++){c.save();c.rotate(i*TAU/6);stroke(c,'M.83-.18Q.49.13 .2 0','#bda2ed',.035);c.restore();}disk(c,0,0,.075,'#ffffff');
  }else if(kind==='leaf-seal'){
   stroke(c,'M.31-.38C-.07-.81-.84-.4-.64.15-.48.63 .24.61 .39.2 .52-.13 .22-.42-.08-.3-.35-.17-.25.2-.04.18 .08.17 .13.04 .08-.05','#101820',.135);
   stroke(c,'M-.54.37-.84.59-.77.1 M.29-.39 .75-.76 .65-.24 .35-.12','#101820',.135);
  }else if(kind==='straw-hat'){
   fill(c,'M-.68.18C-.73-.62-.41-.8 0-.8 .42-.8 .73-.62 .68.18Z','#e9bc5c');
   fill(c,'M-.68-.12Q0 .01 .68-.12L.68.16Q0 .33-.68.16Z','#c82e32');
   c.fillStyle='#f4cf78';c.beginPath();c.ellipse(0,.29,1,.22,0,0,TAU);c.fill();stroke(c,'M-.98.29Q0 .71 .98.29','#9e6827',.055);
   for(const x of [-.55,-.27,.27,.55])stroke(c,`M${x} .23l.07 .17`,'#b8873b',.035);
   stroke(c,'M-.44-.49Q0-.76 .44-.49','#ffdfa0',.06);
  }else if(kind==='hell-butterfly'){
   for(const sign of [-1,1]){c.save();c.scale(sign,1);fill(c,'M.02-.09C.16-.65 .68-1.06 .94-.68 1.08-.31 .71-.03 .22.13 .68.08 .88.43 .65.64L.42 1 .36.65C.16.61 .03.32 .02-.09Z','#1a1428');stroke(c,'M.14.04 .64-.5 M.17.22 .54.49','#b09cd6',.075);c.restore();}fill(c,'M-.06-.35H.06L.09.68H-.09Z','#0d0a16');disk(c,0,-.4,.11,'#0d0a16');stroke(c,'M-.04-.49-.19-.72 M.04-.49 .19-.72','#0d0a16',.05);
  }else if(kind==='hunter-mark'){
   for(const x of [-.48,.48]){c.save();c.translate(x,0);fill(c,'M-.43-.65H-.16L0-.24 .16-.65H.43L.17 0 .43.65H.16L0 .24-.16.65H-.43L-.17 0Z',x<0?'#b72e36':'#184e40');c.restore();}line(c,[[-.88,.85],[.88,.85]],'#c4a665',.1);
  }else if(kind==='clover'){
   for(let i=0;i<5;i++){c.save();c.rotate(i*TAU/5);fill(c,'M0 .05C-.23-.13-.59-.44-.4-.69-.26-.91-.04-.77 0-.59 .05-.81 .3-.94 .44-.68 .59-.41 .22-.12 0 .05Z','#101015');stroke(c,'M0 .05C-.23-.13-.59-.44-.4-.69-.26-.91-.04-.77 0-.59 .05-.81 .3-.94 .44-.68 .59-.41 .22-.12 0 .05Z','#b7283a',.035);c.restore();}stroke(c,'M.03.1Q.22.64 .56.84','#17131c',.1);
  }else if(kind==='millennium'){
   fill(c,'M-1-.75H1L0 1Z','#deaa39');fill(c,'M-1-.75 0 1-.12-.75Z','#f7d777');fill(c,'M.7-.57 0 .7-.05-.57Z','#e5b545');stroke(c,'M-1-.75H1L0 1Z','#744d18',.065);stroke(c,'M-.74-.57H.74L0 .71Z','#9b671f',.045);
   stroke(c,'M-.45-.55V-.27H-.68 M.42-.54V-.3H.63 M-.32.2H.3 M-.12.52V.18','#b07a29',.04);
   fill(c,'M-.49-.12Q0-.58 .49-.12 0 .29-.49-.12Z','#282015');disk(c,0,-.12,.17,'#f4d46a');disk(c,0,-.12,.085,'#201a13');stroke(c,'M-.48.04Q-.25.07-.25.37 M.43.04Q.61.37 .25.3','#282015',.055);
  }else if(kind==='ladybug'){
   fill(c,'M0-1C.26-1 .31-.76 .28-.65 .79-.53 .85.39 .39.83L0 1-.39.83C-.85.39-.79-.53-.28-.65-.31-.76-.26-1 0-1Z','#eac459');
   fill(c,'M-.08-.64C-.64-.6-.76.35-.25.7L-.08.79Z','#315743');fill(c,'M.08-.64C.64-.6 .76.35 .25.7L.08.79Z','#315743');
   for(const x of [-.36,.36])for(const y of [-.23,.27])disk(c,x,y,.13,'#f6d678');line(c,[[0,-.65],[0,.88]],'#97702e',.07);disk(c,0,-.82,.13,'#b28c36');
  }else if(kind==='wise-pin'){
   fill(c,'M-1-.12-.47-.47 0-.27 .47-.47 1-.12 .44.3H-.44Z','#d6ba70');fill(c,'M-.53-.1Q0-.57 .53-.1 0 .35-.53-.1Z','#1d3d35');disk(c,0,-.1,.17,'#d6ba70');stroke(c,'M0 .27V.84 M-.18.6H.18','#d6ba70',.12);
  }else if(kind==='turbo-cat'){
   // Broad face, pointed ears, red collar and the raised beckoning paw.
   fill(c,'M-.61.21-.93-.19-.79-.92-.3-.65Q0-.77 .3-.65L.79-.92 .92-.17 .62.25 .57.84H-.57Z','#eee6d8');fill(c,'M-.77-.73-.68-.34-.4-.55Z M.77-.73 .68-.34 .4-.55Z','#b86055');
   fill(c,'M.54.66C1.15.55 1.11-.44 .83-.5 .57-.55 .63-.06 .54.08Z','#eee6d8');stroke(c,'M.75-.19H.99 M.76-.06H1','#5e5148',.055);
   fill(c,'M-.61-.14Q-.37-.53-.13-.14-.37.04-.61-.14Z M.13-.14Q.37-.53 .61-.14 .37.04 .13-.14Z','#f9f5e9');disk(c,-.37,-.22,.13,'#3f3c50');disk(c,.37,-.22,.13,'#3f3c50');stroke(c,'M-.61-.14Q-.37-.53-.13-.14 M.13-.14Q.37-.53 .61-.14','#403834',.055);fill(c,'M-.18-.68Q0-.56 .18-.68 0-.82-.18-.68Z','#af2834');
   fill(c,'M-.08.03H.08L0 .13Z','#ba4c43');stroke(c,'M0 .13V.28 M-.25.34Q-.1.38 0 .28 .1.38 .25.34 M-.7.03H-.49 M-.71.17H-.49 M.49.03H.7 M.49.17H.71','#403834',.055);
   fill(c,'M-.55.69 0 1 .55.69Z','#3d7751');stroke(c,'M-.59.65Q0 .85 .58.65','#b82f38',.15);disk(c,0,.78,.14,'#dcb44b');
  }else if(kind==='kaiju-mask'){
   fill(c,'M-.85-.94-.45-.67-.2-.82 0-.7 .2-.82 .45-.67 .85-.94 .66-.34 .83-.03 .58.61 .22.96H-.22L-.58.61-.83-.03-.66-.34Z','#c5d6d6');
   fill(c,'M-.67-.16-.12.06-.2.25-.63.12Z M.67-.16 .12.06 .2.25 .63.12Z','#13242a');stroke(c,'M-.58-.09-.24.1 M.58-.09 .24.1','#40e4eb',.07);
   fill(c,'M-.47.32-.25.39-.2.65H.2L.25.39 .47.32 .33.78 0 .91-.33.78Z','#17252b');
   for(const x of [-.24,-.08,.08,.24])fill(c,`M${x-.045} .4h.09l-.01 .2h-.07Z`,'#e0eeee');stroke(c,'M0-.58-.1-.21 0 .18 .1-.21Z','#788e92',.05);
  }else if(kind==='round-glasses'){
   for(const x of [-.47,.47]){disk(c,x,-.17,.4,'#eee4d0');c.strokeStyle='#30332d';c.lineWidth=.11;c.beginPath();c.arc(x,-.17,.4,0,TAU);c.stroke();}stroke(c,'M-.08-.2H.08 M-.88-.23H-1 M.88-.23H1','#30332d',.09);
   fill(c,'M-.05.4C-.15.2-.38.3-.65.5L-.54.64Q-.23.59-.05.47Z M.05.4C.15.2 .38.3 .65.5L.54.64Q.23.59 .05.47Z','#bbc0ad');stroke(c,'M-.65.5Q-.28.23-.05.4 M.05.4Q.28.23 .65.5','#5e6658',.045);
  }else if(kind==='sharingan'){
   c.strokeStyle='#180b12';c.lineWidth=.065;c.beginPath();c.arc(0,0,.73,0,TAU);c.stroke();disk(c,0,0,.17,'#180b12');
   for(let i=0;i<3;i++){c.save();c.rotate(i*TAU/3+phase*.32);disk(c,0,-.6,.115,'#180b12');fill(c,'M.03-.7C.28-.66 .34-.42 .11-.29 .24-.49 .04-.43-.06-.53Z','#180b12');c.restore();}
  }else if(kind==='uchiha-fan'){
   fill(c,'M-.8.12C-.94-.94 .94-.94 .8.12L.13.57V1H-.13V.57Z','#eee5dc');fill(c,'M-.8.12C-.94-.94 .94-.94 .8.12L.55.27H-.55Z','#c63742');stroke(c,'M-.78.13Q0 .43 .78.13','#28242a',.04);
  }else if(kind==='flame-guard'){
   const d='M-.06-1C.2-.83 .08-.66 .35-.55Q.61-.54 .55-.91C1.01-.61 .62-.35 .75-.14Q.83.02 1-.1C1.05.25 .66.36 .65.55Q.67.72 .86.64C.75 1.01 .37.73 .23.82Q.08.9 .16 1.08C-.15 1.07-.21.77-.42.72Q-.64.66-.7.85C-1.03.62-.65.39-.78.15Q-.84.01-1.04.12C-1.05-.22-.7-.32-.63-.5Q-.55-.69-.8-.66C-.51-1.01-.31-.69-.19-.74Q-.04-.81-.06-1Z';fill(c,d,'#bc302e');c.save();c.scale(.82,.82);fill(c,d,'#f5bc43');c.restore();fill(c,'M-.09-.27H.09V.27H-.09Z','#2d2020');
  }else if(kind==='pull-cord'){
   stroke(c,'M0-1V-.4','#242927',.12);fill(c,'M-.67-.43H.67L.87.2 .44.66H-.44L-.87.2Z M-.42-.18-.55.12-.3.38H.3L.55.12 .42-.18Z','#202521');stroke(c,'M-.63-.36H.61','#6b7368',.07);
  }else if(kind==='deku-mask'){
   fill(c,'M-.76-.94-.28-.61 .28-.61 .76-.94 .63-.25 .82.17 .48.86H-.48L-.82.17-.63-.25Z','#3d9773');fill(c,'M-.65-.12-.15.03-.31.2-.65.14Z M.65-.12 .15.03 .31.2 .65.14Z','#132f2b');fill(c,'M-.61.23H.61L.36.85H-.36Z','#e4e6d7');stroke(c,'M-.32.38-.23.72 M-.09.38-.06.74 M.09.38 .06.74 M.32.38 .23.72','#667e72',.065);
  }else if(kind==='chimera'){fill(c,'M-.72-.27-.91-.87-.36-.63Q0-.81 .36-.63L.91-.87 .72-.27Q1 .33 .49.87H-.49Q-1 .33-.72-.27Z','#aac3a3');fill(c,'M-.73-.53-.54-.92-.29-.6Z M.73-.53 .54-.92 .29-.6Z','#503d47');disk(c,-.3,-.03,.14,'#e9d0a1');disk(c,.3,-.03,.14,'#e9d0a1');fill(c,'M-.13.29 0 .14 .13.29 0 .43Z','#ad665c');stroke(c,'M-.28.53Q0 .75 .28.53','#493f3e',.07);
  }else if(kind==='spirit-blade'){fill(c,'M-.17-1 .17-1 .21.32Q.52.77-.12 1L-.1.28Z','#a9c9d0');stroke(c,'M-.08-.95 .05.35Q.27.69-.09.87','#f1ffff',.06);fill(c,'M-.34-.9H.34V-.75H-.34Z M-.11-1.15H.11V-.91H-.11Z','#27313b');
  }else if(kind==='water-crest'){
   for(let i=0;i<3;i++){c.save();c.translate(0,(i-1)*.48);fill(c,'M-1 .22C-.6.19-.3-.51 .15-.37 .52-.29 .53.2 1-.13 .77.51 .36.44 .06.07-.2-.24-.54.61-1 .22Z',i===1?'#287aba':'#59c5de');stroke(c,'M-.81.2Q-.24-.48 .15-.3 .44-.18 .5.14 .73.04','#e3fbf5',.075);c.restore();}
  }
  c.restore();return true;
 }
 function emblem(c,kind,x,y,r,phase=0){c.save();c.translate(x,y);symbol(c,kind,r,phase);c.restore();}
 function shell(c,style,p){
  c.save();c.lineJoin='round';c.lineCap='round';
  if(style==='ninja'){
   fill(c,'M0 0H1672V185L1100 252 972 128H700L572 252 0 185Z','#1c252b');line(c,[[836,266],[836,830]],'#252b2a',12);line(c,[[850,270],[850,829]],'#f9b35d',3);fill(c,'M0 760 310 674 437 941H0Z M1672 760 1362 674 1235 941H1672Z','#1b252b');

  }else if(style==='pirate'){
   fill(c,'M0 690Q350 625 605 748L1060 748Q1350 625 1672 690V941H0Z','#254d80');fill(c,'M0 660Q350 600 605 717H1060Q1350 600 1672 660V711Q1370 660 1060 766H605Q330 660 0 711Z','#e9c56b');fill(c,'M708 0 836 237 964 0Z','#b96c4d');stroke(c,'M692 0 806 288 M980 0 866 288','#791f2a',8);
   stroke(c,'M160 618Q255 540 340 555 M1360 540l40-30 40 30','#6f3440',3);
  }else if(style==='saiyan'){
   fill(c,'M490 0 836 399 1182 0 1050 0 836 225 622 0Z','#164d89');fill(c,'M0 725Q410 637 836 722 1260 637 1672 725V816Q1260 722 836 803 410 722 0 816Z','#195299');fill(c,'M0 724H240V941H0Z M1432 724H1672V941H1432Z','#194c88');stroke(c,'M610 62 836 326 1062 62','#d56320',7);
  }else if(style==='soul'){
   fill(c,'M538 0 836 370 1134 0 1028 0 836 244 644 0Z','#ecebe3');fill(c,'M671 0 840 209 1009 0Z','#131923');fill(c,'M0 730Q835 638 1672 730V802Q835 712 0 802Z','#e2e0d8');stroke(c,'M523 80 792 409 664 685','#40444b',5);stroke(c,'M1149 80 880 409 1008 685','#353b44',5);
  }else if(style==='water'){
   // The existing checker painter provides a single, even green/black grid.
   fill(c,'M589 0 835 300 1081 0 995 0 835 190 675 0Z','#ede4d4');fill(c,'M682 0 835 182 988 0Z','#202523');stroke(c,'M189 730H415 M1257 730H1483','#283b32',6);
  }else if(style==='curse'){
   const gradient=c.createRadialGradient(836,378,2,836,378,470);gradient.addColorStop(0,'#dddcff');gradient.addColorStop(.05,'#5e4b93');gradient.addColorStop(.2,'#1d193b');gradient.addColorStop(1,'#090f20');c.fillStyle=gradient;c.fillRect(0,0,1672,941);
   for(const [x,y,r]of [[237,629,3],[1401,231,3],[1212,760,2],[411,318,2],[1002,502,3]])disk(c,x,y,r,'#e2d6ff');
  }else if(style==='hero'){
   fill(c,'M0 0H435L645 276 533 427 0 295Z M1672 0H1237L1027 276 1139 427 1672 295Z','#e8e7d9');fill(c,'M0 744H1672V824H0Z','#b1383d');fill(c,'M735 740H937V829H735Z','#b5c6bb');fill(c,'M775 758H897V811H775Z','#244f44');stroke(c,'M501 28 690 304V684 M1171 28 982 304V684','#173e35',12);
  }else if(style==='chainsaw'){
   fill(c,'M660 0 835 184 1010 0 929 0 835 89 741 0Z','#b9c4b9');fill(c,'M809 72H861L890 165 860 218 895 632 835 696 775 632 810 218 780 165Z','#202a25');fill(c,'M0 758Q835 690 1672 758V941H0Z','#242d27');stroke(c,'M665 15 772 210 677 174 M1005 15 898 210 993 174','#d2d5c8',6);
  }else if(style==='hunter'){
   fill(c,'M80 86H1592V207H80Z M80 767H1592V865H80Z','#2c7654');fill(c,'M128 259H468V655H128Z','#d9c7a3');fill(c,'M1224 259H1544V655H1224Z','#c8b789');stroke(c,'M134 332H456 M1234 332H1533 M540 826H1128','#9b453f',7);emblem(c,'hunter-mark',1420,475,94);
  }else if(style==='clover'){
   stroke(c,'M156 170H1516V791H156Z','#866c47',13);stroke(c,'M185 198H1487V762H185Z','#493d33',4);
   for(const [x,y]of [[172,186],[1500,186],[172,777],[1500,777]]){fill(c,`M${x-44} ${y-44}h88v15h-73v73h-15Z`,'#a28451');}
   emblem(c,'clover',1390,626,116);stroke(c,'M184 763 225 732 209 786 M1489 197 1449 240 1506 224','#2b2427',11);
  }else if(style==='duelist'){
   for(const [x,a]of [[265,-.12],[1390,.12]]){c.save();c.translate(x,544);c.rotate(a);c.fillStyle='#6a3427';c.fillRect(-147,-222,294,444);c.strokeStyle='#d6b465';c.lineWidth=14;c.strokeRect(-132,-207,264,414);c.strokeStyle='#a77b44';c.lineWidth=5;c.strokeRect(-108,-181,216,272);c.fillStyle='#bd9858';c.fillRect(-108,123,216,51);c.restore();}fill(c,'M725 0H947V121L836 250 725 121Z','#3b2542');
  }else if(style==='gold'){
   fill(c,'M650 0 836 215 1022 0Z','#e9b74e');fill(c,'M836 500C650 390 650 220 836 330 1022 220 1022 390 836 500Z','#241b2c');stroke(c,'M632 0 540 179 677 319 M1040 0 1132 179 995 319','#e4bd60',9);emblem(c,'ladybug',271,662,62);emblem(c,'ladybug',1400,662,62);
  }else if(style==='spy'){
   fill(c,'M628 0H1044L950 250 836 552 722 250Z','#e8ddbf');fill(c,'M794 108 836 71 878 108 856 166 893 433 836 505 779 433 816 166Z','#a4373c');fill(c,'M532 0 762 0 722 152 650 170 765 516 441 218Z M1140 0H910L950 152 1022 170 907 516 1231 218Z','#344f42');stroke(c,'M532 0 650 170 765 516 M1140 0 1022 170 907 516','#799076',5);emblem(c,'wise-pin',1320,353,41);emblem(c,'chimera',264,745,30);
  }else if(style==='occult'){
   fill(c,'M0 675Q300 519 468 674L546 941H0Z M1672 675Q1372 519 1204 674L1126 941H1672Z','#e8e0d2');stroke(c,'M0 713Q280 562 462 713 M1672 713Q1392 562 1210 713','#bd3a43',28);emblem(c,'turbo-cat',1388,643,113);
  }else if(style==='kaiju'){
   fill(c,'M496 0H1176L1118 284 836 443 554 284Z','#273c43');fill(c,'M0 652 360 538 546 941H0Z M1672 652 1312 538 1126 941H1672Z','#1d3038');line(c,[[524,25],[575,252],[720,341]],'#3ec8d6',8);line(c,[[1148,25],[1097,252],[952,341]],'#3ec8d6',8);line(c,[[202,740],[350,700],[440,900]],'#3ec8d6',5);line(c,[[1470,740],[1322,700],[1232,900]],'#3ec8d6',5);
  }else if(style==='assassin'){
   fill(c,'M0 0H1672V329L1118 209 1050 126H622L554 209 0 329Z','#e1dfca');fill(c,'M560 0H635V385H560Z M1037 0H1112V385H1037Z','#42694a');fill(c,'M554 329H1118V866H554Z','#416c49');stroke(c,'M584 359H1088 M650 679H1021V824H650Z','#6d8c63',6);emblem(c,'round-glasses',1374,707,57);
  }else if(style==='uchiha'){
   fill(c,'M0 0H1672V130L1134 182H538L0 130Z','#30313b');stroke(c,'M0 133 538 185H1134L1672 133','#962b38',9);emblem(c,'uchiha-fan',1399,650,100);
  }else if(style==='flame'){
   // Cape edging: broad nested cel flame silhouettes, no distressed slashes.
   const d='M0 941V720Q72 738 117 580C116 689 160 682 164 744Q213 712 282 609C268 730 325 703 333 805Q368 748 418 689C399 829 477 801 499 903L564 850Q560 902 643 941Z';for(const side of [0,1]){c.save();if(side){c.translate(1672,0);c.scale(-1,1);}fill(c,d,'#b8322b');c.save();c.translate(0,55);fill(c,d,'#ed812d');c.restore();c.save();c.translate(0,115);fill(c,d,'#f9c44e');c.restore();c.restore();}fill(c,'M607 0 836 266 1065 0 991 0 836 160 681 0Z','#c6c5ba');stroke(c,'M627 0 836 243 1045 0','#44403b',5);
  }
  c.restore();
 }
 function effect(c,style,p,progress,power=1){
  const q=Math.max(0,Math.min(1,progress)),rise=1-Math.pow(1-q,3),fade=Math.pow(Math.sin(Math.PI*q),.7),a=fade*(.55+.45*power);if(a<.001)return;
  c.save();c.globalAlpha=a;c.lineCap='round';c.lineJoin='round';
  if(style==='ninja'){
   c.translate(1420,664);const r=60+rise*30;disk(c,0,0,r,'#1e6fc2');disk(c,0,0,r*.72,'#49c8ed');
   for(let j=0;j<5;j++){c.save();c.rotate(-q*TAU*1.6+j*TAU/5);stroke(c,`M${-r} 0C${-r*.5} ${-r} ${r*.8} ${-r*.8} ${r*.23} ${r*.08}Q0 ${r*.35} ${-r*.1} 0`,'#defbff',3+j*.4);c.restore();}
  }else if(style==='saiyan'){
   const top=820-rise*470;
   for(const x of [300,1372]){c.save();c.translate(x,0);const sway=Math.sin(q*TAU)*22;
    const aura=`M-211 941C-191 808-202 ${top+170}-122 ${top+40}Q-142 ${top+189}-73 ${top+210}C-59 ${top+106} 12 ${top+53} ${sway+7} ${top-85}Q104 ${top+51} 76 ${top+191}C130 ${top+175} 149 ${top+105} 150 ${top+64}Q211 ${top+228} 211 941Z`;
    fill(c,aura,'#e9aa32');c.save();c.translate(0,72);c.scale(.77,1);fill(c,aura,'#f8d65c');c.restore();c.save();c.translate(0,153);c.scale(.49,1);fill(c,aura,'#fff2ba');c.restore();stroke(c,`M-137 929C-156 802-117 ${top+238}-86 ${top+186} M120 911Q145 ${top+263} 115 ${top+220}`,'#fff2b0',7);c.restore();}
  }else if(style==='pirate'){
   c.translate(-320+rise*1600,590);c.rotate(-.12);fill(c,'M-1200-26Q-620-80-55-34L60-30 62 66Q-620 7-1200 42Z','#d39c70');fill(c,'M-1200-19Q-620-55-55-27L36-24 30 2Q-620-3-1200 30Z','#edbf92');fill(c,'M-11-46Q-6-71 23-67H120Q151-62 154-30V37Q151 74 116 77H17L-15 47Z','#e4ae80');stroke(c,'M-11-46Q-6-71 23-67H120Q151-62 154-30V37Q151 74 116 77H17L-15 47Z','#774b39',5);stroke(c,'M28-60V-13 M65-62V-12 M102-57V-8 M-4 25Q45 4 75 31','#9a664a',5);
  }else if(style==='water'){
   for(let j=0;j<3;j++){const y=735-j*56,x=-240+rise*1600;c.save();c.translate(x,y);stroke(c,'M-490 85C-280-66 50 140 283-22Q391-100 323-146Q232-172 227-72','#236eb7',25-j*5);stroke(c,'M-490 77C-280-72 50 132 282-30Q366-93 328-124L312-101 294-130 274-109 252-130 234-103','#e5fff5',7-j);c.restore();}
  }else if(style==='soul'||style==='flame'){
   c.translate(836,650);c.rotate(-1.2+rise*1.45);const r=650,arc=new Path2D('M-680 80Q-195-310 600-116Q-69-147-680 80Z');
   c.fillStyle=style==='flame'?'#ba332c':'#3b74bd';c.fill(arc);c.save();c.translate(0,-12);c.scale(.95,.68);c.fillStyle=style==='flame'?'#ef8b32':'#80d5ef';c.fill(arc);c.restore();c.save();c.translate(0,-19);c.scale(.9,.35);c.fillStyle=style==='flame'?'#ffe995':'#f0ffff';c.fill(arc);c.restore();
  }else if(style==='curse'){
   c.translate(836,405);const inward=q<.4,stage=inward?q/.4:(q-.4)/.6,rad=inward?430*(1-stage)+35:35+stage*610;
   for(let j=0;j<8;j++){c.save();c.rotate(j*TAU/8);stroke(c,`M${rad} 0Q${rad*.6} -45 ${Math.max(5,rad-110)} 0`,'#a98ae7',4);c.restore();}disk(c,0,0,inward?8+stage*12:20*(1-stage),'#f6efff');if(!inward){c.strokeStyle='#ddd2ff';c.lineWidth=6*(1-stage)+1;c.beginPath();c.ellipse(0,0,rad,rad*.42,-.2,0,TAU);c.stroke();}
  }else if(style==='hero'||style==='kaiju'){
   const bands=style==='hero'?[[[110,790],[200,698],[178,654],[348,520],[369,569],[530,414]],[[1562,790],[1472,698],[1494,654],[1324,520],[1303,569],[1142,414]]]:[[[524,25],[575,252],[720,341]],[[1148,25],[1097,252],[952,341]],[[202,740],[350,700],[440,900]],[[1470,740],[1322,700],[1232,900]]];
   for(const pts of bands){line(c,pts,style==='hero'?'#2dba83':'#37b3cc',13);line(c,pts,style==='hero'?'#baffcd':'#c2fcff',4);}
  }else if(style==='chainsaw'){
   c.translate(-180+rise*1800,610);c.rotate(-.18);fill(c,'M-260-36H236L282 0 236 36H-260Z','#7c9491');for(let i=-5;i<5;i++)fill(c,`M${i*48} -36l22-27 22 27Z M${i*48} 36l22 27 22-27Z`,'#d6e1d9');stroke(c,'M-247 0H220','#293c37',9);for(let j=0;j<4;j++)line(c,[[130+j*25,60],[160+j*40,100+j*18]],'#f3b457',4);
  }else if(style==='hunter'){
   const y=255+rise*430;line(c,[[95,y],[1565,y]],'#66efae',7);line(c,[[95,y+6],[1565,y+6]],'#e2fff0',2);
  }else if(style==='clover'){
   c.translate(836,530);c.rotate(-.45+rise*.3);fill(c,'M-780 100Q-460-35 650-126L400-55 770-85Q240 65-780 100Z','#be3349');c.translate(0,-4);fill(c,'M-780 100Q-460-35 650-126L400-55 770-85Q240 65-780 100Z','#14131b');
  }else if(style==='duelist'){
   c.translate(1260-rise*780,475-rise*120);c.rotate(-.3+rise*.65);c.fillStyle='#dab862';c.fillRect(-98,-142,196,284);c.fillStyle='#523728';c.fillRect(-83,-126,166,252);c.strokeStyle='#d9b560';c.lineWidth=4;c.strokeRect(-65,-100,130,143);emblem(c,'millennium',0,-22,43);
  }else if(style==='gold'){
   c.translate(1390,654);c.scale(1+rise*.2,1+rise*.2);symbol(c,'ladybug',115,q);
  }else if(style==='spy'){
   c.translate(1364,629);c.rotate(-.16);const s=.7+.3*Math.min(1,q/.15);c.scale(s,s);c.strokeStyle='#ab3e46';c.lineWidth=9;c.strokeRect(-118,-86,236,172);c.lineWidth=3;c.strokeRect(-103,-71,206,142);emblem(c,'wise-pin',0,0,64);
  }else if(style==='occult'){
   c.translate(1388,643);for(let i=0;i<2;i++){c.strokeStyle=i?'#b8efe0':'#e26270';c.lineWidth=i?4:8;c.beginPath();c.ellipse(0,0,75+rise*(260+i*50),45+rise*(150+i*40),-.2,0,TAU);c.stroke();}
  }else if(style==='assassin'){
   const x=-400+rise*2100;stroke(c,`M${x-370} 650Q${x-60} 610 ${x+190} 640`,'#d5e1bb',9);
  }else if(style==='uchiha'){
   c.translate(1399,650);c.strokeStyle='#b82f41';c.lineWidth=6;c.beginPath();c.arc(0,0,85+rise*120,-2.8,-.3);c.stroke();emblem(c,'uchiha-fan',0,0,70+rise*8);
  }
  c.restore();
 }
 return{symbol,shell,effect,inspect:()=>({cachedPaths:paths.size})};
}
