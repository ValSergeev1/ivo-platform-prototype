"""Customer home extras and gallery helpers for the V03 prototype (sample data only)."""
from core import *

def phero(pid, name, addr, jobs, photos, img, href, initials, hidden=False, static=False):
    img_html = (
        f'<img class="phero-img" src="../assets/img/ph-{img}.webp" alt="">'
        if img else
        f'<div class="phero-fallback" aria-hidden="true"><span class="phero-mono">{initials}</span></div>'
    )
    job_l = "1 open job" if jobs == 1 else f"{jobs} open jobs"
    if photos == 0:
        photo_l = "Add photos"
    elif photos == 1:
        photo_l = "1 photo"
    else:
        photo_l = f"{photos} photos"
    hide = " hide" if hidden else ""
    cls = "phero static" if static else "phero"
    go = "" if static else f'<span class="grow"></span><span class="sr">Open the photo gallery</span>{ic("chevron-right")}'
    inner = (
        f'{img_html}<div class="phero-shade" aria-hidden="true"></div><div class="phero-body">'
        f'<span class="eyebrow phero-eyebrow">Your property</span>'
        f'<h2 class="phero-name">{name}</h2>'
        f'<p class="phero-addr">{addr}</p>'
        f'<div class="row wrap gap6" style="margin-top:10px"><span class="chip phero-chip">{job_l}</span>'
        f'<span class="chip phero-chip">{ic("camera","sm")}{photo_l}</span>{go}</div></div>'
    )
    if static:
        return f'<div class="{cls}{hide}" data-phero="{pid}">{inner}</div>'
    return f'<a class="{cls}{hide}" href="{href}" data-phero="{pid}">{inner}</a>'

def fthumbs(items):
    n = min(len(items), 4)
    cells = []
    for i, (img, cap) in enumerate(items[:4]):
        extra = f'<span class="fmore">+{len(items)-4}</span>' if i == 3 and len(items) > 4 else ""
        cells.append(
            f'<span class="fthumb"><img src="../assets/img/ph-{img}.webp" alt="{esc(cap)} (sample photo)" loading="lazy">{extra}</span>'
        )
    return f'<span class="fthumbs n{n}">{"".join(cells)}</span>'

def fcard(place, kind, icon, tone, title, when, detail, meta, href, fresh=False, thumbs="", amount=""):
    new = chip("New", "gold fresh-mark") if fresh else ""
    amt = f'<b class="mono fcard-amt">{amount}</b>' if amount else ""
    det = f'<span class="small t2 fcard-detail">{detail}</span>' if detail else ""
    cls = "fcard fresh" if fresh else "fcard"
    return (
        f'<li class="{cls}" data-place="{place}" data-kind="{kind}"><a class="fcard-link" href="{href}">'
        f'<span class="fic {tone}">{ic(icon)}</span><span class="grow fcard-main">'
        f'<span class="row between at fcard-top"><b class="fcard-title">{title}</b>'
        f'<span class="xs t3 fcard-when">{when}</span></span>'
        f'{det}{thumbs}<span class="row wrap gap6 fcard-meta">{amt}<span class="xs t3">{meta}</span>{new}</span>'
        f'</span></a></li>'
    )

def gallery_fig(img, cap, cover=False, job=None):
    cls = "cover" if cover else ""
    star_ic = ic("star", "sm acc") + " " if cover else ""
    if job:
        acts = (
            f'<button type="button" class="btn ghost icon" data-pin-photo aria-label="Pin to your photos">{ic("pin","sm")}</button>'
            f'<button type="button" class="btn ghost icon" data-cover aria-label="Make this the cover photo">{ic("star","sm")}</button>'
        )
        sub = f'{cap} <span class="t3 mono">{job}</span>'
    else:
        acts = "" if cover else f'<button type="button" class="btn ghost icon" data-cover aria-label="Make this the cover photo">{ic("star","sm")}</button>'
        acts += f'<button type="button" class="btn ghost icon" data-remove aria-label="Remove from gallery">{ic("trash-2","sm")}</button>'
        sub = cap
    return (
        f'<figure class="{cls}"><img src="../assets/img/ph-{img}.webp" alt="{esc(cap)} (sample photo)" loading="lazy">'
        f'<figcaption><span class="grow ell">{star_ic}{sub}</span>{acts}</figcaption></figure>'
    )

