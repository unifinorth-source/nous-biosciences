#!/usr/bin/env python3
"""Split one approved ten-product composite into permanent NOUS catalog assets."""
import io,urllib.request
from pathlib import Path
from PIL import Image,ImageFilter
URL="https://d2jqrm6oza8nb6.cloudfront.net/datasets/793f20b1-55e6-4505-a6bd-531720497a76.jpg?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiODhmZTI1ZGZhYjNiOGRiMCIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc5NDA0MDQxNX0.nU2-OIVPWpwDhqbMCPPXlZnZ_S0jIx5ei4EmLO5qjPk"
with urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"NOUS-Approved-Assets/1.0"}),timeout=60) as response:
    payload=response.read()
    assert response.status==200 and len(payload)>150000, (response.status,len(payload))
sheet=Image.open(io.BytesIO(payload)).convert("RGB")
assert sheet.size==(2400,1280),sheet.size
out=Path("vials");out.mkdir(exist_ok=True)
for idx in range(10):
    col=idx%5;row=idx//5
    tile=sheet.crop((col*480,row*640,(col+1)*480,(row+1)*640))
    side=768
    bg=tile.resize((side,side),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(14))
    front=tile.copy();front.thumbnail((side-18,side-16),Image.Resampling.LANCZOS)
    bg.paste(front,((side-front.width)//2,(side-front.height)//2))
    dest=out/f"NB-{idx+1:03}.webp"
    bg.save(dest,"WEBP",quality=88,method=6)
    assert dest.stat().st_size>20000,dest
    print(dest, dest.stat().st_size)
print("Imported ten approved photos")
