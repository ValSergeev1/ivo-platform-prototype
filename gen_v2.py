#!/usr/bin/env python3
"""Generate the IVO platform prototype V02 static pages under /v2/."""
import os, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "v2")

def write(rel, html):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p) if os.path.dirname(rel) else OUT, exist_ok=True)
    open(p, "w").write(html)
    print("wrote", rel, "bytes", len(html))

def cmd_items(items):
    out = []
    for label, href, hint in items:
        out.append(f'<button type="button" data-cmd="{label}" data-href="{href}"><span>{label}</span><small>{hint}</small></button>')
    return "\n".join(out)

def shell(title, body, depth=1, bodyclass="", cmds=None, head=""):
    R = "../" * depth
    cmds = cmds or []
    cmd_html = cmd_items(cmds)
    index = f"{R}index.html" if depth else "index.html"
    v01 = f"{R}../index.html" if depth else "../index.html"
    v02 = f"{R}index.html" if depth else "index.html"
    return f'''<!doctype html>
<html lang="en" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive"><meta name="googlebot" content="noindex,nofollow">
<meta name="theme-color" content="#061d2a">
<title>{title} · IVO Platform prototype V02 (sample data)</title>
<link rel="icon" href="{R}assets/img/favicon.png"><link rel="apple-touch-icon" href="{R}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/app.css">{head}
</head><body class="{bodyclass}">
<a class="tiny" href="#main" style="position:absolute;left:-999px;top:auto">Skip to content</a>
<div class="proto-banner"><b>Prototype – sample data</b><span class="hide-narrow">V02 · fictional companies and people · nothing is sent or saved</span>
<nav class="ver-switch" aria-label="Prototype version"><a href="{v01}">V01</a><span class="on">V02</span></nav>
<span class="grow"></span>
<button class="search-pill" type="button" data-cmd-open style="min-width:auto;padding:4px 10px">Search or jump <span class="kbd">⌘K</span></button>
<button class="icon-btn" type="button" data-theme-toggle aria-label="Switch to light mode" title="Light or dark mode">◐</button>
<a href="{index}">All screens</a></div>
{body}
<div id="cmdk" class="cmdk" role="dialog" aria-modal="true" aria-label="Command bar">
  <div class="box">
    <input type="search" placeholder="Search jobs, people, actions…" aria-label="Command bar" autocomplete="off">
    <div class="res" id="cmdk-results">{cmd_html}</div>
  </div>
</div>
<script src="{R}assets/js/app.js"></script>
</body></html>
'''

MAP = '''
<div class="map-wrap glass" id="coverage-map">
<svg viewBox="0 0 400 420" role="img" aria-label="Map of job sites and contractors across Washington, Oregon, Idaho and Northern California">
  <title>Coverage map: Washington, Oregon, Idaho and Northern California</title>
  <text x="16" y="22" fill="currentColor" font-size="11" letter-spacing="1.6" font-weight="600">WA · OR · ID · NORTHERN CA</text>
  <g fill="var(--map-fill)" stroke="var(--map-stroke)" stroke-width="1.2">
    <path d="M48 40 h128 l10 18 -6 66 -34 10 H52 l-12 -28 8-48 z"/>
    <path d="M48 136 h96 l36 -10 14 16 v76 l-18 12 H50 l6-40 z"/>
    <path d="M186 40 h88 l12 38 -28 22 8 48 -18 78 -42 8 -14-78 6-28 -8-80 z"/>
    <path d="M50 252 h120 l22 -10 12 28 -38 68 -78 18 -26-38 8-48 z"/>
    <path d="M62 352 128 372 148 404 54 414 z" opacity=".35" stroke="none"/>
  </g>
  <g fill="currentColor" opacity=".7" font-size="12" font-weight="600">
    <text x="92" y="96">WA</text><text x="92" y="206">OR</text><text x="226" y="150">ID</text><text x="88" y="314">N. CA</text>
  </g>
  <g class="map-pin urgent" data-map-go="#job" tabindex="0" role="link" aria-label="Tacoma: Unit 3B ceiling leak, on site">
    <circle cx="108" cy="108" r="6"/><text class="lbl" x="118" y="104">Tacoma · REQ-1042 on site</text>
  </g>
  <g class="map-pin" data-map-go="#job" tabindex="0" role="link" aria-label="Lynnwood: supply line leak, waiting on contractor">
    <circle cx="100" cy="58" r="5"/><text class="lbl" x="110" y="54">Lynnwood · plumbing offer</text>
  </g>
  <g class="map-pin" tabindex="0" role="img" aria-label="Bellevue: lobby door closer, scheduled">
    <circle cx="122" cy="70" r="5"/><text class="lbl" x="132" y="84">Bellevue · scheduled</text>
  </g>
  <g class="map-pin" tabindex="0" role="img" aria-label="Portland coverage, 2 contractors">
    <circle cx="96" cy="196" r="5"/><text class="lbl" x="106" y="192">Portland · 2 contractors</text>
  </g>
  <g class="map-pin" tabindex="0" role="img" aria-label="Boise coverage, 1 contractor">
    <circle cx="236" cy="168" r="5"/><text class="lbl" x="246" y="164">Boise · 1 contractor</text>
  </g>
  <g class="map-pin" tabindex="0" role="img" aria-label="Redding coverage, ready to route">
    <circle cx="86" cy="300" r="5"/><text class="lbl" x="96" y="296">Redding · coverage</text>
  </g>
</svg>
<div class="map-legend"><span class="chip bad">On site / urgent</span><span class="chip gold">Active job</span><span class="chip">Coverage only</span></div>
</div>
'''

def timeline():
    evs = [
        ("appr","Mon 8:12 AM","Request received","Maya Ortiz submitted photos and a $4,800 not-to-exceed.","REQ-1042"),
        ("msg","Mon 8:40 AM","IVO reviewed","Dana confirmed drywall & paint, Urgent tier. Rules suggested Bluewater Flooring.","Review"),
        ("appr","Mon 1:05 PM","Contractor confirmed","Sam Rivera accepted the packet. Address released after accept.","Award"),
        ("photo","Tue 9:02 AM","On site","Ana Kim checked in with GPS and a photo of the ceiling.","Check-in"),
        ("co","Tue 11:20 AM","Change order CO-2","Sistering a joist, +$620. Maya can approve in one tap. Waiting.","Needs approval"),
        ("msg","","Closeout and invoice","Later, after punch and sign-off.","Later"),
    ]
    items = []
    for i,(k,when,title,body,tag) in enumerate(evs):
        now = ' style="opacity:.55"' if not when else ""
        items.append(f'''<div class="tev"{now}><div class="m {k}"></div><div><div class="row between"><b>{title}</b><span class="when">{when or "—"}</span></div><p class="small muted">{body}</p><span class="chip">{tag}</span></div></div>''')
    return '<div class="tlive">'+"".join(items)+"</div>"

FLASH = '''
<div class="flash" aria-label="Job status, readable in about three seconds">
  <div class="st done">Received</div>
  <div class="st done">Reviewed</div>
  <div class="st done">Crew assigned</div>
  <div class="st now">On site</div>
  <div class="st">Sign-off</div>
</div>
'''

# ---------- shared command lists ----------
CM_CON = [
    ("Open overview","#overview","Board and map"),
    ("Open triage board","#triage","J/K to move"),
    ("Open approval inbox","#approvals","3 waiting"),
    ("Open REQ-1042 timeline","#job","Unit 3B leak"),
    ("Open coverage map","#map","WA OR ID N-CA"),
    ("Find Bluewater Flooring","#contractor","Why they were picked"),
    ("Applications inbox","#applications","Invite-only, option A"),
    ("Team and role matrix","#team","Still open"),
    ("Invite a contractor","#applications","Staff-vetted invite"),
    ("Open bidding pipeline","#bidding","Outside contracts"),
    ("BID-2201 package","#bidpkg","Cedar Ridge Elementary"),
    ("Sub confirmations","#bidsubs","Approval queue"),
    ("Bid leveling and price","#bidlevel","Recommended price"),
    ("Approve and submit bid","#bidform","Admin approval"),
    ("Integrations","#integrations","Connections"),
]
CM_CUS = [
    ("What's happening now","#home","Home"),
    ("Approve the change order","#approve","One tap"),
    ("New request","#new","8-step wizard"),
    ("Emergency hold button","#emergency","Press and hold"),
    ("Job timeline","#job","REQ-1042"),
    ("Open documents","#docs","Files"),
    ("Company users","#users","Invites"),
]
CM_KON = [
    ("Opportunities","#opps","Swipe to accept"),
    ("Open packet","#opp","Hallway ceiling"),
    ("Camera check-in","#checkin","REQ-1042"),
    ("Earnings and pipeline","#payouts","Tracking only"),
    ("Submit a bid","#bid","Wizard"),
    ("Compliance documents","#compliance","Expiry"),
    ("Punch list","#punch","Job tools"),
    ("Bid confirmation request","#bidconfirm","Confirm price and dates"),
]

def side_nav(active):
    items = [
        ("overview","Overview"),("map","Map"),("triage","Triage"),("approvals","Approvals"),
        ("requests","Requests"),("job","Job timeline"),("bidding","Bidding"),
        ("bids","Outbound packets"),
        ("contractors","Network"),("applications","Applications"),("integrations","Integrations"),("team","Team & roles"),
    ]
    links = []
    for hid,lab in items:
        cls = ' active' if hid==active else ''
        match = ' data-match="bid contractor"' if hid in ("bids","contractors") else ''
        if hid=="bids": match=' data-match="bid"'
        if hid=="bidding": match=' data-match="bidpkg bidsubs bidlevel bidform bidwon bidlost"'
        if hid=="contractors": match=' data-match="contractor"'
        if hid=="job": match=' data-match="job"'
        links.append(f'<a class="nav{cls}" href="#{hid}"{match}>{lab}</a>')
    return "\n".join(links)

def console_chrome(title, screen, inner, top_extra=""):
    return f'''
<div class="shell">
  <aside class="side">
    <div class="brand"><img src="../assets/img/ivo-mark-white.png" alt=""><div><b>IVO</b><span>STAFF CONSOLE · V02</span></div></div>
    {side_nav(screen)}
    <div class="hint">Type <span class="kbd">⌘K</span> to search or jump. On triage: <span class="kbd">J</span> <span class="kbd">K</span> to move, <span class="kbd">Enter</span> to open.</div>
  </aside>
  <div class="main" id="main" data-router>
    <div class="topb"><button class="menu-btn" type="button" aria-label="Open menu">☰</button>
      <h2>{title}</h2>
      <button class="search-pill grow" type="button" data-cmd-open>Search jobs, contractors, actions… <span class="kbd">⌘K</span></button>
      <span class="chip offline">Offline-ready staff tools</span>
      <a class="chip warn" href="#approvals">5 approvals</a>
      {top_extra}
    </div>
    {inner}
  </div>
</div>
'''

print("helpers ok")

