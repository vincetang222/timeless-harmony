# Mặt nạ tóc cho lớp đầu: điểm tối, ấm hoặc xám, nối liền với mái tóc trên đỉnh đầu (loại nét viền thân áo).
import numpy as np
from PIL import Image, ImageFilter
def hsv(a):
    r,g,b=[a[...,i]/255 for i in range(3)]
    mx=np.maximum(np.maximum(r,g),b); mn=np.minimum(np.minimum(r,g),b); d=mx-mn+1e-6
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
    return h,(mx-mn)/(mx+1e-6),mx
def mat_toc(im, cut_frac):
    sm=im.resize((im.width//2,im.height//2),Image.BILINEAR)
    a=np.asarray(sm).astype(float); al=a[...,3]/255
    h,s,v=hsv(a); lum=(0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2])/255
    M=(lum<0.45)&(((h<=55)|(h>=330))|(s<0.2))&(al>0.4)
    H=M.shape[0]; cy=int(H*cut_frac)
    # hạt giống: vùng tóc ở phần trên (đỉnh đầu tới quá trán)
    S=M.copy(); S[int(H*0.12*1.0):]=False
    S[: , :]&=True
    for _ in range(2000):
        D=S.copy(); D[1:]|=S[:-1]; D[:-1]|=S[1:]; D[:,1:]|=S[:,:-1]; D[:,:-1]|=S[:,1:]
        D&=M
        if (D==S).all(): break
        S=D
    m=Image.fromarray((S*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))
    return m.resize(im.size,Image.BILINEAR)
