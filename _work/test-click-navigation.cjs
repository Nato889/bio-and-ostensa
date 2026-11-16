const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'express.js'), 'utf8');
const start = source.indexOf("  document.getElementById('stage').addEventListener('click'");
const end = source.indexOf('  var sx=null;', start);
let click;
const moves = [];
const context = {
  innerWidth:1920,
  document:{getElementById(){return {addEventListener(name, fn){click = fn;}};}},
  prev(){moves.push('prev');}, next(){moves.push('next');}
};
vm.runInNewContext(source.slice(start, end), context);
function tap(x, interactive=false){click({clientX:x, target:{closest(){return interactive;}}});}
for(const width of [390, 1920]){
  context.innerWidth = width; moves.length = 0;
  for(const x of [.15, .25, .49, .5, .51, .75, .85]) tap(width*x);
  assert.deepEqual(moves, [], 'El centro, incluso junto al play, no navega');
  tap(0); tap(width); assert.deepEqual(moves, ['prev', 'next']);
  moves.length = 0; tap(0, true); tap(width, true); tap(width*.5, true);
  assert.deepEqual(moves, [], 'Los controles interactivos no navegan');
}
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const css = fs.readFileSync(path.join(root, 'express.css'), 'utf8');
assert.match(html, /class="bleed intro-video"><video[^>]+data-manual="1"/);
assert.match(css, /\.intro-video\{z-index:1\}/);
assert.match(css, /\.video-start\[hidden\]\{display:none\}/);
console.log('PASS: navegacion solo en extremos 15%, centro y controles seguros; capa del play por encima del lienzo.');
