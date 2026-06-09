from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STYLE = ROOT / "templates" / "handout-style.css"
DEFAULT_WORK = ROOT / "work"
DEFAULT_OUTPUT = ROOT / "outputs"
# No sections are forced onto a new page by default. Each section is kept
# together (break-inside: avoid in the stylesheet), so sections flow and fill
# each page, moving to the next page only when they will not fit as a whole.
# Use --page-start-sections to force specific sections to lead a page.
DEFAULT_PAGE_START_SECTIONS: set[int] = set()


def find_chrome() -> Path:
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    for name in ("chrome", "chrome.exe", "msedge", "msedge.exe"):
        found = shutil.which(name)
        if found:
            return Path(found)
    raise FileNotFoundError("Chrome or Edge was not found. Install one of them or add it to PATH.")


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "student-handout"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}">'
            f"{match.group(1)}</a>"
        ),
        escaped,
    )


def section_number(line: str) -> int | None:
    match = re.match(r"^##\s+(\d+)\.", line)
    return int(match.group(1)) if match else None


def markdown_to_html(markdown: str, page_start_sections: set[int]) -> tuple[str, str]:
    blocks: list[str] = []
    lines = markdown.splitlines()
    title = "Student Handout"
    section_open = False
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        if not line:
            i += 1
            continue

        if line.startswith("# "):
            title = line[2:].strip()
            blocks.append(f"<h1>{inline_markdown(title)}</h1>")
            i += 1
            continue

        if line.startswith("## "):
            if section_open:
                blocks.append("</section>")
            number = section_number(line)
            # Each numbered section is wrapped so it is kept together on one
            # page (break-inside: avoid). Sections that should always lead a
            # page get the page-start class instead.
            section_classes = ["handout-section"]
            h2_classes: list[str] = []
            if number in page_start_sections:
                section_classes.append("page-start")
            if number == 11 or "Resources" in line:
                h2_classes.append("section-resources")
            blocks.append(f'<section class="{" ".join(section_classes)}">')
            section_open = True
            heading = inline_markdown(line[3:].strip())
            class_attr = f' class="{" ".join(h2_classes)}"' if h2_classes else ""
            blocks.append(f"<h2{class_attr}>{heading}</h2>")
            i += 1
            continue

        if line.startswith("### "):
            blocks.append(f"<h3>{inline_markdown(line[4:].strip())}</h3>")
            i += 1
            continue

        if line.startswith("- "):
            items: list[str] = []
            while i < len(lines):
                item_line = lines[i].rstrip()
                if not item_line.startswith("- "):
                    break
                parts = [item_line[2:].strip()]
                i += 1
                while i < len(lines):
                    continuation = lines[i].rstrip()
                    if not continuation:
                        i += 1
                        continue
                    if continuation.startswith(("#", "- ")) or re.match(r"^\d+\. ", continuation):
                        break
                    parts.append(continuation.strip())
                    i += 1
                items.append(format_bullet_parts(parts))
            blocks.append("<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\d+\. ", line):
            items: list[str] = []
            while i < len(lines):
                numbered = lines[i].rstrip()
                match = re.match(r"^\d+\. (.*)$", numbered)
                if not match:
                    break
                items.append(inline_markdown(match.group(1).strip()))
                i += 1
            blocks.append("<ol>" + "".join(f"<li>{item}</li>" for item in items) + "</ol>")
            continue

        paragraph = [line]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith(("#", "- "))
            and not re.match(r"^\d+\. ", lines[i])
        ):
            paragraph.append(lines[i].strip())
            i += 1
        blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")

    if section_open:
        blocks.append("</section>")

    return "\n".join(blocks), title


def format_bullet_parts(parts: list[str]) -> str:
    if len(parts) == 1:
        return inline_markdown(parts[0])

    first, *rest = parts
    formatted = inline_markdown(first)
    for part in rest:
        class_name = "source-line" if part.startswith(("Source:", "Channel:")) else "description-line"
        formatted += f'<br><span class="{class_name}">{inline_markdown(part)}</span>'
    return formatted


def build_html(markdown: str, style: str, page_start_sections: set[int], brief: bool = False) -> tuple[str, str]:
    body, title = markdown_to_html(markdown, page_start_sections)
    sheet_class = "sheet brief" if brief else "sheet"
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
{style}
  </style>
</head>
<body>
  <main class="{sheet_class}">
{body}
  </main>
</body>
</html>
"""
    return document, title


def render_previews(pdf: Path, preview_dir: Path) -> int | None:
    try:
        import fitz  # type: ignore
    except Exception:
        return None

    preview_dir.mkdir(parents=True, exist_ok=True)
    for old in preview_dir.glob("page-*.png"):
        old.unlink()

    doc = fitz.open(pdf)
    for idx, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False)
        pix.save(preview_dir / f"page-{idx}.png")
    return len(doc)


def extract_text_check(pdf: Path, require_resources: bool = True) -> int | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None

    reader = PdfReader(str(pdf))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    # Brief one-page handouts omit Resources by design, so it is only required
    # for the full handout.
    required_sections = ["Lesson Recap"]
    if require_resources:
        required_sections.append("Resources")
    for required in required_sections:
        if required not in text:
            raise RuntimeError(f"PDF text check failed. Missing: {required}")
    return len(reader.pages)


def parse_section_set(raw: str) -> set[int]:
    if not raw.strip():
        return set()
    return {int(part.strip()) for part in raw.split(",") if part.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a consistently styled pickleball lesson handout PDF.")
    parser.add_argument("source", type=Path, help="Markdown handout to convert.")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF path.")
    parser.add_argument("--style", type=Path, default=DEFAULT_STYLE, help="CSS stylesheet path.")
    parser.add_argument(
        "--page-start-sections",
        default="",
        help="Comma-separated numbered sections that should always start on a new page. Empty by default; sections are kept together and flow to fill each page.",
    )
    parser.add_argument("--no-preview", action="store_true", help="Skip rendered PNG page previews.")
    args = parser.parse_args()

    source = args.source.resolve()
    style_path = args.style.resolve()
    output = args.output.resolve() if args.output else DEFAULT_OUTPUT / f"{slugify(source.stem)}.pdf"
    html_out = DEFAULT_WORK / f"{slugify(source.stem)}.html"
    preview_dir = DEFAULT_WORK / f"{slugify(source.stem)}-preview"
    page_start_sections = parse_section_set(args.page_start_sections)

    DEFAULT_OUTPUT.mkdir(parents=True, exist_ok=True)
    DEFAULT_WORK.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    is_brief = "brief" in source.stem.lower()
    markdown = source.read_text(encoding="utf-8")
    style = style_path.read_text(encoding="utf-8")
    html_doc, title = build_html(markdown, style, page_start_sections, brief=is_brief)
    html_out.write_text(html_doc, encoding="utf-8")

    chrome = find_chrome()
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

    page_count = extract_text_check(output, require_resources=not is_brief)
    preview_count = None if args.no_preview else render_previews(output, preview_dir)

    print(f"Title: {title}")
    print(f"PDF: {output}")
    print(f"HTML: {html_out}")
    if page_count is not None:
        print(f"Text-check pages: {page_count}")
    if preview_count is not None:
        print(f"Preview pages: {preview_count}")
        print(f"Preview folder: {preview_dir}")
    else:
        print("Preview rendering skipped; install PyMuPDF with: python -m pip install pymupdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
