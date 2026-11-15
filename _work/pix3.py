"""Genera los 10 cuadros 'se arma / se desarma' de la ovejita, con las mismas 10 grillas (6x6) del preloader de Warhol."""
import json
from PIL import Image
pats = json.load(open('_work/pats_warhol.json'))
sheep = Image.open('assets/slide3/ovejita-03.png').convert('RGBA')
W, H = sheep.size
RED = (0xf4, 0x45, 0x30, 255)
PARAMS = [(2.3, .40, .30), (2.0, .38, .12), (1.6, .42, .36), (3.0, .45, .29), (1.6, .52, .40), (1.8, .72, .62), (1.0, .5, .5), (1.9, .55, .85), (2.4, .22, .40), (1.4, .45, .40)]
N = 900; C = N // 6
for k, ((z, cx, cy), pat) in enumerate(zip(PARAMS, pats)):
    s = N * z / float(H)
    im = sheep.resize((max(1, int(W * s)), max(1, int(H * s))), Image.LANCZOS)
    canvas = Image.new('RGBA', (N, N), RED)
    ox = int(N / 2 - cx * im.size[0]); oy = int(N / 2 - cy * im.size[1])
    canvas.alpha_composite(im, (ox, oy)) if (ox >= 0 and oy >= 0) else canvas.paste(im, (ox, oy), im)
    out = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    for r in range(6):
        for c in range(6):
            if pat[r][c] == '#':
                out.paste(canvas.crop((c * C, r * C, (c + 1) * C, (r + 1) * C)), (c * C, r * C))
    out.save('assets/slide3/pix-%d.webp' % (k + 1), quality=88, method=6)
print('ok')