def page_index():
    tiles = [
        ("console/index.html","ivo-113.webp","Desktop","Staff console","Triage board with keyboard shortcuts, a live job timeline, a coverage map, and a clear reason for every routing pick."),
        ("customer/index.html","ivo-04.webp","Phone app","Customer app","A “What’s happening now” card, a status line you can read in three seconds, and one-tap change-order approval."),
        ("customer-portal/index.html","ivo-21.webp","Desktop","Customer portal","The same workspace on a computer, with the command bar and the job timeline in the middle."),
        ("contractor/index.html","ivo-51.webp","Phone app","Contractor app","Swipe to accept or decline, camera-first check-in, and an earnings glance marked tracking-only."),
        ("vendor-portal/index.html","ivo-76.webp","Desktop","Vendor portal","Office view of opportunities, compliance and the same job timeline."),
        ("console/index.html#bidding","ivo-99.webp","New","Bidding on contracts","IVO bids as a subcontractor. The AI fills the form; you approve before anything is sent."),
        ("apply/index.html","ivo-99.webp","Recorded","Join process","Contractors: option A. Customers: option 1. Already approved by the owner."),
    ]
    thtml=""
    for href,img,chip,h,p in tiles:
        thtml+=f'''<a class="tile glass" href="{href}"><div class="im" style="background-image:url(assets/img/{img})"><span class="chip navy">{chip}</span></div><div class="bd"><h3>{h}</h3><p class="small muted">{p}</p><span class="btn sm line" style="align-self:flex-start;margin-top:8px">Open →</span></div></a>'''
    body=f'''
<header class="land-h">
  <div class="wrap">
    <div class="row between wrap" style="margin-bottom:20px">
      <div class="brand" style="margin:0"><img src="assets/img/ivo-mark-white.png" alt=""><div><b>IVO</b><span>GROUP · PLATFORM PROTOTYPE V02</span></div></div>
      <nav class="ver-switch" aria-label="Prototype version"><a href="../index.html">V01</a><span class="on">V02</span></nav>
    </div>
    <div class="eyebrow" style="color:#e1c395">A bolder design on the same locked launch scope</div>
    <h1>The IVO system, built to feel <em>inevitable</em>.</h1>
    <p style="max-width:680px;margin-top:14px;font-size:16px;color:#cfdbe3">One command bar. One live timeline per job. A map of the network. Dark glass, light mode, and a primary action on every screen — so staff, customers and contractors can move without hunting. Sample data only.</p>
    <div class="row wrap" style="margin-top:22px">
      <a class="btn lg" href="console/index.html">Open the staff console</a>
      <button class="btn lg ghost" type="button" data-cmd-open style="color:#fff;border-color:#ffffff55">Try the command bar <span class="kbd">⌘K</span></button>
    </div>
  </div>
</header>
<div class="wrap" id="main" style="padding:28px 16px 72px">
  <div class="eyebrow">Follow one job</div>
  <div class="flow">
    <a class="glass" href="customer/index.html#new"><span class="n">1 · CUSTOMER</span><b>Submit a request</b></a>
    <a class="glass" href="console/index.html#triage"><span class="n">2 · STAFF</span><b>Triage, with reasons</b></a>
    <a class="glass" href="console/index.html#approvals"><span class="n">3 · OWNER</span><b>Approve routing</b></a>
    <a class="glass" href="contractor/index.html#opp"><span class="n">4 · CONTRACTOR</span><b>Swipe to accept</b></a>
    <a class="glass" href="contractor/index.html#checkin"><span class="n">5 · FIELD</span><b>Camera check-in</b></a>
    <a class="glass" href="customer/index.html#approve"><span class="n">6 · CUSTOMER</span><b>Approve in one tap</b></a>
    <a class="glass" href="contractor/index.html#closeout"><span class="n">7 · CLOSEOUT</span><b>Photos and punch</b></a>
    <a class="glass" href="customer/index.html#closeout"><span class="n">8 · SIGN-OFF</span><b>Done</b></a>
  </div>
  <div class="eyebrow" style="margin-top:36px">The network, at a glance</div>
  {MAP.replace('data-map-go="#job"','data-map-go="console/index.html#job"')}
  <div class="eyebrow" style="margin-top:36px">Every part</div>
  <div class="grid g3">{thtml}</div>
  <div class="eyebrow" style="margin-top:36px" id="decisions">Join process, already recorded</div>
  <div class="grid g2">
    <a class="decision rec" href="apply/index.html"><h3>Contractors · option A</h3><p class="small" style="margin-top:6px"><span class="chip ok">Approved by owner 2026-11-13</span></p><p class="small muted" style="margin-top:8px">Invite-only after staff vetting, with a watched trial first job. The Partner with IVO form feeds Triage. B and C were not chosen.</p></a>
    <a class="decision rec" href="onboarding/index.html"><h3>Customers · option 1</h3><p class="small" style="margin-top:6px"><span class="chip ok">Approved by owner 2026-11-13</span></p><p class="small muted" style="margin-top:8px">Request first, invite after IVO review. Option 2 is allowed for existing accounts. Option 3 stays Later.</p></a>
  </div>
  <div class="later" style="margin-top:20px"><span class="chip later">Later</span> Still out of this build: payments, text messages, and public self-serve access. The AI bidding module and subcontractor outreach (with admin approval) are in the launch scope — open Bidding in the staff console.</div>
  <p class="tiny muted" style="margin-top:28px">IVO Platform prototype V02 · static HTML, CSS and JS on GitHub Pages · not indexed · all names, companies, addresses, emails and amounts are fictional. V01 remains at the original URLs.</p>
</div>
'''
    cmds=[
        ("Open the staff console","console/index.html","Desktop"),
        ("Open the customer app","customer/index.html#home","What's happening now"),
        ("Open the contractor app","contractor/index.html#opps","Swipe to accept"),
        ("Coverage map","console/index.html#map","WA OR ID N-CA"),
        ("Bidding pipeline","console/index.html#bidding","Outside contracts"),
        ("Integrations","console/index.html#integrations","Connections"),
        ("Contractor join decision","apply/index.html","Option A approved"),
        ("Customer join decision","onboarding/index.html","Option 1 approved"),
        ("Back to V01","../index.html","Original prototype"),
    ]
    return shell("Start here", body, depth=0, cmds=cmds)

def bidding_screens():
    def col(title, n, cards):
        return f'<div class="col glass"><h3>{title}<span class="chip">{n}</span></h3>{cards}</div>'

    def card(href, code, name, meta, chip, chipcls="", tag=""):
        t = f'<span class="chip {chipcls}">{chip}</span>' if chip else ""
        extra = (
            f'<p class="tiny" style="margin-top:4px"><span class="chip info">{tag}</span></p>'
            if tag else ""
        )
        return (
            f'<a class="job-card" href="{href}"><div class="row between"><b>{code}</b>{t}</div>'
            f'<p class="small">{name}</p><p class="tiny muted">{meta}</p>{extra}</a>'
        )

    board = col("Found", 1, card("#bidpkg", "BID-2212", "Seattle Piers warehouse TI",
        "Due Dec 4 · invitation received", "New", "", "Imported from external platform"))
    board += col("Reviewing", 1, card("#bidpkg", "BID-2210", "Redding Clinic tenant improvement",
        "Due Nov 25 · AI extracting", "In review"))
    board += col("Pricing", 1, card("#bidlevel", "BID-2198", "Bellevue Library lighting",
        "Due Nov 21, 3:00 PM PT", "2 days", "warn"))
    board += col("Sub confirmations", 1, card("#bidsubs", "BID-2204", "Tacoma Civic Annex HVAC",
        "Due Nov 22 · 1 no reply", "Waiting", "warn"))
    ready = (
        '<a class="job-card" href="#bidform"><div class="row between"><b>BID-2201</b>'
        '<span class="chip gold">Ready</span></div>'
        '<p class="small">Cedar Ridge Elementary modernization</p>'
        '<p class="tiny muted">Due Fri Nov 20, 2:00 PM PT</p>'
        '<div class="countdown" data-sla="980" data-warn="240" style="margin-top:8px;padding:8px 10px">'
        '<span class="tiny muted">Bid due</span><span class="v">-</span></div>'
        '<p class="tiny" style="margin-top:4px"><span class="chip info">Imported from external platform</span></p></a>'
    )
    board += col("Ready for approval", 1, ready)
    board += col("Submitted", 1, card("#bidpkg", "BID-2188", "Portland Fire Station 12",
        "Submitted Nov 12 · awaiting award", "Out"))
    board += col("Won", 1, card("#bidwon", "BID-2175", "Lynnwood Courthouse doors",
        "Awarded Nov 10 · job opened", "Won", "ok"))
    board += col("Lost", 1, card("#bidlost", "BID-2162", "Boise City Hall roof",
        "Lost Nov 6 · price", "Lost", "bad"))
    board += col("No-bid", 1, card("#bidpkg", "BID-2207", "Multnomah Parking garage",
        "No-bid Nov 11 · capacity", "No-bid"))

    pipeline = f"""<section class="content app" data-screen="bidding">
      <div class="row between wrap"><div><h3>Bidding on outside contracts</h3><p class="small muted">IVO acting as a subcontractor. Every filled-out bid and every message to a sub waits here for admin approval.</p></div><a class="btn sm line" href="#integrations">Integrations</a></div>
      <div class="grid g4">
        <div class="metric glass"><div class="l">Due in 7 days</div><div class="v">3</div></div>
        <div class="metric glass"><div class="l">Waiting on your approval</div><div class="v">2</div></div>
        <div class="metric glass"><div class="l">Subs to confirm</div><div class="v">1</div></div>
        <div class="metric glass"><div class="l">Won this month</div><div class="v">1</div></div>
      </div>
      <div class="bid-board">{board}</div>
    </section>"""

    pkg = """<section class="content app" data-screen="bidpkg">
      <div class="row between wrap"><div><a class="tiny gold" href="#bidding">Back to pipeline</a><div class="eyebrow" style="margin-top:8px">BID-2201 · Northline Construction (sample GC)</div><h3>Cedar Ridge Elementary modernization</h3><p class="small muted">Sample School District · Kent, WA · bid due Fri Nov 20, 2026, 2:00 PM PT</p></div>
        <div class="stack" style="align-items:flex-end"><span class="chip gold">Ready for approval</span><span class="chip info">Imported from external platform</span><div class="countdown" data-sla="980" data-warn="240"><span class="tiny muted">Bid due</span><span class="v">-</span></div></div>
      </div>
      <div class="grid g2" style="align-items:start">
        <div class="stack">
          <div class="card"><h3>Uploaded documents</h3>
            <div class="stack s8" style="margin-top:8px">
              <div class="file"><span class="ic">PDF</span><span class="grow">ITB_CedarRidge_sample.pdf<span class="tiny muted" style="display:block">Invitation to bid · 14 pages</span></span></div>
              <div class="file"><span class="ic">PDF</span><span class="grow">Plans_A101-A140_sample.pdf<span class="tiny muted" style="display:block">Architectural plans · 40 sheets</span></span></div>
              <div class="file"><span class="ic">PDF</span><span class="grow">Specs_Div09-26_sample.pdf<span class="tiny muted" style="display:block">Specifications, divisions 9-26</span></span></div>
              <div class="file"><span class="ic">PDF</span><span class="grow">Addendum_02_sample.pdf<span class="tiny muted" style="display:block">Addendum 2 · night work and RTU note</span></span></div>
            </div>
          </div>
          <div class="card"><h3>Requirements the AI pulled out</h3>
            <div class="list" style="margin-top:8px">
              <div class="li"><span class="grow">Bid due Fri Nov 20, 2:00 PM PT, local time</span><span class="cite">ITB p. 3</span></div>
              <div class="li"><span class="grow">Bid bond 5% of the base bid</span><span class="cite">ITB p. 7</span></div>
              <div class="li"><span class="grow">Insurance: general liability $2M, auto, workers' comp</span><span class="cite">ITB p. 8</span></div>
              <div class="li"><span class="grow">Acknowledge addenda 1 and 2</span><span class="cite">ITB p. 4 · Addendum 2</span></div>
              <div class="li"><span class="grow"><span class="chip warn">Risk</span> Liquidated damages $1,500 / day</span><span class="cite">ITB p. 11</span></div>
              <div class="li"><span class="grow"><span class="chip warn">Risk</span> Night work only in occupied wings</span><span class="cite">Addendum 2 p. 2</span></div>
            </div>
          </div>
        </div>
        <div class="stack">
          <div class="card"><h3>Scope by trade, with sources</h3>
            <p class="tiny muted" style="margin-bottom:8px">Each line cites the page it came from so you can check the AI.</p>
            <div class="list">
              <div class="li"><span class="grow"><b>Drywall</b> · 18,400 SF Level 4 finish, corridors and classrooms</span><span class="cite">Specs 09 29 00 · Plans A112</span></div>
              <div class="li"><span class="grow"><b>Flooring</b> · LVP, 6,200 SF in classrooms 101-118</span><span class="cite">Specs 09 65 19</span></div>
              <div class="li"><span class="grow"><b>Electrical</b> · lighting package, rooms 101-118, controls as specified</span><span class="cite">Plans E201</span></div>
              <div class="li"><span class="grow"><b>HVAC</b> · four RTU replacements, same-size, after-hours set</span><span class="cite">Specs 23 74 00 · Addendum 2</span></div>
            </div>
            <div class="row wrap" style="margin-top:12px"><a class="btn" href="#bidsubs">Sub confirmations</a><a class="btn line" href="#bidlevel">Level quotes</a></div>
          </div>
        </div>
      </div>
    </section>"""

    subs = """<section class="content app" data-screen="bidsubs">
      <div class="row between wrap"><div><a class="tiny gold" href="#bidding">Back to pipeline</a><div class="eyebrow" style="margin-top:8px">BID-2201</div><h3>Subcontractor confirmations</h3><p class="small muted">The AI matched these trades from the network and drafted a confirmation request for each. Nothing is sent until you approve the draft.</p></div><a class="btn line sm" href="#bidpkg">Package</a></div>
      <div class="card" data-item style="margin-bottom:12px">
        <div class="row between wrap"><div><span class="chip gold">Drafts waiting</span> <b>2 confirmation requests</b><p class="small muted">Harbor Air LLC (HVAC, no first send yet) and a follow-up to Metro Drywall Co. (declined once). Asks each to confirm price, availability for Nov 30, 2026-Jan 15, 2027, and capacity if IVO is awarded.</p></div><span class="chip warn" data-status>Needs approval</span></div>
        <div class="sheet" style="margin:10px 0"><p class="small">Please confirm your price of $94,800 for the four RTU replacements at Cedar Ridge Elementary, that your crew is available Nov 30-Jan 15, and that you can perform the work if IVO is awarded. Reply in the app or this thread.</p></div>
        <button class="btn" data-set="Approved to send|ok" data-toast="Marked approved. Nothing was sent (prototype).">Approve and send drafts</button>
      </div>
      <div class="card pad0 tscroll"><table class="t"><thead><tr><th>Subcontractor</th><th>Trade</th><th>Price</th><th>Dates</th><th>Capacity</th><th>Status</th></tr></thead><tbody>
        <tr><td>Summit Interiors LLC</td><td>Drywall</td><td>$72,200</td><td>Nov 30-Jan 15</td><td>Open</td><td><span class="chip ok">Confirmed</span></td></tr>
        <tr><td>Bluewater Flooring LLC</td><td>Flooring</td><td>$86,400</td><td>Nov 30-Jan 15</td><td>Open</td><td><span class="chip ok">Confirmed</span></td></tr>
        <tr><td>Cascade Electric</td><td>Electrical</td><td>$124,000 <span class="tiny muted">was $118,500</span></td><td>Nov 30-Jan 15</td><td>Open</td><td><span class="chip warn">Price changed</span></td></tr>
        <tr><td>Harbor Air LLC</td><td>HVAC</td><td>$94,800 est.</td><td>-</td><td>-</td><td><span class="chip">No reply</span></td></tr>
        <tr><td>Metro Drywall Co.</td><td>Drywall (alt.)</td><td>-</td><td>-</td><td>Booked</td><td><span class="chip bad">Declined</span></td></tr>
      </tbody></table></div>
      <a class="btn" style="margin-top:12px" href="#bidlevel">Open leveling</a>
    </section>"""

    level = """<section class="content app" data-screen="bidlevel">
      <div class="row between wrap"><div><a class="tiny gold" href="#bidding">Back to pipeline</a><div class="eyebrow" style="margin-top:8px">BID-2201</div><h3>Leveling and recommended price</h3><p class="small muted">Sub quotes side by side. Gaps and exclusions are flagged. You set the final number.</p></div></div>
      <div class="card pad0 tscroll"><table class="t level"><thead><tr><th>Trade</th><th>Sub</th><th>Quote</th><th>Exclusions</th><th>Flag</th></tr></thead><tbody>
        <tr><td>Drywall</td><td>Summit Interiors LLC</td><td>$72,200</td><td>None noted</td><td><span class="chip ok">Confirmed</span></td></tr>
        <tr class="excl"><td>Drywall</td><td>Metro Drywall Co.</td><td>-</td><td>Declined · booked</td><td><span class="chip bad">Sole source left</span></td></tr>
        <tr><td>Flooring</td><td>Bluewater Flooring LLC</td><td>$86,400</td><td>None noted</td><td><span class="chip ok">Confirmed</span></td></tr>
        <tr><td>Electrical</td><td>Cascade Electric</td><td>$124,000</td><td>Controls allowance held</td><td><span class="chip warn">Price changed +$5,500</span></td></tr>
        <tr class="gap"><td>HVAC</td><td>Harbor Air LLC</td><td>$94,800 est.</td><td>No confirmed quote</td><td><span class="chip warn">Gap · no reply</span></td></tr>
      </tbody></table></div>
      <div class="grid g2" style="align-items:start;margin-top:14px">
        <div class="card">
          <div class="eyebrow">Recommended price</div>
          <div class="v" style="font-size:28px;font-weight:560">$441,558</div>
          <p class="small muted">Confidence 72% - HVAC is still an estimate, and the electrical price moved.</p>
          <dl class="kv" style="margin-top:10px">
            <dt>Confirmed subs</dt><dd>$282,600</dd>
            <dt>HVAC estimate</dt><dd>$94,800</dd>
            <dt>Sub total</dt><dd>$377,400</dd>
            <dt>Markup 12%</dt><dd>$45,288</dd>
            <dt>Contingency 5%</dt><dd>$18,870</dd>
          </dl>
          <p class="tiny muted" style="margin-top:8px">Reasoning: leveled confirmed quotes, historical HVAC unit cost for four RTUs of this size, standard markup and contingency for liquidated-damages risk (ITB p. 11).</p>
        </div>
        <div class="card">
          <div class="eyebrow">Your final price</div>
          <div class="field"><label class="f">Base bid you will submit</label><input class="inp" value="442000" inputmode="numeric"></div>
          <a class="btn block" href="#bidform">Preview the filled bid form</a>
        </div>
      </div>
    </section>"""

    form = """<section class="content app" data-screen="bidform">
      <div class="row between wrap"><div><a class="tiny gold" href="#bidding">Back to pipeline</a><div class="eyebrow" style="margin-top:8px">BID-2201 · AI-filled form</div><h3>Northline Construction bid form (sample)</h3><p class="small muted">Highlighted fields were filled by the AI from the package and your final price. Review them, then approve. Nothing is submitted until you do.</p></div><span class="chip gold">Ready for approval</span></div>
      <div class="card" data-item>
        <div class="hl-field"><label class="f">Bidder legal name</label><input class="inp" value="IVO Serv Group"></div>
        <div class="hl-field"><label class="f">Project</label><input class="inp" value="Cedar Ridge Elementary modernization"></div>
        <div class="grid g2">
          <div class="hl-field"><label class="f">Base bid</label><input class="inp" value="$442,000"></div>
          <div class="hl-field"><label class="f">Calendar days to complete</label><input class="inp" value="90"></div>
        </div>
        <div class="hl-field"><label class="f">Addenda acknowledged</label><input class="inp" value="Addendum 1, Addendum 2"></div>
        <div class="hl-field"><label class="f">Bid bond</label><input class="inp" value="5% of the base bid, included"></div>
        <div class="field"><label class="f">Authorized signature (you)</label><input class="inp" value="Val, IVO Serv Group (sample)"></div>
        <div class="note" style="margin:12px 0">This is a preview. Approving queues the submission; the prototype does not send it to anyone.</div>
        <button class="btn lg" data-set="Approved to submit|ok" data-toast="Marked approved. The bid was not sent (prototype).">Approve and submit</button>
        <span class="chip" data-status hidden style="margin-left:8px"></span>
      </div>
    </section>"""

    won = """<section class="content app" data-screen="bidwon">
      <div class="row between wrap"><div><a class="tiny gold" href="#bidding">Back to pipeline</a><div class="eyebrow" style="margin-top:8px">BID-2175 · Won</div><h3>Lynnwood Courthouse doors</h3><p class="small muted">Awarded Nov 10, 2026. The bid became a job automatically, with the confirmed subs already assigned.</p></div><span class="chip ok">Won</span></div>
      <div class="card">
        <div class="row between"><div><b>JOB-2175</b><p class="small muted">Opened from the won bid. Document check still required before work can start.</p></div><a class="btn" href="#job">Open job timeline</a></div>
        <div class="list" style="margin-top:12px">
          <div class="li"><span class="grow">Pacific Openings LLC · doors and hardware · confirmed $38,400</span><span class="chip ok">Pre-assigned</span></div>
          <div class="li"><span class="grow">Cascade Electric · power to operators · confirmed $6,200</span><span class="chip ok">Pre-assigned</span></div>
        </div>
      </div>
    </section>"""

    lost = """<section class="content app" data-screen="bidlost">
      <div class="row between wrap"><div><a class="tiny gold" href="#bidding">Back to pipeline</a><div class="eyebrow" style="margin-top:8px">BID-2162 · Lost</div><h3>Boise City Hall roof</h3><p class="small muted">Result recorded so the pricing model can learn from it.</p></div><span class="chip bad">Lost</span></div>
      <div class="card">
        <dl class="kv"><dt>Our bid</dt><dd>$186,400</dd><dt>Awarded at</dt><dd>Not disclosed</dd><dt>Reason</dt><dd>Price - we were not the low bidder</dd><dt>What we learned</dt><dd>Markup on membrane roofing was high against recent local results. Flagged for the next similar bid.</dd></dl>
      </div>
    </section>"""
    return "\n".join([pipeline, pkg, subs, level, form, won, lost])


