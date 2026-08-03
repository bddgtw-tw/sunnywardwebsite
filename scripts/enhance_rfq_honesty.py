import os

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

def enhance_rfq():
    # 1. TW
    tw_path = os.path.join(repo_dir, "tw", "products.html")
    with open(tw_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_success_tw = """      <!-- SUCCESS STATE -->
      <div id="rfq-success-container" >
        <div class="rfq-success-icon">✓</div>
        <h4 class="rfq-success-title">詢價單已成功送出</h4>
        <p class="rfq-success-msg">
          感謝您的來信！我們已收到您的詢價需求，團隊專員將於 24 小時內與您聯絡。<br>
          <span class="rfq-success-note">（同時已為您複製詢價內容至剪貼簿，以便您存檔留存。）</span>
        </p>
        <button class="btn btn-primary" onclick="closeRfqModal()" >關閉</button>
      </div>"""
      
    new_success_tw = """      <!-- SUCCESS STATE -->
      <div id="rfq-success-container" >
        <div class="rfq-success-icon">✓</div>
        <h4 class="rfq-success-title">詢價內容已複製到剪貼簿</h4>
        <p class="rfq-success-msg">
          您的詢價草稿已成功複製！請點擊下方按鈕開啟 Email 信件，直接貼上（或使用 Ctrl+V）並發送至 **sales@sunnyward.com**，我們將於 24 小時內為您回信。
        </p>
        <a id="rfq-email-link" href="#" class="btn btn-primary" onclick="closeRfqModal()">開啟 Email 發送</a>
      </div>"""
      
    content = content.replace(old_success_tw, new_success_tw)
    
    # 2. EN
    en_path = os.path.join(repo_dir, "en", "products.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        content_en = f.read()
        
    old_success_en = """      <!-- SUCCESS STATE -->
      <div id="rfq-success-container" >
        <div class="rfq-success-icon">✓</div>
        <h4 class="rfq-success-title">Inquiry Sent Successfully</h4>
        <p class="rfq-success-msg">
          Thank you! We have received your inquiry. Our team will get back to you within 24 hours.<br>
          <span class="rfq-success-note">(A copy of the inquiry has also been copied to your clipboard.)</span>
        </p>
        <button class="btn btn-primary" onclick="closeRfqModal()" >Close</button>
      </div>"""
      
    new_success_en = """      <!-- SUCCESS STATE -->
      <div id="rfq-success-container" >
        <div class="rfq-success-icon">✓</div>
        <h4 class="rfq-success-title">Inquiry Copied to Clipboard</h4>
        <p class="rfq-success-msg">
          Your inquiry draft has been successfully copied! Please click the button below to open your email client, paste it (Ctrl+V), and send it to **sales@sunnyward.com**. We will get back to you within 24 hours.
        </p>
        <a id="rfq-email-link" href="#" class="btn btn-primary" onclick="closeRfqModal()">Open Email & Send</a>
      </div>"""
      
    content_en = content_en.replace(old_success_en, new_success_en)
    
    # 3. JP
    jp_path = os.path.join(repo_dir, "jp", "products.html")
    with open(jp_path, 'r', encoding='utf-8') as f:
        content_jp = f.read()
        
    old_success_jp = """      <!-- SUCCESS STATE -->
      <div id="rfq-success-container" >
        <div class="rfq-success-icon">✓</div>
        <h4 class="rfq-success-title">お問い合わせが送信されました</h4>
        <p class="rfq-success-msg">
          お問い合わせいただきありがとうございます。内容を確認の上、24時間以内に担当者よりご連絡いたします。<br>
          <span class="rfq-success-note">（お問い合わせ内容はお手元での保管用として、クリップボードにもコピーされました。）</span>
        </p>
        <button class="btn btn-primary" onclick="closeRfqModal()" >閉じる</button>
      </div>"""
      
    new_success_jp = """      <!-- SUCCESS STATE -->
      <div id="rfq-success-container" >
        <div class="rfq-success-icon">✓</div>
        <h4 class="rfq-success-title">見積もり内容をクリップボードにコピーしました</h4>
        <p class="rfq-success-msg">
          お見積りの下書きが正常にコピーされました！以下のボタンをクリックしてメールクライアントを開き、貼り付け（Ctrl+V）して **sales@sunnyward.com** 宛てに送信してください。24時間以内にご返信いたします。
        </p>
        <a id="rfq-email-link" href="#" class="btn btn-primary" onclick="closeRfqModal()">メールを開いて送信</a>
      </div>"""
      
    content_jp = content_jp.replace(old_success_jp, new_success_jp)
    
    # Form submission JS logic replacement for all three
    old_js = """        navigator.clipboard.writeText(clipboardText).then(() => {
          console.log('Inquiry copied to clipboard');
        }).catch(err => {
          console.error('Failed to copy text: ', err);
        });
        
        document.getElementById('rfq-form-container').style.display = 'none';
        document.getElementById('rfq-success-container').style.display = 'block';"""
        
    new_js = """        navigator.clipboard.writeText(clipboardText).then(() => {
          console.log('Inquiry copied to clipboard');
        }).catch(err => {
          console.error('Failed to copy text: ', err);
        });
        
        // Generate mailto link
        const mailtoUrl = `mailto:sales@sunnyward.com?subject=Sunnyward%20Inquiry%20-%20${encodeURIComponent(sku)}&body=${encodeURIComponent(clipboardText)}`;
        const emailLink = document.getElementById('rfq-email-link');
        if (emailLink) {
          emailLink.setAttribute('href', mailtoUrl);
        }
        
        document.getElementById('rfq-form-container').style.display = 'none';
        document.getElementById('rfq-success-container').style.display = 'block';
        
        // Automatically open the mail client after 1.5 seconds
        setTimeout(() => {
          window.location.href = mailtoUrl;
        }, 1500);"""
        
    content = content.replace(old_js, new_js)
    content_en = content_en.replace(old_js, new_js)
    content_jp = content_jp.replace(old_js, new_js)
    
    with open(tw_path, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(content_en)
    with open(jp_path, 'w', encoding='utf-8') as f:
        f.write(content_jp)
        
    print("Successfully enhanced RFQ form copy/mailto honesty across all files.")

if __name__ == "__main__":
    enhance_rfq()
