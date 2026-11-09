"""Editorial 3D website for Noida Restaurant Web Studio.

Routes override the original showroom in app.py while preserving its
webhook, health endpoint and all existing links. No payment collection,
fake client claims, or outbound messaging.
"""
import html
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, Response

router = APIRouter()
H = lambda s: html.escape(str(s), quote=True)

CONCEPTS = {
    "modern": {
        "title": "Mitti & Masala", "style": "modern",
        "meta": "A warm, sculptural Indian dining website concept",
        "eyebrow": "01 / THE ART OF GATHERING",
        "headline": "A little spice.<br><i>A lot of soul.</i>",
        "description": "A table made for unhurried lunches, shared plates, and the familiar comfort of good Indian food.",
        "action": "Explore the table",
        "statement": "A familiar feeling,<br><i>made extraordinary.</i>",
        "statement_body": "Clay, warm light, natural textures and an invitation to stay a little longer. An editorial direction for an independent Indian restaurant.",
        "menu_heading": "From our imagined kitchen.",
        "menu_note": "Illustrative menu ideas for this design concept only.",
        "features": [("01", "The slow lunch", "Something to linger over."), ("02", "A little heat", "Comfort with character."), ("03", "A good gathering", "Make room for one more.")],
        "closer": "Make it feel like<br><i>your kind of place.</i>"
    },
    "bold": {
        "title": "FIREPAN", "style": "bold",
        "meta": "A bold street food website concept",
        "eyebrow": "02 / KEEP THE FIRE ON",
        "headline": "GOOD FOOD.<br><i>LOUD ENERGY.</i>",
        "description": "Big appetite. Late night plans. A bright, unapologetic digital home for a fast casual favourite.",
        "action": "Feel the heat",
        "statement": "NOT HERE TO<br><i>PLAY IT SAFE.</i>",
        "statement_body": "An energetic website concept with the attitude of a street food counter and the ease of a mobile first experience.",
        "menu_heading": "Cravings, illustrated.",
        "menu_note": "Fictional food concepts shown for design direction. No ordering here.",
        "features": [("01", "The main event", "A flame kissed classic."), ("02", "Bring the heat", "Built for big flavour."), ("03", "Your crew's spot", "Come hungry, stay loud.")],
        "closer": "FEED THE<br><i>CURIOSITY.</i>"
    },
    "minimal": {
        "title": "The Saffron Table", "style": "minimal",
        "meta": "A quiet luxury dining website concept",
        "eyebrow": "03 / THE BEAUTY OF LESS",
        "headline": "A slower way<br><i>to savour.</i>",
        "description": "Thoughtful flavours, generous space and the quiet pleasure of sitting down together.",
        "action": "Enter the experience",
        "statement": "The details<br><i>make the evening.</i>",
        "statement_body": "Warm stone, soft light, considered composition. An understated visual world for a restaurant where everything has its place.",
        "menu_heading": "A considered selection.",
        "menu_note": "Imagined menu themes for this concept. Not a real dining venue.",
        "features": [("01", "Seasonal", "An appreciation for what is here now."), ("02", "Thoughtful", "Nothing extra. Nothing missing."), ("03", "Together", "Good company is the best ingredient.")],
        "closer": "Every visit<br><i>has a feeling.</i>"
    }
}

def page(title, body, kind="studio", description=None, noindex=False):
    desc = H(description or "Distinctive restaurant websites for independent restaurants and cafés in Noida and Greater Noida. Three design concepts and transparent pricing from ₹3,000.")
    title = H(title)
    attrs = ' data-page="' + H(kind) + '"'
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#121713">
<meta name="description" content="{desc}">
{robots}
<title>{title}</title>
<link rel="icon" href="/assets/luxury-favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/luxury.css?v=2">
<script src="/assets/luxury-ui.js?v=2" defer></script>
<script type="module" src="/assets/luxury-3d.js?v=2"></script>
</head><body{attrs}>
<a class="skip-link" href="#main">Skip to content</a>
{body}
</body></html>"""

def nav(dark=True, demo=None):
    if demo:
        name = H(CONCEPTS[demo]["title"])
        return f"""<header class="site-header demo-header"><div class="nav-shell">
