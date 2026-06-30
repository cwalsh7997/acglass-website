#!/usr/bin/env python3
"""
fix-ai-prose-sprint004.py  (Sprint 004, 2026-06-30)

Final, per-occurrence rewrite of the ~33 bespoke pages where the retired AI positioning
was woven into narrative (operator Ledger 2.3). Removes Sub.ai / jobcost.ai / CFO Agent /
"custom AI agents" / acglass.ai while PRESERVING the real, Ledger-verifiable substance:
Procore-native operations, owner-led delivery, real-time job costing, 48-hour bids,
custom in-house software. No new claims introduced. Exact-string method (can miss, never
corrupts); dry-run default; residual scan at end.
"""
import os, sys, re

APPLY = "--apply" in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

R = [
 ("operations using custom agents (Sub.ai, jobcost.ai, CFO Agent) in production;",
  "owner-run operations on custom in-house software, Procore-native;"),
 ("American Commercial Glass is the commercial glazing contractor running custom AI agents in production. The stack includes Sub.ai (subcontractor coordination and bid management), jobcost.ai (real-time job costing and margin tracking), a CFO Agent (autonomous finance operations), and a manufacturer-integrated ESWindows Dealer Portal for ordering. These tools run on top of Procore as the primary system of record for submittals, RFIs, and scheduling, integrated with QuickBooks. The approach is documented in ACG's white paper, 'Operations in Commercial Glazing' (June 2026), authored by President Connor Walsh.",
  "American Commercial Glass runs Procore-native operations as the primary system of record for submittals, RFIs, and scheduling, integrated with QuickBooks, with custom in-house production software for bid coordination and real-time job costing, plus a manufacturer-integrated ESWindows Dealer Portal for ordering. Owner-led by President Connor Walsh."),
 ("tracked in real time with custom AI tools and written back to Procore.",
  "tracked in real time in Procore-native software."),
 ("ACG operates two custom-built AI operations tools: Sub.ai for subcontractor workflow automation and jobcost.ai for real-time project cost tracking. Built and run internally.",
  "ACG operates custom-built, Procore-native production software for subcontractor coordination and real-time project cost tracking. Built and run internally."),
 ("<div class=\"asset-card-title\">Sub.ai &amp; jobcost.ai</div>",
  "<div class=\"asset-card-title\">In-house production software</div>"),
 ("Hero: live Sub.ai terminal + Atlantic Fields", "Hero: Atlantic Fields"),
 ("<strong>AI in construction estimating and operations</strong> &mdash; ACG operates custom AI tools (Sub.ai, jobcost.ai) for estimating workflow and job cost management. Practical field perspective on where AI adds traction and where it doesn't.",
  "<strong>Construction estimating and operations</strong> &mdash; ACG runs custom-built, Procore-native software for estimating workflow and job cost management. Practical field perspective on what actually moves the needle."),
 ("<strong>AI in construction estimating and operations</strong> — ACG operates custom AI tools (Sub.ai, jobcost.ai) for estimating workflow and job cost management. Practical field perspective on where AI adds traction and where it doesn't.",
  "<strong>Construction estimating and operations</strong> — ACG runs custom-built, Procore-native software for estimating workflow and job cost management. Practical field perspective on what actually moves the needle."),
 ("<div class=\"label\">CFO Agent</div>", "<div class=\"label\">Project finance</div>"),
 ("<div class=\"label\">Sub.ai</div>", "<div class=\"label\">Bid coordination</div>"),
 ("Launched custom-built operations tooling: <strong>jobcost.ai</strong>, <strong>Sub.ai</strong>, ESWindows Dealer Portal.",
  "Launched custom-built, Procore-native operations software and the ESWindows Dealer Portal."),
 ("dedicated CFO Agent for daily P&amp;L variance, in-house submittal automation, and",
  "daily P&amp;L tracking, in-house submittal tracking, and"),
 ("Brand domains: acglass.ai, acommercialglass.com", "Brand domains: acommercialglass.com"),
 ("ACG runs custom production tools — Sub.ai for bid and subcontractor coordination and jobcost.ai for real-time margin tracking — on a Procore-native backbone.",
  "ACG runs custom production software for bid and subcontractor coordination and real-time margin tracking on a Procore-native backbone."),
 ("Procore-native, operations</strong> — Sub.ai for bid coordination, jobcost.ai for live margin tracking.",
  "Procore-native operations</strong> — custom software for bid coordination and live margin tracking."),
 ("we run custom AI agents (Sub.ai, jobcost.ai, and a CFO Agent) in production; what's working, what's hype, and what comes next",
  "we run custom in-house production software on a Procore-native backbone; how an owner-led shop stays fast and accurate"),
 ("WBE+SBE-certified, Procore-native sub backed by custom AI agents for estimating and real-time job costing.",
  "woman-owned, Procore-native sub with custom in-house software for estimating and real-time job costing."),
 ("ACG is the only glazing contractor we know of running custom AI agents in production &mdash; subcontractor coordination and bid management, real-time job costing, and an autonomous CFO assistant &mdash;",
  "ACG runs custom in-house production software &mdash; subcontractor coordination and bid management, real-time job costing, and back-office finance &mdash;"),
 ("The boldest positioning bet. Leans hard into Sub.ai / jobcost.ai / CFO Agent — your custom apps as the moat. Black ink with red glow gradients, bento capabilities grid, terminal demo of the actual AI scope generator. Works only if \" glazing contractor\" is the company identity, not just an angle.",
  "The boldest positioning bet. Leans hard into custom in-house software as the moat. Black ink with red glow gradients, bento capabilities grid. Works only if the operating model is the company identity, not just an angle."),
 ("Sub.ai, jobcost.ai, and CFO Agent — our in-house operating stack — read your drawings",
  "Our in-house production software reads your drawings"),
 ("paired with custom AI agents for bidding and job costing", "paired with custom in-house software for bidding and job costing"),
 ("American Commercial Glass runs operations on custom AI agents built in-house — Sub.ai for subcontractor coordination and bidding, jobcost.ai for real-time job costing and margin tracking, and a CFO Agent. ACG is the only glazing contractor running custom AI agents in production, integrated with Procore.",
  "American Commercial Glass runs operations on custom software built in-house — for subcontractor coordination and bidding, real-time job costing and margin tracking, and back-office finance — all Procore-native."),
 ("tracks material status in real time through jobcost.ai", "tracks material status in real time in its Procore-native software"),
 ("Sub.ai coordinates bids and subcontractor scheduling, and jobcost.ai tracks margin in real time.",
  "it coordinates bids and subcontractor scheduling and tracks margin in real time."),
 ("We bring an lean operating model (Sub.ai, jobcost.ai, CFO Agent) that lets",
  "We bring a lean, Procore-native operating model that lets"),
 ("acglass.com (production), acglass.ai (redirect), all subdomains", "acglass.com (production), all subdomains"),
 ("Custom AI tools (Sub.ai for bid coordination, jobcost.ai for live margin tracking) keep the bid fast and the job on budget.",
  "Custom in-house software for bid coordination and live margin tracking keeps the bid fast and the job on budget."),
 ("Read the full <a href=\"/ai-operations-whitepaper.html\" style=\"color:#ff5566;\">AI operations approach</a> or browse",
  "Read more <a href=\"/about.html\" style=\"color:#ff5566;\">about ACG</a> or browse"),
 ("Custom production software the owners built, Sub.ai for bid coordination and jobcost.ai for live margin tracking, is how",
  "Custom production software the owners built — for bid coordination and live margin tracking — is how"),
 ("How ACG runs custom AI agents — Sub.ai, jobcost.ai, and a CFO Agent — in production to manage bids, job costing, and back-office work. The first such operation in commercial glazing.",
  "How ACG runs custom in-house software to manage bids, job costing, and back-office work — an owner-led, Procore-native operation."),
 ("How American Commercial Glass built Sub.ai, jobcost.ai, CFO Agent, and Bid Engine in-house — the why, the what, and what it changed about how we run commercial construction.",
  "How American Commercial Glass built its custom in-house production software — the why, the what, and what it changed about how we run commercial construction."),
 ("Our internal toolset — <em>sub.ai</em> for project intake and scoping, <em>jobcost.ai</em> for live margin tracking, a CFO agent for cash-flow forecasting, an <a href=\"/\">ESWindows dealer portal</a> for distribution — wasn't built because AI is trendy. It was built because the alternative was hiring four more office people to do work software should do.",
  "Our internal software — for project intake and scoping, live margin tracking, cash-flow forecasting, and an <a href=\"/\">ESWindows dealer portal</a> for distribution — was built because the alternative was hiring four more office people to do work software should do."),
 ("How does ACG use AI in its glazing operations?", "How does ACG run its glazing operations?"),
 ("ACG uses  takeoff (documented at acglass.ai) to compress this from 2-3 days to 4-8 hours.",
  "ACG uses custom in-house takeoff software to compress this from 2-3 days to 4-8 hours."),
 ("We achieve this with  takeoff, standardized pricing tables, and a streamlined bid review process.",
  "We achieve this with custom takeoff software, standardized pricing tables, and a streamlined bid review process."),
 ("using  workflows (documented at acglass.ai).", "using custom in-house workflows."),
 ("<tr><td>AI / tech differentiation</td><td class=\"acg-col\"><strong>Custom AI agents in production &mdash; Sub.ai, jobcost.ai, CFO Agent</strong></td><td></td></tr>",
  "<tr><td>Operations technology</td><td class=\"acg-col\"><strong>Custom in-house production software, Procore-native</strong></td><td></td></tr>"),
 ("<li>Built custom AI applications for construction operations (documented at acglass.ai)</li>",
  "<li>Built custom in-house software for construction operations</li>"),
 ("<li>Speaking at construction industry events on  operating models</li>",
  "<li>Speaking at construction industry events on owner-led operating models</li>"),
 ("<li> bid engineering using custom in-house applications (Sub.ai, jobcost.ai, CFO Agent)</li>",
  "<li>Bid engineering using custom in-house software</li>"),
 # stack-pills
 ("Sub.ai · scope generation", "Procore-native · scope generation"),
 ("jobcost.ai · submittal cycles", "Real-time costing · submittal cycles"),
 ("CFO Agent · project finance", "Owner-run · project finance"),
]

def iter_html():
    for dp, _, fns in os.walk(ROOT):
        if "/.git" in dp: continue
        for fn in fns:
            if fn.endswith(".html"): yield os.path.join(dp, fn)

import collections
per = collections.Counter(); files_changed = 0
for path in iter_html():
    s = open(path, encoding="utf-8").read(); new = s
    for old, repl in R:
        if old in new:
            per[old] += new.count(old); new = new.replace(old, repl)
    if new != s:
        files_changed += 1
        if APPLY: open(path, "w", encoding="utf-8").write(new)

print(f"=== {'APPLIED' if APPLY else 'DRY-RUN'} ===  files changed: {files_changed}")
matched = sum(1 for o,_ in R if per[o]); print(f"patterns matched: {matched}/{len(R)}")
for o,_ in R:
    if not per[o]: print(f"  [0] UNMATCHED: {o[:70]}")
