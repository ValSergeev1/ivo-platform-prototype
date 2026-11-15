from core import *

def topbar(title, depth=1):
    pre = "../" * depth
    return f'''<header class="top" style="top:var(--banner)"><a href="{pre}index.html" class="row" style="text-decoration:none;min-height:44px"><img class="mark-d" src="{pre}assets/img/ivo-mark-white.png" alt="" style="width:26px;height:26px"><img class="mark-l" src="{pre}assets/img/ivo-mark-navy.png" alt="" style="width:26px;height:26px"><b>IVO OS</b></a><span class="t3">/</span><b class="grow ell">{title}</b></header>'''

def flow(wid, steps, done_text):
    st = "".join(f'<div data-step><div class="col gap16"><div class="row between"><span class="eyebrow">{who}</span><span class="small t3" data-count></span></div><h3>{t}</h3>{body}</div></div>' for t, body, who in steps)
    bar = "".join("<i></i>" for _ in steps)
    return f'''<div class="inset wz" data-wizard id="{wid}"><div class="wzbar" style="margin-bottom:14px">{bar}</div>{st}
<div class="row" style="margin-top:16px"><button class="btn" type="button" data-prev>{ic("arrow-left","sm")}<span>Back</span></button><button class="btn primary grow" type="button" data-next data-finish="Done" data-toast="{done_text}"><span>Continue</span>{ic("arrow-right","sm")}</button></div></div>'''

def opt(key, title, sub, status, inner, fit=""):
    cls = {"approved":"chosen","allowed":"","not-chosen":"dim","later":"dim"}[status]
    badge = {"approved":chip(ic("badge-check","sm")+"Approved by owner 2026-11-13","ok"),"allowed":chip("Allowed for existing accounts","info"),"not-chosen":chip("Not chosen","later"),"later":chip("Later","later")}[status]
    return f'''<section class="opt {cls}" aria-labelledby="o-{key}"><div class="row between wrap"><span class="mono acc" style="font-size:20px">{key}</span>{badge}</div><h2 id="o-{key}" class="h3">{title}</h2><p class="small t2">{sub}</p>{inner}{f'<div class="note">{ic("info","sm")}<div>{fit}</div></div>' if fit else ""}</section>'''

