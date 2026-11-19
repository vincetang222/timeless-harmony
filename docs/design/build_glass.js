/* Kính dựng sẵn: mỗi cảnh nền được đưa qua ĐÚNG bộ lọc của tấm kính (làm mờ + bão hoà + nén tương phản) bằng chính
   trình duyệt, rồi lưu ở 1/4 kích thước thành assets/bg/<tên>-glass.webp. Trang web đặt ảnh này sau tấm kính thay cho
   backdrop-filter, nên khi cuộn trình duyệt không phải làm mờ lại ở từng khung hình (xem mục 7b của theme.css).

       node docs/design/build_glass.js

   Chạy lại mỗi khi dựng lại cảnh nền hoặc đổi --backdrop trong theme.css (giữ hai nơi khớp nhau). */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BG = path.join(__dirname, '../../assets/bg');
const DAY = 'saturate(1.3) contrast(.62) brightness(1.24)';   // = --backdrop của chế độ sáng (trừ blur)
const NIGHT = 'saturate(1.25) brightness(.72)';               // = --backdrop của chế độ tối
// bán kính làm mờ tính theo điểm ảnh của ảnh gốc: ảnh ngang hiển thị ở ~0,7–1×, ảnh dọc ở ~0,43× trên điện thoại
const JOBS = [
  ['lake-day', 2000, 1250, 'blur(32px) ' + DAY],
  ['lake-night', 2000, 1250, 'blur(32px) ' + NIGHT],
  ['lake-day-m', 900, 1950, 'blur(46px) ' + DAY],
  ['lake-night-m', 900, 1950, 'blur(46px) ' + NIGHT],
];
const SCALE = 0.25;

(async () => {
  const browser = await chromium.launch();
  for (const [name, w, h, filter] of JOBS) {
    const src = path.join(BG, name + '.webp');
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.goto('file://' + src);
    await page.evaluate(([url, f]) => {
      document.documentElement.innerHTML = '<body style="margin:0">' +
        '<div style="position:fixed;inset:0;background:url(' + url + ') 0 0/100% 100% no-repeat"></div>' +
        '<div style="position:fixed;inset:0;-webkit-backdrop-filter:' + f + ';backdrop-filter:' + f + '"></div></body>';
    }, ['file://' + src, filter]);
    await page.waitForTimeout(400);
    const png = (await page.screenshot({ type: 'png' })).toString('base64');
    const webp = await page.evaluate(async ([b64, scale]) => {
      const img = new Image();
      img.src = 'data:image/png;base64,' + b64;
      await img.decode();
      const c = document.createElement('canvas');
      c.width = Math.round(img.naturalWidth * scale); c.height = Math.round(img.naturalHeight * scale);
      const g = c.getContext('2d');
      g.imageSmoothingQuality = 'high';
      g.drawImage(img, 0, 0, c.width, c.height);         // ảnh đã mờ nên thu nhỏ một bước là đủ
      return c.toDataURL('image/webp', 0.9).split(',')[1];
    }, [png, SCALE]);
    const out = path.join(BG, name + '-glass.webp');
    fs.writeFileSync(out, Buffer.from(webp, 'base64'));
    console.log(path.basename(out), Math.round(w * SCALE) + '×' + Math.round(h * SCALE), fs.statSync(out).size + ' B');
    await page.close();
  }
  await browser.close();
})();
