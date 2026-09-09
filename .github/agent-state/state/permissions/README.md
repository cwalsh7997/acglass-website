# Image permission requests

**Only one draft is still needed.** The manufacturer half resolved without an email.

## Resolved 2026-09-09

Connor confirmed ACG holds **signed dealer/installer agreements with both Euro-Wall
and ES Windows**. Those agreements carry marketing and trademark use terms, which is
exactly the written licence D10 obligation 4 asks for. All 17 manufacturer images
are now `licensed_written` against the agreement rather than waiting on a reply.

Drafts 1 and 2 were deleted. Asking a manufacturer for permission you already hold
in a signed contract wastes their time and yours.

Two images were also swapped out entirely rather than licensed:

| was | now |
|---|---|
| `partners/eurowall/project-allen-residence` | `atlantic-fields-golf-house/sliding-doors` |
| `partners/eurowall/project-hero-multislide` | `atlantic-fields-golf-house/hero-open-wall` |

Both were photographs of other companies' jobs illustrating ACG's pages. Connor
confirmed Atlantic Fields used Euro-Wall, so ACG's own photography of its own
installed work replaces them. The caption changed from "Euro-Wall Vista Fold ·
Allen Residence" to "Euro-Wall · Atlantic Fields Golf House", which is accurate and
does not assert a specific model.

## Still open: 5 GC logos

`3-gc-logos.txt`. Curran Young, Hooks, Made in Rio, Proctor, Rycon.

A subcontract does not normally grant a subcontractor the right to display the GC's
mark, so unlike the manufacturers there is probably no existing document covering
this. The draft asks for a reply on file and explicitly offers them the option to
say no, which is what makes a yes worth having.

When a reply lands, set `rights_status` to `licensed_written` on that row with the
date and sender in `evidence_ref`.
