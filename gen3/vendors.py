"""Shared sample data and UI for customer-invited (managed) vendors. Preview only."""
from core import *

# Qualification items required of every network member, including customer-invited vendors.
# No shortcuts. Staff approval is the last gate; until then the vendor is "Not yet qualified".
QUAL_ITEMS = [
    ("biz", "Business license", "Where the firm is registered"),
    ("trade", "Trade license", "Required when the trade is licensed"),
    ("gl", "General liability insurance", "Certificate with expiry date"),
    ("wc", "Workers’ compensation insurance", "Certificate with expiry date"),
    ("w9", "W-9", "Taxpayer identification"),
    ("sub", "Signed IVO subcontract / terms", "Same terms as every network member"),
    ("safety", "Safety acknowledgment", "IVO safety expectations"),
    ("staff", "IVO staff approval", "A coordinator must approve before any assignment"),
]

# Fictional sample invitations only. Names, firms and emails are invented for the preview.
INVITES = [
    dict(
        id="northshore", company="Northshore Paint Co. (sample)", contact="Elena Vasquez",
        email="elena@northshore-paint.example", phone="(253) 555-0142", trade="Paint",
        customer="Harborline Property Group", person="Maya Ortiz",
        properties="Cedar Court Apartments", date="Nov 14, 2026",
        status="Invited", docs="Not started", preferred=True, qual="notyet",
        new=True, initials="NP",
        items={k: ("missing", "Not started") for k, *_ in QUAL_ITEMS},
    ),
    dict(
        id="pinnacle", company="Pinnacle Glass LLC (sample)", contact="Omar Haddad",
        email="omar@pinnacle-glass.example", phone="(206) 555-0177", trade="Glazing",
        customer="Harborline Property Group", person="Maya Ortiz",
        properties="Harbor Point", date="Nov 12, 2026",
        status="Applying", docs="3 of 8 complete", preferred=False, qual="notyet",
        new=True, initials="PG",
        items={
            "biz": ("ok", "WA UBI on file"),
            "trade": ("ok", "Not required for this trade"),
            "gl": ("ok", "Certificate · expires Mar 8, 2027"),
            "wc": ("missing", "Not uploaded"),
            "w9": ("missing", "Not uploaded"),
            "sub": ("missing", "Not signed"),
            "safety": ("missing", "Not signed"),
            "staff": ("pending", "Waiting on documents"),
        },
    ),
    dict(
        id="ridgeway", company="Ridgeway Mechanical (sample)", contact="Chris Nguyen",
        email="chris@ridgeway-mech.example", phone="(503) 555-0190", trade="HVAC",
        customer="Bayview Commons (sample)", person="Priya Shah",
        properties="Bayview Commons", date="Nov 10, 2026",
        status="Under review", docs="7 of 8 complete · awaiting staff approval", preferred=True, qual="notyet",
        new=False, initials="RM",
        items={
            "biz": ("ok", "OR license on file"),
            "trade": ("ok", "OR HVAC license current"),
            "gl": ("ok", "Certificate · expires Jun 30, 2027"),
            "wc": ("ok", "Certificate · expires Jun 30, 2027"),
            "w9": ("ok", "On file"),
            "sub": ("ok", "Signed Nov 11, 2026"),
            "safety": ("ok", "Signed Nov 11, 2026"),
            "staff": ("pending", "Ready for staff review"),
        },
    ),
    dict(
        id="lakeside", company="Lakeside Flooring Inc. (sample)", contact="Mei Chen",
        email="mei@lakeside-flooring.example", phone="(253) 555-0118", trade="Flooring",
        customer="Harborline Property Group", person="Jordan Lee",
        properties="Cedar Court Apartments", date="Oct 28, 2026",
        status="Approved", docs="Current", preferred=True, qual="ok",
        new=False, initials="LF",
        items={
            "biz": ("ok", "WA UBI on file"),
            "trade": ("ok", "Not required for this trade"),
            "gl": ("ok", "Certificate · expires Apr 2, 2027"),
            "wc": ("ok", "Certificate · expires Apr 2, 2027"),
            "w9": ("ok", "On file"),
            "sub": ("ok", "Signed Oct 29, 2026"),
            "safety": ("ok", "Signed Oct 29, 2026"),
            "staff": ("ok", "Approved Oct 30, 2026"),
        },
    ),
    dict(
        id="harborhw", company="Harbor Hardware Co. (sample)", contact="Luis Ortega",
        email="luis@harbor-hardware.example", phone="(206) 555-0133", trade="Doors & hardware",
        customer="Pioneer Lofts (sample)", person="Ken Walsh",
        properties="Pioneer Lofts", date="Nov 3, 2026",
        status="Not approved", docs="Incomplete", preferred=False, qual="notyet",
        new=False, initials="HH",
        items={
            "biz": ("ok", "WA UBI on file"),
            "trade": ("missing", "Not provided"),
            "gl": ("missing", "Limits did not meet IVO requirements"),
            "wc": ("missing", "Not uploaded"),
            "w9": ("ok", "On file"),
            "sub": ("missing", "Not signed"),
            "safety": ("missing", "Not signed"),
            "staff": ("no", "Not approved Nov 6, 2026"),
        },
    ),
    dict(
        id="clearview", company="Clearview Maintenance (sample)", contact="Dana Brooks",
        email="dana@clearview-maint.example", phone="(208) 555-0164", trade="General repair",
        customer="Lakeside Medical (sample)", person="Avery Cole",
        properties="Lakeside Medical", date="Sep 18, 2026",
        status="Approved", docs="Expired · assignment suspended", preferred=False, qual="suspended",
        new=False, initials="CM",
        items={
            "biz": ("ok", "ID license on file"),
            "trade": ("ok", "Not required for this trade"),
            "gl": ("bad", "Certificate expired Nov 1, 2026 · assignment suspended"),
            "wc": ("ok", "Certificate · expires Jan 15, 2027"),
            "w9": ("ok", "On file"),
            "sub": ("ok", "Signed Sep 20, 2026"),
            "safety": ("ok", "Signed Sep 20, 2026"),
            "staff": ("ok", "Approved Sep 22, 2026 · suspended after expiry"),
        },
    ),
    dict(
        id="willamette", company="Willamette Electric (sample)", contact="Jordan Blake",
        email="jordan@willamette-electric.example", phone="(503) 555-0188", trade="Electrical",
        customer="Rainier Office Park (sample)", person="Sam Park",
        properties="Rainier Office Park", date="Aug 2, 2026",
        status="Approved", docs="GL expires in 12 days · reminder drafted", preferred=True, qual="ok",
        new=False, initials="WE",
        items={
            "biz": ("ok", "OR license on file"),
            "trade": ("ok", "OR electrical license current"),
            "gl": ("warn", "Certificate · expires Nov 28, 2026 · reminder drafted"),
            "wc": ("ok", "Certificate · expires Mar 4, 2027"),
            "w9": ("ok", "On file"),
            "sub": ("ok", "Signed Aug 4, 2026"),
            "safety": ("ok", "Signed Aug 4, 2026"),
            "staff": ("ok", "Approved Aug 5, 2026"),
        },
    ),
]