def integrations_screen():
    def card(title, blurb, status, cls):
        return (
            f'<div class="int-card card"><h3>{title}</h3>'
            f'<p class="small muted" style="margin:6px 0 10px">{blurb}</p>'
            f'<span class="chip {cls} status">{status}</span></div>'
        )
    cards = [
        ("Bid platforms and plan rooms",
         "Pull invitations, plans and addenda from outside bidding platforms and plan rooms. Each real connection needs your approval and that platform's API access.",
         "Available", "info"),
        ("Email import of bid invites",
         "A watched intake mailbox turns a forwarded invitation into a bid in Found, with attachments saved to the package.",
         "Connected sample", "ok"),
        ("Calendar",
         "Push bid due dates and job start windows to the staff calendar, and show sub availability you already confirmed.",
         "Available", "info"),
        ("Accounting",
         "Send awarded job costs and, later, invoices. No payments are processed at launch.",
         "Requires approval", "warn"),
        ("File storage",
         "Private storage for plans, specs and filled forms, with virus scanning and signed links.",
         "Connected sample", "ok"),
        ("Webhooks and API keys",
         "Let approved systems create bids, post sub responses and receive status changes. Keys are scoped and can be revoked.",
         "Requires approval", "warn"),
    ]
    body = "".join(card(*c) for c in cards)
    return f"""<section class="content app" data-screen="integrations">
      <div class="row between wrap"><div><h3>Integrations</h3><p class="small muted">Connect outside tools for bidding and the rest of the work. Sample statuses only - no live connections and no third-party names. Each real hookup needs your approval and that platform's API access.</p></div></div>
      <div class="int-grid">{body}</div>
      <div class="note" style="margin-top:16px">The prototype does not call any outside system. Connecting a real platform is a later, approved step.</div>
    </section>"""


