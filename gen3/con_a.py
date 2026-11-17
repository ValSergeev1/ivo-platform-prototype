from core import *
from vendors import today_invite_brief, today_invite_feed, fee_field, preferred_tag, invite_by_id

def WHY(name="Bluewater Flooring LLC", trade="Trade: flooring + drywall", score="Scorecard 4.7 · on-time 96%"):
    rows = [(trade,"weight 30"),("Coverage: Pierce County","weight 20"),("COI and license current","required"),(score,"weight 25"),("Capacity: 1 of 2 crews free Tue","weight 25")]
    r = "".join(f'<div class="row small">{ic("check","sm okc")}<span class="grow">{a}</span><span class="t3 mono xs">{b}</span></div>' for a,b in rows)
    return (f'<div class="inset"><div class="row between"><b class="small">Why {name}</b>{chip("Rules match 5 of 5","ok")}</div>'
            f'<div class="col gap6" style="margin-top:10px">{r}</div><p class="xs t3" style="margin-top:8px">Routing is rules-based and explainable. A person approves every pick.</p></div>')

def copilot():
    sug = [
        ("Approve change order CO-2", "REQ-1042 · +$620 · Maya already approved", "Joist sistering found on site. Photo evidence attached at 11:20 AM. New total $4,970 stays inside the customer's approval. Margin unchanged at 18%.", "#approvals"),
        ("Send 2 sub confirmation drafts", "BID-2201 · Harbor Air, Metro Drywall", "HVAC is the last unconfirmed trade. The price is an estimate until Harbor Air replies. Bid is due Fri 2:00 PM PT, so asking now leaves 3 business days.", "#bidsubs"),
        ("Reassign roof drain clog", "REQ-1053 · SLA at risk, 18 min", "Evergreen's crew is 42 min out. Cascade's on-call tech is 11 min away and covers plumbing in King County. Draft only.", "#dispatch"),
    ]
    cards = "".join(f'''<div class="sug" data-item><div class="row at"><span class="orb">{ic("sparkles","sm")}</span><div class="grow"><b class="small">{t}</b><div class="xs t3">{s}</div></div><span class="chip" data-status hidden></span></div>
<div class="why">{w}</div><div class="row wrap gap6"><button class="btn sm" type="button" data-explain aria-expanded="false">{ic("lightbulb","sm")}<span>Explain</span></button><a class="btn sm" href="{h}">{ic("arrow-up-right","sm")}<span>Open</span></a><button class="btn sm primary" type="button" data-set="Approved|ok" data-toast="Approved. Logged to the audit trail.">{ic("check","sm")}<span>Approve</span></button></div></div>''' for t,s,w,h in sug)
    return f'''<aside class="copilot" aria-label="IVO Copilot"><div class="hd"><span class="orb">{ic("sparkles","sm")}</span><div class="grow"><b>IVO Copilot</b><div class="xs t3">Explains, drafts, and asks before acting</div></div><button class="btn ghost icon sm" type="button" data-copilot-toggle aria-label="Close copilot">{ic("x")}</button></div>
<div class="bd" data-log>{note("I always ask an admin before I send a bid, message a sub or contractor, or change a job. Every action I take is written to the audit log.","shield-check","gate")}
<div class="eyebrow">Suggested for you · 3</div>{cards}
<div class="msg"><b>Copilot:</b> Bid leveling for BID-2201 is ready. I flagged one gap (HVAC) and one price change (electrical, +$5,500).</div></div>
<form class="ft" data-ask><label class="sr" for="ask">Ask the copilot</label><div class="row"><textarea id="ask" class="input" rows="1" style="min-height:44px" placeholder="Ask or tell me what to draft…"></textarea><button class="btn primary icon" aria-label="Send to copilot">{ic("arrow-up")}</button></div><div class="xs t3" style="margin-top:6px">Sample answers only. Drafts go to Approvals.</div></form></aside>'''

