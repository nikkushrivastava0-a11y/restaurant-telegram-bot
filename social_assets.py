"""Original branded social graphics for agency launch — no real restaurant claims."""
from io import BytesIO
from fastapi import APIRouter
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont

router = APIRouter()
GREEN = "#173B31"
CREAM = "#F8F4EB"
MUTED = "#69786C"
TANGERINE = "#F3B665"
def font(size, bold=False):
    candidates = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"]
    )
    for path in candidates:
        try: return ImageFont.truetype(path, size)
        except (OSError, ValueError): pass
    try: return ImageFont.load_default(size=size)
    except TypeError: return ImageFont.load_default()

def txt(draw, xy, label, size, color=GREEN, bold=False):
    draw.text(xy, label, font=font(size,bold), fill=color, stroke_width=0)

def center(draw, at_x, y, label, size, color=GREEN, bold=False):
    f=font(size,bold)
    b=draw.textbbox((0,0),label,font=f)
    draw.text((int(at_x-(b[2]-b[0])/2),y),label,font=f,fill=color)

def mockup(draw, box, brand, palette, special, index):
    x0,y0,x1,y1=box
    bg, ink, accent=palette
    draw.rounded_rectangle(box,radius=23,fill=bg)
    draw.rounded_rectangle((x0+15,y0+15,x1-15,y0+47),radius=8,fill=ink)
    for j in range(3):
        draw.ellipse((x0+32+j*16,y0+27,x0+39+j*16,y0+34),fill=accent)
    txt(draw,(x0+35,y0+65),f"0{index} / {brand.upper()}",24,ink,True)
    txt(draw,(x0+35,y0+104),special,26,ink,True)
    draw.ellipse((x1-145,y0+69,x1-32,y0+181),fill=accent)
    draw.ellipse((x1-134,y0+80,x1-43,y0+170),fill=bg)
    draw.ellipse((x1-114,y0+100,x1-63,y0+150),fill=accent)
    draw.rounded_rectangle((x0+35,y1-48,x0+190,y1-24),radius=7,fill=ink)
    txt(draw,(x0+48,y1-46),"VIEW SAMPLE",12,bg,True)

def graphic_portrait():
    im=Image.new("RGB",(1080,1350),CREAM);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1080,14),fill=TANGERINE)
    txt(d,(65,55),"NOIDA RESTAURANT WEB STUDIO",32,GREEN,True)
    txt(d,(65,109),"LOCAL WEBSITES  /  NOIDA + GREATER NOIDA",20,MUTED,True)
    txt(d,(62,185),"Great food deserves",67,GREEN,True)
    txt(d,(62,266),"a great website.",73,GREEN,True)
    txt(d,(65,369),"3 design directions. One simple starting price.",24,MUTED)
    mockup(d,(65,450,548,690),"Mitti & Masala",("#DDE7D7",GREEN,TANGERINE),"Warm. Modern. Indian.",1)
    mockup(d,(570,450,1015,690),"FIREPAN",("#242621","#F8F4EB","#EDB442"),"Bold & punchy.",2)
    mockup(d,(65,712,1015,956),"Saffron Table",("#E9E2D2",GREEN,"#BEC69A"),"Minimal / sophisticated / calm",3)
    d.rectangle((0,1000,1080,1350),fill=GREEN)
    txt(d,(65,1041),"ONE-PAGE RESTAURANT WEBSITES",24,"#D7E7D3",True)
    txt(d,(62,1092),"STARTING AT INR 3,000",54,CREAM,True)
    draw_call=(64,1190,1016,1268)
    d.rounded_rectangle(draw_call,18,fill=TANGERINE)
    center(d,540,1210,"SEE DESIGNS - LINK IN BIO",29,GREEN,True)
    txt(d,(66,1300),"DESIGN CONCEPTS - NOT EXISTING CLIENT WORK",17,"#B9D0C1")
    return im

def graphic_wide():
    im=Image.new("RGB",(1200,675),GREEN);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1200,12),fill=TANGERINE)
    txt(d,(55,47),"NOIDA RESTAURANT WEB STUDIO",26,CREAM,True)
    txt(d,(55,100),"Noida  /  Greater Noida",21,"#B9D0C1")
    txt(d,(52,177),"A restaurant",62,CREAM,True)
    txt(d,(52,257),"website that",62,CREAM,True)
    txt(d,(52,337),"works on mobile.",57,CREAM,True)
    txt(d,(55,451),"Menu. Directions. One-tap calls.",24,"#D7E7D3")
    d.rounded_rectangle((55,528,509,606),radius=12,fill=TANGERINE)
    txt(d,(82,547),"STARTING INR 3,000",30,GREEN,True)
    mockup(d,(597,116,1155,350),"Mitti & Masala",("#E9EEE1",GREEN,TANGERINE),"Warm Indian dining",1)
    mockup(d,(597,377,1155,613),"The Saffron Table",("#EAE2D5",GREEN,"#B4C497"),"Minimal dining",2)
    txt(d,(600,636),"ORIGINAL FICTIONAL DESIGN CONCEPTS",16,"#B9D0C1")
    return im

