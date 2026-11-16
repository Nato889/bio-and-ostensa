import random
#!/usr/bin/env python3
"""Genera slides/express.html (todas las pantallas del pitch EXPRESS) a partir de las piezas de assets/.
   Se corre solo desde build.py. Cada pantalla = una función S(...)."""
import os, glob, random
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
_sz = {}
def sz(src):
    if src not in _sz:
        try: _sz[src] = Image.open(src).size
        except Exception: _sz[src] = (1000, 1000)
    return _sz[src]

def _dims(src, w, h):
    iw, ih = sz(src)
    if w is None and h is None: return iw, ih
    if w is None: return round(h * iw / ih), h
    if h is None: return w, round(w * ih / iw)
    return w, h

def _fx(fx, d, r, lp, ld=None, op=None, extra=''):
    c = 'fx f-%s' % fx
    if lp: c += ' l-%s' % lp
    s = '--d:%ss;' % d
    if r: s += '--r:%sdeg;' % r
    if ld: s += '--ld:%ss;' % ld
    if op is not None: s += '--op:%s;' % op
    return c, s + extra

def E(src, x, y, w=None, h=None, fx='pop', d=0, r=0, lp='', ld=None, z=None, cls='ph', op=None, st='', fit=None):
    """imagen suelta con entrada + bucle"""
    w, h = _dims(src, w, h)
    c, s = _fx(fx, d, r, lp, ld, op)
    s += 'left:%dpx;top:%dpx;width:%dpx;height:%dpx;' % (x, y, w, h)
    if z is not None: s += 'z-index:%d;' % z
    if fit: s += 'object-fit:%s;' % fit
    return '<img class="ab %s %s" style="%s%s" src="%s" alt="" loading="lazy">' % (c, cls, s, st, src)

def D(inner, x, y, w=None, h=None, fx='pop', d=0, r=0, lp='', ld=None, z=None, cls='', op=None, st=''):
    c, s = _fx(fx, d, r, lp, ld, op)
    s += 'left:%dpx;top:%dpx;' % (x, y)
    if w: s += 'width:%dpx;' % w
    if h: s += 'height:%dpx;' % h
    if z is not None: s += 'z-index:%d;' % z
    return '<div class="ab %s %s" style="%s%s">%s</div>' % (c, cls, s, st, inner)

def T(html, x, y, size=112, fx='fl', d=0, r=0, lp='', sp=False, color=None, w=None, lh=None, weight=None, z=None, st='', cls=''):
    c, s = _fx(fx, d, r, lp)
    s += 'left:%dpx;top:%dpx;font-size:%dpx;' % (x, y, size)
    if w: s += 'width:%dpx;' % w
    if lh: s += 'line-height:%s;' % lh
    if color: s += 'color:%s;' % color
    if weight: s += 'font-weight:%s;' % weight
    if z is not None: s += 'z-index:%d;' % z
    return '<div class="t %s %s%s" style="%s%s">%s</div>' % (c, 'sp ' if sp else '', cls, s, st, html)

def P(html, x, y, w, size=32, fx='fb', d=0, r=0, color=None, weight=None, lh=None, st='', cls=''):
    c, s = _fx(fx, d, r, '')
    s += 'left:%dpx;top:%dpx;width:%dpx;font-size:%dpx;' % (x, y, w, size)
    if color: s += 'color:%s;' % color
    if weight: s += 'font-weight:%s;' % weight
    if lh: s += 'line-height:%s;' % lh
    return '<div class="p %s %s" style="%s%s">%s</div>' % (c, cls, s, st, html)

