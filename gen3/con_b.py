from con_a import *
from vendors import staff_directory, staff_vendor_detail, staff_notif_bell

BIDS = [("Found","BID-2212","Seattle Piers warehouse TI","Due Dec 4 · invitation received","New","",True,"#bidpkg"),
        ("Reviewing","BID-2210","Redding Clinic tenant improvement","Due Nov 25 · AI extracting","In review","info",False,"#bidpkg"),
        ("Pricing","BID-2198","Bellevue Library lighting","Due Nov 21, 3:00 PM PT","2 days","warn",False,"#bidlevel"),
        ("Sub confirmations","BID-2204","Tacoma Civic Annex HVAC","Due Nov 22 · 1 no reply","Waiting","warn",False,"#bidsubs"),
        ("Ready for approval","BID-2201","Cedar Ridge Elementary modernization","Due Fri Nov 20, 2:00 PM PT","Ready","gold",True,"#bidform"),
        ("Submitted","BID-2188","Portland Fire Station 12","Submitted Nov 12 · awaiting award","Out","",False,"#bidpkg"),
        ("Won","BID-2175","Lynnwood Courthouse doors","Awarded Nov 10 · job opened","Won","ok",False,"#bidwon"),
        ("Lost","BID-2162","Boise City Hall roof","Lost Nov 6 · price","Lost","bad",False,"#bidlost"),
        ("No-bid","BID-2207","Multnomah Parking garage","No-bid Nov 11 · capacity","No-bid","",False,"#bidpkg")]
IMP = lambda: chip(ic("download","sm")+"Imported from external platform","info")

def s_bidding():
    k = "".join([kpi("Due in 7 days","3","$1.24M total value","t2",None,icon="calendar-clock"),kpi("Waiting on your approval","2","1 bid, 1 outreach","warnc",None,icon="shield-check"),kpi("Subs to confirm","1","Harbor Air · HVAC","t2",None,icon="users"),kpi("Win rate · 90 days","31%","▲ 6 pts","okc",[22,24,25,27,28,30,31],"ok","trophy")])
    kb = ""
    for st,i,n,m,ch,c,imp,h in BIDS:
        extra = f'<div style="margin-top:8px">{IMP()}</div>' if imp else ""
        kb += f'<div class="colk"><header>{st}<span class="ct">1</span></header><a class="kc{" hot" if c=="gold" else ""}" href="{h}"><div class="row between"><span class="id">{i}</span>{chip(ch,c)}</div><h4>{n}</h4><div class="meta">{ic("calendar","sm")}{m}</div>{extra}</a></div>'
    rows = "".join(f'<tr><td class="lead" data-label="Bid"><a class="mono" href="{h}">{i}</a> {n}</td><td data-label="Stage">{st}</td><td data-label="Due">{m}</td><td data-label="Status">{chip(ch,c)}</td><td data-label="Source">{"Imported from external platform" if imp else "Direct invite"}</td></tr>' for st,i,n,m,ch,c,imp,h in BIDS)
    inner = f'''<div class="grid g4 kpis" style="margin-bottom:16px">{k}</div>
<div class="row between wrap" style="margin-bottom:12px">{gate("every filled bid and every sub message waits for admin approval")}<div class="seg" data-views role="group" aria-label="View"><button type="button" data-view="board" aria-pressed="true">{ic("kanban","sm")}Board</button><button type="button" data-view="table" aria-pressed="false">{ic("table-2","sm")}Table</button></div></div>
<div data-pane="board"><div class="kb" style="grid-auto-columns:minmax(240px,1fr)">{kb}</div></div>
<div data-pane="table" class="hide panel"><div class="tscroll"><table class="tbl cards"><thead><tr><th>Bid</th><th>Stage</th><th>Due</th><th>Status</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div></div>'''
    return screen("bidding", "Bidding pipeline", inner, "Win work · IVO as a subcontractor", "Outside contracts from GCs and owners. The AI reads packages, structures scope, levels sub quotes and fills the bid form.", btn("Integrations","",icon="plug",href="#integrations") + btn("Import invitation","primary",icon="download",attrs=' data-toast="Forward invites to the intake mailbox (sample)."'))

def bid_head(code="BID-2201", st=("Ready for approval","gold")):
    nav = [("bidpkg","Package"),("bidscope","Scope"),("bidsubs","Subs"),("bidlevel","Leveling"),("bidform","Bid form")]
    return f'''<div class="row wrap between" style="margin-bottom:16px"><div class="row wrap gap6">{btn("Pipeline","sm ghost",icon="arrow-left",href="#bidding")}<span class="mono acc">{code}</span>{chip(st[0],st[1])}{IMP()}<span class="chip warn">{ic("timer","sm")}Due in <span class="mono" data-countdown="{5*86400+16*3600}"></span></span></div>
<nav class="seg wrapseg navset" aria-label="Bid steps">{"".join(f'<a href="#{a}">{b}</a>' for a,b in nav)}</nav></div>'''