STATUS_CHIP = {
    "Invited": "info",
    "Applying": "info",
    "Under review": "warn",
    "Approved": "ok",
    "Not approved": "bad",
}
QUAL_CHIP = {
    "notyet": ("Not yet qualified", "warn"),
    "ok": ("Qualified", "ok"),
    "suspended": ("Assignment suspended", "bad"),
}
ITEM_CHIP = {
    "ok": ("Complete", "ok"),
    "missing": ("Missing", "bad"),
    "pending": ("Waiting", "warn"),
    "warn": ("Expiring", "warn"),
    "bad": ("Expired", "bad"),
    "no": ("Not approved", "bad"),
}
ITEM_ICON = {
    "ok": "circle-check",
    "warn": "triangle-alert",
    "bad": "circle-alert",
    "missing": "circle-alert",
    "pending": "hourglass",
    "no": "circle-x",
}

TRADE_OPTIONS = [
    "Paint", "Glazing", "Flooring", "HVAC", "Electrical",
    "Plumbing", "Drywall", "Doors & hardware", "General repair", "Other",
]


def invite_by_id(vid):
    return next(v for v in INVITES if v["id"] == vid)


def customer_invites(customer="Harborline Property Group"):
    return [v for v in INVITES if v["customer"] == customer]


def new_invites():
    return [v for v in INVITES if v.get("new")]


