# Copy rules

Phase 2 artifact. Lists DESIGN.md, COMPONENTS.md, MOTION.md and COPY.md together;
the first three shipped and this one did not.

These are constraints, not style advice. Where a rule conflicts with what reads
better, follow the rule.

## Absolute

**Never an em dash or an en dash. Anywhere. Ever.** Rewrite with a period, a comma,
or two sentences. Grep before shipping copy:

    git grep -nP '[\x{2014}\x{2013}]' -- '*.html'

Never fabricate. A number, date, certification or capability that is not confirmed
does not ship. `{{NEEDS: ...}}` is the only permitted missing-fact convention. Square
bracket placeholders are banned in content files and `check-placeholders.sh` fails
the build on them.

## Banned words

    delve   leverage   seamless   robust   comprehensive
    world-class   best-in-class

They are filler, and on a contractor site filler reads as a company with nothing
specific to say.

## Sentence shape

Median sentence length 15 words. p90 under 50. Nothing over 140.

Short sentences are not a stylistic preference here. The reader is a project manager
or an estimator scanning on a phone between site visits, and long sentences are where
qualifications get lost.

Say what changed and why. Cut the preamble. A paragraph that opens by announcing
what the paragraph is about has wasted its first line.

## Claims

Every claim about ACG passes through the claims ledger. Three questions before any
number, credential or capability ships:

1. Is it true today, or was it true when someone wrote it?
2. Can a GC verify it in under a minute? If yes, assume they will.
3. Does it have an expiry? If yes, it belongs in `reverify.csv` with a date.

The site tells GCs to check whether a glazier's licence qualifier changed recently
and treat it as a yellow flag. Copy that invites verification has to survive it.

## Voice

Write the way the estimate reads. Specific, unhedged, and willing to state a
limitation. "We do not self-perform in that county" is stronger copy than a vague
claim of statewide coverage, because the first one is checkable and survives.

No exclamation marks. No rhetorical questions as headings. No emoji.
