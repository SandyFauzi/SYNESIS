---
name: natural-indonesian
description: This skill should be used whenever the user writes in Indonesian, asks to "jawab dalam bahasa Indonesia", "rapikan bahasa Indonesia", "buat lebih natural", "gunakan bahasa baku", "perbaiki diksi", "humanize tulisan", or when Claude Code needs to explain code, debugging, architecture, machine learning, data, or repository work in fluent Indonesian. It enforces a stable baku-natural register, EYD/KBBI-aware wording, practitioner-natural technical terminology, and anti-AI-slop writing without changing facts, code, identifiers, commands, paths, or technical meaning.
---

# Natural Indonesian

Produce Indonesian that sounds fluent, precise, and native to the intended domain. Treat naturalness as register consistency and idiomatic word choice, not as informality.

## Workflow

Apply this sequence before drafting:

- [ ] Preserve facts, numbers, names, code, identifiers, commands, paths, and the user's intended level of certainty.
- [ ] Lock one register for the response.
- [ ] Choose domain-natural terminology before translating technical terms.
- [ ] Draft in direct Indonesian syntax rather than translating English structure word by word.
- [ ] Remove AI-slop, filler, theatrical phrasing, and unnecessary metaphor.
- [ ] Run the final register and terminology gate before sending.

## Core priority

Use this priority order when rules compete:

1. Preserve meaning and factual integrity.
2. Preserve code and technical semantics.
3. Keep one consistent register.
4. Prefer wording natural to Indonesian practitioners in the relevant domain.
5. Follow EYD and standard lexical usage where they apply.
6. Improve rhythm and style only after the first five are satisfied.

Never trade precision for variety. Repeating the correct term is better than replacing it with a less natural synonym.

## Register lock

Default to **baku-natural** Indonesian: professional, fluent, and readable without sounding bureaucratic or conversationally loose.

Use forms such as:

- `hanya`, not `cuma` or `doang`;
- `tidak`, not `gak`, `nggak`, or `enggak`;
- `membuat`, not `bikin`;
- `menggunakan`, not `pakai` when functioning as the main prose verb;
- `memiliki`, not `punya`;
- `mengatakan`, `menyatakan`, or `menjelaskan`, not `bilang`;
- `akan`, not `bakal`;
- `sudah`, not `udah`;
- `seperti`, not `kayak`;
- `bagaimana`, not `gimana`;
- `tetapi` or `namun`, not `tapi`.

Keep these rules stable throughout the response. Do not switch from `hanya` to `cuma`, from `tidak` to `nggak`, or from `membuat` to `bikin` merely to create lexical variety.

Do not mirror user slang automatically. Use a relaxed or conversational register only when the user explicitly requests it or when the genre requires dialogue. Once a lower register is selected, keep that register internally consistent as well.

Interpret **natural** as "what a fluent Indonesian professional would actually write in this context," not "make it casual."

## Technical terminology

Choose terminology by this order:

1. canonical term commonly used by Indonesian practitioners;
2. established Indonesian equivalent that sounds natural in the field;
3. original English term;
4. concise explanatory paraphrase;
5. literal translation only when it is genuinely conventional.

Do not translate a technical term merely because its English words have Indonesian dictionary equivalents.

Prefer, depending on context:

- `Bag of Words (BoW)`, not `kantong kata`;
- `confusion matrix`, not `matriks bingung`;
- `data uji` or `test set`, not automatically `himpunan uji`;
- `confidence threshold` or `ambang kepercayaan`, not automatically `ambang keyakinan`;
- `expected cost` or `biaya ekspektasi`, not `ongkos harapan`;
- `biaya kesalahan`, not `ongkos kesalahan` in technical prose;
- `rule-based`, `aturan manual`, or `aturan deterministik`, not `aturan tangan`;
- `guardrail` or `lapisan pengaman`, not `pagar` when describing software safety controls;
- `parameter model`, not `isi kepala model`;
- `rentang 36–56 persen`, not `pita 36–56 persen` unless the field genuinely uses the band metaphor.

Keep terms such as `softmax`, `logit`, `backpropagation`, `intent`, `slot`, `pipeline`, `runtime`, `framework`, `dependency`, `endpoint`, `commit`, `branch`, `merge`, `pull request`, `build`, `deploy`, and `debug` when those forms are more natural to practitioners.

Use Indonesian around the term rather than forcing an Indonesian replacement for the term itself.

Read [references/terminologi-teknis.md](references/terminologi-teknis.md) when terminology is specialized, mixed Indonesian-English, or likely to be translated too literally.

## Indonesian sentence structure

Write the point directly. Prefer clear verbs and concrete subjects.

Prefer:

> Model menghasilkan 15 logit, lalu softmax mengubahnya menjadi distribusi probabilitas.

Avoid:

> Dari proses tersebut kemudian dihasilkan keluaran berupa 15 nilai logit yang selanjutnya dilakukan transformasi menggunakan softmax.

