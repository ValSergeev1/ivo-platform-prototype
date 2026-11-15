"""IVO OS V03 generator core: icons, page shell, app shells, shared components."""
import json, os, re, html as _h
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "v3")
LUCIDE = "/workspace/ivo-proto-test/v3/node_modules/lucide-static/icons"
ICONS = set()
BASE_ICONS = {"check","x","info","siren","clock","calendar-check","shield-check","package-check","camera","search-x","sun-moon","arrow-right","search","keyboard","house","layout-grid","moon"}
ALIAS = {}

def esc(s): return _h.escape(str(s), quote=True)

def ic(name, cls=""):
    name = ALIAS.get(name, name)
    ICONS.add(name)
    return f'<svg class="i{(" "+cls) if cls else ""}" aria-hidden="true"><use href="#i-{name}"/></svg>'

def sprite():
    out = []
    for n in sorted(ICONS | BASE_ICONS):
        p = os.path.join(LUCIDE, n + ".svg")
        if not os.path.exists(p):
            raise SystemExit(f"missing icon {n}")
        s = open(p).read()
        inner = s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")].strip()
        inner = re.sub(r"\s+", " ", inner)
        out.append(f'<symbol id="i-{n}" viewBox="0 0 24 24">{inner}</symbol>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">'
            '<defs><style>symbol{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;overflow:visible}</style></defs>'
            + "".join(out) + "</svg>")

def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)

# ---------- small components ----------
def chip(t, cls="", dot=False, attrs=""):
    return f'<span class="chip {cls}"{attrs}>{"<i class=d></i>" if dot else ""}{t}</span>'

def btn(label, cls="", icon=None, href=None, attrs="", ic_after=None):
    inner = (ic(icon, "sm") if icon else "") + (f"<span>{label}</span>" if label else "") + (ic(ic_after, "sm") if ic_after else "")
    if href is not None:
        return f'<a class="btn {cls}" href="{href}"{attrs}>{inner}</a>'
    return f'<button class="btn {cls}" type="button"{attrs}>{inner}</button>'

def panel(title, body, icon=None, acts="", cls="", bd="bd", hid=None, tag="section", skel=False):
    h = f'<h2{(" id="+chr(34)+hid+chr(34)) if hid else ""}>{title}</h2>'
    lab = f' aria-labelledby="{hid}"' if hid else ""
    sk = " data-skel" if skel else ""
    return (f'<{tag} class="panel {cls}"{lab}><div class="hd">{ic(icon) if icon else ""}{h}<span class="grow"></span>{acts}</div>'
            f'<div class="{bd}"{sk}>{body}</div></{tag}>')