def s_today():
    k = "".join([
        kpi("SLA hit · 7 days", "94%", "▲ 3 pts vs last week", "okc", [88,90,89,91,92,93,94], "ok", "gauge"),
        kpi("Open work orders", "23", "6 urgent · 1 emergency", "t2", [18,19,22,21,24,22,23], "acc", "clipboard-list"),
        kpi("Bids due · 7 days", "3", "$1.24M in play", "t2", [1,2,2,3,2,3,3], "info", "file-text"),
        kpi("Waiting on you", "5", "Oldest 2h 10m", "warnc", [2,3,5,4,6,5,5], "warn", "inbox"),
    ])
    brief = f'''<section class="panel ai" data-coach="today-board" aria-labelledby="brief-h"><div class="hd"><span class="orb">{ic("sparkles","sm")}</span><h2 id="brief-h">Morning brief</h2><span class="grow"></span>{chip("Generated 7:00 AM PT","gold")}</div>
<div class="list">
{li("Confirm change order CO-2 on REQ-1042", "+$620 · customer already approved in the app", "file-pen-line", "gold", btn("Review","sm",href="#approvals"))}
{li("Submit BID-2201 by Fri 2:00 PM PT", "Cedar Ridge Elementary · AI-filled form ready · $442,000", "send", "info", btn("Open","sm",href="#bidform"))}
{li("Roof drain clog is 18 min from an SLA breach", "REQ-1053 · Harbor Point · suggest reassign", "siren", "urgent", btn("Dispatch","sm",href="#dispatch"))}
{today_invite_brief()}
</div></section>'''
    sla = "".join(f'''<div class="li"><span class="ic {c}">{ic(i)}</span><div class="grow"><div style="font-weight:550">{t}</div><div class="small t3">{s}</div></div><span class="mono num {tc}" data-countdown="{sec}" aria-label="time left"></span></div>''' for t,s,i,c,tc,sec in [
        ("Roof drain clog","REQ-1053 · Harbor Point · Urgent","droplets","urgent","urgc",1080),
        ("HVAC not cooling, medical office","Triage · Tacoma · Urgent","thermometer-sun","urgent","urgc",5400),
        ("Lobby LED retrofit · bids close","REQ-1051 · Cedar Court","lightbulb","info","t2",26*3600)])
    feed = timeline([
        ("map-pin","9:02 AM","Ana Kim checked in at Cedar Court","GPS verified · 2 photos · REQ-1042","now"),
        ("message-square-reply","8:51 AM","Summit Interiors confirmed $72,200","BID-2201 drywall · available Nov 30–Jan 15",""),
        ("inbox","8:40 AM","New request from Harbor Point","Roof drain clog · Urgent · AI suggests plumbing",""),
        ("file-check-2","8:12 AM","Package analyzed · BID-2210","Redding Clinic TI · 6 requirements, 2 risks",""),
    ] + today_invite_feed())
    pins = [("Tacoma","bad","REQ-1053 roof drain · SLA at risk","#job"),("Kent","","BID-2201 site · Cedar Ridge","#bidpkg"),("Lynnwood","ok","JOB-2175 courthouse doors","#bidwon"),("Bellevue","crew","Cascade Electric on call",None),("Portland","crew","2 crews ready",None),("Boise","crew","Coverage ready",None),("Redding","","BID-2210 clinic TI","#bidpkg")]
    legend = '<div class="legend" style="margin-top:12px"><span><i class="dot gold"></i>Job site</span><span><i class="dot bad"></i>At risk</span><span><i class="dot ok"></i>Won / active</span><span><i class="dot info"></i>Crew</span></div>'
    inner = f'''<div class="grid g4 kpis" style="margin-bottom:16px">{k}</div>
<div class="grid g-main-l" style="margin-bottom:16px">{brief}{panel("SLA timers", f'<div class="list">{sla}</div>', "timer", btn("All","sm ghost",href="#workorders"), bd="bd p0")}</div>
<div class="grid g-main-l">{panel("Live operations map", mapbox(pins, routes=[("Bellevue","Tacoma")]) + legend, "map", btn("Open dispatch","sm",href="#dispatch"), skel=True)}
{panel("Live activity", feed, "activity", '<span class="live">Live</span>', skel=True)}</div>
<div style="margin-top:16px">{note("Payments, text messages and store apps stay out of the launch build and show as <b>Later</b>.","clock-4")}</div>'''
    return screen("today", "Good morning, Dana", inner, "Today · Sat Nov 14 · Pacific", "", btn("New work order","",icon="plus",href="#triage") + btn("Ask copilot","primary",icon="sparkles",attrs=' data-copilot-toggle aria-expanded="false"'), default=True)

