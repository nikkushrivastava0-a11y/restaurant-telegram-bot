"""Noida Restaurant Website Studio — safe WhatsApp Cloud API preview.
Never sends cold outreach; only signed inbound WhatsApp webhooks after explicit setup.
"""
import hashlib
import hmac
import html
import json
import logging
import os
import re
from pathlib import Path
import requests
from fastapi import FastAPI, Request, HTTPException, Query, Header
from fastapi.responses import HTMLResponse, PlainTextResponse

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Noida Restaurant Web Studio")
# Luxury router registered first, so its pages override only the original showroom.
# Existing /webhook and /health handlers remain untouched.
from luxury_site import router as luxury_router
app.include_router(luxury_router)
from sales_quote import router as sales_router
app.include_router(sales_router)
from social_assets import router as social_asset_router
app.include_router(social_asset_router)
SEND_ENABLED = os.getenv("SEND_ENABLED", "false").lower() == "true"
SIMULATOR_ENABLED = os.getenv("SIMULATOR_ENABLED", "false").lower() == "true"
PHONE_ID = os.getenv("WA_PHONE_NUMBER_ID", "")
ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN", "")
APP_SECRET = os.getenv("WA_APP_SECRET", "")
VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "")
SALES_WHATSAPP = re.sub(r"\D", "", os.getenv("SALES_WHATSAPP", ""))
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "")
GRAPH_VERSION = os.getenv("WA_GRAPH_VERSION", "v23.0")
BRAND = "Noida Restaurant Web Studio"
PUBLIC_URL = os.getenv("PUBLIC_URL", "").rstrip("/")
# This preview deliberately has no outbound campaign, contact imports, or scheduled marketing.
if SEND_ENABLED and not all((PHONE_ID, ACCESS_TOKEN, APP_SECRET, VERIFY_TOKEN)):
    raise RuntimeError("Missing official Meta WhatsApp Cloud API settings.")
