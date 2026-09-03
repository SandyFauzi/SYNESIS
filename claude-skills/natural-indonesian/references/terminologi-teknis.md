# Terminologi teknis yang natural dalam Bahasa Indonesia

Use this reference when writing about software engineering, AI, machine learning, data science, systems, tooling, or Claude Code.

## Why terminology drifts

Technical Indonesian commonly mixes Indonesian grammar with canonical English terminology. Literal translation can be grammatically valid yet pragmatically unnatural because practitioners do not use the translated form.

Treat practitioner usage as part of correctness. A term that is technically translatable but alien to the field lowers clarity.

## Decision rule

Choose terminology in this order:

1. Keep the canonical term if Indonesian practitioners commonly use it.
2. Use an Indonesian equivalent when it is established and immediately recognizable.
3. Introduce both once when the audience may need orientation: `confidence threshold (ambang kepercayaan)`.
4. Use a paraphrase when neither term alone is clear to a general audience.
5. Avoid literal calques that sound invented.

Do not switch among several equivalents merely for variety. Choose one form and keep it stable.

## Machine learning and AI

Prefer the following defaults unless the user's field has a different convention.

| Concept | Prefer | Avoid by default | Reason |
| --- | --- | --- | --- |
| Bag of Words | `Bag of Words (BoW)` | `kantong kata` | Canonical method name is clearer. |
| confusion matrix | `confusion matrix` | `matriks bingung` | Literal translation sounds nontechnical. |
| test set | `data uji`, `test set` | `himpunan uji` when prose is not mathematical | `data uji` is more natural in ML prose. |
| confidence threshold | `confidence threshold`, `ambang kepercayaan` | `ambang keyakinan` by default | Use field-natural phrasing. |
| expected cost | `expected cost`, `biaya ekspektasi` | `ongkos harapan` | Literal wording sounds unnatural. |
| misclassification cost | `biaya kesalahan klasifikasi` | `ongkos salah` | Prefer precise noun phrase. |
| rule-based | `rule-based`, `berbasis aturan`, `aturan manual` | `aturan tangan` | Avoid direct calque from hand-written rules. |
| guardrail | `guardrail`, `lapisan pengaman`, `mekanisme pengaman` | `pagar` | Preserve system-safety meaning. |
| model parameters | `parameter model` | `isi kepala model` | Use the actual concept. |
| feature vector | `vektor fitur` | invented metaphor | Established equivalent exists. |
| embedding | `embedding`, `vektor embedding` | forced literal translation | Canonical term is common. |
| logits | `logit` / `logit-logit` only if natural in a specific mathematical context | descriptive metaphor | Keep canonical term. |
| softmax | `softmax` | translated name | Proper technical name. |
| backpropagation | `backpropagation`, optionally `propagasi balik` when explaining | forced Indonesian-only form | Canonical form is widely understood. |
| gradient | `gradien` | translation paraphrase | Established Indonesian technical term. |
| loss | `loss`, `fungsi loss`, or `fungsi kerugian` only when the audience convention supports it | `kerugian` everywhere | Context decides. |
| intent | `intent` | `niat` in NLU/agent architecture | `niat` changes the technical register. |
| slot | `slot` | `celah` | Keep NLU term. |

## Software engineering

Keep canonical forms when they are standard in Indonesian engineering discourse:

`commit`, `branch`, `merge`, `pull request`, `repository`, `runtime`, `build`, `deploy`, `debug`, `framework`, `dependency`, `endpoint`, `request`, `response`, `cache`, `pipeline`, `rollback`, `retry`, `fallback`, `thread`, `worker`, `race condition`, `deadlock`, `event loop`, `middleware`, `scaffolding`, `boilerplate`, `throttling`, `debounce`.

Translate the surrounding explanation, not the token itself.

Prefer:

> Cache lama membuat build gagal ketika pipeline dijalankan ulang.

Avoid:

> Penyimpanan sementara lama membuat pembangunan gagal ketika jalur pipa dijalankan ulang.

## Cost, risk, and decision terminology

Prefer `biaya` over `ongkos` in technical, statistical, or decision-theoretic prose unless the domain itself conventionally uses `ongkos`.

Prefer:

- `biaya kesalahan`;
- `biaya salah klasifikasi`;
- `biaya ekspektasi`;
- `expected cost`;
- `fungsi biaya`;
- `matriks biaya`.

Avoid metaphorical or literal constructions such as `ongkos harapan`.

## Metaphor policy

Use metaphor only to explain after naming the real concept.

Good:

> Model ini memiliki 11.850 parameter. Jika ingin membayangkannya secara sederhana, parameter-parameter itu adalah angka yang dipelajari selama training.

Avoid:

> Otaknya hanya berisi sebelas ribu angka.

Good:

> Sebelum tool dipanggil, sistem masih menjalankan tiga lapisan pengaman.

Avoid:

> Sebelum alat dipanggil masih ada tiga pagar.

## Practitioner test

Before using an Indonesian equivalent, ask internally:

- Would an Indonesian engineer, researcher, or student in this field actually say this term in a technical discussion?
- Does the translation preserve the concept, or merely translate the English words?
- Would keeping the English term reduce ambiguity?
- Is the Indonesian alternative established enough that it sounds ordinary rather than invented?

If the answer is uncertain, keep the canonical term and explain it in Indonesian once.

## Consistency

After selecting a term, keep it stable. Do not alternate between `confusion matrix`, `matriks konfusi`, and `matriks kebingungan` merely to avoid repetition. Repetition of a precise technical term is preferable to terminological drift.