def s_dispatch():
    data = [("REQ-1053","Urgent","urgent","Roof drain clog","Harbor Point · Tacoma","Cascade Electric","fit 91","On-call tech 11 min away · plumbing in King + Pierce · COI current"),
            ("REQ-1060","Standard","","Door closer replacement","Cedar Court Bldg A · Tacoma","Bluewater · Ben Okafor","fit 84","Free 1–3 PM · 6 min from current job · general repair")]
    q = "".join(f'''<div class="kc dragcard" draggable="true" data-job="{j}" tabindex="0" aria-label="{j} {n}, drag to a crew lane"><div class="row between"><span class="id">{j}</span>{chip(t,c,True)}</div><h4>{n}</h4><div class="meta">{ic("map-pin","sm")}{w}</div>
<div class="inset" style="margin-top:10px;padding:10px"><div class="row small">{ic("sparkles","sm acc")}<span class="grow">Suggest <b>{s}</b></span><span class="mono xs t3">{sc}</span></div><div class="xs t3" style="margin-top:4px">{why}</div></div>
<div class="row wrap" style="margin-top:10px"><button class="btn sm primary" type="button" data-assign="{j}|{s}">{ic("calendar-plus","sm")}<span>Assign draft</span></button><span class="xs t3">or drag onto a lane</span></div></div>''' for j,t,c,n,w,s,sc,why in data)
    north = invite_by_id("northshore")
    lake = invite_by_id("lakeside")
    blocked = (
        '<div class="kc" data-job="REQ-1068" tabindex="0" aria-label="REQ-1068 Suite 4 paint touch-up, not assignable yet">'
        '<div class="row between"><span class="id">REQ-1068</span>' + chip("Standard", "", True) + '</div>'
        '<h4>Suite 4 paint touch-up</h4>'
        '<div class="meta">' + ic("map-pin", "sm") + "Cedar Court · Tacoma</div>"
        '<div class="row wrap" style="margin-top:8px">'
        + chip(ic("star", "sm") + "Preferred by customer", "gold")
        + chip("Not yet qualified", "warn", True)
        + "</div>"
        '<p class="xs t2" style="margin-top:8px">Harborline prefers <b>Northshore Paint Co. (sample)</b>. '
        "This vendor is not yet qualified and cannot be assigned until every required document is complete and staff approve it.</p>"
        '<div class="row wrap" style="margin-top:10px">'
        '<button class="btn sm" type="button" disabled aria-disabled="true">' + ic("lock", "sm") + "<span>Cannot assign</span></button>"
        '<a class="btn sm" href="#invited-vendors">' + ic("list-checks", "sm") + "<span>View checklist</span></a>"
        "</div></div>"
    )
    assignable = (
        '<div class="kc dragcard" draggable="true" data-job="REQ-1071" tabindex="0" aria-label="REQ-1071 Flooring punch, preferred qualified vendor">'
        '<div class="row between"><span class="id">REQ-1071</span>' + chip("Standard", "", True) + '</div>'
        "<h4>Corridor flooring punch</h4>"
        '<div class="meta">' + ic("map-pin", "sm") + "Cedar Court · Tacoma</div>"
        '<div class="row wrap" style="margin-top:8px">'
        + chip(ic("star", "sm") + "Preferred by customer", "gold")
        + chip("Qualified", "ok", True)
        + "</div>"
        '<p class="xs t2" style="margin-top:8px">Harborline prefers <b>Lakeside Flooring Inc. (sample)</b>, '
        "a customer-invited vendor who has completed qualification.</p>"
        + fee_field()
        + '<div class="row wrap" style="margin-top:10px">'
        '<button class="btn sm primary" type="button" data-assign="REQ-1071|Lakeside Flooring Inc. (sample)">'
        + ic("calendar-plus", "sm") + "<span>Assign draft</span></button>"
        '<span class="xs t3">or drag onto a lane</span></div></div>'
    )
    q = q + '<div class="col gap16" data-coach="dispatch-vendors">' + blocked + assignable + "</div>"

    crews = [("Bluewater · Ana Kim","AK",[(2,46,"REQ-1042 Unit 3B ceiling","gold")]),
             ("Bluewater · Ben Okafor","BO",[(0,18,"REQ-1059 hallway",""),(70,20,"REQ-1036 punch","")]),
             ("Evergreen Restoration","ER",[(10,40,"REQ-1048 water mitigation","")]),
             ("Cascade Electric","CE",[(30,30,"REQ-1051 site walk","")]),
             ("Summit Interiors","SI",[])]
    lanes = ""
    for n, ini, blocks in crews:
        b = "".join(f'<div class="blk {c}" style="left:{l}%;width:{w}%">{t}</div>' for l,w,t,c in blocks)
        lanes += f'<div class="lane"><div class="who"><span class="avatar navy sm">{ini}</span><div class="small" style="font-weight:600">{n}</div></div><div class="trk" data-crew="{n}" aria-label="{n} schedule">{b}<div class="nowline" style="left:24%" aria-hidden="true"></div></div></div>'
    hours = '<div class="hours"><span>Crew</span>' + "".join(f"<span>{h}</span>" for h in ["7a","8a","9a","10a","11a","12p","1p","2p","3p","4p"]) + "</div>"
    pins = [("Tacoma","bad","REQ-1053 roof drain · unassigned",None),("Kent","crew","Ana Kim · on site REQ-1042",None),("Seattle","crew","Ben Okafor · en route",None),("Bellevue","crew","Cascade Electric · on call",None),("Lynnwood","crew","Evergreen crew",None),("Portland","crew","Portland crews ready",None)]
    inner = f'''<div class="grid dgrid" style="margin-bottom:16px">
<section class="panel" aria-labelledby="uq"><div class="hd">{ic("inbox")}<h2 id="uq">Unassigned · 4</h2><span class="grow"></span>{chip("AI suggestions","gold")}</div><div class="bd col gap16">{q}<span class="chip ok" data-dispatch-status hidden></span></div></section>
{panel("Live crew map", mapbox(pins, routes=[("Seattle","Tacoma"),("Bellevue","Tacoma")], extra_cls="lg") + '<div class="legend" style="margin-top:12px"><span><i class="dot bad"></i>Unassigned, at risk</span><span><i class="dot info"></i>Crew position (sample)</span></div>', "radar", '<span class="live">Live</span>')}
</div>
{panel("Today's schedule · Puget Sound", f'<div class="tscroll"><div class="lanes">{hours}{lanes}</div></div>', "gantt-chart", btn("Week","sm ghost",icon="calendar",attrs=' data-toast="Week view (prototype)."'), bd="bd p0")}
<div style="margin-top:12px">{note("Assignments are drafts. Notifying a contractor waits in Approvals, and the address is released only after they accept.","shield-check","gate")}</div>'''
    return screen("dispatch", "Dispatch board", inner, "Operate", "Drag a job onto a crew lane, or take the AI suggestion. Every pick shows why.", btn("Auto-plan day","",icon="wand-sparkles",attrs=' data-toast="Draft plan ready for review. Nothing was sent."'))