def s_bidpkg():
    docs = "".join(li(n, d, "file-text", "gold" if i==0 else "", chip(p)) for i,(n,d,p) in enumerate([("ITB_CedarRidge_sample.pdf","Invitation to bid","14 pp"),("Plans_A101-A140_sample.pdf","Architectural plans","40 sheets"),("Specs_Div09-26_sample.pdf","Specifications 9–26","212 pp"),("Addendum_02_sample.pdf","Night work, RTU note","3 pp")]))
    reqs = [("calendar-clock","Bid due Fri Nov 20, 2:00 PM PT","p3","ITB p. 3",""),("landmark","Bid bond 5% of base bid","p7","ITB p. 7",""),("shield","GL $2M, auto, workers’ comp","p7","ITB p. 8",""),("files","Acknowledge addenda 1 and 2","p3","ITB p. 4",""),("triangle-alert","Liquidated damages $1,500 / day","p11","ITB p. 11","bad"),("moon","Night work only in occupied wings","a2","Add. 2 p. 2","bad")]
    rl = "".join(f'<div class="li"><span class="ic {"bad" if c else "gold"}">{ic(i)}</span><div class="grow small" style="font-weight:550">{t}{" "+chip("Risk","bad") if c else ""}</div><button class="ref" type="button" data-page="{pg}" aria-label="Show source {r}">{r}</button></div>' for i,t,pg,r,c in reqs)
    L = '<span class="ln"></span>'
    def pg(pid, num, title, body, on=False):
        return f'<div class="docpg{" on" if on else ""}" data-docpage="{pid}"><div class="sheetpg"><div class="pg"><span>{"Addendum_02_sample.pdf" if pid=="a2" else "ITB_CedarRidge_sample.pdf"}</span><span>{num}</span></div><h3 class="h4">{title}</h3>{body}</div></div>'
    viewer = pg("p3","Page 3","1.4 Bid submission", f'{L}<p>Sealed bids are due <mark>Friday, November 20, 2026, at 2:00 PM local time</mark>. Late bids will not be opened.</p>{L}<p>Bidders shall acknowledge all addenda on the bid form.</p>{L*2}', True)
    viewer += pg("p7","Page 7","2.2 Bonds and insurance", f'{L}<p>Each bid shall be accompanied by a <mark>bid bond of five percent (5%)</mark> of the base bid.</p>{L}<p>Minimum insurance: <mark>general liability $2,000,000</mark>, automobile, and workers’ compensation as required by law.</p>{L}')
    viewer += pg("p11","Page 11","4.1 Time and liquidated damages", f'{L}<p>Substantial completion within 46 calendar days of notice to proceed. <mark>Liquidated damages of $1,500 per calendar day</mark> apply thereafter.</p>{L*2}')
    viewer += pg("a2","Page 2","Occupied wings", f'{L}<p>Work in Wings B and C shall be performed <mark>at night, 6:00 PM to 4:00 AM</mark>, while classes are in session. RTU sets require a crane after hours.</p>{L*2}')
    inner = bid_head() + f'''<div class="grid pkg3">
{panel("Documents · 4", f'<div class="list">{docs}</div>', "folder-open", bd="bd p0")}
<section class="panel" aria-label="Document viewer"><div class="hd">{ic("scan-text")}<h2>Source viewer</h2><span class="grow"></span>{chip("Click a page reference","gold")}</div><div class="bd"><div class="doc">{viewer}</div></div></section>
{panel("Requirements the AI found", f'<div class="list">{rl}</div><div class="bd" style="border-top:1px solid var(--line)"><p class="xs t3">Every line cites its page so you can check the AI. 2 risks raise contingency.</p></div>', "list-checks", bd="bd p0", skel=True)}</div>'''
    return screen("bidpkg", "Package analysis", inner, "BID-2201 · Northline Construction (sample GC)", "Cedar Ridge Elementary modernization · Sample School District · Kent, WA · due Fri Nov 20, 2026, 2:00 PM PT")

def s_bidscope():
    rows = [("09 29 00","Drywall · Level 4 finish, corridors and classrooms","18,400","SF","Specs 09 29 00 · A112","Drywall","0.96",""),
            ("09 65 19","Flooring · LVP, classrooms 101–118","6,200","SF","Specs 09 65 19","Flooring","0.94",""),
            ("26 51 00","Electrical · lighting package, rooms 101–118, controls","1","LS","Plans E201","Electrical","0.81","review"),
            ("23 74 00","HVAC · four RTU replacements, same size, after-hours set","4","EA","Specs 23 74 00 · Add. 2","HVAC","0.92",""),
            ("01 35 00","Night work premium, Wings B and C","1","LS","Add. 2 p. 2","General","0.77","review"),
            ("01 74 19","Construction waste and final clean","1","LS","Specs 01 74 19","General","0.90","")]
    tr = "".join(f'<tr><td data-label="CSI" class="mono">{a}</td><td class="lead" data-label="Line">{b}</td><td data-label="Qty" class="r mono">{c}</td><td data-label="Unit" class="mono">{d}</td><td data-label="Source"><span class="ref">{e}</span></td><td data-label="Trade">{chip(f,"gold")}</td><td data-label="Confidence">{chip(g,"warn" if h else "ok")}</td></tr>' for a,b,c,d,e,f,g,h in rows)
    inner = bid_head() + f'''<div class="grid g4 kpis" style="margin-bottom:16px">{kpi("Line items","6","from 4 documents",icon="list-tree")}{kpi("Trades","4 + general","Drywall, flooring, electrical, HVAC",icon="hard-hat")}{kpi("Needs review","2","confidence under 0.85","warnc",icon="eye")}{kpi("Pages read","269","in 41 seconds",icon="scan-text")}</div>
<div class="panel" data-item><div class="hd">{ic("list-tree")}<h2>Structured scope</h2><span class="grow"></span><span class="chip" data-status hidden></span></div><div class="tscroll"><table class="tbl cards"><thead><tr><th>CSI</th><th>Line</th><th class="r">Qty</th><th>Unit</th><th>Source</th><th>Trade</th><th>Confidence</th></tr></thead><tbody>{tr}</tbody></table></div>
<div class="hd" style="border-top:1px solid var(--line);border-bottom:0;flex-wrap:wrap"><span class="xs t3 grow">Low-confidence lines are flagged for a person to check.</span><button class="btn primary sm" type="button" data-set="Scope accepted|ok">{ic("check","sm")}<span>Accept structure</span></button></div></div>'''
    return screen("bidscope", "Scope structuring", inner, "BID-2201 · Cedar Ridge Elementary", "The AI split the package into trade line items with quantities and sources.")

