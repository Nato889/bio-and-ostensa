#!/usr/bin/env python3
"""Arma index.html del pitch EXPRESS: corre _work/gen.py (pantallas) y las mete en template.html."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.check_call([sys.executable, '_work/gen.py'])
slides = open('slides/express.html', encoding='utf-8').read()
tpl = open('template.html', encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(tpl.replace('<!--SLIDES-->', slides))
print('index.html listo:', slides.count('<section'), 'pantallas')