<a class="wordmark demo-wordmark" href="/samples/{demo}/" aria-label="{name} homepage">{name}</a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="Open menu"><span></span><span></span></button>
<nav id="site-menu" class="nav-actions" aria-label="Primary navigation">
<a href="#story">Philosophy</a><a href="#experience">The experience</a>
<a href="/" class="nav-cta">The studio <span aria-hidden="true">↗</span></a>
</nav></div></header>"""
    return """<header class="site-header"><div class="nav-shell">
<a href="/" class="wordmark" aria-label="Noida Restaurant Web Studio home"><span class="wordmark-icon">N<span class="mark-dot">.</span></span><span class="wordmark-copy">NOIDA<br>WEB STUDIO</span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="Open menu"><span></span><span></span></button>
<nav class="nav-actions" id="site-menu" aria-label="Primary navigation">
<a href="/#work">The work</a><a href="/#approach">Approach</a><a href="/#investment">Investment</a>
<a class="nav-cta" href="/quote">Request a quote <span aria-hidden="true">↗</span></a>
</nav></div></header>"""

def studio_footer():
    return """<footer class="studio-footer" id="contact">
<div class="footer-top"><a class="footer-brand" href="/">NOIDA <span>WEB STUDIO.</span></a>
<p>Independent website studio for restaurants and cafés.<br>Noida · Greater Noida · Delhi NCR</p></div>
<div class="footer-line"><span>Made to be useful. Designed to be remembered.</span><span><a href="/privacy">Privacy</a> <a href="/terms">Terms</a> <a href="/quote">Enquire ↗</a></span></div>
<p class="legal-note">All three portfolio restaurants are fictional concept studies, not real customers. No testimonials, customer results, bookings or ordering services are represented as real.</p>
</footer>"""

def studio_work():
    return """<section id="work" class="section work-section">
<div class="section-intro reveal"><span class="overline">01 &nbsp; / &nbsp; SELECTED CONCEPTS</span><h2>One city.<br><i>Three different moods.</i></h2>
<p>Not three versions of the same template. Three distinct starting points for a restaurant’s own identity.</p></div>
<div class="case-stack">
<a class="case-case reveal" href="/samples/modern/" aria-label="Explore Mitti and Masala design concept">
<div class="case-copy"><span class="overline">STUDY 001 / WARM MODERN</span><h3>Mitti <em>&</em><br>Masala</h3><p>Warm terracotta. Unhurried dining. An invitation to stay.</p><span class="case-link">Enter the concept <span aria-hidden="true">↗</span></span></div>
<div class="case-art case-modern" aria-hidden="true"><span class="art-top">MITTI & MASALA <span>MENU &nbsp; STORY &nbsp; VISIT</span></span><div class="art-disk art-disk-modern"><span>m<span class="disk-s">·</span>m</span></div><span class="art-bigtype">The good<br>kind of slow.</span><span class="art-corner">01 / A LITTLE SPICE</span></div></a>
<a class="case-case case-reversed reveal" href="/samples/bold/" aria-label="Explore FIREPAN design concept">
<div class="case-copy"><span class="overline">STUDY 002 / ELECTRIC EXPRESSION</span><h3 class="firepan-heading">FIREPAN</h3><p>For those who believe the first bite should make some noise.</p><span class="case-link">Enter the concept <span aria-hidden="true">↗</span></span></div>
<div class="case-art case-bold" aria-hidden="true"><span class="art-top">FIREPAN <span>EST. IN THE IMAGINATION</span></span><span class="art-bold-main">FEED<br>YOUR<br>FIRE.</span><div class="art-bold-ring"></div><span class="art-corner">02 / STREET ENERGY</span></div></a>
<a class="case-case reveal" href="/samples/minimal/" aria-label="Explore The Saffron Table design concept">
<div class="case-copy"><span class="overline">STUDY 003 / QUIET CONFIDENCE</span><h3>The Saffron<br><em>Table</em></h3><p>Space to breathe. Space to gather. Nothing more than needed.</p><span class="case-link">Enter the concept <span aria-hidden="true">↗</span></span></div>
<div class="case-art case-minimal" aria-hidden="true"><span class="art-top">THE SAFFRON TABLE <span>AN INVITATION TO SLOW DOWN</span></span><div class="art-disk art-disk-minimal"><span>ST</span></div><span class="art-minimal-type">A beautiful<br><i>little pause.</i></span><span class="art-corner">03 / QUIET DINING</span></div></a>
</div>
</section>"""

@router.get("/", response_class=HTMLResponse)
def studio():
    body = nav()+"""<main id="main">