if SEND_ENABLED and not (SUPPORT_EMAIL or SALES_WHATSAPP):
    raise RuntimeError("Human escalation contact is required before live messages.")

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap');
*{box-sizing:border-box}body{margin:0;font-family:'DM Sans',system-ui,Arial,sans-serif}a{text-decoration:none;color:inherit}
.wrap{max-width:1120px;margin:auto;padding:0 27px}nav{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:29px 0}
.logo{font-size:20px;font-weight:800;letter-spacing:-.04em}.navlinks{display:flex;gap:26px;font-size:13px;font-weight:650}
.hero{min-height:580px;display:grid;grid-template-columns:1.1fr 0.9fr;align-items:center;gap:34px;padding:60px 0}
.kicker{text-transform:uppercase;letter-spacing:.22em;font-size:12px;font-weight:800}
h1{font-size:clamp(48px,6.3vw,90px);line-height:1.04;letter-spacing:-.055em;margin:21px 0}
h2{font-size:clamp(31px,4vw,51px);letter-spacing:-.045em;line-height:1.12;margin:0 0 19px}
.sub{font-size:17px;line-height:1.8;max-width:490px;opacity:.83}
.cta{display:inline-flex;align-items:center;gap:12px;padding:17px 26px;margin-top:22px;font-weight:800;font-size:14px;border-radius:3px}
.visual{position:relative;min-height:450px;display:grid;place-items:center;overflow:hidden}
.plate{width:295px;height:295px;border-radius:50%;display:grid;place-items:center;font-size:120px;box-shadow:0 30px 90px #0003;transform:rotate(-8deg)}
.tag{position:absolute;bottom:35px;right:20px;padding:14px 18px;font-weight:800;font-size:12px;text-transform:uppercase;letter-spacing:.11em}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:28px 0 74px}
.item{padding:27px;min-height:185px}.item h3{font-size:20px;margin:13px 0 8px}.item p{font-size:14px;line-height:1.65;opacity:.75}
.section{padding:72px 0}footer{padding:25px 0;border-top:1px solid #8883;font-size:12px;line-height:1.8}
.notice{font-size:11px;opacity:.66} .back{font-size:13px;font-weight:800}
@media(max-width:750px){.hero{grid-template-columns:1fr;padding:34px 0;gap:8px}.visual{min-height:310px}.plate{width:235px;height:235px;font-size:100px}.cols{grid-template-columns:1fr;gap:12px;padding-bottom:45px}.navlinks{display:none}.tag{bottom:12px}h1{font-size:54px}}
"""
DEMOS = {
    "modern": dict(name="Mitti & Masala", locality="Contemporary Indian Kitchen", label="GOOD FOOD. GOOD COMPANY.", headline="A little spice. A lot of soul.", text="Seasonal Indian plates, timeless flavours and a table that always makes room for one more.", food="🍛", action="Explore the menu", theme="modern", address="Restaurant concept • Noida", cards=[("The slow lunch","Comforting dishes inspired by our everyday kitchens."),("Flavours that stay","Honest ingredients, big heart, modern craft."),("Come as you are","Unhurried meals with friends and family.")]),
    "bold": dict(name="FIREPAN", locality="FRESH FROM THE FLAME", label="LOUD FLAVOUR. ZERO BORING.", headline="HUNGRY? WE GOT YOU.", text="Big bites. Fiery grills. No apologies. The street-food energy your cravings have been looking for.", food="🍔", action="Get the vibe", theme="bold", address="Restaurant concept • Greater Noida", cards=[("THE BIG BITE","Bold, messy and worth every napkin."),("TURN UP THE HEAT","Hot, fresh and cooked with attitude."),("BRING YOUR CREW","Good food deserves a full table.")]),
    "minimal": dict(name="The Saffron Table", locality="A QUIETER KIND OF DINING", label="TABLE • TASTE • TOGETHER", headline="Simple things, beautifully made.", text="An intimate dining experience celebrating slow meals, good conversation, and thoughtful flavours.", food="🥗", action="Discover the concept", theme="minimal", address="Restaurant concept • Noida", cards=[("Curated flavours","Considered ingredients with room to shine."),("Warm hospitality","A place to gather, linger and feel at home."),("Everyday special","Make a little room for something beautiful.")]),
}
THEMES = {
 "modern": "body{background:#f6f1e8;color:#173e37}.cta{background:#e9ae62;color:#183b35}.visual{background:radial-gradient(circle at 65% 35%,#f4bd7b,#c77447 55%,#7a4936)}.plate{background:#f0dcc1}.tag{background:#153d36;color:#fff}.item{background:#e8e5d8}.kicker{color:#9b6b3c}h1,h2{font-family:'Playfair Display',Georgia,serif}",
 "bold": "body{background:#171714;color:#faf3dd}.cta{background:#e7fc44;color:#111}.visual{background:radial-gradient(circle,#ee7d32,#bd3329 52%,#3d211f)}.plate{background:#252520}.tag{background:#e7fc44;color:#111}.item{background:#272722}.kicker{color:#e7fc44}h1{font-weight:800;letter-spacing:-.075em;text-transform:uppercase}",
 "minimal": "body{background:#f4f0e8;color:#302c27}.cta{background:#282924;color:#fff}.visual{background:radial-gradient(circle at 45% 40%,#c8c8a3,#8c9b7e 62%,#5d755c)}.plate{background:#f6f0dd}.tag{background:#f4eee0;color:#342c23}.item{background:#e7e1d4}.kicker{color:#867257}h1,h2{font-family:'Playfair Display',Georgia,serif;font-weight:500}",
}

@app.get("/health")
def health():
    return {"ok": True, "mode": "live-inbound" if SEND_ENABLED else "preview-only", "outbound_enabled": SEND_ENABLED}

@app.get("/", response_class=HTMLResponse)
def landing():
    contact = ("<a class='button' href='https://wa.me/" + SALES_WHATSAPP + "?text=Hi%2C%20I%20want%20a%20restaurant%20website'>Ask for a demo →</a>") if SALES_WHATSAPP else "<a class='button' href='/quote'>Request a free proposal →</a>"
    return """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Noida Restaurant Web Studio</title><style>""" + BASE_CSS + """body{background:#10241f;color:#f5f1e5}.top{display:flex;justify-content:space-between;padding:30px 0}.hero{text-align:center;display:block;min-height:0;padding:92px 0 42px}h1{font-size:clamp(52px,9vw,100px);max-width:950px;margin:22px auto}h1 span{color:#c5ee9f}.lead{font-size:19px;line-height:1.75;max-width:580px;margin:auto;color:#bdd0c3}.button{background:#c5ee9f;color:#10241f;padding:18px 27px;display:inline-block;margin:23px 0;font-weight:800}.badge{padding:11px;border:1px solid #ffffff49;display:inline-block;margin-top:20px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding:55px 0 90px}.card{border:1px solid #ffffff30;padding:30px;background:#17352b}.card h2{font-size:33px;margin:12px 0}.card p{color:#a5c3b4;line-height:1.7}.card a{display:inline-block;border-bottom:1px solid #c5ee9f;padding:10px 0;color:#c5ee9f}.price{text-align:center;color:#d7e4c8;margin-top:25px}@media(max-width:700px){.cards{grid-template-columns:1fr}} </style></head><body><div class="wrap"><div class="top"><b class="logo">RESTAURANT WEB STUDIO.</b><span class="kicker">Noida × Greater Noida</span></div><div class="hero"><div class="kicker">Your next customer is searching</div><h1>Great food deserves a <span>great website.</span></h1><p class="lead">Mobile-first restaurant websites with menu, directions and click-to-call. Clear pricing. Designed for local businesses, not templates that all look alike.</p>""" + contact + """<p class="price">Website packages ₹3,000–₹8,000 · Optional maintenance from ₹500/month</p></div><div class="cards"><div class="card"><span class="kicker">01 / Warm & editorial</span><h2>Mitti & Masala</h2><p>Modern Indian food, fresh typography and welcoming colours.</p><a href="/samples/modern/">View Modern demo →</a></div><div class="card"><span class="kicker">02 / Bold & punchy</span><h2>FIREPAN</h2><p>Fast-food energy, dramatic contrasts and fearless copy.</p><a href="/samples/bold/">View Bold demo →</a></div><div class="card"><span class="kicker">03 / Quiet luxury</span><h2>The Saffron Table</h2><p>Minimal visual design with spacious, editorial layouts.</p><a href="/samples/minimal/">View Minimal demo →</a></div></div><footer>Independent studio · <a href="/privacy">Privacy</a><p class="notice">Demonstration brands are entirely fictional. No business ratings, photos, testimonials, menus or endorsements are represented as real.</p></footer></div></body></html>"""

def render_demo(style: str):
    d = DEMOS.get(style)
    if not d:
        raise HTTPException(404, "Unknown demo")
    cards = "".join("<div class='item'><div class='kicker'>0" + str(i + 1) + "</div><h3>" + html.escape(title) + "</h3><p>" + html.escape(desc) + "</p></div>" for i, (title, desc) in enumerate(d["cards"]))
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>""" + html.escape(d["name"]) + """ — Restaurant Website Concept</title><style>""" + BASE_CSS + THEMES[style] + """</style></head><body><div class="wrap"><nav><a class="logo" href="/samples/""" + style + """/">""" + html.escape(d["name"]) + """</a><div class="navlinks"><a href="#story">Our story</a><a href="#menu">The experience</a><a href="#visit">Visit</a></div><a class="back" href="/">Studio ↗</a></nav><main><div class="hero"><div><div class="kicker">""" + html.escape(d["label"]) + """</div><h1>""" + html.escape(d["headline"]) + """</h1><p class="sub">""" + html.escape(d["text"]) + """</p><a href="#menu" class="cta">""" + html.escape(d["action"]) + """ →</a></div><div class="visual"><div class="plate">""" + d["food"] + """</div><div class="tag">Visual placeholder · Concept</div></div></div><section id="story" class="section"><span class="kicker">""" + html.escape(d["locality"]) + """</span><h2>A place to return to.</h2><p class="sub">Thoughtful, responsive design with dedicated space for your verified menu, real food photography, location and opening hours after the owner approves the details.</p></section><section id="menu"><div class="kicker">The Experience</div><div class="cols">""" + cards + """</div></section></main><footer id="visit"><b>""" + html.escape(d["name"]) + """</b> · """ + html.escape(d["address"]) + """<br><span class="notice">Unofficial fictional restaurant concept, not a live restaurant or ordering service. No bookings or payments are accepted.</span></footer></div></body></html>"""

@app.get("/samples/{style}/", response_class=HTMLResponse)
def demo(style: str):
    return render_demo(style)

@app.get("/privacy", response_class=HTMLResponse)
def privacy():
    return "<main style='max-width:680px;margin:8vh auto;font:16px/1.7 system-ui;padding:25px'><h1>Privacy</h1><p>WhatsApp chatbot is currently disabled. If enabled with official Meta Business consent, we use message content to answer your enquiry, not for unsolicited outreach. Reply STOP to end contact.</p><a href='/'>Back</a></main>"

@app.get("/webhook", response_class=PlainTextResponse)
def verify(mode: str = Query("", alias="hub.mode"), token: str = Query("", alias="hub.verify_token"), challenge: str = Query("", alias="hub.challenge")):
    if not VERIFY_TOKEN or mode != "subscribe" or not hmac.compare_digest(token, VERIFY_TOKEN):
        raise HTTPException(403)
    return challenge

def reply_for(text: str):
    msg = text.strip().lower()
    if msg in ("stop", "unsubscribe"):
        return None
    if "price" in msg or "kitna" in msg or "rate" in msg:
        return "Restaurant website ₹3,000–₹8,000 one-time, optional maintenance from ₹500/month. Written scope aur agreement ke baad hi 50% advance. DEMO ya HUMAN reply karein."
    if "human" in msg or "call" in msg:
        if SUPPORT_EMAIL:
            return "Human support: " + SUPPORT_EMAIL
        if SALES_WHATSAPP:
            return "Human support: +" + SALES_WHATSAPP
        return "Human contact details abhi configure nahi hain."
    if "demo" in msg or "website" in msg or "site" in msg:
        return "Restaurant website demo: " + (PUBLIC_URL or "Please check our profile") + "/samples/modern/ . PRICE ya HUMAN reply karein."
    return "Hi! Noida Restaurant Web Studio bot. Restaurant website ke demo ke liye DEMO, pricing ke liye PRICE, aur human help ke liye HUMAN likhein. STOP se updates band."

@app.post("/webhook")
async def webhook(request: Request, x_hub_signature_256: str | None = Header(None)):
    data = await request.body()
    if len(data) > 500000:
        raise HTTPException(413)
    if not APP_SECRET:
        raise HTTPException(503, "Meta integration not activated")
    sig = "sha256=" + hmac.new(APP_SECRET.encode(), data, hashlib.sha256).hexdigest()
    if not x_hub_signature_256 or not hmac.compare_digest(sig, x_hub_signature_256):
        raise HTTPException(403)
    payload = json.loads(data)
    if payload.get("object") != "whatsapp_business_account":
        return {"ok": True, "processed": 0}
    # No outbound response unless the owner specifically activates official Meta credentials and SEND_ENABLED.
    count = 0
    for e in payload.get("entry", []):
        for change in e.get("changes", []):
            for message in change.get("value", {}).get("messages", []):
                if message.get("type") != "text":
                    continue
                phone = str(message.get("from", ""))
                if not re.fullmatch(r"[0-9]{9,15}", phone):
                    continue
                answer = reply_for(str(message.get("text", {}).get("body", ""))[:1500])
                if answer and SEND_ENABLED:
                    r = requests.post(
                        "https://graph.facebook.com/" + GRAPH_VERSION + "/" + PHONE_ID + "/messages",
                        headers={"Authorization":"Bearer " + ACCESS_TOKEN, "Content-Type":"application/json"},
                        json={"messaging_product":"whatsapp","to":phone,"type":"text","text":{"body":answer}},
                        timeout=12,
                    )
                    r.raise_for_status()
                count += 1
    return {"ok": True, "processed": count, "messages_sent": "disabled" if not SEND_ENABLED else "inbound_replies_only"}

@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return "User-agent: *\\nAllow: /\\nSitemap: https://noida-restaurant-web-studio.onrender.com/sitemap.xml\\n".replace("\\n","\n")

@app.get("/sitemap.xml", response_class=PlainTextResponse)
def sitemap():
    u="https://noida-restaurant-web-studio.onrender.com"
    return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join("<url><loc>"+u+p+"</loc></url>" for p in ("/","/quote","/samples/modern/","/samples/bold/","/samples/minimal/"))+"</urlset>"