@router.get("/assets/agency-launch.png")
def launch_png():
    out=BytesIO()
    graphic_portrait().save(out,format="PNG",optimize=True)
    return Response(out.getvalue(),media_type="image/png",headers={"Cache-Control":"public,max-age=86400"})

@router.get("/assets/agency-linkedin.png")
def linkedin_png():
    out=BytesIO()
    graphic_wide().save(out,format="PNG",optimize=True)
    return Response(out.getvalue(),media_type="image/png",headers={"Cache-Control":"public,max-age=86400"})


# Square concept pages are based on the *same fictional* brands displayed
# on the existing /samples/{style}/ website routes.
from fastapi import HTTPException
CONCEPTS={
    "modern": {
        "brand":"Mitti & Masala",
        "eyebrow":"MODERN / WARM INDIAN KITCHEN",
        "head1":"A little spice.",
        "head2":"A lot of soul.",
        "body":"An inviting dining site for menus, hours, maps and one-tap calls.",
        "bg":"#F8F2E8","ink":"#173B31","accent":"#E7A66B","plate":"#EACDA7",
        "url":"/samples/modern/"
    },
    "bold":{
        "brand":"FIREPAN",
        "eyebrow":"BOLD / HIGH-ENERGY STREET FOOD",
        "head1":"HUNGRY?",
        "head2":"WE GOT YOU.",
        "body":"Punchy type, big flavour, and a clear menu call-to-action.",
        "bg":"#20211E","ink":"#F6F2DA","accent":"#F6DE53","plate":"#C95B3D",
        "url":"/samples/bold/"
    },
    "minimal":{
        "brand":"The Saffron Table",
        "eyebrow":"MINIMAL / THOUGHTFUL DINING",
        "head1":"Simple things,",
        "head2":"beautifully made.",
        "body":"A calm, understated restaurant website that stays useful.",
        "bg":"#F2EEE5","ink":"#35372F","accent":"#B6BDA4","plate":"#9AA989",
        "url":"/samples/minimal/"
    }
}

def concept_graphic(style):
    if style not in CONCEPTS:
        raise HTTPException(404,"Unknown concept")
    c=CONCEPTS[style]
    bg,ink,accent=c["bg"],c["ink"],c["accent"]
    im=Image.new("RGB",(1080,1350),bg)
    d=ImageDraw.Draw(im)
    d.rectangle((0,0,1080,11),fill=accent)
    txt(d,(65,55),"NOIDA RESTAURANT WEB STUDIO",28,ink,True)
    txt(d,(66,120),c["eyebrow"],19,ink,True)
    name_size=55 if len(c["brand"])<18 else 48
    txt(d,(60,202),c["brand"],name_size,ink,True)
    # A restaurant home page mockup with a visual food placeholder.
    d.rounded_rectangle((57,330,1024,986),radius=25,fill=ink)
    d.rounded_rectangle((79,355,1002,960),radius=15,fill=bg)
    d.rectangle((79,355,1002,414),fill=accent)
    txt(d,(105,372),"HOME     MENU     STORY     VISIT",20,ink,True)
    d.ellipse((620,488,953,821),fill=accent)
    d.ellipse((654,522,919,787),fill=bg)
    d.ellipse((691,558,882,749),fill=c["plate"])
    d.ellipse((735,605,837,706),fill=accent)
    txt(d,(118,516),c["head1"],54,ink,True)
    txt(d,(118,585),c["head2"],47,ink,True)
    txt(d,(122,694),"YOUR MENU, ONLINE",19,ink,True)
    d.rounded_rectangle((115,762,414,827),radius=8,fill=ink)
    txt(d,(144,782),"VIEW THE MENU",24,bg,True)
    txt(d,(82,915),"MOBILE-FIRST RESTAURANT WEBSITE CONCEPT",19,ink,True)
    txt(d,(69,1040),"01  /  MENU     02  /  MAP     03  /  CALL",25,ink,True)
    txt(d,(66,1115),"LIVE DEMO:",19,ink,True)
    txt(d,(65,1153),"noida-restaurant-web-studio.onrender.com",22,ink)
    txt(d,(65,1190),c["url"],22,ink)
    d.rectangle((0,1260,1080,1350),fill=accent)
    txt(d,(65,1291),"FICTIONAL CONCEPT - NOT CLIENT WORK",24,ink,True)
    return im

@router.get("/assets/concept-{style}.png")
def concept_png(style: str):
    out=BytesIO()
    concept_graphic(style).save(out,format="PNG",optimize=True)
    return Response(out.getvalue(),media_type="image/png",headers={"Cache-Control":"public,max-age=86400"})