def s_bidsubs():
    rows = [("Summit Interiors LLC","Drywall","$72,200","Nov 30–Jan 15","Open","Confirmed","ok"),("Bluewater Flooring LLC","Flooring","$86,400","Nov 30–Jan 15","Open","Confirmed","ok"),("Cascade Electric","Electrical",'$124,000 <span class="xs t3">was $118,500</span>',"Nov 30–Jan 15","Open","Price changed","warn"),("Harbor Air LLC","HVAC","$94,800 est.","—","—","No reply","bad"),("Metro Drywall Co.","Drywall (alt.)","—","—","Booked","Declined","")]
    tr = "".join(f'<tr><td class="lead" data-label="Sub"><b>{a}</b></td><td data-label="Trade">{b}</td><td data-label="Price" class="mono">{c}</td><td data-label="Dates">{d}</td><td data-label="Capacity">{e}</td><td data-label="Status">{chip(f,g,True)}</td></tr>' for a,b,c,d,e,f,g in rows)
    prog = f'<div class="col"><div class="row"><div class="ring" style="--p:60"><span>3/5</span></div><div class="small t2">3 of 5 confirmed. HVAC is the only open trade. Each sub confirms price, dates and capacity if IVO wins.</div></div>' + timeline([("check","Nov 13","Summit confirmed","Price and dates",""),("triangle-alert","Nov 13","Cascade changed price","+$5,500, controls allowance",""),("clock","Now","Harbor Air · no reply","Draft follow-up ready","now")]) + '</div>'
    inner = bid_head() + f'''<div class="grid g-main-l"><div class="panel" data-item><div class="hd">{ic("mail")}<h2>Drafts waiting · 2</h2><span class="grow"></span>{chip("Needs approval","warn")}<span class="chip" data-status hidden></span></div><div class="bd stack">
<div class="inset"><div class="row between"><div class="xs t3">To Harbor Air LLC · first request</div>{chip("AI draft","gold")}</div><p class="small" style="margin-top:6px">Please confirm your price of $94,800 for the four RTU replacements at Cedar Ridge Elementary, that your crew is available Nov 30–Jan 15, and that you can perform the work if IVO is awarded. Reply in the app or this thread.</p></div>
<div class="inset"><div class="row between"><div class="xs t3">To Metro Drywall Co. · follow-up</div>{chip("AI draft","gold")}</div><p class="small" style="margin-top:6px">Checking whether your crew frees up for Cedar Ridge Elementary drywall between Nov 30 and Jan 15.</p></div>
{note("Nothing is sent until you approve. Replies land in the vendor portal and update this table.","shield-check","gate")}
<div class="row wrap"><button class="btn primary" type="button" data-set="Approved · queued to send|ok" data-toast="Approved. Prototype: nothing was sent.">{ic("send","sm")}<span>Approve and send drafts</span></button><button class="btn" type="button" data-toast="Editor opened (prototype).">{ic("pencil","sm")}<span>Edit</span></button></div></div></div>
{panel("Confirmation progress", prog, "gauge")}</div>
<div class="panel" style="margin-top:16px"><div class="hd">{ic("users")}<h2>Confirmations</h2><span class="grow"></span>{btn("Open leveling","sm",href="#bidlevel",ic_after="arrow-right")}</div><div class="tscroll"><table class="tbl cards"><thead><tr><th>Subcontractor</th><th>Trade</th><th>Price</th><th>Dates</th><th>Capacity</th><th>Status</th></tr></thead><tbody>{tr}</tbody></table></div></div>'''
    return screen("bidsubs", "Sub outreach &amp; confirmations", inner, "BID-2201 · Cedar Ridge Elementary", "The AI matched each trade from the network and drafted a confirmation request.")

LEVEL = {
 "Drywall": (["Summit Interiors LLC","Northshore Walls (sample)","Metro Drywall Co."], [
    ("Base quote",["$72,200","$79,900","Declined"]),("Level 4 finish, 18,400 SF",["in","in","—"]),("Night work, Wings B & C",["in","ex +$6,400","—"]),
    ("Addenda 1 & 2 acknowledged",["in","in","—"]),("Cleanup",["in","in","—"]),("Leveled total",["$72,200","$86,300","—"])], 0),
 "Flooring": (["Bluewater Flooring LLC","Ridgeline Floors (sample)","Coastal Surfaces (sample)"], [
    ("Base quote",["$86,400","$81,200","$92,700"]),("LVP, 6,200 SF",["in","in","in"]),("Moisture testing",["in","ex +$3,900","in"]),
    ("Furniture moving",["in","ex +$2,100","ex +$2,600"]),("Addenda acknowledged",["in","in","in"]),("Leveled total",["$86,400","$87,200","$95,300"])], 0),
 "Electrical": (["Cascade Electric","Pacific Current Electric (sample)","Lumen Works Electric (sample)"], [
    ("Base quote",["$124,000 ↑","$131,500","No bid"]),("Lighting, rooms 101–118",["in","in","—"]),("Controls as specified",["allowance $6,000","in","—"]),
    ("Night work",["in","in","—"]),("Addenda acknowledged",["in","ex","—"]),("Leveled total",["$124,000","$131,500","—"])], 0),
 "HVAC": (["Harbor Air LLC","Coldwater Mechanical (sample)","Ridge Air Systems (sample)"], [
    ("Base quote",["$94,800 est.","$101,300","No reply"]),("4 RTUs, same size",["in","in","—"]),("Crane, after hours",["in","ex +$4,500","—"]),
    ("Curb adapters",["in","in","—"]),("Addenda acknowledged",["unconfirmed","in","—"]),("Leveled total",["$94,800 est.","$105,800","—"])], 0),
}
def lvl_table(trade):
    subs, rows, best = LEVEL[trade]
    def cell(v, ri, ci):
        cls = ""
        if v == "in":
            v = f'<span class="in">{ic("check","sm")}</span><span class="sr">Included</span>'
        elif v.startswith("ex"):
            cls = "gap"
            v = f'<span class="row gap4"><span class="ex">{ic("x","sm")}</span><span class="sr">Excluded</span>{v[3:]}</span>'
        elif "est." in v or "unconfirmed" in v or "No reply" in v: cls = "gap"
        elif "↑" in v or "allowance" in v: cls = "chg"
        if rows[ri][0] == "Leveled total" and ci == best: cls = "best"
        return f'<td class="{cls} mono">{v}</td>'
    head = "".join(f'<th scope="col">{s}</th>' for s in subs)
    body = "".join(f'<tr><th scope="row">{r[0]}</th>{"".join(cell(v,ri,ci) for ci,v in enumerate(r[1]))}</tr>' for ri, r in enumerate(rows))
    return f'<div class="tscroll"><table class="lvl"><caption class="sr">{trade} leveling</caption><thead><tr><th scope="col">{trade}</th>{head}</tr></thead><tbody>{body}</tbody></table></div>'