WO = [("REQ-1053","Roof drain clog","Harbor Point","Urgent","urgent","Timer at risk","urgent","Evergreen Restoration","18 min","urgent waiting"),
      ("REQ-1042","Ceiling leak, Unit 3B","Harborline · Cedar Court","Urgent","urgent","On site","info","Bluewater Flooring","On track","urgent onsite"),
      ("REQ-1062","No power, suite 210","Pioneer Lofts","Emergency","emergency","Routing","warn","—","1h target","emergency waiting"),
      ("REQ-1051","Lobby LED retrofit","Harborline · Cedar Court","Standard","","Bidding","","3 invited","Fri 5 PM","standard"),
      ("REQ-1059","Hallway ceiling","Harborline · Cedar Court","Standard","","Scheduled","ok","Bluewater Flooring","Mon 8 AM","standard"),
      ("REQ-1048","Water mitigation, unit 12","Bayview Commons","Urgent","urgent","On site","info","Evergreen Restoration","On track","urgent onsite"),
      ("REQ-1060","Door closer replacement","Cedar Court Bldg A","Standard","","New","","—","2 days","standard waiting"),
      ("REQ-1044","Tenant turnover, suite 4","Rainier Office Park","Standard","","Closeout","ok","Summit Interiors","Sign-off","standard"),
      ("REQ-1039","ADA ramp handrail","Lakeside Medical","Standard","","Punch","info","Pacific Openings LLC","2 items","standard")]