def console_screens():
    why='''<div class="why"><div class="tiny muted" style="margin-bottom:4px">Why this contractor</div>
      <b>Bluewater Flooring LLC</b>
      <p class="small muted" style="margin:4px 0 8px">Rules, not an AI model: trade, region, documents and scorecard.</p>
      <span class="chip gold">Flooring + drywall</span><span class="chip gold">Pierce coverage</span><span class="chip ok">COI current</span><span class="chip ok">Score 4.7</span><span class="chip">Capacity 1 of 2 jobs</span>
    </div>'''
    overview=f'''<section class="content app" data-screen="overview">
      <div class="grid g4">
        <div class="metric glass"><div class="l">SLA hit, 7 days</div><div class="v">94%</div></div>
        <div class="metric glass"><div class="l">Open approvals</div><div class="v">5</div></div>
        <div class="metric glass"><div class="l">Bids due this week</div><div class="v">3</div></div>
        <div class="metric glass"><div class="l">At-risk timers</div><div class="v" style="color:var(--bad)">1</div></div>
      </div>
      <div class="board">
        <div class="col glass"><h3>Breach risk</h3>
          <a class="job-card" href="#job"><div class="row between"><b>Roof drain clog</b><span class="chip bad">18 min left</span></div><p class="tiny muted">Urgent · Harbor Point</p></a>
        </div>
        <div class="col glass"><h3>Waiting on IVO</h3>
          <a class="job-card" href="#approvals"><div class="row between"><b>Lobby LVP replacement</b><span class="chip gold">Approve award</span></div><p class="tiny muted">Standard · 3 bids to level</p></a>
          <a class="job-card" href="#triage"><div class="row between"><b>New inquiry, Tacoma</b><span class="chip gold">Confirm triage</span></div><p class="tiny muted">Rules: repair, plumbing</p></a>
        </div>
        <div class="col glass"><h3>On track</h3>
          <a class="job-card" href="#job"><div class="row between"><b>Unit 3B ceiling leak</b><span class="chip ok">On site</span></div><p class="tiny muted">Urgent · crew Tue 9:00 AM</p></a>
        </div>
      </div>
      <div class="row between"><h3>Coverage</h3><a class="btn sm line" href="#map">Open full map</a></div>
      {MAP}
      <div class="card"><div class="row between wrap"><div><h3>Bidding on outside contracts</h3><p class="small muted">AI reads the package, drafts sub confirmations and fills the bid form. Nothing leaves without your approval.</p></div><a class="btn" href="#bidding">Open bidding</a></div></div>
      <div class="later"><span class="chip later">Later</span> Payments and text messages stay out of the launch build.</div>
    </section>'''
    amap=f'''<section class="content app" data-screen="map">
      <p class="small muted">Job sites and in-network contractors across Washington, Oregon, Idaho and Northern California. Built with SVG only — no map vendor, no tracking.</p>
      {MAP}
      <div class="grid g3">
        <div class="card"><div class="eyebrow">Washington</div><b>4 active</b><p class="small muted">Tacoma, Lynnwood, Bellevue, plus Puget Sound coverage.</p></div>
        <div class="card"><div class="eyebrow">Oregon</div><b>2 contractors ready</b><p class="small muted">Portland metro coverage, no open jobs today.</p></div>
        <div class="card"><div class="eyebrow">Idaho &amp; Northern CA</div><b>Coverage only</b><p class="small muted">Boise and Redding are ready to route when a request lands.</p></div>
      </div>
    </section>'''
    triage=f'''<section class="content app" data-screen="triage">
      <div class="row between wrap"><p class="small muted">Keyboard: <span class="kbd">J</span> <span class="kbd">K</span> move · <span class="kbd">Enter</span> open · <span class="kbd">1</span> confirm. A person still confirms every type and path.</p><span class="chip">2 in queue</span></div>
      <div class="stack" id="triagelist">
        <article class="job-card sel" data-board-item data-item>
          <div class="row between wrap"><b>HVAC not cooling, medical office</b><span class="chip warn">Urgent</span></div>
          <p class="small muted">Tacoma inquiry · public form · 14 min ago</p>
          {why}
          <div class="row wrap" style="margin-top:10px">
            <span class="chip" data-status hidden></span>
            <button class="btn sm" data-set="Confirmed → REQ-1058|ok" data-toast="Created REQ-1058. Routing suggestion added to the Approval inbox." data-open>Confirm type</button>
            <a class="btn sm line" href="#job">Open timeline</a>
            <button class="btn sm ghost" data-modal="#editTriage">Edit</button>
          </div>
        </article>
        <article class="job-card" data-board-item data-item>
          <div class="row between wrap"><b>Lobby lighting, evening work</b><span class="chip">Standard</span></div>
          <p class="small muted">Bellevue · email intake · today 4:02 PM PT</p>
          <div class="why"><div class="tiny muted">Why these contractors</div><span class="chip gold">Electrical</span><span class="chip gold">King County</span><span class="chip ok">All COIs current</span><span class="chip">3 to invite, then you approve</span></div>
          <div class="row wrap" style="margin-top:10px"><span class="chip" data-status hidden></span><button class="btn sm" data-set="Confirmed → REQ-1057|ok" data-toast="Created REQ-1057.">Confirm type</button><button class="btn sm ghost" data-modal="#editTriage">Edit</button></div>
        </article>
      </div>
      <div class="modal" id="editTriage"><div class="box"><h3>Edit triage</h3><p class="small muted" style="margin:8px 0">Type, trade and urgency — a person decides, rules only suggest.</p>
        <div class="opts" data-multi><button class="on">HVAC</button><button>Electrical</button><button>Plumbing</button></div>
        <div class="row" style="margin-top:12px"><button class="btn sm" data-close data-toast="Triage updated (prototype)">Save</button><button class="btn sm line" data-close>Cancel</button></div>
      </div></div>
    </section>'''
    approvals='''<section class="content app" data-screen="approvals">
      <p class="small muted">Everything that reaches a customer or contractor waits here. One primary action per row.</p>
      <div class="stack">
        <div class="card" data-item><div class="row between wrap"><div><span class="chip gold">Change order</span> <b>CO-2 on REQ-1042 · +$620</b><p class="small muted">Maya Ortiz already approved in the app. New NTE $4,970.</p></div><span class="chip warn" data-status>Needs IVO</span></div><div class="primary-slot"><button class="btn" data-set="Approved|ok" data-toast="Change order approved.">Approve change order</button></div></div>
        <div class="card" data-item><div class="row between wrap"><div><span class="chip">Bid invitations</span> <b>REQ-1051 · Lobby LED · invite 3 electricians</b></div><span class="chip warn" data-status>Waiting</span></div><div class="primary-slot"><button class="btn" data-set="Invites queued|ok" data-toast="Invites will send after you approve (prototype).">Approve invites</button></div></div>
        <div class="card" data-item><div class="row between wrap"><div><span class="chip">Template email</span> <b>REQ-1053 · “Crew dispatched”</b></div><span class="chip warn" data-status>Waiting</span></div><div class="primary-slot"><button class="btn" data-set="Send approved|ok" data-toast="Marked approved. Nothing was sent.">Approve send</button></div></div>
        <div class="card" data-item><div class="row between wrap"><div><span class="chip gold">Sub outreach</span> <b>BID-2201 · 2 confirmation drafts</b><p class="small muted">Ask Harbor Air and a follow-up to Metro Drywall to confirm price, dates and capacity. Nothing sends until you approve.</p></div><span class="chip warn" data-status>Waiting</span></div><div class="primary-slot"><a class="btn" href="#bidsubs">Review drafts</a></div></div>
        <div class="card" data-item><div class="row between wrap"><div><span class="chip gold">Bid submission</span> <b>BID-2201 · Cedar Ridge Elementary · $442,000</b><p class="small muted">AI-filled bid form is ready. Submit waits on your approval.</p></div><span class="chip warn" data-status>Waiting</span></div><div class="primary-slot"><a class="btn" href="#bidform">Review form</a></div></div>
      </div>
    </section>'''
    requests='''<section class="content app" data-screen="requests">
      <div class="row wrap" data-filter-group="#rtable" style="margin-bottom:8px"><button class="btn sm" data-f="all">All</button><button class="btn sm line" data-f="urgent">Urgent</button><button class="btn sm line" data-f="standard">Standard</button></div>
      <div class="card pad0 tscroll"><table class="t" id="rtable"><thead><tr><th>Request</th><th>Customer</th><th>Tier</th><th>Status</th></tr></thead><tbody>
        <tr data-f="urgent"><td><a href="#job">REQ-1042 · Ceiling leak, Unit 3B</a></td><td>Harborline</td><td>Urgent</td><td><span class="chip ok">On site</span></td></tr>
        <tr data-f="urgent"><td>REQ-1053 · Roof drain clog</td><td>Harbor Point</td><td>Urgent</td><td><span class="chip bad">Timer at risk</span></td></tr>
        <tr data-f="standard"><td>REQ-1051 · Lobby LED retrofit</td><td>Cedar Court</td><td>Standard</td><td><span class="chip">Bidding</span></td></tr>
      </tbody></table></div>
    </section>'''
    job=f'''<section class="content app" data-screen="job">
      <div class="grid g2" style="align-items:start">
        <div class="stack">
          <div class="card"><div class="row between"><div><div class="eyebrow">REQ-1042</div><h3>Ceiling leak, drywall &amp; paint</h3><p class="small muted">Cedar Court Apartments, Unit 3B · Tacoma, Pierce County</p></div><span class="chip ok">On site</span></div>
            <div class="countdown" data-sla="182" data-warn="60"><span class="tiny muted">Written plan due</span><span class="v">—</span></div>
          </div>
          <div class="card"><h3 style="margin-bottom:10px">Live timeline</h3>{timeline()}</div>
        </div>
        <div class="stack">
          {why}
          <div class="card"><div class="eyebrow">Primary action</div><a class="btn block" href="#approvals">Review CO-2 · +$620</a><p class="tiny muted" style="margin-top:8px">Maya already approved. This is the IVO confirmation.</p></div>
          <div class="card"><div class="row between"><span>NTE</span><b>$4,800</b></div><div class="prog warn" style="margin:8px 0"><i style="width:91%"></i></div><p class="tiny muted">Quote $4,350 · CO-2 +$620 pending</p></div>
        </div>
      </div>
    </section>'''
    bids='''<section class="content app" data-screen="bids">
      <div class="card"><div class="row between"><b>REQ-1051 · Lobby LED retrofit</b><span class="chip">3 invites drafted</span></div><p class="small muted">Deadline Fri Nov 20, 5:00 PM PT. Duplicate check: no matching open package.</p><div class="primary-slot" style="margin-top:10px"><a class="btn" href="#bid">Open packet</a></div></div>
      <p class="small muted" style="margin-top:12px">This is IVO inviting contractors onto a customer job. For IVO bidding as a subcontractor on an outside contract, use <a class="gold" href="#bidding">Bidding</a>.</p>
    </section>'''
    bid='''<section class="content app" data-screen="bid">
      <div class="card"><h3>Packet · REQ-1051</h3><p class="small muted">Scope, photos, files and a hard deadline — a packet cannot go out without all four.</p>
        <div class="list"><div class="li"><span class="dot ok"></span>Scope attached</div><div class="li"><span class="dot ok"></span>3 files, virus-scanned</div><div class="li"><span class="dot ok"></span>Deadline + time zone set</div><div class="li"><span class="dot warn"></span>Invites wait in Approvals</div></div>
        <a class="btn" href="#approvals" style="margin-top:12px">Send to approvals</a>
      </div>
    </section>'''
    contractors='''<section class="content app" data-screen="contractors">
      <div class="card pad0 tscroll"><table class="t" id="ctable"><thead><tr><th>Company</th><th>Trades</th><th>Coverage</th><th>Docs</th><th></th></tr></thead><tbody>
        <tr><td><a href="#contractor">Bluewater Flooring LLC</a></td><td>Flooring, drywall</td><td>King, Pierce</td><td><span class="chip ok">Current</span></td><td><span class="chip">Score 4.7</span></td></tr>
        <tr><td>Evergreen Restoration Co.</td><td>Water, rebuild</td><td>King, Snohomish</td><td><span class="chip ok">Current</span></td><td><span class="chip">Score 4.8</span></td></tr>
        <tr><td>Cascade Electric</td><td>Electrical</td><td>Multnomah</td><td><span class="chip warn">COI in 21 days</span></td><td><span class="chip">Score 4.5</span></td></tr>
      </tbody></table></div>
    </section>'''
    contractor=f'''<section class="content app" data-screen="contractor">
      <div class="card"><div class="row between"><h3>Bluewater Flooring LLC</h3><span class="chip ok">Ready for routing</span></div>
        <p class="small muted">Sam Rivera · flooring &amp; drywall · King, Pierce · trial first job completed.</p>
        {why}
        <p class="small" style="margin-top:10px">Joined by invite after staff vetting (option A). First job was a watched trial.</p>
      </div>
    </section>'''
    applications='''<section class="content app" data-screen="applications">
      <div class="note">Approved join process: contractors are invite-only after staff vetting, with a watched trial first job. The Partner with IVO form lands in Triage; staff decide whether to invite.</div>
      <div class="card" style="margin-top:12px" data-item>
        <div class="row between"><div><b>Invite Bluewater Flooring LLC</b><p class="small muted">Staff-vetted · Partner with IVO inquiry, Triage #104</p></div><span class="chip" data-status hidden></span></div>
        <button class="btn" style="margin-top:10px" data-set="Invite sent|ok" data-toast="Invite marked sent (prototype).">Send invite</button>
      </div>
    </section>'''
    team='''<section class="content app" data-screen="team">
      <div class="card"><h3>Role matrix</h3><p class="small muted">Still open: who besides the owner can approve a contractor or a new customer workspace, and naming a second admin.</p>
        <table class="t"><thead><tr><th>Role</th><th>Can approve routing</th><th>Can approve contractors</th></tr></thead><tbody>
          <tr><td>Owner</td><td>Yes</td><td>Yes</td></tr>
          <tr><td>Admin</td><td>Yes, if named</td><td>To be decided</td></tr>
          <tr><td>Coordinator</td><td>Draft only</td><td>No</td></tr>
        </tbody></table>
      </div>
    </section>'''
    # wrap each section as data-screen inside one router - already in console_chrome via inner
    inner = "\n".join([overview,amap,triage,approvals,requests,job,bidding_screens(),bids,bid,contractors,contractor,applications,integrations_screen(),team])
    # console_chrome already has data-router on main, but each section needs to be a screen inside it. show() looks for [data-screen] inside [data-router]. Good.
    # But I used class "content app" and data-screen - CSS .app[data-screen]{display:none} and .on{display:flex}. For desktop I need them to display as block when on. The .app[data-screen].on{display:flex} + .content{padding... flex-direction column} works if display:flex and flex-direction column.
    body = console_chrome("Today at IVO", "overview", inner)
    # Fix: all screens start hidden; JS show() will add .on. Need a default - JS runs show() on hash or first screen.
    return shell("Staff console", body, cmds=CM_CON+[("Go to V02 home","../index.html","Home")])

print("index+console defs ok")

def tabs_customer(active="Home"):
    items=[("Home","#home","home job requests"),("Requests","#requests","requests submitted"),("New","#new","new","fab"),("Files","#docs","docs"),("Account","#account","account users invoices")]
    # fix structure
    pass

def tabbar(items, active):
    # items: (label, href, match, kind?)
    out=[]
    for it in items:
        label,href,match=it[0],it[1],it[2]
        kind=it[3] if len(it)>3 else ""
        cls=" active" if label==active else ""
        inner=f'<span class="fab">+</span>{label}' if kind=="fab" else label
        out.append(f'<a class="{cls.strip()}" href="{href}" data-match="{match}">{inner}</a>')
    return '<nav class="tabbar" aria-label="Main">'+"".join(out)+"</nav>"

CUS_TABS=[("Home","#home","home job"),("Requests","#requests","requests submitted"),("New","#new","new","fab"),("Files","#docs","docs"),("Account","#account","account users invoices")]
KON_TABS=[("Jobs","#jobs","jobs job punch co closeout"),("Opps","#opps","opps opp bid bid-sent bidconfirm"),("Check in","#checkin","checkin"),("Docs","#compliance","compliance"),("Profile","#profile","profile payouts signin")]

def phone(index_html, screens_html, notes_html):
    return f'''<div class="phone-page" id="main">
<nav class="phone-index" aria-label="Screens">{index_html}</nav>
<div class="phone"><div class="notch"></div><div data-router>
{screens_html}
</div></div>
<aside class="phone-notes">{notes_html}</aside>
</div>'''

