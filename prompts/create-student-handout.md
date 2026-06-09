# Create a Pickleball Student Handout

Use this prompt when asking an AI assistant to create a new handout for this project.

```text
Create a student-facing pickleball lesson handout for: [LESSON TOPIC].

Use the template at:
C:\Coding\Pickleball_Lesson_Handouts\templates\student-handout-template.md

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
- Save the finished Markdown handout in:
  C:\Coding\Pickleball_Lesson_Handouts\examples\[lesson-slug]-student-handout.md

After writing the Markdown, build the PDF using:
python C:\Coding\Pickleball_Lesson_Handouts\scripts\build-handout-pdf.py C:\Coding\Pickleball_Lesson_Handouts\examples\[lesson-slug]-student-handout.md -o C:\Coding\Pickleball_Lesson_Handouts\outputs\[lesson-slug]-student-handout.pdf

Before delivering the PDF, visually inspect the generated preview PNGs in:
C:\Coding\Pickleball_Lesson_Handouts\work\[lesson-slug]-student-handout-preview

Confirm that major sections do not break awkwardly across pages and that Resources is present and coherent.
```