def s_workorders():
    rows = "".join(f'''<tr data-st="{f}"><td class="lead" data-label="Work order"><a href="#job" class="mono">{i}</a> <span style="font-weight:550">{n}</span></td><td data-label="Customer">{c}</td><td data-label="Tier">{chip(t,tc,True)}</td><td data-label="Status">{chip(s,sc)}</td><td data-label="Assigned">{a}</td><td data-label="SLA" class="mono">{sla}</td></tr>''' for i,n,c,t,tc,s,sc,a,sla,f in WO)
    cols = [("New",["REQ-1060"]),("Routing",["REQ-1062","REQ-1053"]),("Bidding",["REQ-1051"]),("Scheduled",["REQ-1059"]),("On site",["REQ-1042","REQ-1048"]),("Punch & closeout",["REQ-1039","REQ-1044"])]
    d = {w[0]:w for w in WO}
    kb = ""
    for n, ids in cols:
        cards = "".join(f'<a class="kc{" hot" if d[x][3]!="Standard" else ""}" href="#job"><span class="id">{x}</span><h4>{d[x][1]}</h4><div class="meta">{chip(d[x][3],d[x][4],True)}<span>{d[x][2]}</span></div></a>' for x in ids)
        kb += f'<div class="colk"><header>{n}<span class="ct">{len(ids)}</span></header>{cards}</div>'
    fl = "".join(f'<button type="button" data-filter="{v}" aria-pressed="{"true" if v=="all" else "false"}">{l}</button>' for v,l in [("all","All 9"),("emergency","Emergency"),("urgent","Urgent"),("standard","Standard"),("waiting","Waiting")])
    inner = f'''<div class="row wrap between" style="margin-bottom:12px"><div class="seg wrapseg" data-filter-group data-target="#wo-table" role="group" aria-label="Filter">{fl}</div>
<div class="row wrap"><label class="sr" for="wo-q">Search work orders</label><input id="wo-q" class="input" style="width:200px" placeholder="Filter…" data-filter-input data-target="#wo-table">
<div class="seg" data-views role="group" aria-label="View"><button type="button" data-view="table" aria-pressed="true">{ic("table-2","sm")}List</button><button type="button" data-view="board" aria-pressed="false">{ic("kanban","sm")}Board</button></div></div></div>
<div data-pane="table" class="panel"><div class="tscroll" data-jk><table class="tbl cards" id="wo-table"><thead><tr><th>Work order</th><th>Customer</th><th>Tier</th><th>Status</th><th>Assigned</th><th>SLA</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="hd" style="border-top:1px solid var(--line);border-bottom:0"><span class="xs t3">Press <span class="kbd">J</span> <span class="kbd">K</span> to move, <span class="kbd">↵</span> to open · Saved views: Mine, At risk, This week</span></div></div>
<div data-pane="board" class="hide"><div class="kb">{kb}</div></div>'''
    return screen("workorders", "Work orders", inner, "Operate", "", btn("Export CSV","",icon="download",attrs=' data-toast="CSV prepared (prototype)."') + btn("New","primary",icon="plus",href="#triage"))

