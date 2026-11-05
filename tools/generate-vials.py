#!/usr/bin/env python3
"""Generate 22 NOUS Biosciences photographic vial labels from blank-label assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

PRODUCTS=[
("NB-001","BPC-157","10 mg"),("NB-002","TB-500","10 mg"),
("NB-003","GLP3-RT","10 mg"),("NB-004","CJC-1295 / Ipamorelin","10mg/10mg"),
("NB-005","GHK-Cu","50 mg"),("NB-006","GLP-2TZ","10 mg"),
("NB-007","MOTS-C","10 mg"),("NB-008","Recon H²O","10 mL"),
("NB-009","PT-141","10 mg"),("NB-010","Ipamorelin","10 mg"),
("NB-011","CJC-1295 (no DAC)","10 mg"),("NB-012","AOD-9604","10 mg"),
("NB-013","Thymosin Alpha-1","10 mg"),("NB-014","Tesamorelin","10 mg"),
("NB-015","NAD+","500 mg"),("NB-016","Semax","10 mg"),
("NB-017","Kisspeptin","10 mg"),("NB-018","Epithalon","10 mg"),
("NB-019","KLOW Blend","80 mg"),("NB-020","GLOW Blend","70 mg"),
("NB-021","5-Amino-1MQ","10 mg"),("NB-022","IGF-1 LR3","1 mg")]
def font(sz,bold=False):
    f="/usr/share/fonts/truetype/dejavu/DejaVuSans"+("-Bold" if bold else "")+".ttf"
    return ImageFont.truetype(f,max(10,sz))
def fitted(draw,txt,width,size,lower,bold):
    for sz in range(size,lower-1,-1):
        f=font(sz,bold)
        box=draw.textbbox((0,0),txt,font=f)
        if box[2]-box[0]<=width:return f
    return font(lower,bold)
def make_image(base,name,qty):
    im=base.copy().convert("RGB")
    W,H=im.size
    cx=int(W*0.485)
    dr=ImageDraw.Draw(im)
    y_name=int(H*.611)
    y_qty=int(H*.695)
    # Tiny helix printed in metallic gold, within existing blank label.
    yy=int(H*.556)
    width=int(W*.16)
    for n in range(width):
        x=cx-width//2+n
        angle=n/max(1,width)*2*math.pi
        y1=int(yy+H*.009*math.sin(angle))
        y2=int(yy-H*.009*math.sin(angle))
        dr.point((x,y1),fill=(191,148,72))
        dr.point((x,y2),fill=(191,148,72))
        if n%max(3,int(W*.012))==0:dr.line((x,y1,x,y2),fill=(150,120,70),width=1)
    title=name.replace(" / ","/")
    tf=fitted(dr,title,int(W*.305),int(W*.045),int(W*.020),True)
    tbox=dr.textbbox((0,0),title,font=tf)
    dr.text((cx-(tbox[2]-tbox[0])/2,y_name-(tbox[3]-tbox[1])/2-tbox[1]),
            title,font=tf,fill=(245,243,241))
    bw,bh=int(W*.25),int(H*.06)
    dr.rounded_rectangle((cx-bw//2,y_qty-bh//2,cx+bw//2,y_qty+bh//2),
        radius=max(2,int(W*.008)),outline=(185,141,66),width=max(1,int(W*.002)))
    qf=fitted(dr,qty,bw-12,int(W*.034),int(W*.018),False)
    qb=dr.textbbox((0,0),qty,font=qf)
    dr.text((cx-(qb[2]-qb[0])/2,y_qty-(qb[3]-qb[1])/2-qb[1]),
        qty,font=qf,fill=(236,234,233))
    if max(im.size)>900:
        im.thumbnail((900,900),Image.Resampling.LANCZOS)
    return im
def main():
    out=Path("vials");out.mkdir(exist_ok=True)
    standard=Image.open("nous-peptide-lab.png").convert("RGB")
    diluent=Image.open("nous-diluent-lab.png").convert("RGB") if Path("nous-diluent-lab.png").exists() else standard
    for sku,name,qty in PRODUCTS:
        image=make_image(diluent if sku=="NB-008" else standard,name,qty)
        image.save(out/(sku+".webp"),"WEBP",quality=85,method=6)
    print("Generated",len(PRODUCTS),"product vial images")
if __name__=="__main__":
    main()