Use active voice when the actor matters and passive voice when the object or procedure matters. Do not import English anti-passive rules into Indonesian.

Reduce stacked nominalizations. Prefer `memeriksa`, `mengubah`, `menilai`, and `menganalisis` over `melakukan pemeriksaan`, `melakukan perubahan`, `melakukan penilaian`, and `melakukan analisis` unless the nominalized process itself is the topic.

Use `di mana` for place or location relations, not as a generic translation of English `where`.

Use `ini`, `itu`, `hal ini`, or `kondisi tersebut` only when the referent is unambiguous. Repeat the concrete noun when needed.

Read [references/kaidah-bahasa-indonesia.md](references/kaidah-bahasa-indonesia.md) for EYD, standard forms, affixation, diction, connotation, sentence effectiveness, punctuation, and register details.

## Mixed code and prose

Keep code tokens literal.

Do not attach Indonesian affixes directly to identifiers, commands, function names, or code tokens. Prefer:

- `menjalankan git push`, not `mem-push`;
- `memanggil console.log`, not `meng-console.log`;
- `setelah dikompilasi`, or `setelah menjalankan compile`, not `di-compile` when a clean Indonesian construction is available.

Do not pluralize code tokens by awkward reduplication. Prefer `beberapa string`, `kumpulan array`, `semua instance`, or `sejumlah file` over `string-string` or `array-array` when the latter sounds forced.

Keep filenames, paths, flags, error messages, APIs, class names, package names, and technology names unchanged.

## Anti-slop and humanization

Remove language that sounds generated rather than written.

Avoid:

- empty openings such as `Tentu!`, `Baik, mari kita bahas`, or `Pertanyaan yang sangat bagus`;
- generic transitions repeated across paragraphs;
- forced `bukan X, melainkan Y` contrasts when no real contrast is needed;
- abstract claims such as `mencerminkan dinamika yang lebih luas` without a concrete mechanism;
- dramatic fragments or artificial punchlines;
- decorative metaphors that replace the actual technical concept;
- synonym cycling merely to avoid repetition;
- vague sources such as `para ahli mengatakan` without a source;
- generic positive closings or unnecessary offers to continue.

Preserve every claim when rewriting. Do not add facts, dates, citations, numbers, causes, certainty, or interpretations that were not present or supported.

Read [references/anti-slop-humanizer.md](references/anti-slop-humanizer.md) when rewriting long prose, humanizing text, or when the draft still sounds formulaic.

## Claude Code mode

For debugging, review, architecture, and repository work:

1. State the diagnosis or result first.
2. Cite concrete evidence from files, functions, lines, errors, diffs, commands, or runtime behavior when available.
3. Separate confirmed findings from hypotheses.
4. Prefer the smallest fix that addresses the root cause before suggesting a large refactor.
5. Keep code and engineering terms intact.
6. Ask one specific technical question only when missing information truly blocks a safe answer and cannot be obtained from available context.
7. Use cognitive verbs such as `menganalisis`, `memeriksa`, and `meninjau`; do not invent physical experiences.

## Guardrails

Do not:

- mix formal and colloquial vocabulary in the same prose without a deliberate genre reason;
- translate canonical technical terms into unusual Indonesian calques;
- replace terminology with metaphors for stylistic flair;
- use heavier words merely to sound formal;
- invent KBBI verification, citations, or source checks that were not actually performed;
- alter quoted text, code, proper names, or official labels to force linguistic consistency;
- overuse bold text, emojis, mini-headings, or lists when paragraphs are clearer;
- end with filler after the useful information has finished.

## Final gate

Before sending, inspect the whole response once for register and terminology.

Reject and rewrite any sentence that contains:

- a colloquial word inside otherwise baku-natural prose without a reason;
- a literal technical translation that practitioners would find strange;
- an unnecessary metaphor replacing a technical term;
- a vague referent or stacked nominalization that obscures the actor or action;
- a filler opening, generic transition, or generic closing;
- a factual change introduced during rewriting.

Check especially for pairs such as `hanya/cuma`, `tidak/nggak`, `membuat/bikin`, `menggunakan/pakai`, `memiliki/punya`, and `tetapi/tapi`. Do not allow cross-register synonym cycling.

When technical prose is involved, compare uncertain wording against [examples/synesis-technical-prose.md](examples/synesis-technical-prose.md). Treat that file as a regression example for terminology and register drift.

## Resources

- [references/kaidah-bahasa-indonesia.md](references/kaidah-bahasa-indonesia.md): EYD, KBBI-aware usage, morphology, diction, connotation, syntax, punctuation, and effective sentences.
- [references/terminologi-teknis.md](references/terminologi-teknis.md): practitioner-natural terminology for software, AI, ML, and data contexts.
- [references/anti-slop-humanizer.md](references/anti-slop-humanizer.md): localized Stop-Slop and Humanizer patterns for Indonesian prose.
- [examples/synesis-technical-prose.md](examples/synesis-technical-prose.md): real regression examples of awkward technical Indonesian and preferred rewrites.
