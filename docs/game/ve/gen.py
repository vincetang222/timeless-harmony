import json, base64, io, sys, subprocess, urllib.request, concurrent.futures as cf
from PIL import Image
URL="https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
def one(name, text, src=None, size=None):
    content=[]
    if src:
        im=Image.open(src).convert('RGB'); im.thumbnail((1400,1400)); b=io.BytesIO(); im.save(b,'JPEG',quality=92)
        content.append({"image":"data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()})
    content.append({"text":text})
    par={"watermark":False,"prompt_extend":False}
    if size: par["size"]=size
    req={"model":"qwen-image-3.0-pro","input":{"messages":[{"role":"user","content":content}]},"parameters":par}
    open(f"req-{name}.json","w").write(json.dumps(req))
    out=subprocess.run(["curl","-sS","-m","300","-X","POST",URL,"-H","Content-Type: application/json","-d","@req-"+name+".json"],capture_output=True,text=True).stdout
    try:
        u=json.loads(out)['output']['choices'][0]['message']['content'][0]['image']; urllib.request.urlretrieve(u,name+".png"); return name+" ok"
    except Exception as e: return name+" FAIL "+out[:300]
import time
def thu(*a):
    for i in range(6):
        r=one(*a)
        if 'Throttling' not in r: return r
        time.sleep(20*(i+1))
    return r
if __name__=="__main__":
    jobs=json.load(open(sys.argv[1]))
    with cf.ThreadPoolExecutor(int(__import__("os").environ.get("SONG","6"))) as ex:
        for r in ex.map(lambda j: thu(*j), jobs): print(r, flush=True)