def build_apply():
    wa = flow("wa", [
        ("IVO invites the contractor", f'<div class="panel"><div class="bd"><div class="xs t3">Email from IVO</div><p class="small" style="margin-top:6px">“Dana at IVO Group invited Bluewater Flooring LLC to apply.”</p><div style="margin-top:10px">{btn("Accept invitation","sm primary")}</div></div></div>', "IVO staff"),
        ("Sign in with email code", '<div class="otp row" style="gap:6px">' + "".join(f'<input class="input mono" style="text-align:center;padding:0" value="{d}" aria-label="Digit {i+1}">' for i,d in enumerate("204816")) + '</div>', "Contractor"),
        ("Company info", '<label class="field"><span>Legal name</span><input class="input" value="Bluewater Flooring LLC"></label>', "Contractor"),
        ("Trades &amp; regions", '<fieldset class="pick" style="border:0;padding:0;margin:0"><legend class="sr">Trades</legend><label><input type="checkbox" checked><span>Flooring</span></label><label><input type="checkbox" checked><span>Drywall</span></label><label><input type="checkbox"><span>Paint</span></label></fieldset>', "Contractor"),
        ("Documents", li("COI_sample.pdf","Uploaded · virus-scanned","file-check","ok",chip("Uploaded","ok")), "Contractor"),
        ("References", '<label class="field"><span>Reference 1</span><input class="input" value="Evergreen Restoration Co."></label><p class="xs t3">Count still open: 1 or 2.</p>', "Contractor"),
        ("Compliance check", f'<div class="col gap6"><div class="row small">{ic("circle-check","sm okc")}State registration lookup active</div><div class="row small">{ic("circle-check","sm okc")}Certificate limits ok</div></div>', "IVO staff"),
        ("Approval", f'<p class="small">Approve Bluewater Flooring LLC?</p><div>{btn("Approve","sm primary",attrs=" data-toast=&quot;Approved (prototype).&quot;")}</div>', "Owner"),
        ("Onboarding", f'<div class="col gap6"><div class="row small">{ic("eye","sm acc")}Watched trial first job</div><div class="row small">{ic("route","sm acc")}Ready for routing</div></div><a class="btn sm" href="../contractor/index.html#today">See the contractor app</a>', "Contractor"),
    ], "Bluewater Flooring is ready for routing (prototype).")
    wb = '<div class="inset small t2">Open application form on the website. Anyone can apply, then verification and a trial job.</div>'
    wc = '<div class="inset small t2">A trusted contractor or customer refers them. IVO reviews, then the same invite as A.</div>'
    body = topbar("Contractor join process") + f'''<main id="main" class="page" tabindex="-1"><div class="ph"><div><div class="eyebrow">Decision recorded · 13 Nov 2026</div><h1 style="margin-top:6px">How contractors join the network</h1><p>The owner approved option A. Click through it step by step. Sample data only.</p></div><div class="acts">{btn("Customer join process","",href="../onboarding/index.html",ic_after="arrow-right")}</div></div>
<div class="grid g-main-l">{opt("A","Invite-only, staff-vetted","Staff invite contractors they choose, after vetting. The first job is a closely watched trial.","approved",wa,"The existing “Partner with IVO” form stays as an inquiry that lands in Triage; staff decide whether to invite.")}
<div class="col gap16">{opt("B","Open application → verification → trial job","Anyone can apply on the website.","not-chosen",wb)}{opt("C","Referral-based","A trusted contractor or customer refers them.","not-chosen",wc,"Not chosen for launch. Could work later as an extra source, using the same invite as A.")}
{note("Still open: how many references to require (1 or 2), required documents, and who besides the owner can approve a contractor (a second admin).","circle-help")}</div></div></main>'''
    page("apply/index.html", "Contractor join process", body, cmds=[("Navigate","Option A flow","#wa","Approved","badge-check"),("Prototype","Contractor app","../contractor/index.html#today","","smartphone"),("Prototype","Customer join","../onboarding/index.html","Option 1","users")], app="IVO join process")

def build_onboarding():
    o1 = flow("o1", [
        ("Customer sends a request", '<div class="panel"><div class="bd small t2">Website request form: trade, location, scope, urgency, budget, photos. No account needed.</div></div>', "Customer"),
        ("Confirmation email", '<div class="inset small">“We received REQ-1059”</div>', "System"),
        ("IVO reviews &amp; calls", '<p class="small t2">Triage in the staff console.</p><a class="btn sm" href="../console/index.html#triage">See triage</a>', "IVO staff"),
        ("Approve the invite", f'<p class="small">Invite Maya Ortiz to a Harborline workspace?</p><div>{btn("Approve invite","sm primary",attrs=" data-toast=&quot;Invite approved (prototype).&quot;")}</div>', "IVO staff"),
        ("Accept &amp; sign in", '<p class="small t2">Invite email → email code → the request is already inside.</p><a class="btn sm" href="../customer/index.html#invite">See it in the customer app</a>', "Customer"),
        ("Set up the company", f'<div class="col gap6"><div class="row small">{ic("building-2","sm acc")}Add properties</div><div class="row small">{ic("user-plus","sm acc")}Invite colleagues (IVO confirms)</div></div>', "Customer"),
    ], "Customer workspace ready (prototype).")
    o2 = '<div class="inset small t2">Staff set up the company for a customer IVO already works with, then send the same invite. Email code, then an empty workspace with properties.</div>'
    o3 = '<div class="inset small t2">Like option 1, plus a no-login private tracker link until they’re invited. Out of launch scope.</div>'
    body = topbar("Customer join process") + f'''<main id="main" class="page" tabindex="-1"><div class="ph"><div><div class="eyebrow">Decision recorded · 13 Nov 2026</div><h1 style="margin-top:6px">How customers get into the portal</h1><p>The portal is invite-only. The owner approved option 1: request first, then an invite after IVO reviews it. Sample data only.</p></div><div class="acts">{btn("Contractor join process","",href="../apply/index.html",ic_after="arrow-right")}</div></div>
<div class="grid g-main-l">{opt("1","Request first, then invite","New customers send a request; after IVO reviews it, they’re invited.","approved",o1,"Staff can still use option 2 for accounts IVO already knows.")}
<div class="col gap16">{opt("2","Account first (staff-invited)","IVO sets up accounts for customers it already works with.","allowed",o2,"Same invite, no extra build.")}{opt("3","Request first + private tracker link","A no-login status page until they’re invited.","later",o3,"Stays marked Later.")}
{note("Still open: who can approve a new customer workspace, and the role matrix.","circle-help")}</div></div></main>'''
    page("onboarding/index.html", "Customer join process", body, cmds=[("Navigate","Option 1 flow","#o1","Approved","badge-check"),("Prototype","Customer app","../customer/index.html#invite","","smartphone"),("Prototype","Contractor join","../apply/index.html","Option A","hard-hat")], app="IVO join process")