<section class="studio-hero" aria-labelledby="hero-title">
<div class="hero-hairline" aria-hidden="true"><span>INDEPENDENT DIGITAL ATELIER</span><span>28.57° N &nbsp; 77.32° E</span></div>
<div class="hero-layout"><div class="hero-copy">
<span class="overline hero-enter">RESTAURANT WEBSITES &nbsp; / &nbsp; NOIDA + GREATER NOIDA</span>
<h1 id="hero-title" class="hero-enter">Your place.<br><em>In their plans.</em></h1>
<p class="hero-description hero-enter">A restaurant is more than a pin on a map. We design its home on the internet, with a menu, directions and one simple way to get in touch.</p>
<div class="hero-actions hero-enter"><a class="button button-light" href="/quote">Request your proposal <span aria-hidden="true">↗</span></a><a href="#work" class="text-link">Explore our concepts <span aria-hidden="true">↓</span></a></div>
<p class="hero-meta hero-enter">One-page websites from ₹3,000 · Clear scope before payment</p>
</div><div class="hero-sculpture">
<div class="sculpture-halo" aria-hidden="true"></div>
<div class="canvas-wrap"><div class="sculpture-fallback studio-fallback" aria-hidden="true"><i></i><b></b><span></span></div><canvas data-scene="studio" aria-hidden="true"></canvas></div>
<span class="sculpture-index">FORM STUDY / 001</span>
</div></div>
<div class="hero-bottom"><span>CRAFTED FOR INDEPENDENT RESTAURANTS</span><a href="#work">SCROLL TO EXPLORE <span aria-hidden="true">↓</span></a></div>
</section>
<div class="running-line" aria-hidden="true"><span>MENU</span><b>✳</b><span>LOCATION</span><b>✳</b><span>HOURS</span><b>✳</b><span>ONE TAP TO CALL</span><b>✳</b><span>MADE FOR MOBILE</span></div>
""" + studio_work() + """
<section class="declaration section" id="approach"><span class="overline reveal">02 &nbsp; / &nbsp; WHY WE EXIST</span>
<div class="declaration-inner"><h2 class="statement reveal">Good food is personal.<br><em>Its website should be too.</em></h2>
<p class="reveal">A menu should be easy to read. Your location should be easy to find. And the site should feel like the restaurant people actually walk into.</p>
</div><div class="approach-grid">
<div class="approach-item reveal"><span>01</span><h3>Know the place</h3><p>You share your menu, photos and the details that make the restaurant yours.</p></div>
<div class="approach-item reveal"><span>02</span><h3>Shape the experience</h3><p>We agree on the design, scope and working features before the build.</p></div>
<div class="approach-item reveal"><span>03</span><h3>Make it useful</h3><p>Mobile-first pages with readable menus, directions and clear contact actions.</p></div>
</div></section>
<section class="investment-section section" id="investment">
<div class="investment-intro reveal"><span class="overline">03 &nbsp; / &nbsp; THE INVESTMENT</span><h2>Clear from<br><i>the beginning.</i></h2><p>No inflated promises. A defined scope, written quote and room for the details that matter.</p></div>
<div class="price-list reveal">
<a class="price-row" href="/quote?package=Starter"><span class="price-number">01</span><div><h3>Starter</h3><p>One-page site · Menu highlights · Maps and contact links</p></div><strong>₹3,000</strong><span class="price-arrow" aria-hidden="true">↗</span></a>
<a class="price-row" href="/quote?package=Growth"><span class="price-number">02</span><div><h3>Growth</h3><p>Expanded menu · Gallery · Custom visual direction</p></div><strong>₹5,000</strong><span class="price-arrow" aria-hidden="true">↗</span></a>
<a class="price-row" href="/quote?package=Premium"><span class="price-number">03</span><div><h3>Premium</h3><p>More sections · Agreed integrations and added details</p></div><strong>₹8,000</strong><span class="price-arrow" aria-hidden="true">↗</span></a>
</div><p class="price-note reveal">Optional maintenance from ₹500/month. Domain, hosting upgrades and third-party services, if needed, are quoted separately. No payment required to request a proposal.</p>
</section>
<section class="closing section"><span class="overline reveal">NOIDA RESTAURANT WEB STUDIO</span>
<h2 class="reveal">Let's give them<br><em>somewhere to go.</em></h2>
<p class="reveal">Tell us what you serve. We'll help you find the right visual direction.</p>
<a href="/quote" class="button button-dark reveal">Start your website enquiry <span aria-hidden="true">↗</span></a>
<div class="closing-mark" aria-hidden="true">N<span>.</span></div></section>
</main>""" + studio_footer()
    return page("Noida Restaurant Web Studio — Editorial Restaurant Websites", body)

def demo_footer(style, d):
    return f"""<footer class="demo-footer"><div><span class="overline">{H(d['title'])}</span>
