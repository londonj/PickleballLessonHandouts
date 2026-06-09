# Pickleball Lesson Handouts

Reusable project for creating consistently formatted student handouts for pickleball lessons.

The goal is to keep content and visual design separate:

- `templates/student-handout-template.md` defines the handout structure and content rules.
- `templates/new-handout-starter.md` is a blank handout file with the required headings already in place.
- `templates/handout-style.css` defines the locked visual system: fonts, colors, heading bars, spacing, margins, and page-break behavior.
- `prompts/create-student-handout.md` contains a reusable prompt for generating new handouts.
- `docs/how-to-create-new-handouts.md` is the full handoff guide for creating new documents.
- `docs/how-to-create-new-handouts.pdf` is the printable PDF version of that handoff guide.
- `docs/production-checklist.md` is the review checklist to use before sharing a PDF.
- `docs/style-system.md` documents the shared visual design rules.
- `scripts/build-handout-pdf.py` converts a Markdown handout into a PDF using the shared style.
- `scripts/build-doc-pdf.py` converts project documentation Markdown into a polished PDF.
- `examples/` contains completed Markdown handouts that can be copied for future lessons.
- `outputs/` is where generated PDFs should go.
- `work/` stores generated HTML and page preview images for visual checks.

## Standard Workflow

1. Copy `templates/student-handout-template.md` or an existing file from `examples/`.
2. Write the new lesson handout in Markdown.
3. Keep drills in `7. Homework 🏠`, quick review cues in `10. Quick Reminders 🎗️`, and outside links in `11. Resources 🔗`.
4. Build the PDF with the shared stylesheet.
5. Open the generated preview images in `work/` and visually check page breaks before sharing the PDF.
6. Run through `docs/production-checklist.md`.

## Build Example

From this folder:

```powershell
python .\scripts\build-handout-pdf.py .\examples\third-shot-drop-student-handout.md -o .\outputs\third-shot-drop-student-handout.pdf
```

By default, no section is forced onto a new page. Each section is kept together and sections flow to fill each page, moving to the next page only when they will not fit as a whole. To force specific sections to start on a new page for a particular handout:

```powershell
python .\scripts\build-handout-pdf.py .\examples\third-shot-drop-student-handout.md --page-start-sections 11
```

## Requirements

- Google Chrome or Microsoft Edge for PDF generation.
- Python 3.10 or newer.
- Optional but recommended:
  - `pypdf` for text checks.
  - `pymupdf` for rendered PNG page previews.

Install optional packages:

```powershell
python -m pip install pypdf pymupdf
```

Or install from the project requirements file:

```powershell
python -m pip install -r requirements.txt
```

## Visual Consistency Rules

Do not manually style individual handouts. If colors, fonts, margins, section heading shapes, or resource spacing need to change, update `templates/handout-style.css` so every future PDF changes together.

Do not duplicate practice content in Resources. Resources are for outside articles, videos, and rule or strategy references only.
