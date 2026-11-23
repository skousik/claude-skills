# Tone profile: systems papers

Use this profile when the paper's argument rests on a working method, system, dataset, or study evaluated empirically (robot learning, VLA deployment, manipulation pipelines, teleoperation, planners judged by experiments).
The voice is modeled mainly on papers by Bajcsy, Bansal, Sinha, Xu, Shi, Garg, and Pavone, then pulled about a third of the way toward the ICRA 2024–26 award finalists.
The templates below are sentence *shapes*; do not reuse their wording verbatim.

## Targets

Rates are per 1,000 words of main-body prose, which is about one page of a two-column IEEE paper.
"Aim" is the typical value to write toward; "flag above/below" is where `scripts/tone_check.py --profile systems` raises a flag.

| Feature | Aim (per page) | Flag above / below |
|---|---|---|
| Mean sentence length | ~21 words | outside 18–25 |
| Sentences > 35 words | ~9% | outside 4–16% |
| Sentences < 12 words | ~17% | below 12% |
| Paragraph length | ~90 words (about 4 sentences) | outside 65–115 |
| "our" | ~3 | above 4.5 |
| "our approach/method/framework/system" | ~1 every 2 pages | above 1.0 |
| Passive constructions | ~1 per 6 sentences, where the agent is irrelevant | above 9.5 |
| Promotional words (novel, significantly, state-of-the-art, crucial, …) | ~1–2 | above 3.0 |
| "challenge(s)/challenging" | ≤ 1 every 2 pages | above 1.0 |
| "to address/tackle/overcome/bridge" | ~1 every 5 pages | above 0.35 |
| "In this paper/work" | ~1 every 3 pages | above 0.5 |
| "However" | ≤ 1, for genuine reversals | above 1.0 |
| "Moreover/Furthermore/Additionally" | ~1 every 2 pages | above 0.75 |
| Semicolons | ~1–2 | below 0.75 |
| Colons | only before displays, lists introduced by a full sentence, and caption panel labels; no mid-sentence elaboration colons | above 12 (mid-sentence colons are listed as hints) |
| Em-dashes | none | any |

The numbers are a sanity check after drafting, not a goal to optimize sentence by sentence.
A paper that passes every band can still read badly; one or two flags on a strong section are fine.

## Abstract

Write about 8 sentences and 180–200 words:

1. The capability the field now has.
2. The specific failure or brittleness that remains.
3. Why the obvious fix is inadequate.
4. *We introduce [name], which [mechanism].*
5. One or two sentences on how it works.
6. The assumptions or access model (what the method needs, what it does not).
7. The headline result, stated as a measurement, with at most one number.
8. *(Optional)* Link to the project page.

About a third of target abstracts include a number; when one appears, it is the main result, not a list of every metric.

## Introduction

Follow the shared arc in SKILL.md.
Systems-specific points:

- The opening can be a concrete deployment scenario the reader can picture, instead of a field-level claim.
- Paragraph 2 describes prior systems by what they assume access to (privileged state, demonstrations, a simulator, a fixed embodiment) and where that assumption breaks.
- No separate results-preview paragraph. The experiment contribution names the hardware or benchmark and gives at most one headline number; the rest of the numbers first appear in the experiments. Only a strongly results-driven systems paper carries more.

## Contributions

Use either a **Contributions.** (or **Statement of Contributions.**) paragraph with (i), (ii), (iii), or a list with an inline bold label and one sentence per item.

- The first item is often the **problem formulation**: *We formulate [deployment problem] as [scheduling / filtering / data-valuation] problem.*
  Treat the framing as a contribution when the framing is what makes the method possible.
- The middle items are the method and any released artifact (dataset, benchmark, code), stated by what each computes or enables.
- The last item is the **empirical finding**, with at most one headline number: *On [suite], [name] improves [metric] by X over [strongest baseline].*
- Study papers list **findings** instead ("Finding 1: …").

## Section architecture

- Headings may state findings when the section establishes one claim: "[Name] Matches Continuous Action Heads with Discrete Tokens", "Why Success Rate Misses [effect]".
  Keep plain headings ("Experimental Setup") for sections that only describe.
- Typical order: Introduction; Related Work; Problem Formulation; Method; Experiments (questions, then setup, then one subsection per question); Limitations; Conclusion.

## Experiments

- The opening paragraph lists the research questions (or hypotheses), and each maps to a subsection that answers it.
  Shape: *We evaluate [name] to answer: (Q1) [comparison with the strongest alternative]? (Q2) [does component X matter]? (Q3) [does it transfer to hardware / other policies]?*
  About 40% of target papers list questions or hypotheses explicitly, and the rest state the same goals in prose. Always use an explicit list here: research questions (Q1, Q2, …) or hypotheses (H1, H2, …).
- A setup paragraph covers the policy, hardware, tasks, data, metrics, and baselines.
  State deliberate choices with their reason: *We detune the nominal controller so that, without filtering, it [fails]; this isolates the filter's contribution.*
- **Results sentences: finding, then number, then reason.**
  Shape: *[Name] improves [metric] on three of four tasks and matches [baseline] on [task]; [baseline] fails on [case] because [mechanism].*
- Report where the method does not win in the same paragraph as where it does.
- Mark explanations as explanations: *We hypothesize that …*, *One explanation is …*, *The intuition is that …*.

## Limitations

Write 2–4 concrete items.
Each names a dependency or an untested regime, says where it matters, and says what would remove it.
Shape: *[Component] relies on [external module]; errors there lie outside [name], so a better [module] improves the system without changing the method.*
State scope plainly: *All experiments use a single embodiment.*
Do not end with a generic "future work will explore" line.

## Tone

Confident about what was measured, plain about what was not.
Mechanism-oriented: say why a design choice works (*This works because …*, *The intuition is that …*).
Prefer verbs of measurement ("improves X from A to B", "matches", "reduces") over adjectives ("impressive", "remarkable", "superior").
"Significantly" only with a reported significance test.

## Shape examples

These pairs show the move, not wording to reuse.

- Ownership → name.
  Before: *Our method achieves a higher success rate than the baselines.*
  After: *[Name] succeeds on 41 of 50 trials, against 29 for the strongest baseline, [baseline].*
- Challenge framing → the trade-off itself.
  Before: *Deploying large policies in real time is challenging. To address this challenge, we propose …*
  After: *A 7B-parameter policy runs at 3 Hz on the robot's GPU, which is too slow to react to contact; [name] runs the policy at 3 Hz and a 200 Hz residual controller between its outputs.*
- Results with the reason attached.
  Before: *Our approach outperforms all baselines. This shows the effectiveness of our method.*
  After: *[Name] outperforms all baselines on the cluttered tasks but matches [baseline] on the open-table task, where occlusion, the failure it targets, never occurs.*