def page_customer():
    idx='''
  <div class="eyebrow">Customer app · phone</div><h1>Harborline Property Group</h1><p class="small muted">Signed in as Maya Ortiz (sample), org admin.</p>
  <div class="grp">Getting in</div><a class="nav" href="#invite">1 · Invitation</a><a class="nav" href="#signin">2 · Sign in with email code</a>
  <div class="grp">Everyday</div><a class="nav" href="#home">3 · Home &amp; what’s happening now</a><a class="nav" href="#new">4 · New request wizard</a><a class="nav" href="#submitted">5 · Request sent</a><a class="nav" href="#emergency">6 · Emergency button</a><a class="nav" href="#emergency-sent">7 · Emergency in progress</a>
  <div class="grp">Jobs</div><a class="nav" href="#requests">8 · All requests</a><a class="nav" href="#job">9 · Job tracker</a><a class="nav" href="#approve">10 · Approve change order</a><a class="nav" href="#closeout">11 · Closeout &amp; sign-off</a>
  <div class="grp">Account</div><a class="nav" href="#docs">12 · Documents</a><a class="nav" href="#invoices">13 · Invoices (Later)</a><a class="nav" href="#users">14 · Company users</a><a class="nav" href="#account">15 · Account</a>
  <p style="margin-top:16px"><a class="btn line sm" href="../customer-portal/index.html">Desktop portal view →</a></p>
'''
    tb=lambda a: tabbar(CUS_TABS,a)
    screens=f'''
<section class="app" data-screen="invite"><div class="app-b np"><div class="stack" style="padding:28px 22px;min-height:100%;background:linear-gradient(180deg,#061d2a,#0c2938);color:#eef3f6">
  <img src="../assets/img/ivo-mark-white.png" alt="IVO" style="width:52px;margin-top:24px">
  <div class="eyebrow" style="color:#e1c395;margin-top:auto">You're invited</div>
  <h2>Your IVO workspace is ready.</h2>
  <p class="small" style="color:#cfdbe3">Dana Whitfield invited <b>maya.ortiz@harborline.example</b> to Harborline Property Group after reviewing your Cedar Court request.</p>
  <a class="btn lg block" href="#signin">Accept invitation</a>
  <p class="tiny" style="color:#8fa4b2;text-align:center">Invite-only. No password — a code is emailed to you.</p>
</div></div></section>

<section class="app" data-screen="signin"><div class="app-b" style="padding:48px 22px">
  <img src="../assets/img/ivo-mark-navy.png" alt="IVO" style="width:48px;margin:0 auto 16px;filter:none">
  <h2 style="text-align:center">Check your email</h2>
  <p class="small muted" style="text-align:center;margin:8px 0 16px">We sent a 6-digit code to maya.ortiz@harborline.example</p>
  <div class="otp" id="cotp" data-then="#home"><input inputmode="numeric" aria-label="Digit 1"><input inputmode="numeric" aria-label="Digit 2"><input inputmode="numeric"><input inputmode="numeric"><input inputmode="numeric"><input inputmode="numeric"></div>
  <button class="btn block" style="margin-top:18px" data-fill-otp="#cotp">Use sample code 204816</button>
</div></section>

<section class="app" data-screen="home"><header class="app-h"><img src="../assets/img/ivo-mark-navy.png" alt="" style="width:22px;height:22px"><div class="grow"><b>Good evening, Maya</b><div class="tiny muted">Harborline Property Group</div></div><span class="chip offline">Offline-ready</span></header>
<div class="app-b">
  <div class="now-card">
    <div class="eyebrow">What’s happening now</div>
    <h3>Unit 3B ceiling leak</h3>
    <p class="small muted">Cedar Court · crew is on site</p>
    {FLASH}
    <div class="countdown" data-sla="182" data-warn="60" style="margin-top:12px"><span class="tiny muted">Next update due</span><span class="v">—</span></div>
    <a class="btn block" style="margin-top:12px" href="#approve">Approve change order · +$620</a>
  </div>
  <div class="row between" style="margin:16px 0 8px"><h3>Also open</h3><a class="tiny gold" href="#requests">All requests</a></div>
  <a class="card" href="#job" style="display:block"><div class="row between"><b>REQ-1059 · Hallway ceiling</b><span class="chip">Scheduled</span></div><p class="tiny muted">Mon 8:00 AM · Bldg B</p></a>
</div>{tb("Home")}</section>

<section class="app" data-screen="new"><header class="app-h"><a href="#home">‹</a><h2>New request</h2></header>
<div class="app-b" data-wizard data-finish="submitted" data-reset>
  <div class="row between"><span class="tiny muted" data-count></span><span class="tiny gold" data-step-label></span></div><div class="steps" style="margin:8px 0 14px"></div>
  <div class="wstep" data-label="Where"><h3>Where is the work?</h3><div class="field"><label class="f">Property</label><input class="inp" value="Cedar Court Apartments (sample)"></div><div class="field"><label class="f">Exact location</label><input class="inp" value="Bldg B Unit 7 hallway"></div></div>
  <div class="wstep" data-label="Trade"><h3>What kind of work?</h3><div class="opts" data-multi><button class="on">Drywall</button><button class="on">Paint</button><button>Plumbing</button><button>Electrical</button><button>HVAC</button><button>Flooring</button></div></div>
  <div class="wstep" data-label="Urgency"><h3>How urgent?</h3><div class="opts"><button>Emergency</button><button>Urgent</button><button class="on">Standard</button></div></div>
  <div class="wstep" data-label="Scope"><h3>Describe the work</h3><textarea class="inp" rows="4">Hallway ceiling stain after a supply-line leak. About 4 sq ft. Unit above already repaired.</textarea></div>
  <div class="wstep" data-label="Budget"><h3>Not-to-exceed</h3><div class="field"><label class="f">NTE amount</label><input class="inp" value="2500" inputmode="numeric"></div><p class="tiny muted">IVO will ask before going over this number.</p></div>
  <div class="wstep" data-label="Photos"><h3>Photos</h3><button class="drop" data-add-thumb="#cthumbs">📷 Add photos</button><div class="thumbs" id="cthumbs" style="margin-top:10px"></div></div>
  <div class="wstep" data-label="Files"><h3>Files</h3><button class="drop" data-add-file="#cfiles">⇪ Add files</button><div class="stack s8" id="cfiles" style="margin-top:10px"><div class="file"><span class="ic">PDF</span><span class="grow">Building B floor plan_sample.pdf</span><span class="chip ok">Uploaded</span></div></div></div>
  <div class="wstep" data-label="Review"><h3>Review &amp; send</h3><div class="sheet"><dl class="kv" style="grid-template-columns:90px 1fr"><dt>Where</dt><dd>Cedar Court, Bldg B Unit 7 hallway</dd><dt>Trade</dt><dd>Drywall &amp; paint</dd><dt>Urgency</dt><dd>Standard</dd><dt>NTE</dt><dd>$2,500</dd></dl></div><div class="note" style="margin-top:12px">An IVO coordinator reviews this, then invites a verified contractor. You’ll see every step here.</div></div>
  <div class="row" style="margin-top:18px"><button class="btn line" data-prev>Back</button><button class="btn grow" data-next data-last-label="Send request">Continue</button></div>
</div>{tb("New")}</section>

<section class="app" data-screen="submitted"><div class="app-b" style="padding:40px 22px;text-align:center">
  <div class="eyebrow">Sent</div><h2>Request received</h2><p class="small muted" style="margin:10px 0 18px">REQ-1059 is with an IVO coordinator. Updates will show here and by email until you were already invited — you are signed in, so they appear in this app.</p>
  <a class="btn block" href="#home">Back to home</a>
</div>{tb("Home")}</section>

<section class="app" data-screen="emergency"><header class="app-h"><a href="#home">‹</a><h2>Emergency</h2></header>
<div class="app-b">
  <p class="small muted" style="margin-bottom:14px">Press and hold to reach IVO now. This is for active leaks, no power, or an unsafe condition — not for a standard request.</p>
  <button class="emerg" type="button" data-hold="emergency-sent"><span class="hl">Hold to reach IVO now</span><small>Takes about one second. You can still add a photo next.</small></button>
  <button class="drop" style="margin-top:16px" data-add-thumb="#ethumbs">📷 Add a photo (optional)</button>
  <div class="thumbs" id="ethumbs" style="margin-top:10px"></div>
</div>{tb("Home")}</section>

<section class="app" data-screen="emergency-sent"><div class="app-b" style="padding:36px 22px">
  <span class="chip bad">Emergency in progress</span>
  <h2 style="margin-top:10px">IVO has your alert.</h2>
  <p class="small muted">A coordinator is being reached. Keep your phone nearby. You’ll see the job appear on Home as soon as it is opened.</p>
  <div class="countdown" data-sla="8" data-warn="15" style="margin:16px 0"><span class="tiny muted">Target first answer</span><span class="v">—</span></div>
  <a class="btn block" href="#home">Back to home</a>
</div>{tb("Home")}</section>

<section class="app" data-screen="requests"><header class="app-h"><h2>Requests</h2></header>
<div class="app-b"><div class="stack">
  <a class="card" href="#job"><div class="row between"><b>REQ-1042 · Unit 3B ceiling leak</b><span class="chip ok">On site</span></div><p class="tiny muted">Cedar Court · needs your approval on CO-2</p></a>
  <a class="card" href="#job"><div class="row between"><b>REQ-1059 · Hallway ceiling</b><span class="chip">Scheduled</span></div></a>
</div></div>{tb("Requests")}</section>

<section class="app" data-screen="job"><header class="app-h"><a href="#home">‹</a><h2>REQ-1042</h2><span class="chip offline">Saved on this phone</span></header>
<div class="app-b">
  <h3>Ceiling leak, Unit 3B</h3>
  {FLASH}
  <div class="countdown" data-sla="182" data-warn="60" style="margin:12px 0"><span class="tiny muted">Next update due</span><span class="v">—</span></div>
  {timeline()}
  <a class="btn block" style="margin-top:14px" href="#approve">Approve change order · +$620</a>
</div>{tb("Home")}</section>

<section class="app" data-screen="approve"><header class="app-h"><a href="#job">‹</a><h2>Change order</h2></header>
<div class="app-b" data-item>
  <div class="now-card">
    <div class="eyebrow">Needs your approval</div>
    <h3>Sister a ceiling joist · +$620</h3>
    <p class="small muted">Original NTE $4,800 · new total $4,970. Photos attached.</p>
    <div class="thumbs" style="margin:10px 0"><div class="thumb" style="background-image:url(../assets/img/ivo-36.webp)"><span>sample</span></div><div class="thumb" style="background-image:url(../assets/img/ivo-05.webp)"><span>sample</span></div></div>
    <button class="btn lg block" data-set="Approved|ok" data-toast="Approved. IVO has been notified (prototype)." data-hide-on-set>Approve +$620</button>
    <div data-done hidden class="note" style="margin-top:12px">Approved. The crew can continue. IVO still confirms on their side.</div>
    <button class="btn line block" style="margin-top:8px" data-toast="Question sent to IVO (prototype).">Ask a question</button>
  </div>
</div>{tb("Home")}</section>

<section class="app" data-screen="closeout"><header class="app-h"><a href="#job">‹</a><h2>Sign off</h2></header>
<div class="app-b" data-item>
  <p class="small muted">Before and after photos, punch complete. Sign to close REQ-1042.</p>
  <div class="thumbs" style="margin:12px 0"><div class="thumb" style="background-image:url(../assets/img/ivo-51.webp)"><span>before</span></div><div class="thumb" style="background-image:url(../assets/img/ivo-76.webp)"><span>after</span></div></div>
  <button class="btn lg block" data-set="Signed off|ok" data-toast="Signed off (prototype).">Sign off</button>
  <span class="chip" data-status hidden style="margin-top:10px"></span>
</div>{tb("Home")}</section>

<section class="app" data-screen="docs"><header class="app-h"><h2>Documents</h2></header>
<div class="app-b"><div class="file"><span class="ic">PDF</span><span class="grow">REQ-1042 closeout package (sample)</span></div></div>{tb("Files")}</section>

<section class="app" data-screen="invoices"><header class="app-h"><h2>Invoices</h2></header>
<div class="app-b"><div class="later"><span class="chip later">Later</span> Invoices and payments are out of launch scope. You’ll still see the approved amounts on each job.</div></div>{tb("Account")}</section>

<section class="app" data-screen="users"><header class="app-h"><h2>Company users</h2></header>
<div class="app-b"><div class="list"><div class="li"><span class="grow">Maya Ortiz · admin</span><span class="chip">You</span></div><div class="li"><span class="grow">Jordan Lee · requester</span></div></div><p class="tiny muted" style="margin-top:10px">IVO confirms every colleague invite.</p></div>{tb("Account")}</section>

<section class="app" data-screen="account"><header class="app-h"><h2>Account</h2></header>
<div class="app-b"><p><b>Maya Ortiz</b></p><p class="small muted">maya.ortiz@harborline.example · Harborline Property Group</p>
<p class="small" style="margin-top:12px">Workspace opened after IVO reviewed your request (option 1).</p>
<div class="row" style="margin-top:16px"><button class="btn line sm" data-theme-toggle>Light / dark</button></div>
</div>{tb("Account")}</section>
'''
    notes='''
<div class="notes-card glass" data-note="home job approve"><h3>Designed to be obvious</h3><ul><li>Home opens on the one job that needs you.</li><li>Status is five steps you can read in about three seconds.</li><li>Approving a change order is one primary tap.</li><li>The app stays usable if the signal drops (offline-ready badge).</li></ul></div>
<div class="notes-card glass" data-note="emergency emergency-sent" hidden><h3>Emergency is still press-and-hold</h3><p class="small muted">A long press avoids pocket taps. The keyboard still has a fallback.</p></div>
<div class="notes-card glass" data-note="invite signin new submitted" hidden><h3>Invite-only, request first</h3><p class="small muted">New customers send a request, then IVO invites them (option 1, approved 13 Nov 2026).</p></div>
'''
    body=phone(idx,screens,notes)
    head='<link rel="manifest" href="manifest.webmanifest">'
    return shell("Customer app", body, cmds=CM_CUS+[("Desktop portal","../customer-portal/index.html","Same workspace")], head=head)

