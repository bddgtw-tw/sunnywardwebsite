const SITE_VERSION = "v2.4.0";

document.addEventListener("DOMContentLoaded", () => {

  // Project films start with an accessible, localized title card.
  document.querySelectorAll(".uc-video-poster").forEach(poster => {
    const video = poster.parentElement?.querySelector("video");
    if (!video) return;
    poster.addEventListener("click", () => {
      video.controls = true;
      const playback = video.play();
      if (playback && typeof playback.then === "function") {
        playback.then(() => poster.classList.add("is-hidden")).catch(() => {});
      } else {
        poster.classList.add("is-hidden");
      }
    });
    video.addEventListener("play", () => poster.classList.add("is-hidden"));
    video.addEventListener("ended", () => poster.classList.remove("is-hidden"));
  });

  // Inject version into footer
  document.querySelectorAll(".site-version").forEach(el => {
    el.textContent = SITE_VERSION;
  });

  // 1. PAGE TRANSITION
  document.body.classList.add("page-ready");

  // 2. LANGUAGE SWITCHER CLICK-TOGGLE & CACHE
  document.querySelectorAll(".lang-dropdown").forEach(dropdown => {
    const current = dropdown.querySelector(".lang-current");
    if (current) {
      current.setAttribute("aria-haspopup", "true");
      current.setAttribute("aria-expanded", "false");
      current.addEventListener("click", e => {
        e.stopPropagation();
        // Close others
        document.querySelectorAll(".lang-dropdown").forEach(d => {
          if (d !== dropdown) {
            d.classList.remove("open");
            const c = d.querySelector(".lang-current");
            if (c) c.setAttribute("aria-expanded", "false");
          }
        });
        const isOpen = dropdown.classList.toggle("open");
        current.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
    }
  });

  document.addEventListener("click", () => {
    document.querySelectorAll(".lang-dropdown").forEach(dropdown => {
      dropdown.classList.remove("open");
      const current = dropdown.querySelector(".lang-current");
      if (current) current.setAttribute("aria-expanded", "false");
    });
  });

  document.addEventListener("keydown", e => {
    if (e.key !== "Escape") return;
    document.querySelectorAll(".lang-dropdown.open").forEach(dropdown => {
      dropdown.classList.remove("open");
      const current = dropdown.querySelector(".lang-current");
      if (current) {
        current.setAttribute("aria-expanded", "false");
        current.focus();
      }
    });
  });

  document.querySelectorAll(".lang-dropdown-item").forEach(item => {
    item.addEventListener("click", function() {
      const lang = this.getAttribute("data-lang");
      if (lang) localStorage.setItem("sw_lang", lang);
    });
  });

  // SPA routing interception for category links
  document.addEventListener("click", e => {
    const link = e.target.closest('a[href*="category="]');
    if (link) {
      const url = new URL(link.href, window.location.href);
      if (url.pathname.endsWith("products.html") && window.location.pathname.endsWith("products.html")) {
        e.preventDefault();
        const cat = url.searchParams.get("category");
        if (cat && typeof window.switchCategory === "function") {
          window.switchCategory(cat.toLowerCase());
          window.history.pushState(null, "", link.href);
        }
      }
    }
  });

  // 3. HEADER SCROLL BEHAVIOUR
  const header = document.getElementById("site-header");
  if (header) {
    const onScroll = () => {
      if (window.scrollY > 60) {
        header.classList.add("nav-scrolled");
        header.classList.remove("nav-transparent");
      } else {
        header.classList.remove("nav-scrolled");
        // Only re-add transparent if it started transparent (hero pages)
        if (header.dataset.transparent === "true") header.classList.add("nav-transparent");
      }
    };
    if (header.classList.contains("nav-transparent")) header.dataset.transparent = "true";
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // 4. MOBILE DRAWER
  const toggle = document.getElementById("mobile-toggle");
  const drawer = document.getElementById("mobile-drawer");
  if (toggle && drawer) {
    toggle.addEventListener("click", () => {
      const isOpen = drawer.classList.toggle("open");
      toggle.classList.toggle("open", isOpen);
      toggle.setAttribute("aria-expanded", isOpen);
      document.body.style.overflow = isOpen ? "hidden" : "";
    });
  }

  // 5. MAGNETIC BUTTONS
  document.querySelectorAll(".magnetic-wrap").forEach(wrap => {
    const btn = wrap.querySelector(".btn") || wrap;
    btn.addEventListener("mouseenter", () => { btn.style.transition = "none"; });
    btn.addEventListener("mousemove", e => {
      const r = btn.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width  / 2) * 0.3;
      const y = (e.clientY - r.top  - r.height / 2) * 0.3;
      btn.style.transform = `translate(${x}px, ${y}px)`;
    });
    btn.addEventListener("mouseleave", () => {
      btn.style.transition = "transform 0.55s cubic-bezier(0.16,1,0.3,1)";
      btn.style.transform = "translate(0,0)";
    });
  });

  // 6. OFFICE STATUS BADGE
  function renderStatus() {
    document.querySelectorAll(".office-status").forEach(el => {
      const offset = parseInt(el.getAttribute("data-offset") || "8");
      const now = new Date();
      const local = new Date(now.getTime() + (now.getTimezoneOffset() * 60000) + (3600000 * offset));
      const day = local.getDay(), h = local.getHours(), m = local.getMinutes();
      const dec = h + m / 60;
      const open = day >= 1 && day <= 5 && dec >= 8.5 && dec < 17.5;
      const t = local.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: false });
      const lang = document.documentElement.lang || "en";
      let txt = "";
      if (lang === "tw")      txt = open ? `営業中 (本地時間 ${t})` : `休息中 (本地時間 ${t})`;
      else if (lang === "ja") txt = open ? `営業中 (現地時間 ${t})` : `営業時間外 (現地時間 ${t})`;
      else                    txt = open ? `Open Now · ${t} SGT` : `Closed · ${t} SGT`;
      el.innerHTML = `<span class="badge ${open ? "badge-open" : "badge-closed"}"><span class="dot"></span>${txt}</span>`;
    });
  }
  renderStatus();
  setInterval(renderStatus, 15000);

  // 7. TABLE MATCHER
  const topOpts  = document.querySelectorAll(".matcher-option-top");
  const baseOpts = document.querySelectorAll(".matcher-option-base");
  let selTop = "marble", selBase = "round";

  const tops = {
    marble:     { name: "Cultured Marble",    bg: "radial-gradient(circle, #F2F1EC 0%, #CFCAC4 100%)", desc: "Non-porous surface. Mimics natural marble. Heat, scratch and stain-resistant." },
    rubberwood: { name: "Compressed Rubberwood", bg: "radial-gradient(circle, #DFD4C6 0%, #B8A895 100%)", desc: "High-density heat-pressed. Moisture-resistant. Available in 14 colourways." },
    phenolic:   { name: "Phenolic Compact",   bg: "radial-gradient(circle, #4A413A 0%, #2A2420 100%)", desc: "Multi-layer phenolic resin. Maximum abrasion and impact resistance." },
    fiberglass: { name: "Fibreglass (FRP)",   bg: "radial-gradient(circle, #FFFFFF 0%, #E0E6EC 100%)", desc: "Lightweight, fully corrosion-proof. Ideal for outdoor and coastal environments." }
  };
  const bases = {
    round:   { name: "Round Disc Pedestal", w: "40%", r: "50% 50% 0 0" },
    square:  { name: "Square Disc Pedestal", w: "40%", r: "2px 2px 0 0" },
    xleg:    { name: "X-Cross Steel",        w: "8%",  r: "0" },
    hleg:    { name: "4-Leg Frame",          w: "16%", r: "0" }
  };

  function updateMatcher() {
    const top = tops[selTop], base = bases[selBase];
    const rt = document.getElementById("matcher-render-top");
    const rb = document.getElementById("matcher-render-base");
    const tit = document.getElementById("matcher-title");
    const dsc = document.getElementById("matcher-desc");
    const btn = document.getElementById("matcher-inquire-btn");
    if (!rt) return;
    rt.style.background = top.bg;
    rb.style.width = base.w;
    rb.style.borderRadius = base.r;
    if (tit) tit.textContent = top.name + " + " + base.name;
    if (dsc) dsc.textContent = top.desc;
    if (btn) {
      const sub = encodeURIComponent("Table Config Inquiry: " + top.name + " + " + base.name);
      const body = encodeURIComponent("Hello Sunnyward,\n\nI am interested in:\n- Tabletop: " + top.name + "\n- Base: " + base.name + "\n\nPlease provide a quote. Thank you.");
      btn.href = "mailto:sales@sunnyward.com?subject=" + sub + "&body=" + body;
    }
  }

  topOpts.forEach(o => {
    o.addEventListener("click", function() {
      topOpts.forEach(x => x.classList.remove("active"));
      this.classList.add("active");
      selTop = this.dataset.top;
      updateMatcher();
    });
  });
  baseOpts.forEach(o => {
    o.addEventListener("click", function() {
      baseOpts.forEach(x => x.classList.remove("active"));
      this.classList.add("active");
      selBase = this.dataset.base;
      updateMatcher();
    });
  });
  if (topOpts.length) updateMatcher();

  // 8. CATALOG MODAL (Dynamic Multi-step)
  const catalogs = [
    { id: "cat1", name: "2025 Funife Premium Outdoor Catalogue (A4)", file: "../catalogs/2025_Funife_Premium_Outdoor_catalogue_A4.pdf" },
    { id: "cat2", name: "2026 Sunnyward Balau Wood Outdoor Furniture", file: "../catalogs/2026_Sunnyward_Balau_wood_outdoor_furniture_catalogue.pdf" },
    { id: "cat3", name: "2026 SWA Office Furniture Specification", file: "../catalogs/2026_SWA_Office_Furniture_Specification.pdf" },
    { id: "cat4", name: "2026 SWA Outdoor Selection Catalog", file: "../catalogs/2026_SWA_Outdoor_Selection_Catalog.pdf" },
    { id: "cat5", name: "2026 SWA Project Catalog", file: "../catalogs/2026_SWA_project_catalog.pdf" },
    { id: "cat6", name: "SWA Racking System", file: "../catalogs/SWA_Racking_System.pdf" }
  ];

  function createCatalogModal() {
    if (document.getElementById("catalog-modal")) return;
    
    const lang = document.documentElement.lang || "en";
    const t = {
      title: lang === "ja" ? "カタログのダウンロード" : lang === "tw" ? "下載型錄" : "Download Catalog",
      desc1: lang === "ja" ? "ダウンロードするカタログを選択してください（複数選択可）。" : lang === "tw" ? "請選擇您要下載的型錄 (可多選)。" : "Select the catalogs you wish to download (multiple allowed).",
      desc2: lang === "ja" ? "詳細を入力して、選択したPDFを受け取ります。" : lang === "tw" ? "請輸入您的聯絡資訊以取得 PDF。" : "Enter your details to receive the selected PDFs.",
      next: lang === "ja" ? "次へ" : lang === "tw" ? "下一步" : "Next",
      download: lang === "ja" ? "送信してダウンロード" : lang === "tw" ? "送出並下載" : "Send & Download",
      name: lang === "ja" ? "氏名" : lang === "tw" ? "姓名" : "Full Name",
      email: lang === "ja" ? "勤務先メールアドレス" : lang === "tw" ? "公司信箱" : "Business Email",
      back: lang === "ja" ? "戻る" : lang === "tw" ? "返回" : "Back",
      err: lang === "ja" ? "少なくとも1つのカタログを選択してください。" : lang === "tw" ? "請至少選擇一份型錄。" : "Please select at least one catalog.",
      success: lang === "ja" ? "ありがとうございます！ダウンロードが開始されます。" : lang === "tw" ? "感謝填寫！下載即將開始。" : "Thank you! Downloads will begin shortly."
    };

    const modalHTML = `
      <div class="modal" id="catalog-modal">
        <div class="modal-overlay modal__overlay" id="catalog-overlay"></div>
        <div class="modal-content modal__box" style="max-width: 500px;">
          <button class="modal-close modal__close" id="catalog-close">&times;</button>
          <h3 class="modal__title">${t.title}</h3>
          
          <!-- Step 1: Selection -->
          <div id="catalog-step-1">
            <p class="modal__desc">${t.desc1}</p>
            <div class="catalog-list" style="margin-bottom: 2rem; max-height: 300px; overflow-y: auto; text-align: left; background: var(--bg-alt); padding: 1rem; border-radius: 4px;">
              ${catalogs.map(c => `
                <label style="display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.75rem; cursor: pointer;">
                  <input type="checkbox" name="selected_catalogs" value="${c.file}" style="margin-top: 0.3rem;">
                  <span style="font-size: 0.95rem; line-height: 1.4;">${c.name}</span>
                </label>
              `).join('')}
            </div>
            <button class="btn btn-primary" id="catalog-next-btn" style="width: 100%;">${t.next}</button>
          </div>

          <!-- Step 2: Form -->
          <div id="catalog-step-2" style="display: none;">
            <p class="modal__desc">${t.desc2}</p>
            <form id="catalog-form">
              <div class="form-field" style="text-align: left;">
                <label for="catalog-name" class="form-label">${t.name}</label>
                <input type="text" id="catalog-name" class="form-input" required>
              </div>
              <div class="form-field" style="text-align: left;">
                <label for="catalog-email" class="form-label">${t.email}</label>
                <input type="email" id="catalog-email" class="form-input" required>
              </div>
              <div style="display: flex; gap: 1rem;">
                <button type="button" class="btn btn-ghost" id="catalog-back-btn" style="flex: 1;">${t.back}</button>
                <button type="submit" class="btn btn-primary" style="flex: 2;">${t.download}</button>
              </div>
            </form>
          </div>
          
        </div>
      </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = document.getElementById("catalog-modal");
    const closeBtn = document.getElementById("catalog-close");
    const overlay = document.getElementById("catalog-overlay");
    const nextBtn = document.getElementById("catalog-next-btn");
    const backBtn = document.getElementById("catalog-back-btn");
    const form = document.getElementById("catalog-form");
    
    const s1 = document.getElementById("catalog-step-1");
    const s2 = document.getElementById("catalog-step-2");

    const close = () => {
      modal.classList.remove("active");
      setTimeout(() => { s1.style.display = 'block'; s2.style.display = 'none'; form.reset(); }, 300);
    };

    closeBtn.addEventListener("click", close);
    overlay.addEventListener("click", close);

    nextBtn.addEventListener("click", () => {
      const selected = document.querySelectorAll('input[name="selected_catalogs"]:checked');
      if (selected.length === 0) {
        alert(t.err);
        return;
      }
      s1.style.display = 'none';
      s2.style.display = 'block';
    });

    backBtn.addEventListener("click", () => {
      s2.style.display = 'none';
      s1.style.display = 'block';
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const selected = document.querySelectorAll('input[name="selected_catalogs"]:checked');
      
      alert(t.success);
      
      selected.forEach((cb, index) => {
        setTimeout(() => {
          const a = document.createElement("a");
          a.href = cb.value;
          a.download = "";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        }, index * 500); // Stagger downloads
      });
      
      close();
    });
  }

  createCatalogModal();
  document.querySelectorAll(".open-catalog-btn").forEach(b => {
    b.addEventListener("click", e => { 
      e.preventDefault(); 
      document.getElementById("catalog-modal").classList.add("active"); 
    });
  });

  // 9. INTERSECTION OBSERVER — REVEAL ANIMATIONS
  const revealEl = document.querySelectorAll(".scroll-reveal, .reveal, .reveal-fade");
  const obs = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: "0px 0px -60px 0px" });
  revealEl.forEach(el => obs.observe(el));

  // 10. HERO SCROLL CTA
  const heroScroll = document.querySelector(".hero__scroll");
  if (heroScroll) {
    heroScroll.addEventListener("click", () => {
      window.scrollTo({ top: window.innerHeight, behavior: "smooth" });
    });
  }
});
