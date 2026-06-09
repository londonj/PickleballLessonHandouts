"""Build a compact, upload-friendly handout PDF.

Chrome's color-emoji glyphs (Segoe UI Emoji) embed as hundreds of vector
objects and balloon a 4-page handout to ~600 KB. The Google Drive upload tool
requires the file to be inlined as base64, so we need a much smaller PDF.

This script reuses the normal handout HTML generation, but replaces each emoji
with a small PNG rendered once from Segoe UI Emoji and embedded inline as a
data URI. The result looks identical at heading size while dropping the file to
~120 KB. The canonical full-quality PDF from build-handout-pdf.py is unchanged;
this is only for producing an upload copy.

Usage:
    python scripts/compact-handout-pdf.py <handout.md> -o <out.pdf>
"""
from __future__ import annotations

import argparse
import base64
import importlib.util
import io
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EMOJI_FONT = Path(r"C:\Windows\Fonts\seguiemj.ttf")
# Render emoji at this pixel size, then display at 1em. 2x heading size keeps
# them crisp when printed.
RENDER_PX = 72

# Match runs of emoji codepoints, keeping a base glyph together with any
# variation selector (FE0F), ZWJ (200D), or skin-tone modifier.
EMOJI_RE = re.compile(
    "([\U0001F000-\U0001FAFF☀-➿⬀-⯿←-⇿⌀-⏿"
    "️‍\U0001F3FB-\U0001F3FF]+)"
)


def load_builder():
    path = ROOT / "scripts" / "build-handout-pdf.py"
    spec = importlib.util.spec_from_file_location("handout_builder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_emoji_png(cluster: str) -> str:
    font = ImageFont.truetype(str(EMOJI_FONT), RENDER_PX)
    canvas = RENDER_PX + 16
    img = Image.new("RGBA", (canvas, canvas), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.text((8, 4), cluster, font=font, embedded_color=True)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def replace_emoji_with_images(html_doc: str) -> str:
    cache: dict[str, str] = {}

    def sub(match: re.Match) -> str:
        cluster = match.group(1)
        # Leave a bare variation selector / ZWJ alone if it somehow matches.
        if all(ord(c) in (0xFE0F, 0x200D) for c in cluster):
            return match.group(0)
        if cluster not in cache:
            cache[cluster] = render_emoji_png(cluster)
        data = cache[cluster]
        return (
            f'<img class="emoji" alt="{cluster}" '
            f'src="data:image/png;base64,{data}">'
        )

    html_doc = EMOJI_RE.sub(sub, html_doc)
    emoji_css = (
        ".emoji{height:1em;width:auto;vertical-align:-0.15em;"
        "margin:0 0.05em;display:inline-block;}"
    )
    return html_doc.replace("</style>", emoji_css + "\n</style>", 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a compact upload-ready handout PDF.")
    parser.add_argument("source", type=Path, help="Markdown handout to convert.")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF path.")
    parser.add_argument("--page-start-sections", default="")
    args = parser.parse_args()

    builder = load_builder()
    source = args.source.resolve()
    output = args.output.resolve()
    style = builder.DEFAULT_STYLE.read_text(encoding="utf-8")
    markdown = source.read_text(encoding="utf-8")
    page_start = builder.parse_section_set(args.page_start_sections)

    html_doc, title = builder.build_html(markdown, style, page_start)
    html_doc = replace_emoji_with_images(html_doc)

    work = ROOT / "work"
    work.mkdir(parents=True, exist_ok=True)
    html_out = work / f"{builder.slugify(source.stem)}-compact.html"
    html_out.write_text(html_doc, encoding="utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    chrome = builder.find_chrome()
    subprocess.run(
        [
            str(chrome),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output}",
            html_out.resolve().as_uri(),
        ],
        check=True,
    )
    print(f"Title: {title}")
    print(f"Compact PDF: {output}")
    print(f"Bytes: {output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
