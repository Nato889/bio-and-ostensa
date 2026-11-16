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
    async function scroll(win,y,duration){
      const from=win.scrollY, begin=performance.now();
      do{const p=Math.min(1,(performance.now()-begin)/duration),ease=p*p*(3-2*p);win.scrollTo(0,from+(y-from)*ease);if(p===1)break;await wait(16);}while(!signal.aborted);
    }
    function unload(){web.src='about:blank';app.src='about:blank';}
    signal.addEventListener('abort',unload,{once:true});
    web.src='web-demo/index.html';app.src='app-real/pitch.html#home';
    try{
      await wait(650);
      for(const letter of 'www.bioferia.com.ar'){typed.textContent+=letter;await wait(letter==='.'?180:100);}
      await wait(450);enter.classList.add('pressed');await wait(220);enter.classList.remove('pressed');
      const webDoc=await until(()=>web.contentDocument?.querySelector('#inicio')&&web.contentDocument);
      webDoc.documentElement.style.scrollBehavior='auto';
      const scrollbar=webDoc.createElement('style');scrollbar.textContent='html{scrollbar-width:none}::-webkit-scrollbar{display:none}';webDoc.head.appendChild(scrollbar);
      web.contentWindow.scrollTo(0,0);scene.classList.add('web-open');
      await wait(3000);
      const max=Math.max(0,webDoc.documentElement.scrollHeight-web.contentWindow.innerHeight);
      const section=webDoc.getElementById('quienes');
      const target=Math.min(max,section?section.getBoundingClientRect().top+web.contentWindow.scrollY:2000);
      await scroll(web.contentWindow,target,8000);await wait(1000);
      const appDoc=await until(()=>app.contentDocument?.querySelector('.page-home')&&app.contentDocument);
      await wait(700);scene.classList.add('split');await wait(3000);
      const win=app.contentWindow, hand=appDoc.querySelector('.pitch-hand');
      async function tap(selector){
        const el=await until(()=>appDoc.querySelector(selector));
        let rect=el.getBoundingClientRect();
        if(rect.top<55||rect.bottom>win.innerHeight-90){
          hand.classList.remove('visible');
          await scroll(win,Math.max(0,win.scrollY+rect.top-win.innerHeight*.45),1000);await wait(500);rect=el.getBoundingClientRect();
        }
        hand.classList.add('visible');
        hand.style.left=(rect.left+rect.width*.62)+'px';hand.style.top=(rect.top+rect.height*.5)+'px';
        await wait(950);hand.classList.add('press');await wait(180);
        if(el.disabled)throw new Error('La opcion todavia no esta disponible');
        el.click();hand.classList.remove('press');await wait(450);
      }
      await tap('a[href="#quiz/consumo"]');
      await until(()=>appDoc.querySelector('[data-action="answer"]'));
      hand.classList.remove('visible');await wait(2600);
      await tap('[data-action="answer"][data-value="1"]');await wait(1200);
      await tap('[data-action="quiz-next"]');
      await until(()=>appDoc.querySelector('a[href="#quiz/consumo/compare"]'));
      hand.classList.remove('visible');await wait(2400);
      await tap('a[href="#quiz/consumo/compare"]');
      const comparison=await until(()=>appDoc.querySelector('.quiz-comparison'));
      hand.classList.remove('visible');await wait(1000);
      // Dejar la eleccion y las otras miradas juntas, sin seguir de largo.
      const bottom=comparison.getBoundingClientRect().bottom;
      if(bottom>win.innerHeight-40)await scroll(win,win.scrollY+bottom-win.innerHeight+60,1200);
      scene.dataset.finished='true';
    }catch(error){
      if(!signal.aborted){status.textContent='Volvé a esta slide para reiniciar la experiencia.';console.error('Slide 8:',error);}
    }
  }
  window.BioferiaSlide8={start,stop};
})();