def s_bidlevel():
    tabs = "".join(f'<button role="tab" type="button" data-tab="lv-{t}" aria-selected="{"true" if i==0 else "false"}">{t}</button>' for i,t in enumerate(LEVEL))
    panes = "".join(f'<div data-tabpane="lv-{t}" class="{"" if i==0 else "hide"}">{lvl_table(t)}</div>' for i,t in enumerate(LEVEL))
    summary = "".join(f'<div class="li"><span class="grow small"><b>{t}</b> · {s}</span><span class="mono">{p}</span>{chip(c,cl)}</div>' for t,s,p,c,cl in [("Drywall","Summit Interiors","$72,200","Confirmed","ok"),("Flooring","Bluewater Flooring","$86,400","Confirmed","ok"),("Electrical","Cascade Electric","$124,000","Changed","warn"),("HVAC","Harbor Air","$94,800","Estimate","bad")])
    wf = [("Confirmed subs",0,64,"$282,600","",""),("HVAC estimate",64,21,"$94,800","est",""),("Markup",85,10,"$45,288","","markup"),("Contingency",95,5,"$18,870","","cont"),("Recommended",0,100,"$441,558","tot","total")]
    wfh = "".join(f'<div class="r"><span class="t2">{l}</span><span class="b"><i class="{c}" style="left:{a}%;width:{w}%"></i></span><span class="mono" style="text-align:right"{(" data-out="+o) if o else ""}>{v}</span></div>' for l,a,w,v,c,o in wf)
    calc = f'''<section class="panel glow" data-calc data-base="377400" aria-labelledby="rec-h"><div class="hd">{ic("sparkles")}<h2 id="rec-h">Recommended price</h2><span class="grow"></span>{chip("Confidence 72%","warn")}</div><div class="bd stack">
<div class="big" data-out="total">$441,558</div><p class="small t2">HVAC is still an estimate and the electrical price moved. Leveled confirmed quotes + historical RTU unit cost + liquidated-damages risk (ITB p. 11).</p>
<div class="wf">{wfh}</div>
<label class="field"><span>Markup <b class="mono" data-out="mpct">12%</b> · open decision</span><input class="range" type="range" min="6" max="20" value="12" data-markup></label>
<label class="field"><span>Contingency <b class="mono" data-out="cpct">5%</b></span><input class="range" type="range" min="0" max="12" value="5" data-cont></label>
<div class="inset"><div class="row between small"><span class="t2">Modeled win chance</span><b class="mono" data-out="winp">61%</b></div><div class="bar" style="margin-top:8px"><i data-out="winbar" style="width:61%"></i></div><div class="xs t3" style="margin-top:6px">From 38 past local bids (sample). Guidance, not a promise.</div></div>
<label class="field"><span>Your final base bid</span><input class="input mono" data-final value="$442,000"></label>
<div class="row wrap"><button class="btn" type="button" data-use-rec>{ic("copy","sm")}<span>Use recommended</span></button>{btn("Preview the bid form","primary",icon="file-text",href="#bidform")}</div></div></section>'''
    inner = bid_head() + f'''<div class="grid g-main"><div class="col gap16"><section class="panel" aria-labelledby="lv-h" data-tabscope><div class="hd" style="flex-wrap:wrap">{ic("table-2")}<h2 id="lv-h">Leveling grid</h2><span class="grow"></span><div class="seg wrapseg" role="tablist" aria-label="Trade">{tabs}</div></div><div class="bd">{panes}
<div class="legend" style="margin-top:12px"><span>{ic("check","sm okc")}Included</span><span>{ic("x","sm badc")}Excluded, priced back in</span><span><i class="dot warn"></i>Changed or allowance</span><span><i class="dot bad"></i>Gap</span><span><i class="dot ok"></i>Best leveled</span></div></div></section>
{panel("Selected per trade", f'<div class="list">{summary}</div>', "check-check", bd="bd p0")}</div>{calc}</div>'''
    return screen("bidlevel", "Leveling &amp; price", inner, "BID-2201 · Cedar Ridge Elementary", "Sub quotes normalized side by side. Exclusions are priced back in so totals compare fairly. You set the final number.")

