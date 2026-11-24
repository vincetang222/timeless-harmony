# Tách lớp đầu và lớp thân. Mọi ảnh cùng một người gốc nên trùng khít khung 1520×2736.
import sys, os, json, glob, numpy as np
sys.path.insert(0,'.')
from key import key
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from toc import mat_toc, hsv
W,H=1520,2736; TH=1300
CUT={'nam':(600,18),'nu':(630,15)}
os.makedirs('out2',exist_ok=True)
def prep(n):
    im=Image.open(n+'.png').convert('RGB')
    if im.size!=(W,H): im=im.resize((W,H),Image.LANCZOS)
    im.save('/tmp/_k.png'); k=key('/tmp/_k.png')
    rgb=k.convert('RGB'); a=k.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    rgb=ImageEnhance.Color(rgb).enhance(0.9); rgb=ImageEnhance.Contrast(rgb).enhance(0.93)
    rgb=Image.blend(rgb,Image.new('RGB',rgb.size,(255,236,205)),0.08)
    o=rgb.convert('RGBA'); o.putalpha(a); return o
def ramp(a,b):
    y=np.arange(H,dtype=float)[:,None]; return np.clip((y-a)/(b-a),0,1)
def save(im,name,box,s):
    c=im.crop(box); c=ImageOps.mirror(c)  # vẽ nắng từ trái → lật cho khớp nắng từ phải của cảnh
    c=c.resize((round(c.width*s),round(c.height*s)),Image.LANCZOS); c.save(f'out2/{name}.webp',quality=84,method=6)
meta={}
for g in ['nam','nu']:
    cy,f=CUT[g]
    dau=sorted(os.path.basename(p)[:-4] for p in glob.glob(g+'-*.png'))
    than=sorted(os.path.basename(p)[:-4] for p in glob.glob('than-'+g+'-*.png'))+sorted(os.path.basename(p)[:-4] for p in glob.glob('ad-'+g+'-*.png'))
    ims={n:prep(n) for n in dau+than}
    ims_full=ims
    box=None
    for im in ims.values():
        b=im.getchannel('A').point(lambda v:255 if v>60 else 0).filter(ImageFilter.MinFilter(9)).getbbox()
        box=b if box is None else (min(box[0],b[0]),min(box[1],b[1]),max(box[2],b[2]),max(box[3],b[3]))
    box=(max(0,box[0]-20),max(0,box[1]-20),min(W,box[2]+20),min(H,box[3]+4))
    s=TH/(box[3]-box[1])
    headbox=(box[0],box[1],box[2],min(box[3],1500))
    for n in dau:   # lớp đầu: trên vết cắt, mờ dần qua cổ; cô dâu tóc dài giữ cả phần tóc rủ xuống vai
        a=np.asarray(ims[n]).astype(float); al=a[...,3]/255
        dac=(al>0.9).astype(float)
        keep=dac*(1-ramp(cy-f,cy+f))+(1-dac)*(1-ramp(cy+f,cy+f+6))
        if g=='nu':
            toc=np.asarray(mat_toc(ims[n],0.2)).astype(float)/255
            keep=np.maximum(keep,toc*(np.arange(H)[:,None]>=cy-f))
        a[...,3]=al*keep*255
        save(Image.fromarray(a.astype('uint8'),'RGBA'),'dau-'+n,headbox,s)
    def than_layer(n,ten):
        a=np.asarray(ims[n]).astype(float); dac=(a[...,3]>230).astype(float)
        a[...,3]=a[...,3]*(dac*ramp(cy-2*f,cy-f)+(1-dac)*ramp(cy+f,cy+f+6)); save(Image.fromarray(a.astype('uint8'),'RGBA'),ten,box,s)
    for v in ['goc','manh','day']: than_layer(f'{g}-{v}', f'than-{g}-{v}-can')
    for n in than:
        than_layer(n,n)
        if n.startswith('ad-'):
            a=np.asarray(ims[n]).astype(float); h_,s_,v_=hsv(a)
            da=(h_>=8)&(h_<=42)&(s_>=0.12)&(s_<=0.62)&(v_>=0.42)
            y=np.arange(H)[:,None]; vung=(y>=cy-90)&(y<cy+f)
            m=((~da)&(s_>0.22)&(a[...,3]>200)&vung).astype(np.uint8)*255
            m=np.asarray(Image.fromarray(m).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))).astype(float)/255
            a[...,3]=a[...,3]*m; save(Image.fromarray(a.astype('uint8'),'RGBA'),'co-'+n,box,s)
    hb=(headbox[3]-headbox[1])/(box[3]-box[1])
    ref=ims['nam-goc' if g=='nam' else 'nu-toc-ngan'].getchannel('A').point(lambda v:255 if v>60 else 0).filter(ImageFilter.MinFilter(9)).getbbox()
    meta[g]={'w':round((box[2]-box[0])*s),'h':TH,'hdau':round((headbox[3]-headbox[1])*s),'dinh':(ref[1]-box[1])/(box[3]-box[1]),
             'cx':1-((ref[0]+ref[2])/2-box[0])/(box[2]-box[0]),'dau':dau,'than':than,'box':box,'s':s}
    print(g,box,len(dau),len(than))
json.dump(meta,open('out2/meta.json','w'))
import pickle; pickle.dump({g:None for g in meta},open('/dev/null','wb'))
