/**
 * 将机制图 SVG 导出为投稿所需格式：
 *   - PDF：矢量，字体已嵌入（子集化），适合 Elsevier / Springer 等直接投稿
 *   - PNG：600 dpi，用于 Word 排版或需要位图的期刊（可再转 TIFF）
 *
 * 依赖安装在 ../../.node-fig/node_modules，运行方式见同目录 README.md
 */
const fs = require('fs');
const path = require('path');
const PDFDocument = require('pdfkit');
const SVGtoPDF = require('svg-to-pdfkit');
const { Resvg } = require('@resvg/resvg-js');

const MM2PT = 72 / 25.4;
const W_MM = 180;
const H_MM = 110;
const DPI = 600;

const FONTS = {
  regular: '/System/Library/Fonts/Supplemental/Arial.ttf',
  bold: '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
  italic: '/System/Library/Fonts/Supplemental/Arial Italic.ttf',
  boldItalic: '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf',
  cjk: '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
};
const PINGFANG = '/System/Library/Fonts/PingFang.ttc';

function toPdf(svgPath, outPath, isCJK) {
  const svg = fs.readFileSync(svgPath, 'utf8');
  const doc = new PDFDocument({
    size: [W_MM * MM2PT, H_MM * MM2PT],
    margin: 0,
    info: { Title: path.basename(outPath, '.pdf'), Creator: 'make_mechanism_figure.py' },
  });
  const stream = fs.createWriteStream(outPath);
  doc.pipe(stream);

  for (const [key, file] of Object.entries(FONTS)) {
    if (fs.existsSync(file)) doc.registerFont(key, file);
  }

  // 中文版优先嵌入 PingFang（TTC 需指定子字族名），排版优于 Arial Unicode；
  // 取不到时回退到 Arial Unicode 以保证不缺字。
  let cjkOK = false;
  if (isCJK) {
    try {
      doc.registerFont('cjkRegular', PINGFANG, 'PingFangSC-Regular');
      doc.registerFont('cjkBold', PINGFANG, 'PingFangSC-Semibold');
      cjkOK = true;
    } catch (e) {
      console.warn('PingFang 不可用，回退 Arial Unicode:', e.message);
    }
  }

  const pick = (bold, italic) => {
    if (isCJK) return cjkOK ? (bold ? 'cjkBold' : 'cjkRegular') : 'cjk';
    if (bold && italic) return 'boldItalic';
    if (bold) return 'bold';
    if (italic) return 'italic';
    return 'regular';
  };

  SVGtoPDF(doc, svg, 0, 0, {
    width: W_MM * MM2PT,
    height: H_MM * MM2PT,
    assumePt: false,
    fontCallback: (family, bold, italic) => pick(bold, italic),
  });
  doc.end();
  return new Promise((res) => stream.on('finish', res));
}

function toPng(svgPath, outPath) {
  const svg = fs.readFileSync(svgPath, 'utf8');
  const widthPx = Math.round((W_MM / 25.4) * DPI);
  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: widthPx },
    background: 'white',
    font: { loadSystemFonts: true, defaultFontFamily: 'Arial' },
  });
  fs.writeFileSync(outPath, resvg.render().asPng());
  return widthPx;
}

(async () => {
  const dir = __dirname;
  for (const tag of ['EN', 'CN']) {
    const svgPath = path.join(dir, `mechanism_VB6_SPP1_TAM_${tag}.svg`);
    if (!fs.existsSync(svgPath)) continue;
    const pdfPath = svgPath.replace(/\.svg$/, '.pdf');
    const pngPath = svgPath.replace(/\.svg$/, `_${DPI}dpi.png`);
    await toPdf(svgPath, pdfPath, tag === 'CN');
    const px = toPng(svgPath, pngPath);
    console.log(`${tag}: PDF -> ${path.basename(pdfPath)}, PNG ${px}px -> ${path.basename(pngPath)}`);
  }
})();
