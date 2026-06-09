# Create a Pickleball Student Handout

Use this prompt when asking an AI assistant to create a new handout for this project.

**Every topic always gets two versions: the full handout and the brief one-page version. Both are required deliverables every time — never produce only one.**

```text
Create a student-facing pickleball lesson handout for: [LESSON TOPIC].

Produce BOTH required versions for this topic: the full handout and the brief one-page version. Both are mandatory every time.

Use the template at:
C:\Coding\Pickleball_Lesson_Handouts\templates\student-handout-template.md

== PART 1: FULL HANDOUT ==

Follow these rules:
- Use the exact numbered section headings and emojis from the template.
- Write for beginner to intermediate adult students.
- Keep the tone clear, practical, encouraging, and coach-like.
- Do not frame the handout around a lesson or a point in time. Open by describing the skill directly (for example "The dink volley is...") rather than "This lesson covers..." or "today's lesson," so the handout reads correctly whenever the student reviews it.
- Put all practice drills and assignments in 7. Homework 🏠.
- Put quick pre-play reminders in 10. Quick Reminders 🎗️.
- Put only outside references in 11. Resources 🔗.
- Do not duplicate drills or review lists in Resources.
- Use current web research for Resources.
- Include exactly three article links from three different sources.
- Include exactly three YouTube links from three different creators/channels.
- Include useful rule or strategy references only when they support the lesson.
- A numbered section must never split across pages. The build keeps each section together automatically; if a section is too tall to fit on one page, shorten it so it fits.
- Always visually inspect the rendered preview PNGs after building, and confirm no section is split across pages. Never rely on page count alone.
- Name the files using the pattern Lesson-Handout-[Technique] in Title-Case with dashes (for example Lesson-Handout-Overhead-Smash). Save the finished Markdown handout in:
  C:\Coding\Pickleball_Lesson_Handouts\examples\Lesson-Handout-[Technique].md

Build the full PDF using:
python C:\Coding\Pickleball_Lesson_Handouts\scripts\build-handout-pdf.py C:\Coding\Pickleball_Lesson_Handouts\examples\Lesson-Handout-[Technique].md -o C:\Coding\Pickleball_Lesson_Handouts\outputs\Lesson-Handout-[Technique].pdf

Visually inspect the preview PNGs in:
C:\Coding\Pickleball_Lesson_Handouts\work\lesson-handout-[technique]-preview
Confirm no section breaks across pages and that Resources is present and coherent.

== PART 2: BRIEF ONE-PAGE VERSION (also required) ==

Create the condensed one-page companion to the full handout above.

Follow these rules:
- Everything must fit on a single page.
- Include only these sections, in order, keeping the same titles and emojis but renumbered consecutively 1–9: 1. Lesson Recap 🧠, 2. Big Idea 💡, 3. Key Cues 🎯, 4. Step-by-Step 👣, 5. Common Mistakes ⚠️, 6. Self-Check ✅, 7. Homework 🏠, 8. Game Application 🎮, 9. Quick Reminders 🎗️.
- Omit the Visualization and Resources sections entirely.
- No section may contain more than three items. Keep the three most important per section, using best judgment. Keep prose sections to a few short sentences.
- Keep the same tone and the same rule against lesson- or time-anchored framing.
- Name the files Lesson-Handout-[Technique]-Brief in Title-Case with dashes. Save the Markdown in:
  C:\Coding\Pickleball_Lesson_Handouts\examples\Lesson-Handout-[Technique]-Brief.md

Build the brief PDF with:
python C:\Coding\Pickleball_Lesson_Handouts\scripts\build-handout-pdf.py C:\Coding\Pickleball_Lesson_Handouts\examples\Lesson-Handout-[Technique]-Brief.md -o C:\Coding\Pickleball_Lesson_Handouts\outputs\Lesson-Handout-[Technique]-Brief.pdf

Visually inspect the preview PNGs and confirm the handout renders on exactly one page with no section split.

== DELIVER ==

Confirm both versions are complete: two Markdown files in examples\ and two PDFs in outputs\ (full and brief), each visually verified.
```