def status_chip(status):
    return chip(status, STATUS_CHIP.get(status, ""), True)


def qual_chip(v):
    lab, cls = QUAL_CHIP[v["qual"]]
    return chip(lab, cls, True)


def can_assign(v):
    return v["qual"] == "ok"


def docs_ready(v):
    return all(v["items"][k][0] == "ok" for k, *_ in QUAL_ITEMS if k != "staff")


def trade_select(selected="Paint"):
    opts = []
    for t in TRADE_OPTIONS:
        sel = " selected" if t == selected else ""
        opts.append(f"<option{sel}>{t}</option>")
    return "".join(opts)


def standards_note(who="customer"):
    if who == "customer":
        return note(
            "Invited vendors complete the same license, insurance, document and process checks as every IVO network member. "
            "IVO staff must approve them before they can be assigned work. You can see their status here, but you cannot override it. "
            "Sample data only — nothing is sent or saved.",
            "shield-check", "gate")
    if who == "apply":
        return note(
            "The same checks apply to every vendor, including those invited by a property manager. "
            "There are no shortcuts. You cannot be assigned work until every required item is complete and IVO staff approves.",
            "shield-check", "gate")
    return note(
        "Customer-invited vendors must pass the same full qualification as any network member. "
        "Until every required item is complete and staff-approved, they show as <b>Not yet qualified</b> and cannot be assigned. "
        "Expiring documents trigger a reminder; expired documents automatically suspend assignment. "
        "The customer can see status but cannot override it. Sample data only — nothing is sent.",
        "shield-check", "gate")


def checklist_html(v):
    rows = []
    for key, title, sub in QUAL_ITEMS:
        st, detail = v["items"].get(key, ("missing", "Not started"))
        lab, cls = ITEM_CHIP.get(st, ("—", ""))
        icon = ITEM_ICON.get(st, "info")
        rows.append(li(title, f"{sub} · {detail}", icon, cls, chip(lab, cls, True)))
    done = sum(1 for k, *_ in QUAL_ITEMS if v["items"].get(k, ("missing",))[0] == "ok")
    head = (
        '<div class="row between wrap" style="margin-bottom:8px">'
        '<h3 class="h4" style="margin:0">Qualification checklist</h3>'
        f'<span class="small t3">{done} of {len(QUAL_ITEMS)} complete</span></div>'
    )
    return (
        head
        + f'<div class="panel" data-qual-list data-vendor="{esc(v["id"])}"><div class="list">'
        + "".join(rows)
        + "</div></div>"
    )


def preferred_tag(v):
    if not v["preferred"]:
        return ""
    return chip(ic("star", "sm") + "Preferred by customer", "gold")


def fee_field():
    return (
        '<label class="field" data-vendor-fee>'
        "<span>Managed vendor fee</span>"
        '<input class="input mono" placeholder="To be set by the owner" '
        'aria-label="Managed vendor fee, to be set by the owner">'
        '<span class="xs t3">Placeholder. The owner sets the fee on jobs with a customer-invited vendor. '
        "Preview only — nothing is saved.</span>"
        "</label>"
    )