def spark(vals, cls="acc", fill=True):
    w, h = 120, 32
    mn, mx = min(vals), max(vals)
    rng = (mx - mn) or 1
    pts = [(i * w / (len(vals) - 1), h - 3 - (v - mn) / rng * (h - 6)) for i, v in enumerate(vals)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = d + f" L{w},{h} L0,{h} Z"
    col = {"acc": "var(--accent-2)", "ok": "var(--ok)", "warn": "var(--warn)", "bad": "var(--bad)", "info": "var(--info)"}[cls]
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="{area}" fill="{col}" opacity=".14"/><path d="{d}" fill="none" stroke="{col}" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>')

def kpi(label, value, delta="", dcls="t3", vals=None, scls="acc", icon=None):
    return (f'<div class="panel kpi"><div class="row between"><span class="eyebrow">{label}</span>{ic(icon,"sm t3") if icon else ""}</div>'
            f'<div class="v">{value}</div><div class="d {dcls}">{delta}</div>{spark(vals, scls) if vals else ""}</div>')

def steps(labels, now):
    out = []
    for i, l in enumerate(labels):
        c = "done" if i < now else ("now" if i == now else "")
        cur = ' aria-current="step"' if i == now else ""
        out.append(f'<div class="s {c}"{cur}>{l}</div>')
    return f'<div class="steps" role="list" aria-label="Status">{"".join(out).replace("<div class=", "<div role=listitem class=")}</div>'

def timeline(evs):
    """evs: (icon, when, title, body, state) state in '', 'now', 'future'"""
    out = []
    for icon, when, title, body, st in evs:
        out.append(f'<div class="ev {st}"><div class="nd">{ic(icon)}</div><div><div class="row between at"><b>{title}</b><span class="when">{when}</span></div>'
                   f'<p class="small t2" style="margin-top:2px">{body}</p></div></div>')
    return '<div class="tl">' + "".join(out) + "</div>"

def li(title, sub="", icon=None, icls="", right="", href=None, attrs=""):
    icn = f'<span class="ic {icls}">{ic(icon)}</span>' if icon else ""
    body = f'{icn}<div class="grow"><div style="font-weight:550">{title}</div>{f"<div class=\"small t3\">{sub}</div>" if sub else ""}</div>{right}'
    if href:
        return f'<a class="li" href="{href}"{attrs}>{body}</a>'
    return f'<div class="li"{attrs}>{body}</div>'

def note(text, icon="info", cls=""):
    return f'<div class="note {cls}">{ic(icon,"sm")}<div>{text}</div></div>'

def gate(text="Nothing is sent until an admin approves it."):
    return f'<span class="gatebadge">{ic("shield-check","sm")}Approval gate · {text}</span>'

def photo(img, cap, when="", tag="", depth=2):
    pre = "../" * (depth - 1)
    t = f'<span class="tagp">{tag}</span>' if tag else ""
    return (f'<figure class="ph-tile" style="margin:0">{t}<img src="{pre}assets/img/ph-{img}.webp" alt="{esc(cap)} (sample photo)" loading="lazy" width="400" height="300">'
            f'<figcaption><span>{cap}</span><span class="mono">{when}</span></figcaption></figure>')

# ---------- map ----------
STATES = {
 "wa": "M40,24 L330,24 L332,170 L64,170 L50,140 L44,110 L22,58 Z",
 "or": "M64,170 L332,170 L344,196 L326,258 L324,350 L30,350 L38,270 L50,210 Z",
 "id": "M332,24 L372,24 L374,108 L402,160 L432,198 L420,232 L470,252 L484,350 L324,350 L326,258 L344,196 L332,170 Z",
 "ca": "M30,350 L252,350 L252,468 L322,540 L60,540 L48,500 L26,420 Z",
}
CITIES = {"Seattle":(104,66),"Tacoma":(96,90),"Bellevue":(122,70),"Lynnwood":(108,50),"Kent":(112,82),"Spokane":(306,66),
          "Portland":(92,186),"Salem":(84,218),"Eugene":(80,262),"Bend":(182,262),"Boise":(396,286),"Redding":(112,412),"Sacramento":(132,505)}
def pct(x, y): return (x / 500 * 100, y / 560 * 100)

def mapbox(pins, routes=(), labels=True, extra_cls="", aria="Schematic coverage map of Washington, Oregon, Idaho and Northern California"):
    """pins: (city, kind, tip, href)"""
    svg = [f'<svg class="base" viewBox="0 0 500 560" role="img" aria-label="{aria}">']
    for k, d in STATES.items():
        svg.append(f'<path class="st" d="{d}"/>')
    for a, b in routes:
        (x1, y1), (x2, y2) = CITIES[a], CITIES[b]
        mx, my = (x1 + x2) / 2 + 20, (y1 + y2) / 2 - 30
        svg.append(f'<path class="route" d="M{x1},{y1} Q{mx},{my} {x2},{y2}"/>')
    svg.append("</svg>")
    out = ["".join(svg)]
    if labels:
        for t, (x, y) in {"Washington": (190, 104), "Oregon": (190, 290), "Idaho": (412, 200), "N. California": (140, 452)}.items():
            px, py = pct(x, y)
            out.append(f'<span class="mlab" style="left:{px:.1f}%;top:{py:.1f}%">{t}</span>')
    for city, kind, tip, href in pins:
        x, y = CITIES[city]
        px, py = pct(x, y)
        tag = "a" if href else "button"
        hr = f' href="{href}"' if href else ' type="button"'
        out.append(f'<{tag} class="pin {kind}"{hr} style="left:{px:.1f}%;top:{py:.1f}%" data-tip="{esc(tip)}" aria-label="{esc(tip)}"><i></i></{tag}>')
    return f'<div class="mapbox {extra_cls}">{"".join(out)}</div>'

# ---------- floor plan with punch pins ----------
PUNCH = [
 (1, 38, 30, "Close ceiling opening", "Hallway · 4 sq ft", True),
 (2, 46, 34, "Texture to match", "Hallway ceiling", False),
 (3, 70, 62, "Final paint after dry", "Unit 3B living room", False),
 (4, 22, 70, "Replace stained base trim", "Bedroom 2", False),
 (5, 82, 26, "Check smoke detector reinstalled", "Kitchen", False),
]
def plan_svg():
    return ('<svg viewBox="0 0 400 260" role="img" aria-label="Unit 3B floor plan, sheet A-201 (sample)">'
            '<rect class="room" x="10" y="10" width="380" height="240"/>'
            '<rect class="room" x="10" y="10" width="120" height="120"/><rect class="room" x="130" y="10" width="140" height="70"/>'
            '<rect class="room" x="270" y="10" width="120" height="110"/><rect class="room" x="10" y="130" width="140" height="120"/>'
            '<rect class="room" x="150" y="80" width="240" height="170"/>'
            '<rect class="hatch" x="130" y="58" width="80" height="40" rx="4"/>'
            '<path class="wall" d="M10 10 H390 V250 H10 Z"/>'
            '<path d="M130 10 V130 M10 130 H150 M150 130 V250 M270 10 V120 M130 80 H390" stroke="var(--text-3)" stroke-width="2" fill="none"/>'
            '</svg>')

def punch_plan(depth=2, compact=False):
    pins = "".join(f'<button class="ppin{" done" if d else ""}" type="button" data-pin="{n}" style="left:{x}%;top:{y}%" aria-label="Punch item {n}: {esc(t)}"><span><b>{n}</b></span></button>' for n, x, y, t, w, d in PUNCH)
    items = "".join(
        f'<div class="li punch-li" data-punch="{n}"><label class="check" style="min-height:44px"><input type="checkbox"{" checked" if d else ""} aria-label="Mark item {n} done"></label>'
        f'<span class="mono acc" style="width:22px">#{n}</span><div class="grow"><div style="font-weight:550">{t}</div><div class="small t3">{w}</div></div>'
        f'{chip("Closed","ok") if d else chip("Open","warn")}</div>' for n, x, y, t, w, d in PUNCH)
    done = sum(1 for p in PUNCH if p[5])
    plan = f'<div class="plan">{plan_svg()}{pins}</div>'
    lst = f'<div class="panel"><div class="hd">{ic("list-checks")}<h2>Punch items</h2><span class="grow"></span><span class="small t3" data-punch-count>{done} of {len(PUNCH)} done</span></div><div class="list">{items}</div></div>'
    if compact:
        return f'<div data-punchscope class="col gap16">{plan}{lst}</div>'
    return f'<div data-punchscope class="grid g-main-l">{plan}{lst}</div>'

def before_after(a="slab", b="office", depth=2, label="Before and after, drag to compare"):
    pre = "../" * (depth - 1)
    return (f'<div class="ba"><img src="{pre}assets/img/ph-{a}.webp" alt="Before (sample photo)"><img class="after" src="{pre}assets/img/ph-{b}.webp" alt="After (sample photo)">'
            f'<span class="h"></span><span class="lb" style="left:10px">Before</span><span class="lb" style="right:10px">After</span>'
            f'<input type="range" min="0" max="100" value="50" aria-label="{label}"></div>')

# ---------- page shell ----------
def cmd_json(items):
    return '<script type="application/json" id="cmd-data">' + json.dumps([{"g": g, "t": t, "h": h, "s": s, "ic": i} for g, t, h, s, i in items]).replace("</", "<\\/") + "</script>"

def page(rel, title, body, depth=1, cmds=(), app="IVO OS", bodyattrs="", head="", hub=False):
    for c in cmds:
        ICONS.add(c[4])
    pre = "../" * depth if depth else ""
    v1 = pre + "../index.html"
    v2 = pre + "../v2/index.html"
    hubh = pre + "index.html"
    banner = f'''<div class="proto-banner" role="region" aria-label="Prototype notice">
<span class="tag"><span class="pulse"></span>Prototype</span><span class="hide-n t-b">V03 · fictional sample data · nothing is sent or saved</span>
<nav class="ver" aria-label="Prototype version"><a href="{v1}">V01</a><a href="{v2}">V02</a><span aria-current="page">V03</span></nav>
<span class="grow"></span>
<button type="button" data-cmd-open aria-label="Search or jump (Command K)">{ic("search","sm")}<span class="hide-n">Search</span><span class="kbd hide-n" style="background:transparent;color:#e8eef2;border-color:rgba(255,255,255,.3)">⌘K</span></button>
<button type="button" data-keys-open class="hide-n" aria-label="Keyboard shortcuts">{ic("keyboard","sm")}</button>
<button type="button" data-theme-toggle aria-label="Switch to light theme">{ic("sun-moon","sm")}</button>
<a href="{hubh}" aria-label="All apps">{ic("layout-grid","sm")}<span class="hide-n">All apps</span></a>
</div>'''
    cmd_all = list(cmds) + [("Prototype", "All V03 apps", hubh, "Hub", "layout-grid"), ("Prototype", "V02 design", v2, "Previous", "history"), ("Prototype", "Toggle theme (button in the top bar)", "#", "Light / dark", "sun-moon")]
    for c in cmd_all: ICONS.add(c[4])
    dialogs = f'''<dialog id="cmdk" aria-label="Command menu"><div class="cmdk"><div class="q">{ic("search")}<input type="text" role="combobox" aria-expanded="true" aria-controls="cmd-res" aria-label="Search screens, records and actions" placeholder="Search screens, records, actions…" autocomplete="off"><span class="kbd">esc</span></div>
<div class="res" id="cmd-res" role="listbox" aria-label="Results"></div><div class="ft"><span><span class="kbd">↑</span> <span class="kbd">↓</span> move</span><span><span class="kbd">↵</span> open</span><span><span class="kbd">esc</span> close</span><span class="grow"></span><span>Actions that send anything open a draft for approval</span></div></div></dialog>
<dialog id="keys" aria-labelledby="keys-h"><div class="keys"><div class="row between"><h2 id="keys-h">Keyboard shortcuts</h2><form method="dialog"><button class="btn ghost icon" aria-label="Close">{ic("x")}</button></form></div>
<dl><dt><span class="kbd">⌘</span><span class="kbd">K</span></dt><dd>Command menu (also <span class="kbd">/</span>)</dd><dt><span class="kbd">G</span> then a letter</dt><dd>Go to a screen (letters shown in the sidebar)</dd><dt><span class="kbd">J</span> <span class="kbd">K</span></dt><dd>Move through a list, <span class="kbd">↵</span> to open</dd><dt><span class="kbd">.</span></dt><dd>Open or close the copilot</dd><dt><span class="kbd">?</span></dt><dd>This sheet</dd><dt><span class="kbd">esc</span></dt><dd>Close menus and sheets</dd></dl></div></dialog>
<div class="scrim" aria-hidden="true"></div><div class="toasts" id="toasts" role="status" aria-live="polite"></div>'''
    body_html = banner + body + dialogs + cmd_json(cmd_all)
    doc = f'''<!doctype html>
<html lang="en" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive"><meta name="googlebot" content="noindex,nofollow">
<meta name="theme-color" content="#061d2a"><meta name="color-scheme" content="dark light">
<title>{esc(title)} · IVO OS V03 prototype (sample data)</title>
<link rel="icon" href="{pre}assets/img/favicon.png"><link rel="apple-touch-icon" href="{pre}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400..700&family=Geist+Mono:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/ivo-os.css">{head}
<script>try{{var t=localStorage.getItem('ivo-v3-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
</head><body data-app="{esc(app)}"{bodyattrs}>
<a class="skip" href="#main">Skip to content</a>
{sprite_placeholder()}
{body_html}
<script src="{pre}assets/js/ivo-os.js" defer></script>
</body></html>'''
    doc = doc.replace("@@SPRITE@@", sprite())
    write(rel, doc)
    ICONS.clear()

def sprite_placeholder(): return "@@SPRITE@@"

# ---------- desktop app shell ----------
def os_shell(brand_sub, groups, screens, bnav, user=("DW", "Dana Whitfield", "Operations · sample"), copilot="", depth=1, top_right=""):
    pre = "../" * depth
    rail = [f'<div class="brandbox"><img class="mark-d" src="{pre}assets/img/ivo-mark-white.png" alt=""><img class="mark-l" src="{pre}assets/img/ivo-mark-navy.png" alt=""><div><b>IVO OS</b><span>{brand_sub}</span></div></div>',
            f'<button class="search" type="button" data-cmd-open style="min-width:0;margin:0 0 6px">{ic("search","sm")}<span>Jump to…</span><span class="kbd">⌘K</span></button>']
    sheet_links = []
    for g, items in groups:
        rail.append(f'<div class="grp">{g}</div>')
        for it in items:
            sid, lab, icon = it[0], it[1], it[2]
            ct = it[3] if len(it) > 3 else ""
            match = it[4] if len(it) > 4 else ""
            gk = it[5] if len(it) > 5 else ""
            ctc = f'<span class="ct{" hot" if ct and ct.startswith("!") else ""}">{ct.lstrip("!")}</span>' if ct else ""
            gattr = f' data-g="{gk}" title="G then {gk.upper()}"' if gk else ""
            m = f' data-match="{match}"' if match else ""
            rail.append(f'<a class="nav" href="#{sid}"{m}{gattr}>{ic(icon)}<span>{lab}</span>{ctc}</a>')
            sheet_links.append(f'<a class="nav" href="#{sid}"{m}>{ic(icon)}<span>{lab}</span></a>')
    rail.append(f'<div class="foot"><span class="avatar">{user[0]}</span><div class="grow"><div class="small" style="font-weight:600">{user[1]}</div><div class="xs t3">{user[2]}</div></div></div>')
    bn = []
    for sid, lab, icon, match in bnav:
        m = f' data-match="{match}"' if match else ""
        bn.append(f'<a href="#{sid}"{m}>{ic(icon)}<span>{lab}</span></a>')
    bn.append(f'<button type="button" data-sheet-open="more-sheet" aria-label="All sections">{ic("menu")}<span>More</span></button>')
    cp_btn = (f'<button class="btn sm" type="button" data-copilot-toggle aria-expanded="false" aria-label="Open IVO Copilot">{ic("sparkles","sm")}<span class="hide-m">Copilot</span></button>') if copilot else ""
    top = f'''<header class="top"><div class="crumbs grow"><span class="hide-m">{brand_sub.title()}</span><span class="hide-m">/</span><b data-crumb></b></div>
<button class="search hide-m" type="button" data-cmd-open>{ic("search","sm")}<span class="lbl-long">Search jobs, bids, contractors, actions…</span><span class="kbd">⌘K</span></button>
<span class="live hide-m">Live · synced <span data-ago>2s ago</span></span>{top_right}{cp_btn}</header>'''
    return f'''<div class="os">
<nav class="rail navset" aria-label="Main">{"".join(rail)}</nav>
<div class="mainwrap">{top}<main id="main" data-router tabindex="-1">{screens}</main></div>
{copilot}
</div>
<nav class="bnav navset" aria-label="Main (mobile)">{"".join(bn)}</nav>
<div class="sheet navset" id="more-sheet" role="dialog" aria-label="All sections"><div class="grab"></div><div class="navs">{"".join(sheet_links)}</div></div>'''

def screen(sid, title, inner, eyebrow="", sub="", acts="", default=False, extra="", crumb=None):
    d = " data-default" if default else ""
    ph = f'''<div class="ph"><div><div class="eyebrow">{eyebrow}</div><h1 style="margin-top:6px">{title}</h1>{f"<p>{sub}</p>" if sub else ""}</div><div class="acts">{acts}</div></div>''' if title else ""
    return f'<section class="page" data-screen="{sid}" data-title="{esc(crumb or _h.unescape(re.sub("<[^>]+>","",title)) or sid)}"{d}{extra}>{ph}{inner}</section>'

# ---------- mobile app shell ----------
def m_shell(app_title, persona, idx, screens, tabs, notes, depth=1, portal_href=None):
    side = [f'<div class="panel" style="padding:14px"><div class="eyebrow">{app_title}</div><div style="font-weight:600;margin-top:6px">{persona[0]}</div><div class="small t3">{persona[1]}</div></div>',
            '<nav class="navset col gap4" aria-label="Prototype screens" style="margin-top:14px">']
    for g, items in idx:
        side.append(f'<div class="eyebrow" style="padding:10px 10px 4px">{g}</div>')
        for sid, lab in items:
            side.append(f'<a class="nav" href="#{sid}">{lab}</a>')
    side.append("</nav>")
    if portal_href:
        side.append(f'<a class="btn block" style="margin-top:12px" href="{portal_href[0]}">{ic("monitor","sm")}<span>{portal_href[1]}</span></a>')
    tb = []
    for sid, lab, icon, match, *k in tabs:
        cls = ' class="fab"' if k and k[0] == "fab" else ""
        m = f' data-match="{match}"' if match else ""
        tb.append(f'<a href="#{sid}"{m}{cls}>{ic(icon)}<span>{lab}</span></a>')
    return f'''<div class="mshell">
<aside class="mside" aria-label="Screen index">{"".join(side)}</aside>
<div class="device"><main id="main" class="scr" data-router tabindex="-1">{screens}</main>
<nav class="tabbar navset" aria-label="App">{"".join(tb)}</nav></div>
<aside class="notes" aria-label="Design notes">{notes}</aside>
</div>'''

def mscreen(sid, title, inner, back=None, right="", notab=False, default=False, hdr=True, title_tag="h1"):
    b = f'<a class="back" href="{back}" aria-label="Back">{ic("chevron-left")}</a>' if back else ""
    head = f'<header class="ahd">{b}<{title_tag} class="grow ell">{title}</{title_tag}>{right}</header>' if hdr else ""
    nt = " data-notab" if notab else ""
    d = " data-default" if default else ""
    return f'<section data-screen="{sid}" data-title="{esc(_h.unescape(re.sub("<[^>]+>","",title)))}"{nt}{d}>{head}<div class="abd">{inner}</div></section>'
