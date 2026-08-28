---
name: prd-jtbd
description: "Generate an implementation-ready Product Requirements Document using Jobs to Be Done, user stories, component inventory, data models, API specifications, state mapping, and testable acceptance criteria. Use for complex product or feature planning, AI prototyping briefs, design-heavy PRDs, or when asked for /prd-jtbd."
---

# PRD with JTBD

Create a concise but implementation-ready PRD for both cross-functional teams and AI coding or prototyping tools. Do not implement the feature while using this skill.

Adapted from `johnnychauvet/prd-skill`.

## Discovery

Use a feature or project name supplied by the user as the working title. Otherwise, ask what feature or project is being documented.

Ask these questions one at a time and incorporate any answers already present in the request:

1. What problem are we solving, and who is most affected?
2. Who are the primary and secondary users?
3. Is there a preferred tech stack, or should one be recommended?
4. What hard constraints apply, such as platform, authentication, offline support, compliance, or accessibility?

Ask only follow-ups that materially affect scope or architecture. Surface missing edge cases, error states, empty states, loading behavior, accessibility, and offline behavior where relevant.

## Writing principles

- Ground decisions in user impact and the reason behind the feature.
- Balance user needs, technical feasibility, and business goals.
- Prefer bullets and plain language over padded prose.
- Omit sections that genuinely do not apply.
- Make technical sections precise enough to serve as an AI build brief.
- Use binary, testable acceptance criteria; never use vague criteria such as "works correctly."

## PRD structure

Write the result to `tasks/prd-[feature-name].md` using a kebab-case feature name unless the user requests another destination.

### 1. Overview

Include:

- Feature or project name
- Problem statement in two to four sentences
- Proposed solution in one or two sentences
- AI build summary in imperative voice, stating what to build, the stack when known, and the hardest constraints

### 2. Goals and success metrics

Include one primary goal, one to three measurable success signals, and explicit anti-goals.

### 3. Scope and constraints

List in-scope and out-of-scope work. Record applicable platform, authentication, accessibility, offline, performance, data residency, and compliance constraints.

### 4. Jobs to Be Done

Provide two to five prioritized job statements:

> When [situation], I want to [motivation], so I can [expected outcome].

Assign stable IDs such as J1, J2, and J3.

### 5. User stories

For every story, include a stable ID, role, action, benefit, and JTBD reference. Use the form:

> As a [role], I want to [action], so that [benefit].

### 6. Proposed experience

Describe the design direction, interaction model, primary flow, and key screens. Include relevant empty, error, loading, undo, keyboard, screen-reader, and contrast behavior.

### 7. Component inventory

Enumerate every meaningful UI component. For each component, state its type, purpose, and linked user stories.

### 8. Data models

Define all data read or mutated by the feature. Prefer TypeScript interfaces when the stack uses TypeScript; otherwise use JSON Schema or clear field descriptions. Explain non-obvious fields and relationships.

### 9. API and integration surface

Enumerate required endpoints or external integrations. For endpoints, include method, path, purpose, authentication, request shape when relevant, response shape, and key failures. For a BaaS, describe table operations instead.

### 10. State management map

For each state value, specify its location, persistence, and rationale. Distinguish server state, local UI state, URL state, authentication context, and cache.

### 11. Tech stack recommendation

Respect the user's preferred stack. If none is given, recommend choices for frontend, styling, backend or BaaS, database, authentication, hosting, and key libraries with short rationales.

### 12. Suggested file structure

Provide a compact ASCII directory tree containing only new or materially changed files.

### 13. Acceptance criteria

Group checklist items by user-story ID. Make every item independently verifiable and include important edge cases and failure states.

### 14. Open questions and risks

List unresolved questions with owners, risks with mitigations, and material tradeoffs.

### 15. Rollout and next steps

Define the smallest shippable MVP, explicit exclusions, later-phase ideas, required sign-offs, and concrete next actions.

## Completion

After saving the PRD, report its path and offer to refine a specific section or adjust scope. Do not start implementation unless the user separately requests it.