def customer_vendor_screen():
    """Phone app: invite form + Harborline's invite list."""
    mine = customer_invites()
    cards = []
    for v in mine:
        pref = " · Preferred" if v["preferred"] else ""
        sub = f'{v["trade"]} · {v["properties"]}{pref}<br>{v["date"]} · {v["docs"]}'
        cards.append(
            li(v["company"], sub, "hard-hat", "", status_chip(v["status"]) + " " + qual_chip(v),
               attrs=f' data-st="{esc(v["status"])}" data-vendor="{esc(v["id"])}"')
        )
    form = f"""<form class="col gap16" data-vendor-invite-form data-coach="vendors" onsubmit="return false">
{standards_note("customer")}
<label class="field"><span>Vendor company</span><input class="input lg" name="company" value="Northshore Paint Co. (sample)" autocomplete="organization"></label>
<label class="field"><span>Contact name</span><input class="input lg" name="contact" value="Elena Vasquez" autocomplete="name"></label>
<label class="field"><span>Email</span><input class="input lg" name="email" value="elena@northshore-paint.example" inputmode="email" autocomplete="email"></label>
<label class="field"><span>Phone</span><input class="input lg" name="phone" value="(253) 555-0142" inputmode="tel" autocomplete="tel"></label>
<label class="field"><span>Trade</span><select class="input lg" name="trade">{trade_select()}</select></label>
<fieldset class="field" style="border:0;padding:0;margin:0"><legend class="lbl">Property or properties</legend>
<label class="li check"><input type="checkbox" name="property" value="Cedar Court Apartments" checked><span class="grow">Cedar Court Apartments</span></label>
<label class="li check"><input type="checkbox" name="property" value="Harbor Point"><span class="grow">Harbor Point</span></label>
</fieldset>
<div class="row between" style="align-items:center">
<div><div style="font-weight:550">Preferred for this property</div><div class="xs t3">IVO will see this when assigning work, after the vendor is qualified.</div></div>
<button type="button" class="toggle on" role="switch" aria-checked="true" data-pref-toggle aria-label="Preferred for this property"></button>
</div>
<button class="btn primary xl block" type="submit">{ic("send","sm")}<span>Send invite</span></button>
<p class="xs t3">Preview only. The invite is not emailed and nothing is saved.</p>
</form>"""
    listing = (
        '<section class="panel" aria-labelledby="vl-h" style="margin-top:8px">'
        f'<div class="hd"><h2 id="vl-h">Your invited vendors</h2><span class="grow"></span>'
        f'<span class="small t3">{len(mine)} · sample</span></div>'
        f'<div class="list" data-vendor-list>{"".join(cards)}</div></section>'
    )
    return form + listing


def portal_vendor_screen():
    mine = customer_invites()
    rows = []
    for v in mine:
        pref = preferred_tag(v) if v["preferred"] else ""
        rows.append(
            f'<tr data-st="{esc(v["status"])}">'
            f'<td class="lead" data-label="Vendor">{esc(v["company"])}</td>'
            f'<td data-label="Trade">{esc(v["trade"])}</td>'
            f'<td data-label="Property">{esc(v["properties"])}</td>'
            f'<td data-label="Invited">{esc(v["date"])}</td>'
            f'<td data-label="Status">{status_chip(v["status"])}</td>'
            f'<td data-label="Qualification">{qual_chip(v)} {pref}</td></tr>'
        )
    form = f"""<form class="formgrid" data-vendor-invite-form onsubmit="return false">
<label class="field"><span>Vendor company</span><input class="input" name="company" value="Northshore Paint Co. (sample)"></label>
<label class="field"><span>Contact name</span><input class="input" name="contact" value="Elena Vasquez"></label>
<label class="field"><span>Email</span><input class="input" name="email" value="elena@northshore-paint.example" inputmode="email"></label>
<label class="field"><span>Phone</span><input class="input" name="phone" value="(253) 555-0142" inputmode="tel"></label>
<label class="field"><span>Trade</span><select class="input" name="trade">{trade_select()}</select></label>
<fieldset class="field"><legend class="lbl">Property or properties</legend>
<label class="li check"><input type="checkbox" name="property" value="Cedar Court Apartments" checked><span class="grow">Cedar Court Apartments</span></label>
<label class="li check"><input type="checkbox" name="property" value="Harbor Point"><span class="grow">Harbor Point</span></label>
</fieldset>
<div class="field" style="justify-content:center">
<div class="row between" style="align-items:center">
<div><div style="font-weight:550">Preferred for this property</div><div class="xs t3">Shown to IVO at assignment, after the vendor is qualified.</div></div>
<button type="button" class="toggle on" role="switch" aria-checked="true" data-pref-toggle aria-label="Preferred for this property"></button>
</div></div>
<div style="grid-column:1/-1" class="row wrap">{btn("Send invite","primary",icon="send")}<span class="xs t3">Preview only. The invite is not emailed and nothing is saved.</span></div>
</form>"""
    table = (
        '<div class="tscroll"><table class="tbl cards"><thead><tr>'
        "<th>Vendor</th><th>Trade</th><th>Property</th><th>Invited</th><th>Status</th><th>Qualification</th>"
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )
    return (
        standards_note("customer")
        + '<div class="grid g-main" style="margin-top:16px">'
        + '<section class="panel" aria-labelledby="iv-h"><div class="hd">'
        + ic("user-plus") + '<h2 id="iv-h">Invite your vendor</h2></div><div class="bd">'
        + form + "</div></section>"
        + '<section class="panel" aria-labelledby="vl-h"><div class="hd">'
        + ic("handshake") + '<h2 id="vl-h">Your invited vendors</h2>'
        + '<span class="grow"></span><span class="small t3">Sample data</span></div>'
        + table + "</section></div>"
    )


