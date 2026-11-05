#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageFilter
import io,urllib.request
URLS={"NB-001":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/5fed331e-bb6d-46eb-8c9c-3bb1be678bd6.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiZDM2ODQxMTIxNzY5ZjVhZiIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc5NDAyODE3OH0.Br0r7Oh17IMnmako2K4pXkRDPveG2Umii8LrgQNTBW8","NB-002":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/b7890c3d-76c7-4c34-bf01-8caa310b4a18.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiYTAzZDE2ZjdhMDU0M2JjOCIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc5NDAzMTczNX0.d18JGV3AnUN4Dzraa-WBmPrrRD5qJDo3YKWBmZK45EE","NB-003":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/e273484c-d5cf-4f5e-98cf-fe5df90c5fb3.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiNWIyNDE0NGYwZGE1NTNjNiIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsImV4cCI6MTc5NDA3OTk1MX0.SOuIlXn0CM78SW1DY7PVmfryz3R0gW1wU0vedJBDuA0","NB-004":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/ea586f11-4b3c-4dd2-ba89-bdee3e1bd25a.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiNmY4ZWExMDFlYTc2NjM3YyIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsImV4cCI6MTc5NDAzMTEwNX0.WdQXIG4WJgcrhc4SUByIDi4RqI1ZiZR5S4zWgSFT7VE","NB-005":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/5e563224-74b5-4ab7-b86c-677500a4d843.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiZTQ5NDMwOWRjZTBmNTM2NCIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc5NDA2MjYyMX0.NKG2QHHxCXzMPbtwk-L5QwHtJERT8XPl2ZU1nVQ1rvY","NB-006":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/a59a1804-5d63-45bd-afe4-3233b8d753fe.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiNGVkZjRiNzYyZGRkNjUzZSIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsImV4cCI6MTc5NDA1MDI5NH0.Pv9AFFeMWUCy8GeSL4m6bF5RP9M4G6AQwGF27OSUASQ","NB-007":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/c4222354-17ce-4180-a2de-11edaf359196.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiM2NjYWIyMjc4ZTI0MTUxYyIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTc5NDA2MDgzOX0.MpfNtPU8N8sXMOPT4ioqoUUnTENTvxqEv6JAlX8y-IM","NB-008":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/5186e71f-d085-48d1-8b81-34547aa9b7bb.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiMTliZDhmYzdkNmRkZWI2MCIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsInN0YWdlIjoicHJvZCI6IiIsImV4cCI6MTc5NDAzNTkxNX0.z9UGKQjU2AcQC8pM3bzpPvrTLbSQjA91upiZ2OZSvNs","NB-009":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/16b3fc04-c488-48c4-8bbe-f3383bf9e08f.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiOThhYmJiMTU2YTBiMjFkMiIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsImV4cCI6MTc5NDA3Mjk4MX0.49cC3bLcReFP5WjOQmQUx5M8t2n5OLz9o9GfkPxGAx4","NB-010":"https://d2jqrm6oza8nb6.cloudfront.net/datasets/899561e7-4561-48a7-9829-b526bcfc8862.png?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiMjEzNDMyNTQwNDU4NDcwYyIsImJ1Y2tldCI6InJ1bndheS1kYXRhc2V0cyIsImV4cCI6MTc5NDA1NzY4NH0.R9tDke7SvBopivGhUkRf0Gf3oA411bSa_jyLb_Al9m4"}
out=Path("vials");out.mkdir(exist_ok=True)
for sku,url in URLS.items():
    req=urllib.request.Request(url,headers={"User-Agent":"NOUS-Catalog-Import/1.0"})
    with urllib.request.urlopen(req,timeout=45) as response:
        data=response.read()
        assert response.status==200 and len(data)>10000,(sku,response.status,len(data))
    im=Image.open(io.BytesIO(data)).convert("RGB")
    assert min(im.size)>=500,(sku,im.size)
    side=768
    bg=im.resize((side,side),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(14))
    front=im.copy();front.thumbnail((side-18,side-16),Image.Resampling.LANCZOS)
    bg.paste(front,((side-front.width)//2,(side-front.height)//2))
    target=out/(sku+".webp")
    bg.save(target,"WEBP",quality=85,method=6)
    assert target.stat().st_size>20000,sku
    print(sku,target.stat().st_size)
assert len(URLS)==10
