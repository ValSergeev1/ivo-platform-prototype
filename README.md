# IVO Platform prototype · V01 (sample data)

Step 2 of the IVO work order: a clickable front-end prototype of the new IVO system, reviewed by link before anything is built.
Static HTML/CSS/JS, no backend, no build step for the browser. **Everything is fictional sample data.** Nothing is sent, saved or connected to ivoservgroup.com or the live console.

Start at `index.html`.

| Part | Path | Screens |
|---|---|---|
| Staff console (desktop) | `console/` | overview (one count source), approval inbox, inquiry triage, requests, job detail with timeline and response timers, bid packages with files, deadline + time zone and duplicate check, contractor directory with compliance, applications, team and roles. Before/after notes against today's console |
| Customer app (phone, installable) | `customer/` | invite, email-code sign-in, home, 8-step request wizard, emergency button, job tracker, change order vs NTE, closeout sign-off, documents, company users, account |
| Customer portal (desktop) | `customer-portal/` | dashboard, requests, job, new request, approvals, documents, properties, users |
| Contractor app (phone, installable) | `contractor/` | sign-in, opportunities, packet, bid wizard, jobs and schedule, check-in, punch list, change-order request, closeout, compliance, company and crew |
| Vendor portal (desktop) | `vendor-portal/` | overview and scorecard, opportunities, packet and bid, bids, jobs and crew schedule, compliance, company and crew |
| Decision: contractor application | `apply/` | options A / B / C side by side, each clickable step by step, with a recommendation |
| Decision: customer onboarding | `onboarding/` | options 1 / 2 / 3 side by side, clickable, with a recommendation |

Launch scope (locked by the owner): items outside it (AI drafting and bid engine, payments, SMS, store apps, public self-serve) appear only as greyed **Later** placeholders. Routing suggestions are rule-based.

Source: `src/*.html` fragments are wrapped by `python3 build.py` (shared head, noindex, "Prototype – sample data" banner). `python3 gen_decisions.py` regenerates `src/apply.html` and `src/onboarding.html`. Shared UI: `assets/css/app.css`, `assets/js/app.js`. Screenshots: `screens/`.

noindex is set on every page and `robots.txt` disallows all crawling.
