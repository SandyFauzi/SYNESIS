---
name: lesson-plan-designer
description: >
  Builds a single class session minute-by-minute: an opening hook that creates
  the question, a timed plan with activity/purpose/duration, at least two active
  learning moments, transitions written out verbatim, a formative check at the
  halfway point, a closing reflection that maps to the next session, a backup
  move for when energy drops, and a materials list. Use when the user says
  "lesson plan designer", "plan this class session", "build a lesson plan",
  "minute-by-minute plan", "design tomorrow's class", or invokes
  /lesson-plan-designer.
---

# Lesson Plan Designer

Choreograph one class session end to end — what happens, when, why, and what to
do when it stops working.

This skill designs **how the room runs**. For what gets taught and with which
examples, use `lecture-builder` — run it first when the content is still open,
then bring its sections here.

---

## Step 0 — Read ABOUT ME first (mandatory)

Before asking anything, read **every file** in the ABOUT ME folder.

Search in order:
1. `~/.claude/ABOUT ME/`
2. `<project root>/ABOUT ME/`
3. Glob `**/ABOUT*ME*/` from the working directory

Pull out: default modality, typical class size, activities that work well,
**activities that fall flat**, tech actually available in the room, student
level and common gaps, and voice for the written-out transitions.

**If the folder is missing or empty:** say so plainly, ask for the path, and
stop. Never propose activities without knowing which ones fall flat with these
students — that is the fastest way to produce a plan that dies in the room.

---

## Step 1 — Intake

Ask for all six at once, numbered. **Skip anything already supplied.** Where
ABOUT ME answers one, propose that default and ask only to confirm.

1. **Course and topic** for this session
2. **Session length and class size**
3. **Modality** — in-person / online sync / hybrid
4. **The one thing students must leave understanding** — exactly one. If they
   give several, ask which survives if the session goes badly.
5. **What they were supposed to do before class** — and realistically, how many
   actually did it
6. **Materials and tech available**

That last part of #5 matters more than it looks. A plan built on completed
pre-work collapses when a third of the room did none. Ask for the honest number.

---

## Step 2 — Let class size and modality pick the activities

Do not choose activities before checking these. The same activity that works
with 18 students fails with 180.

| Class size | Works | Avoid |
|---|---|---|
| ≤ 20 | Full-group discussion, fishbowl, board work, cold-call with warmth | Anything needing anonymity to feel safe |
| 20-50 | Think-pair-share, small groups, gallery walk, polling | Full-group discussion — the quiet ones vanish |
| 50-150 | Polling, minute paper, structured pair work, worked-example pairs | Anything requiring the whole room to report back |
| 150+ | Polling, peer instruction, silent written response | Group formation, verbal reporting, movement |

| Modality | Mechanics | Watch for |
|---|---|---|
| In-person | Physical grouping, board, movement, paper | Back rows disengaging |
| Online sync | Breakouts, chat waterfall, shared doc, polls | Silent cameras-off; **always** give breakouts a written deliverable |
| Hybrid | Shared doc as the common surface | Remote students becoming spectators — pair them **with** in-room students, never against |

Then filter everything through the "activities that fall flat" list from
ABOUT ME. Those are veto entries, not suggestions.

**Minimum two active learning moments.** Active means students produce
something — spoken, written, or selected. Listening attentively does not count.
Space them so neither falls in the last five minutes.

---

## Step 3 — Budget the time, then check the arithmetic

```
Opening hook              3-5 min
Body                      <blocks of 8-15 min, each with a purpose>
Formative check           at the halfway mark, 5-8 min
Closing reflection        5-7 min
Buffer                    ~10%    ← the first thing beginners cut, and the
                                    reason plans fail
─────────────────────────────────
TOTAL                     must equal session length exactly
```

No single block runs past 15 minutes without a state change — a question, a
turn to a neighbour, a switch in medium.

---

## Step 4 — Output

```markdown
# <Topic> — <Course>
**Length:** <n> min · **Size:** <n> · **Modality:** <...>

## They must leave understanding
> <the one thing>

## Assumed pre-work
<what was assigned> — **planned for <n>% completion**
<the specific adjustment that keeps the session working if fewer did it>

---

## Materials and setup
- [ ] <item — with who brings it and when it is needed>
- [ ] <tech, with the fallback if it fails>

---

## Minute-by-minute

### 0:00-0:0X — Opening hook
**Activity:** <what happens>
**Purpose:** <creates the question the session answers — not a preview, not an
agenda slide. Students should feel a gap they want closed.>

> **Say:** "<written out, in the instructor's voice>"

### 0:0X-0:XX — <block name>
**Activity:** <...>
**Purpose:** <...>
**Instructor does:** <...>  ·  **Students do:** <...>

> **Transition:** "<written out verbatim — the exact sentence that moves the
> room from the last thing to this one>"

### <continue, every block, until the session ends>
```

Mark active learning blocks clearly: **🔵 ACTIVE LEARNING**

### Formative check at the halfway point

Must produce a signal the instructor can read **in the room, in under two
minutes**, and must include what to do with each outcome:

```markdown
### 0:XX-0:XX — Formative check  🔵
**Method:** <minute paper / poll / show of hands on a claim / one-sentence
summary on a shared doc>
**Reading the result:**
- Most got it → <what changes: go deeper, move faster>
- Split → <what changes: pair the confident with the unsure>
- Most missed it → <what changes: which planned block gets cut to re-teach>
```

A check with no branch is decoration. Always write all three branches.

### Closing reflection

```markdown
### 0:XX-<end> — Closing reflection
**Prompt:** <maps to the one thing they must leave understanding>
**Bridge to next session:** "<written out — plants the question the next
session opens with>"
```

### Backup move — if energy drops

```markdown
## ⚡ If energy drops
**Signs:** <what it actually looks like at this size and modality>
**Move:** <deployable in under 60 seconds, needs no new materials>
**Where it fits:** <which block to interrupt>
**What it costs:** <which block absorbs the lost minutes>
```

Make it concrete: "stand up, turn to the person behind you, one sentence each
on why the second method fails" — not "increase engagement".

---

## Quality checks before returning

- Does the timeline sum **exactly** to the session length?
- Is there a real buffer, or was it quietly spent?
- At least two active learning moments, neither stranded at the end?
- Is every transition written out as a sentence that could be said aloud?
- Does the formative check land at the halfway point, with all three branches?
- Does the hook create a question, or just announce the topic?
- Is the backup move deployable in under 60 seconds?
- Does every activity survive the class size, the modality, **and** the
  falls-flat list from ABOUT ME?
- Does the closing genuinely set up the next session?

---

## Related

- `lecture-builder` — content, examples, and slide outlines
- `revision-coach` — turning feedback into student action lists
