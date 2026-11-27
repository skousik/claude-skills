# Citation Audit

A procedure for checking that every citation in a paper is correct, points at the specific result it relies on, and resolves to the right record. Run it before submission or posting, after large restructures, or whenever the user asks to check citations. It is slow; budget for reading sources, not only metadata.

## 1. Collect every citation with its sentence

Extract each `\cite` (with its optional pinpoint) and the full sentence around it, in document order, into one list keyed by bib entry. The unit of checking is the pair (sentence, cited work), not the bib entry: one work cited in three places makes three claims, and a multi-cite `\cite{a,b}` makes a claim for each key.

## 2. Check the metadata

For each bib entry, check that it resolves to the right record and that the record matches the entry:

- Resolve the DOI through Crossref (`https://api.crossref.org/works/<doi>`) and compare title, authors, venue, volume, number, pages, and year. For preprints, query the arXiv API; for old or non-DOI works, use zbMATH, NASA NTRS, or the publisher page.
- Crossref is a strong check but not ground truth. When it disagrees with the entry, check the publisher's page or the PDF before changing anything (a registry can have wrong page ranges or a variant title).
- Flag entries that cite a preprint when a published version exists, or the reverse, and say which version the pinpoints were checked in.

## 3. Get the source text

Read the cited work itself, not its title or abstract. Sources in order of preference: the project's reference PDFs, the publisher's open-access copy, arXiv, the author's homepage (often a free pre-publication draft of a book), the Wayback Machine for dead links, and Semantic Scholar for the open-access PDF link. Convert each PDF to text so it can be searched. Keep downloads in their own directory, apart from scripts.

If the original is paywalled and no copy is reachable, check the claim against a secondary source that states the result with its number (a survey or a later paper that restates it), and mark the citation as checked only secondarily.

## 4. Check each claim against the source

For each (sentence, work) pair:

1. **Find the passage.** Search the text for the terms the sentence attributes to the work, then read the surrounding statement. Do not stop at a hit in the introduction or related work of the cited paper; find where the result is stated.
2. **Use absence as evidence.** If a construction the sentence attributes to the work (a named object, a term, a method) never appears in its text, the attribution is wrong. A search for the term across the full text settles this quickly.
3. **Compare strength.** Check that the source says at least what the sentence says. Common gaps: the source gives orders of magnitude (`O(·)`) but the sentence claims explicit constants; the source covers a special case; the source proves one direction; the source's result is a different theorem with a similar name.
4. **Check the pinpoint.** Confirm the theorem, definition, section, or equation number in the copy you read, and that the numbered item is the one that states the result (not a lemma used in its proof, or a section that only mentions it). For a long work, point to the most specific unit that contains the statement, down to a paragraph locator when needed (`\cite[Sec.~2.2.1, after Prop.~2.3]{…}`).
5. **Check the framing.** When the sentence restates a result in the paper's own terms (for example "conditioning on an event" for what the source calls "subtractive contamination"), confirm the source defines its terms so the translation is faithful, and prefer the paper's term if it is the natural one in its setting.

## 5. Classify and fix

Classify each pair, and fix it as follows:

| Finding | Fix |
|---|---|
| Correct, no pinpoint, source is long | Add the pinpoint |
| Wrong pinpoint | Correct the number |
| Wrong source (the result is elsewhere) | Cite the work that contains it, with its pinpoint, and drop the wrong one |
| Multi-cite where each work supports a different part | Split the sentence so each part cites the work that supports it |
| Source says less than the sentence | Weaken the sentence to what the source says, and if the paper supplies the rest, say so ("we make explicit the constants in known bounds of order …") |
| The paper's own construction attributed to prior work | Claim it ("what we call the X") and cite what it follows ("following … \cite[Sec.~…]{…}") |
| Claim needs no citation (common knowledge, or argued in the paper) | Drop the citation |
| Unverifiable | Keep it, and report it to the user with the secondary source used |

Make each fix the smallest sentence change that makes the citation exact, and keep one sentence per source line.

## 6. Propagate

The same attribution often appears outside the manuscript. Search the project website, code docstrings and comments, slides, companion papers, and other versions of the manuscript (arXiv, journal, conference) for the same wording or citation key, and fix those too, or list them for the user if those files are outside the requested scope.

## 7. Report

Report every change with its location (file and passage, or a URL), the old and new wording, and a link to the source that supports the fix (DOI, arXiv, or the open copy read, with the page or section). List separately what could not be verified and why (paywalled original, only a draft edition available), so the user can check those against their own copies.

## Delegating

For a long bibliography, split the claim checks across parallel subagents, each given the sentences and the source PDFs or links for a few works. Ask each to find and quote the statement that supports each sentence, with its number and page, and to report when it cannot, rather than asking it to confirm the citation, since an agent asked to confirm tends to. Check any finding that changes a citation in the source yourself before editing.
