/* BioFeria · El hecho · EXPRESS — motor de pantallas */
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide')), N=slides.length, cur=-1, t0=null;
  var root=document.documentElement;
  var cnt=document.getElementById('cnt'), bar=document.querySelector('#prog i'), tm=document.getElementById('tm');
  var notes=document.getElementById('notes'), help=document.getElementById('help'), mute=document.getElementById('mute');
  var TARGET=15*60;

  /* ---- escala del lienzo ---- */
  function fit(){ root.style.setProperty('--s',Math.min(innerWidth/1920,innerHeight/1080)); }
  addEventListener('resize',fit); fit();

  /* ---- letras sueltas: <… class="sp"> se parte en <i> con trayectorias al azar ---- */
  function rnd(seed){ var x=Math.sin(seed*9999.13)*10000; return x-Math.floor(x); }
  function splitNode(node,ctr){
    [].slice.call(node.childNodes).forEach(function(ch){
      if(ch.nodeType===3){
        var f=document.createDocumentFragment();
        ch.textContent.split(/(\s+)/).forEach(function(tok){
          if(!tok) return;
          if(/^\s+$/.test(tok)){ f.appendChild(document.createTextNode(' ')); return; }
          var w=document.createElement('span'); w.style.cssText='display:inline-block;white-space:nowrap';
          tok.split('').forEach(function(c){
            var i=document.createElement('i'); i.textContent=c;
            var k=ctr.n++;
            i.style.setProperty('--k',k);
            i.style.setProperty('--ox',Math.round((rnd(k+1)-.5)*900)+'px');
            i.style.setProperty('--oy',Math.round(-300-rnd(k+7)*700)+'px');
            i.style.setProperty('--or',Math.round((rnd(k+3)-.5)*220)+'deg');
            w.appendChild(i);
          });
          f.appendChild(w);
        });
        node.replaceChild(f,ch);
      }else if(ch.nodeType===1&&ch.tagName!=='I'&&ch.tagName!=='BR'){ splitNode(ch,ctr); }
    });
  }
  [].forEach.call(document.querySelectorAll('.sp'),function(el){ splitNode(el,{n:0}); });

  /* ---- contadores ---- */
  function runCount(el){
    var to=parseFloat(el.dataset.to||'0'), dur=parseFloat(el.dataset.dur||'1800'), s=null;
    function step(ts){ if(s===null) s=ts; var p=Math.min(1,(ts-s)/dur), e=1-Math.pow(1-p,3);
      el.textContent=Math.round(to*e); if(p<1&&el._on) requestAnimationFrame(step); }
    el._on=true; el.textContent='0'; requestAnimationFrame(step);
  }

  /* ---- montaje final ---- */
  var mtgTimer=null;
  var mtgDelay=null;
  function runMontage(sl){
    var box=sl.querySelector('.mtg'); if(!box) return;
    var im=[].slice.call(box.querySelectorAll('img')), k=0;
    sl.classList.remove('fin-on'); im.forEach(function(x){x.classList.remove('on');});
    clearInterval(mtgTimer); clearTimeout(mtgDelay);
    mtgDelay=setTimeout(function(){
      if(!sl.classList.contains('on')) return;
      mtgTimer=setInterval(function(){
        if(!sl.classList.contains('on')){ clearInterval(mtgTimer); return; }
        im.forEach(function(x){x.classList.remove('on');});
        if(k<im.length){ im[k].classList.add('on'); k++; }
        else{ clearInterval(mtgTimer); im[im.length-1].classList.add('on'); sl.classList.add('fin-on'); }
      },105);
    },(parseFloat(box.dataset.start)||0)*1000);
  }

  /* ---- video / iframes ---- */
  function media(i){
    slides.forEach(function(s,k){
      var on=(k===i);
      [].forEach.call(s.querySelectorAll('video.av'),function(v){
        if(on){
          if(!v.getAttribute('src')&&v.dataset.src){
            v.setAttribute('src',v.dataset.src);
            if(v.dataset.src2){ v.addEventListener('error',function(){ if(v.getAttribute('src')!==v.dataset.src2){ v.setAttribute('src',v.dataset.src2); try{v.load();}catch(e){} var q=v.play(); if(q&&q.catch) q.catch(function(){}); } },{once:true}); }
          }
          v.muted=true; try{v.currentTime=0;}catch(e){}
          if(v.dataset.rate) v.playbackRate=parseFloat(v.dataset.rate);
          clearTimeout(v._at);
          if(v.dataset.at){ v.pause(); v._at=setTimeout(function(){ try{v.currentTime=parseFloat(v.dataset.from||0);}catch(e){} var q=v.play(); if(q&&q.catch) q.catch(function(){}); },parseFloat(v.dataset.at)*1000); }
          else{ var p=v.play(); if(p&&p.catch) p.catch(function(){}); }
        }else{ clearTimeout(v._at); v.pause(); }
      });
      if(Math.abs(k-i)<=1){
        [].forEach.call(s.querySelectorAll('iframe[data-src]'),function(f){ if(f.getAttribute('src')!==f.getAttribute('data-src')) f.setAttribute('src',f.getAttribute('data-src')); });
      }
      [].forEach.call(s.querySelectorAll('iframe.pitch-web'),function(f){
        clearTimeout(f._dl);
        var send=function(){ try{f.contentWindow.postMessage(on?'pitch-start':'pitch-stop','*');}catch(e){} };
        if(on && f.dataset.delay){ f._dl=setTimeout(send,parseFloat(f.dataset.delay)); } else { send(); }
      });
      if(!on){ [].forEach.call(s.querySelectorAll('.ophone'),function(e){e.classList.remove('tilt');}); [].forEach.call(s.querySelectorAll('.dlimg'),function(e){e.classList.remove('on');}); }
      [].forEach.call(s.querySelectorAll('.runner'),function(box){
        if(box._raf){ cancelAnimationFrame(box._raf); box._raf=0; }
        if(!on) return;
        var d=box.dataset, cx=+d.cx, cy=+d.cy, rx=+d.rx, ry=+d.ry, per=(+d.per)*1000, w=+d.w, feet=+d.feet;
        var im=[].slice.call(box.querySelectorAll('img.rb')), bear=box.querySelector('.bear'), t0=performance.now(), seq=[0,1,0,2];
        (function f(now){
          var a=2*Math.PI*(now-t0)/per, x=cx+rx*Math.cos(a), y=cy+ry*Math.sin(a), dir=(-Math.sin(a))>=0?1:-1;
          var fr=Math.floor((now-t0)/105)%4, bob=(fr%2===0)?0:-10;
          im.forEach(function(e,k){ e.style.opacity=(k===seq[fr])?1:0; });
          bear.style.transform='translate('+Math.round(x-w/2)+'px,'+Math.round(y-feet+bob)+'px) scaleX('+dir+')';
          box._raf=requestAnimationFrame(f);
        })(t0);
      });
      [].forEach.call(s.querySelectorAll('.vch'),function(box){
        var vs=[].slice.call(box.querySelectorAll('video')), rate=parseFloat(box.dataset.rate)||1, rates=(box.dataset.rates||'').split(',').map(parseFloat), lens=(box.dataset.lens||'').split(',').map(parseFloat);
        vs.forEach(function(v){ v.onended=null; }); clearTimeout(box._lt);
        if(!on){ vs.forEach(function(v){ v.pause(); v.classList.remove('act'); }); return; }
        vs.forEach(function(v){ if(!v.getAttribute('src')) v.setAttribute('src',v.dataset.src); v.muted=true; v.preload='auto'; v.pause(); try{v.currentTime=0;}catch(e){} v.classList.remove('act'); });
        var cur=-1; function go(k){ cur=k; var v0=vs[k]; v0.classList.add('act'); setTimeout(function(){ vs.forEach(function(w,n){ if(n!==k){ w.classList.remove('act'); w.pause(); } }); },380); var v=vs[k]; try{v.currentTime=0;}catch(e){} v.playbackRate=rates[k]||rate; clearTimeout(box._lt); if(lens[k]){ box._lt=setTimeout(function(){ go((k+1)%vs.length); },lens[k]*1000); } var q=v.play(); if(q&&q.catch) q.catch(function(){}); }
        vs.forEach(function(v,n){ v.onended=function(){ if(cur===n) go((n+1)%vs.length); }; });
        go(0);
      });
      [].forEach.call(s.querySelectorAll('.chain'),function(box){
        var c1=box.querySelector('.c1'), c2=box.querySelector('.c2');
        if(on){
          [c1,c2].forEach(function(v){ if(!v.getAttribute('src')) v.setAttribute('src',v.dataset.src); v.muted=true; v.preload='auto'; });
          box.classList.remove('p2'); c2.pause(); try{c2.currentTime=0;}catch(e){}
          c1.onended=function(){ box.classList.add('p2'); try{c2.currentTime=0;}catch(e){} var q=c2.play(); if(q&&q.catch) q.catch(function(){}); };
          c2.onended=function(){ box.classList.remove('p2'); try{c1.currentTime=0;}catch(e){} var q=c1.play(); if(q&&q.catch) q.catch(function(){}); };
          try{c1.currentTime=0;}catch(e){} var p1=c1.play(); if(p1&&p1.catch) p1.catch(function(){});
        }else{ c1.onended=c2.onended=null; c1.pause(); c2.pause(); }
      });
      [].forEach.call(s.querySelectorAll('.vseq'),function(box){
        clearInterval(box._iv);
        var v=box.querySelector('video'), lab=box.querySelector('.vlab'), num=box.querySelector('.vnum'), list=(box.dataset.seq||'').split('|'), names=(box.dataset.names||'').split('|'), k=0;
        function show(n){ v.setAttribute('src',list[n]); v.muted=true; try{v.currentTime=0;}catch(e){} var p=v.play(); if(p&&p.catch) p.catch(function(){}); if(lab) lab.textContent=names[n]||''; if(num) num.textContent=String(n+1).padStart(2,'0')+' / '+String(list.length).padStart(2,'0'); }
        if(on){ show(0); box._iv=setInterval(function(){ k=(k+1)%list.length; show(k); },(parseFloat(box.dataset.each)||4)*1000); }
        else{ v.pause(); }
      });
      [].forEach.call(s.querySelectorAll('.cnt-n'),function(el){ if(on) runCount(el); else el._on=false; });
      if(on) runMontage(s); else s.classList.remove('fin-on');
    });
    var has=slides[i].querySelector('video.av[data-snd]');
    mute.classList.toggle('show',!!has);
  }

  /* ---- navegación ---- */
  function go(i){
    i=Math.max(0,Math.min(N-1,i)); if(i===cur) return;
    var old=cur; cur=i;
    slides.forEach(function(s,k){
      if(k===i){ s.classList.remove('out'); s.classList.add('on'); }
      else if(k===old){ s.classList.remove('on'); s.classList.add('out'); clearTimeout(s._t); s._t=setTimeout(function(){s.classList.remove('out');},950); }
      else{ s.classList.remove('on','out'); }
    });
    document.body.classList.toggle('clean',slides[i].classList.contains('clean'));document.body.classList.toggle('nologo',slides[i].classList.contains('nologo'));document.body.dataset.tone=slides[i].classList.contains('tone-b')?'b':'a';
    cnt.textContent=String(i+1).padStart(2,'0')+' / '+String(N).padStart(2,'0');
    bar.style.width=((i+1)/N*100)+'%';
    document.getElementById('prev').disabled=i===0; document.getElementById('next').disabled=i===N-1;
    var a=slides[i].querySelector('aside.n'); notes.innerHTML=a?a.innerHTML:'';
    media(i);
    if(i>0&&t0===null){ t0=Date.now(); }
    try{history.replaceState(null,'','#'+(i+1));}catch(e){}
  }
  function next(){ go(cur+1); } function prev(){ go(cur-1); }

  document.getElementById('next').addEventListener('click',function(e){e.stopPropagation();next();});
  document.getElementById('prev').addEventListener('click',function(e){e.stopPropagation();prev();});
  addEventListener('keydown',function(e){
    var k=e.key;
    if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='Enter'){e.preventDefault();next();}
    else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'){e.preventDefault();prev();}
    else if(k==='Home'){go(0);} else if(k==='End'){go(N-1);}
    else if(k==='f'||k==='F'){ if(!document.fullscreenElement) document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen(); else document.exitFullscreen(); }
    else if(k==='n'||k==='N'){ notes.classList.toggle('show'); }
    else if(k==='t'||k==='T'){ tm.classList.toggle('show'); if(t0===null) t0=Date.now(); }
    else if(k==='m'||k==='M'){ toggleSound(); }
  });
  function toggleSound(){
    var v=slides[cur].querySelector('video.av[data-snd]'); if(!v) return;
    v.muted=!v.muted; if(!v.muted){ v.volume=.35; var p=v.play(); if(p&&p.catch)p.catch(function(){}); }
    mute.textContent=v.muted?'🔇 M · activar sonido':'🔊 M · silenciar';
  }
  mute.addEventListener('click',function(e){e.stopPropagation();toggleSound();});
  document.getElementById('stage').addEventListener('click',function(e){
    if(e.target.closest('video[controls]')) return;
    (e.clientX<innerWidth*.28)?prev():next();
  });
  var sx=null; addEventListener('touchstart',function(e){sx=e.touches[0].clientX;},{passive:true});
  addEventListener('touchend',function(e){ if(sx===null)return; var dx=e.changedTouches[0].clientX-sx; if(Math.abs(dx)>50){dx<0?next():prev();} sx=null; },{passive:true});

  /* ---- cronómetro (T) ---- */
  setInterval(function(){
    if(t0===null){ tm.textContent='00:00 / 15:00'; return; }
    var s=Math.floor((Date.now()-t0)/1000), m=Math.floor(s/60), r=s%60;
    tm.textContent=String(m).padStart(2,'0')+':'+String(r).padStart(2,'0')+' / 15:00';
    tm.classList.toggle('over',s>TARGET);
  },500);

  help.classList.add('show'); setTimeout(function(){help.classList.remove('show');},5000);
  var h=parseInt((location.hash||'').slice(1),10);
  go(isNaN(h)?0:h-1);
})();

window.addEventListener('message',function(ev){
  if(ev.data!=='oso-dl'&&ev.data!=='oso-dl-off') return;
  var on=(ev.data==='oso-dl');
  [].forEach.call(document.querySelectorAll('.slide.on .ophone'),function(e){e.classList.toggle('tilt',on);});
  [].forEach.call(document.querySelectorAll('.slide.on .dlimg'),function(e){e.classList.toggle('on',on);});
});
