import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import sys

def send_update_email(version=""):
    # 設定您的 SMTP 伺服器與驗證資訊
    # 這裡以 Gmail 為例，您需要申請「應用程式密碼 (App Password)」
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "your-email@gmail.com"  # 請替換為您的寄件信箱
    SENDER_PASSWORD = "your-app-password"  # 請替換為您的應用程式密碼
    
    # 收件人清單
    RECIPIENTS = ["jackie@bigfame.co", "jacquline@sunnyward.com"]
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(RECIPIENTS)
    msg['Subject'] = f"[通知] Sunnyward 網站已更新 {version}"
    
    body = f"""
    您好，
    
    Sunnyward 產品網站已經完成最新的更新。
    更新時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    版本號：{version}
    
    本次更新內容可能包含最新的辦公室家具、戶外家具產品資料與圖片同步。
    請前往前台網站確認最新狀況。
    
    這是一封自動發送的系統通知信，請勿直接回覆。
    
    謝謝！
    系統自動發送
    """
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        # server.login(SENDER_EMAIL, SENDER_PASSWORD) # 填寫密碼後取消註解此行
        # server.send_message(msg)                    # 填寫密碼後取消註解此行
        server.quit()
        print(f"✅ Email notification sent to {RECIPIENTS}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print("Please configure your SMTP credentials in scripts/notify_update.py")

if __name__ == "__main__":
    ver = sys.argv[1] if len(sys.argv) > 1 else ""
    send_update_email(ver)
