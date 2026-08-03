const fs = require('fs');

const catTranslations = {
  office: "Office Desks & Chairs",
  dining: "Dining Chairs",
  stools: "Bar Stools",
  lounge: "Lounge Chairs",
  outdoor: "Outdoor Furniture",
  equipment: "Commercial Racks",
  materials: "Tabletops & Bases"
};

const products = JSON.parse(fs.readFileSync('en/products.json', 'utf-8'));
let allProducts = products.sort((a, b) => Number(Boolean(b.img && b.img.trim())) - Number(Boolean(a.img && a.img.trim())));

const counts = {};
const grouped = {};
Object.keys(catTranslations).forEach(key => {
  counts[key] = 0;
  grouped[key] = [];
});

allProducts.forEach(p => {
  if (grouped[p.tab]) {
    grouped[p.tab].push(p);
    counts[p.tab]++;
  }
});

function renderCards(products) {
  return products.map(p => {
    return `
      <article class="product-card" role="button" tabindex="0" aria-label="View specifications for ${p.name}" data-product-sku="${encodeURIComponent(p.sku)}" onclick="openProductModalBySku(this.dataset.productSku)" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();openProductModalBySku(this.dataset.productSku)}" style="cursor: pointer;">
        <div class="product-card__image product-img-wrapper">
          ${p.img && p.img.trim() ? `<img src="${p.img}" alt="${p.name}" class="product-img" loading="lazy" onerror="markImagePending(this)">` : `<div class="product-image-pending">Image pending</div>`}
          <div class="product-card__overlay"></div>
          <button class="product-card__cta" onclick="event.stopPropagation(); inquire('${p.name}', '${p.sku}')">Inquire</button>
        </div>
        <div class="product-card__body product-info">
          <div class="product-card__name product-title" style="display:flex; justify-content:space-between; align-items:flex-start;">
            <span>${p.name}</span>
            <span style="font-size:0.68rem; background:#eae5e0; padding:2px 6px; border-radius:4px; font-weight:normal; color:#777;">${p.sku}</span>
          </div>
          <div class="product-card__desc" style="font-size:0.8rem; margin-top:0.3rem; color:#666; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">${p.desc}</div>
        </div>
        <div class="product-card__meta product-size">
          <span class="product-card__dims" style="font-size:0.72rem; color:#888;">📐 ${p.dims}</span>
          <a class="btn-arrow" href="#" onclick="event.stopPropagation(); inquire('${p.name}', '${p.sku}')" style="font-size:0.7rem;">RFQ</a>
        </div>
      </article>
    `;
  }).join('');
}

let stageHtml = "";
Object.keys(catTranslations).forEach((key, idx) => {
  const isActive = idx === 0 ? "active" : "";
  if (key === "materials") {
      stageHtml += "materials html";
  } else {
    try {
      stageHtml += `
        <div class="product-category-group ${isActive}" id="cat-${key}">
          <div class="cat-header">
            <h3>${catTranslations[key]}</h3>
            <span class="cat-header-count">Featured ${counts[key]} models</span>
          </div>
          <div class="products-grid">
            ${renderCards(grouped[key])}
          </div>
        </div>
      `;
    } catch (e) {
      console.error("ERROR IN renderCards for " + key, e);
    }
  }
});

console.log("Success! Rendered stageHtml length:", stageHtml.length);
