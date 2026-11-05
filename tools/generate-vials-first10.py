#!/usr/bin/env python3
"""Rebuild only NB-001 through NB-010 using a centered label on NOUS photographic vial assets."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
PRODUCTS=[
('NB-001','BPC-157','10 mg'),('NB-002','TB-500','10 mg'),
('NB-003','GLP3-RT','10 mg'),('NB-004','CJC-1295 / Ipamorelin','10mg/10mg'),
('NB-005','GHK-Cu','50 mg'),('NB-006','GLP-2TZ','10 mg'),
('NB-007','MOTS-C','10 mg'),('NB-008','Recon H²O','10 mL'),
('NB-009','PT-141','10 mg'),('NB-010','Ipamorelin','10 mg')]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
OUT=Path('vials');OUT.mkdir(exist_ok=True)
REG=Image.open('nous-peptide-lab.png').convert('RGB')
WATER=Image.open('nous-diluent-lab.png').convert('RGB')
def make(sku,name,qty):
    im=(WATER if sku=='NB-008' else REG).copy().resize((700,700),Image.Resampling.LANCZOS)
    d=ImageDraw.Draw(im); cx=339; maxwidth=215; gold=(196,151,70)
    # The original photographic label remains visible; draw only the new printed text.
    # All coordinates are centered on the photographed label, x approx 219..458.
    y=388;rad=12;lo,hi=292,386
    top=[];bottom=[]
    for x in range(lo,hi+1):
        a=(x-lo)/(hi-lo)*2*math.pi
        top.append((x,round(y+rad*math.sin(a))))
        bottom.append((x,round(y-rad*math.sin(a))))
    d.line(top,fill=gold,width=2);d.line(bottom,fill=gold,width=2)
    for x in range(lo+3,hi,12):
        a=(x-lo)/(hi-lo)*2*math.pi
        d.line((x,round(y+rad*math.sin(a)),x,round(y-rad*math.sin(a))),fill=(157,121,64),width=1)
    lines=['CJC-1295 /','Ipamorelin'] if sku=='NB-004' else [name]
    maxsize=27 if len(lines)==1 else 23
    for sz in range(maxsize,15,-1):
        ft=ImageFont.truetype(BOLD,sz)
        if all(d.textbbox((0,0),part,font=ft)[2] <= maxwidth for part in lines):break
    top_y=433-(len(lines)*(sz+4))/2
    for i,part in enumerate(lines):
        bb=d.textbbox((0,0),part,font=ft)
        d.text((cx-(bb[2]-bb[0])/2,top_y+i*(sz+4)-bb[1]),part,font=ft,fill=(242,242,238))
    frame=(257,468,421,506)
    d.rounded_rectangle(frame,radius=6,outline=gold,width=2)
    for fs in range(23,14,-1):
        ft=ImageFont.truetype(FONT,fs);bb=d.textbbox((0,0),qty,font=ft)
        if bb[2]-bb[0] <= 148:break
    d.text((cx-(bb[2]-bb[0])/2,487-(bb[3]-bb[1])/2-bb[1]),qty,font=ft,fill=(237,237,232))
    path=OUT/(sku+'.webp')
    im.save(path,'WEBP',quality=93,method=6)
    assert path.stat().st_size > 15000, path
for sku,name,qty in PRODUCTS:
    make(sku,name,qty)
print('Finished first ten:',', '.join(x[0] for x in PRODUCTS))
