/* Sin dependencias: verifica orden, esperas, cancelacion y reinicio del guion. */
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../slide08.js'),'utf8');
function harness(){
  let time=0,id=0,route='home',answer=false;
  const tasks=new Map(),events=[],eventTimes=[],styles=[];
  const classes=()=>{const set=new Set();return {add(...v){v.forEach(x=>set.add(x));},remove(...v){v.forEach(x=>set.delete(x));},contains(v){return set.has(v);}};};
  const el=()=>({classList:classes(),style:{},dataset:{},textContent:''});
  const hand=el(),typed=el(),enter=el(),status=el();
  const appWin={innerHeight:926,scrollY:0,scrollTo(x,y){this.scrollY=y;}};
  const webWin={innerHeight:722,scrollY:0,scrollTo(x,y){this.scrollY=y;}};
  const target=(next,y=300,disabled=false)=>({disabled,getBoundingClientRect(){return {left:24,top:y-appWin.scrollY,bottom:y-appWin.scrollY+60,width:380,height:60};},click(){events.push(next);eventTimes.push(time);if(next==='answer')answer=true;else{route=next;appWin.scrollY=0;}}});
  const appDoc={querySelector(s){
    if(s==='.page-home')return route==='home'?el():null;
    if(s==='.pitch-hand')return hand;
    if(s==='a[href="#quiz/consumo"]')return route==='home'?target('question',450):null;
    if(s==='[data-action="answer"]'||s==='[data-action="answer"][data-value="1"]')return route==='question'?target('answer',620):null;
    if(s==='[data-action="quiz-next"]')return route==='question'?target('choice',1000,!answer):null;
    if(s==='a[href="#quiz/consumo/compare"]')return route==='choice'?target('compare',750):null;
    if(s==='.quiz-comparison')return route==='compare'?{getBoundingClientRect(){return {bottom:1100-appWin.scrollY};}}:null;
    return null;
  }};
  const webDoc={documentElement:{style:{},scrollHeight:4000},querySelector(){return el();},createElement:el,head:{appendChild(style){styles.push(style.textContent);}}};
  const web={contentDocument:webDoc,contentWindow:webWin},app={contentDocument:appDoc,contentWindow:appWin};
  const scene=el();scene.querySelector=s=>({'.s8-web':web,'.s8-app':app,'.s8-typed':typed,'.s8-enter':enter,'.s8-status':status})[s];
  const slide={querySelector(){return scene;}};
  const context={window:{},AbortController,console,performance:{now:()=>time},setTimeout(fn,ms){tasks.set(++id,{at:time+ms,fn});return id;},clearTimeout(i){tasks.delete(i);}};
  vm.runInNewContext(source,context);
  async function advance(limit=60000){
    const end=time+limit;
    for(let n=0;n<20000;n++){
      for(let k=0;k<8;k++)await Promise.resolve();
      const pair=[...tasks].sort((a,b)=>a[1].at-b[1].at)[0];
      if(!pair||pair[1].at>end){time=end;return;}
      time=pair[1].at;tasks.delete(pair[0]);pair[1].fn();
    }
    throw Error('Timers did not settle');
  }
  return {api:context.window.BioferiaSlide8,slide,scene,events,eventTimes,styles,typed,status,web,app,webDoc,webWin,appWin,advance,tasks,reset(){route='home';answer=false;events.length=0;eventTimes.length=0;}};
}
(async()=>{
  for(const height of [4000,12000]){
    const sync=harness();sync.webDoc.documentElement.scrollHeight=height;
    const playback=sync.api.start(sync.slide);
    await sync.advance(8000);
    const sideY=sync.webWin.scrollY;
    // Simular contenido que cambia de alto despues de reducir la web.
    sync.webDoc.documentElement.scrollHeight+=1800;
    await sync.advance(13000);
    const bottom=sync.webDoc.documentElement.scrollHeight-sync.webWin.innerHeight;
    assert.equal(sync.events.at(-1),'compare');
    assert.ok(sync.webWin.scrollY>sideY);
    assert.ok(Math.abs(sync.webWin.scrollY-230*18.5)<5,'Ritmo intermedio constante aunque cambie la altura');
    const before=sync.webWin.scrollY;
    assert.ok(before<bottom,'No forzar llegada al final junto con el quiz');
    await sync.advance(500);
    assert.ok(Math.abs(sync.webWin.scrollY-before-115)<5,'Mantener el mismo ritmo despues de la comparacion');
    sync.api.stop();await sync.advance();await playback;assert.equal(sync.tasks.size,0);
  }
  const h=harness();let run=h.api.start(h.slide);
  await h.advance(4000);assert.equal(h.typed.textContent,'www.bioferia.com.ar');assert.equal(h.events.length,0);
  await h.advance(4000);assert.ok(h.scene.classList.contains('split'));const sideScroll=h.webWin.scrollY;
  await h.advance(4000);assert.ok(h.webWin.scrollY>sideScroll);assert.deepEqual(h.events,['question']);
  await h.advance(13999);assert.equal(h.scene.dataset.finished,undefined);
  await h.advance(1);await run;
  assert.deepEqual(h.events,['question','answer','choice','compare']);
  assert.equal(h.scene.dataset.finished,'true');assert.equal(h.status.textContent,'');
  assert.deepEqual(h.eventTimes,[11000,14500,17800,21000]);assert.ok(h.appWin.scrollY>0);
  assert.ok(h.styles.some(css=>css.includes('.leaf-fly{display:none!important}')));
  const afterQuiz=h.webWin.scrollY;await h.advance(1000);assert.notEqual(h.webWin.scrollY,afterQuiz);
  h.api.stop();assert.equal(h.web.src,'about:blank');assert.equal(h.app.src,'about:blank');
  h.reset();run=h.api.start(h.slide);await h.advance(5000);h.api.stop();await h.advance();await run;
  assert.deepEqual(h.events,[]);assert.equal(h.tasks.size,0);assert.equal(h.scene.dataset.finished,undefined);
  h.reset();run=h.api.start(h.slide);await h.advance();await run;
  assert.deepEqual(h.events,['question','answer','choice','compare']);
  h.api.stop();h.reset();run=h.api.start(h.slide);await h.advance(15500);
  const beforeExit=h.events.slice();assert.ok(beforeExit.length>0&&beforeExit.length<4);
  h.api.stop();await h.advance();await run;assert.deepEqual(h.events,beforeExit);assert.equal(h.tasks.size,0);
  console.log('PASS: steady intermediate scroll at 230px/s, dynamic page heights, 26-second timeline, app at 8s, continuous scroll, hidden leaf, quiz, cancellation, restart');
})().catch(e=>{console.error(e);process.exitCode=1;});
