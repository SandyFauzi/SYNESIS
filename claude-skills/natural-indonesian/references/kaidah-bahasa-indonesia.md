# Kaidah Bahasa Indonesia untuk prosa baku-natural

Use this reference when the task requires careful Indonesian spelling, morphology, diction, connotation, syntax, punctuation, or formal editing.

## Reference hierarchy

Apply sources by function:

1. Use EYD Edisi V for spelling, capitalization, word writing, borrowed elements, and punctuation.
2. Use KBBI knowledge for standard lemmas, word class, meaning, usage labels, and lexical status.
3. Use Indonesian grammar for phrase, clause, sentence, valency, and interclausal relations.
4. Use domain convention for established technical terminology.
5. Use genre and intended audience to choose the appropriate register.

Do not treat every dictionary entry as equally suitable for every register.

## Diction

Choose words by meaning, collocation, register, connotation, and pragmatic effect.

Distinguish strength of claim:

- `berkaitan` is not `menyebabkan`;
- `indikasi` is not `bukti`;
- `mungkin` is not `pasti`;
- `menyatakan` is more neutral than `mengklaim` in many contexts.

Prefer the least evaluative wording that still preserves the intended meaning.

## Verbs

Prefer direct verbs when possible:

- `menilai` rather than `melakukan penilaian terhadap`;
- `memeriksa` rather than `melakukan pemeriksaan terhadap`;
- `mengubah` rather than `melakukan perubahan terhadap`;
- `menganalisis` rather than `melakukan analisis terhadap`.

Use nominalization when the process itself is the subject of discussion.

## Active and passive voice

Use active voice when the actor or responsibility matters:

> Server menolak request karena token sudah kedaluwarsa.

Use passive voice when the object, result, or procedure matters:

> Token disimpan di environment variable.

Do not avoid `di-` merely because English style guides often prefer active voice.

## Affixes

Use established `meN-`, `di-`, `-kan`, and `-i` forms. Do not attach Indonesian affixes directly to code identifiers or commands.

Distinguish forms whose valency changes:

- `mengisi formulir`;
- `mengisikan data ke formulir`;
- `mengirimkan berkas kepada dosen`;
- `mengirimi dosen berkas`.

When a derived form feels doubtful, choose a clearer established construction rather than inventing a derivation.

## `di`, `ke`, and `dari`

Write prepositions separately when they indicate place, direction, or origin:

- `di rumah`;
- `di dalam sistem`;
- `ke kampus`;
- `dari Jakarta`.

Write prefixes together when they form words:

- `ditulis`;
- `diperiksa`;
- `dikirim`.

## `di mana`

Use `di mana` primarily for location. Do not use it as a generic relative-clause connector translated from English `where`.

Prefer:

> Sistem memakai cache yang menyimpan data selama lima menit.

Avoid:

> Sistem memakai cache, di mana data disimpan selama lima menit.

when no place relation is intended.

## Conjunctions

Match conjunctions to the real logical relation:

- cause: `karena`, `sebab`;
- result: `sehingga`, `akibatnya`;
- condition: `jika`, `apabila`;
- concession: `meskipun`, `walaupun`;
- contrast: `tetapi`, `namun`;
- addition: `dan`, `serta`;
- purpose: `agar`, `supaya`;
- time: `ketika`, `setelah`, `sebelum`.

Do not add conjunctions as decoration.

## Effective sentences

Ensure each sentence has a clear syntactic and logical center.

Check:

- subject and predicate clarity;
- parallel structure in coordinated elements;
- unambiguous pronoun and demonstrative references;
- modifier placement;
- economy without deleting necessary information;
- absence of stacked abstract nouns that hide the action.

Prefer:

> Tim menguji sistem untuk memastikan kestabilannya.

Avoid:

> Pelaksanaan proses pengujian dilakukan untuk melakukan verifikasi terhadap kestabilan sistem.

## Paragraphs

Use one paragraph for one coherent line of thought. Place the controlling point early, then provide explanation, evidence, exceptions, or consequences.

Do not force every sentence into a separate paragraph.

## Capitalization

Apply standard capitalization to sentence beginnings, proper names, institutions, geographic names, official titles when used as names, and other EYD-governed cases.

Do not capitalize common technical nouns merely for emphasis.

## Italics and foreign terms

Use italics according to the target medium and style convention, not as an automatic wrapper around every English technical word.

Do not italicize code, identifiers, commands, paths, package names, or names normally formatted as code.

## Punctuation

Use punctuation to clarify syntax rather than create dramatic rhythm.

Use commas for syntactically justified separation, not every spoken pause.

Use a colon after a complete clause that introduces a list, explanation, or quotation where appropriate.

Use semicolons only when they improve clarity between closely related independent structures.

Avoid em-dash-like rhetorical habits when a comma, colon, parenthesis, or new sentence is clearer. Use Indonesian punctuation conventions where a dash is genuinely required.

## Numbers and units

Keep numeric precision supplied by the source. Do not silently round or convert decimal conventions unless requested.

Use standard SI unit symbols where relevant. Preserve code or data formats when formatting is semantically significant.

## Standard and nonstandard forms

Default to standard forms in professional, academic, explanatory, and technical prose.

Use nonstandard forms only when the chosen register or quoted material requires them.

Maintain register consistency. A single colloquial synonym can make an otherwise formal paragraph feel unstable.

## Register consistency

Default to baku-natural prose.

Prefer:

- `hanya` over `cuma`;
- `tidak` over `nggak`;
- `membuat` over `bikin`;
- `menggunakan` over `pakai` as the main formal prose verb;
- `memiliki` over `punya`;
- `akan` over `bakal`;
- `sudah` over `udah`;
- `seperti` over `kayak`;
- `bagaimana` over `gimana`;
- `tetapi` or `namun` over `tapi`.

Do not change to a colloquial synonym simply to avoid repetition.

## Connotation

Treat synonyms as noninterchangeable when they carry different stance or intensity.

Examples:

- `keliru`, `salah`, and `menyesatkan` differ in severity;
- `menyatakan`, `menegaskan`, and `mengklaim` differ in stance;
- `keras kepala`, `teguh`, and `konsisten` differ in evaluation.

Choose the wording that adds the least unintended judgment.

## Final language check

Before sending carefully edited prose, verify:

- spelling and word separation;
- affixation;
- punctuation;
- clear referents;
- sentence economy;
- stable register;
- precise diction and connotation;
- technical terminology that follows domain convention rather than literal translation.

Do not claim to have consulted the live KBBI or EYD site unless an actual lookup was performed.
