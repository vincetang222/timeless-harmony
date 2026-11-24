import numpy as np
from PIL import Image, ImageFilter
def key(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(float); r,g,b=a[...,0],a[...,1],a[...,2]
    k=g-np.maximum(r,b); al=1-np.clip((k-30)/70,0,1)
    g2=np.minimum(g,np.maximum(r,b)+10); a[...,1]=np.where(k>0,g2,g)
    m=Image.fromarray((al*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
    o=Image.fromarray(a.astype('uint8')).convert('RGBA'); o.putalpha(m); return o
def bbox_head(im):
    al=np.asarray(im)[...,3]; ys,xs=np.nonzero(al>128); return ys.min(), xs.min(), xs.max()
