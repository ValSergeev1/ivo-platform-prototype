"""Full-bleed join / sign-up stepper for customers and contractors. Sample data only."""
from core import *

CUSTOMER_STEPS = [
    ("role", "How you'll join"),
    ("company", "Your company"),
    ("property", "Properties"),
    ("request", "First request"),
    ("finish", "All done"),
]
CONTRACTOR_STEPS = [
    ("role", "How you'll join"),
    ("invite", "Your invitation"),
    ("code", "Sign in"),
    ("firm", "Company"),
    ("trades", "Trades"),
    ("area", "Service area"),
    ("docs", "License & insurance"),
    ("availability", "Availability"),
    ("done", "You're in"),
]

def _rail(steps, key):
    items = []
    for i, (sid, lab) in enumerate(steps, 1):
        items.append(
            f'<li><button type="button" class="join-rail-item" data-join-goto="{sid}">'
            f'<span class="n">{i:02d}</span><span>{lab}</span></button></li>'
        )
    return f'<ol class="join-rail-list" data-join-rail="{key}" hidden>{"".join(items)}</ol>'

def _role_step(default):
    def card(role, icon, title, sub, pressed):
        pr = "true" if pressed else "false"
        return (
            f'<button type="button" class="role-card" data-join-role="{role}" aria-pressed="{pr}">'
            f'<span class="apic gold" style="width:52px;height:52px">{ic(icon,"lg")}</span>'
            f'<b>{title}</b><span class="small t2">{sub}</span>{ic("arrow-right")}</button>'
        )
    return f'''<section class="join-step on" data-join-step="role" data-join-roles="customer contractor">
<p class="eyebrow acc">Join IVO</p>
<h1>How will you work with us?</h1>
<p class="t2 lead">One focused path. Customers send a request first; contractors join by invite after IVO vets them. Sample data only — nothing is sent or saved.</p>
<div class="role-pick" role="group" aria-label="Choose a role">
{card("customer","building-2","I'm a property owner or manager","Send a first request. After IVO reviews it, we invite you into the workspace.", default=="customer")}
{card("contractor","hard-hat","I bid and work as a contractor","Join by invitation, share trades, service area, license and insurance.", default=="contractor")}
</div>
</section>'''