print("customer def ok")

def portal_chrome(kind, title, nav, inner, cmds):
    # kind: customer|vendor
    mark = "CUSTOMER PORTAL" if kind=="customer" else "VENDOR PORTAL"
    app = "../customer/index.html" if kind=="customer" else "../contractor/index.html"
    return f'''
<div class="shell">
  <aside class="side">
    <div class="brand"><img src="../assets/img/ivo-mark-white.png" alt=""><div><b>IVO</b><span>{mark} · V02</span></div></div>
    {nav}
    <div class="hint">Type <span class="kbd">⌘K</span> to search. Same workspace as the phone app.</div>
    <a class="nav" href="{app}">Phone app →</a>
  </aside>
  <div class="main" id="main" data-router>
    <div class="topb"><button class="menu-btn" type="button" aria-label="Open menu">☰</button>
      <h2>{title}</h2>
      <button class="search-pill grow" type="button" data-cmd-open>Search this workspace… <span class="kbd">⌘K</span></button>
      <span class="chip offline">Offline-ready</span>
    </div>
    {inner}
  </div>
</div>
'''

def page_customer_portal():
    nav='''
    <a class="nav active" href="#dashboard" data-match="dashboard">Home</a>
    <a class="nav" href="#requests" data-match="requests">Requests</a>
    <a class="nav" href="#job" data-match="job">Job timeline</a>
    <a class="nav" href="#new" data-match="new">New request</a>
    <a class="nav" href="#approvals" data-match="approvals">Approvals</a>
    <a class="nav" href="#documents" data-match="documents">Documents</a>
    <a class="nav" href="#properties" data-match="properties">Properties</a>
    <a class="nav" href="#users" data-match="users">Users</a>
    <a class="nav" href="#invoices" data-match="invoices">Invoices (Later)</a>
    '''
    inner=f'''
<section class="content app" data-screen="dashboard">
  <div class="now-card">
    <div class="eyebrow">What’s happening now</div>
    <div class="row between wrap"><h3>Unit 3B ceiling leak</h3><span class="chip ok">On site</span></div>
    {FLASH}
    <div class="countdown" data-sla="182" data-warn="60" style="margin-top:12px"><span class="tiny muted">Next update due</span><span class="v">—</span></div>
    <a class="btn" style="margin-top:12px" href="#approvals">Approve change order · +$620</a>
  </div>
  <div class="grid g3" style="margin-top:8px">
    <div class="metric glass"><div class="l">Open requests</div><div class="v">2</div></div>
    <div class="metric glass"><div class="l">Waiting on you</div><div class="v">1</div></div>
    <div class="metric glass"><div class="l">Properties</div><div class="v">4</div></div>
  </div>
</section>
<section class="content app" data-screen="requests">
  <div class="card pad0"><table class="t"><thead><tr><th>Request</th><th>Property</th><th>Status</th></tr></thead><tbody>
    <tr><td><a href="#job">REQ-1042 · Unit 3B ceiling leak</a></td><td>Cedar Court</td><td><span class="chip ok">On site</span></td></tr>
    <tr><td>REQ-1059 · Hallway ceiling</td><td>Cedar Court Bldg B</td><td><span class="chip">Scheduled</span></td></tr>
  </tbody></table></div>
</section>
<section class="content app" data-screen="job">
  <div class="card"><div class="row between"><h3>REQ-1042 · Ceiling leak</h3><span class="chip ok">On site</span></div>{FLASH}{timeline()}<a class="btn" style="margin-top:12px" href="#approvals">Approve change order · +$620</a></div>
</section>
<section class="content app" data-screen="new">
  <div class="card" data-wizard data-finish="requests">
    <div class="row between"><span class="tiny muted" data-count></span><span class="tiny gold" data-step-label></span></div><div class="steps" style="margin:8px 0"></div>
    <div class="wstep" data-label="Where"><h3>Where?</h3><div class="field"><label class="f">Property</label><input class="inp" value="Cedar Court Apartments"></div></div>
    <div class="wstep" data-label="Trade"><h3>Trade</h3><div class="opts" data-multi><button class="on">Drywall</button><button class="on">Paint</button></div></div>
    <div class="wstep" data-label="Details"><h3>Scope &amp; NTE</h3><textarea class="inp" rows="3">Hallway ceiling stain, about 4 sq ft.</textarea><div class="field" style="margin-top:8px"><label class="f">NTE</label><input class="inp" value="2500"></div>
      <button class="drop" data-add-thumb="#pthumbs" style="margin-top:8px">📷 Photos</button><div class="thumbs" id="pthumbs" style="margin-top:8px"></div>
      <button class="drop" data-add-file="#pfiles" style="margin-top:8px">⇪ Files</button><div id="pfiles" class="stack s8" style="margin-top:8px"></div>
    </div>
    <div class="row" style="margin-top:12px"><button class="btn line" data-prev>Back</button><button class="btn grow" data-next data-last-label="Send request">Continue</button></div>
  </div>
</section>
<section class="content app" data-screen="approvals">
  <div class="card" data-item>
    <div class="eyebrow">Needs your approval</div>
    <h3>CO-2 · sister a joist · +$620</h3>
    <p class="small muted">New total $4,970 vs original NTE $4,800.</p>
    <button class="btn lg" data-set="Approved|ok" data-toast="Approved (prototype)." data-hide-on-set>Approve +$620</button>
    <div data-done hidden class="note" style="margin-top:10px">Approved. IVO still confirms.</div>
    <span class="chip" data-status hidden></span>
  </div>
</section>
<section class="content app" data-screen="documents">
  <div class="file"><span class="ic">PDF</span><span class="grow">REQ-1042 closeout package (sample)</span></div>
</section>
<section class="content app" data-screen="properties">
  <div class="card"><b>Cedar Court Apartments</b><p class="small muted">410 Sample Ave, Tacoma WA · 4 open or recent jobs</p></div>
</section>
<section class="content app" data-screen="users">
  <div class="list"><div class="li"><span class="grow">Maya Ortiz · admin</span></div><div class="li"><span class="grow">Jordan Lee · requester</span></div></div>
</section>
<section class="content app" data-screen="invoices">
  <div class="later" id="cinv"><span class="chip later">Later</span> Invoices and payments are out of launch scope.</div>
</section>
'''
    body=portal_chrome("customer","Harborline Property Group",nav,inner,CM_CUS)
    return shell("Customer portal", body, cmds=CM_CUS+[("Phone app","../customer/index.html#home","Same workspace")])

