# Tone profile: theory papers

Use this profile when the paper's argument rests on a formulation, guarantee, or analysis, and the experiments validate it (safety filters, reachability, game-theoretic planning, certificates, identifiability, convergence).
The voice is modeled mainly on papers by Fisac, Fridovich-Keil, Bansal, and Pavone, then pulled about a third of the way toward the ICRA 2024–26 award finalists.
The templates below are sentence *shapes*; do not reuse their wording verbatim.

## Targets

Rates are per 1,000 words of main-body prose, which is about one page of a two-column IEEE paper.
"Aim" is the typical value to write toward; "flag above/below" is where `scripts/tone_check.py --profile theory` raises a flag.

| Feature | Aim (per page) | Flag above / below |
|---|---|---|
| Mean sentence length | ~20 words | outside 18–25 |
| Sentences > 35 words | ~9% | outside 4–16% |
| Sentences < 12 words | ~20% | below 15% |
| Paragraph length | ~85 words (about 4 sentences) | outside 60–115 |
| "our" | ~2 | above 4 |
| "our approach/method/framework" | almost never | above 0.5 |
| Passive constructions | ~1 per 5 sentences, where the agent is irrelevant | above 12.5 |
| Promotional words (novel, significantly, state-of-the-art, crucial, …) | ~1 | above 1.5 |
| "challenge(s)/challenging" | ~1 every 3 pages | above 0.75 |
| "to address/tackle/overcome/bridge" | rarely | above 0.25 |
| "In this paper/work" | ~1 every 3 pages | above 0.6 |
| "However" | ≤ 1, for genuine reversals | above 1.0 |
| "Moreover/Furthermore/Additionally" | ≤ 1 every 2 pages | above 0.9 |
| Semicolons | ~2 | below 0.5 |
| Colons | only before displays, lists introduced by a full sentence, and caption panel labels; no mid-sentence elaboration colons | above 12 (mid-sentence colons are listed as hints) |
| Em-dashes | none | any |
| Theorem-like environments in the main text | ~4–5 | not flagged |
| Displayed equations in the main text | ~15 | not flagged |

The numbers are a sanity check after drafting, not a goal to optimize sentence by sentence.
A paper that passes every band can still read badly; one or two flags on a strong section are fine.

## Abstract

Write about 6–8 sentences and 160–210 words, with no hedges and no experimental numbers (numbers first appear in the experiments):

1. The setting.
2. What existing approaches cannot certify, decide, or compute.
3. One sentence per main result in plain language: *We characterize / prove / derive / bound …*
4. One sentence on validation (systems, scale, hardware).
5. *(Optional)* The practical consequence of the result.

Use verbs that name the result type: *characterize, prove, derive, bound, show that … is identifiable / invariant / convergent.*
Do not "propose" a theorem.

## Introduction

Follow the shared arc in SKILL.md.
Theory-specific points:

- Paragraph 2 says what prior methods *guarantee* and under which assumption, then what they leave uncertified.
  Shape: *[Prior methods] guarantee [X] when [assumption], but they do not [Y].*
- The question paragraph names the formal object the paper resolves: an existence question, a characterization, a bound.
- The results preview states the guarantees in words, not experimental percentages.
- Optional **Outline.** and **Notation.** paragraphs close the introduction, each led by an inline bold label.

## Contributions

List results, not artifacts, about three of them (see *Contributions* in SKILL.md for the count and when to cite sections). In a short paper, point each one to the section or theorem that establishes it.
Either form is fine:

- Labeled items: **Error bound:** *[what is bounded] for [class], via [technique] (\Cref{thm: …}).*
  **Guarantee:** *[property] for [system], at [cost].*
  **Validation:** *[systems tested]; [the comparison against baselines, in words].*
- "Our main results are as follows," followed by numbered results, each one or two sentences on what is characterized and under which condition.

## Section architecture

- Headings name the result or the object, not the paper's role.
  Prefer "Identifiability from Observations" or "Coupled Reduction-Error Certificates" over "Method" or "Proposed Approach".
- Typical order: Introduction; Related Work (or Preliminaries and Related Work); Problem Formulation; one section per result; Algorithm or Implementation; Experiments; Limitations; Conclusion.

## Around each theorem

- **Before the statement,** write one sentence on what is about to be established and why the next step needs it.
  Shape: *We first characterize [set] on which [property] holds, and then bound [error] outside it.*
- **After the proof,** add one of: a remark interpreting the result, a corollary that specializes it, or a short practical note on how its constants are obtained (e.g. a paragraph led by **Offline construction.**).
- **After a group of results,** close with one sentence on what they establish together: *Together, these results certify [guarantee] whenever [condition].*
- Keep logical connectives that carry inference ("thus", "therefore", "hence", "in particular"); they are the most common transitions in the target papers, about twice as frequent as in systems papers.

## Experiments

- Open by stating what the experiments test about the theory as an explicit list of research questions (Q1, Q2, …) or hypotheses (H1, H2, …): does the guarantee hold in practice, how conservative is the bound, and what happens when an assumption fails.
- Include at least one setting where every assumption holds, and say so.
  Include at least one where an assumption is violated, and report what happens.
- Name each baseline by what it guarantees: *[Baseline] is complete but scales exponentially in [dimension]; [ours] trades completeness for …*

## Tone

Declarative and precise, with modest framing.
State novelty explicitly: *To the best of our knowledge, this is the first work to [result]*, or *[X] is the only [class] that [property]*, in the method-summary paragraph before the contributions, with the supporting comparison at the end of each Related Work subsection (see *Novelty claims* in SKILL.md).
"Foundational" is the ceiling of assertiveness in the target papers; use it only for a result that is clearly new.

## Shape examples

These pairs show the move, not wording to reuse.

- Ownership → object.
  Before: *Our method guarantees that the system remains safe.*
  After: *The filter keeps the state inside the viability kernel for all admissible disturbances (\Cref{thm: invariance}).*
- Stock challenge framing → mechanism.
  Before: *However, computing the safe set is challenging in high dimensions. To address this challenge, we propose …*
  After: *Exact reachability scales exponentially in the state dimension; we instead certify a learned value function on the region the filter actually visits.*
- Two sentences joined by their logic.
  Before: *The bound holds when the model is exact. When the model has error, the bound is conservative.*
  After: *With an exact model the bound is tight; with model error, it is conservative by at most [term].*
