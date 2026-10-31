"""Turn the preview page (written for claude.ai, which adds the document
skeleton itself) into a complete index.html that GitHub Pages can serve.

Usage: python wrap_page.py <preview page.html> <output index.html>
"""
import sys
from pathlib import Path

page = Path(sys.argv[1]).read_text(encoding="utf-8")
head_end = page.index("</style>") + len("</style>")
head, body = page[:head_end], page[head_end:]

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta property="og:title" content="Alice no País das Maravilhas">
<meta property="og:description" content="Um jogo gratuito em onze episódios, baseado no livro de Lewis Carroll. Em português e em inglês, no navegador ou no Windows.">
<meta property="og:image" content="https://fbrandao2k.github.io/alice-no-pais-das-maravilhas/img/social.jpg">
<meta property="og:locale" content="pt_BR">
<meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1c1410">
<style>
:root {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
{head.strip()}
</head>
<body>
{body.strip()}
</body>
</html>
"""
Path(sys.argv[2]).write_text(html, encoding="utf-8", newline="\n")
print("wrote", sys.argv[2])
