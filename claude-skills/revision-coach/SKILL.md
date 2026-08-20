---
name: revision-coach
description: >
  Turns instructor feedback into a student-facing revision action list: top 3
  priorities ranked by impact on the next score, where in the artifact to fix
  each one, a pre-submission self-check, the proficiency standard, what is
  already strong, and an encouragement line in the instructor's voice. Use when
  the user says "revision coach", "turn my feedback into an action list", "make
  this feedback student-facing", "help this student revise", "resubmission
  guidance", or invokes /revision-coach. For grading feedback being handed back
  to a student, not for writing the feedback itself.
---

# Revision Coach

Convert instructor feedback into something a student can act on tonight.

The instructor already did the judging. This skill does **translation and
triage** — it never re-grades, softens, or invents new criticism.

---

## Step 0 — Read ABOUT ME first (mandatory)

Before asking anything, read **every file** in the ABOUT ME folder.

Search in order:
1. `~/.claude/ABOUT ME/`
2. `<project root>/ABOUT ME/`
3. Glob `**/ABOUT*ME*/` from the working directory

Pull out: voice and tone, banned phrases, student-facing language, the
proficiency standard, default reassessment policy, and typical student level.

**If the folder is missing or empty:** say so plainly, ask for the path, and
stop. Do not guess the instructor's tone, standards, or student population —
a fabricated encouragement line in the wrong voice is worse than none.

---

## Step 1 — Intake

Ask for all four at once, as a numbered list. **Skip any the user already
supplied in their invocation** — never re-ask for something already pasted.

1. **The feedback comment** — paste it verbatim, however rough.
2. **The rubric and the student's current scores** — criteria, point values,
   what they scored on each.
3. **The reassessment policy** — deadline, attempts allowed, how the new score
   is handled (replace / average / cap).
4. **The student's apparent skill level** — where they actually are, not where
   the course assumes they are.

If ABOUT ME already answers #3, propose it and ask only for confirmation.

Missing rubric scores is the one blocker: without them the ranking is
guesswork. Ask again. Everything else can proceed with a stated assumption.

---

## Step 2 — Rank by score impact

This is the core of the skill. Priorities are **not** ordered by how annoyed
the feedback sounds. Rank by points recoverable before the deadline:

For each distinct issue in the feedback:

1. Map it to the rubric criterion it lives under.
2. Compute the gap: `points available − points scored`.
3. Estimate how much of that gap is realistically closable, given the
   student's level and the time to deadline.
4. Score = closable points × likelihood of success.

Then apply the policy constraints:

- **One attempt only** → favour high-certainty fixes. Drop ambitious rewrites.
- **Multiple attempts** → a structural fix worth many points can outrank two
  safe cosmetic ones.
- **Tight deadline** → cut anything needing new research or data collection.
- **Score capped** → say so, and prioritise learning value once the cap is hit.

Keep exactly **three** priorities. If the feedback raises more, fold the small
ones into the self-check. If it raises fewer, say so rather than padding.

---

## Step 3 — Output

Student-facing document. Second person, addressed to the student.

### Hard rules

- **Only what the feedback and rubric support.** Never introduce a flaw the
  instructor did not raise.
- **Never soften or inflate.** If the work is below standard, the action list
  says what is missing without cushioning it into vagueness.
- **No instructor jargon** the student cannot parse, and no rubric-speak
  quoted without translation.
- **No comparison to other students**, no class statistics, no ranking.
- **Every priority must be doable** with what the student already has.
- Match the language and formality from ABOUT ME.

### Structure

```markdown
# Revision Plan — <assignment>

**Deadline:** <date>  ·  **Attempts left:** <n>  ·  **How the new score counts:** <...>

## What is already working — keep this
<2-4 specific things, quoted or located in the artifact. Concrete, never generic
praise. This is a preservation instruction: name what a careless rewrite would
destroy.>

## Priority 1 — <short label>  ·  worth ~<n> points
**What to do:** <one concrete action, imperative>
**Where:** <section, page, paragraph, line, slide — as specific as possible>
**Done when:** <observable success condition the student can check alone>

## Priority 2 — <...>
## Priority 3 — <...>

## Before you resubmit — self-check
- [ ] <checks tied directly to the three priorities>
- [ ] <plus the folded-in minor issues>
- [ ] <plus one check against the proficiency standard>

## The standard you are aiming for
<2-3 sentences, plain language, from ABOUT ME. What proficient looks like here —
not a restatement of the rubric table.>

---
<Encouragement line — one or two sentences, in the instructor's ABOUT ME voice.
Specific to this student's situation. Never generic, never hollow.>
```

---

## Quality checks before returning

- Do the three priorities actually track the biggest recoverable points?
- Could the student start Priority 1 in the next five minutes without asking
  a follow-up question?
- Is every "Where" specific enough to navigate to?
- Is every "Done when" checkable **without** the instructor?
- Does the encouragement line sound like this instructor, or like generic
  chatbot warmth? If the latter, rewrite it.
- Did anything get invented that the source feedback never said? Cut it.

---

## Related

- `lecture-builder` — content architecture for a session
- `lesson-plan-designer` — minute-by-minute session choreography