<p>Fictional restaurant design concept. Not a real restaurant, booking page or online ordering service. Menu descriptions are illustrative.</p></div><a href="/" class="text-link">Back to Noida Web Studio ↗</a></footer>"""

@router.get("/samples/{style}/", response_class=HTMLResponse)
def demo(style: str):
    d=CONCEPTS.get(style)
    if not d:
        raise HTTPException(404, "Unknown restaurant concept")
    cards="".join(f'<div class="demo-feature reveal"><span class="feature-num">{H(num)}</span><h3>{H(heading)}</h3><p>{H(body)}</p></div>' for num,heading,body in d["features"])
    body=f"""{nav(demo=style)}
<main id="main">
<section class="demo-hero" aria-labelledby="demo-title"><div class="demo-hero-inner">
<div class="demo-hero-copy"><span class="overline hero-enter">{H(d['eyebrow'])}</span>
<h1 id="demo-title" class="hero-enter">{d['headline']}</h1>
<p class="hero-description hero-enter">{H(d['description'])}</p>
<a href="#experience" class="demo-primary hero-enter">{H(d['action'])} <span aria-hidden="true">↗</span></a>
<p class="demo-concept-note hero-enter">A DESIGN CONCEPT · NOT AN OPERATING RESTAURANT</p>
</div><div class="demo-hero-art"><div class="canvas-wrap">
<div class="sculpture-fallback demo-fallback" aria-hidden="true"><i></i><b></b><span></span></div>
<canvas data-scene="{H(style)}" aria-hidden="true"></canvas></div>
<div class="art-stamp" aria-hidden="true">EST. IN THE IMAGINATION &nbsp; / &nbsp; NOIDA CONCEPT SERIES</div></div>
</div><div class="demo-hero-bottom"><span>CONCEPT STUDY / {H(style.upper())}</span><span>SCROLL TO EXPLORE ↓</span></div></section>
<section class="demo-story section" id="story">
<div class="overline reveal">01 / THE PHILOSOPHY</div>
<div class="demo-story-grid"><h2 class="reveal">{d['statement']}</h2><p class="reveal">{H(d['statement_body'])}</p></div></section>
<section class="demo-experience section" id="experience"><div class="demo-experience-head"><span class="overline reveal">02 / WHAT THE EXPERIENCE FEELS LIKE</span>
<h2 class="reveal">{H(d['menu_heading'])}</h2><p class="reveal">{H(d['menu_note'])}</p></div>
<div class="demo-feature-list">{cards}</div></section>
<section class="demo-close section"><span class="overline reveal">THIS IS A DESIGN DIRECTION</span>
<h2 class="reveal">{d['closer']}</h2>
<p class="reveal">Imagine this identity shaped around your real menu, photography and story.</p>
<a class="demo-primary reveal" href="/quote">Discuss a website like this <span aria-hidden="true">↗</span></a>
</section></main>{demo_footer(style,d)}"""
    return page(f"{d['title']} | Restaurant Design Concept — Noida Web Studio",body,kind=style,description=d["meta"],noindex=True)

@router.get("/quote",response_class=HTMLResponse)
def quote():
    email = H(os.environ.get("CONTACT_EMAIL","").strip())
    disabled = "" if email else "disabled"
    body = nav()+f"""<main id="main" class="quote-page">