def apply_invite_customer_panel():
    return f"""<div data-invite-customer hidden>
<p class="eyebrow acc">Step 2 of 9</p>
<h1>You've been invited.</h1>
<p class="t2 lead">Invited by <b>Harborline Property Group</b> (Maya Ortiz) for <b>Cedar Court Apartments</b>.</p>
<div class="panel glow"><div class="bd col gap16">
<div class="eyebrow">Customer invitation</div>
<p>Maya Ortiz at Harborline Property Group invited <b>Northshore Paint Co. (sample)</b> to join IVO as their vendor for Cedar Court Apartments.</p>
<p class="small t2">You complete the same license, insurance and document checks as every network member. You cannot be assigned work until every item is complete and IVO staff approves — no shortcuts.</p>
<p class="xs t3">Sample invitation · nothing was emailed.</p>
</div></div>
</div>"""


def apply_docs_customer():
    v = dict(invite_by_id("northshore"))
    v["items"] = dict(v["items"])
    v["items"]["biz"] = ("ok", "Uploaded in this preview (stays on your screen)")
    v["items"]["gl"] = ("ok", "Certificate uploaded · expires Mar 1, 2027")
    drop = f"""<div class="doc-drop" data-toast="Documents uploaded (preview). Nothing was sent.">
{ic("upload","lg")}
<b>Upload required documents</b>
<span class="small t2">Business license, trade license if required, GL and workers’ comp certificates (with expiry dates), W-9, signed subcontract and safety acknowledgment. PDF, JPEG or PNG.</span>
<input type="file" accept=".pdf,image/*" multiple class="sr" aria-label="Upload qualification documents">
</div>"""
    return '<div data-invite-customer hidden>' + standards_note("apply") + drop + checklist_html(v) + "</div>"


def apply_docs_ivo():
    v = dict(
        id="bluewater-apply",
        items={
            "biz": ("ok", "WA UBI on file"),
            "trade": ("ok", "Not required for this trade"),
            "gl": ("ok", "Certificate · expires Apr 2, 2027"),
            "wc": ("missing", "Not uploaded"),
            "w9": ("missing", "Not uploaded"),
            "sub": ("missing", "Not signed"),
            "safety": ("missing", "Not signed"),
            "staff": ("pending", "Waiting on documents"),
        },
    )
    drop = f"""<div class="doc-drop" data-toast="Documents uploaded (preview). Nothing was sent.">
{ic("upload","lg")}
<b>Upload license, insurance, W-9, subcontract and safety acknowledgment</b>
<span class="small t2">Certificates must show expiry dates. PDF, JPEG or PNG. Uploads in this preview stay on your screen.</span>
<input type="file" accept=".pdf,image/*" multiple class="sr" aria-label="Upload qualification documents">
</div>"""
    return '<div data-invite-ivo>' + standards_note("apply") + drop + checklist_html(v) + "</div>"


