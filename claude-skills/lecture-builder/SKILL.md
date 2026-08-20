---
name: lecture-builder
description: >
  Turns a topic into structured lecture notes or a slide outline: an opening
  hook tied to current real-world context, 3-5 main sections with key points,
  two examples and one analogy per section, discussion prompts every 10-15
  minutes, a closing synthesis question, optional speaker notes, and a ranked
  cut list for running short on time. Use when the user says "lecture builder",
  "build a lecture", "turn this topic into lecture notes", "make a slide
  outline", "structure this lecture", or invokes /lecture-builder.
---

# Lecture Builder

Turn a topic into teachable structure: what gets said, in what order, with what
examples, and what gets cut when the clock runs out.

This skill designs **content architecture**. For minute-by-minute choreography
of the room, use `lesson-plan-designer` instead — the two chain well.

---

## Step 0 — Read ABOUT ME first (mandatory)

Before asking anything, read **every file** in the ABOUT ME folder.

Search in order:
1. `~/.claude/ABOUT ME/`
2. `<project root>/ABOUT ME/`
3. Glob `**/ABOUT*ME*/` from the working directory

Pull out: subjects taught, student level and typical gaps, default pacing,
default visual style, favourite anchors and running examples, voice, and
activities that fall flat.

**If the folder is missing or empty:** say so plainly, ask for the path, and
stop. Do not invent the instructor's pacing, style, or student population.

---

## Step 1 — Intake

Ask for all six at once, numbered. **Skip anything already supplied.** Where
ABOUT ME already answers one, propose that default and ask only to confirm.

1. **Course, topic, and session length**
2. **Student level** — year, prior background, what they have already covered
3. **Three things they should walk out understanding** — the spine of the
   whole lecture; push for exactly three, phrased as claims not topics
4. **Current real-world contexts to anchor to** — what is live right now in
   the field, the news, or the students' own experience
5. **Pacing** — lots of stops for discussion / fewer stops / pure delivery
6. **Visual style** — text-heavy slides / image-led / minimal

Also ask, if not obvious: **notes or slide outline, or both?**

If the user gives more than three walk-out understandings, ask them to cut to
three. A lecture with six goals teaches none of them.

---

## Step 2 — Budget the time before writing anything

Do the arithmetic first and show it. Sections that overrun are the single most
common lecture failure.

```
Opening hook            5-8 min
Sections (3-5)          <remaining, distributed by weight>
Discussion stops        <count × 3-5 min each>
Closing synthesis       5-7 min
Buffer                  8-10% of session   ← never skip this
─────────────────────────────────────────
TOTAL                   must equal session length
```

Discussion stop count comes from the pacing answer:

| Pacing | Stops in a 90-min session | Interval |
|---|---|---|
| Lots of stops | 6-8 | every 10-12 min |
| Fewer stops | 3-4 | every 20-25 min |
| Pure delivery | 1-2 | midpoint and end only |

Even "pure delivery" keeps at least one — attention reliably decays past the
20-minute mark, and one prompt costs less than losing the room.

**Every section must serve at least one of the three walk-out understandings.**
If a section serves none, it is interesting material that belongs in a reading,
not in this lecture. Cut it and say why.

---

## Step 3 — Output

```markdown
# <Topic> — <Course>
**Length:** <n> min · **Level:** <...> · **Pacing:** <...> · **Visuals:** <...>

## They walk out understanding
1. <claim>
2. <claim>
3. <claim>

## Time budget
<the table — must sum to session length>

---

## Opening hook (<n> min)
<Tied to the current context they gave. A question, a tension, a surprising
number, a thing that just happened. It must set up a question the lecture
answers — not a summary of what is coming.>

**Transition into Section 1:** "<written out>"

---

## Section 1 — <title> (<n> min)
*Serves walk-out understanding #<n>*

**Key points**
- <...>

**Example A — <label>:** <concrete, worked>
**Example B — <label>:** <different in kind from A: different scale, domain,
or difficulty. Not a restatement.>

**Analogy:** <one, mapped explicitly — say what corresponds to what, and where
the analogy breaks down. An unbounded analogy creates misconceptions.>

**⏸ Discussion prompt (<n> min):** <a question with more than one defensible
answer. Not a comprehension check.>

**Transition:** "<written out>"

---

## Sections 2-5 — same structure

---

## Closing synthesis (<n> min)
**Question:** <requires combining at least two of the three walk-out
understandings. Not answerable from a single section.>

<How to land it, and what a good answer sounds like.>

---

## Cut list — if you are running short
Ranked, cut from the top:

1. **<item>** (saves ~<n> min) — <why this goes first, what is lost>
2. **<item>** (saves ~<n> min) — <...>
3. **<item>** (saves ~<n> min) — <...>

**Load-bearing — do not cut:** <the pieces the three understandings depend on.
If these go, the lecture stops working.>
```

### If a slide outline was requested

Add per slide: number, title, on-slide content matching the requested visual
style, and speaker notes.

Respect the visual style honestly:

| Style | On-slide | Notes carry |
|---|---|---|
| Text-heavy | Full phrases, structured bullets | Elaboration, examples |
| Image-led | One image + ≤6 words | Nearly all the content |
| Minimal | A word or a number | Everything |

Slide budget: roughly **one slide per 2-3 minutes**. Flag it if the count
drifts far from that.

---

## Quality checks before returning

- Does the time budget actually sum to the session length?
- Does every section serve a stated walk-out understanding?
- Are the two examples per section genuinely different in kind?
- Is every analogy bounded — is its breaking point stated?
- Are discussion prompts open questions, not quiz questions?
- Does the closing question need more than one section to answer?
- Does the cut list protect what the understandings depend on?
- Does the hook use the context they actually gave, or a generic stand-in?

---

## Related

- `lesson-plan-designer` — minute-by-minute session run
- `revision-coach` — turning feedback into student action lists
