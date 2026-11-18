"""Genera upwork/index.html: la misma página, sin precios ni datos de contacto.

Uso: python3 tools/upwork.py  (correr cada vez que se cambie index.html)
"""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")


def sub(pattern, repl, text, count=0, flags=re.S):
    new, n = re.subn(pattern, repl, text, count=count, flags=flags)
    if n == 0:
        sys.exit(f"No se encontró: {pattern[:70]}")
    return new


# Rutas relativas: la página vive un nivel más abajo
html = html.replace('"v/', '"../v/').replace('"ejemplos/', '"../ejemplos/')

# No indexar la copia
html = sub(r"(<head>)", r'\1\n<meta name="robots" content="noindex">', html, count=1)

# Precios
html = sub(r'\s*<p class="price">.*?</p>', "", html)
html = sub(r'\s*<li>[^<]*\d[\d.]*\s*COP[^<]*</li>', "", html)
html = sub(r'\s*<article class="svc">(?:(?!</article>).)*?Landing por mensualidad.*?</article>', "", html)
html = sub(r'\s*<p class="note pay-note">.*?</p>', "", html)
html = sub(r"Precios fijos y claros\. Todos los proyectos empiezan con 50 % de anticipo e incluyen 2 rondas de cambios\.",
           "Procesos claros y entregas puntuales. Todos los proyectos incluyen 2 rondas de cambios.", html)
html = sub(r"Recibes alcance, fechas y precio por escrito\. Con el 50 % empezamos\.",
           "Recibes el alcance y las fechas por escrito antes de empezar.", html)
html = sub(r"12 reels or shorts a month for 700 USD, or single videos from 200 USD, with",
           "monthly packages or single videos, with", html)

# Contacto: en Upwork todo pasa por la plataforma
html = sub(r'(<section id="contacto" class="contact">\s*<div class="wrap">\s*<p class="eyebrow">Contacto</p>\s*<h2>.*?</h2>).*?(\s*</div>\s*</section>)',
           r'\1\n    <p style="margin-top:24px;font-size:1.15rem">Escríbeme por Upwork y te respondo el mismo día con una propuesta para tu proyecto.</p>\2',
           html)

out = root / "upwork" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")

left = re.findall(r"[^>\s][^<>]{0,40}(?:COP|USD)[^<>]{0,20}", html)
print("Generado:", out)
print("Menciones de precio restantes:", left or "ninguna")
