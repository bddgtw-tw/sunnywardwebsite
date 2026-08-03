from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COPY = {
    "en": {"heading":"Prepare a project enquiry","name":"Your name","name_ph":"e.g. Sarah Jenkins","company":"Company / organisation","company_ph":"e.g. Studio North","email":"Work email","email_ph":"e.g. sarah@interiors.com","phone":"Phone (optional)","phone_ph":"e.g. +65 9123 4567","market":"Project country / market (optional)","market_ph":"e.g. Singapore","subject":"Subject","subject_ph":"e.g. Quote request for resort project","message":"Requirements and specifications","message_ph":"Please include product, quantity, delivery location and target timeline.","prepare":"Prepare enquiry options","status":"Complete the form to prepare an enquiry draft. Nothing is sent automatically.","email_action":"Continue with Email","wa_action":"Continue with WhatsApp","copy":"Copy draft"},
    "tw": {"heading":"準備專案詢價草稿","name":"聯絡人姓名","name_ph":"例如：林設計師","company":"公司／組織名稱","company_ph":"例如：晴川設計事務所","email":"公司電子信箱","email_ph":"例如：designer@studio.com","phone":"聯絡電話（選填）","phone_ph":"例如：+886 912-345-678","market":"專案國家／市場（選填）","market_ph":"例如：新加坡","subject":"詢價主旨","subject_ph":"例如：度假飯店家具報價需求","message":"需求詳情與規格","message_ph":"請提供產品、數量、交貨地點與預計時程。","prepare":"準備詢價傳送方式","status":"填寫表單後將產生詢價草稿；網站不會自動送出任何資料。","email_action":"使用 Email 繼續","wa_action":"使用 WhatsApp 繼續","copy":"複製草稿"},
    "jp": {"heading":"プロジェクトお問い合わせの準備","name":"お名前","name_ph":"例：鈴木 太郎","company":"会社・組織名","company_ph":"例：サニーデザイン株式会社","email":"業務用メールアドレス","email_ph":"例：suzuki@studio.jp","phone":"電話番号（任意）","phone_ph":"例：+81 90-1234-5678","market":"プロジェクトの国・市場（任意）","market_ph":"例：日本","subject":"件名","subject_ph":"例：リゾート家具の見積もり依頼","message":"ご要望・仕様","message_ph":"製品、数量、納品先、希望時期をご記入ください。","prepare":"送信方法を準備する","status":"入力後にお問い合わせ下書きを作成します。情報が自動送信されることはありません。","email_action":"Email で続ける","wa_action":"WhatsApp で続ける","copy":"下書きをコピー"},
}

CONTACT_INFO = {
    "en": {"hours":"Our Singapore and Johor Bahru offices operate on UTC+8, Monday to Friday, 8:30 AM–5:30 PM. Response time depends on the project information provided.","whatsapp":"WhatsApp: <a href=\"https://wa.me/60165262894\" target=\"_blank\" rel=\"noopener\">+6016-526 2894</a> &amp; <a href=\"https://wa.me/60167252894\" target=\"_blank\" rel=\"noopener\">+6016-725 2894</a>"},
    "tw": {"hours":"新加坡與柔佛辦公室採 UTC+8 時區，週一至週五 8:30–17:30 營運；實際回覆時間依所提供的專案資料而定。","whatsapp":"WhatsApp：<a href=\"https://wa.me/60165262894\" target=\"_blank\" rel=\"noopener\">+6016-526 2894</a> &amp; <a href=\"https://wa.me/60167252894\" target=\"_blank\" rel=\"noopener\">+6016-725 2894</a>"},
    "jp": {"hours":"シンガポールおよびジョホールバルの営業時間は、月曜日から金曜日の8:30–17:30（UTC+8）です。回答時間は、ご提供いただく案件情報により異なります。","whatsapp":"WhatsApp：<a href=\"https://wa.me/60165262894\" target=\"_blank\" rel=\"noopener\">+6016-526 2894</a> &amp; <a href=\"https://wa.me/60167252894\" target=\"_blank\" rel=\"noopener\">+6016-725 2894</a>"},
}


