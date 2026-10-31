# Alice no País das Maravilhas

Site do jogo *Alice no País das Maravilhas*, uma aventura gratuita em onze episódios, baseada no livro de Lewis Carroll (1865). Em português e em inglês.

- **Site:** https://fbrandao2k.github.io/alice-no-pais-das-maravilhas/
- **Jogar no navegador:** https://fbrandao2k.github.io/alice-no-pais-das-maravilhas/jogar/
- **Baixar o jogo (Windows):** [AliceNoPaisDasMaravilhas-Windows.zip](https://github.com/fbrandao2k/alice-no-pais-das-maravilhas/releases/latest/download/AliceNoPaisDasMaravilhas-Windows.zip), na página de [versões](https://github.com/fbrandao2k/alice-no-pais-das-maravilhas/releases).

*A free game in eleven episodes, based on Lewis Carroll's book, in Portuguese and English. [Play in the browser](https://fbrandao2k.github.io/alice-no-pais-das-maravilhas/jogar/?lang=en) or download it for Windows.*

---

## Maintenance notes (English)

This repository holds only what is public: the website and the playable game, served by GitHub Pages from `main` (root). The game's source lives in a separate private repository (`Game2D_AliceNoPaisDasMaravilhas`), with its working files.

- `index.html`: the page GitHub Pages serves. Do not edit it by hand.
- `tools/preview_page.html`: the source of the page, written for claude.ai previews (no document skeleton). Edit this, then rebuild `index.html` with `python tools/wrap_page.py tools/preview_page.html index.html`.
- `jogar/`: the game itself, a copy of the game repo's `dist/` (`npm run build`). Do not edit it by hand.
- `img/`: the site's pictures, exported from the game's art and screenshots.
- `tools/build_site.py`: rebuilds `img/` and `jogar/` from the game repo at `D:\Games\AliceNoPaisDasMaravilhas`. Build the game and run both playthroughs there first (`npm run build`, `npm run test:e2e -- --build` and `npm run test:e2e -- --build --lang=en`), since the gallery uses their screenshots. `--no-game` skips `jogar/`.
- The Windows ZIP is a release asset, never committed. Make it in the game repo with `npm run package:win -- --check` (it lands in `release/`), then attach it to a new release here under the same file name, so the download link keeps working.

To publish a new version of the game: build it, run `python tools/build_site.py`, commit `jogar/` (and `img/` if it changed), push, and upload the new ZIP to a new release.
