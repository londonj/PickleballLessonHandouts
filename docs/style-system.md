# Handout Style System

This project uses one shared stylesheet to keep every handout visually consistent.

## Single Source of Truth

All visual design decisions live in:

`templates/handout-style.css`

Change this file when you want to update:

- page margins
- font family
- font sizes
- line height
- colors
- heading bar style
- border radius
- link color
- bullet spacing
- Resources compaction
- print page-break behavior

Do not manually restyle individual PDFs. Future handouts should differ in content only.

## Current Design Tokens

- Body font: Aptos, Segoe UI, Arial, sans-serif
- Body size: 10.25pt
- Main title size: 30pt
- Section heading size: 14.5pt
- Subheading size: 11.8pt
- Body color: `#1f2933`
- Teal accent: `#0f766e`
- Blue accent: `#2563eb`
- Standard section background: `#e8f5f2`
- Resources section background: `#eef2ff`
- Heading radius: 5px
- Title radius: 8px

## Page-Break Policy

Every numbered section is kept together so it never splits across pages. Each section is wrapped in a `.handout-section` element with `break-inside: avoid`, so a section that will not fit in the remaining space moves to the next page as a whole. This can leave white space at the bottom of a page, which is acceptable. A section is only forced to break if it is too tall to fit on a single page on its own; in that case, shorten the section.

The PDF builder also starts sections 8 and 11 on new pages by default, which keeps Game Application and Resources leading their own pages.

Override the page starts only when a specific handout genuinely reads better with different page starts:

```powershell
python .\scripts\build-handout-pdf.py .\examples\example.md --page-start-sections 11
```

