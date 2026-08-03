const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.join(__dirname, '..');
const STAGING_DIR = path.join(PROJECT_ROOT, 'products_staging');
const RAW_TEXTS_DIR = path.join(STAGING_DIR, 'raw_texts');
const RAW_IMAGES_DIR = path.join(STAGING_DIR, 'raw_images');
const PROCESSED_DIR = path.join(STAGING_DIR, 'processed');
const PRODUCTS_JSON_PATH = path.join(PROJECT_ROOT, 'js', 'products.json');
const MEDIA_DIR = path.join(PROJECT_ROOT, '_assets', 'media');

// Helper to ensure directory exists
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

ensureDir(PROCESSED_DIR);
ensureDir(MEDIA_DIR);

// Parse Markdown content
function parseProductMarkdown(content) {
  const lines = content.split(/\r?\n/);
  const product = {
    id: '',
    category: 'dining',
    status: 'active',
    name: { tw: '', en: '', jp: '' },
    description: { tw: '', en: '', jp: '' },
    images: [],
    badges: { tw: [], en: [], jp: [] },
    specs: []
  };

  let currentSection = '';
  let descriptionLines = [];

  for (let line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    // Heading # Name TW
    if (trimmed.startsWith('# ')) {
      product.name.tw = trimmed.substring(2).trim();
      // Generate initial ID from English name later, or use clean version of TW
      continue;
    }

    // Headers metadata
    if (trimmed.startsWith('Name EN:')) {
      product.name.en = trimmed.replace('Name EN:', '').trim();
      continue;
    }
    if (trimmed.startsWith('Name JP:')) {
      product.name.jp = trimmed.replace('Name JP:', '').trim();
      continue;
    }
    if (trimmed.startsWith('Category:')) {
      product.category = trimmed.replace('Category:', '').trim();
      continue;
    }
    if (trimmed.startsWith('Image:')) {
      const imgName = trimmed.replace('Image:', '').trim();
      if (imgName) product.images.push(imgName);
      continue;
    }
    if (trimmed.startsWith('Badge TW:')) {
      const b = trimmed.replace('Badge TW:', '').trim();
      if (b) product.badges.tw.push(b);
      continue;
    }
    if (trimmed.startsWith('Badge EN:')) {
      const b = trimmed.replace('Badge EN:', '').trim();
      if (b) product.badges.en.push(b);
      continue;
    }
    if (trimmed.startsWith('Badge JP:')) {
      const b = trimmed.replace('Badge JP:', '').trim();
      if (b) product.badges.jp.push(b);
      continue;
    }

    // Sections
    if (trimmed.startsWith('## Description TW')) {
      currentSection = 'desc_tw';
      descriptionLines = [];
      continue;
    }
    if (trimmed.startsWith('## Description EN')) {
      currentSection = 'desc_en';
      descriptionLines = [];
      continue;
    }
    if (trimmed.startsWith('## Description JP')) {
      currentSection = 'desc_jp';
      descriptionLines = [];
      continue;
    }
    if (trimmed.startsWith('## Specs')) {
      currentSection = 'specs';
      continue;
    }

    // Content lines
    if (currentSection === 'desc_tw') {
      descriptionLines.push(trimmed);
      product.description.tw = descriptionLines.join('\n');
    } else if (currentSection === 'desc_en') {
      descriptionLines.push(trimmed);
      product.description.en = descriptionLines.join('\n');
    } else if (currentSection === 'desc_jp') {
      descriptionLines.push(trimmed);
      product.description.jp = descriptionLines.join('\n');
    } else if (currentSection === 'specs' && trimmed.startsWith('-')) {
      // Parse list item: "- Label (EN / JP): Value (EN / JP)" or simple "- Label: Value"
      const specLine = trimmed.substring(1).trim();
      const separatorIndex = specLine.indexOf(':');
      if (separatorIndex !== -1) {
        const labelRaw = specLine.substring(0, separatorIndex).trim();
        const valueRaw = specLine.substring(separatorIndex + 1).trim();

        // Check for slash separated translations like "尺寸 (Dimensions / サイズ)"
        // For simplicity, if we don't have distinct translations, we default to the raw value for all.
        const parseMultilingual = (str) => {
          // Detect formats like "中文字 (English / 日本語)"
          const match = str.match(/(.*?)\((.*?)\/(.*?)\)/);
          if (match) {
            return {
              tw: match[1].trim(),
              en: match[2].trim(),
              jp: match[3].trim()
            };
          }
          return { tw: str, en: str, jp: str };
        };

        product.specs.push({
          label: parseMultilingual(labelRaw),
          value: parseMultilingual(valueRaw)
        });
      }
    }
  }

  // Generate clean ID from English name
  const nameToUse = product.name.en || product.name.tw;
  product.id = nameToUse.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

  return product;
}

