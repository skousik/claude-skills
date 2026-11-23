# Revision examples

Illustrative before/after rewrites. The specific content comes from a robot motion-planning paper; the patterns apply to any technical manuscript.

## Replace vague value claims with the concrete property

**Before:** "The trajectory has a useful structure."
**After:** "The terminal configuration is affine in the initial state and plan parameter, so a local target certificate can retain all 21 variables."

Why: the rewrite names the property (affine), the object it holds for, and the consequence it enables. "Useful" tells the reader nothing they can check.

## Replace announcements with the content they announce

**Before:** "Three parts make the result useful."
**After:** Name the terminal and collision certificates, then state the inclusion that follows from their conjunction.

Why: a sentence that counts or praises parts is a placeholder. Say what the parts are and what they jointly give.

## State what is true, not what is absent

**Before:** "No interpolation of the error itself is used."
**After:** "The same box contains every admissible error at every time in the interval, including discontinuous errors."

Why: a negative statement leaves the reader guessing what is done instead. The positive statement gives the actual guarantee and its scope.

## Motivate a definition before displaying it

**Before:** Display the error-bound set $E$, then explain it.
**After:** "Because affine velocity reaches its largest absolute value at an interval endpoint, we bound the error using only the endpoint velocities:" followed by the definition of $E$, then one sentence on what $E$ lets the next step do.

## Topic sentences carry the paragraph

**Before:** "In this section, we consider several aspects of the problem. First, ..."
**After:** "The collision constraint must hold over the whole motion, not only at the terminal time, so we bound occupancy on each time interval separately."

Why: the reader skimming first sentences learns the actual point; "we consider several aspects" teaches nothing.

## Keep the claim as strong as the evidence

**Before:** "Our method finds optimal plans in 12 ms."
**After:** "Feasible-plan search returned a plan in 12 ms on average over 500 queries (per-query mean); we do not evaluate plan cost."

Why: the experiment measured feasibility and time, not optimality, and the denominator and averaging are stated.