<section class="quote-hero"><div class="quote-heading"><span class="overline hero-enter">A CONVERSATION STARTS HERE</span>
<h1 class="hero-enter">Tell us about<br><em>your place.</em></h1>
<p class="hero-enter">A few details are enough to get started. You'll receive a written scope before any payment discussion.</p></div>
<div class="quote-disc" aria-hidden="true"><span class="quote-disc-inner">N<span>.</span></span><span class="quote-disc-outer"></span></div></section>
<section class="quote-content section"><div class="quote-aside reveal"><span class="overline">THE PROCESS / 001</span>
<h2>A beautiful site<br><i>starts with a real story.</i></h2>
<p>Choose a direction. Share what matters. We'll discuss the scope, visuals and functionality before preparing a quote.</p>
<div class="quote-steps"><div><b>01</b><span>Tell us what you need</span></div><div><b>02</b><span>Review the proposal</span></div><div><b>03</b><span>Agree on the build</span></div></div>
<a class="text-link" href="/#work">Explore the concept studies ↗</a></div>
<div class="quote-form-wrap reveal"><span class="overline">YOUR ENQUIRY</span>
<h2>Your next chapter.</h2>
<form id="luxury-enquiry" class="quote-form" data-email="{email}" novalidate>
<div class="field"><label for="business">Restaurant or café name <span aria-hidden="true">*</span></label><input id="business" name="business" autocomplete="organization" maxlength="85" placeholder="What is your place called?" required></div>
<div class="field"><label for="owner">Your name <span aria-hidden="true">*</span></label><input id="owner" name="owner" autocomplete="name" maxlength="70" placeholder="How should we address you?" required></div>
<div class="two-fields"><div class="field"><label for="phone">Phone number <span aria-hidden="true">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" minlength="10" maxlength="18" placeholder="+91 98..." required></div>
<div class="field"><label for="area">Location <span aria-hidden="true">*</span></label><select id="area" name="area" required><option value="">Select location</option><option>Noida</option><option>Greater Noida</option><option>Delhi NCR</option><option>Other</option></select></div></div>
<fieldset class="package-choices"><legend>What are you looking for?</legend>
<label class="package-choice"><input type="radio" name="package" value="Starter" checked><span><b>Starter</b><small>One-page essentials</small></span><strong>₹3,000</strong></label>
<label class="package-choice"><input type="radio" name="package" value="Growth"><span><b>Growth</b><small>More menu and imagery</small></span><strong>₹5,000</strong></label>
<label class="package-choice"><input type="radio" name="package" value="Premium"><span><b>Premium</b><small>Additional agreed features</small></span><strong>₹8,000</strong></label>
</fieldset>
<div class="field"><label for="notes">A little more about your idea <span class="optional">(optional)</span></label>
<textarea id="notes" name="notes" rows="4" maxlength="650" placeholder="Your menu, the atmosphere, photos you have, or features you need..."></textarea></div>
<label class="consent-label"><input id="consent" type="checkbox" required> <span>I am requesting a quote and agree to be contacted about this enquiry only.</span></label>
<button class="button button-dark quote-submit" type="submit" {disabled}>Open email to request a quote <span aria-hidden="true">↗</span></button>
<p class="form-feedback" id="form-feedback" role="status" aria-live="polite"></p>
<p class="form-fine">This opens your email application with the details filled in. Nothing is sent until you press Send. No payment is collected here.</p>
</form></div></section>
</main>""" + studio_footer()
    return page("Request a Website Proposal — Noida Restaurant Web Studio",body,kind="quote",description="Request a restaurant or café website quotation. Packages from ₹3,000, clear scope, and three design directions for Noida and Greater Noida.")

@router.get("/privacy",response_class=HTMLResponse)
def privacy():
    body=nav()+"""<main id="main" class="legal-page"><span class="overline">THE FINE PRINT</span><h1>Privacy, kept simple.</h1>