def page_contractor():
    idx='''
  <div class="eyebrow">Contractor app · phone</div><h1>Bluewater Flooring LLC</h1><p class="small muted">Signed in as Sam Rivera (sample), owner.</p>
  <div class="grp">Getting in</div><a class="nav" href="#signin">1 · Sign in</a>
  <div class="grp">Work</div><a class="nav" href="#opps">2 · Opportunities</a><a class="nav" href="#opp">3 · Packet</a><a class="nav" href="#bid">4 · Submit a bid</a><a class="nav" href="#bid-sent">5 · Bid sent</a><a class="nav" href="#bidconfirm">6 · Bid confirmation request</a>
  <div class="grp">On site</div><a class="nav" href="#jobs">7 · My jobs &amp; schedule</a><a class="nav" href="#job">8 · Job</a><a class="nav" href="#checkin">9 · Camera check-in</a><a class="nav" href="#punch">10 · Punch list</a><a class="nav" href="#co">11 · Change-order request</a><a class="nav" href="#closeout">12 · Closeout</a>
  <div class="grp">Company</div><a class="nav" href="#compliance">13 · Compliance</a><a class="nav" href="#payouts">14 · Earnings (tracking only)</a><a class="nav" href="#profile">15 · Company &amp; crew</a>
  <p style="margin-top:16px"><a class="btn line sm" href="../vendor-portal/index.html">Desktop portal view →</a></p>
'''
    tb=lambda a: tabbar(KON_TABS,a)
    screens=f'''
<section class="app" data-screen="signin"><div class="app-b" style="padding:48px 22px">
  <img src="../assets/img/ivo-mark-navy.png" alt="IVO" style="width:48px;margin:0 auto 16px">
  <h2 style="text-align:center">Check your email</h2>
  <p class="small muted" style="text-align:center;margin:8px 0 16px">Code sent to sam@bluewater.example</p>
  <div class="otp" id="kotp" data-then="#opps"><input inputmode="numeric"><input inputmode="numeric"><input inputmode="numeric"><input inputmode="numeric"><input inputmode="numeric"><input inputmode="numeric"></div>
  <button class="btn block" style="margin-top:18px" data-fill-otp="#kotp">Use sample code 204816</button>
</div></section>

<section class="app" data-screen="opps"><header class="app-h"><div class="grow"><b>Opportunities</b><div class="tiny muted">Swipe right to accept, left to decline</div></div><span class="chip offline">Offline-ready</span></header>
<div class="app-b">
  <div class="card" style="margin-bottom:12px">
    <div class="eyebrow">Earnings &amp; pipeline</div>
    <div class="row between"><div><div class="tiny muted">This month (tracking)</div><b style="font-size:22px">$6,430</b></div><div style="text-align:right"><div class="tiny muted">In pipeline</div><b>$2,500</b></div></div>
    <p class="tiny muted" style="margin-top:8px">Tracking only — payouts are not in the launch build. <span class="chip later">Later</span></p>
  </div>
  <a class="card" href="#bidconfirm" style="display:block;margin-bottom:12px">
    <div class="row between"><div class="eyebrow">Needs a reply</div><span class="chip gold">Bid confirmation</span></div>
    <h3 style="margin-top:4px">Cedar Ridge Elementary · flooring</h3>
    <p class="small muted">Confirm $86,400, dates Nov 30, 2026-Jan 15, 2027, and capacity if IVO is awarded.</p>
  </a>
  <div class="swipe-deck">
    <article class="swipe-card" data-swipe data-swipe-yes="Accepted. Opening the packet." data-swipe-no="Declined (prototype)." data-go-yes="opp">
      <span class="swipe-hint yes">ACCEPT</span><span class="swipe-hint no">DECLINE</span>
      <div class="row between"><h3>Hallway ceiling repair</h3><span class="chip gold">Direct offer</span></div>
      <p class="small muted">Tacoma (Pierce) · drywall &amp; paint · NTE $2,500</p>
      <div class="row wrap" style="margin-top:8px"><span class="chip">3 files</span><span class="chip">2 photos</span><span class="chip info">Respond by Fri Nov 20, 5:00 PM PT</span></div>
      <div class="row" style="margin-top:14px"><a class="btn grow" href="#opp">Review packet</a></div>
    </article>
  </div>
  <p class="tiny muted" style="margin-top:10px">Prefer buttons? Open the packet and use Accept there. Address is hidden until you accept.</p>
</div>{tb("Opps")}</section>

<section class="app" data-screen="opp"><header class="app-h"><a href="#opps">‹</a><h2>Packet</h2></header>
<div class="app-b">
  <h3>Hallway ceiling repair</h3>
  <p class="small muted">REQ-1059 · Cedar Court Bldg B · exact address after you accept</p>
  <div class="list"><div class="li"><span class="dot ok"></span>Scope, 3 files, 2 photos</div><div class="li"><span class="dot ok"></span>Deadline Fri Nov 20, 5:00 PM PT</div><div class="li"><span class="dot warn"></span>Address locked until accept</div></div>
  <div class="row" style="margin-top:16px"><a class="btn grow" href="#jobs" data-toast="Accepted (prototype).">Accept</a><a class="btn line grow" href="#bid">Bid</a></div>
  <button class="btn bad block" style="margin-top:8px" data-toast="Declined (prototype).">Decline</button>
</div>{tb("Opps")}</section>

<section class="app" data-screen="bid"><header class="app-h"><a href="#opp">‹</a><h2>Submit a bid</h2></header>
<div class="app-b" data-wizard data-finish="bid-sent" data-reset>
  <div class="row between"><span class="tiny muted" data-count></span><span class="tiny gold" data-step-label></span></div><div class="steps" style="margin:8px 0 14px"></div>
  <div class="wstep" data-label="Price"><h3>Your price</h3><div class="field"><label class="f">Bid amount</label><input class="inp" value="2350" inputmode="numeric"></div></div>
  <div class="wstep" data-label="Schedule"><h3>When can you start?</h3><input class="inp" value="Mon Nov 23, 8:00 AM PT"></div>
  <div class="wstep" data-label="Notes"><h3>Exclusions &amp; notes</h3><textarea class="inp" rows="3">Paint color to match existing. No wallpaper.</textarea>
    <button class="drop" style="margin-top:8px" data-add-file="#kbfiles">⇪ Attach a file</button><div id="kbfiles" class="stack s8" style="margin-top:8px"></div></div>
  <div class="wstep" data-label="Review"><h3>Review bid</h3><div class="sheet"><dl class="kv" style="grid-template-columns:90px 1fr"><dt>Amount</dt><dd>$2,350</dd><dt>Start</dt><dd>Mon Nov 23</dd></dl></div></div>
  <div class="row" style="margin-top:16px"><button class="btn line" data-prev>Back</button><button class="btn grow" data-next data-last-label="Send bid">Continue</button></div>
</div>{tb("Opps")}</section>

<section class="app" data-screen="bid-sent"><div class="app-b" style="padding:40px 22px;text-align:center"><div class="eyebrow">Sent</div><h2>Bid submitted</h2><p class="small muted" style="margin:10px 0 18px">IVO will compare bids and approve any award before you’re contacted with a decision.</p><a class="btn block" href="#opps">Back to opportunities</a></div>{tb("Opps")}</section>

<section class="app" data-screen="bidconfirm"><header class="app-h"><a href="#opps">‹</a><h2>Bid confirmation</h2></header>
<div class="app-b" data-item>
  <div class="eyebrow">BID-2201 · IVO is bidding as a sub</div>
  <h3>Cedar Ridge Elementary modernization</h3>
  <p class="small muted">Flooring · LVP, 6,200 SF. IVO needs you to confirm price, dates and capacity if they are awarded the work.</p>
  <div class="sheet" style="margin:12px 0"><dl class="kv" style="grid-template-columns:110px 1fr">
    <dt>Your price</dt><dd>$86,400</dd>
    <dt>Dates</dt><dd>Nov 30, 2026-Jan 15, 2027</dd>
    <dt>Capacity</dt><dd>Can you perform the work if IVO wins?</dd>
  </dl></div>
  <button class="btn block lg" data-set="Confirmed|ok" data-toast="Confirmed (prototype). IVO was not notified by a live message.">Confirm this price and these dates</button>
  <div class="field" style="margin-top:16px"><label class="f">Or adjust your price</label><input class="inp" value="86400" inputmode="numeric"></div>
  <button class="btn line block" data-set="Price changed|warn" data-toast="Price change noted (prototype). Nothing was sent.">Send a new price</button>
  <button class="btn bad block" style="margin-top:8px" data-set="Declined|bad" data-toast="Marked declined (prototype).">Not available</button>
  <span class="chip" data-status hidden style="margin-top:10px"></span>
</div>{tb("Opps")}</section>

<section class="app" data-screen="jobs"><header class="app-h"><h2>Jobs &amp; schedule</h2></header>
<div class="app-b"><div class="stack">
  <a class="card" href="#job"><div class="row between"><b>Ceiling leak, drywall &amp; paint</b><span class="chip info">In progress</span></div><p class="tiny muted">REQ-1042 · Cedar Court Unit 3B · today 9:00 AM–3:00 PM</p></a>
  <a class="card" href="#job"><div class="row between"><b>Hallway ceiling repair</b><span class="chip">Scheduled</span></div><p class="tiny muted">REQ-1059 · Mon 8:00 AM</p></a>
</div></div>{tb("Jobs")}</section>

<section class="app" data-screen="job"><header class="app-h"><a href="#jobs">‹</a><h2>REQ-1042</h2></header>
<div class="app-b">
  <h3>Ceiling leak, drywall &amp; paint</h3>
  <p class="small muted">Cedar Court Apartments, Unit 3B · 410 Sample Ave, Tacoma WA</p>
  <div class="card" style="margin:10px 0"><div class="row between"><span>Approved (NTE)</span><b>$4,800</b></div><div class="prog warn" style="margin:6px 0"><i style="width:91%"></i></div><p class="tiny muted">Your quote $4,350 · CO-2 +$620 pending</p></div>
  {timeline()}
  <a class="btn block" style="margin-top:12px" href="#checkin">Open camera check-in</a>
</div>{tb("Jobs")}</section>

<section class="app" data-screen="checkin"><header class="app-h"><a href="#job">‹</a><h2>Check in</h2><span class="chip offline">Works offline</span></header>
<div class="app-b" data-item>
  <div class="viewfinder" style="background-image:url(../assets/img/ivo-36.webp)"><div class="cross"></div></div>
  <p class="small muted" style="text-align:center;margin:10px 0">GPS: Cedar Court Apartments · Tue Nov 17, 9:02 AM PT (sample)</p>
  <button class="shutter" type="button" data-add-thumb="#kthumbs" data-toast="Photo captured (sample)." aria-label="Take check-in photo"></button>
  <div class="thumbs" id="kthumbs" style="margin:12px 0"></div>
  <button class="btn lg block" data-set="Checked in|ok" data-toast="Checked in with photo and GPS (prototype).">Complete check-in</button>
  <span class="chip" data-status hidden style="margin-top:8px"></span>
</div>{tb("Check in")}</section>

<section class="app" data-screen="punch"><header class="app-h"><a href="#job">‹</a><h2>Punch list</h2></header>
<div class="app-b"><div class="list"><div class="li"><span class="dot ok"></span><span class="grow">Close ceiling opening</span></div><div class="li"><span class="dot ok"></span><span class="grow">Texture to match</span></div><div class="li"><span class="dot warn"></span><span class="grow">Final paint after dry</span></div></div></div>{tb("Jobs")}</section>

<section class="app" data-screen="co"><header class="app-h"><a href="#job">‹</a><h2>Change order</h2></header>
<div class="app-b">
  <div class="field" data-nte="4800" data-spent="4350"><label class="f">Extra amount</label><input class="inp" value="620" inputmode="numeric"><div class="prog" style="margin:10px 0 6px"><i></i></div><p class="small" data-nte-out></p></div>
  <button class="drop" data-add-thumb="#cothumbs">📷 Add photos</button><div class="thumbs" id="cothumbs" style="margin-top:8px"></div>
  <button class="btn block" style="margin-top:12px" data-toast="Change order sent to IVO (prototype).">Request change order</button>
</div>{tb("Jobs")}</section>

<section class="app" data-screen="closeout"><header class="app-h"><a href="#job">‹</a><h2>Closeout</h2></header>
<div class="app-b" data-item>
  <button class="drop" data-add-thumb="#kcthumbs">📷 Before / after</button><div class="thumbs" id="kcthumbs" style="margin:8px 0"></div>
  <button class="drop" data-add-file="#kcfiles">⇪ Waiver or extra file</button><div id="kcfiles" class="stack s8" style="margin:8px 0"></div>
  <button class="btn lg block" data-set="Closeout sent|ok" data-toast="Closeout sent (prototype).">Submit closeout</button>
  <span class="chip" data-status hidden></span>
</div>{tb("Jobs")}</section>

<section class="app" data-screen="compliance"><header class="app-h"><h2>Compliance</h2></header>
<div class="app-b">
  <div class="list"><div class="li"><span class="grow">Certificate of insurance</span><span class="chip ok">Current</span></div><div class="li"><span class="grow">W-9</span><span class="chip ok">On file</span></div><div class="li"><span class="grow">State registration</span><span class="chip ok">Active</span></div></div>
</div>{tb("Docs")}</section>

<section class="app" data-screen="payouts"><header class="app-h"><h2>Earnings</h2></header>
<div class="app-b">
  <div class="card"><div class="eyebrow">Pipeline glance</div><div class="row between"><b style="font-size:24px">$6,430</b><span class="chip later">Tracking only</span></div>
    <p class="small muted" style="margin-top:8px">Payouts are not processed in the launch build. These numbers help you plan. Payment setup comes later.</p></div>
  <div class="stack" style="margin-top:12px">
    <div class="file"><span class="ic">$</span><span class="grow">REQ-1031 · Gutter cleaning</span><b>$980</b></div>
    <div class="file"><span class="ic">$</span><span class="grow">REQ-1036 · Water mitigation</span><b>$1,200</b></div>
    <div class="file"><span class="ic">$</span><span class="grow">REQ-1024 · Door closer</span><b>$260</b></div>
  </div>
</div>{tb("Profile")}</section>

<section class="app" data-screen="profile"><header class="app-h"><h2>Company &amp; crew</h2></header>
<div class="app-b"><p><b>Bluewater Flooring LLC</b></p><p class="small muted">Sam Rivera · King, Pierce · flooring &amp; drywall</p>
<p class="small" style="margin-top:8px">Joined by invite after staff vetting, with a watched trial first job (option A).</p>
<div class="list" style="margin-top:12px"><div class="li">Ana Kim · field</div><div class="li">Ben Okafor · field</div></div>
</div>{tb("Profile")}</section>
'''
    notes='''
<div class="notes-card glass" data-note="opps opp bidconfirm"><h3>Fast in the field</h3><ul><li>Swipe right to accept, left to decline.</li><li>A big primary button is always there if you don’t want to swipe.</li><li>Earnings are a glance only — no payments at launch.</li></ul></div>
<div class="notes-card glass" data-note="checkin" hidden><h3>Camera first</h3><p class="small muted">Check-in starts on the viewfinder. GPS time and a photo are the point, not a form.</p></div>
'''
    body=phone(idx,screens,notes)
    head='<link rel="manifest" href="manifest.webmanifest">'
    return shell("Contractor app", body, cmds=CM_KON+[("Desktop portal","../vendor-portal/index.html","Office view")], head=head)

def page_vendor():
    nav='''
    <a class="nav active" href="#overview" data-match="overview">Overview</a>
    <a class="nav" href="#opps" data-match="opps">Opportunities</a>
    <a class="nav" href="#bidconfirm" data-match="bidconfirm">Bid confirmation</a>
    <a class="nav" href="#packet" data-match="packet">Packet</a>
    <a class="nav" href="#bids" data-match="bids">Bids</a>
    <a class="nav" href="#jobs" data-match="jobs job">Jobs</a>
    <a class="nav" href="#compliance" data-match="compliance">Compliance</a>
    <a class="nav" href="#company" data-match="company">Company &amp; crew</a>
    <a class="nav" href="#payouts" data-match="payouts">Earnings (Later)</a>
    '''
    inner=f'''
<section class="content app" data-screen="overview">
  <div class="grid g3">
    <div class="metric glass"><div class="l">Scorecard</div><div class="v">4.7</div></div>
    <div class="metric glass"><div class="l">Open jobs</div><div class="v">2</div></div>
    <div class="metric glass"><div class="l">Pipeline (tracking)</div><div class="v">$2,500</div></div>
  </div>
  <div class="card"><div class="eyebrow">Why you were picked · REQ-1042</div>
    <span class="chip gold">Drywall in Pierce</span><span class="chip ok">COI current</span><span class="chip ok">Score 4.7</span><span class="chip">Capacity open</span>
    <p class="small muted" style="margin-top:8px">Rules, not an AI model. A person at IVO still approved the invite.</p>
  </div>
  {MAP.replace('data-map-go="#job"','data-map-go="#jobs"')}
</section>
<section class="content app" data-screen="opps">
  <div class="card"><div class="row between"><h3>Hallway ceiling repair</h3><span class="chip gold">Direct offer</span></div><p class="small muted">Tacoma · NTE $2,500 · respond by Fri Nov 20, 5:00 PM PT</p><a class="btn" href="#packet">Review packet</a></div>
  <div class="card" style="margin-top:12px"><div class="row between"><h3>Cedar Ridge Elementary · flooring</h3><span class="chip gold">Bid confirmation</span></div><p class="small muted">Confirm $86,400, dates Nov 30, 2026-Jan 15, 2027, and capacity if IVO is awarded.</p><a class="btn" href="#bidconfirm">Open request</a></div>
</section>
<section class="content app" data-screen="bidconfirm">
  <div class="card" data-item>
    <div class="eyebrow">BID-2201 · IVO is bidding as a sub</div>
    <h3>Cedar Ridge Elementary modernization</h3>
    <p class="small muted">Flooring · LVP, 6,200 SF. Confirm price, dates and capacity if IVO is awarded.</p>
    <dl class="kv" style="margin:12px 0"><dt>Your price</dt><dd>$86,400</dd><dt>Dates</dt><dd>Nov 30, 2026-Jan 15, 2027</dd></dl>
    <button class="btn" data-set="Confirmed|ok" data-toast="Confirmed (prototype). Nothing was sent.">Confirm this price and these dates</button>
    <div class="field" style="margin-top:14px"><label class="f">Or adjust your price</label><input class="inp" value="86400" inputmode="numeric"></div>
    <button class="btn line" data-set="Price changed|warn" data-toast="Price change noted (prototype).">Send a new price</button>
    <button class="btn bad" data-set="Declined|bad" data-toast="Marked declined (prototype).">Not available</button>
    <span class="chip" data-status hidden style="margin-left:8px"></span>
  </div>
</section>
<section class="content app" data-screen="packet">
  <div class="card" data-wizard id="vbid" data-finish="bids">
    <h3>Packet · REQ-1059</h3>
    <div class="row between"><span class="tiny muted" data-count></span><span class="tiny gold" data-step-label></span></div><div class="steps" style="margin:8px 0"></div>
    <div class="wstep" data-label="Scope"><p>Hallway ceiling repair, Bldg B. Exact address after accept.</p></div>
    <div class="wstep" data-label="Bid"><div class="field"><label class="f">Amount</label><input class="inp" value="2350"></div><button class="drop" data-add-file="#vbfiles">⇪ File</button><div id="vbfiles" class="stack s8" style="margin-top:8px"></div></div>
    <div class="row" style="margin-top:12px"><button class="btn line" data-prev>Back</button><button class="btn grow" data-next data-last-label="Send bid">Continue</button></div>
  </div>
</section>
<section class="content app" data-screen="bids">
  <div class="card"><b>REQ-1059 bid · $2,350</b><p class="small muted">Submitted. Waiting on IVO’s award approval.</p></div>
</section>
<section class="content app" data-screen="jobs">
  <a class="card" href="#job" style="display:block"><div class="row between"><b>REQ-1042 · Unit 3B ceiling leak</b><span class="chip info">In progress</span></div></a>
</section>
<section class="content app" data-screen="job">
  <div class="card"><h3>REQ-1042</h3>{timeline()}<a class="btn" href="#jobs">Back to jobs</a></div>
</section>
<section class="content app" data-screen="compliance">
  <div class="list"><div class="li"><span class="grow">Certificate of insurance</span><span class="chip ok">Current</span></div><div class="li"><span class="grow">W-9</span><span class="chip ok">On file</span></div></div>
</section>
<section class="content app" data-screen="company">
  <div class="card"><b>Bluewater Flooring LLC</b><p class="small muted">Crew: Ana Kim, Ben Okafor. Joined by invite, option A, after a watched trial job.</p></div>
</section>
<section class="content app" data-screen="payouts">
  <div class="later"><span class="chip later">Later</span> Earnings are shown as tracking only. Payouts are not processed at launch.</div>
</section>
'''
    body=portal_chrome("vendor","Bluewater Flooring LLC",nav,inner,CM_KON)
    return shell("Vendor portal", body, cmds=CM_KON+[("Phone app","../contractor/index.html#opps","Field view")])