def apply_done_customer():
    v = dict(invite_by_id("northshore"))
    v["items"] = dict(v["items"])
    v["items"]["biz"] = ("ok", "Uploaded in this preview")
    v["items"]["gl"] = ("ok", "Certificate uploaded · expires Mar 1, 2027")
    recap = (
        '<div class="join-recap panel"><div class="list">'
        + li("Invited by", "Harborline Property Group · Maya Ortiz · Cedar Court Apartments", "handshake")
        + li("Northshore Paint Co. (sample)", "Elena Vasquez · paint", "hard-hat")
        + li("Status", "Under review · not yet qualified", "shield-check")
        + "</div></div>"
    )
    return (
        '<div class="join-done" data-invite-customer hidden>'
        f'<span class="apic warn" style="width:64px;height:64px">{ic("hourglass","xl")}</span>'
        '<p class="eyebrow acc">Application received</p>'
        "<h1>You're not yet qualified.</h1>"
        '<p class="t2 lead">Northshore Paint Co. (sample) has submitted its application. IVO staff still have to review every required item. '
        "You cannot be assigned work until the checklist is complete and staff approve it — the property manager cannot override this.</p>"
        + checklist_html(v)
        + recap
        + '<p class="xs t3">Preview only. Nothing was sent or saved. The first watched trial job comes only after qualification.</p>'
        "</div>"
    )


