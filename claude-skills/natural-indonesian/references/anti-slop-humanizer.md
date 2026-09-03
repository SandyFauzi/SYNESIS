# Anti-slop dan humanisasi untuk Bahasa Indonesia

Use this reference when rewriting long prose, editing AI-sounding text, or when a draft is grammatically correct but still feels generated.

This guide adapts the useful principles of Stop-Slop and Humanizer to Indonesian. Do not copy English-specific rules mechanically.

## Preserve meaning first

Keep every factual claim, name, number, date, quote, citation, ranking, code token, and level of certainty unless the user asks to change the content.

Do not invent facts to make prose feel more human.

## Remove empty openings

Delete openings that merely announce the answer:

- `Tentu!`;
- `Baik, mari kita bahas`;
- `Pertanyaan yang sangat bagus`;
- `Mari kita selami`;
- `Perlu diketahui bahwa`;
- `Penting untuk dicatat bahwa`.

Start with the answer or the first useful fact.

## Remove formulaic transitions

Do not open paragraph after paragraph with `Selain itu`, `Lebih lanjut`, `Di sisi lain`, `Dalam konteks ini`, or `Oleh karena itu` unless the logical relation truly needs to be named.

Let paragraph order carry the transition when possible.

## Avoid inflated abstraction

Prefer concrete mechanisms over phrases such as:

- `mencerminkan dinamika yang lebih luas`;
- `menyoroti pentingnya`;
- `menggarisbawahi peran krusial`;
- `dalam lanskap yang terus berkembang`;
- `mendorong sinergi`;
- `menghadirkan solusi komprehensif`.

Replace them with the actual effect, evidence, or mechanism.

## Avoid forced contrasts

Do not overuse patterns such as:

> Bukan hanya X, tetapi juga Y.

> Ini bukan sekadar X, melainkan Y.

Use a contrast only when the distinction matters logically.

## Avoid forced groups of three

Do not package every point into three items for rhetorical symmetry. Let the number of items follow the content.

## Avoid dramatic fragments

Do not create artificial rhythm with repeated short fragments:

> Tidak ada fallback. Tidak ada retry. Tidak ada jalan kembali.

Prefer a complete statement:

> Implementasi ini tidak memiliki fallback atau retry, sehingga kegagalan request langsung menghentikan proses.

## Avoid decorative metaphor

Do not replace technical concepts with anthropomorphic or cinematic language.

Avoid:

- `otak model` when `parameter model` is intended;
- `tiga pagar` when `tiga lapisan pengaman` is intended;
- `pita akurasi` when `rentang akurasi` is intended;
- `mesin mengingat siapa berasal dari siapa` when `graf mencatat dependensi operasi` is more precise.

Metaphor is allowed after the technical concept has been named and only when it genuinely helps explanation.

## Avoid synonym cycling

Do not rename the same concept simply to avoid repetition.

Keep `cache` as `cache` rather than cycling through `penyimpanan sementara`, `lapisan simpan`, and `mekanisme simpan`.

Keep the selected register as well. Do not cycle `hanya` into `cuma`, `tidak` into `nggak`, or `membuat` into `bikin`.

## Prefer simple verbs

Prefer:

- `menilai` over `melakukan penilaian terhadap`;
- `memeriksa` over `melakukan pemeriksaan terhadap`;
- `mengubah` over `melakukan perubahan terhadap`;
- `menganalisis` over `melakukan analisis terhadap` when the process itself is not the topic.

Do not make every sentence formal by increasing noun density.

## Avoid vague attribution

Do not write `para ahli mengatakan`, `banyak penelitian menunjukkan`, or `sejumlah sumber menyebutkan` without a source.

Name the source if available. Otherwise state only what the evidence actually supports.

## Avoid generic endings

Do not end with:

- `Semoga membantu`;
- `Pada akhirnya semuanya kembali pada kebutuhan Anda`;
- `Dengan pendekatan yang tepat, hasil optimal dapat dicapai`;
- `Masa depan terlihat menjanjikan`.

End on the final useful fact, decision, or next action.

## Rhythm

Vary sentence length naturally. Use short sentences for decisions or clear findings, and longer sentences for relationships that benefit from being kept together.

Do not manufacture rhythm through fragments, rhetorical questions, or repeated sentence templates.

## Final humanization check

Ask internally:

1. Does any sentence sound translated from English?
2. Does any sentence use a word merely because it sounds more sophisticated?
3. Did any synonym change the register or technical meaning?
4. Did any metaphor replace the real concept?
5. Did the rewrite add or remove a factual claim?

Rewrite the paragraph, not just the flagged word, when the surrounding structure is the actual problem.
