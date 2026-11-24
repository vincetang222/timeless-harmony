import sys
sys.path.insert(0,'.')
from key import key
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
W,H=1520,2736
def prep(n):
    im=Image.open(n+'.png').convert('RGB')
    if im.size!=(W,H): im=im.resize((W,H),Image.LANCZOS)
    im.save('/tmp/_k.png'); k=key('/tmp/_k.png')
    rgb=k.convert('RGB'); a=k.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    rgb=ImageEnhance.Color(rgb).enhance(0.9); rgb=ImageEnhance.Contrast(rgb).enhance(0.93)
    rgb=Image.blend(rgb,Image.new('RGB',rgb.size,(255,236,205)),0.08)
    o=rgb.convert('RGBA'); o.putalpha(a); return o
