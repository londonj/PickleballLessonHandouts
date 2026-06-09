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
- Put all practice drills and assignments in 7. Homework 🏠.
- Put quick pre-play reminders in 10. Before You Play Again 🔁.
- Put only outside references in 11. Resources 🔗.
- Do not duplicate drills or review lists in Resources.
- Use current web research for Resources.
- Include exactly three article links from three different sources.
- Include exactly three YouTube links from three different creators/channels.
- Include useful rule or strategy references only when they support the lesson.
- Save the finished Markdown handout in:
  C:\Coding\Pickleball_Lesson_Handouts\examples\[lesson-slug]-student-handout.md

After writing the Markdown, build the PDF using:
python C:\Coding\Pickleball_Lesson_Handouts\scripts\build-handout-pdf.py C:\Coding\Pickleball_Lesson_Handouts\examples\[lesson-slug]-student-handout.md -o C:\Coding\Pickleball_Lesson_Handouts\outputs\[lesson-slug]-student-handout.pdf

Before delivering the PDF, visually inspect the generated preview PNGs in:
C:\Coding\Pickleball_Lesson_Handouts\work\[lesson-slug]-student-handout-preview

Confirm that major sections do not break awkwardly across pages and that Resources is present and coherent.
```

