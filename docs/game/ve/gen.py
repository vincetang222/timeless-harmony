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
# Giới hạn của chủ dự án (25/11/2026): game chỉ dùng tối đa 40% gói Model Studio mỗi tháng, phần còn lại để việc khác.
# Sổ đếm nằm cạnh tệp này (so-luot.json, đưa vào repo sau mỗi lô). Lô nào làm vượt giới hạn tháng thì bị từ chối trước khi gọi.
import os, datetime, threading
SO = os.path.join(os.path.dirname(os.path.realpath(__file__)), "so-luot.json")   # realpath: bản sao dạng liên kết vẫn ghi vào sổ trong repo
_khoa = threading.Lock()
def doc_so():
    d = json.load(open(SO)) if os.path.exists(SO) else {}
    d.setdefault("gioi_han_phan_tram", 40); d.setdefault("phan_tram_moi_hinh", 0.24); d.setdefault("thang", {})
    return d
def tran(d): return int(d["gioi_han_phan_tram"] / d["phan_tram_moi_hinh"])
def ghi_mot(ten):
    with _khoa:
        d = doc_so(); t = datetime.date.today().strftime("%Y-%m"); m = d["thang"].setdefault(t, {"so_hinh": 0, "ten": []})
        m["so_hinh"] += 1; m["ten"].append(ten); json.dump(d, open(SO, "w"), ensure_ascii=False, indent=1)
if __name__=="__main__":
    jobs=json.load(open(sys.argv[1]))
    d = doc_so(); t = datetime.date.today().strftime("%Y-%m"); da = d["thang"].get(t, {}).get("so_hinh", 0)
    if da + len(jobs) > tran(d):
        sys.exit(f"Từ chối: tháng {t} đã dùng {da} hình, lô này {len(jobs)} hình, vượt giới hạn {tran(d)} hình ({d['gioi_han_phan_tram']}% gói). Chủ dự án đổi giới hạn trong {SO} nếu muốn.")
    print(f"Tháng {t}: đã dùng {da}/{tran(d)} hình; lô này {len(jobs)} hình.", flush=True)
    def chay(j):
        r = thu(*j)
        if r.endswith(" ok"): ghi_mot(j[0])
        return r
    with cf.ThreadPoolExecutor(int(os.environ.get("SONG","6"))) as ex:
        for r in ex.map(chay, jobs): print(r, flush=True)
