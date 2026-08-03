"""Render the localized B2B project-enquiry brief."""

from __future__ import annotations

import html


COPY = {
    "en": {
        "title": "Tell us what you need", "name": "Your name", "name_ph": "e.g. Sarah Jenkins",
        "company": "Company (optional)", "company_ph": "e.g. Studio North", "email": "Email",
        "email_ph": "e.g. sarah@interiors.com", "phone": "Phone (optional)", "phone_ph": "e.g. +65 9123 4567",
        "type": "Project type", "choose": "Select a project type", "types": ["Hotel / resort", "Restaurant / café", "Leisure / poolside", "Retail / commercial", "Residential development", "Other"],
        "market": "Delivery city / country", "market_ph": "e.g. Singapore", "quantity": "Estimated quantity (optional)", "quantity_ph": "e.g. 80 dining chairs",
        "timeline": "Target delivery timing (optional)", "timeline_ph": "e.g. October 2026", "subject": "Subject", "subject_ph": "e.g. Quote request for resort project",
        "message": "How can we help?", "message_ph": "Tell us briefly about the furniture or space you are planning.",
        "default_subject": "Website project enquiry", "submit": "Contact Sunnyward", "status": "Choose Email or WhatsApp to continue.",
        "email_action": "Continue with Email", "wa_action": "Continue with WhatsApp", "copy": "Copy draft",
    },
    "tw": {
        "title": "告訴我們您的需求", "name": "您的姓名", "name_ph": "例如：王小姐", "company": "公司（選填）", "company_ph": "例如：晴空設計",
        "email": "電子信箱", "email_ph": "例如：buyer@example.com", "phone": "電話（選填）", "phone_ph": "例如：+886 912 345 678",
        "type": "專案類型", "choose": "請選擇專案類型", "types": ["飯店／度假村", "餐廳／咖啡廳", "休閒／泳池空間", "零售／商業空間", "住宅開發案", "其他"],
        "market": "交貨城市／國家", "market_ph": "例如：台北，台灣", "quantity": "預估數量（選填）", "quantity_ph": "例如：80 張餐椅",
        "timeline": "目標交貨時程（選填）", "timeline_ph": "例如：2026 年 10 月", "subject": "主旨", "subject_ph": "例如：度假村專案報價需求",
        "message": "您想詢問什麼？", "message_ph": "簡單告訴我們正在規劃的家具或空間即可。",
        "default_subject": "網站專案詢問", "submit": "聯絡 Sunnyward", "status": "請選擇 Email 或 WhatsApp 繼續。",
        "email_action": "使用 Email 繼續", "wa_action": "使用 WhatsApp 繼續", "copy": "複製草稿",
    },
    "jp": {
        "title": "ご要望をお聞かせください", "name": "お名前", "name_ph": "例：山田 花子", "company": "会社名（任意）", "company_ph": "例：ABCデザイン",
        "email": "メールアドレス", "email_ph": "例：buyer@example.com", "phone": "電話番号（任意）", "phone_ph": "例：+81 90 1234 5678",
        "type": "プロジェクト種別", "choose": "プロジェクト種別を選択", "types": ["ホテル／リゾート", "レストラン／カフェ", "レジャー／プールサイド", "小売／商業施設", "住宅開発", "その他"],
        "market": "納品先の都市／国", "market_ph": "例：東京、日本", "quantity": "予定数量（任意）", "quantity_ph": "例：ダイニングチェア80脚",
        "timeline": "希望納期（任意）", "timeline_ph": "例：2026年10月", "subject": "件名", "subject_ph": "例：リゾート案件の見積依頼",
        "message": "お問い合わせ内容", "message_ph": "計画中の家具や空間について、簡単にお聞かせください。",
        "default_subject": "ウェブサイトからのプロジェクト相談", "submit": "Sunnywardへ連絡", "status": "Email または WhatsApp を選択してください。",
        "email_action": "Emailで続ける", "wa_action": "WhatsAppで続ける", "copy": "下書きをコピー",
    },
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def field(label: str, field_id: str, name: str, field_type: str, placeholder: str, required: bool = False, autocomplete: str = "") -> str:
    required_attr = " required" if required else ""
    autocomplete_attr = f' autocomplete="{autocomplete}"' if autocomplete else ""
    return f'<div class="form-group"><label for="{field_id}" class="form-label">{esc(label)}</label><input type="{field_type}" id="{field_id}" name="{name}" class="form-control" placeholder="{esc(placeholder)}"{autocomplete_attr}{required_attr}></div>'


def render_contact_form(lang: str) -> str:
    ui = COPY[lang]
    return f'''<form class="contact-form" id="contact-inquiry-form">
            <h3 style="margin-bottom: 1.5rem; font-size:1.8rem;">{esc(ui['title'])}</h3>
            {field(ui['name'], 'contact-name', 'name', 'text', ui['name_ph'], True, 'name')}
            {field(ui['company'], 'contact-company', 'company', 'text', ui['company_ph'], False, 'organization')}
            {field(ui['email'], 'contact-email', 'email', 'email', ui['email_ph'], True, 'email')}
            {field(ui['phone'], 'contact-phone', 'phone', 'tel', ui['phone_ph'], False, 'tel')}
            <input type="hidden" id="contact-subject" name="subject" value="{esc(ui['default_subject'])}">
            <div class="form-group"><label for="contact-message" class="form-label">{esc(ui['message'])}</label><textarea id="contact-message" name="message" class="form-control" placeholder="{esc(ui['message_ph'])}" required></textarea></div>
            <button type="submit" class="btn btn-primary" style="width:100%; padding:1rem;">{esc(ui['submit'])}</button>
            <div class="inquiry-actions" id="inquiry-actions" hidden aria-live="polite">
              <p id="inquiry-status">{esc(ui['status'])}</p>
              <div class="inquiry-actions__buttons"><a id="inquiry-email-action" class="btn btn-primary" href="mailto:sales@sunnyward.com">{esc(ui['email_action'])}</a><a id="inquiry-whatsapp-action" class="btn btn-secondary" href="https://wa.me/60165262894" target="_blank" rel="noopener">{esc(ui['wa_action'])}</a><button id="inquiry-copy-action" class="btn btn-secondary" type="button">{esc(ui['copy'])}</button></div>
            </div>
          </form>'''
