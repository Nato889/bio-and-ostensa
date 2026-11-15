# BioFeria · Pitch express v2 (Ostensa)

Presentación HTML de 20 pantallas (seis voces: NATI · SOLE · LU · JOR · MARTU · LOUR). No necesita instalar nada para presentarla.

## Cómo verla / presentarla
1. Bajá el repositorio (botón verde **Code → Download ZIP**, o `git clone`).
2. Abrí `index.html` con Chrome (o Safari). Para que todo funcione igual que en la presentación, mejor servirla local:
   ```
   cd bio-and-ostensa
   python3 -m http.server 8000
   ```
   y abrir <http://localhost:8000>.
3. Teclas: `←` `→` avanzar · `F` pantalla completa · `T` cronómetro · `N` notas del orador · `M` sonido · para saltar a una pantalla: `index.html#12`.

> Los videos son pesados. Si algo se traba, probá en la compu donde se va a presentar y dejá cargar la pantalla un momento antes.

## Cómo modificarla
Todo el contenido de las pantallas se arma desde **`_work/gen.py`** (una pantalla = un bloque `# --- NN · VOZ …`). Después se regenera `index.html`:
```
pip3 install pillow        # una sola vez
python3 build.py
```
- `express.css` y `express.js`: estilos y comportamiento (animaciones, videos, interacciones).
- `template.html`: la estructura de la página.
- `slides/express.html`: lo que genera `gen.py` (no editar a mano).
- Para **reemplazar un video o una imagen**: guardá el archivo nuevo en `assets/…` (con otro nombre para que el navegador no use el viejo guardado) y cambiá la ruta en `gen.py`.
- Las rutas son relativas, siempre dentro de esta carpeta. No uses archivos de otros lugares de tu compu.

## Qué hay en cada carpeta
- `assets/` imágenes, videos, logos y piezas del pitch (todo lo que usa la presentación).
- `fonts/` Barlow Semi Condensed, SA Yesenin, Efrancd.
- `game/` el juego «Oso sin conexión» (pantalla 14, copia para la presentación).
- `app-real/` la app (prototipo) de las pantallas 8.
- `web-demo/` la web de la pantalla 8.
- `_work/` generador de pantallas y scripts auxiliares (`oso2.py` y `pix3.py` son de los dibujos del osito y de los cuadros de píxeles; los resultados ya están en `assets/`).

## Videos grandes
GitHub no acepta archivos de más de 100 MB dentro del repositorio. Si una pantalla necesita un video así, hay que subirlo a **Releases** (o exportarlo más liviano) y no al repositorio.
- El video concepto largo (`v3-alta-video-concepto-75perceto.mp4`, ~299 MB) ya **no se usa** en la presentación; quedó guardado en Releases (etiqueta `video-concepto`) solo como respaldo.

## Reglas del proyecto (para no romper nada)
- Paleta: rojo `#f44530`, azul `#0c6fdc`, violeta `#7779de`, crema `#f0eee4`, oscuro `#332e34`, amarillo `#fdff1a`.
- Tipografías: Barlow Semi Condensed (títulos) y SA Yesenin (palabra resaltada, siempre en mayúscula).
- Cajas de texto: formas amorfas (nunca rectángulos rígidos). Videos «a pantalla completa»: de borde a borde.
- No subir archivos de más de 100 MB.
