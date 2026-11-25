# lưu sẵn ảnh đã tách nền của 54 đầu và 18 ảnh lông mày để thử thuật toán cho nhanh
import sys, os, json, glob; sys.path.insert(0,'.')
from prep import prep
meta=json.load(open('out2/meta.json'))
ds=[n for g in ['nam','nu'] for n in meta[g]['dau']]+sorted(os.path.basename(p)[:-4] for p in glob.glob('may-*.png'))
for n in ds:
    f=f'work/{n}.png'
    if os.path.exists(f): continue
    im=prep(n); im.crop((0,0,1520,1560)).save(f,compress_level=1); print(n,flush=True)