def s_bidform():
    f = [("Bidder legal name","IVO Serv Group","Company profile"),("Project","Cedar Ridge Elementary modernization","ITB p. 1"),("Base bid","$442,000","Your final price"),("Calendar days to complete","46","ITB p. 11"),("Addenda acknowledged","Addendum 1, Addendum 2","ITB p. 4 · Add. 2"),("Bid bond","5% of the base bid, included","ITB p. 7"),("Insurance","GL $2M · auto · workers’ comp · COI on file","ITB p. 8"),("Authorized signature (you)","Val, IVO Serv Group (sample)","Applied only on approval")]
    fields = "".join(f'<label class="field"><span>{l}</span><input class="input ai" value="{esc(v)}"><span class="prov">{ic("sparkles","sm acc")}Filled from <span class="ref">{s}</span></span></label>' for l,v,s in f)
    checks = "".join(f'<div class="row small">{ic("circle-check","sm okc")}<span>{t}</span></div>' for t in ["All 8 required fields filled","Addenda match the package","Bond and insurance meet the ITB","Price matches leveling ($441,558 rec.)"])
    inner = bid_head() + f'''<div class="grid g-main"><section class="panel" aria-labelledby="bf-h"><div class="hd">{ic("file-text")}<h2 id="bf-h">Northline Construction bid form (sample)</h2><span class="grow"></span>{chip("AI-filled","gold")}</div><div class="bd"><div class="formgrid">{fields}</div></div></section>
<section class="panel glow" data-item aria-labelledby="ap-h"><div class="hd">{ic("shield-check")}<h2 id="ap-h">Submission approval</h2></div><div class="bd stack">{checks}
{note("Highlighted fields were filled by the AI from the package and your final price. Nothing is submitted until you approve.","shield-check","gate")}
<div class="row between"><span class="small t3">Status</span><span class="chip warn" data-status>Ready for approval</span></div>
<button class="btn primary lg block" type="button" data-set="Approved to submit|ok" data-toast="Marked approved. The bid was not sent (prototype).">{ic("send","sm")}<span>Approve and submit</span></button>
<p class="xs t3">Approving queues the submission and writes it to the audit log. The prototype does not send it to anyone.</p></div></section></div>'''
    return screen("bidform", "Bid form auto-fill", inner, "BID-2201 · AI-filled form", "Every field shows where it came from.")

def s_bidwon():
    flow = "".join(f'<div class="vstep {"on" if o else ""}"><span class="n">{ic(i,"sm")}</span><div><b>{t}</b><div class="small t3">{s}</div></div></div>' for i,t,s,o in [("trophy","Bid won","Awarded Nov 10, 2026 · $46,800",True),("briefcase","Job JOB-2175 created","Scope, schedule and budget copied from the bid",True),("users","Confirmed subs pre-assigned","Pacific Openings LLC, Cascade Electric",True),("file-check","Document check","COIs and W-9s must be current before work starts",False),("send","Kickoff notices","Drafted · waiting in Approvals",False)])
    inner = f'''<div class="grid g-main-l"><section class="panel"><div class="bd stack">{chip("Won","ok",True)}<h2>Lynnwood Courthouse doors</h2><p class="small t2">The won bid became a job automatically, with the confirmed subs already assigned.</p><div class="col gap16" style="margin-top:12px">{flow}</div>
<div class="row wrap" style="margin-top:12px">{btn("Open job timeline","primary",icon="activity",href="#job")}{btn("Review kickoff drafts","",icon="inbox",href="#approvals")}</div></div></section>
{panel("Pre-assigned subs", '<div class="list">'+li("Pacific Openings LLC","Doors and hardware · confirmed $38,400","door-open","ok",chip("Pre-assigned","ok"))+li("Cascade Electric","Power to operators · confirmed $6,200","zap","ok",chip("Pre-assigned","ok"))+'</div>', "users", bd="bd p0")}</div>'''
    return screen("bidwon", "Win → job", inner, "BID-2175 · Won", "")

def s_bidlost():
    bars = "".join(f'<div class="r"><span class="t2">{l}</span><span class="b"><i class="{c}" style="left:0;width:{w}%"></i></span><span class="mono" style="text-align:right">{v}</span></div>' for l,w,v,c in [("Our bid",100,"$186,400",""),("Est. low bid",88,"~$164,000","est"),("Membrane markup",70,"18% vs 11%","")])
    inner = f'''<div class="grid g2"><section class="panel"><div class="bd stack">{chip("Lost","bad",True)}<h2>Boise City Hall roof</h2><div class="wf">{bars}</div><div class="inset small">Reason: price, we were not the low bidder. Awarded at: not disclosed.</div></div></section>
{panel("What the pricing model learned", note("Markup on membrane roofing was high against recent local results. Flagged for the next similar bid. The change is proposed, not applied, until an admin approves it.","brain","gate") + '<div style="margin-top:12px">'+btn("Review proposed rule","",icon="sliders-horizontal",href="#settings")+'</div>', "graduation-cap")}</div>'''
    return screen("bidlost", "Loss review", inner, "BID-2162 · Lost", "Result recorded so the next price recommendation improves.")

def s_contractors():
    rows = [("Bluewater Flooring LLC","Flooring, drywall","King, Pierce","Current","ok",4.7,50),("Evergreen Restoration Co.","Water, rebuild","King, Snohomish","Current","ok",4.8,80),("Cascade Electric","Electrical, on-call plumbing","King, Multnomah","COI in 21 days","warn",4.5,30),("Summit Interiors LLC","Drywall, framing","Pierce, Thurston","Current","ok",4.6,60),("Pacific Openings LLC","Doors, hardware","Snohomish","Current","ok",4.4,40),("Harbor Air LLC","HVAC","Pierce, King","W-9 missing","bad",4.6,20)]
    tr = "".join(f'<tr><td class="lead" data-label="Company"><a href="#contractor">{a}</a></td><td data-label="Trades">{b}</td><td data-label="Coverage">{c}</td><td data-label="Docs">{chip(d,e,True)}</td><td data-label="Score" class="mono">{s}</td><td data-label="Booked" style="min-width:120px"><div class="bar" role="img" aria-label="{cap}% booked"><i style="width:{cap}%"></i></div></td></tr>' for a,b,c,d,e,s,cap in rows)
    inner = f'''<div class="grid g4 kpis" style="margin-bottom:16px">{kpi("In network","42","across 4 regions",icon="network")}{kpi("Docs expiring · 30d","3","reminders drafted","warnc",icon="file-warning")}{kpi("Avg response","22 min","to a direct offer",icon="timer")}{kpi("Trades covered","14","list still open",icon="hard-hat")}</div>
<div class="panel"><div class="hd">{ic("network")}<h2>Directory</h2><span class="grow"></span><label class="sr" for="c-q">Filter contractors</label><input id="c-q" class="input" style="max-width:200px" placeholder="Filter…" data-filter-input data-target="#c-table"></div><div class="tscroll" data-jk><table class="tbl cards" id="c-table"><thead><tr><th>Company</th><th>Trades</th><th>Coverage</th><th>Docs</th><th>Score</th><th>Booked</th></tr></thead><tbody>{tr}</tbody></table></div></div>'''
    return screen("contractors", "Contractor network", inner, "Network", "Invite-only. Every contractor was vetted and did a watched trial job.", btn("Invite a contractor","primary",icon="user-plus",href="#applications"))

