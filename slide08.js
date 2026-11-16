/* Slide 8: la web y la app reales, en una demostracion local reproducible. */
(function(){
  'use strict';
  let current=null;
  function stop(){
    if(!current)return;
    current.abort(); current=null;
  }
  async function start(slide){
    stop();
    const scene=slide.querySelector('.s8-sequence');
    if(!scene)return;
    const run=new AbortController();current=run;
    const started=performance.now();
    const signal=run.signal, web=scene.querySelector('.s8-web'), app=scene.querySelector('.s8-app');
    const typed=scene.querySelector('.s8-typed'), enter=scene.querySelector('.s8-enter'), status=scene.querySelector('.s8-status');
    scene.classList.remove('web-open','split');delete scene.dataset.finished;typed.textContent='';enter.classList.remove('pressed');status.textContent='';
    function wait(ms){return new Promise((resolve,reject)=>{
      if(signal.aborted){reject(new Error('stopped'));return;}
      const cancel=()=>{clearTimeout(timer);reject(new Error('stopped'));};
      const timer=setTimeout(()=>{signal.removeEventListener('abort',cancel);resolve();},ms);
      signal.addEventListener('abort',cancel,{once:true});
    });}
    async function until(check){
      for(let i=0;i<200;i++){if(signal.aborted)throw new Error('stopped');const value=check();if(value)return value;await wait(100);}
      throw new Error('No se pudo cargar la demostracion');
    }
    const at=ms=>wait(Math.max(0,started+ms-performance.now()));
    async function scroll(win,y,duration){
      const from=win.scrollY, begin=performance.now();
      do{const p=Math.min(1,(performance.now()-begin)/duration),ease=p*p*(3-2*p);win.scrollTo(0,from+(y-from)*ease);if(p===1)break;await wait(16);}while(!signal.aborted);
    }
    async function keepWebScrolling(doc){
      const win=web.contentWindow;
      let last=performance.now(),direction=1;
      while(!signal.aborted){
        await wait(16);
        const now=performance.now(),max=Math.max(0,doc.documentElement.scrollHeight-win.innerHeight);
        let y=win.scrollY+direction*145*(now-last)/1000;last=now;
        // Al llegar al extremo, volver sin pausas ni saltar de golpe al inicio.
        if(y>max){y=Math.max(0,2*max-y);direction=-1;}
        else if(y<0){y=Math.min(max,-y);direction=1;}
        win.scrollTo(0,y);
      }
    }
    function unload(){web.src='about:blank';app.src='about:blank';}
    signal.addEventListener('abort',unload,{once:true});
    web.src='web-demo/index.html';app.src='app-real/pitch.html#home';
    try{
      await at(350);
      for(const letter of 'www.bioferia.com.ar'){typed.textContent+=letter;await wait(letter==='.'?100:65);}
      await at(2100);enter.classList.add('pressed');await wait(180);enter.classList.remove('pressed');
      const webDoc=await until(()=>web.contentDocument?.querySelector('#inicio')&&web.contentDocument);
      webDoc.documentElement.style.scrollBehavior='auto';
      const scrollbar=webDoc.createElement('style');scrollbar.textContent='html{scrollbar-width:none}::-webkit-scrollbar{display:none}.leaf-fly{display:none!important}';webDoc.head.appendChild(scrollbar);
      await at(2500);web.contentWindow.scrollTo(0,0);scene.classList.add('web-open');
      keepWebScrolling(webDoc).catch(error=>{if(!signal.aborted)console.error('Slide 8 scroll:',error);});
      const appDoc=await until(()=>app.contentDocument?.querySelector('.page-home')&&app.contentDocument);
      await at(8000);scene.classList.add('split');await at(9500);
      const win=app.contentWindow, hand=appDoc.querySelector('.pitch-hand');
      async function tap(selector,clickAt){
        const el=await until(()=>appDoc.querySelector(selector));
        let rect=el.getBoundingClientRect();
        if(rect.top<55||rect.bottom>win.innerHeight-90){
          hand.classList.remove('visible');
          await scroll(win,Math.max(0,win.scrollY+rect.top-win.innerHeight*.45),600);await wait(120);rect=el.getBoundingClientRect();
        }
        hand.classList.add('visible');
        hand.style.left=(rect.left+rect.width*.62)+'px';hand.style.top=(rect.top+rect.height*.5)+'px';
        await wait(700);await at(clickAt-120);hand.classList.add('press');await wait(120);
        if(el.disabled)throw new Error('La opcion todavia no esta disponible');
        el.click();hand.classList.remove('press');await wait(180);
      }
      await tap('a[href="#quiz/consumo"]',11000);
      await until(()=>appDoc.querySelector('[data-action="answer"]'));
      hand.classList.remove('visible');await at(12700);
      await tap('[data-action="answer"][data-value="1"]',14500);await at(16000);
      await tap('[data-action="quiz-next"]',17800);
      await until(()=>appDoc.querySelector('a[href="#quiz/consumo/compare"]'));
      hand.classList.remove('visible');await at(19200);
      await tap('a[href="#quiz/consumo/compare"]',21000);
      const comparison=await until(()=>appDoc.querySelector('.quiz-comparison'));
      hand.classList.remove('visible');await at(21800);
      // Dejar la eleccion y las otras miradas juntas, sin seguir de largo.
      const bottom=comparison.getBoundingClientRect().bottom;
      if(bottom>win.innerHeight-40)await scroll(win,win.scrollY+bottom-win.innerHeight+60,600);
      await at(26000);
      scene.dataset.finished='true';
    }catch(error){
      if(!signal.aborted){status.textContent='Volvé a esta slide para reiniciar la experiencia.';console.error('Slide 8:',error);}
    }
  }
  window.BioferiaSlide8={start,stop};
})();