def ST(text, x, y, kind='', fx='pop', d=0, r=-3, size=None, lp='', z=6, st=''):
    """cartel con forma amorfa (bordes irregulares, sin cajas rígidas); la sombra dura va en el contenedor"""
    c, s = _fx(fx, d, r, lp)
    s += 'left:%dpx;top:%dpx;z-index:%d;' % (x, y, z)
    fs = ('font-size:%dpx;--j:%.1fpx;' % (size, max(1.0, size / 20.0))) if size else ''
    amo = 1 + (len(text) + x // 7) % 4
    return '<div class="stw %s" style="%s%s"><div class="st amo%d %s" style="%s">%s</div></div>' % (c, s, st, amo, kind, fs, text)

def V(src, poster, x, y, w, h, fx='fl', d=0, r=0, snd=False, controls=False, cls='card', lp='', z=None, fit='cover', st='', src2=None):
    c, s = _fx(fx, d, r, lp)
    s += 'left:%dpx;top:%dpx;width:%dpx;height:%dpx;' % (x, y, w, h)
    if z is not None: s += 'z-index:%d;' % z
    v = '<video class="av" data-src="%s"%s poster="%s" muted loop playsinline preload="none"%s%s style="width:100%%;height:100%%;object-fit:%s;display:block;background:#111"></video>' % (
        src, (' data-src2="%s"' % src2) if src2 else '', poster, ' data-snd="1"' if snd else '', ' controls controlslist="nodownload"' if controls else '', fit)
    return '<div class="ab %s %s" style="%s%s">%s</div>' % (c, cls, s, st, v)

def MQ(items, x, y, w, h, mt=40, rev=False, vertical=False, gap=18, z=None, st='', cls=''):
    """tira que corre; items = lista de html. Se duplica para el bucle."""
    seq = ''.join(items)
    dup = seq + seq
    g = 'gap:%dpx;' % gap
    inner = '<div class="tk" style="%s">%s</div>' % (g, dup)
    s = 'left:%dpx;top:%dpx;width:%dpx;height:%dpx;--mt:%ss;' % (x, y, w, h, mt)
    if z is not None: s += 'z-index:%d;' % z
    return '<div class="mq %s%s%s" style="%s%s">%s</div>' % ('v ' if vertical else '', 'rev ' if rev else '', cls, s, st, inner)

def IM(src, w=None, h=None, st=''):
    """imagen para usar dentro de una tira"""
    w, h = _dims(src, w, h)
    return '<img src="%s" alt="" loading="lazy" style="width:%dpx;height:%dpx;object-fit:cover;%s">' % (src, w, h, st)

SLIDES = []
TRS = ['circle', 'up', 'left', 'diag', 'zoom', 'blinds']
def BL(html):
    return '<!--BL-->' + html + '<!--/BL-->'

def VB(src, poster='', extra=''):
    return BL('<div class="bleed"><video class="av" data-src="%s" poster="%s" muted loop playsinline preload="none"%s></video></div>' % (src, poster, extra))

def S(tone, title, body, note, secs, tr=None):
    i = len(SLIDES)
    tr = tr or TRS[i % len(TRS)]
    import re as _re
    bleed = ''.join(_re.findall(r'<!--BL-->(.*?)<!--/BL-->', body, _re.S))
    body = _re.sub(r'<!--BL-->(.*?)<!--/BL-->', '', body, flags=_re.S)
    SLIDES.append('<section class="slide tone-%s" data-tr="%s" data-t="%s">%s<div class="fit">\n%s\n</div><aside class="n"><b>~%s s</b> · %s</aside></section>' % (
        tone, tr, title, bleed, body, secs, note))


# ===================================================================================
# PITCH EXPRESS v2 · 22 pantallas en el orden del guion nuevo (seis voces)
# Voces: 1 NATI · 2 SOLE · 3 LU · 4 JOR · 5 MARTU · 6 LOUR
# Piezas que faltan = placeholder (cuadro punteado). Para reemplazarlas basta con dejar el archivo en la ruta indicada.
# ===================================================================================
def PH(label, x, y, w, h, fx='fb', d=0, r=0, z=None, circle=False, sub='placeholder · todavía no está la pieza'):
    inner = '<div style="position:absolute;inset:0;display:grid;place-items:center;text-align:center;padding:30px"><div><div style="font:800 %dpx/1.05 var(--f-ui);text-transform:uppercase;letter-spacing:.06em;color:#fdff1a">%s</div><div style="font:500 22px var(--f-ui);margin-top:14px;opacity:.8">%s</div></div></div>' % (46 if w > 900 else 30, label, sub)
    st = 'background:repeating-linear-gradient(135deg,#3a3540 0 26px,#322e33 26px 52px);outline:4px dashed #fdff1a;outline-offset:-14px;color:#f1ede4;%s' % ('border-radius:50%;' if circle else '')
    return D(inner, x, y, w, h, fx=fx, d=d, r=r, z=z, cls='card', st=st)

def VS(srcs, names, x, y, w, h, each=4, fx='zoom', d=0, r=0, z=None, poster=''):
    """montaje: un video por vez (cada `each` s) con su rótulo; así no se cargan todos juntos"""
    c, s = _fx(fx, d, r, '')
    s += 'left:%dpx;top:%dpx;width:%dpx;height:%dpx;' % (x, y, w, h)
    if z is not None: s += 'z-index:%d;' % z
    return '<div class="ab card vseq %s" style="%s" data-seq="%s" data-names="%s" data-each="%s"><video muted loop playsinline preload="none" poster="%s" style="width:100%%;height:100%%;object-fit:cover;display:block;background:#111"></video><div class="vlab"></div><div class="vnum"></div></div>' % (c, s, '|'.join(srcs), '|'.join(names), each, poster)

def PHONE(src, x, y, w=230, fx='fb', d=0, r=0, ld=6, z=None, lms=None):
    h = round(w * 2.164); sc = w / 390.0
    zz = 'z-index:%d;' % z if z is not None else ''
    return '<div class="phone fx f-%s l-fl" style="--d:%ss;--r:%sdeg;--ld:%ss;left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:%dpx;outline-width:5px;%s"><iframe class="pitch-web"%s data-src="%s" title="app" style="position:absolute;left:0;top:0;width:390px;height:846px;transform:scale(%.4f);transform-origin:0 0;pointer-events:none;border:0" tabindex="-1"></iframe></div>' % (fx, d, r, ld, x, y, w, h, round(w * .14), zz, (' data-ld="%d"' % lms) if lms else '', src, sc)

# ------------------------------------------------------------------ 01 · VOZ 1 · Ostensa
b = ''
vid1 = 'assets/ostensa/final-sin-sonido.mp4'
b += VB(vid1)
S('a clean', 'Ostensa', b, 'VOZ 1 · NATI — «Buenas tardes, somos Ostensa…» Pantalla limpia: solo el video concepto, sin textos, logo ni interfaz.', 70, 'circle')

# ------------------------------------------------------------------ 02 · VOZ 1 · el osito y el punto de partida
TT = 32.0
LT0 = 11.4          # entra el logo (estilo Disney: rebote)
def _pc(t): return '%.3f%%' % (100.0 * t / TT)
def kfw(name, t0, t1, hop=True):
    k = '@keyframes %s{0%%{opacity:0}%s{opacity:0}' % (name, _pc(max(t0 - .01, 0)))
    k += '%s{opacity:1;transform:translateY(%s)}%s{opacity:1;transform:none}' % (_pc(t0), '-50px' if hop else '0', _pc(t0 + .18))
    if t1 is not None:
        k += '%s{opacity:1}%s{opacity:0}100%%{opacity:0}' % (_pc(t1 - .01), _pc(t1))
    else:
        k += '100%{opacity:1;transform:none}'
    return k + '}'
def kfseq(name, pts):
    """pts = [(t, 'transform', easing)], sostiene el último estado"""
    k = '@keyframes %s{' % name
    if pts[0][0] > 0:
        k += '0%%{transform:%s}' % pts[0][1]
    for t, tr, ez in pts:
        k += '%s{transform:%s%s}' % (_pc(t), tr, (';animation-timing-function:' + ez) if ez else '')
    return k + '100%{transform:' + pts[-1][1] + '}}'
css = '<style>.s2 .sp{position:absolute;image-rendering:pixelated;opacity:0;animation-duration:%ss;animation-fill-mode:both;animation-timing-function:steps(1,end)}' % TT
ks = [kfw('sA', .4, 3.6), kfw('sB', 3.6, 5.4)]
ks += ['@keyframes sV{0%%{opacity:0}%s{opacity:1;transform:none}%s{opacity:1;transform:translate(60px,120px) rotate(18deg)}%s{opacity:1;transform:translate(120px,520px) rotate(50deg)}%s{opacity:0}100%%{opacity:0}}' % (_pc(3.59), _pc(4.0), _pc(4.9), _pc(5.0))]
ks += [kfw('sT1', 5.6, None), kfw('sT2', 6.1, None), kfw('sT3', 6.6, None)]
# variantes de gesto (sonríe / ok con el pulgar) y corazoncitos
def _win(name, t0, t1):
    return '@keyframes %s{0%%{opacity:0}%s{opacity:0}%s{opacity:1}%s{opacity:1}%s{opacity:0}100%%{opacity:0}}' % (name, _pc(t0 - .01), _pc(t0), _pc(t1 - .01), _pc(t1))
ks += [_win('sVb', 7.0, 8.9), _win('sVd', 9.0, 10.9)]
def _heart(name, t0):
    return '@keyframes %s{0%%{opacity:0;transform:translate(0,0)}%s{opacity:0;transform:translate(0,0)}%s{opacity:1;transform:translate(0,0)}%s{opacity:1;transform:translate(14px,-56px)}%s{opacity:0;transform:translate(-8px,-120px)}100%%{opacity:0}}' % (name, _pc(t0 - .01), _pc(t0), _pc(t0 + .6), _pc(t0 + 1.2))
ks += [_heart('sH1', 8.0), _heart('sH2', 8.4), _heart('sH3', 8.8)]
# logo: entra desde abajo, pasa de largo, rebota
L = LT0
ks += [kfseq('sLiftL', [(L, 'translateY(640px)', 'ease-in'), (L + .7, 'translateY(330px)', 'ease-out'), (L + 1.4, 'translateY(-70px)', 'ease-in'), (L + 1.9, 'translateY(0)', 'ease-out'),
                        (L + 2.24, 'translateY(-26px)', 'ease-in'), (L + 2.52, 'translateY(0)', 'ease-out'), (L + 2.69, 'translateY(-7px)', 'ease-in'), (L + 2.8, 'translateY(0)', '')])]
# los osos: esperan abajo, el logo los empuja, vuelan, caen sobre el logo
ks += [kfseq('sLiftB', [(L, 'translateY(330px)', 'linear'), (L + .7, 'translateY(330px)', 'ease-out'), (L + 1.4, 'translateY(-150px)', 'ease-out'), (L + 1.4 + .01, 'translateY(-150px)', 'ease-in'),
                        (L + 2.52, 'translateY(0)', 'ease-out'), (L + 2.69, 'translateY(-7px)', 'ease-in'), (L + 2.8, 'translateY(0)', '')])]
# estirar y aplastar (squash & stretch) sobre cada osito
ks += [kfseq('sSq', [(L + .7, 'scaleY(1)', ''), (L + .78, 'scaleY(.85)', 'ease-out'), (L + .95, 'scaleY(1.12)', 'ease-in-out'), (L + 1.25, 'scaleY(1)', ''), (L + 2.52, 'scaleY(1)', ''),
                     (L + 2.57, 'scaleY(.82)', 'ease-out'), (L + 2.77, 'scaleY(1.06)', 'ease-in-out'), (L + 2.9, 'scaleY(1)', '')])]
# una sola hojita del isologotipo que flota alrededor de los osos
_pts = [(16.3, -200, 260, -25, 1), (16.9, 130, 330, 20, .7), (17.5, 470, 400, -15, 1), (18.0, 770, 560, 25, .75), (18.5, 960, 420, -20, 1), (19.0, 1180, 610, 20, .7),
        (19.5, 1360, 470, -18, 1), (20.0, 1700, 330, 25, .8), (20.5, 2150, 140, -20, 1)]
k = '@keyframes sLf{0%{opacity:1;transform:translate(-200px,260px) rotate(-25deg)}'
for t, x, y, r, sx in _pts:
    k += '%s{transform:translate(%dpx,%dpx) rotate(%ddeg) scaleX(%s);animation-timing-function:ease-in-out}' % (_pc(t), x, y, r, sx)
k += '100%{opacity:1;transform:translate(2150px,140px) rotate(-20deg)}}'
ks += [k]
ks += ['@keyframes sBob{0%{transform:translateY(0)}50%{transform:translateY(-10px)}100%{transform:translateY(0)}}']
def look(name, ts):
    k = '@keyframes %s{0%%{transform:none}' % name
    for i, t in enumerate(ts):
        dx = 14 if i % 2 == 0 else -14
        k += '%s{transform:none}%s{transform:translate(%dpx,-24px)}%s{transform:translate(%dpx,0)}%s{transform:none}' % (_pc(t), _pc(t + .12), dx, _pc(t + .3), dx, _pc(t + .48))
    return k + '100%{transform:none}}'
def gest(name, t0, kind):
    seq = {'hop': [(0, 'none'), (.1, 'translateY(-40px)'), (.28, 'none'), (.42, 'translateY(-40px)'), (.6, 'none')],
           'shimmy': [(0, 'none'), (.1, 'translateX(14px)'), (.2, 'translateX(-14px)'), (.3, 'translateX(14px)'), (.4, 'translateX(-14px)'), (.5, 'none')],
           'flex': [(0, 'none'), (.12, 'scaleY(.88)'), (.3, 'scaleY(1.1)'), (.48, 'scaleY(.92)'), (.66, 'scaleY(1.06)'), (.85, 'none')]}[kind]
    k = '@keyframes %s{0%%{transform:none}' % name
    for t1 in (t0, t0 + 1.5):
        for dt, tr in seq:
            k += '%s{transform:%s}' % (_pc(t1 + dt), tr)
    return k + '100%{transform:none}}'
GX = [(440, 670), (840, 840), (1240, 1010)]
for _i, (_a, _b) in enumerate(GX):
    ks += ['@keyframes sGx%d{0%%{left:%dpx}%s{left:%dpx;animation-timing-function:ease-in-out}%s{left:%dpx}100%%{left:%dpx}}' % (_i + 1, _a, _pc(LT0 + 1.0), _a, _pc(LT0 + 2.5), _b, _b)]
ks += [gest('sLk1', 7.0, 'hop'), gest('sLk2', 8.0, 'shimmy'), gest('sLk3', 9.0, 'flex')]
css += ''.join(ks)
for n in ('sA', 'sB', 'sV', 'sT1', 'sT2', 'sT3'): css += '.slide.on .s2 .%s{animation-name:%s}' % (n, n)
css += '.s2 .lift,.s2 .lg{position:absolute;left:0;top:0;width:1920px;height:1080px}'
css += '.slide.on .s2 .lift{animation:sLiftB %ss both}.slide.on .s2 .lg{animation:sLiftL %ss both}' % (TT, TT)
css += '.s2 .bw{position:absolute;width:240px;height:304px;transform-origin:50%% 95%%}.s2 .bw .sp{transform-origin:50%% 95%%}.slide.on .s2 .bw{animation:sSq %ss both}' % TT
for i in (1, 2, 3):
    css += '.slide.on .s2 .bw.k%d{animation:sSq %ss both,sGx%d %ss both}' % (i, TT, i, TT)
    css += '.slide.on .s2 .bw.k%d .sp{animation-name:sT%d}' % (i, i)
    css += '.slide.on .s2 .bw.k%d .gw{animation:sLk%d %ss steps(1,end) both,sBob 1.2s steps(1,end) %ss infinite backwards}' % (i, i, TT, LT0 + 3.2)
css += '.s2 .gw{position:absolute;inset:0;transform-origin:50%% 95%%}.s2 .sv{position:absolute;left:0;top:0;image-rendering:pixelated;opacity:0;animation-duration:%ss;animation-fill-mode:both;animation-timing-function:steps(1,end)}' % TT
css += '.slide.on .s2 .sv.vb{animation-name:sVb}.slide.on .s2 .sv.vd{animation-name:sVd}.s2 .ht{position:absolute;image-rendering:pixelated;opacity:0;animation-duration:%ss;animation-fill-mode:both;animation-timing-function:steps(8,end)}' % TT
css += '.slide.on .s2 .ht.h1{animation-name:sH1}.slide.on .s2 .ht.h2{animation-name:sH2}.slide.on .s2 .ht.h3{animation-name:sH3}'
css += '.s2 .lf{position:absolute;left:0;opacity:0;pointer-events:none;z-index:6}.slide.on .s2 .lf{animation:sLf '+str(TT)+'s both}</style>'
def spr(n, cls, left, top, sc):
    return '<img class="sp %s" src="assets/oso2/%s.png" alt="" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (cls, n, left, top, 30 * sc, 38 * sc)
b = css + '<div class="s2" style="position:absolute;inset:0">'
# primer plano del osito con la venda (de los hombros para arriba, escala entera 44)
SC = 44; CL = 300; CT = 130
b += '<div style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:700px;overflow:hidden">' % (CL, CT, 30 * SC)
b += spr('a-blind', 'sA', 0, -7 * SC, SC) + spr('a-open', 'sB', 0, -7 * SC, SC) + '</div>'
b += spr('venda', 'sV', CL, CT - 7 * SC, SC)
# los tres, de a poco, con sus indumentarias (escala 10; parados abajo; después los levanta el logo)
b += '<div class="lift">'
for i, (n, cl) in enumerate([('b', 'sT1'), ('c', 'sT2'), ('d', 'sT3')]):
    extra = ''
    if i == 0: extra = '<img class="sv vb" src="assets/oso2/b-smile.png" alt="" style="width:240px;height:304px">'
    if i == 2: extra = '<img class="sv vd" src="assets/oso2/d-smile.png" alt="" style="width:240px;height:304px">'
    hearts = ''
    if i == 1:
        for j in (1, 2, 3):
            hearts += '<img class="ht h%d" src="assets/oso2/heart.png" alt="" style="left:%dpx;top:20px;width:54px;height:48px">' % (j, 140 + (j - 2) * 20)
    b += '<div class="bw k%d" style="left:%dpx;top:%dpx"><div class="gw">%s%s</div>%s</div>' % (i + 1, 440 + i * 400, 212, spr(n, cl, 0, 0, 8), extra, hearts)
b += '</div>'
# hojitas del isologotipo
b += '<div class="lg"><img src="assets/logo/bioferia-sobre-oscuro-hd.png" alt="" style="position:absolute;left:360px;top:470px;width:1200px;height:auto"></div>'
b += '</div>'
b += T('Y ahí encontramos nuestro <span class="y">punto de partida</span>', 360, 750, 60, fx='fb', d=LT0 + 2.8, w=1200, lh='1')
S('a nologo', 'El punto de partida', b, 'VOZ 1 · NATI — «A simple vista, quizás no demasiado. Tienen intereses distintos, necesidades distintas y maneras diferentes de mirar a su alrededor. Pero hay algo que los conecta: BioFeria. Y ahí encontramos nuestro punto de partida.» Primer plano del osito con una venda en los ojos que se saca; desaparece y aparecen de a poco tres ositos con distintas indumentarias (intereses, necesidades, maneras de mirar). Los tres aparecen uno tras otro, más chicos, y cada uno hace su gesto: el del sombrero sonríe, el de la gorra manda corazoncitos y el de los lentes sonríe. Con «hay algo que los conecta» entra el logo de BioFeria desde abajo con rebote, los levanta y ellos caen parados sobre el logo. Abajo, la frase. Dura unos 16 s.', 50, 'zoom')

# ------------------------------------------------------------------ 03 · VOZ 2 · hero tipo "WARHOL": píxeles + letras-ventana (28 s, sin loop)
T3 = 28.0
def _p3(t): return '%.3f%%' % (100.0 * t / T3)
def _kf(name, pts, init):
    """pts=[(t, 'transform', easing)] -> @keyframes con transform sostenido"""
    k = '@keyframes %s{0%%{transform:%s}' % (name, init)
    for t, tr, ez in pts:
        k += '%s{transform:%s%s}' % (_p3(t), tr, (';animation-timing-function:' + ez) if ez else '')
    return k + '100%{transform:' + pts[-1][1] + '}}'
WORD = 'CUIDAR'
ADV = {'C': 543, 'U': 549, 'I': 253, 'D': 551, 'A': 623, 'R': 553}
FS, SXF = 857, .645
LW = [round(ADV[c] * FS / 1000.0 * SXF) for c in WORD]
GAP = 10; LH = 630; LTOP = 215; BASE = 612
LX0 = int((1920 - (sum(LW) + GAP * (len(LW) - 1))) / 2)
_xs = []
_x = LX0
for w in LW:
    _xs.append(_x); _x += w + GAP
css = '<style>.s3h{position:absolute;inset:0;background:#332e34;overflow:hidden}.s3h .abs{position:absolute}'
css += '.s3h .pers{position:absolute;inset:0;perspective:1600px}.s3h .Lz,.s3h .Lh,.s3h .Lf,.s3h .Lt{position:absolute;inset:0;transform-style:preserve-3d}'
css += '.s3h .Lz{inset:auto;height:%dpx}.s3h .Lc{position:absolute;inset:0}.s3h .fill{position:absolute;inset:0;background:#f44530}' % LH
css += '.s3h .cont{position:absolute;inset:0;opacity:0;background:repeating-linear-gradient(135deg,#7779de 0 34px,#0c6fdc 34px 68px)}.s3h .cont video,.s3h .cont img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
css += '.s3h .cell{position:absolute;opacity:0;background-image:url(assets/montana.webp);background-size:960px 679px}'
css += '.s3h .cnt{position:absolute;left:1500px;top:700px;font:300 150px/1 var(--f-ui);color:#f0eee4;opacity:1}.s3h .cnt:after{counter-reset:n var(--n);content:counter(n) " %"}'
css += '.s3h .ln{position:absolute;left:800px;top:905px;height:2px;background:#f0eee4;width:0}'
css += '.s3h .dif{position:absolute;left:0;width:1920px;top:20px;text-align:center;font:400 175px/1 "SA Yesenin","Efrancd",cursive;color:#f44530;text-transform:uppercase;opacity:0;clip-path:inset(0 100% 0 0)}'
css += '.s3h .hbg{position:absolute;inset:0;opacity:0;transform-origin:50% 50%}.s3h .hbg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.s3h .hbg .hg{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(51,46,52,0) 0%,rgba(51,46,52,0) 20%,#332e34 68%)}'
css += '@keyframes hbgIn{0%{opacity:0;transform:scale(1)}' + _p3(3.5) + '{opacity:0;transform:scale(1)}' + _p3(4.6) + '{opacity:.55}' + _p3(18.6) + '{opacity:.55}' + _p3(19.5) + '{opacity:0}100%{opacity:0;transform:scale(1.1)}}.slide.on .s3h .hbg{animation:hbgIn ' + str(T3) + 's ease-out both}'
css += '@property --n{syntax:"<integer>";initial-value:0;inherits:false}@keyframes cnt{from{--n:0}to{--n:100}}@keyframes lnw{from{width:0}to{width:320px}}@keyframes pgone{0%{opacity:1}100%{opacity:0}}'
css += '.slide.on .s3h .cnt{animation:cnt 3s cubic-bezier(.645,.045,.355,1) .5s both,pgone .01s steps(1) 4.5s forwards}.slide.on .s3h .ln{animation:lnw 3.9s cubic-bezier(.645,.045,.355,1) .5s both,pgone .01s steps(1) 4.5s forwards}'
css += '@keyframes cOn{from{opacity:0}to{opacity:1}}@keyframes cOff{from{opacity:1}to{opacity:0}}'
css += '.s3h .pf{position:absolute;left:640px;top:150px;width:640px;height:640px;opacity:0}.slide.on .s3h .pf{animation-duration:28s;animation-timing-function:steps(1,end);animation-fill-mode:both}'
# 10 cuadros que se arman y se desarman (como el preloader de Warhol): cortes secos, una grilla distinta en cada uno
cells = ''
for k in range(10):
    ta = .4 + k * .32
    if k < 9:
        cells += '<img class="pf pf%d" src="assets/slide3/pix-%d.webp" alt="">' % (k, k + 1)
        css += '@keyframes pfk%d{0%%{opacity:0}%s{opacity:0}%s{opacity:1}%s{opacity:1}%s{opacity:0}100%%{opacity:0}}.slide.on .s3h .pf%d{animation-name:pfk%d}' % (k, _p3(ta - .001), _p3(ta), _p3(ta + .32 - .001), _p3(ta + .32), k, k)
    else:
        cells += '<img class="pf pf%d" src="assets/slide3/pix-%d.webp" alt="">' % (k, k + 1)
        css += '@keyframes pfk%d{0%%{opacity:0}%s{opacity:0}%s{opacity:1}%s{opacity:1}%s{opacity:0}100%%{opacity:0}}.slide.on .s3h .pf%d{animation-name:pfk%d}' % (k, _p3(ta - .001), _p3(ta), _p3(4.6 - .001), _p3(4.6), k, k)
# animaciones por letra
TON_ = 18.7
dy = [30, -20, 40, -30, 20, -40]; rz = [-4, 3, -2, 4, -3, 2]
for i in range(len(WORD)):
    t0 = 4.8 + i * .08
    css += _kf('h3e%d' % i, [(t0, 'scale(0)', ''), (t0 + .3, 'scale(1.18)', ''), (t0 + .54, 'scale(.92)', ''), (t0 + .74, 'scale(1.05)', ''), (t0 + .96, 'scale(.99)', ''), (t0 + 1.2, 'scale(1)', '')], 'scale(0)')
    tf = 8.3 + i * 1.5
    css += _kf('h3f%d' % i, [(0, 'none', '')], 'none')
    css += _kf('h3t%d' % i, [(0, 'none', '')], 'none')
    tc = 17.8
    _tot = sum(LW) + (-52) * (len(LW) - 1); _l = 960 - _tot / 2.0 + sum(LW[:i]) + (-52) * i; dxc = int(round(_l - _xs[i]))
    css += _kf('h3z%d' % i, [(tc, 'none', 'ease-out'), (tc + .55, 'translateX(%dpx)' % int(dxc * 1.05), 'ease-in-out'), (tc + .85, 'translateX(%dpx)' % dxc, '')], 'none')
    # relleno: rojo -> crema (ola) ; contenido aparece en el giro
    tw = 5.9 + i * .09
    css += '@keyframes h3w%d{0%%{background:#f44530}%s{background:#f44530}%s{background:#f0eee4}100%%{background:#f0eee4}}' % (i, _p3(tw - .001), _p3(tw))
    css += '@keyframes h3fo%d{0%%{opacity:1}%s{opacity:1}%s{opacity:0}%s{opacity:0}%s{opacity:1}%s{opacity:1}%s{opacity:0}100%%{opacity:0}}' % (i, _p3(tf - .001), _p3(tf), _p3(tf + 1.499), _p3(tf + 1.5), _p3(TON_ - .001), _p3(TON_))
    css += '@keyframes h3co%d{0%%{opacity:0}%s{opacity:0}%s{opacity:1}%s{opacity:1}%s{opacity:0}%s{opacity:0}%s{opacity:1}100%%{opacity:1}}' % (i, _p3(tf - .001), _p3(tf), _p3(tf + 1.499), _p3(tf + 1.5), _p3(TON_ - .001), _p3(TON_))
    css += '.slide.on .s3h .Lh%d{animation:h3e%d %ss both}.slide.on .s3h .Lf%d{animation:h3f%d %ss both}.slide.on .s3h .Lt%d{animation:h3t%d %ss both}.slide.on .s3h .Lz%d{animation:h3z%d %ss both}' % (i, i, T3, i, i, T3, i, i, T3, i, i, T3)
    css += '.slide.on .s3h .fill%d{animation:h3w%d %ss steps(1,end) both,h3fo%d %ss steps(1,end) both}.slide.on .s3h .cont%d{animation:h3co%d %ss steps(1,end) both}' % (i, i, T3, i, T3, i, i, T3)
css += _kf('h3g', [(17.8, 'scale(1)', 'ease-out'), (18.35, 'scale(1.27)', 'ease-in-out'), (18.65, 'scale(1.25)', '')], 'scale(1)')
css += '.s3h .grp{position:absolute;inset:0;transform-origin:960px 530px}.slide.on .s3h .grp{animation:h3g ' + str(T3) + 's both}</style>'
defs = '<svg width="0" height="0" style="position:absolute"><defs>'
for i, c in enumerate(WORD):
    defs += '<clipPath id="lc%d" clipPathUnits="userSpaceOnUse"><text x="0" y="%d" transform="scale(%s,1)" font-family="Barlow Semi Condensed" font-weight="900" font-size="%d">%s</text></clipPath>' % (i, BASE, SXF, FS, c)
defs += '</defs></svg>'
b = css + defs + '<div class="s3h">'
b += cells
b += '<div class="hbg"><img src="assets/slide3/ovejita-bg.webp" alt=""><div class="hg"></div></div>'
b += '<div class="pers"><div class="grp">'
for i, c in enumerate(WORD):
    src = None
    for ext in ('mp4', 'webp', 'jpg', 'png'):
        if os.path.exists('assets/slide3/letra-%d.%s' % (i + 1, ext)): src = 'assets/slide3/letra-%d.%s' % (i + 1, ext); break
    if src and src.endswith('.mp4'):
        inner = '<video class="av" data-src="%s" data-at="%s" muted loop playsinline preload="none"></video>' % (src, 8.3 + i * 1.5)
    elif src:
        inner = '<img src="%s" alt="">' % src
    else:
        inner = ''
    b += '<div class="Lz Lz%d" style="left:%dpx;top:%dpx;width:%dpx"><div class="Lh Lh%d"><div class="Lf Lf%d"><div class="Lt Lt%d"><div class="Lc" style="clip-path:url(#lc%d)"><div class="cont cont%d">%s</div><div class="fill fill%d"></div></div></div></div></div></div>' % (i, _xs[i], LTOP, LW[i], i, i, i, i, i, inner, i)
b += '</div></div></div>'
S('a', 'Cuidar', b, 'VOZ 2 · SOLE — «Cuando pensamos en cuidado medioambiental, imaginamos equilibrio, naturaleza, armonía. Pero en la realidad, las cosas no siempre funcionan así…» Estilo hero: 0–4 s la ovejita se arma y se desarma en bloques (10 cuadros, como el preloader de Warhol); 3,5–4,6 s aparece de a poco la ovejita grande con degradé de fondo, y recién cuando ya está se apagan los píxeles; después entran arriba las letras de CUIDAR con rebote y una ola roja→crema; desde los 8,3 s se enciende el video de cada letra, 1,5 s cada una (C, U, I, D, A, R), sin giro (placeholders en assets/slide3/letra-1…6); a los 20,8 s, con todas las letras claras, se acercan hasta quedar pegadas y la palabra se agranda; a los 21,7 s se encienden los seis videos a la vez y el fondo (la ovejita) se apaga hasta quedar el oscuro plano #332e34, hasta el final. Dura 28 s. Dura 28 s, sin loop.', 28, 'zoom')

# ------------------------------------------------------------------ 04 · VOZ 2 · COEXISTENCIA (video completo a pantalla completa; ya trae su propia entrada de la palabra)
b = BL('<div class="bleed"><video class="av" data-src="assets/coexistencia-voz2-36s-v3.mp4" muted playsinline preload="none"></video></div>')
S('a clean', 'Coexistencia', b, 'VOZ 2 · SOLE — «De ahí nace nuestra propuesta: COEXISTENCIA.» Video completo de la pantalla 4 (38,5 s) a pantalla completa, desde el segundo 0: la palabra COEXISTENCIA y después las cuatro maneras (conectar, intercambiar, accionar, hibridar). Sin textos ni otros elementos; no hace loop (queda en el último cuadro).', 39, 'diag')

# ------------------------------------------------------------------ 05 · VOZ 2 · Sumate a encontrar lo que falta
b = ''
b += V('assets/tagline/tagline-estilos.mp4', 'assets/tagline/tagline-estilos.jpg', 96, 100, 1728, 700, fx='fl', d=.1, r=-.5, cls='card')
b += T('Sumate a encontrar <span class="y">lo que falta.</span>', 96, 850, 100, fx='fb', sp=True, d=.8)
S('a', 'Sumate a encontrar lo que falta', b, 'VOZ 2 · SOLE — «Sumate a encontrar lo que falta. Porque a toda feria le falta algo, y la mejor forma de encontrarlo es entre muchos.» Cartel animado.', 50, 'up')

# ------------------------------------------------------------------ 06 · VOZ 3 · el afiche de la calle (tres videos empalmados, a pantalla completa, sin textos)
b = BL('<div class="bleed vch" data-rate="1" data-rates="1.8,1,1.1,1.67" data-lens="0,0,0,5.9" style="background:#111"><video data-src="assets/calle/calle1.mp4" muted playsinline preload="none"></video><video data-src="assets/calle/calle2-b.mp4" muted playsinline preload="none"></video><video data-src="assets/calle/calle3-b.mp4" muted playsinline preload="none"></video><video data-src="assets/calle/calle4-sin-cuadro-final.mp4" muted playsinline preload="none"></video></div>')
S('a clean', 'El afiche de la calle', b, 'VOZ 3 · LU — «Imaginen que van al trabajo y, mientras esperan el colectivo, se cruzan con una imagen que les llama la atención… “Che, nunca lo había visto de esa manera”.» Cuatro videos (calle 1, 2, 3 y 4) empalmados uno tras otro, a pantalla completa y sin textos. Velocidades: calle 1 a 1,8×, calle 2 a 1×, calle 3 a 1,1× (unos 15 s en total, como antes) y calle 4 a 1,67× (6 s más, sin el cuadro final de los dos afiches sobre negro): unos 21 s en total. Al terminar el cuarto vuelve al primero.', 21, 'left')

# ------------------------------------------------------------------ 07 · VOZ 3 · primero el feed completo y despues las historias, en la misma pantalla
estaticas = ['assets/ig/est/e%02d.jpg' % i for i in range(1, 11)]
anis = ['assets/ig/ani/a%02d.jpg' % i for i in range(1, 11)]
b = BL('<div class="bleed vd7"><video class="av" data-src="assets/redes/ig-feed-07.mp4" data-reveal="stories" muted playsinline preload="none"></video></div>')
b += '<div class="fo7" style="position:absolute;left:0;top:0;width:1920px;height:1080px">'
b += MQ([IM(p_, 169, 300, 'margin-right:16px;border-radius:10px;box-shadow:8px 10px 0 rgba(0,0,0,.35)') for p_ in estaticas], 0, 215, 1920, 320, mt=50, st='')
b += MQ([IM(p_, 169, 300, 'margin-right:16px;border-radius:10px;box-shadow:8px 10px 0 rgba(0,0,0,.35)') for p_ in anis], 0, 555, 1920, 320, mt=60, rev=True)
b += '<div class="celu fx f-zoom" style="--d:.5s;--r:-2deg;left:745px;top:105px;width:430px;height:870px;z-index:5"><div class="scr"><video class="av" data-src="assets/ig/historias.mp4" data-wait="feed" poster="assets/ig/historias.jpg" muted loop playsinline preload="none"></video></div><i class="isl"></i></div>'
b += '</div>'
S('a clean', 'Redes', b, 'VOZ 3 · LU — «Pasás el dedo por un feed que va rápido, y algo te frena. Abrís una historia, y otra, y empiezan a moverse…» Primero el video completo del feed de Instagram; al terminar aparecen las tiras de historias estaticas y animadas con el celular pasando historias al medio.', 40, 'left')

# ------------------------------------------------------------------ 08 · VOZ 3 · URL, web y recorrido completo del quiz
b = """<div class="s8-sequence">
<div class="browser s8-browser"><div class="bar"><b></b><b></b><b></b><span>www.bioferia.com.ar</span></div><div class="s8-web-viewport"><iframe class="s8-web" title="Recorrido por la web de Bioferia" tabindex="-1"></iframe></div></div>
<div class="s8-address"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><circle cx="13" cy="13" r="9"/><path d="m20 20 9 9"/></svg><span class="s8-typed"></span><span class="s8-enter">Enter ↵</span></div>
<div class="s8-phone"><div class="s8-phone-screen"><iframe class="s8-app" title="Demo animada del quiz de Bioferia" tabindex="-1"></iframe></div></div>
<div class="s8-caption">Una pregunta por día. Otras formas de mirar.</div><div class="s8-status" role="status"></div>
</div>"""
S('b nologo', 'Web y app', b, 'VOZ 3 · LU — Se escribe www.bioferia.com.ar y Enter abre la web casi a pantalla completa. Scroll suave; la ventana se reduce a la izquierda y entra el celular desde Inicio. Un cursor de mano abre el quiz de ropa, elige una respuesta, continúa y muestra la elección junto a otras miradas. Secuencia de 26 s: app desde el segundo 8, comparación desde el 22. Scroll web continuo aun al costado y despues del quiz; sin hoja flotante. Al volver a entrar, todo se reinicia.', 26, 'blinds')

# ------------------------------------------------------------------ 09 · VOZ 4 · todo lo que estamos sumando
b = ''
b += PH('Video · persona caminando con el celu frente a un afiche', 620, 90, 1200, 675, fx='fr', d=.3, r=1.2)
for i, (p, y, r) in enumerate([('assets/ig/feed/f05.jpg', 110, -4), ('assets/yt/cel-1.jpg', 400, 3), ('assets/posters/poster03.jpg', 690, -3)]):
    b += E(p, 100 + (i % 2) * 120, y, 330, fx=['fl', 'fl', 'fl'][i], d=.6 + i * .5, r=r, lp='fl', ld=6 + i, z=3)
b += T('Fíjense todo lo<br>que estamos <span class="y">sumando</span>', 620, 810, 80, fx='fb', sp=True, d=1.2, lh='.98')
b += ST('Redes · web · app', 1500, 840, 'vi', 'pop', d=2.4, r=-3, size=30)
S('a', 'Todo lo que estamos sumando', b, 'VOZ 4 · JOR — «Fíjense todo lo que estamos sumando: BioFeria ya no necesita esperar a que abran sus puertas para conectar con las personas.» Repaso rápido de redes, web y app; la persona caminando con el celu frente a un afiche.', 40, 'up')

# ------------------------------------------------------------------ 10 · VOZ 4 · ¡Y por fin llegamos!
b = VB('assets/espacios/entrada-apertura.mp4', 'assets/espacios/3di-entrada.jpg')
b += BL('<div class="bleed" style="background:linear-gradient(180deg,rgba(0,0,0,.5) 0,transparent 28%,transparent 55%,rgba(0,0,0,.75) 100%)"></div>')
b += T('¡Y por fin <span class="y">llegamos!</span>', 0, 770, 150, w=1920, fx='slam', sp=True, d=.6, z=5, st='text-align:center;text-shadow:0 4px 24px rgba(0,0,0,.6)')
b += V('assets/espacios/escenario-feria.mp4', 'assets/espacios/3di-escenario.jpg', 1230, 70, 600, 338, fx='fr', d=2.2, r=3, cls='card', z=6, st='outline:5px solid #f1ede4')
S('a', 'Y por fin llegamos', b, 'VOZ 4 · JOR — «Así, cuando finalmente llega el día de la feria… ¡Y por fin llegamos!» El video del portal de ingreso a pantalla completa, con el título centrado, y el video del escenario en una caja a la derecha.', 40, 'zoom')

# ------------------------------------------------------------------ 11 · VOZ 4 · la Reserva
b = ''
b += '<!--BL--><div class="bleed"><video class="av" data-src="assets/reserva/recorrido-reserva-v4-sin-sonido-extendido.mp4" muted playsinline preload="none"></video></div><!--/BL-->'
S('a clean', 'La Reserva', b, 'VOZ 4 · JOR — «Reserva Ecológica Costanera Sur… plantas, animales, especies… ¿Se imaginan disfrutar de BioFeria en un entorno así?» Pantalla limpia: recorrido reserva v4 sin audio, con dos segundos adicionales del ultimo cuadro, sin deformacion.', 40, 'blinds')

# ------------------------------------------------------------------ 12 · VOZ 4 · cada persona, su rol (indumentaria)
b = ''
b += BL('<div class="bleed" style="background:#f1eee6"></div>')
b += V('assets/indumentaria/indu-bio-v1.mp4', '', 300, 40, 1320, 743, fx='zoom', d=.2, r=0, cls='', st='-webkit-mask-image:linear-gradient(to right,transparent,#000 5%,#000 88%,transparent 96%),linear-gradient(to bottom,#000 95%,transparent);-webkit-mask-composite:source-in;mask-image:linear-gradient(to right,transparent,#000 5%,#000 88%,transparent 96%),linear-gradient(to bottom,#000 95%,transparent);mask-composite:intersect;clip-path:inset(0 3% 0 0);', z=3)
items = []
for i in range(12):
    p = 'assets/crew/c%02d.webp' % i
    w, h = _dims(p, None, 170)
    items.append('<div style="width:%dpx;margin-right:28px;text-align:center"><img src="%s" style="width:%dpx;height:170px" alt=""></div>' % (w, p, w))
b += MQ(items, 0, 830, 1920, 190, mt=40, st='filter:drop-shadow(4px 5px 0 rgba(0,0,0,.3))')
S('b', 'Cada persona, su rol', b, 'VOZ 4 · JOR — «Cada persona que trabaja se viste de acuerdo a su rol, y se reconoce de lejos: sabés a quién acercarte.» Video de la indumentaria de los roles, grande y centrado, con la hilera chica de todas las prendas pasando abajo.', 40, 'up')

# ------------------------------------------------------------------ 13 · VOZ 5 · recorrer: mapa, señales, íconos y espacios
b = ''
b += T('Entrás y todo está <span class="y">ahí</span>', 96, 50, 78, fx='fl', d=.1, sp=True)
b += '<div class="ab card cyc2 fx f-fl" style="--d:.3s;--cy:9s;--r:-1.5deg;left:96px;top:170px;width:640px;height:392px;background:#f0eee4"><div style="--k:0;--n:2"><img class="kb" src="assets/senal2/mapa-recorrido.webp" style="width:100%;height:100%;object-fit:cover" alt=""></div><div style="--k:1;--n:2"><img src="assets/senal2/mapa-picto-m.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 40%" alt=""></div></div>'
b += ST('Un mapa que te ubica', 110, 575, 'dk', 'pop', d=1.0, r=-2, size=22, z=7)
mm = ['hito-moda-m', 'colgante-m', 'dist-1-m', 'muro-m', 'mercado-m']
inner = ''.join('<div style="--k:%d;--n:5"><img src="assets/senal2/%s.jpg" style="width:100%%;height:100%%;object-fit:cover" alt=""></div>' % (k, n) for k, n in enumerate(mm))
b += '<div class="ab card cyc fx f-fb" style="--d:.7s;--cy:10s;--r:2deg;left:96px;top:630px;width:640px;height:330px;background:#222">%s</div>' % inner
b += ST('Señales que te guían', 110, 970, 'vi', 'pop', d=1.4, r=2, size=22, z=7)
pic = sorted(p.replace(os.sep, '/') for p in glob.glob('assets/pictos/*.svg'))
random.seed(11)
AMORFAS = ['4% 10%,38% 0,96% 6%,100% 52%,94% 100%,52% 94%,0 100%,6% 48%','3% 8%,48% 2%,97% 7%,100% 55%,95% 96%,45% 100%,2% 93%,0 40%','6% 4%,55% 0,100% 10%,96% 58%,100% 96%,50% 98%,0 94%,3% 45%','0 6%,42% 3%,94% 0,98% 46%,92% 100%,40% 95%,5% 100%,4% 52%'];tilec = ['#f0eee4']*4
def _tile(p, i, sz, im):
    poly = AMORFAS[i % len(AMORFAS)]
    return '<div style="width:%dpx;height:%dpx;margin-right:20px;filter:drop-shadow(7px 9px 0 rgba(0,0,0,.28))"><div style="width:100%%;height:100%%;background:#332e34;clip-path:polygon(%s);display:grid;place-items:center"><div style="width:calc(100%% - 6px);height:calc(100%% - 6px);background:#f0eee4;clip-path:polygon(%s);display:grid;place-items:center"><img src="%s" style="width:%dpx;height:%dpx" alt=""></div></div></div>' % (sz, sz, poly, poly, p, im, im)
for r_, (y_, off_, rev_, mt_) in enumerate([(200, 0, False, 55), (470, 7, True, 65), (740, 14, False, 60)]):
    seq_ = pic[off_:] + pic[:off_]
    b += MQ([_tile(p_, k_ + r_, 200, 138) for k_, p_ in enumerate(seq_)], 790, y_, 1130, 230, mt=mt_, rev=rev_)
b += ST('Íconos: se entienden de un vistazo', 1300, 970, 'dk', 'pop', d=1.8, r=-2, size=24, z=7)
S('a', 'Recorrer', b, 'VOZ 5 · MARTU — «Esta es la BioFeria que imaginamos para recibirlos. Entrás y todo lo que viste en la pantalla está ahí, en tamaño real. Un mapa que te ubica, señales que te guían, los iconos… y espacios para cada momento.» Mapa, señales y pictogramas (los espacios en video pasaron a la pantalla siguiente).', 40, 'zoom')

# ------------------------------------------------------------------ 14 · VOZ 5 · los espacios en video, uno tras otro a pantalla completa (antes estaban dentro de la pantalla 13)
esp = ['info-tickets', 'escenario-feria', 'charlas1', 'expositores', 'gazebo', 'descanso', 'instagrameable360']
b = BL('<div class="bleed vch" data-rate="1" data-lens="%s" style="background:#111">%s</div>' % (','.join(['4'] * len(esp)), ''.join('<video data-src="assets/espacios/%s.mp4" muted playsinline preload="none"></video>' % e for e in esp)))
S('a clean', 'Los espacios', b, 'VOZ 5 · MARTU — «…Además hay espacios para cada momento, esos que viste en la web: para llegar, para escuchar, para charlar, para descansar.» Los siete videos de los espacios (boletería, escenario, charlas, stand, gazebo, descanso y 360), uno tras otro a pantalla completa y sin textos, 4 s cada uno (28 s en total); al terminar vuelve al primero.', 28, 'blinds')

# ------------------------------------------------------------------ 14 · VOZ 5 · Oso sin conexión (sin textos: el oso corre en círculos y después aparece la app grande jugándose sola con la flechita)
import math as _mm
b = ''
trk = '<svg width="1920" height="1080" style="position:absolute;left:0;top:0"><ellipse cx="960" cy="640" rx="650" ry="200" fill="none" stroke="#7779de" stroke-width="10" stroke-linecap="round" stroke-dasharray="0.1 24"/>'
for _k in range(8):
    _a = 2 * _mm.pi * _k / 8
    trk += '<circle cx="%d" cy="%d" r="15" fill="#fdff1a" stroke="#332e34" stroke-width="5"/>' % (960 + 650 * _mm.cos(_a), 640 + 200 * _mm.sin(_a))
trk += '</svg>'
bear = '<div class="runner" data-cx="960" data-cy="640" data-rx="650" data-ry="200" data-per="2.4" data-w="360" data-feet="432" style="position:absolute;left:0;top:0;width:1920px;height:1080px"><div class="bear" style="position:absolute;left:0;top:0;width:360px;height:456px;will-change:transform">'
for _n in ('run-a', 'run-b', 'run-c'):
    bear += '<img class="rb" src="assets/oso2/%s.png" alt="" style="position:absolute;left:0;top:0;width:360px;height:456px;image-rendering:pixelated;opacity:0">' % _n
bear += '</div></div>'
b += '<div class="ab rgd" style="left:0;top:0;width:1920px;height:1080px">' + D(trk + bear, 0, 0, 1920, 1080, fx='fb', d=.1) + '</div>'
_pl = D('<div class="pulse" style="position:absolute;left:0;top:96px;width:440px;height:900px;border-radius:80px;background:#fdff1a;filter:blur(50px);opacity:.45"></div>', 740, 0, 440, 1080, fx='fb', d=.9, z=1)
b += '<div class="ophone">' + _pl + '<div class="phone fx f-zoom" style="--d:.9s;left:740px;top:20px;width:440px;height:954px;border-radius:60px;z-index:3"><iframe class="pitch-web" data-src="game/index.html" data-delay="1100" title="oso" style="position:absolute;left:0;top:0;width:390px;height:846px;transform:scale(1.1282);transform-origin:0 0;pointer-events:none" tabindex="-1"></iframe></div></div>'
b += '<img class="dlimg" src="assets/oso/tarjeta-ana.png" alt="">'
S('a', 'Oso sin conexión', b, 'VOZ 5 · MARTU — «Y como esto es una feria que también juega, en una pantalla gigante hay un oso. Escaneás un QR, se cae internet, y aparece él dando vueltas, siempre igual. Un juego de un minuto que te deja pensando.» Sin textos: el oso corre en círculos sin parar sobre el recorrido punteado (apenas el primer paso); enseguida el celular aparece y baja la opacidad del oso; la app grande se juega sola con una flechita de mouse: toca para saltar, aparece la revelación, «Guardar este conocimiento», escribe el nombre en la tarjeta, y al «Descargar imagen» el celular se inclina y aparece la imagen descargada; después «Jugar de nuevo».', 60, 'circle')

# ------------------------------------------------------------------ 15 · VOZ 5 · el librito (mockup en video)
b = ''
b += VB('assets/libro/librito-mockup.mp4', 'assets/libro/p00.webp')
b += E('assets/libro/suelta-tortuga.webp', 1290, 250, 290, fx='drop', d=1.5, r=-8, lp='fl', ld=6, z=4)
b += E('assets/libro/suelta-redondo.webp', 1590, 230, 270, fx='drop', d=1.8, r=7, lp='sw', ld=7, z=4)
b += E('assets/libro/pag29-troquel.webp', 1330, 560, 310, fx='fr', d=2.1, r=4, lp='fl', ld=8, z=4)
for i, (n, x, y, w, r) in enumerate([('stk-1', 1640, 600, 150, -8), ('stk-3', 1740, 780, 140, 6), ('stk-4', 1380, 880, 140, -4), ('stk-7', 1560, 880, 130, 10)]):
    b += E('assets/libro/%s.webp' % n, x, y, w, fx='slam', d=2.6 + i * .2, r=r, lp='bo', ld=3 + i * .5, z=5)
b += E('assets/libro/ticket26.webp', 1300, 800, 110, fx='drop', d=3.4, r=-12, z=5)
S('a', 'El librito', b, 'VOZ 5 · MARTU — «Hay experiencias que necesitan sentirse en las manos… El librito es un anotador, de esos donde entraban ideas de todos los momentos de tu vida. Lo abrís, lo llenás, lo guardás.» Pantalla sin textos: el mockup en video a pantalla completa y, arriba, las piezas que se sueltan.', 40, 'left')

# ------------------------------------------------------------------ 16 · VOZ 5 · folletos y volantes (uno a la vez, a pantalla completa, acelerados, sin textos)
b = BL('<div class="bleed vch" data-rate="1" data-rates="1.9825,1,1"><video data-src="assets/folletos/persona-volante.mp4" muted playsinline preload="none"></video><video data-src="assets/folletos/diptico-cierre-derecha-izquierda.mp4" muted playsinline preload="none"></video><video data-src="assets/folletos/cruz.mp4" muted playsinline preload="none"></video></div>')
S('b', 'Folletos y volantes', b, 'VOZ 5 · MARTU — «Los folletos y los volantes te cuentan lo importante sin aburrir. Hay un desplegable chiquito, con una forma distinta a todo lo demás, que le habla al mar y a vos te hace una pregunta amable…» Sin textos: los tres videos a pantalla completa, uno tras otro: persona dando vuelta el folleto completo acelerado a 4 s, díptico con cierre de derecha a izquierda (5,25 s) y desplegable en cruz (8 s). En loop, sin sonido; unos 17,25 s por vuelta. Duración de la pantalla a definir.', 30, 'left')

# ------------------------------------------------------------------ 17 · VOZ 5 · posters (video a pantalla completa, solo la frase en una caja amorfa)
b = VB('assets/posters/poster-video-17.mp4')
b += ST('El intercambio no termina<br>cuando el sol se va', 96, 800, '', 'pop', d=2.0, r=-2, size=54, z=7, st='line-height:1.1;')
S('a', 'Posters', b, 'VOZ 5 · MARTU — «Y también hay posters, para llevarte a casa y dejar pegados en la pared. Lo que gana BioFeria: que el intercambio no termine cuando el sol se va.» Video de los posters a pantalla completa; solo queda la frase «El intercambio no termina cuando el sol se va», en una caja amorfa.', 30, 'circle')

# ------------------------------------------------------------------ 18 · VOZ 6 · invitación, kit, credenciales, tickets
# El video vertical (invitación + entrada, partes 18 y 18.1 encadenadas) entra desde la izquierda y queda en el margen izquierdo; el resto de las piezas flotan del otro lado.
b = ''
b += BL('<div class="vleft chain"><video class="c1" data-src="assets/entrada/entrada-invitacion-18.mp4" muted playsinline preload="none"></video><video class="c2" data-src="assets/entrada/entrada-invitacion-18-1.mp4" muted playsinline preload="none"></video></div>')
b += T('Desde que llegás,<br><span class="y">ya es parte de uno</span>', 700, 40, 72, fx='fl', d=.5, sp=True, lh='1')
b += ST('El kit de ingreso', 1500, 90, 'rd', 'pop', d=1.2, r=2, size=36, z=8)
b += E('assets/acc/pulsera-oscura.webp', 700, 215, 450, fx='fr', d=.9, r=4, lp='fl', ld=6)
b += E('assets/acc/pulsera-clara.webp', 1210, 235, 450, fx='fr', d=1.2, r=-3, lp='fl', ld=7)
b += ST('Pulseras', 1700, 380, '', 'pop', d=1.5, r=-2, size=24, z=8)
for i, n in enumerate(['comida', 'bebida', 'parking', 'taller']):
    b += E('assets/merch/tk-%s.webp' % n, 700 + i * 295, 545, 285, fx='slam', d=1.7 + i * .2, r=[-3, 2, 2, -2][i], z=5)
b += ST('Tickets', 1700, 505, 'cr', 'pop', d=2.6, r=-2, size=24, z=8)
b += E('assets/merch/cup-blanca.webp', 700, 775, 330, fx='drop', d=2.8, r=-4, z=5)
b += E('assets/merch/cup-negra.webp', 1060, 790, 330, fx='drop', d=3.1, r=3, z=5)
b += ST('Cuponeras', 1430, 860, 'vi', 'pop', d=3.5, r=-2, size=24, z=8)
S('a', 'Entrada y kit', b, 'VOZ 6 · LOUR — «Desde que llegás, la invitación y la entrada ya son parte de uno. Además te sumamos el kit de ingreso… los tickets y las cuponeras que sirven para comer y tomar algo.» El video vertical (invitación y entrada, partes 18 y 18.1 encadenadas, en loop) entra desde la izquierda y ocupa todo el alto de la pantalla, pegado al borde izquierdo; del otro lado, el kit de ingreso completo: pulseras, tickets y cuponeras (se quitaron las credenciales y el tote). El título va en dos renglones, arrancando donde termina el video.', 50, 'diag')

# ------------------------------------------------------------------ 20 · VOZ 6 · los objetos (merch): primero el video (10 s, pantalla completa) y después las piezas
b = ''
_pre = BL('<div class="bleed vo"><video class="av" data-src="assets/merch/merch-video-20.mp4" muted playsinline preload="none"></video></div>')
b += '<div class="ghost" style="left:60px;top:430px;font-size:520px;opacity:.07;color:#322e33">MERCH</div>'
b += T('En tu mesa, en tu mochila, <span class="y">en tu ropa</span>', 96, 70, 66, fx='fl', d=.1, sp=True)
b += E('assets/merch/tote-png.webp', 90, 290, None, 560, fx='drop', d=.5, r=-4, lp='bo', ld=4.2, z=2)
b += E('assets/merch/agenda-png.webp', 470, 360, None, 520, fx='drop', d=.8, r=3, lp='bo', ld=3.6, z=3)
b += E('assets/merch/taza-png.webp', 790, 640, 400, fx='drop', d=1.1, r=-3, lp='bo', ld=4.6, z=3)
b += D('<img src="assets/merch/remera.jpg" style="width:100%;height:100%;object-fit:cover" alt="">', 1020, 250, 300, 450, fx='drop', d=1.4, r=4, cls='card')
b += E('assets/merch/lapices-n.webp', 1380, 250, 470, fx='drop', d=1.7, r=-3, lp='bo', ld=3.9, z=3)
b += E('assets/merch/cartuchera.webp', 1330, 560, 480, fx='drop', d=2.0, r=3, lp='bo', ld=4.4, z=3)
for i, (t, x, y) in enumerate([('Tote bag', 130, 880), ('Agenda', 540, 900), ('Taza', 880, 950), ('Remera', 1050, 720), ('Lápices', 1560, 210), ('Cartuchera', 1520, 880)]):
    b += ST(t, x, y, ['dk', 'rd', 'vi', 'dk', 'rd', 'vi'][i], 'pop', d=2.3 + i * .15, r=[-3, 2, -2, 3, -2, 2][i], size=22, z=8)
b = _pre + '<div class="later" data-after="9.8" style="position:absolute;left:0;top:0;width:1920px;height:1080px">' + b + '</div>'
S('b clean', 'Los objetos', b, 'VOZ 6 · LOUR — «Y no nos olvidemos de esos objetos que meten un pedacito de BioFeria en tu día a día: en tu mesa, en tu mochila, en tu escritorio y en tu ropa.» Primero entra el video del merch (10 s, a pantalla completa) y después salen remera, taza, agenda, tote, cartuchera y lápices.', 50, 'circle')

# ------------------------------------------------------------------ 21 · VOZ 6 · todas las piezas en una pantalla
mos = (['assets/ig/feed/f%02d.jpg' % i for i in (1, 4, 8, 12, 16, 20)] + ['assets/posters/poster%02d.jpg' % i for i in (1, 2, 3, 4, 5, 6, 7)]
       + ['assets/merch/tote-png.webp', 'assets/merch/agenda-png.webp', 'assets/merch/taza-png.webp', 'assets/merch/cartuchera.webp']
       + ['assets/yt/canal-n.jpg', 'assets/yt/repro.jpg', 'assets/yt/cel-1.jpg', 'assets/edit/diptico-tapa.jpg', 'assets/edit/volante-frente.jpg',
          'assets/libro/p01.webp', 'assets/libro/suelta-redondo.webp', 'assets/acc/entrada-n-frente.webp', 'assets/acc/pulsera-clara.webp',
          'assets/conc/c1.jpg', 'assets/conc/c2.jpg', 'assets/espacios/3di-entrada.jpg', 'assets/espacios/3di-escenario.jpg', 'assets/senal2/mapa-picto.webp',
          'assets/crew/c00.webp', 'assets/crew/c03.webp', 'assets/loops/loop2.jpg', 'assets/ig/ani/a03.jpg'])
b = ''
random.seed(21)
cols, rows = 8, 4
cw, ch_ = 240, 270
for i, p in enumerate(mos[:cols * rows]):
    c, r = i % cols, i // cols
    b += D('<img src="%s" style="width:100%%;height:100%%;object-fit:cover" alt="" loading="lazy">' % p, 0 + c * cw, 70 + r * (ch_ + 6) - (0 if r % 2 == 0 else 0), cw, ch_, fx='pop', d=.2 + i * .12, r=random.choice([-2, 1.5, -1, 2]), cls='card', st='box-shadow:6px 8px 0 rgba(0,0,0,.35)')
b += D('<div style="width:100%;height:100%;filter:drop-shadow(8px 10px 0 rgba(0,0,0,.4))"><div style="--j:2.6px;width:100%;height:100%;background:#332e34" class="amo2"></div></div>', 56, 752, 1150, 270, fx='fb', d=4.0, z=7)
b += T('Ya convoca a personas<br>con ganas de <span class="y">involucrarse</span>', 96, 790, 84, fx='fb', sp=True, d=4.2, z=8, lh='.98')
m21 = b

# ------------------------------------------------------------------ 22 · VOZ 6 · cierre
imgs = ''.join('<img src="assets/cierre/m%02d.webp" alt="" loading="lazy">' % i for i in range(1, 89))
b = BL('<div class="bleed mtg" data-start="9">%s</div>' % imgs) + '<div class="fo21" style="position:absolute;left:0;top:0;width:1920px;height:1080px">' + m21 + '</div>'
S('a', 'Todo en una pantalla y cierre', b, 'VOZ 6 · LOUR — «Ese pequeño descubrimiento resume la experiencia que queremos abrir. BioFeria ya convoca a personas con ganas de involucrarse… Sumate a encontrar lo que falta.» Pantalla unida (antes 21 y 22): primero el mosaico con todas las piezas y la frase «Ya convoca a personas con ganas de involucrarse» (unos 9 s); después el montaje de cierre, sin tarjeta superpuesta, QR ni miniatura del manual. Se quitó la pantalla «primera impresión».', 60, 'up')


# ------------------------------------------------------------------ 22 · Video concepto con sonido y avance automatico
b = BL('<div class="bleed"><video class="av" data-src="assets/ostensa/video-concepto-cierre-con-sonido.mp4" data-snd="1" data-hide-sound="1" data-autosound="1" data-next="1" playsinline preload="none"></video></div>')
S('a clean', 'Video concepto', b, 'Video concepto completo con sonido. Al finalizar avanza automaticamente a Segui con la experiencia.', 53, 'up')

# ------------------------------------------------------------------ 23 · Segui con la experiencia
b = '<div class="closing-videos vch">' + ''.join('<video data-src="assets/cierre-videos/pieza-%02d.mp4" muted playsinline preload="none"></video>' % i for i in range(1, 7)) + '</div>'
b += T('Seguí con<br><span class="y">la experiencia</span>', 780, 90, 100, fx='fb', d=.1, w=1080, lh='1.02')
b += '<div class="qr-grid">'
b += "<a class=\"qr-card\" href=\"https://web-biobyostensa.netlify.app/\" target=\"_blank\" rel=\"noopener noreferrer\"><img src=\"assets/cierre-qr/web.png\" alt=\"QR: Web\"><span>Web</span></a>"
b += "<a class=\"qr-card\" href=\"https://bioferia-app.vercel.app/#welcome/0\" target=\"_blank\" rel=\"noopener noreferrer\"><img src=\"assets/cierre-qr/app.png\" alt=\"QR: App\"><span>App</span></a>"
b += "<a class=\"qr-card\" href=\"https://claude.ai/artifact/TLqTEsjNuRPyxYzXG45buD\" target=\"_blank\" rel=\"noopener noreferrer\"><img src=\"assets/cierre-qr/juego.png\" alt=\"QR: Jueguito\"><span>Jueguito</span></a>"
b += "<a class=\"qr-card\" href=\"https://www.figma.com/design/Uw3IziPhIKbeLgcD4brIXM/Bioferia-%C2%B7-Presentaci%C3%B3n-por-temas?node-id=3-577&amp;p=f&amp;m=dev\" target=\"_blank\" rel=\"noopener noreferrer\"><img src=\"assets/cierre-qr/presentacion.png\" alt=\"QR: Todo el material\"><span>Todo el material</span></a>"
b += '</div>'
S('a nologo', 'Segui con la experiencia', b, 'Seis videos verticales completos en secuencia y en bucle. QR de web, app, juego y presentacion del material en Figma.', 60, 'up')

# ===================================================================================
html = '\n\n'.join(SLIDES)
open('slides/express.html', 'w', encoding='utf-8').write(html)
print('slides/express.html listo:', len(SLIDES), 'pantallas')