def staff_directory():
    new_n = len(new_invites())
    customers = sorted({v["customer"] for v in INVITES})
    trades = sorted({v["trade"] for v in INVITES})
    statuses = ["Invited", "Applying", "Under review", "Approved", "Not approved"]
    cust_opts = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in customers)
    trade_opts = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in trades)
    st_opts = "".join(f'<option value="{esc(s)}">{esc(s)}</option>' for s in statuses)

    queue = [v for v in INVITES if v["status"] in ("Invited", "Applying", "Under review")]
    qcards = []
    for v in queue:
        ready = v["status"] == "Under review" and docs_ready(v)
        if ready:
            acts = (
                '<div class="row wrap" style="margin-top:10px">'
                + btn("Review checklist", "sm primary", icon="list-checks", href="#invited-vendor")
                + f'<button class="btn sm" type="button" data-vendor-approve="{esc(v["id"])}" data-toast="Approval recorded (preview). Nothing was sent.">{ic("check","sm")}<span>Approve</span></button>'
                + f'<button class="btn sm" type="button" data-vendor-reject="{esc(v["id"])}" data-toast="Not approved (preview). Nothing was sent.">{ic("x","sm")}<span>Reject</span></button>'
                + "</div>"
            )
        else:
            open_btn = btn("Open", "sm", icon="list-checks", href="#invited-vendor") if v["id"] == "ridgeway" else ""
            acts = (
                '<div class="row wrap" style="margin-top:10px">'
                + open_btn
                + '<span class="xs t3">Cannot approve until every required document is on file.</span></div>'
            )
        qcards.append(
            f'<div class="kc" data-item data-vendor="{esc(v["id"])}">'
            f'<div class="row wrap gap6">{status_chip(v["status"])}{qual_chip(v)}</div>'
            f'<h3 class="h4" style="margin-top:8px">{esc(v["company"])}</h3>'
            f'<div class="meta">{esc(v["trade"])} · {esc(v["properties"])}</div>'
            f'<div class="xs t3" style="margin-top:6px">Invited by {esc(v["person"])}, {esc(v["customer"])} · {esc(v["date"])}<br>Docs: {esc(v["docs"])}</div>'
            f'{preferred_tag(v)}{acts}</div>'
        )

    rows = []
    for v in INVITES:
        href = "#invited-vendor" if v["id"] == "ridgeway" else "#invited-vendors"
        pref = chip("Preferred", "gold") if v["preferred"] else '<span class="t3">—</span>'
        st_tokens = " ".join(filter(None, [
            v["status"].lower().replace(" ", "-"),
            v["qual"],
            "preferred" if v["preferred"] else "",
            "new" if v.get("new") else "",
        ]))
        rows.append(
            f'<tr data-st="{esc(st_tokens)}" data-customer="{esc(v["customer"])}" data-status="{esc(v["status"])}" data-trade="{esc(v["trade"])}" data-vendor="{esc(v["id"])}">'
            f'<td class="lead" data-label="Vendor"><a href="{href}">{esc(v["company"])}</a>'
            f'<div class="xs t3">{esc(v["contact"])}</div></td>'
            f'<td data-label="Trade">{esc(v["trade"])}</td>'
            f'<td data-label="Invited by">{esc(v["customer"])}<div class="xs t3">{esc(v["person"])}</div></td>'
            f'<td data-label="Property">{esc(v["properties"])}</td>'
            f'<td data-label="Invite date">{esc(v["date"])}</td>'
            f'<td data-label="Status">{status_chip(v["status"])}</td>'
            f'<td data-label="Docs">{esc(v["docs"])}</td>'
            f'<td data-label="Preferred">{pref}</td>'
            f'<td data-label="Qualification">{qual_chip(v)}</td>'
            "</tr>"
        )

    filters = f"""<div class="row wrap gap16" data-vendor-filters style="margin-bottom:12px">
<label class="field grow"><span class="sr">Search invited vendors</span>
<input class="input" id="iv-q" placeholder="Search vendor, customer, property…" data-vendor-search></label>
<label class="field"><span>Customer</span><select class="input" data-vendor-filter="customer"><option value="">All customers</option>{cust_opts}</select></label>
<label class="field"><span>Status</span><select class="input" data-vendor-filter="status"><option value="">All statuses</option>{st_opts}</select></label>
<label class="field"><span>Trade</span><select class="input" data-vendor-filter="trade"><option value="">All trades</option>{trade_opts}</select></label>
</div>"""

    k = "".join([
        kpi("All invited", str(len(INVITES)), "from every customer", "t2", None, icon="handshake"),
        kpi("New invites", str(new_n), "waiting in Notifications", "warnc", None, icon="bell"),
        kpi("Not yet qualified", str(sum(1 for v in INVITES if v["qual"] == "notyet")), "cannot be assigned", "warnc", None, icon="hourglass"),
        kpi("Suspended", str(sum(1 for v in INVITES if v["qual"] == "suspended")), "expired documents", "t2", None, icon="ban"),
    ])

    inner = (
        standards_note("staff")
        + f'<div class="grid g4 kpis" style="margin:16px 0">{k}</div>'
        + f'<section class="panel" aria-labelledby="vq-h"><div class="hd">{ic("inbox")}<h2 id="vq-h">Approval queue · {len(queue)}</h2>'
        + '<span class="grow"></span>' + chip("Docs required before approval", "gold")
        + f'</div><div class="bd"><div class="grid g3">{"".join(qcards)}</div></div></section>'
        + '<section class="panel" style="margin-top:16px" aria-labelledby="vd-h"><div class="hd">'
        + ic("handshake") + '<h2 id="vd-h">All invited vendors</h2>'
        + '<span class="grow"></span><span class="small t3">Every customer invite · sample data</span></div>'
        + f'<div class="bd">{filters}<div class="tscroll" data-jk><table class="tbl cards" id="iv-table"><thead><tr>'
        "<th>Vendor</th><th>Trade</th><th>Invited by</th><th>Property</th><th>Invite date</th>"
        "<th>Status</th><th>Docs</th><th>Preferred</th><th>Qualification</th>"
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
        f'<p class="xs t3" data-vendor-count style="margin-top:8px">{len(INVITES)} vendors</p>'
        "</div></section>"
    )
    return screen(
        "invited-vendors", "Invited vendors", inner, "Network",
        "Every vendor any customer has invited. Search and filter by customer, status and trade.",
    )


