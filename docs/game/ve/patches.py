import sys, os, json, numpy as np
sys.path.insert(0,'.')
from prep import prep
from PIL import Image, ImageOps
meta=json.load(open('out2/meta.json'))
TAM={'nam':{'mat':[(690,350),(810,348)],'may':[(690,305),(810,303)]},'nu':{'mat':[(690,445),(805,440)],'may':[(690,405),(805,400)]}}
NUA={'mat':(64,42),'may':(70,28)}
KIEU={'mat':['hanh','motmi','to','phuong'],'may':['manh','dam','tunhien']}
GOCMAT={'goc':'{g}-goc','tron':'{g}-mat-tron','vuong':'{g}-mat-vuong'}
def ten_dau(g,v,m,t):
    if v=='vua':
        if m=='goc' and t=='goc': return f'{g}-goc'
        if m=='goc': return f'{g}-toc-{t}'
        if t=='goc': return f'{g}-mat-{m}'
        return f'{g}-{m}-{t}'
    return f'{g}-{v}'+(f'-{m}' if m!='goc' else '')+(f'-{t}' if t!='goc' else '')
TOC={'nam':['goc','vuot','xoan'],'nu':['goc','dai','ngan']}
from numpy.lib.stride_tricks import sliding_window_view as swv
_cache={}
def xam_ten(n):
    if n not in _cache:
        im=Image.open(n+'.png').convert('L')
        if im.size!=(1520,2736): im=im.resize((1520,2736),Image.LANCZOS)
        _cache[n]=np.asarray(im).astype(np.float32)
    return _cache[n]
def xam(im):
    a=np.asarray(im.convert('RGB')).astype(np.float32); return (0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2])
def _ncc(p,T):
    p=(p-p.mean())/(p.std()+1e-6); W=swv(T,p.shape)
    m=W.mean(axis=(2,3),keepdims=True); sd=W.std(axis=(2,3),keepdims=True)+1e-6
    return (((W-m)/sd)*p).mean(axis=(2,3))
def khop(P,T,cx,cy):
    w,h,R=130,95,40
    q=4; p=P[cy-h:cy+h:q, cx-w:cx+w:q]; t=T[cy-h-R:cy+h+R:q, cx-w-R:cx+w+R:q]
    sc=_ncc(p,t); iy,ix=np.unravel_index(sc.argmax(),sc.shape); dx,dy=int(ix*q-R),int(iy*q-R)
    # tinh chỉnh ±4 px ở độ phân giải đầy đủ hơn
    p=P[cy-h:cy+h:2, cx-w:cx+w:2]; r=4
    t=T[cy-h+dy-r:cy+h+dy+r:2, cx-w+dx-r:cx+w+dx+r:2]; sc2=_ncc(p,t)
    iy,ix=np.unravel_index(sc2.argmax(),sc2.shape)
    return float(sc2.max()), int(dx+ix*2-r), int(dy+iy*2-r)
out={}
os.makedirs('out2',exist_ok=True)
for g in ['nam','nu']:
    box=meta[g]['box']; s=meta[g]['s']; Wc=box[2]-box[0]
    out[g]={'manh':{},'vitri':{}}
    goc={m:xam_ten(GOCMAT[m].format(g=g)) for m in GOCMAT}
    for kind in ['mat','may']:
        hw,hh=NUA[kind]
        yy,xx=np.mgrid[-hh:hh,-hw:hw]; r=np.sqrt((xx/hw)**2+(yy/hh)**2); mask=np.clip((1-r)/0.35,0,1)
        for m in GOCMAT:
            for k in KIEU[kind]:
                n=f'{kind}-{g}-{m}-{k}'
                if not os.path.exists(n+'.png'): continue
                Pim=prep(n); P=xam_ten(n); A=np.asarray(Pim).astype(float)
                for side,(cx,cy) in enumerate(TAM[g][kind]):
                    # chỗ của mắt trong ảnh sửa so với ảnh gốc của chính nó
                    sc,dx0,dy0=khop(goc[m],P,cx,cy)
                    x0,y0=cx+dx0-hw,cy+dy0-hh
                    crop=A[y0:y0+2*hh,x0:x0+2*hw].copy(); crop[...,3]*=mask
                    im=ImageOps.mirror(Image.fromarray(crop.astype('uint8'),'RGBA'))
                    W2,H2=round(2*hw*s),round(2*hh*s); im=im.resize((W2,H2),Image.LANCZOS)
                    f=f'{n}-{side}'; im.save(f'out2/{f}.webp',quality=88)
                    out[g]['manh'].setdefault(kind,{}).setdefault(m,{}).setdefault(k,[None,None])[side]={'f':f,'w':W2,'h':H2,'x0':x0,'y0':y0}
    # vị trí trên từng đầu: dò đầu so với khuôn mặt gốc cùng họ
    for v in ['vua','manh','day']:
        for m in GOCMAT:
            for t in TOC[g]:
                hn=ten_dau(g,v,m,t); T=xam_ten(hn); vt={}
                for kind in ['mat','may']:
                    hw,hh=NUA[kind]; vt[kind]=[]
                    for side,(cx,cy) in enumerate(TAM[g][kind]):
                        sc,dx,dy=khop(goc[m],T,cx,cy)
                        vt[kind].append([round((Wc-(cx+dx+hw-box[0]))*s,1),round((cy+dy-hh-box[1])*s,1),round(sc,3)])
                out[g]['vitri']['dau-'+hn]=vt
                print(hn,vt,flush=True)
    # đổi sang toạ độ ảnh xuất (đã lật ngang và thu nhỏ): mỗi mảnh dùng x0,y0 của nó + độ lệch đầu
    out[g]['box']=[int(v) for v in box]; out[g]['s']=float(s); out[g]['Wc']=int(Wc); out[g]['nua']=NUA
json.dump(out,open('out2/manh.json','w'))