def s_contractor():
    k = "".join([kpi("On-time","96%","last 20 jobs","okc",[90,92,94,93,95,96,96],"ok"),kpi("Callbacks","1","in 90 days","t2",None),kpi("Response","18 min","median to offers","t2",[30,26,24,22,20,19,18],"info"),kpi("Scorecard","4.7","of 5 · 34 reviews","t2",None)])
    docs = "".join(li(a,b,"file-check","ok",chip(d,"ok")) for a,b,d in [("Certificate of insurance","GL $2M · expires Apr 2, 2027","Current"),("WA contractor registration","Active · checked weekly","Active"),("W-9","On file","On file"),("Trial first job","REQ-0988 · watched · passed","Passed")])
    inner = f'''<div class="panel" style="padding:18px;margin-bottom:16px"><div class="row wrap"><span class="avatar" style="width:52px;height:52px;font-size:16px">BF</span><div class="grow"><h1>Bluewater Flooring LLC</h1><div class="small t3">Sam Rivera · flooring &amp; drywall · King, Pierce · joined by invite after vetting (option A)</div></div>{chip("Ready for routing","ok",True)}</div></div>
<div class="grid g4 kpis" style="margin-bottom:16px">{k}</div><div class="grid g2">{panel("Why the router picks them", WHY(), "route")}{panel("Compliance", f'<div class="list">{docs}</div>', "shield-check", bd="bd p0")}</div>'''
    return screen("contractor", "", inner, crumb="Bluewater Flooring LLC")

def s_applications():
    stages = [("Inquiry",[("Northwest Glazing (sample)","Glazing · King","Partner with IVO form · Triage #108")]),("Invited",[("Bluewater Flooring LLC","Flooring, drywall","Staff-vetted · Triage #104")]),("Documents",[("Ridgeline Floors (sample)","Flooring","COI uploaded · W-9 pending")]),("Compliance check",[("Lumen Works Electric (sample)","Electrical","Registration lookup active")]),("Watched trial job",[("Coldwater Mechanical (sample)","HVAC","REQ-1057 · supervisor assigned")]),("Ready for routing",[("Summit Interiors LLC","Drywall","Passed Oct 30")])]
    kb = ""
    for s, cs in stages:
        cards = ""
        for a,b,n in cs:
            act = f'<div class="row wrap" style="margin-top:10px"><button class="btn sm primary" type="button" data-set="Invite approved|ok" data-toast="Invite approved. Prototype: not sent.">{ic("send","sm")}<span>Approve invite</span></button><span class="chip" data-status hidden></span></div>' if s=="Invited" else ""
            cards += f'<div class="kc" data-item><h3 class="h4">{a}</h3><div class="meta">{b}</div><div class="xs t3" style="margin-top:6px">{n}</div>{act}</div>'
        kb += f'<div class="colk"><header>{s}<span class="ct">{len(cs)}</span></header>{cards}</div>'
    inner = note("Approved join process (option A, owner 2026-11-13): contractors are invite-only after staff vetting, with a closely watched trial first job. The Partner with IVO form lands in Triage; staff decide whether to invite.","badge-check","gate") + f'<div class="kb" style="margin-top:16px">{kb}</div>'
    return screen("applications", "Contractor vetting", inner, "Network", "")

def s_integrations():
    cards = [("Bid platforms and plan rooms","Pull invitations, plans and addenda from outside bidding platforms and plan rooms. Each real connection needs your approval and that platform's API access.","Available","info","radio-tower"),
             ("Email import of bid invites","A watched intake mailbox turns a forwarded invitation into a bid in Found, with attachments saved to the package.","Connected sample","ok","mail-plus"),
             ("Calendar","Push bid due dates and job windows to the staff calendar, and show sub availability you already confirmed.","Available","info","calendar"),
             ("Accounting","Send awarded job costs and, later, invoices. No payments are processed at launch.","Requires approval","warn","calculator"),
             ("File storage","Private storage for plans, specs and filled forms, with virus scanning and signed links.","Connected sample","ok","hard-drive"),
             ("Webhooks and API keys","Let approved systems create bids, post sub responses and receive status changes. Keys are scoped and can be revoked.","Requires approval","warn","webhook")]
    ch = "".join(f'<div class="panel"><div class="bd stack"><div class="row"><span class="apic gold">{ic(i)}</span><h2 class="grow h3">{t}</h2></div><div>{chip(s,c,True)}</div><p class="small t2">{b}</p><div class="row">{btn("Configure" if c=="ok" else "Request connection","sm",attrs=" data-toast=&quot;Connecting a real platform is a later, approved step.&quot;")}</div></div></div>' for t,b,s,c,i in cards)
    log = '<div class="code">POST /v1/hooks/bid.created   200  8:12:04 AM  BID-2212 (sample)\nPOST /v1/hooks/sub.response  200  8:51:22 AM  BID-2201 Summit Interiors\nPOST /v1/hooks/job.status    200  9:02:10 AM  REQ-1042 on_site</div>'
    inner = f'<div class="grid g3">{ch}</div><div style="margin-top:16px">{panel("Event log · sample", log, "terminal")}</div><div style="margin-top:12px">{note("The prototype does not call any outside system. Sample statuses only, no third-party names.","info")}</div>'
    return screen("integrations", "Integrations", inner, "System", "Connect outside tools for bidding and the rest of the work. Each real hookup needs your approval and that platform's API access.")