<p>We operate Noida Restaurant Web Studio as an independent restaurant website design service.</p>
<h2>Enquiries</h2><p>Our enquiry form prepares an email in your own email app. The site does not store the form details on a database or send them automatically. You choose whether to send the email. If you email us, we use what you share to discuss your enquiry and proposed project.</p>
<h2>WhatsApp</h2><p>Automated WhatsApp outbound messages are currently disabled. No unsolicited WhatsApp marketing is sent by this website.</p>
<h2>Third-party services</h2><p>This site is hosted on Render. Google Fonts and optional 3D library resources may be loaded by your browser. These services may process network requests under their own policies. We do not deliberately add third-party advertising trackers.</p>
<h2>Your choices</h2><p>You can contact the studio using the quotation page. If you no longer want us to contact you about your enquiry, reply to our email asking us to stop and we will respect that request.</p>
<a class="button button-dark" href="/quote">Ask a question ↗</a></main>""" + studio_footer()
    return page("Privacy | Noida Restaurant Web Studio",body,kind="legal")

@router.get("/terms",response_class=HTMLResponse)
def terms():
    body=nav()+"""<main id="main" class="legal-page"><span class="overline">THE FINE PRINT</span><h1>Working together.</h1>
<p>Prices displayed here are starting package prices in Indian rupees for restaurant website design. They are not a binding offer or a guarantee of delivery time.</p>
<h2>Before a project begins</h2><p>We agree in writing on the exact pages, design, content, scope, delivery requirements, revisions, price and any optional fees. A deposit, if applicable, is discussed only after agreement. Never pay without verifying the written scope and recipient.</p>
<h2>Domains and other services</h2><p>Domain registration, hosting upgrades, optional integrations and third-party charges may be separate. We ask before any paid services are activated.</p>
<h2>Portfolio concepts</h2><p>Mitti & Masala, FIREPAN and The Saffron Table are fictional design studies. They are not operating restaurants or client testimonials. Sample menus, brands and imagery demonstrate design directions only.</p>
<h2>No ordering or bookings</h2><p>This showcase does not operate a restaurant, sell food, accept table reservations or process payments.</p>
<a class="button button-dark" href="/quote">Request a proposal ↗</a></main>""" + studio_footer()
    return page("Terms | Noida Restaurant Web Studio",body,kind="legal")


# Content files are served directly without any separate, billable asset service.
# The ESM 3D bundle is optional and respects reduced-motion preferences.
from pathlib import Path

@router.get("/assets/luxury.css")
def luxury_css():
    return Response(Path(__file__).with_name("luxury.css").read_bytes(),
                    media_type="text/css; charset=utf-8",
                    headers={"Cache-Control":"public,max-age=3600"})

@router.get("/assets/luxury-ui.js")
def luxury_ui_js():
    return Response(Path(__file__).with_name("luxury-ui.js").read_bytes(),
                    media_type="application/javascript; charset=utf-8",
                    headers={"Cache-Control":"public,max-age=3600"})

@router.get("/assets/luxury-3d.js")
def luxury_3d_js():
    return Response(Path(__file__).with_name("luxury-3d.js").read_bytes(),
                    media_type="application/javascript; charset=utf-8",
                    headers={"Cache-Control":"public,max-age=3600"})

@router.get("/assets/luxury-favicon.svg")
def favicon():
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="#13201a"/><path d="M12 47V18h8l21 22V18h10v29h-9L22 26v21z" fill="#d0b68b"/><circle cx="53" cy="51" r="4" fill="#d0b68b"/></svg>'
    return Response(svg,media_type="image/svg+xml",headers={"Cache-Control":"public,max-age=604800"})
