"""Conversion-friendly owner-initiated enquiry page. No unsolicited sends, tracking pixels or payment collection."""
import html
import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()
def contact_email():
    return os.getenv("CONTACT_EMAIL", "").strip()

@router.get("/quote", response_class=HTMLResponse)
def quote_page():
    email = contact_email()
    safe_email = html.escape(email, quote=True)
    if not email:
        contact = "<p class='fine'>Enquiries will open after the studio contact email is connected.</p>"
    else:
        contact = "<span class='fine'>Aapka email app khulega. Kuch automatically send nahi hoga; Send aapko press karna hoga.</span>"
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Restaurant Website Quote · Noida Restaurant Web Studio</title>
<meta name="description" content="Get a clear quote for a mobile-first restaurant website in Noida or Greater Noida. Packages ₹3,000 to ₹8,000, without hidden subscription fees.">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
*{box-sizing:border-box}body{margin:0;background:#f8f5ed;color:#183b32;font-family:'DM Sans',sans-serif}a{color:inherit}
.shell{max-width:1050px;margin:auto;padding:24px}header{display:flex;justify-content:space-between;align-items:center;gap:15px;font-size:14px;font-weight:800}
header a{text-decoration:none}.eyebrow{font-size:12px;letter-spacing:.18em;font-weight:800;text-transform:uppercase;color:#9c734f}
.hero{max-width:780px;padding:70px 0 46px}h1{font:600 clamp(46px,6.4vw,76px)/1.06 'Playfair Display',serif;letter-spacing:-.04em;margin:22px 0}h2{font:600 27px/1.2 'Playfair Display',serif;margin:12px 0}
.lead{line-height:1.75;color:#48685d;max-width:610px}
.layout{display:grid;grid-template-columns:1fr .85fr;gap:25px;padding-bottom:70px}
.panel{border:1px solid #ddd8ca;background:white;padding:30px;border-radius:8px}
.panel.alt{background:#e7e8da}
label{font-size:13px;font-weight:800;display:block;margin:19px 0 8px}input,select,textarea{width:100%;font:inherit;border:1px solid #b5bdb4;background:#fff;padding:13px;border-radius:5px;outline-color:#325c43}
button{cursor:pointer;width:100%;background:#164938;color:#fff;font:800 15px 'DM Sans',sans-serif;border:0;border-radius:5px;padding:17px;margin-top:22px}
button:hover{background:#0d3226}button:disabled{opacity:.45;cursor:not-allowed}
.fine{font-size:12px;color:#586c62;line-height:1.6}.price{font-weight:800;font-size:34px;letter-spacing:-.04em;margin:10px 0}
.row{display:flex;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid #d6dccf;font-size:14px}
.list{padding:0 0 0 16px;line-height:2;font-size:14px}.kicker{font-size:12px;font-weight:800;letter-spacing:.13em}
footer{border-top:1px solid #ddd5ca;padding:24px 0;color:#6b756d;font-size:12px}
@media(max-width:760px){.layout{grid-template-columns:1fr}.hero{padding:40px 0}.panel{padding:22px}}
</style></head><body><div class="shell"><header><a href="/">↖ RESTAURANT WEB STUDIO</a><span class="eyebrow">Noida · Greater Noida</span></header>
<div class="hero"><div class="eyebrow">Clarity first. No surprises.</div><h1>Get a restaurant website that actually brings customers in.</h1>
<p class="lead">Your own mobile-friendly website: clear menu, opening hours, location, one-tap calls and WhatsApp button. Choose a package, share what you need, and request a written proposal.</p></div>
<div class="layout"><section class="panel"><div class="eyebrow">Quick enquiry</div><h2>Tell us about your restaurant.</h2>
<form id="leadform">
<label for="business">Restaurant / café name</label><input id="business" required maxlength="85" autocomplete="organization" placeholder="e.g. Sharma's Kitchen">
<label for="owner">Your name</label><input id="owner" required maxlength="70" autocomplete="name" placeholder="Owner / manager">
<label for="phone">Your preferred contact number</label><input id="phone" required type="tel" minlength="10" maxlength="18" autocomplete="tel" placeholder="+91 ...">
<label for="area">Area</label><select id="area" required><option value="">Select location</option><option>Noida</option><option>Greater Noida</option><option>Other Delhi NCR</option></select>
<label for="package">Website package</label><select id="package"><option value="Starter" selected>Starter — ₹3,000</option><option value="Growth">Growth — ₹5,000</option><option value="Premium">Premium — ₹8,000</option></select>
<label for="notes">Anything else? (optional)</label><textarea id="notes" maxlength="450" rows="3" placeholder="Menu, bookings, delivery links, preferred colours..."></textarea>
<label style="font-weight:500"><input id="consent" type="checkbox" required style="width:auto;margin-right:8px">I am requesting a quote and agree to be contacted about this enquiry only.</label>
<button id="send" type="submit" """ + ("" if email else "disabled") + """>Prepare enquiry email →</button>
<div id="feedback" role="status" aria-live="polite" class="fine" style="margin-top:12px"></div>
""" + contact + """
<p class="fine">We don't buy or scrape personal contact lists. No unsolicited WhatsApp marketing. Submission opens your email app; you decide whether to send.</p>
</form></section>
<aside class="panel alt"><div class="eyebrow">Straightforward pricing</div><h2>Only pay for what you need.</h2>
<div class="row"><b>Starter</b><span>₹3,000</span></div><p class="fine">One page · Menu highlights · Google Maps link · Phone & WhatsApp buttons</p>
<div class="row"><b>Growth</b><span>₹5,000</span></div><p class="fine">Starter + expanded menu, image gallery and polished custom layout</p>
<div class="row"><b>Premium</b><span>₹8,000</span></div><p class="fine">Growth + extra sections and agreed integrations</p>
<div class="row"><span>Optional maintenance</span><b>from ₹500/month</b></div>
<h2 style="margin-top:34px">How it works</h2><ol class="list"><li>Request a quote, tell us your requirements.</li><li>Review scope and demo first.</li><li>Pay 50% advance after written agreement.</li><li>Approve finished website before final payment.</li></ol>
<p class="fine">Domain costs, additional features and third-party fees are quoted separately, if applicable. Never pay anyone before receiving a written scope and verifying payment details.</p>
<a href="/samples/modern/" style="display:inline-block;margin-top:20px;font-weight:800;font-size:14px">See a design example ↗</a></aside></div>
<footer>Independent freelance website studio · <a href="/privacy">Privacy</a> · Website designs are samples, not real restaurant endorsements.</footer></div>
<script>
const dest=""" + repr_js(email) + """;
document.getElementById('leadform').addEventListener('submit', function(e){
 e.preventDefault();
 if (!this.reportValidity() || !document.getElementById('consent').checked) return;
 if (!dest){document.getElementById('feedback').textContent='Contact email not available yet.';return;}
 const val=(id)=>document.getElementById(id).value.trim();
 const subject='Restaurant Website Enquiry — '+val('business');
 const body='Hello Noida Restaurant Web Studio,\\n\\nI want a restaurant website quote.\\n\\nBusiness: '+val('business')+'\\nName: '+val('owner')+'\\nPhone: '+val('phone')+'\\nArea: '+val('area')+'\\nPackage: '+val('package')+'\\nRequirements: '+val('notes')+'\\n\\nI asked to be contacted about my enquiry.\\n';
 const url='mailto:'+dest+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
 document.getElementById('feedback').textContent='Opening your email app. Please press Send to complete the enquiry.';
 window.location.href=url;
});
</script></body></html>"""

def repr_js(s):
    import json
    return json.dumps(s)