def s_settings():
    tiles = "".join(f'<button class="tile-btn" type="button" role="tab" data-tab="{k}" aria-selected="{"true" if k=="roles" else "false"}">{ic(i,"lg")}<b>{t}</b><span class="small t3">{s}</span></button>' for k,i,t,s in [("roles","users-round","Roles &amp; permissions","4 roles · matrix open"),("policy","shield-check","Approval policies","Gates on every outgoing action"),("routing","route","Routing rules","Weights and requirements"),("tiers","timer","Response-time tiers","Draft · open decision"),("notif","bell","Notifications","Email only at launch"),("sec","lock-keyhole","Security &amp; audit","Email-code sign-in")])
    roles = [("Owner admin","Yes","Yes","Yes","Everything"),("Staff","Draft","Draft","Draft","Assigned work"),("Customer","—","Own CO only","—","Own company"),("Contractor","—","—","Own bids","Own jobs")]
    rt = "".join(f'<tr><td class="lead" data-label="Role"><b>{a}</b></td><td data-label="Approve routing">{b}</td><td data-label="Approve CO">{c}</td><td data-label="Submit bids">{d}</td><td data-label="Sees">{e}</td></tr>' for a,b,c,d,e in roles)
    pol = ""
    for t,s,lk in [("Every outgoing bid needs admin approval","Owner rule · cannot be turned off",True),("Every message to a subcontractor needs admin approval","Owner rule · cannot be turned off",True),("AI asks before implementing anything","Copilot drafts only",True),("Change orders over NTE need IVO confirmation","After the customer approves",False),("Template emails to customers","Approve each send",False)]:
        lock = chip(ic("lock","sm")+"Locked on","gold") if lk else '<span class="toggle on" role="img" aria-label="On"></span>'
        pol += f'<div class="li"><div class="grow"><div style="font-weight:550">{t}</div><div class="small t3">{s}</div></div>{lock}</div>'
    rules = "".join(f'<div class="li"><span class="mono acc" style="width:44px">{w}</span><div class="grow small">{t}</div>{chip(c)}</div>' for w,t,c in [("req","COI, license and W-9 current","Required"),("30","Trade matches the request","Weight"),("20","Covers the county","Weight"),("25","Scorecard and on-time rate","Weight"),("25","Free capacity in the window","Weight")])
    tiers = "".join(f'<div class="li"><span class="ic {c}">{ic(i)}</span><div class="grow"><b>{t}</b><div class="small t3">{s}</div></div>{chip("Draft","later")}</div>' for t,s,i,c in [("Emergency","First answer 15 min · on site 2 h","siren","emergency"),("Urgent","First answer 1 h · on site 4 h","zap","urgent"),("Standard","Plan within 2 business days","clock","")])
    panes = f'''<div data-tabpane="roles" class="panel"><div class="hd" style="flex-wrap:wrap">{ic("users-round")}<h2>Role matrix</h2><span class="grow"></span>{chip("Open decision: second admin","warn")}</div><div class="tscroll"><table class="tbl cards"><thead><tr><th>Role</th><th>Approve routing</th><th>Approve CO</th><th>Submit bids</th><th>Sees</th></tr></thead><tbody>{rt}</tbody></table></div></div>
<div data-tabpane="policy" class="panel hide"><div class="hd">{ic("shield-check")}<h2>Approval policies</h2></div><div class="list">{pol}</div></div>
<div data-tabpane="routing" class="panel hide"><div class="hd">{ic("route")}<h2>Routing rules</h2><span class="grow"></span>{chip("Rules, not a model","gold")}</div><div class="list">{rules}</div></div>
<div data-tabpane="tiers" class="panel hide"><div class="hd">{ic("timer")}<h2>Response-time tiers</h2></div><div class="list">{tiers}</div></div>
<div data-tabpane="notif" class="panel hide"><div class="bd stack">{note("Email through the company mail relay at launch. Text messages are <b>Later</b>.","bell")}</div></div>
<div data-tabpane="sec" class="panel hide"><div class="list">{li("Sign-in","One-time code by email, no passwords","mail","gold")}{li("Session length","Open decision","timer","warn")}{li("Audit log","Append-only, hash-chained","scroll-text","ok",btn("Open","sm",href="#audit"))}</div></div>'''
    inner = f'<div data-tabscope><div class="grid g3" role="tablist" aria-label="Settings sections" style="margin-bottom:16px">{tiles}</div>{panes}</div>'
    return screen("settings", "Settings", inner, "System", "Who can do what, and what needs approval.", btn("Audit log","",icon="scroll-text",href="#audit"))

