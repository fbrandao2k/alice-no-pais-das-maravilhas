"""Builds the website's pictures (img/) and the playable game (jogar/) from the game repo.

Usage: python tools/build_site.py [--no-game]

Needs the game repo at GAME, built with `npm run build`. The gallery comes from its
screenshots: `npm run test:e2e -- --build` (Portuguese, test-results/) and
`npm run test:e2e -- --build --lang=en` (English, test-results/en/).
"""
import shutil
import sys
from pathlib import Path

from PIL import Image

GAME = Path(r"D:\Games\AliceNoPaisDasMaravilhas")
SITE = Path(__file__).resolve().parent.parent
IMG = SITE / "img"
ASSETS = GAME / "public" / "assets"

# The game's paintings: name in img/, file under public/assets/, width.
PAINTINGS = {
    "hero": ("bg/title.webp", 1600),
    "riverbank": ("bg/riverbank.webp", 960),
    "ep01": ("bg/smalldoor_open.webp", 720),
    **{f"ep{n:02}": (f"bg/ep{n}_title.webp", 720) for n in range(2, 12)},
}
PORTRAITS = {
    "alice": "portraits/alice_happy.webp",
    "rabbit": "portraits/rabbit_worried.webp",
    "caterpillar": "portraits/caterpillar.webp",
    "cat": "portraits/cat.webp",
    "duchess": "portraits/duchess.webp",
    "queen": "portraits/queen.webp",
    "gryphon": "portraits/gryphon.webp",
    "mockturtle": "portraits/mockturtle.webp",
}
# The gallery: a screenshot's name in the test run (NN-name.png) and its name in img/. The
# Episode 11 pair (the whole pack at once) was taken by hand: tools/shots/cards-pt.png, -en.png.
SHOTS = {
    "race": "shot-race",
    "giant-catch": "shot-giant",
    "twinkle-song": "shot-twinkle",
    "croquet": "shot-croquet",
    "court": "shot-court",
    "cards": "shot-cards",
}


def webp(image, name, width, quality=80):
    if image.width > width:
        image = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
    out = IMG / f"{name}.webp"
    image.save(out, "WEBP", quality=quality, method=6)
    return out


def shot(folder, name, lang):
    # A screenshot chosen by hand (tools/shots/<name>-pt.png or -en.png) wins over the test's.
    chosen = SITE / "tools" / "shots" / f"{name}-{lang}.png"
    if chosen.exists():
        return Image.open(chosen).convert("RGB")
    found = sorted(folder.glob(f"[0-9]*-{name}.png"))
    if not found:
        sys.exit(f"no screenshot {name} in {folder}: run the playthrough first")
    return Image.open(found[-1]).convert("RGB")


def main():
    IMG.mkdir(exist_ok=True)
    for name, (src, width) in PAINTINGS.items():
        webp(Image.open(ASSETS / src).convert("RGB"), name, width)
    for name, src in PORTRAITS.items():
        webp(Image.open(ASSETS / src).convert("RGBA"), name, 192, quality=85)
    webp(Image.open(ASSETS / "chars/cat/cat_grin.webp").convert("RGBA"), "grin", 312, quality=90)
    for icon in ("icon-64.png", "icon-192.png"):
        shutil.copyfile(GAME / "public" / icon, IMG / icon)
    # The picture shown when the site is shared: the title painting at 1200 × 630.
    title = Image.open(ASSETS / "bg/title.webp").convert("RGB")
    h = round(title.width * 630 / 1200)
    title.crop((0, (title.height - h) // 2, title.width, (title.height + h) // 2)).resize((1200, 630), Image.LANCZOS).save(
        IMG / "social.jpg", "JPEG", quality=85
    )
    for test, name in SHOTS.items():
        webp(shot(GAME / "test-results", test, "pt"), f"{name}-pt", 960)
        webp(shot(GAME / "test-results" / "en", test, "en"), f"{name}-en", 960)
    print("pictures:", len(list(IMG.iterdir())), "files in", IMG)

    if "--no-game" not in sys.argv:
        dist = GAME / "dist"
        if not (dist / "index.html").exists():
            sys.exit("the game isn't built: run `npm run build` in the game repo")
        shutil.rmtree(SITE / "jogar", ignore_errors=True)
        shutil.copytree(dist, SITE / "jogar")
        size = sum(f.stat().st_size for f in (SITE / "jogar").rglob("*") if f.is_file())
        print(f"game: jogar/ ({size / 1e6:.0f} MB)")


main()
