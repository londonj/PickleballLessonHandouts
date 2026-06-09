from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STYLE = ROOT / "templates" / "document-style.css"
DEFAULT_WORK = ROOT / "work"


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
    return value.strip("-") or "document"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"`([^`]+)`",
        lambda match: f"<code>{match.group(1)}</code>",
        escaped,
    )
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}">'
            f"{match.group(1)}</a>"
        ),
        escaped,
    )
    escaped = re.sub(
        r"&lt;(https?://[^&]+)&gt;",
        lambda match: f'<a href="{html.escape(match.group(1), quote=True)}">{match.group(1)}</a>',
        escaped,
    )
    return escaped


def markdown_to_html(markdown: str) -> tuple[str, str]:
    blocks: list[str] = []
    lines = markdown.splitlines()
    title = "Document"
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        if not line:
            i += 1
            continue

        if line.startswith("```"):
            language = line[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            language_class = f' class="language-{html.escape(language)}"' if language else ""
            code = html.escape("\n".join(code_lines))
            blocks.append(f"<pre><code{language_class}>{code}</code></pre>")
            continue

        if line.startswith("# "):
            title = line[2:].strip()
            blocks.append(f"<h1>{inline_markdown(title)}</h1>")
            i += 1
            continue

        if line.startswith("## "):
            blocks.append(f"<h2>{inline_markdown(line[3:].strip())}</h2>")
            i += 1
            continue

        if line.startswith("### "):
            blocks.append(f"<h3>{inline_markdown(line[4:].strip())}</h3>")
            i += 1
            continue

        if line.startswith("- "):
            items: list[str] = []
            while i < len(lines) and lines[i].rstrip().startswith("- "):
                item_parts = [lines[i].rstrip()[2:].strip()]
                i += 1
                while (
                    i < len(lines)
                    and lines[i].strip()
                    and not lines[i].startswith(("#", "- ", "```"))
                    and not re.match(r"^\d+\. ", lines[i])
                ):
                    item_parts.append(lines[i].strip())
                    i += 1
                items.append(inline_markdown(" ".join(item_parts)))
            blocks.append("<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\d+\. ", line):
            items: list[str] = []
            while i < len(lines):
                numbered = lines[i].rstrip()
                match = re.match(r"^\d+\. (.*)$", numbered)
                if not match:
                    break
                item_parts = [match.group(1).strip()]
                i += 1
                while (
                    i < len(lines)
                    and lines[i].strip()
                    and not lines[i].startswith(("#", "- ", "```"))
                    and not re.match(r"^\d+\. ", lines[i])
                ):
                    item_parts.append(lines[i].strip())
                    i += 1
                items.append(inline_markdown(" ".join(item_parts)))
            blocks.append("<ol>" + "".join(f"<li>{item}</li>" for item in items) + "</ol>")
            continue

        paragraph = [line]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith(("#", "- ", "```"))
            and not re.match(r"^\d+\. ", lines[i])
        ):
            paragraph.append(lines[i].strip())
            i += 1
        blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")

    return "\n".join(blocks), title


def build_html(markdown: str, style: str) -> tuple[str, str]:
    body, title = markdown_to_html(markdown)
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
  <main class="doc">
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
        pix = page.get_pixmap(matrix=fitz.Matrix(1.35, 1.35), alpha=False)
        pix.save(preview_dir / f"page-{idx}.png")
    return len(doc)


def text_check(pdf: Path, required: list[str]) -> int | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None

    reader = PdfReader(str(pdf))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"PDF text check failed. Missing: {missing}")
    return len(reader.pages)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a styled PDF from a project Markdown document.")
    parser.add_argument("source", type=Path, help="Markdown document to convert.")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF path.")
    parser.add_argument("--style", type=Path, default=DEFAULT_STYLE, help="CSS stylesheet path.")
    parser.add_argument("--required", action="append", default=[], help="Required text to verify in the PDF.")
    parser.add_argument("--no-preview", action="store_true", help="Skip rendered PNG page previews.")
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    style_path = args.style.resolve()
    html_out = DEFAULT_WORK / f"{slugify(source.stem)}-doc.html"
    preview_dir = DEFAULT_WORK / f"{slugify(source.stem)}-doc-preview"

    DEFAULT_WORK.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    html_doc, title = build_html(
        source.read_text(encoding="utf-8"),
        style_path.read_text(encoding="utf-8"),
    )
    html_out.write_text(html_doc, encoding="utf-8")

    subprocess.run(
        [
            str(find_chrome()),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output}",
            html_out.resolve().as_uri(),
        ],
        check=True,
    )

    required = args.required or [title]
    page_count = text_check(output, required)
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