def form_markup(c: dict[str, str]) -> str:
    return f'''<form class="contact-form" id="contact-inquiry-form">
            <h3 style="margin-bottom: 1.5rem; font-size:1.8rem;">{c['heading']}</h3>
            <div class="form-group"><label for="contact-name" class="form-label">{c['name']}</label><input type="text" id="contact-name" name="name" class="form-control" autocomplete="name" placeholder="{c['name_ph']}" required></div>
            <div class="form-group"><label for="contact-company" class="form-label">{c['company']}</label><input type="text" id="contact-company" name="company" class="form-control" autocomplete="organization" placeholder="{c['company_ph']}" required></div>
            <div class="form-group"><label for="contact-email" class="form-label">{c['email']}</label><input type="email" id="contact-email" name="email" class="form-control" autocomplete="email" placeholder="{c['email_ph']}" required></div>
            <div class="form-group"><label for="contact-phone" class="form-label">{c['phone']}</label><input type="tel" id="contact-phone" name="phone" class="form-control" autocomplete="tel" placeholder="{c['phone_ph']}"></div>
            <div class="form-group"><label for="contact-market" class="form-label">{c['market']}</label><input type="text" id="contact-market" name="market" class="form-control" autocomplete="country-name" placeholder="{c['market_ph']}"></div>
            <div class="form-group"><label for="contact-subject" class="form-label">{c['subject']}</label><input type="text" id="contact-subject" name="subject" class="form-control" placeholder="{c['subject_ph']}" required></div>
            <div class="form-group"><label for="contact-message" class="form-label">{c['message']}</label><textarea id="contact-message" name="message" class="form-control" placeholder="{c['message_ph']}" required></textarea></div>
            <button type="submit" class="btn btn-primary" style="width:100%; padding:1rem;">{c['prepare']}</button>
            <div class="inquiry-actions" id="inquiry-actions" hidden aria-live="polite">
              <p id="inquiry-status">{c['status']}</p>
              <div class="inquiry-actions__buttons"><a id="inquiry-email-action" class="btn btn-primary" href="mailto:sales@sunnyward.com">{c['email_action']}</a><a id="inquiry-whatsapp-action" class="btn btn-secondary" href="https://wa.me/60165262894" target="_blank" rel="noopener">{c['wa_action']}</a><button id="inquiry-copy-action" class="btn btn-secondary" type="button">{c['copy']}</button></div>
            </div>
          </form>'''


def main() -> None:
    for lang, copy in COPY.items():
        path = ROOT / lang / "contact.html"
        text = path.read_text(encoding="utf-8")
        text, form_count = re.subn(r'<form class="contact-form" id="contact-inquiry-form">.*?</form>', form_markup(copy), text, count=1, flags=re.S)
        if form_count != 1:
            raise RuntimeError(f"Contact form not found: {path}")
        if '../js/contact-inquiry.js' not in text:
            text, script_count = re.subn(r'\s*<script>\s*(?://[^\n]*\n\s*)?document\.getElementById\(\'contact-inquiry-form\'\).*?</script>', '\n  <script src="../js/contact-inquiry.js"></script>', text, count=1, flags=re.S)
            if script_count != 1:
                raise RuntimeError(f"Legacy mailto handler not found: {path}")
        text = re.sub(r'src="\.\./js/inquiry-context\.js(?:\?v=[^"]+)?"', 'src="../js/inquiry-context.js?v=20260715-2"', text)
        text = re.sub(r'src="\.\./js/contact-inquiry\.js(?:\?v=[^"]+)?"', 'src="../js/contact-inquiry.js?v=20260715-2"', text)
        info = CONTACT_INFO[lang]
        text = re.sub(r'(<div class="office-status" data-offset="8"></div>\s*</div>\s*)<p style="font-size:0\.9rem; margin-top:0\.5rem;">.*?</p>', rf'\1<p style="font-size:0.9rem; margin-top:0.5rem;">{info["hours"]}</p>', text, count=1, flags=re.S)
        text = re.sub(r'(<p style="font-size:1\.1rem; font-weight: 500; margin-top:0\.5rem;">)\s*WhatsApp.*?(</p>)', rf'\1\n              {info["whatsapp"]}\n            \2', text, count=1, flags=re.S)
        path.write_text(text, encoding="utf-8", newline="\n")
    print("Replaced three implicit mailto forms with explicit Email and WhatsApp enquiry preparation flows.")


if __name__ == "__main__":
    main()