def s_triage():
    why_hvac = WHY("Harbor Air LLC", "Trade: HVAC", "Scorecard 4.6 · on-time 93%")
    cards = f'''<div class="panel" data-item data-coach="triage"><div class="hd">{ic("thermometer-sun")}<h2>HVAC not cooling, medical office</h2><span class="grow"></span>{chip("Urgent","urgent",True)}<span class="chip" data-status hidden></span></div><div class="bd grid g2">
<div class="col"><div class="small t3">Tacoma · public request form · 14 min ago · Lakeside Medical (new customer)</div>
<p class="small">“Exam rooms 3–6 are at 81°F and climbing. Patients are scheduled from 1 PM. Rooftop unit is making a clicking noise.”</p>
<div class="inset"><div class="row small">{ic("sparkles","sm acc")}<b>AI classification</b><span class="grow"></span><span class="mono xs t3">conf. 0.93</span></div>
<div class="row wrap gap6" style="margin-top:8px">{chip("HVAC","gold")}{chip("Repair")}{chip("Urgent · 4h tier","urgent")}{chip("Medical occupancy")}</div><p class="xs t3" style="margin-top:8px">Keywords: “not cooling”, “rooftop unit”, occupied clinic → Urgent per response-time tiers (draft).</p></div></div>
<div class="col">{why_hvac}
<div class="row wrap"><button class="btn primary" type="button" data-set="Confirmed · routing draft in Approvals|ok" data-hide=".alt">{ic("check","sm")}<span>Confirm type &amp; route</span></button><button class="btn alt" type="button" data-toast="Edit opened (prototype).">{ic("pencil","sm")}<span>Edit</span></button><button class="btn ghost alt" type="button" data-set="Asked to request first|info" data-toast="New customer goes through request first (option 1).">Invite flow</button></div></div></div></div>
<div class="panel" data-item><div class="hd">{ic("lightbulb")}<h2>Lobby lighting, evening work</h2><span class="grow"></span>{chip("Standard","",True)}<span class="chip" data-status hidden></span></div><div class="bd row wrap between">
<div class="small t3 grow">Bellevue · email intake · today 4:02 PM PT · AI: Electrical · 3 contractors match in King County, all COIs current</div>
<button class="btn" type="button" data-set="Confirmed|ok">{ic("check","sm")}<span>Confirm</span></button></div></div>
<div class="panel"><div class="hd">{ic("handshake")}<h2>Partner with IVO · Bluewater Flooring LLC</h2><span class="grow"></span>{chip("Contractor inquiry","info")}</div><div class="bd row wrap between">
<div class="small t3 grow">Inquiry #104 · flooring &amp; drywall · King, Pierce. Contractors join by invite after vetting (option A).</div>{btn("Open in Vetting","",href="#applications",ic_after="arrow-right")}</div></div>'''
    return screen("triage", "Triage inbox", f'<div class="col gap16">{cards}</div>', "Operate", "AI suggests type, trade and urgency. A person confirms every one.", chip("3 new","gold"))

def job_header():
    return f'''<div class="panel" style="padding:18px;margin-bottom:16px"><div class="row wrap between at"><div><div class="row wrap gap6"><span class="mono acc">REQ-1042</span>{chip("Urgent","urgent",True)}{chip("On site","info",True)}</div>
<h1 style="margin-top:6px">Ceiling leak, drywall &amp; paint</h1><div class="small t3" style="margin-top:4px">Cedar Court Apartments, Unit 3B · Tacoma, Pierce County · Harborline Property Group</div></div>
<div class="row wrap"><span class="avs"><span class="avatar">MO</span><span class="avatar navy">SR</span><span class="avatar navy">AK</span></span>{btn("Message","",icon="message-square",attrs=' data-toast="Draft opened. Sending waits for approval."')}{btn("Review CO-2","primary",icon="file-pen-line",href="#approvals")}</div></div>
<div style="margin-top:16px">{steps(["Received","Reviewed","Assigned","On site","Punch","Sign-off"],3)}</div></div>'''

def ptimeline(depth=2):
    days = [("Tue Nov 17", [("site","Arrival · GPS","9:02","CHECK-IN"),("slab","Ceiling opened","9:40","BEFORE"),("lock","Joist damage","11:20","CO-2")]),
            ("Mon Nov 16", [("exterior","Building exterior","1:05","SURVEY"),("office","Unit 3B hallway","1:12","SURVEY")])]
    return '<div class="ptl">' + "".join(f'<div class="day">{d}</div><div class="photos">{"".join(photo(i,c,w,t,depth) for i,c,w,t in ps)}</div>' for d,ps in days) + "</div>"

def job_tl():
    return timeline([
        ("inbox","Mon 8:12 AM","Request received","Maya Ortiz sent photos and a $4,800 not-to-exceed.",""),
        ("user-check","Mon 8:40 AM","IVO reviewed","Dana confirmed drywall &amp; paint, Urgent tier. Rules suggested Bluewater Flooring.",""),
        ("handshake","Mon 1:05 PM","Contractor accepted","Sam Rivera accepted. Address released after accept.",""),
        ("map-pin","Tue 9:02 AM","On site","Ana Kim checked in with GPS and a photo.",""),
        ("file-pen-line","Tue 11:20 AM","Change order CO-2 · +$620","Sister a joist. Maya approved in one tap. IVO confirmation waiting.","now"),
        ("list-checks","Next","Punch, sign-off and closeout package","After the work is done.","future")])