def build_hub():
    apps = [("console/index.html","layout-dashboard","Staff console","Desktop + phone","Command center, dispatch board with live map, work orders, approvals, AI copilot, bidding, network, settings and the audit log."),
            ("console/index.html#bidding","file-text","Bidding on contracts","AI module","Package analysis with page references, scope structuring, gated sub outreach, leveling grid, price recommendation, auto-filled bid form."),
            ("customer/index.html","smartphone","Customer app","Phone, installable","One-tap Emergency, a “Happening now” card, one-tap change orders, photo timeline, sign-off."),
            ("customer-portal/index.html","monitor","Customer portal","Desktop","The same workspace on a computer: requests table, approvals, documents, invoices, properties, users."),
            ("contractor/index.html","hard-hat","Contractor app","Phone, installable","A Today job card, camera check-in, photo timeline, punch pins on plans, bids on posted projects, closeout."),
            ("vendor-portal/index.html","building","Vendor / sub portal","Desktop","Office view: bid confirmations of price and availability, packets, crew schedule, compliance."),
            ("apply/index.html","badge-check","Contractor join process","Decision · option A","Invite-only after vetting, with a watched trial first job."),
            ("onboarding/index.html","users","Customer join process","Decision · option 1","Request first, invited after review. Staff can create known accounts.")]
    cards = "".join(f'<a class="appcard" href="{h}"><div class="row between"><span class="ic">{ic(i)}</span>{chip(c)}</div><h2 class="h3">{t}</h2><p class="small t2">{d}</p><span class="go">Open {ic("arrow-right","sm")}</span></a>' for h,i,t,c,d in apps)
    tick = "".join(f'<span>{ic(i,"sm acc")}{t}</span>' for i,t in [("map-pin","Ana Kim checked in · REQ-1042 · 9:02 AM"),("message-square-reply","Summit Interiors confirmed $72,200 · BID-2201"),("shield-check","CO-2 approved by customer · waiting on IVO"),("scan-text","Package analyzed · BID-2210 · 269 pages"),("siren","Emergency tier · first answer 15 min"),("file-check-2","Bid form auto-filled · waiting for admin approval")])
    fl = "".join(f'<a href="{h}"><span class="n">{n}</span><b class="small">{t}</b></a>' for n,t,h in [("1 · CUSTOMER","Request or one-tap emergency","customer/index.html#home"),("2 · STAFF","AI triage, a person confirms","console/index.html#triage"),("3 · DISPATCH","Drag to a crew, see why","console/index.html#dispatch"),("4 · APPROVE","One queue for every send","console/index.html#approvals"),("5 · FIELD","Today card, camera check-in","contractor/index.html#today"),("6 · CHANGE","Customer approves in one tap","customer/index.html#approve"),("7 · PUNCH","Pins on the plan","contractor/index.html#punch"),("8 · CLOSEOUT","Package builder, sign-off","console/index.html#closeout")])
    news = "".join(li(t,s,i,"gold") for t,s,i in [("New design system","Geist type scale, Lucide icons, dark and light themes from navy and gold","palette"),("Command menu and shortcuts","⌘K everywhere, G-letter jumps, J/K lists, ? for help","command"),("AI copilot that asks first","Explain, approve or edit. Every draft lands in Approvals","sparkles"),("Dispatch board","Live map, crew lanes, drag-to-assign, why-this-contractor","radar"),("Bid leveling grid","Exclusions priced back in, price slider, win chance","table-2"),("Field-first apps","44 px targets, offline-ready, camera in the tab bar","smartphone")])
    sw = "".join(f'<div><div class="swatch" style="background:{c}"></div><div class="small" style="margin-top:6px;font-weight:600">{n}</div><div class="xs t3 mono">{c}</div></div>' for n,c in [("Navy","#061d2a"),("Navy 2","#0c2938"),("Gold","#b38a55"),("Gold light","#e1c395")])
    body = f'''<header class="hub-hero"><div class="wrap" style="padding-top:56px;padding-bottom:48px">
<div class="row wrap gap16" style="margin-bottom:28px"><img class="mark-d" src="assets/img/ivo-mark-white.png" alt="" style="width:40px;height:40px"><img class="mark-l" src="assets/img/ivo-mark-navy.png" alt="" style="width:40px;height:40px"><div><b style="letter-spacing:.04em">IVO OS</b><div class="xs t3 mono">PLATFORM PROTOTYPE · V03 · COMPLETE REDESIGN</div></div></div>
<h1 class="display">One operating system for<br><em>every job IVO runs.</em></h1>
<p class="lead" style="margin-top:18px">Requests, emergencies, dispatch, field work, closeout and AI bidding as a subcontractor, in one fast, keyboard-first, field-ready system. The AI explains itself and asks before anything is sent.</p>
<div class="row wrap" style="margin-top:26px">{btn("Open the staff console","primary lg",icon="layout-dashboard",href="console/index.html")}{btn("Try the command menu","lg",icon="command",attrs=" data-cmd-open")}<span class="small t3">Fictional sample data · nothing is sent or saved</span></div></div>
<div class="tickwrap"><div class="ticker">{tick}{tick}</div></div></header>
<main id="main" class="wrap" style="padding-top:40px;padding-bottom:80px" tabindex="-1">
<div class="eyebrow">Every app</div><div class="grid g4" style="margin-top:12px">{cards}</div>
<div class="eyebrow" style="margin-top:44px">Follow one job</div><div class="flow" style="margin-top:12px">{fl}</div>
<div class="grid g2" style="margin-top:44px">{panel("What’s new in V03", f'<div class="list">{news}</div>', "sparkles", bd="bd p0")}
<div class="col gap16">{panel("Brand, kept", f'<div class="grid g4" style="grid-template-columns:repeat(4,minmax(0,1fr));gap:10px">{sw}</div><p class="small t2" style="margin-top:12px">Only the brand colors carried over. Type, icons, layout, motion and components are all new.</p>', "palette")}
{panel("Join process, recorded", '<div class="list">'+li("Contractors · option A","Approved by owner 2026-11-13 · invite-only, watched trial first job","hard-hat","ok",href="apply/index.html")+li("Customers · option 1","Approved by owner 2026-11-13 · request first, then invite","users","ok",href="onboarding/index.html")+'</div>', "badge-check", bd="bd p0")}</div></div>
<p class="foot-note" style="margin-top:32px">Prototype only, not indexed. Icons: Lucide (ISC license). Earlier versions: <a href="../index.html">V01</a> · <a href="../v2/index.html">V02</a>.</p></main>'''
    cmds = [("Apps","Staff console","console/index.html","","layout-dashboard"),("Apps","Bidding pipeline","console/index.html#bidding","","file-text"),("Apps","Dispatch board","console/index.html#dispatch","","radar"),("Apps","Customer app","customer/index.html","","smartphone"),("Apps","Customer portal","customer-portal/index.html","","monitor"),("Apps","Contractor app","contractor/index.html","","hard-hat"),("Apps","Vendor portal","vendor-portal/index.html","","building"),("Apps","Contractor join process","apply/index.html","","badge-check"),("Apps","Customer join process","onboarding/index.html","","users")]
    page("index.html", "All apps", body, depth=0, cmds=cmds, app="IVO OS V03")