def customer_home_body():
    live_card = (
        '<li class="fcard fresh" data-place="cedar" data-kind="visits">'
        f'<a class="fcard-link" href="#job"><span class="fic">{ic("map-pin-off")}</span>'
        '<span class="grow fcard-main"><span class="row between at fcard-top">'
        '<b class="fcard-title">Crew left the site</b><span class="xs t3 fcard-when">just now</span></span>'
        f'<span class="row wrap gap6 fcard-meta"><span class="xs t3">REQ-1042 · Cedar Court</span>{chip("New","gold fresh-mark")}</span>'
        '</span></a></li>'
    )
    thumbs = fthumbs([
        ("site", "Arrival at unit door"),
        ("lock", "Joist above the opening"),
        ("slab", "Ceiling opening"),
        ("door", "Hallway stain"),
    ])
    feed = "\n".join([
        fcard("cedar","visits","map-pin","ok","Crew arrived on site","12 min ago","Ana Kim checked in at Unit 3B.","REQ-1042 · Cedar Court","#job",True),
        fcard("cedar","photos","camera","info","4 new photos from the crew","1h ago","","REQ-1042 · Cedar Court","#job",True,thumbs),
        fcard("cedar","money","file-pen","warn","Change order needs your approval","11:24 AM","Joist cracked above the opening. Sister with a 2x8, 6 ft.","REQ-1042 · Cedar Court","#approve",False,"","+$620"),
        fcard("cedar","photos","pen-tool","gold","Marked-up plan shared","Yesterday","Sheet A-201 · Version 2, shared by IVO.","REQ-1042 · Cedar Court","#job"),
        fcard("cedar","visits","calendar-clock","info","Visit scheduled","Mon 8:00 AM","","REQ-1059 · Hallway ceiling","#requests"),
        fcard("harbor","visits","badge-check","ok","Signed off and closed","Oct 28","","REQ-1031 · Harbor Point","#docs"),
        fcard("harbor","money","receipt","gold","Invoice INV-1031 issued","Oct 28","","REQ-1031 · Harbor Point","#invoices",False,"","$980"),
        fcard("cedar","visits","clipboard-check","gold","Work complete, ready for your sign-off","Oct 21","","REQ-1036 · Water mitigation","#closeout"),
    ])
    return f'''<div data-places>
<div class="phero-wrap" aria-label="Your property">
{phero("cedar","Cedar Court Apartments","410 Sample Ave, Tacoma, WA",2,6,"exterior","#gallery","CC")}
{phero("harbor","Harbor Point","88 Harbor Way, Tacoma, WA",0,2,"lobby","#gallery-hp","HP",hidden=True)}
<div class="pchips" role="group" aria-label="Show updates for">
<button type="button" class="chip-btn" data-place="all" aria-pressed="false">All properties</button>
<button type="button" class="chip-btn" data-place="cedar" aria-pressed="true"><img class="chip-thumb" src="../assets/img/ph-exterior.webp" alt="">Cedar Court</button>
<button type="button" class="chip-btn" data-place="harbor" aria-pressed="false"><img class="chip-thumb" src="../assets/img/ph-lobby.webp" alt="">Harbor Point</button>
</div></div>
<a class="sos" href="#emergency" aria-label="Emergency: alert IVO now. One tap, with 5 seconds to cancel."><span class="ic">{ic("siren","lg")}</span><span class="grow">Emergency<small>Active leak, no power, unsafe. One tap alerts IVO.</small></span>{ic("chevron-right")}</a>
<div data-place-block="cedar"><div class="hero" data-coach="job-card"><div class="row between"><span class="eyebrow" style="color:#e1c395">Happening now</span><span class="chip gold"><i class="d" style="background:#e1c395;width:7px;height:7px;border-radius:50%"></i>Live</span></div>
<h2 style="margin-top:10px;font-size:22px">Unit 3B ceiling leak</h2><p class="t3x small" style="margin-top:4px">Cedar Court · Ana Kim is on site since 9:02 AM</p>
<div style="margin:16px 0">{steps(["Received","Reviewed","Assigned","On site","Sign-off"],3)}</div>
<a class="btn primary lg block" href="#approve">{ic("check","sm")}<span>Approve change order · +$620</span></a></div>
<div class="grid g2" style="grid-template-columns:1fr 1fr;gap:10px"><a class="tile-btn" href="#new" style="min-height:96px">{ic("plus","lg")}<b>New request</b></a><a class="tile-btn" href="#docs" style="min-height:96px">{ic("folder","lg")}<b>Documents</b></a></div>
<section class="panel" aria-labelledby="hm-o"><div class="hd"><h2 id="hm-o">Also open</h2><span class="grow"></span><a class="btn sm ghost" href="#requests">All</a></div><div class="list">{li("REQ-1059 · Hallway ceiling","Scheduled Mon 8:00 AM · Bldg B","calendar","info",chip("Scheduled","ok"),href="#requests")}</div></section></div>
<section class="feed" aria-labelledby="feed-h">
<div class="feed-head" data-coach="feed"><div class="row between wrap" style="gap:8px"><h2 id="feed-h" class="feed-h">{ic("sparkles","sm acc")} Job updates</h2><span class="chip gold"><i class="d" style="background:#e1c395;width:7px;height:7px;border-radius:50%"></i>Live</span></div>
<div class="seg feed-filters" role="group" aria-label="Show" data-feed-filter>
<button type="button" data-filter="all" aria-pressed="true">All</button>
<button type="button" data-filter="visits" aria-pressed="false">Visits</button>
<button type="button" data-filter="photos" aria-pressed="false">Photos</button>
<button type="button" data-filter="money" aria-pressed="false">Approvals and invoices</button>
</div>
</div>
<p class="sr" aria-live="polite" data-feed-announce></p>
<ol class="feed-list">
{feed}
</ol>
<template data-feed-live>{live_card}</template>
</section>
</div>'''