def s_job():
    fin = f'''<div class="col"><div class="row between small"><span class="t3">Not-to-exceed</span><b class="num">$4,800</b></div><div class="bar"><i style="width:91%"></i></div>
<div class="row between small"><span class="t3">Quote $4,350 + CO-2 $620</span><b class="num warnc">$4,970</b></div><div class="xs t3">CO-2 takes the job $170 over the original NTE. Maya approved the new total.</div></div>'''
    tabs = f'''<div class="seg wrapseg" role="tablist" aria-label="Job sections" style="margin-bottom:16px"><button role="tab" type="button" data-tab="ov" aria-selected="true">{ic("activity","sm")}Overview</button><button role="tab" type="button" data-tab="ph" aria-selected="false">{ic("images","sm")}Photos</button><button role="tab" type="button" data-tab="pu" aria-selected="false">{ic("map-pinned","sm")}Punch on plan</button><a href="#closeout">{ic("package-check","sm")}Closeout</a></div>'''
    inner = job_header() + tabs + f'''<div data-tabpane="ov" class="grid g-main-l">{panel("Live timeline", job_tl(), "activity", '<span class="live">Live</span>')}<div class="col gap16">{panel("Money", fin, "wallet")}{panel("Routing", WHY(), "route")}</div></div>
<div data-tabpane="ph" class="hide">{panel("Photo timeline · 5 photos", ptimeline(), "images", btn("Before/after","sm",href="#closeout"))}</div>
<div data-tabpane="pu" class="hide">{punch_plan()}</div>'''
    return screen("job", "", inner, crumb="REQ-1042")

def s_closeout():
    items = [("Before and after photos (12)",True,True),("Punch list closed · 5 of 5",True,True),("Customer sign-off",True,False),("Change orders summary (CO-1, CO-2)",True,True),("Lien waiver from Bluewater Flooring",True,True),("Warranty letter · 1 year workmanship",False,True),("Product data · paint and texture",False,False),("Final invoice amount (no payment at launch)",True,True),("Permit closeout",False,False)]
    cks = "".join(f'<label class="li check" style="cursor:pointer"><input type="checkbox"{" data-req" if r else ""}{" checked" if c else ""}><span class="grow">{t}</span>{chip("Required","gold") if r else chip("Optional")}</label>' for t,r,c in items)
    inner = f'''<div class="grid g-main-l" data-closeout data-coach="closeout"><section class="panel" aria-labelledby="co-h"><div class="hd">{ic("package")}<h2 id="co-h">Package contents</h2><span class="grow"></span><span class="small t3" data-co-count></span></div><div class="list">{cks}</div></section>
<section class="panel"><div class="bd col"><div class="row"><div class="ring"><span>0%</span></div><div><b>REQ-1042 closeout package</b><div class="small t3">PDF + photo archive · IVO branded</div></div></div>
{before_after()}
<button class="btn primary lg block" type="button" data-generate>{ic("package-check","sm")}<span>Assemble package</span></button><span class="chip" data-status hidden></span>
<p class="xs t3">Tick “Customer sign-off” to unlock. Assembling is internal; sending it to Harborline waits for admin approval.</p></div></section></div>'''
    return screen("closeout", "Closeout package builder", inner, "REQ-1042 · Ceiling leak, Unit 3B", "Pick what goes in. Required items unlock the package.", btn("Back to job","",icon="arrow-left",href="#job"))

