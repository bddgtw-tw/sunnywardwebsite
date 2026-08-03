import json
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        
    def handle_starttag(self, tag, attrs):
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
            self.stack.append(tag)
            
    def handle_endtag(self, tag):
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            else:
                print(f"Mismatched tag: expected {self.stack[-1] if self.stack else 'nothing'}, got {tag}")

def test():
    with open('en/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
        
    outdoor = [p for p in products if p.get('tab') == 'outdoor']
    html = ""
    for p in outdoor:
        name = p.get('name', '').replace('"', '&quot;')
        sku = p.get('sku', '').replace('"', '&quot;')
        desc = p.get('desc', '')
        dims = p.get('dims', '')
        img = p.get('img', '')
        
        card = f"""
        <article class="product-card" data-product-sku="{sku}">
            <div class="product-card__image product-img-wrapper">
                <img src="{img}" alt="{name}">
            </div>
            <div class="product-card__body">
                <div class="product-card__name"><span>{name}</span></div>
                <div class="product-card__desc">{desc}</div>
            </div>
        </article>
        """
        html += card

    print(f"Checking HTML with length {len(html)}")
    parser = MyHTMLParser()
    parser.feed(html)
    print("Remaining stack:", parser.stack)

test()