def _customer_steps():
    otp = "".join(
        f'<input class="input mono" style="text-align:center;font-size:22px;padding:0;min-height:56px;width:100%" inputmode="numeric" maxlength="1" aria-label="Digit {i+1}" value="">'
        for i in range(6)
    )
    # otp not used in customer path (invite happens after review)
    return f'''
<section class="join-step" data-join-step="company" data-join-roles="customer">
<p class="eyebrow acc">Step 2 of 5</p>
<h1>Tell us about your company.</h1>
<p class="t2 lead">This becomes your workspace after IVO reviews your request.</p>
<label class="field"><span>Company name</span><input class="input lg" value="Harborline Property Group"></label>
<label class="field"><span>Your name</span><input class="input lg" value="Maya Ortiz"></label>
<label class="field"><span>Work email</span><input class="input lg" value="maya.ortiz@harborline.example" inputmode="email"></label>
</section>
<section class="join-step" data-join-step="property" data-join-roles="customer">
<p class="eyebrow acc">Step 3 of 5</p>
<h1>Where is the property?</h1>
<p class="t2 lead">Add the place this first request is about. You can add more later.</p>
<label class="field"><span>Property name</span><input class="input lg" value="Cedar Court Apartments"></label>
<label class="field"><span>Street address</span><input class="input lg" value="410 Sample Ave"></label>
<div class="row wrap gap16"><label class="field grow"><span>City</span><input class="input lg" value="Tacoma"></label>
<label class="field" style="width:100px"><span>State</span><input class="input lg" value="WA"></label></div>
<button class="btn" type="button" data-toast="A second property can be added after you're invited (preview).">{ic("plus","sm")}<span>Add another property</span></button>
</section>
<section class="join-step" data-join-step="request" data-join-roles="customer">
<p class="eyebrow acc">Step 4 of 5</p>
<h1>What needs doing?</h1>
<p class="t2 lead">No account needed yet. An IVO coordinator reviews this, then invites you.</p>
<label class="field"><span>Describe the work</span>
<textarea class="input lg" style="min-height:140px">Hallway ceiling stain after a supply-line leak. About 4 sq ft. Unit above already repaired.</textarea></label>
<div class="seg wrapseg" role="group" aria-label="Urgency">
<button type="button" aria-pressed="false">Emergency</button>
<button type="button" aria-pressed="false">Urgent</button>
<button type="button" aria-pressed="true">Standard</button>
<button type="button" aria-pressed="false">Planned</button>
</div>
<label class="field"><span>Not-to-exceed (optional)</span><input class="input lg mono" value="$2,500" inputmode="decimal"></label>
<button class="btn" type="button" data-toast="Photo added (preview)." data-ic="camera">{ic("camera","sm")}<span>Add a photo</span></button>
</section>
<section class="join-step" data-join-step="finish" data-join-roles="customer">
<div class="join-done">
<span class="apic ok" style="width:64px;height:64px">{ic("circle-check","xl")}</span>
<p class="eyebrow acc">Request received</p>
<h1>We've got it. IVO will review and invite you.</h1>
<p class="t2 lead">REQ-1059 is with a coordinator. Updates will arrive by email. After the invite, your request is already waiting in the workspace.</p>
<div class="join-recap panel"><div class="list">
{li("Harborline Property Group","Maya Ortiz · maya.ortiz@harborline.example","building-2")}
{li("Cedar Court Apartments","410 Sample Ave, Tacoma, WA","map-pin")}
{li("Hallway ceiling repair","Standard · NTE $2,500","hammer")}
</div></div>
<a class="btn primary xl block" href="../customer/index.html#invite">{ic("smartphone","sm")}<span>See the invitation in the customer app</span></a>
<p class="xs t3">Approved path (option 1, 13 Nov 2026): request first, then an invite after IVO reviews it. Staff can still set up a workspace for a company IVO already knows.</p>
</div>
</section>'''

