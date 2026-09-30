---
name: status-report-generator
description: Generates a daily status report from a raw activity log (commits, tickets, meeting notes, chat updates). Use whenever the user asks for a daily status report, standup summary, or end-of-day update from an activity log.
---

# Daily Status Report Generator

Turn a raw activity log into a daily status report a PM can read in under 60 seconds.

## Procedure

1. Read the whole activity log before writing anything.
2. Group entries by workstream or project, not by person or timestamp.
3. Classify each item as **Done**, **In progress**, or **Blocked**.
4. Drop noise: routine meetings with no decisions, duplicate entries, trivial chores.
5. Write the report using the exact template below.

## Template

```
# Daily Status Report — <Month D, YYYY>

**Overall status:** 🟢 On track | 🟡 At risk | 🔴 Off track
**TL;DR:** <One sentence: the single most important thing that happened today.>

## ✅ Completed
- <Workstream>: <what shipped or got decided>. (<owner>)

## 🔄 In progress
- <Workstream>: <what's moving> — <expected completion>. (<owner>)

## 🚧 Blockers
- <Blocker> — **Impact:** <what it delays> — **Needs:** <who/what unblocks it> — **Owner:** <name>

## 📅 Next 24 hours
- <Top 3 priorities max>
```

## Rules

- **Tone:** factual, neutral, no hype. No "great progress!" or "amazing work".
- **Length:** whole report under 250 words. Each bullet is one line.
- **Summarize outcomes, not activity.** "Checkout API merged to main" beats "worked on checkout API all day".
- **Blockers:**
  - Every blocker must name an owner and what unblocks it. If the log doesn't say, write `Owner: TBD` rather than guessing.
  - Any blocker older than 2 days, or blocking a deadline this week, sets overall status to 🟡 or 🔴.
  - If there are no blockers, write `- None` — never omit the section.
- **Overall status:** 🟢 if no blockers threaten a deadline; 🟡 if one does; 🔴 if a deadline will be missed.
- **Dates and names:** use what's in the log. Never invent owners, dates, or numbers.
- If the log is empty or unreadable, say so in one line instead of producing a report.
