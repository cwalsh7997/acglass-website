# Image permission requests

**None outstanding.** Every draft was deleted unsent, because the permissions
already existed in documents ACG had signed.

## What actually resolved this, 2026-09-09

| images | covered by |
|---:|---|
| 17 | signed dealer/installer agreements with Euro-Wall and ES Windows |
| 5 | publicity/marketing clauses in the executed GC subcontracts |
| 2 | swapped for ACG's own Atlantic Fields photography, so no permission needed |

I had written three emails asking seven companies for permission ACG already held
in contract. Asking one question first, "do you have a signed agreement", made all
three unnecessary and saved sending letters that would have read as though ACG did
not know what it had signed.

The lesson worth keeping: the blocker was never the permission. It was that nobody
had written down where the permission lived.

## If this comes back

`image-rights.csv` now carries the evidence reference on every row. If a dealer
agreement lapses or a GC relationship ends, set that row back to `unverified` and
`check-image-rights.sh` will block publication under D10 obligation 4 again.
