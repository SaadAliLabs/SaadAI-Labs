#!/usr/bin/env python3
"""Render a storyboard contact sheet (one frame per scene) for approval before voicing/rendering.

    python3 storyboard.py <short_dir> [--final]

Default uses props.draft.json (run `build.py <dir> --draft` first). --final uses props.json.
Writes <short_dir>/storyboard.jpg (scene number, type and the narration under each frame).
"""
import shutil
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import ENGINE, FPS, die, load_json, need_engine, run  # noqa: E402

FONT = ENGINE / "public" / "fonts" / "Inter.ttf"


def sheet(frames, labels, out: Path, cols=4, w=270, h=480):
    pad, cap = 14, 92
    rows = (len(frames) + cols - 1) // cols
    img = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + cap + pad) + pad), (24, 24, 32))
    d = ImageDraw.Draw(img)
    try:
        f1 = ImageFont.truetype(str(FONT), 17)
        f2 = ImageFont.truetype(str(FONT), 13)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    for k, (fp, (head, body)) in enumerate(zip(frames, labels)):
        x = pad + (k % cols) * (w + pad)
        y = pad + (k // cols) * (h + cap + pad)
        im = Image.open(fp).convert("RGB").resize((w, h))
        img.paste(im, (x, y))
        d.text((x, y + h + 6), head, fill=(255, 210, 63), font=f1)
        for j, line in enumerate(textwrap.wrap(body, 38)[:4]):
            d.text((x, y + h + 30 + j * 15), line, fill=(220, 220, 230), font=f2)
    img.save(out, quality=88)


def main():
    if len(sys.argv) < 2:
        die(__doc__)
    need_engine()
    short_dir = Path(sys.argv[1]).resolve()
    final = "--final" in sys.argv
    props_p = short_dir / ("props.json" if final else "props.draft.json")
    props = load_json(props_p)
    spec = load_json(short_dir / "short.json")
    frames = [s["start"] + max(int(s["dur"] * 0.62), min(s["dur"] - 1, 24)) for s in props["scenes"]]
    tmp = short_dir / ".stills"
    shutil.rmtree(tmp, ignore_errors=True)
    run(["node", "scripts/stills.mjs", str(props_p), str(tmp), ",".join(map(str, frames)), "0.25"], cwd=ENGINE, quiet=True)
    files = sorted(tmp.glob("f*.png"))
    labels = []
    for i, (s, sc) in enumerate(zip(props["scenes"], spec["scenes"])):
        labels.append((f"{i + 1}. {s['type']}  {s['start'] / FPS:.1f}s", sc.get("say", "") or "(no narration)"))
    out = short_dir / "storyboard.jpg"
    sheet(files, labels, out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"storyboard: {out}")


if __name__ == "__main__":
    main()