def staff_vendor_detail():
    v = invite_by_id("ridgeway")
    acts = (
        f'<button class="btn primary" type="button" data-vendor-approve="{esc(v["id"])}" data-toast="Approval recorded (preview). Nothing was sent.">{ic("check","sm")}<span>Approve</span></button>'
        f'<button class="btn" type="button" data-vendor-reject="{esc(v["id"])}" data-toast="Not approved (preview). Nothing was sent.">{ic("x","sm")}<span>Reject</span></button>'
    )
    head = (
        '<div class="panel vendor-head" style="padding:18px;margin-bottom:16px">'
        '<div class="row" style="align-items:flex-start;gap:12px">'
        f'<span class="avatar" style="width:52px;height:52px;font-size:16px;flex:none">{esc(v["initials"])}</span>'
        f'<div class="grow"><h1 style="margin:0">{esc(v["company"])}</h1>'
        f'<div class="small t3" style="margin-top:6px">{esc(v["contact"])}</div>'
        f'<div class="small t3">{esc(v["email"])} · {esc(v["phone"])}</div>'
        f'<div class="small t3" style="margin-top:6px">Invited by {esc(v["person"])}, {esc(v["customer"])}</div>'
        f'<div class="small t3">{esc(v["properties"])} · {esc(v["date"])}</div>'
        f'<div class="row wrap gap6" style="margin-top:10px">{status_chip(v["status"])}{qual_chip(v)}{preferred_tag(v)}</div>'
        "</div></div></div>"
    )
    inv_list = (
        '<div class="list">'
        + li("Invited by", f'{v["customer"]} · {v["person"]}', "users")
        + li("Property", v["properties"], "building-2")
        + li("Trade", v["trade"], "hard-hat")
        + li("Preferred", "Yes — show this tag at dispatch after qualification" if v["preferred"] else "No", "star")
        + "</div>"
    )
    rule = (
        '<p class="small t2">This vendor is <b>Not yet qualified</b> and cannot be assigned to any job. '
        "The customer can see that status but cannot override it.</p>"
        + fee_field()
    )
    inner = (
        head
        + standards_note("staff")
        + '<div class="grid g-main" style="margin-top:16px"><div class="col gap16">'
        + checklist_html(v)
        + '<div class="row wrap">'
        + acts
        + btn("Back to directory", "", icon="arrow-left", href="#invited-vendors")
        + '</div><p class="xs t3">Approve is available only when every required document is on file. Preview only — nothing is sent.</p>'
        + '</div><div class="col gap16">'
        + panel("Invitation", inv_list, "mail", bd="bd p0")
        + panel("Assignment rule", rule, "ban")
        + "</div></div>"
    )
    return screen("invited-vendor", "", inner, crumb="Ridgeway Mechanical (sample)")


def staff_notifications_items():
    items = []
    for v in new_invites():
        items.append(
            li(
                f'New vendor invite · {v["company"]}',
                f'Invited by {v["person"]}, {v["customer"]} · {v["properties"]} · {v["date"]}',
                "bell", "gold", btn("Review", "sm", href="#invited-vendors"),
                attrs=f' data-vendor-note="{esc(v["id"])}"',
            )
        )
    return "".join(items)


def staff_notif_bell():
    notes = staff_notifications_items()
    n = len(new_invites())
    return f"""<div class="notif-wrap" data-notif>
<button class="btn sm icon" type="button" data-notif-toggle aria-expanded="false" aria-haspopup="true" aria-controls="notif-pop" aria-label="Notifications, {n} new vendor invites">{ic("bell")}<span class="notif-dot" aria-hidden="true">{n}</span></button>
<div class="notif-pop panel hide" id="notif-pop" role="menu" aria-label="New vendor invites">
<div class="hd"><h2 class="h4" style="margin:0">New invites</h2><span class="chip warn">{n} new</span></div>
<div class="list">{notes}</div>
<div class="bd">{btn("Open invited vendors","sm primary block",icon="handshake",href="#invited-vendors")}</div>
</div></div>"""


def today_invite_brief():
    return "".join(
        li(
            f'New vendor invite · {v["company"]}',
            f'Invited by {v["person"]}, {v["customer"]} · {v["properties"]} · {v["date"]}',
            "handshake", "gold", btn("Review", "sm", href="#invited-vendors"),
        )
        for v in new_invites()
    )


def today_invite_feed():
    evs = []
    for v in new_invites():
        evs.append((
            "handshake",
            v["date"].split(",")[0],
            f'New vendor invite · {v["company"]}',
            f'{v["person"]}, {v["customer"]} · {v["properties"]}',
            "now" if v["id"] == "northshore" else "",
        ))
    return evs