def s_approvals():
    items = [("co","file-pen-line","gold","Change order CO-2","REQ-1042 · +$620 · customer approved","2h"),
             ("subs","send","info","Sub outreach · 2 drafts","BID-2201 · Harbor Air, Metro Drywall","1h"),
             ("bid","file-check-2","gold","Bid submission · $442,000","BID-2201 · Cedar Ridge Elementary","35m"),
             ("inv","users","","Bid invitations · 3 electricians","REQ-1051 · Lobby LED retrofit","3h"),
             ("dsp","calendar-check","warn","Dispatch draft","REQ-1053 → Cascade Electric","new")]
    lst = "".join(f'<button class="ap-item" type="button" data-ap="{k}" aria-selected="{"true" if n==0 else "false"}"><span class="apic {c}">{ic(i)}</span><span class="grow"><b class="small" style="display:block">{t}</b><span class="xs t3">{s}</span></span><span class="mono xs t3">{a}</span></button>' for n,(k,i,c,t,s,a) in enumerate(items))
    def pane(k, title, body, act, on=False):
        return f'''<div data-appane="{k}" class="{"" if on else "hide"}" data-item><div class="row between wrap"><h2>{title}</h2><span class="chip" data-status hidden></span></div><div class="stack" style="margin-top:12px">{body}</div>
<div class="row wrap" style="margin-top:16px"><button class="btn primary" type="button" data-set="Approved|ok" data-dec="#ap-count" data-toast="Approved and logged. (Prototype: nothing was sent.)">{ic("check","sm")}<span>{act}</span></button><button class="btn" type="button" data-toast="Opened for edits (prototype).">{ic("pencil","sm")}<span>Edit</span></button><button class="btn ghost" type="button" data-set="Rejected|bad" data-toast="Rejected and logged.">{ic("x","sm")}<span>Reject</span></button></div></div>'''
    panes = pane("co","Change order CO-2 · REQ-1042", f'<p class="small t2">Sister a ceiling joist found during demo. +$620. Maya Ortiz approved in the customer app at 11:34 AM.</p><div style="max-width:360px">{photo("lock","Joist damage","11:20","EVIDENCE")}</div><div class="inset small">New total $4,970 · original NTE $4,800 · margin 18%</div>', "Approve change order", True)
    panes += pane("subs","Sub outreach drafts · BID-2201", f'''<div class="inset"><div class="xs t3">To: Harbor Air LLC · estimating@harborair.example</div><p class="small" style="margin-top:6px">Please confirm your price of $94,800 for the four RTU replacements at Cedar Ridge Elementary, that your crew is available Nov 30–Jan 15, and that you can perform the work if IVO is awarded. Reply in the app or this thread.</p></div>
<div class="inset"><div class="xs t3">To: Metro Drywall Co. · follow-up</div><p class="small" style="margin-top:6px">Checking whether your crew frees up for Cedar Ridge Elementary drywall (18,400 SF, Level 4) between Nov 30 and Jan 15.</p></div>{note("The AI drafted these. It will not contact any sub until you approve.","shield-check","gate")}''', "Approve and send drafts")
    panes += pane("bid","Bid submission · BID-2201", f'<p class="small t2">AI-filled bid form for Northline Construction (sample GC). Base bid $442,000. Bond 5%. Addenda 1 and 2 acknowledged.</p><div>{btn("Open the filled form","",icon="file-text",href="#bidform")}</div>', "Approve and submit")
    panes += pane("inv","Bid invitations · REQ-1051", '<p class="small t2">Invite Cascade Electric, Pacific Current Electric and Lumen Works Electric (sample) to bid on the lobby LED retrofit. Deadline Fri Nov 20, 5:00 PM PT. Addresses stay hidden until a contractor accepts.</p>', "Approve invites")
    panes += pane("dsp","Dispatch draft · REQ-1053", f'<p class="small t2">Reassign the roof drain clog to Cascade Electric on-call (11 min away). Evergreen is released.</p>{WHY("Cascade Electric","Trade: plumbing (on-call)","Scorecard 4.5 · on-time 92%")}', "Approve dispatch")
    inner = f'''<div class="split"><section class="panel" aria-label="Approval queue"><div class="hd">{ic("inbox")}<h2>Waiting · <span id="ap-count">5</span></h2><span class="grow"></span>{chip("Oldest 2h","warn")}</div><div class="list" aria-label="Approvals">{lst}</div></section>
<section class="panel" aria-label="Approval detail"><div class="bd">{panes}</div></section></div>
<div style="margin-top:12px">{note("Everything that reaches a customer, contractor, sub or GC waits here: bids, sub messages, invites, change orders and dispatch. Open decision: whether the person who requested an approval can also approve it.","shield-check","gate")}</div>'''
    return screen("approvals", "Approvals", inner, "Operate", "One queue for every outgoing action. Approve, edit or reject with a reason.")