def s_audit():
    ev = [("9:02:10 AM","Ana Kim","contractor","checked in","REQ-1042","a41f…9c02","7be1…41aa"),("8:51:22 AM","System","integration","recorded sub response","BID-2201 · Summit","7be1…41aa","f03c…22d9"),("8:44:05 AM","Dana Whitfield","staff","confirmed triage","Inquiry · Tacoma HVAC","f03c…22d9","19d0…b7e4"),("8:40:31 AM","Copilot","AI","drafted 2 sub messages","BID-2201","19d0…b7e4","c6a2…0e15"),("8:12:44 AM","System","AI","analyzed package","BID-2210 · 6 requirements","c6a2…0e15","5e88…aa31"),("Fri 6:10 PM","Val","owner admin","approved change order","CO-1 · REQ-1042","5e88…aa31","90b4…7c6f"),("Fri 4:02 PM","Maya Ortiz","customer","approved change order","CO-2 · REQ-1042","90b4…7c6f","2d17…e820")]
    tr = "".join(f'<tr><td data-label="Time" class="mono">{a}</td><td class="lead" data-label="Actor"><b>{b}</b> <span class="xs t3">{c}</span></td><td data-label="Action">{d}</td><td data-label="Object">{e}</td><td data-label="Hash" class="hash">{f}</td><td data-label="Prev" class="hash">{g}</td></tr>' for a,b,c,d,e,f,g in ev)
    inner = f'''<div class="panel" style="margin-bottom:16px"><div class="bd row wrap between"><div class="row">{ic("shield-check","lg acc")}<div><b>Tamper-evident log</b><div class="small t3">Append-only. Each entry stores the hash of the one before it.</div></div></div><div class="row wrap"><span class="small" data-verify-out aria-live="polite">Not verified this session</span><button class="btn primary" type="button" data-verify="1284">{ic("scan-search","sm")}<span>Verify chain</span></button></div></div></div>
<div class="panel"><div class="hd" style="flex-wrap:wrap">{ic("scroll-text")}<h2>Events</h2><span class="grow"></span><label class="sr" for="au-q">Filter audit events</label><input id="au-q" class="input" style="max-width:220px" placeholder="Filter by actor, object…" data-filter-input data-target="#au-table">{btn("Export","sm",icon="download",attrs=' data-toast="Export prepared (prototype)."')}</div><div class="tscroll"><table class="tbl cards" id="au-table"><thead><tr><th>Time</th><th>Actor</th><th>Action</th><th>Object</th><th>Hash</th><th>Prev hash</th></tr></thead><tbody>{tr}</tbody></table></div></div>'''
    return screen("audit", "Audit log", inner, "System · Settings", "Who did what, when, including every AI draft and every approval.")

GROUPS = [("Operate",[("today","Today","layout-dashboard","","","t"),("dispatch","Dispatch","radar","2","","d"),("workorders","Work orders","clipboard-list","23","job closeout","w"),("triage","Triage","inbox","3","","r"),("approvals","Approvals","shield-check","!5","","a")]),
          ("Win work",[("bidding","Bidding","file-text","9","bidpkg bidscope bidsubs bidlevel bidform bidwon bidlost","b")]),
          ("Network",[("contractors","Contractors","network","42","contractor","c"),("invited-vendors","Invited vendors","handshake","!2","invited-vendor","n"),("applications","Vetting","badge-check","6","","v")]),
          ("System",[("integrations","Integrations","plug","","","i"),("settings","Settings","settings","","audit","s")])]

CMDS = [("Navigate","Today","#today","Command center","layout-dashboard"),("Navigate","Dispatch board","#dispatch","Map + lanes","radar"),("Navigate","Work orders","#workorders","List and board","clipboard-list"),("Navigate","Triage inbox","#triage","3 new","inbox"),("Navigate","Approvals","#approvals","5 waiting","shield-check"),("Navigate","Bidding pipeline","#bidding","9 bids","file-text"),("Navigate","Contractor network","#contractors","42","network"),("Navigate","Invited vendors","#invited-vendors","All customer invites","handshake"),("Navigate","Vendor qualification","#invited-vendor","Ridgeway checklist","list-checks"),("Navigate","Vetting","#applications","Option A","badge-check"),("Navigate","Integrations","#integrations","","plug"),("Navigate","Settings","#settings","Roles, policies","settings"),("Navigate","Audit log","#audit","Hash chain","scroll-text"),
        ("Records","REQ-1042 · Ceiling leak, Unit 3B","#job","On site","clipboard"),("Records","REQ-1042 closeout package","#closeout","Builder","package-check"),("Records","BID-2201 · Cedar Ridge Elementary","#bidpkg","Package","file-text"),("Records","BID-2201 scope","#bidscope","6 lines","list-tree"),("Records","BID-2201 leveling","#bidlevel","Rec. $441,558","table-2"),("Records","Bluewater Flooring LLC","#contractor","Score 4.7","hard-hat"),("Records","BID-2175 won → job","#bidwon","","trophy"),("Records","BID-2162 lost","#bidlost","","circle-x"),
        ("Actions","Approve change order CO-2","#approvals","Opens approval","check"),("Actions","Approve and submit BID-2201","#bidform","Admin approval","send"),("Actions","Review sub outreach drafts","#bidsubs","2 drafts","mail"),("Actions","Assign REQ-1053","#dispatch","Draft","calendar-plus"),("Actions","Verify audit chain","#audit","","shield-check")]

def build():
    screens = "".join([s_today(), s_dispatch(), s_workorders(), s_triage(), s_job(), s_closeout(), s_approvals(), s_bidding(), s_bidpkg(), s_bidscope(), s_bidsubs(), s_bidlevel(), s_bidform(), s_bidwon(), s_bidlost(), s_contractors(), s_contractor(), staff_directory(), staff_vendor_detail(), s_applications(), s_integrations(), s_settings(), s_audit()])
    bnav = [("today","Today","layout-dashboard",""),("dispatch","Dispatch","radar",""),("approvals","Approvals","shield-check",""),("bidding","Bids","file-text","bidpkg bidscope bidsubs bidlevel bidform bidwon bidlost")]
    body = os_shell("staff console", GROUPS, screens, bnav, copilot=copilot(), top_right=staff_notif_bell())
    page("console/index.html", "Staff console", body, depth=1, cmds=CMDS, app="IVO staff console")
