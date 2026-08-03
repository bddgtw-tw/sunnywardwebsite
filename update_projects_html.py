import os
import re

def update_file(filepath, lang):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the HTML project cards
    cards_html = """
        <!-- Case 1: Tsutaya Bookstore -->
        <div class="project-card scroll-reveal" onclick="openProjectModal(0)" style="cursor: pointer;">
          <div class="project-img-wrapper" style="background-color: var(--bg-secondary); overflow: hidden; position: relative;">
            <video src="../_assets/projects/2024.11_tsutaya_bookstore.mp4#t=0.1" muted playsinline style="width:100%; height:100%; object-fit:cover;" onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="project-info">
            <span class="project-meta">BOOKSTORE</span>
            <h3 style="font-size:1.6rem; margin-bottom:0.5rem;">Tsutaya Bookstore</h3>
            <p class="project-desc">Premium furniture integrated seamlessly into the modern bookstore environment.</p>
          </div>
        </div>

        <!-- Case 2: Legoland Cafeteria -->
        <div class="project-card scroll-reveal" onclick="openProjectModal(1)" style="cursor: pointer; transition-delay: 0.15s;">
          <div class="project-img-wrapper" style="background-color: var(--bg-secondary); overflow: hidden; position: relative;">
            <video src="../_assets/projects/2025.12_legoland_cafeteria.mp4#t=0.1" muted playsinline style="width:100%; height:100%; object-fit:cover;" onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="project-info">
            <span class="project-meta">THEME PARK</span>
            <h3 style="font-size:1.6rem; margin-bottom:0.5rem;">Legoland Cafeteria</h3>
            <p class="project-desc">Durable and colorful dining furniture for high traffic family areas.</p>
          </div>
        </div>

        <!-- Case 3: Sushi Plus Outlet -->
        <div class="project-card scroll-reveal" onclick="openProjectModal(2)" style="cursor: pointer;">
          <div class="project-img-wrapper" style="background-color: var(--bg-secondary); overflow: hidden; position: relative;">
            <video src="../_assets/projects/2026.06_sushi_plus_outlet.mp4#t=0.1" muted playsinline style="width:100%; height:100%; object-fit:cover;" onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="project-info">
            <span class="project-meta">RESTAURANT</span>
            <h3 style="font-size:1.6rem; margin-bottom:0.5rem;">Sushi Plus Outlet</h3>
            <p class="project-desc">High-turnover dining area with easy-to-clean, comfortable seating.</p>
          </div>
        </div>

        <!-- Case 4: Family Restaurant -->
        <div class="project-card scroll-reveal" onclick="openProjectModal(3)" style="cursor: pointer; transition-delay: 0.15s;">
          <div class="project-img-wrapper" style="background-color: var(--bg-secondary); overflow: hidden; position: relative;">
            <video src="../_assets/projects/2024.01_family_restaurant.mp4#t=0.1" muted playsinline style="width:100%; height:100%; object-fit:cover;" onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="project-info">
            <span class="project-meta">RESTAURANT</span>
            <h3 style="font-size:1.6rem; margin-bottom:0.5rem;">Family Restaurant</h3>
            <p class="project-desc">Family restaurant seating solutions focusing on comfort and durability.</p>
          </div>
        </div>

        <!-- Case 5: Kai Restaurant -->
        <div class="project-card scroll-reveal" onclick="openProjectModal(4)" style="cursor: pointer;">
          <div class="project-img-wrapper" style="background-color: var(--bg-secondary); overflow: hidden; position: relative;">
            <video src="../_assets/projects/2026.01_kai_restaurant.mp4#t=0.1" muted playsinline style="width:100%; height:100%; object-fit:cover;" onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="project-info">
            <span class="project-meta">PREMIUM DINING</span>
            <h3 style="font-size:1.6rem; margin-bottom:0.5rem;">Kai Restaurant</h3>
            <p class="project-desc">Premium dining furniture elevating the culinary experience.</p>
          </div>
        </div>

        <!-- Case 6: Dragon Ginseng -->
        <div class="project-card scroll-reveal" onclick="openProjectModal(5)" style="cursor: pointer; transition-delay: 0.15s;">
          <div class="project-img-wrapper" style="background-color: var(--bg-secondary); overflow: hidden; position: relative;">
            <video src="../_assets/projects/2024.05_dragon_ginseng.mp4#t=0.1" muted playsinline style="width:100%; height:100%; object-fit:cover;" onmouseover="this.play()" onmouseout="this.pause()"></video>
          </div>
          <div class="project-info">
            <span class="project-meta">COMMERCIAL</span>
            <h3 style="font-size:1.6rem; margin-bottom:0.5rem;">Dragon Ginseng</h3>
            <p class="project-desc">Blending traditional aesthetics with modern comfort.</p>
          </div>
        </div>
"""
    # Use regex to replace everything inside <div class="projects-grid"> ... </div>
    content = re.sub(r'(<div class="projects-grid">).*?(</div>\s*</div>\s*</section>)', r'\1\n' + cards_html + r'\n\2', content, flags=re.DOTALL)

    # 2. Update Modal HTML
    modal_img_html = """          <img id="project-modal-img" src="" alt="" style="width: 100%; border-radius: 8px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">"""
    new_modal_html = """          <div id="project-modal-media-container" style="width: 100%; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <img id="project-modal-img" src="" alt="" style="width: 100%; display: block; object-fit: cover;">
            <video id="project-modal-video" src="" style="width: 100%; display: none; object-fit: cover;" autoplay loop muted playsinline></video>
          </div>"""
    content = content.replace(modal_img_html, new_modal_html)

    # 3. Update JavaScript Data
    js_data = """    const projectsData = [
      {
        title: "Tsutaya Bookstore",
        location: "Global",
        img: "../_assets/projects/2024.11_tsutaya_bookstore.mp4",
        isVideo: true,
        desc: "Premium furniture integrated seamlessly into the modern bookstore environment.",
        products: []
      },
      {
        title: "Legoland Cafeteria",
        location: "Global",
        img: "../_assets/projects/2025.12_legoland_cafeteria.mp4",
        isVideo: true,
        desc: "Durable and colorful dining furniture for high traffic family areas.",
        products: []
      },
      {
        title: "Sushi Plus Outlet",
        location: "Global",
        img: "../_assets/projects/2026.06_sushi_plus_outlet.mp4",
        isVideo: true,
        desc: "High-turnover dining area with easy-to-clean, comfortable seating.",
        products: []
      },
      {
        title: "Family Restaurant",
        location: "Global",
        img: "../_assets/projects/2024.01_family_restaurant.mp4",
        isVideo: true,
        desc: "Family restaurant seating solutions focusing on comfort and durability.",
        products: []
      },
      {
        title: "Kai Restaurant",
        location: "Global",
        img: "../_assets/projects/2026.01_kai_restaurant.mp4",
        isVideo: true,
        desc: "Premium dining furniture elevating the culinary experience.",
        products: []
      },
      {
        title: "Dragon Ginseng",
        location: "Global",
        img: "../_assets/projects/2024.05_dragon_ginseng.mp4",
        isVideo: true,
        desc: "Blending traditional aesthetics with modern comfort.",
        products: []
      }
    ];"""
    
    content = re.sub(r'const projectsData = \[.*?\];', js_data, content, flags=re.DOTALL)

    # 4. Update JS Modal Logic
    old_modal_js = """      document.getElementById('project-modal-img').src = p.img;
      document.getElementById('project-modal-img').alt = p.title;"""
    
    new_modal_js = """      if (p.isVideo) {
        document.getElementById('project-modal-img').style.display = 'none';
        document.getElementById('project-modal-video').src = p.img;
        document.getElementById('project-modal-video').style.display = 'block';
      } else {
        document.getElementById('project-modal-video').style.display = 'none';
        document.getElementById('project-modal-img').src = p.img;
        document.getElementById('project-modal-img').alt = p.title;
        document.getElementById('project-modal-img').style.display = 'block';
      }"""
    content = content.replace(old_modal_js, new_modal_js)

    old_close_js = """      document.getElementById('project-detail-modal').classList.remove('active');"""
    new_close_js = """      document.getElementById('project-detail-modal').classList.remove('active');
      document.getElementById('project-modal-video').pause();
      document.getElementById('project-modal-video').src = "";"""
    content = content.replace(old_close_js, new_close_js)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
update_file(os.path.join(base_path, "en", "projects.html"), "en")
update_file(os.path.join(base_path, "tw", "projects.html"), "tw")
update_file(os.path.join(base_path, "jp", "projects.html"), "jp")
print("Updated all projects.html files.")
