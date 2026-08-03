import os
import re

css_content = """
/* Carousel for Visuals */
.uc-carousel {
  position: relative;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  background: #000;
}
.uc-carousel-inner {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}
.uc-carousel-inner::-webkit-scrollbar {
  display: none;
}
.uc-slide {
  flex: 0 0 100%;
  width: 100%;
  scroll-snap-align: start;
  position: relative;
}
.uc-slide video, .uc-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
/* Carousel Navigation */
.uc-carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.8);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #333;
  z-index: 10;
  transition: all 0.2s ease;
}
.uc-carousel-btn:hover {
  background: #fff;
  color: var(--copper);
}
.uc-carousel-btn.prev { left: 10px; }
.uc-carousel-btn.next { right: 10px; }
.uc-carousel-dots {
  position: absolute;
  bottom: 15px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 10;
}
.uc-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  cursor: pointer;
  transition: 0.3s;
}
.uc-dot.active {
  background: #fff;
  transform: scale(1.2);
}
"""

js_content = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  const carousels = document.querySelectorAll('.uc-carousel');
  carousels.forEach(carousel => {
    const inner = carousel.querySelector('.uc-carousel-inner');
    const prevBtn = carousel.querySelector('.prev');
    const nextBtn = carousel.querySelector('.next');
    const dots = carousel.querySelectorAll('.uc-dot');
    
    let currentIndex = 0;
    const slideCount = dots.length;

    function updateCarousel() {
      const width = carousel.offsetWidth;
      inner.scrollTo({ left: width * currentIndex, behavior: 'smooth' });
      dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentIndex);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % slideCount;
        updateCarousel();
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + slideCount) % slideCount;
        updateCarousel();
      });
    }
    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        currentIndex = index;
        updateCarousel();
      });
    });

    // Optional: listen to scroll to update dots
    inner.addEventListener('scroll', () => {
      const width = carousel.offsetWidth;
      const scrollLeft = inner.scrollLeft;
      const newIndex = Math.round(scrollLeft / width);
      if (newIndex !== currentIndex && newIndex >= 0 && newIndex < slideCount) {
        currentIndex = newIndex;
        dots.forEach((dot, index) => {
          dot.classList.toggle('active', index === currentIndex);
        });
      }
    });
  });
});
</script>
"""

def inject_css(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'Carousel for Visuals' not in content:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(css_content)

def transform_visuals(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to replace:
    # <div class="uc-visuals scroll-reveal">
    #   <div class="uc-video-wrap">
    #     <video src="../_assets/projects/2026.01 Kai restaurant.mp4" autoplay loop muted playsinline preload="metadata"></video>
    #   </div>
    #   <div class="uc-img-wrap" style="position: relative;">
    #     <div style="position: absolute; ...">Before & After Highlight</div>
    #     <img src="../_assets/projects/..." alt="..." loading="lazy">
    #   </div>
    # </div>
    # With a carousel structure.
    
    # Regex to find uc-visuals blocks
    pattern = r'<div class="uc-visuals scroll-reveal">\s*<div class="uc-video-wrap">\s*<video src="([^"]+)"(.*?)</video>\s*</div>\s*<div class="uc-img-wrap" style="position: relative;">\s*<div.*?</div>\s*<img src="([^"]+)" alt="([^"]+)" loading="lazy">\s*</div>\s*</div>'
    
    def replacer(match):
        video_src = match.group(1)
        video_attrs = match.group(2)
        img_src = match.group(3)
        img_alt = match.group(4)
        
        return f'''<div class="uc-visuals scroll-reveal">
          <div class="uc-carousel">
            <div class="uc-carousel-inner">
              <div class="uc-slide">
                <video src="{video_src}"{video_attrs}</video>
              </div>
              <div class="uc-slide">
                <div style="position: absolute; top: 15px; left: 15px; background: rgba(0,0,0,0.7); color: #fff; padding: 4px 12px; font-size: 0.75rem; font-weight: bold; letter-spacing: 1px; border-radius: 4px; text-transform: uppercase; z-index: 5;">Before & After Highlight</div>
                <img src="{img_src}" alt="{img_alt}" loading="lazy">
              </div>
            </div>
            <button class="uc-carousel-btn prev">❮</button>
            <button class="uc-carousel-btn next">❯</button>
            <div class="uc-carousel-dots">
              <div class="uc-dot active"></div>
              <div class="uc-dot"></div>
            </div>
          </div>
        </div>'''
        
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    # Inject JS at the end of body if not there
    if 'updateCarousel()' not in new_content:
        new_content = new_content.replace('</body>', js_content + '\n</body>')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
inject_css(os.path.join(base_path, "css", "style.css"))
transform_visuals(os.path.join(base_path, "en", "projects.html"))
transform_visuals(os.path.join(base_path, "tw", "projects.html"))
transform_visuals(os.path.join(base_path, "jp", "projects.html"))
print("Successfully transformed uc-visuals into carousels.")