print("portals+contractor defs ok")

def mini_wizard(wid, steps):
    parts=[f'<div class="mini" data-wizard id="{wid}"><div class="row between"><span class="tiny muted" data-count></span><span class="tiny gold" data-step-label></span></div><div class="steps" style="margin:6px 0 10px"></div>']
    for title, body, who in steps:
        parts.append(f'<div class="wstep" data-label="{who}"><h4 style="margin-bottom:8px">{title}</h4>{body}</div>')
    parts.append('<div class="row" style="margin-top:12px"><button class="btn sm line" data-prev>Back</button><button class="btn sm grow" data-next>Next step</button></div></div>')
    return "\n".join(parts)

def opt_col(key, title, sub, status, inner, fit=""):
    chips={"approved":'<span class="chip ok">Approved by owner 2026-11-13</span>',"not-chosen":'<span class="chip">Not chosen</span>',"later":'<span class="chip later">Later</span>',"allowed":'<span class="chip info">Allowed for existing accounts</span>'}
    cls={"approved":" rec approved","not-chosen":" not-chosen","later":" later-opt","allowed":" allowed"}.get(status,"")
    return f'''<div class="opt-col{cls}"><div class="oh"><div class="row between"><span class="k">OPTION {key}</span>{chips.get(status,"")}</div><h3 style="margin-top:4px">{title}</h3><p class="small muted">{sub}</p></div>
<div class="ob stack">{inner}{fit}</div></div>'''

def page_apply():
    wa=mini_wizard("wa",[
        ("IVO invites the contractor",'<div class="sheet small"><b>Email from IVO</b><p class="muted" style="margin-top:4px">“Dana at IVO Group invited Bluewater Flooring LLC to apply.”</p><a class="btn sm" style="margin-top:8px" data-goto="1" href="#">Accept invitation</a></div>','IVO staff'),
        ("Sign in with email code",'<div class="otp" style="gap:4px"><input value="2"><input value="0"><input value="4"><input value="8"><input value="1"><input value="6"></div>','Contractor'),
        ("Company info",'<div class="field"><label class="f">Legal name</label><input class="inp" value="Bluewater Flooring LLC (sample)"></div>','Contractor'),
        ("Trades &amp; regions",'<div class="opts" data-multi><button class="on">Flooring</button><button>Drywall</button></div>','Contractor'),
        ("Documents",'<div class="file"><span class="ic">PDF</span><span class="grow">COI_sample.pdf</span><span class="chip ok">uploaded</span></div>','Contractor'),
        ("References",'<div class="field"><label class="f">Reference 1</label><input class="inp" value="Property manager · ref1@example.com"></div><p class="tiny muted">Count still open: 1 or 2.</p>','Contractor'),
        ("Compliance check",'<div class="list small"><div class="li"><span class="dot ok"></span><span class="grow">State registration lookup</span><span class="chip ok">active</span></div><div class="li"><span class="dot ok"></span><span class="grow">Certificate limits</span><span class="chip ok">ok</span></div></div>','IVO staff'),
        ("Approval",'<div class="sheet" data-item><b>Approve Bluewater Flooring LLC?</b><div class="row" style="margin-top:8px"><span class="chip" data-status hidden></span><button class="btn sm ok" data-set="Approved|ok">Approve</button></div></div>','Owner'),
        ("Onboarding",'<div class="list small"><div class="li">Watched trial first job</div><div class="li">Ready for routing</div></div><a class="btn sm block" style="margin-top:10px" href="../contractor/index.html#opps">See the contractor app →</a>','Contractor'),
    ])
    wb=mini_wizard("wb",[("Open application form",'<div class="sheet"><b>Partner with IVO</b><p class="muted">Public form. Anyone can apply.</p></div>','Contractor'),("Verification",'<p class="small muted">Documents, then a trial job.</p>','IVO staff')])
    wc=mini_wizard("wc",[("Someone refers them",'<div class="sheet">Referral from Evergreen Restoration Co.</div>','Referrer'),("IVO reviews",'<p class="small muted">Same invite as A, if approved.</p>','IVO staff')])
    body=f'''
<div class="land-h" style="padding:30px 24px 34px"><div class="wrap"><a class="row small" href="../index.html" style="color:#e1c395;margin-bottom:12px">← Prototype home</a>
  <div class="eyebrow" style="color:#e1c395">Decision recorded</div>
  <h1>How contractors <em>join</em> the network</h1>
  <p style="max-width:760px;margin-top:10px">The owner approved option A on 13 Nov 2026. Click through each flow. Sample data only.</p>
</div></div>
<div class="wrap" id="main" style="padding:24px 16px 60px">
  <div class="opt-cols">
    {opt_col("A","Invite-only, staff-vetted","Staff invite contractors they choose, after vetting. First job is a watched trial.","approved",wa,'<div class="note"><b>Approved by owner 2026-11-13.</b> Invite-only after staff vetting, with a closely watched trial first job. The existing “Partner with IVO” form stays as an inquiry that lands in Triage; staff decide whether to invite.</div>')}
    {opt_col("B","Open application → verification → trial job","Anyone can apply on the website.","not-chosen",wb)}
    {opt_col("C","Referral-based","A trusted contractor or customer refers them.","not-chosen",wc,'<div class="note">Not chosen for launch. Could work later as an extra source. Same invite mechanism as A.</div>')}
  </div>
  <div class="decision rec" style="margin-top:20px"><h3>Recorded 13 Nov 2026</h3>
    <p class="small" style="margin-top:8px">The owner approved <b>option A</b>: invite-only after staff vetting, with a watched trial first job. The Partner with IVO form stays as an inquiry in Triage. Options B and C were not chosen.</p>
    <p class="small" style="margin-top:8px">Still open: how many references to require (1 or 2), and who besides the owner can approve a contractor (a second admin).</p>
  </div>
</div>
'''
    return shell("Contractor application: decision", body, cmds=[("See option A","#wa","Approved"),("Contractor app","../contractor/index.html#opps","After onboarding"),("Customer join","../onboarding/index.html","Option 1")])

def page_onboarding():
    o1=mini_wizard("o1",[
        ("Customer sends a request",'<div class="sheet"><b>Request form (website)</b><p class="muted">Trade, location, scope, urgency, budget, photos. No account needed.</p></div><div class="field"><label class="f">Email</label><input class="inp" value="maya.ortiz@harborline.example"></div>','Customer'),
        ("Confirmation email",'<div class="sheet"><b>“We received REQ-1059”</b></div>','System'),
        ("IVO reviews &amp; calls",'<div class="sheet">Triage in the staff console.</div><a class="btn sm line block" style="margin-top:8px" href="../console/index.html#triage">See triage →</a>','IVO staff'),
        ("Approve the invite",'<div class="sheet" data-item><b>Invite Maya Ortiz to a Harborline workspace?</b><div class="row" style="margin-top:8px"><span class="chip" data-status hidden></span><button class="btn sm ok" data-set="Invite sent|ok">Approve invite</button></div></div>','IVO staff'),
        ("Accept &amp; sign in",'<div class="sheet">Invite email → email code → the request is already inside.</div><a class="btn sm block" style="margin-top:8px" href="../customer/index.html#invite">See it in the customer app →</a>','Customer'),
        ("Set up the company",'<div class="list"><div class="li">Add properties</div><div class="li">Invite colleagues (IVO confirms)</div></div>','Customer'),
    ])
    o2=mini_wizard("o2",[("IVO creates the account",'<div class="sheet">Staff set up the company for a customer IVO already works with.</div>','IVO staff'),("Approve the invite",'<div class="sheet">Same invite as option 1.</div>','Owner / admin'),("Accept &amp; sign in",'<div class="sheet">Invite email → email code → empty workspace with properties.</div>','Customer'),("First request in the app",'<a class="btn sm block" href="../customer/index.html#new">See the request wizard →</a>','Customer')])
    o3=mini_wizard("o3",[("Customer sends a request",'<div class="sheet">Same request form as option 1.</div>','Customer'),("Private tracker link",'<div class="sheet"><b>Track REQ-1059</b><p class="muted">A no-login status page. Out of launch scope.</p></div>','Customer'),("Invite on approval",'<div class="sheet">Once they approve a quote, IVO invites them.</div>','IVO staff'),("Accept &amp; sign in",'<a class="btn sm block" href="../customer/index.html#invite">See the customer app →</a>','Customer')])
    body=f'''
<div class="land-h" style="padding:30px 24px 34px"><div class="wrap"><a class="row small" href="../index.html" style="color:#e1c395;margin-bottom:12px">← Prototype home</a>
  <div class="eyebrow" style="color:#e1c395">Decision recorded</div>
  <h1>How customers <em>get into</em> the portal</h1>
  <p style="max-width:760px;margin-top:10px">The portal is invite-only. The owner approved option 1 on 13 Nov 2026: request first, then an invite after IVO reviews it. Sample data only.</p>
</div></div>
<div class="wrap" id="main" style="padding:24px 16px 60px">
  <div class="opt-cols">
    {opt_col("1","Request first, then invite","New customers send a request; after IVO reviews it, they're invited.","approved",o1,'<div class="note"><b>Approved by owner 2026-11-13.</b> Staff can still use option 2 for accounts IVO already knows.</div>')}
    {opt_col("2","Account first (staff-invited)","IVO sets up accounts for customers it already works with.","allowed",o2,'<div class="note">Allowed for existing accounts. Same invite, no extra build.</div>')}
    {opt_col("3","Request first + private tracker link","Like option 1, plus a no-login status page until they're invited.","later",o3,'<div class="note">Stays marked <b>Later</b>.</div>')}
  </div>
  <div class="decision rec" style="margin-top:20px"><h3>Recorded 13 Nov 2026</h3>
    <p class="small" style="margin-top:8px">The owner approved <b>option 1</b>. Option 2 stays allowed for existing accounts. Option 3 stays marked Later.</p>
    <p class="small" style="margin-top:8px">Still open: who can approve a new customer workspace, and the role matrix.</p>
  </div>
</div>
'''
    return shell("Customer onboarding: decision", body, cmds=[("See option 1","#o1","Approved"),("Customer app","../customer/index.html#invite","After invite"),("Contractor join","../apply/index.html","Option A")])

def copy_pwa():
    for app in ("customer","contractor"):
        src=os.path.join(ROOT,app)
        dst=os.path.join(OUT,app)
        os.makedirs(dst, exist_ok=True)
        for fn in ("sw.js","manifest.webmanifest"):
            s=os.path.join(src,fn)
            if os.path.exists(s):
                shutil.copy2(s, os.path.join(dst,fn))

def main():
    write("index.html", page_index())
    write("console/index.html", console_screens())
    write("customer/index.html", page_customer())
    write("customer-portal/index.html", page_customer_portal())
    write("contractor/index.html", page_contractor())
    write("vendor-portal/index.html", page_vendor())
    write("apply/index.html", page_apply())
    write("onboarding/index.html", page_onboarding())
    copy_pwa()
    print("V02 build complete")

if __name__=="__main__":
    main()
