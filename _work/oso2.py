import re
from PIL import Image
src=open('../pitch-hecho-2d/game3.js',encoding='utf-8').read()
m=re.search(r"var BEAR=\[(.*?)\];",src,re.S)
BEAR=re.findall(r"'([^']+)'",m.group(1))
INK=(0x2b,0x27,0x2c);Y=(0xfd,0xff,0x1a);RED=(0xf4,0x45,0x30);BLUE=(0x0c,0x6f,0xdc);VIO=(0x77,0x79,0xde);CR=(0xf0,0xee,0xe4)
W,H,OX,OY=30,38,3,8
def base(fill):
    g={}
    for y,row in enumerate(BEAR):
        lo=row.find('X');hi=row.rfind('X')
        if lo<0:continue
        for x in range(lo,hi+1):g[(x,y)]=INK if row[x]=='X' else fill
    for y in range(21,24):
        for x in range(5,19):
            if g.get((x,y))==INK:g[(x,y)]=fill
    for y in range(24,28):
        g.pop((11,y),None);g.pop((12,y),None)
    for y in range(24,27):g[(10,y)]=INK;g[(13,y)]=INK
    g[(10,27)]=INK;g[(13,27)]=INK
    return g
def rect(g,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):g[(x,y)]=c
def save(g,name):
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    for (x,y),c in g.items():
        X,Y_=x+OX,y+OY
        if 0<=X<W and 0<=Y_<H:im.putpixel((X,Y_),c+(255,))
    im.save('assets/oso2/'+name+'.png')
def band(g):
    for y in (3,4,5):
        row=BEAR[y];lo=row.find('X');hi=row.rfind('X')
        for x in range(lo,hi+1):g[(x,y)]=RED
    return g
# A: ciego / abierto
g=base(Y);save(g,'a-open')
g=band(base(Y));rect(g,19,4,20,4,RED);rect(g,20,5,21,6,RED);save(g,'a-blind')
v={}
for y in (3,4,5):
    row=BEAR[y];lo=row.find('X');hi=row.rfind('X')
    for x in range(lo,hi+1):v[(x,y)]=RED
rect(v,19,4,20,4,RED);rect(v,20,5,21,6,RED);save(v,'venda')
# B: sombrero crema
g=base(Y)
rect(g,8,-4,16,0,INK);rect(g,9,-3,15,0,CR);rect(g,9,-1,15,-1,VIO)
rect(g,5,1,19,2,INK);rect(g,6,1,18,1,CR);save(g,'b')
# C: violeta + gorra azul
g=base(VIO)
rect(g,8,-3,16,0,INK);rect(g,9,-2,15,0,BLUE)
rect(g,14,0,22,1,INK);rect(g,15,0,21,0,BLUE);save(g,'c')
# D: rojo + lentes de sol
g=base(RED)
rect(g,8,3,18,4,INK);rect(g,13,3,13,3,INK);rect(g,9,3,9,3,BLUE);rect(g,15,3,15,3,BLUE);
g[(12,4)]=INK;g[(14,4)]=INK;g[(13,4)]=RED;save(g,'d')

# ---- variantes de gesto (pantalla 2) ----
def outline_add(g, pix, ink=INK):
    for (x, y) in list(pix):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in pix and q not in g:
                g[q] = ink
# B sonríe: sonrisa grande + rubor
g = base(Y)
g.update({(10, 9): INK, (11, 10): INK, (12, 10): INK, (13, 10): INK, (14, 10): INK, (15, 10): INK, (16, 9): INK})
rect(g, 8, -4, 16, 0, INK); rect(g, 9, -3, 15, 0, CR); rect(g, 9, -1, 15, -1, VIO)
rect(g, 5, 1, 19, 2, INK); rect(g, 6, 1, 18, 1, CR)
g[(8, 8)] = RED; g[(9, 8)] = RED; g[(17, 8)] = RED; g[(18, 8)] = RED
save(g, 'b-smile')
# D hace "ok" con el pulgar
g = base(RED)
rect(g, 8, 3, 18, 4, INK); g[(13, 3)] = INK; g[(9, 3)] = BLUE; g[(15, 3)] = BLUE
g[(12, 4)] = INK; g[(14, 4)] = INK; g[(13, 4)] = RED
hand = {}
for (x0, y0, x1, y1) in ((23, 5, 24, 7), (22, 8, 26, 12), (19, 12, 22, 14)):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): hand[(x, y)] = RED
for k_, v_ in hand.items(): g[k_] = v_
outline_add(g, hand)
save(g, 'd-ok')
# corazoncito pixel (9x8)
HEART = ['.##.##.', '#######', '#######', '.#####.', '..###..', '...#...']
hp = {(x + 1, y + 1): RED for y, row in enumerate(HEART) for x, c in enumerate(row) if c == '#'}
hg = dict(hp); outline_add(hg, hp)
im = Image.new('RGBA', (9, 8), (0, 0, 0, 0))
for (x, y), c in hg.items():
    if 0 <= x < 9 and 0 <= y < 8: im.putpixel((x, y), c + (255,))
im.save('assets/oso2/heart.png')

# D sonríe (sin mano)
g = base(RED)
rect(g, 8, 3, 18, 4, INK); g[(13, 3)] = INK; g[(9, 3)] = BLUE; g[(15, 3)] = BLUE
g[(12, 4)] = INK; g[(14, 4)] = INK; g[(13, 4)] = RED
g.update({(10, 9): INK, (11, 10): INK, (12, 10): INK, (13, 10): INK, (14, 10): INK, (15, 10): INK, (16, 9): INK})
save(g, 'd-smile')

# ---- cuadros de carrera (pantalla 14): pies que alternan ----
def run_frame(lift):
    g = base(Y)
    if lift:
        x0, x1 = (3, 10) if lift == 'L' else (13, 20)
        moved = {}
        for y in (26, 27):
            for x in range(x0, x1 + 1):
                if (x, y) in g: moved[(x, y - 3)] = g.pop((x, y))
        for k_, v_ in moved.items(): g[k_] = v_
    return g
save(run_frame(None), 'run-a'); save(run_frame('L'), 'run-b'); save(run_frame('R'), 'run-c')
