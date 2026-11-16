const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../express.js'), 'utf8');
const setup = source.slice(source.indexOf("  [].forEach.call(document.querySelectorAll('.video-start')"), source.indexOf('  function media(i)'));
const playback = source.slice(source.indexOf("      [].forEach.call(s.querySelectorAll('video.av')"), source.indexOf('      if(Math.abs(k-i)<=1)'));
let active = true, plays = 0, stopped = 0;
const events = {}, videoEvents = {};
const slide = {classList:{contains(){return active;}}, querySelectorAll(){return [video];}};
const button = {
  hidden:false, blur(){}, closest(){return slide;},
  addEventListener(name, fn){events[name] = fn;},
  parentNode:{querySelector(){return video;}}
};
const video = {
  dataset:{manual:'1',src:'intro.mp4'}, currentTime:42,
  parentNode:{querySelector(){return button;}},
  addEventListener(name, fn){videoEvents[name] = fn;},
  getAttribute(name){return this[name];}, setAttribute(name, value){this[name] = value;},
  pause(){this.paused = true;}, play(){plays++; this.paused = false; return Promise.resolve();}
};
const context = {document:{querySelectorAll(){return [button];}}, s:slide, on:true, clearTimeout(){}};
vm.runInNewContext(setup, context);
vm.runInNewContext(playback, context);
assert.equal(plays, 0); assert.equal(video.paused, true); assert.equal(video.currentTime, 0); assert.equal(button.hidden, false);
events.click({stopPropagation(){stopped++;}});
assert.equal(plays, 1); assert.equal(stopped, 1);
assert.equal(button.hidden, false); // Sigue disponible si el navegador no logra iniciar.
videoEvents.playing(); assert.equal(button.hidden, true);
for(const key of ['Enter', ' ']) events.keydown({key, stopPropagation(){stopped++;}});
assert.equal(stopped, 3);
context.on = false; active = false; vm.runInNewContext(playback, context);
assert.equal(video.paused, true);
events.click({stopPropagation(){}}); assert.equal(plays, 1);
context.on = true; active = true; video.currentTime = 20; vm.runInNewContext(playback, context);
assert.equal(video.currentTime, 0); assert.equal(button.hidden, false); assert.equal(plays, 1);
delete video.dataset.manual; vm.runInNewContext(playback, context); assert.equal(plays, 2);
console.log('PASS: intro pausada, play por clic sin avanzar, teclado accesible, ocultar al reproducir, salida/reentrada y autoplay de otros videos.');
