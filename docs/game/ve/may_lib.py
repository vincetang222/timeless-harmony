# Dùng chung: toạ độ mắt, lông mày của từng đầu trong ảnh nguồn (1520×2736, chưa lật)
import json, numpy as np
from PIL import Image
META=json.load(open('out2/meta.json')); MANH=json.load(open('out2/manh.json'))
NUA={'mat':(64,42),'may':(70,28)}
def tam(g, ten_dau, kind):
    """tâm mắt hoặc lông mày (2 bên) trong ảnh nguồn"""
    box=META[g]['box']; s=META[g]['s']; Wc=box[2]-box[0]; hw,hh=NUA[kind]
    return [(box[0]+Wc-x/s-hw, y/s+hh+box[1]) for x,y,_ in MANH[g]['vitri'][ten_dau][kind]]
def mo_anh(n): return Image.open(f'work/{n}.png').convert('RGBA')
def luma(a): return (0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2])/255
