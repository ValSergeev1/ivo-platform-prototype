# Changes

## V03 · Nov 14, 2026
A complete from-scratch redesign at `/v3/` (V01 and V02 untouched). New design system (“IVO OS”): Geist type scale, Lucide SVG icons, dark and light themes built only from the brand navy and gold, new grid, motion and components. Staff console: command center, dispatch board (live map, crew lanes, drag-to-assign with why-this-contractor), work-order list/board, triage, split-view approvals, AI copilot that explains and asks before acting, bidding (pipeline, package analysis with page references, scope structuring, gated sub outreach, full leveling grid, price recommendation, auto-filled bid form, win-to-job, loss review), network, vetting, integrations, settings hub and a hash-chain audit-log viewer. Customer app with one-tap Emergency on Home, customer portal, contractor app with a Today job card, camera check-in, photo timeline and punch pins on plans, vendor portal with bid confirmations, and the two join-process pages. Verified at 1440 and 390 px in both themes: no horizontal overflow, no text under 12 px, 44 px touch targets on phone, contrast passes, no console errors. Source: `python3 gen_v3.py` (modules in `gen3/`). Screenshots: `screens/v3/`.

## V02 · Nov 13, 2026 (late)
Launch scope now includes an AI bidding module (IVO as a subcontractor on outside contracts) and platform integrations. Every filled bid and every subcontractor message waits on admin approval. New V02 screens: bidding pipeline, package extraction with citations, sub confirmations, leveling and recommended price, auto-filled bid form, won-to-job and lost reason, contractor/vendor bid confirmation, and an Integrations page with generic sample cards (no third-party names). Some sample bids are tagged "Imported from external platform." Payments and text messages stay Later.

## V02 · Nov 13, 2026 (evening)
A second design, at `/v2/`, kept separate from V01. Dark-navy glass, light and dark mode, a command bar (⌘K), one live timeline per job, an SVG coverage map, swipe-to-accept, camera-first check-in, a “What’s happening now” card, and one-tap change-order approval. Join decisions (contractors A, customers 1) are shown as approved. Launch-scope later features appear only as teasers.

## V01 · Nov 13, 2026 (evening)
Join process recorded: contractors option A (invite-only, watched trial first job, Partner with IVO form feeds Triage) and customers option 1 (request first, invite after review). Option 2 allowed for existing accounts. Options B and C marked not chosen; customer option 3 stays Later.

## V01 · Nov 13, 2026
First clickable prototype: staff console, customer app and portal, contractor app and vendor portal, and two decision screens. Kept to the locked launch scope; out-of-scope items are marked Later.