def gallery_screen(sid, name, addr, img, initials, mine, jobs, back="#home", open_jobs=0, extra=""):
    mine_html = "".join(gallery_fig(*m) if len(m) == 2 else gallery_fig(m[0], m[1], cover=m[2]) for m in mine)
    job_html = "".join(gallery_fig(img_, cap, job=job) for img_, cap, job in jobs)
    return mscreen(sid, name, f'''<div data-gallery data-coach="gallery">
{phero(sid, name, addr, open_jobs, len(mine)+len(jobs), img, "#gallery", initials, static=True)}
<div class="panel"><div class="bd col gap16">
<label class="field"><span>Caption (optional)</span><input class="input" placeholder="e.g. Front entrance"></label>
<label class="btn primary lg block" style="cursor:pointer">{ic("image-plus","sm")}<span>Add photos of this property</span>
<input type="file" accept="image/*,.heic,.heif" multiple class="sr" data-add-photos></label>
<p class="xs t3">Only your company and IVO can see these photos. This preview stays on your phone.</p>
</div></div>
<section class="panel" aria-labelledby="mine-h-{sid}"><div class="hd"><h2 id="mine-h-{sid}">Your photos</h2></div>
<div class="gallery" data-mine>{mine_html}</div></section>
<section class="panel" aria-labelledby="jobs-h-{sid}"><div class="hd"><h2 id="jobs-h-{sid}">From your jobs</h2></div>
<div class="gallery">{job_html}</div></section>
{extra}
</div>''', back=back)

