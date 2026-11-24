# chỉ dựng lại lớp cổ áo dài (không chạy lại toàn bộ)
import sys, json, numpy as np; sys.path.insert(0,'.')
from prep import prep
from toc import hsv
from PIL import Image, ImageFilter, ImageOps
import glob, os
meta=json.load(open('out2/meta.json')); CUT={'nam':(600,18),'nu':(630,15)}; H=2736
for g in ['nam','nu']:
    cy,f=CUT[g]; box=meta[g]['box']; s=meta[g]['s']
    for p in sorted(glob.glob(f'ad-{g}-*.png')):
        n=os.path.basename(p)[:-4]; a=np.asarray(prep(n)).astype(float); h_,s_,v_=hsv(a)
        da=(h_>=8)&(h_<=42)&(s_>=0.12)&(s_<=0.62)&(v_>=0.42)
        y=np.arange(H)[:,None]; vung=(y>=cy-90)&(y<cy+f)
        m=((~da)&((s_>0.22) if g=='nu' else (v_<0.75))&(a[...,3]>200)&vung).astype(np.uint8)*255
        m=np.asarray(Image.fromarray(m).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))).astype(float)/255
        a[...,3]=a[...,3]*m; c=Image.fromarray(a.astype('uint8'),'RGBA').crop(box); c=ImageOps.mirror(c)
        c=c.resize((round(c.width*s),round(c.height*s)),Image.LANCZOS); c.save(f'out2/co-{n}.webp',quality=84,method=6)
print('ok')