def _contractor_steps():
    otp = "".join(
        f'<input class="input mono" style="text-align:center;font-size:22px;padding:0;min-height:56px;flex:1" inputmode="numeric" maxlength="1" aria-label="Digit {i+1}" value="{d}">'
        for i, d in enumerate("204816")
    )
    trades = [("Flooring", True), ("Drywall", True), ("Paint", False), ("Electrical", False), ("Plumbing", False), ("Roofing", False), ("Glazing", False), ("Doors & hardware", False)]
    trade_btns = "".join(
        f'<button type="button" class="pick-card" aria-pressed="{"true" if on else "false"}"><span>{n}</span></button>'
        for n, on in trades
    )
    areas = [("WA", "Washington", True), ("OR", "Oregon", False), ("ID", "Idaho", False), ("N. CA", "Northern California", False)]
    area_btns = "".join(
        f'<button type="button" class="pick-card area" aria-pressed="{"true" if on else "false"}"><b>{k}</b><span class="small t2">{n}</span></button>'
        for k, n, on in areas
    )
    return f'''
<section class="join-step" data-join-step="invite" data-join-roles="contractor">
<p class="eyebrow acc">Step 2 of 9</p>
<h1>You've been invited.</h1>
<p class="t2 lead">IVO vets contractors, then sends an invite. The first job is a closely watched trial.</p>
<div class="panel glow"><div class="bd col gap16">
<div class="eyebrow">Email from IVO</div>
<p>Dana at IVO Group invited <b>Bluewater Flooring LLC</b> to join the network.</p>
</div></div>
</section>
<section class="join-step" data-join-step="code" data-join-roles="contractor">
<p class="eyebrow acc">Step 3 of 9</p>
<h1>Check your email.</h1>
<p class="t2 lead">We sent a 6-digit code to <b>sam@bluewater.example</b>. No password.</p>
<fieldset style="border:0;padding:0;margin:0"><legend class="lbl" style="margin-bottom:8px">Sign-in code</legend>
<div class="otp row" style="gap:8px">{otp}</div></fieldset>
<button class="btn" type="button" data-fill-otp="204816">{ic("key-round","sm")}<span>Use sample code 204816</span></button>
</section>
<section class="join-step" data-join-step="firm" data-join-roles="contractor">
<p class="eyebrow acc">Step 4 of 9</p>
<h1>Your company.</h1>
<label class="field"><span>Legal name</span><input class="input lg" value="Bluewater Flooring LLC"></label>
<label class="field"><span>Doing business as (optional)</span><input class="input lg" value="Bluewater Flooring"></label>
<label class="field"><span>Primary contact</span><input class="input lg" value="Sam Rivera"></label>
</section>
<section class="join-step" data-join-step="trades" data-join-roles="contractor">
<p class="eyebrow acc">Step 5 of 9</p>
<h1>What work do you take on?</h1>
<p class="t2 lead">Pick every trade you want IVO to route to you. You can change this later.</p>
<div class="pick-grid" role="group" aria-label="Trades">{trade_btns}</div>
</section>
<section class="join-step" data-join-step="area" data-join-roles="contractor">
<p class="eyebrow acc">Step 6 of 9</p>
<h1>Where do you work?</h1>
<p class="t2 lead">IVO covers Washington, Oregon, Idaho and Northern California.</p>
<div class="pick-grid areas" role="group" aria-label="Service area">{area_btns}</div>
</section>
<section class="join-step" data-join-step="docs" data-join-roles="contractor">
<p class="eyebrow acc">Step 7 of 9</p>
<h1>License and insurance.</h1>
<p class="t2 lead">IVO only routes work when required documents are current. Uploads in this preview stay on your screen.</p>
<div class="doc-drop" data-toast="Documents uploaded (preview). Nothing was sent.">
{ic("upload","lg")}
<b>Upload license, COI and W-9</b>
<span class="small t2">PDF, JPEG or PNG. Drag in or tap to choose.</span>
<input type="file" accept=".pdf,image/*" multiple class="sr" aria-label="Upload license, insurance and W-9">
</div>
<div class="panel"><div class="list">{li("COI_sample.pdf","General liability $2M · virus-scanned","file-check","ok",chip("Uploaded","ok"))}{li("WA contractor license","Active · looked up automatically","badge-check","ok",chip("Verified","ok"))}</div></div>
</section>
<section class="join-step" data-join-step="availability" data-join-roles="contractor">
<p class="eyebrow acc">Step 8 of 9</p>
<h1>When can you start?</h1>
<p class="t2 lead">This helps IVO route the first, closely watched trial job.</p>
<div class="pick-grid" role="group" aria-label="Availability">
<button type="button" class="pick-card" aria-pressed="true"><b>This week</b><span class="small t2">Ready now</span></button>
<button type="button" class="pick-card" aria-pressed="false"><b>Next 2 weeks</b><span class="small t2">Scheduled work first</span></button>
<button type="button" class="pick-card" aria-pressed="false"><b>Next month</b><span class="small t2">Booking out</span></button>
</div>
<label class="field"><span>Crew you can send</span>
<select class="input lg"><option>2–3 people</option><option selected>4–6 people</option><option>7 or more</option></select></label>
</section>
<section class="join-step" data-join-step="done" data-join-roles="contractor">
<div class="join-done">
<span class="apic ok" style="width:64px;height:64px">{ic("badge-check","xl")}</span>
<p class="eyebrow acc">Welcome to the network</p>
<h1>You're in. Your first job is a watched trial.</h1>
<p class="t2 lead">Bluewater Flooring LLC is approved to receive work. IVO will watch the first job closely, then you'll be ready for regular routing.</p>
<div class="join-recap panel"><div class="list">
{li("Bluewater Flooring LLC","Sam Rivera · flooring & drywall","hard-hat")}
{li("Service area","Washington (add OR, ID or N. CA anytime)","map")}
{li("Documents","COI and license on file","shield-check")}
{li("Availability","This week · 4–6 people","calendar")}
</div></div>
<a class="btn primary xl block" href="../contractor/index.html#today">{ic("smartphone","sm")}<span>Open the contractor app</span></a>
<p class="xs t3">Approved path (option A, 13 Nov 2026): invite-only after vetting, with a watched trial first job. The public “Partner with IVO” form stays an inquiry; staff decide whether to invite.</p>
</div>
</section>'''