// Main execution function
function main() {
  console.log('--- Sunnyward Product Import Script ---');

  if (!fs.existsSync(RAW_TEXTS_DIR)) {
    console.log('Staging raw_texts folder not found.');
    return;
  }

  const files = fs.readdirSync(RAW_TEXTS_DIR).filter(f => f.endsWith('.txt') || f.endsWith('.md'));
  if (files.length === 0) {
    console.log('No raw product text files found in staging.');
    return;
  }

  // Read existing database or create new skeleton
  let db = {
    settings: {
      supportedLanguages: ['tw', 'en', 'jp'],
      defaultLanguage: 'tw'
    },
    categories: {
      dining: {
        name: { tw: '設計師餐椅', en: 'Designer Dining Chairs', jp: 'デザイナーダイニングチェア' },
        desc: {
          tw: '工程級商用單椅，採用人體工學靠背支撐與剛性卡榫結構，專為高流量餐飲空間打造。',
          en: 'Contract-grade commercial chairs featuring ergonomic back support and rigid joinery built for high-traffic environments.',
          jp: 'エルゴノミクスに基づいた背もたれと高剛性の接合構造を持ち、高頻度な使用に耐えうる商業空間向けチェア。'
        }
      },
      stools: {
        name: { tw: '高強度吧檯椅', en: 'Commercial Bar Stools', jp: '高強度カウンターチェア' },
        desc: {
          tw: '商業空間剛性吧檯椅，具備防鏽鋼製結構與耐磨防刮塗層，適用於吧檯、高腳桌區域。',
          en: 'Heavy-duty commercial bar stools with rust-proof steel frames and abrasion-resistant coating, perfect for bar and high table zones.',
          jp: '商業空間用の高耐久バーチェア。防錆スチールフレームと耐摩耗性コーティングを施し、バーやハイテーブルエリアに最適です。'
        }
      },
      lounge: {
        name: { tw: '沙發休閒椅', en: 'Premium Lounge Chairs', jp: 'プレミアムラウンジチェア' },
        desc: {
          tw: '精選奢華休閒椅，配備寬大支撐的座面幾何形狀與高回彈軟墊，適用於大廳與精品休息區。',
          en: 'Curated premium lounge chairs with generous seating profiles and high-resilience cushioning, ideal for lobbies and boutique lounge areas.',
          jp: 'ゆったりとした座面と高反発クッションを備えた高級ラウンジチェア。ロビーや特別待合室に最適です。'
        }
      }
    },
    products: []
  };

  if (fs.existsSync(PRODUCTS_JSON_PATH)) {
    try {
      db = JSON.parse(fs.readFileSync(PRODUCTS_JSON_PATH, 'utf8'));
    } catch (e) {
      console.error('Error parsing existing products.json, recreating empty structure.', e);
    }
  }

  for (let file of files) {
    const filePath = path.join(RAW_TEXTS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    const newProduct = parseProductMarkdown(content);

    if (!newProduct.id) {
      console.log(`Skipped ${file}: Missing product name.`);
      continue;
    }

    // Process images
    const processedImages = [];
    for (let imgName of newProduct.images) {
      const rawImgPath = path.join(RAW_IMAGES_DIR, imgName);
      if (fs.existsSync(rawImgPath)) {
        // Generate optimized name
        const ext = path.extname(imgName);
        const newImgName = `${newProduct.id}${ext}`;
        const destImgPath = path.join(MEDIA_DIR, newImgName);
        
        // Move / copy image
        fs.copyFileSync(rawImgPath, destImgPath);
        processedImages.push(`../_assets/media/${newImgName}`);
        
        // Move raw image to processed
        const rawImgDest = path.join(PROCESSED_DIR, imgName);
        fs.renameSync(rawImgPath, rawImgDest);
        console.log(`Processed image: ${imgName} -> ${newImgName}`);
      } else {
        // Fallback or keep as-is if it's already an external/existing path
        processedImages.push(imgName);
        console.log(`Image not found in raw_images, keeping original value: ${imgName}`);
      }
    }
    newProduct.images = processedImages;

    // Merge/update into products array
    const existingIndex = db.products.findIndex(p => p.id === newProduct.id);
    if (existingIndex !== -1) {
      db.products[existingIndex] = { ...db.products[existingIndex], ...newProduct };
      console.log(`Updated product: ${newProduct.name.tw} (ID: ${newProduct.id})`);
    } else {
      db.products.push(newProduct);
      console.log(`Added new product: ${newProduct.name.tw} (ID: ${newProduct.id})`);
    }

    // Move text file to processed
    const txtDest = path.join(PROCESSED_DIR, file);
    if (fs.existsSync(txtDest)) {
      fs.unlinkSync(txtDest); // Remove old processed file if exists
    }
    fs.renameSync(filePath, txtDest);
  }

  // Save database
  ensureDir(path.dirname(PRODUCTS_JSON_PATH));
  fs.writeFileSync(PRODUCTS_JSON_PATH, JSON.stringify(db, null, 2), 'utf8');
  console.log(`Saved database to ${PRODUCTS_JSON_PATH}`);
}

main();