def markup_plan_svg():
    return '''<svg class="mk-img" viewBox="0 0 400 260" role="img" aria-label="Unit 3B floor plan, sheet A-201 (sample)">
<rect fill="#f7f4ee" x="0" y="0" width="400" height="260"/>
<rect fill="#efe8d8" stroke="#8a7350" stroke-width="1.5" x="10" y="10" width="120" height="120"/>
<rect fill="#efe8d8" stroke="#8a7350" stroke-width="1.5" x="130" y="10" width="140" height="70"/>
<rect fill="#efe8d8" stroke="#8a7350" stroke-width="1.5" x="270" y="10" width="120" height="110"/>
<rect fill="#efe8d8" stroke="#8a7350" stroke-width="1.5" x="10" y="130" width="140" height="120"/>
<rect fill="#f7f4ee" stroke="#8a7350" stroke-width="1.5" x="150" y="80" width="240" height="170"/>
<rect fill="#e4d7bc" stroke="#8a7350" x="130" y="58" width="80" height="40" rx="3"/>
<rect fill="none" stroke="#061d2a" stroke-width="3" x="8" y="8" width="384" height="244"/>
<text fill="#6b5a3e" font-family="Geist,system-ui,sans-serif" font-size="9" letter-spacing="1.2" x="28" y="72">BEDROOM 2</text>
<text fill="#6b5a3e" font-family="Geist,system-ui,sans-serif" font-size="9" letter-spacing="1.2" x="168" y="42">KITCHEN</text>
<text fill="#6b5a3e" font-family="Geist,system-ui,sans-serif" font-size="9" letter-spacing="1.2" x="300" y="62">BATH</text>
<text fill="#6b5a3e" font-family="Geist,system-ui,sans-serif" font-size="9" letter-spacing="1.2" x="40" y="196">BEDROOM 1</text>
<text fill="#6b5a3e" font-family="Geist,system-ui,sans-serif" font-size="9" letter-spacing="1.2" x="220" y="170">LIVING / HALL</text>
<text fill="#061d2a" font-family="Geist Mono,ui-monospace,monospace" font-size="8" x="16" y="252">A-201 · UNIT 3B · SAMPLE</text>
<text fill="#061d2a" font-family="Geist Mono,ui-monospace,monospace" font-size="8" x="300" y="252">1/4&quot; = 1'-0&quot;</text>
</svg>'''

SWATCHES = [("red","#d62828","Red"),("orange","#e8590c","Orange"),("yellow","#f5c400","Yellow"),("green","#2b9348","Green"),("blue","#1d6fd8","Blue"),("navy","#061d2a","Navy"),("black","#111111","Black"),("white","#ffffff","White")]
TOOLS = [("hand","hand","Move"),("pen","pen","Pen"),("highlighter","highlighter","Highlighter"),("arrow","arrow-up-right","Arrow"),("rect","square","Box"),("ellipse","circle","Circle"),("text","type","Text"),("pin","map-pin","Punch pin"),("eraser","eraser","Eraser")]

def markup_editor():
    tools = "".join(
        f'<button class="mk-tool" type="button" data-mk-tool="{tid}" aria-pressed="{"true" if tid=="pen" else "false"}" aria-label="{lab}" title="{lab}">{ic(icon)}</button>'
        for tid, icon, lab in TOOLS
    )
    colors = "".join(
        f'<button class="mk-swatch" type="button" data-mk-color="{cid}" aria-pressed="{"true" if cid=="red" else "false"}" aria-label="{lab}" title="{lab}"><span style="background:{hex_}"></span></button>'
        for cid, hex_, lab in SWATCHES
    )
    return f'''<div class="mk" data-markup>
<div class="mk-top">
<a class="back" href="#punch" aria-label="Back">{ic("chevron-left")}</a>
<div class="grow ell"><div class="mk-title">Sheet A-201</div><div class="xs t3 ell">REQ-1042 · Unit 3B · <span data-version-current>Version 1 · Ana Kim</span></div></div>
<button class="btn ghost icon" type="button" data-mk-versions-toggle aria-label="Saved versions" title="Versions">{ic("layers")}</button>
<button class="btn sm primary" type="button" data-mk-save>{ic("save","sm")}<span>Save version</span></button>
</div>
<div class="mk-sub"><span class="xs t3" data-mk-count>4 marks on this page</span><span class="grow"></span><span class="xs t3">Original plan never changes</span></div>
<div class="mk-versions hide panel" data-versions><div class="hd"><h2>Versions</h2></div><div data-version-list></div></div>
<div class="mk-stage drawing">
<div class="mk-sheet">{markup_plan_svg()}<canvas class="mk-layer" aria-hidden="true"></canvas>
<div class="mk-hit" role="img" aria-label="Markup layer. Draw with your finger or a stylus."></div></div>
</div>
<div class="mk-ask hide panel"><div class="bd col gap16">
<label class="field"><span data-ask-kind>Text on the plan</span><input class="input" data-ask-text maxlength="300"></label>
<p class="xs t3">Saving the markup adds a punch item when you drop a pin.</p>
<div class="row"><button class="btn grow" type="button" data-ask-cancel>Cancel</button>
<button class="btn primary grow" type="button" data-ask-ok>Add</button></div>
</div></div>
<div class="mk-tools">
<div class="mk-row" role="toolbar" aria-label="Drawing tools">{tools}</div>
<div class="mk-row" style="overflow:visible">
<div class="mk-undoredo" role="group" aria-label="Undo and redo">
<button class="mk-tool" type="button" data-mk-undo aria-label="Undo" title="Undo">{ic("undo-2")}</button>
<button class="mk-tool" type="button" data-mk-redo aria-label="Redo" title="Redo">{ic("redo-2")}</button>
</div>
<div class="mk-row grow" role="group" aria-label="Color">{colors}</div>
</div>
</div>
</div>'''

