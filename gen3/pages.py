from core import *
from join import build_join

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
    build_join("apply")

def build_onboarding():
    build_join("onboarding")

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
