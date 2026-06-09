# Handout Production Checklist

Use this checklist before sharing a student handout PDF.

Every topic ships as two versions — the full handout and the brief one-page version. Both are required. Run the Content, Resources, and PDF Layout checks below against the full handout, then complete the Brief Version checklist for its companion.

## Content

- The lesson topic appears as the title.
- All 11 required sections are present and in order.
- Section headings use the exact required emojis.
- The writing is student-facing, practical, and encouraging.
- Technical terms are explained simply.
- The Big Idea is focused and memorable.
- Homework contains practice drills and assignments.
- Quick Reminders contains only short pre-play cues.
- Resources contains outside references only.
- No drills or review lists are duplicated in Resources.

## Resources

- Exactly three article links are included.
- The three articles come from three different websites or sources.
- Exactly three YouTube videos are included.
- The three videos come from three different creators or channels.
- Rules and Strategy References are relevant and external.
- Links were checked at the time the handout was created.

## PDF Layout

- The PDF was built with `scripts/build-handout-pdf.py`.
- The PDF uses `templates/handout-style.css`.
- The generated preview PNGs were visually inspected (not just the page count).
- No numbered section is split across two pages. Each section sits wholly on one page.
- Pages are reasonably filled; there is no large gap of white space left by a forced page break that more content could have filled.
- The Resources section is visible and complete.
- No text is clipped, overlapped, or unreadably small.
- Link titles with special characters render correctly.

## Brief Version

- A brief companion exists for this topic (this is required, not optional).
- Markdown is saved as `examples/Lesson-Handout-{Technique}-Brief.md` and the PDF as `outputs/Lesson-Handout-{Technique}-Brief.pdf`.
- It includes only nine sections, renumbered 1–9: Lesson Recap, Big Idea, Key Cues, Step-by-Step, Common Mistakes, Self-Check, Homework, Game Application, Quick Reminders.
- The Visualization and Resources sections are omitted.
- No section has more than three items; prose sections are a few short sentences.
- The preview PNGs were visually inspected and it renders on exactly one page with no section split.

## Files

- Markdown sources (full and brief) are saved in `examples/` or another intentional source folder.
- Both PDF outputs (full and brief) are saved in `outputs/`.
- Generated HTML and PNG previews are in `work/`.
- Any visual style changes were made in `templates/handout-style.css`, not manually in one PDF.