def markup_versions_screen():
    rows = [
        ("v1","Version 1 · Ana Kim","This morning (sample) · 4 marks"),
        ("v2","Version 2 · Sam Rivera","Saved 2 hours ago (sample) · 5 marks"),
    ]
    items = "".join(
        f'<a class="mk-sheet-btn" href="#markup" data-load-version="{vid}"><span class="mk-thumb">{markup_plan_svg()}</span>'
        f'<span class="grow"><b>{name}</b><div class="small t3">{when}</div></span>{ic("chevron-right")}</a>'
        for vid, name, when in rows
    )
    return f'''<p class="small t2">Each save is a new layer over the original sheet, which never changes. Open a version to keep drawing.</p>
<div class="panel"><div class="list mk-sheets">{items}</div></div>
<a class="btn primary lg block" href="#markup">{ic("pen","sm")}<span>Open the latest and draw</span></a>'''

def voice_notes_body():
    n1 = f'''<li class="li vn">
<div class="row gap6 wrap"><b class="grow">Ana Kim</b>{chip("Punch item 3","info")}<span class="chip">Example</span><span class="xs t3 mono">Today 11:18 AM · 0:18</span></div>
<div class="vn-text"><p lang="es">Hay una grieta en la viga sobre la abertura. Hay que hermanar con un 2x8 de 6 pies.</p>
<p class="vn-tr">{chip("Translated to English","warn")} <span lang="en">There's a crack in the joist above the opening. Sister it with a 2x8, 6 feet.</span></p>
<p class="xs t3">Sample transcript, labeled as an example. Customers never see voice notes.</p>
</div></li>'''
    n2 = f'''<li class="li vn">
<div class="row gap6 wrap"><b class="grow">Sam Rivera</b><span class="chip">Example</span><span class="xs t3 mono">Today 9:40 AM · 0:09</span></div>
<div class="vn-text"><p lang="en">Checked the paint match in 3B. Close enough to proceed.</p>
<p class="xs t3">Sample transcript, labeled as an example.</p>
</div></li>'''
    return f'''<div data-voice>
<section class="panel" aria-labelledby="vn-h"><div class="hd">{ic("mic","sm")}<h2 id="vn-h">Voice notes</h2>{chip("2")}</div>
<div class="bd col gap16">
<label class="field"><span>About</span>
<select class="input"><option>The whole job</option><option>3. Final paint after dry</option><option>2. Texture to match</option></select></label>
<div data-vn-idle class="col gap6">
<button class="btn primary lg block" type="button" data-vn-start>{ic("mic","sm")}<span>Record a voice note</span></button>
<p class="xs t3">Up to 3 minutes. If the microphone isn't allowed, this preview saves a sample note instead. A transcript is written in the language you speak; IVO staff can read a translation.</p>
</div>
<div data-vn-live class="vn-rec hide" role="status" aria-live="polite">
<span class="vn-dot" aria-hidden="true"></span>
<span class="grow mono">Recording <span data-vn-clock>0:00 / 3:00</span></span>
<button class="btn primary lg" type="button" data-vn-stop>{ic("square","sm")}<span>Stop and save</span></button>
</div>
</div>
<ul class="list vn-list" data-vn-list style="list-style:none;margin:0;padding:0">{n1}{n2}</ul>
</section>
</div>'''