def join_body(default_role):
    other = "apply/index.html" if default_role == "customer" else "onboarding/index.html"
    other_lab = "Contractor join" if default_role == "customer" else "Customer join"
    other_href = f"../{other}" if default_role == "customer" else f"../{other}"
    # fix paths: from onboarding/, apply is ../apply/index.html; from apply/, onboarding is ../onboarding/index.html
    if default_role == "customer":
        other_href = "../apply/index.html"
        other_lab = "I'm a contractor instead"
    else:
        other_href = "../onboarding/index.html"
        other_lab = "I'm a customer instead"
    pitch_c = "Send a request first. After IVO reviews it, we invite you into a workspace — option 1, approved 13 Nov 2026."
    pitch_k = "IVO invites contractors after vetting. The first job is a closely watched trial — option A, approved 13 Nov 2026."
    pitch = pitch_c if default_role == "customer" else pitch_k
    return f'''<div class="join" data-join data-default-role="{default_role}">
<aside class="join-rail" aria-label="Join progress">
<a class="join-brand" href="../index.html"><img class="mark-d" src="../assets/img/ivo-mark-white.png" alt=""><img class="mark-l" src="../assets/img/ivo-mark-white.png" alt=""><span>IVO</span></a>
<p class="eyebrow" style="color:#e1c395">Join the network</p>
<h2 class="join-rail-title">One path. One question at a time.</h2>
<p class="join-rail-pitch small">{pitch}</p>
{_rail(CUSTOMER_STEPS, "customer")}
{_rail(CONTRACTOR_STEPS, "contractor")}
<div class="grow"></div>
<p class="xs t3x join-rail-note">Prototype · fictional sample data · nothing is sent or saved.</p>
<a class="join-switch xs" href="{other_href}">{other_lab} {ic("arrow-right","sm")}</a>
</aside>
<div class="join-stage">
<main id="main" class="join-main" tabindex="-1">
{_role_step(default_role)}
{_customer_steps()}
{_contractor_steps()}
</main>
<nav class="join-bar" aria-label="Step">
<button class="btn lg" type="button" data-join-prev>{ic("arrow-left","sm")}<span>Back</span></button>
<button class="btn primary xl grow" type="button" data-join-next><span>Continue</span>{ic("arrow-right","sm")}</button>
</nav>
</div>
</div>'''

def build_join(kind):
    role = "customer" if kind == "onboarding" else "contractor"
    title = "Customer join" if role == "customer" else "Contractor join"
    body = join_body(role)
    if role == "customer":
        cmds = [
            ("Join","How you'll join","#role","","users"),
            ("Join","Your company","#company","","building-2"),
            ("Join","Properties","#property","","map-pin"),
            ("Join","First request","#request","","clipboard"),
            ("Join","Finish","#finish","Request received","circle-check"),
            ("Prototype","Customer app invitation","../customer/index.html#invite","","smartphone"),
            ("Prototype","Contractor join","../apply/index.html","","hard-hat"),
        ]
        page("onboarding/index.html", title, body, cmds=cmds, app="IVO join")
    else:
        cmds = [
            ("Join","How you'll join","#role","","hard-hat"),
            ("Join","Your invitation","#invite","","mail"),
            ("Join","Sign in","#code","","key-round"),
            ("Join","Company","#firm","","building"),
            ("Join","Trades","#trades","","hammer"),
            ("Join","Service area","#area","WA, OR, ID, N. CA","map"),
            ("Join","License & insurance","#docs","","file-up"),
            ("Join","Availability","#availability","","calendar"),
            ("Join","Finish","#done","You're in","badge-check"),
            ("Prototype","Contractor app","../contractor/index.html#today","","smartphone"),
            ("Prototype","Customer join","../onboarding/index.html","","users"),
        ]
        page("apply/index.html", title, body, cmds=cmds, app="IVO join")
