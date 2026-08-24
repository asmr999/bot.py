import requests
import time

# --- البيانات والمفاتيح الخاصة بك ---
CRYPTORANK_API_KEY = "497d41132b239b213d9bdbbc038b144248324792a76ca0647c1acb4063d3"
TELEGRAM_BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_CHAT_ID = "7926863163"

# رابط سحب أحدث جولات التمويل
URL = f"https://api.cryptorank.io/v1/funding-rounds?api_key={CRYPTORANK_API_KEY}&limit=5"

def send_telegram_message(text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(telegram_url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"خطأ في إرسال رسالة التليجرام: {e}")
        return None

def fetch_and_notify():
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            message = "🚨 *أحدث المشاريع وجولات التمويل (CryptoRank)* 🚨\n\n"
            
            for project in data["data"]:
                name = project.get("projectName", "غير معروف")
                raised = project.get("raised", "غير محدد")
                category = project.get("category", "عام")
                stage = project.get("stage", "Seed/IDO")
                
                # تنسيق قيمة التمويل
                raised_str = f"{raised:,.0f}" if isinstance(raised, (int, float)) else str(raised)
                
                message += f"🔹 *المشروع:* `{name}`\n"
                message += f"💰 *التمويل:* `{raised_str}$`\n"
                message += f"🏷 *التصنيف:* `{category}`\n"
                message += f"📌 *المرحلة:* `{stage}`\n"
                message += "-------------------------\n"
                
            send_telegram_message(message)
            print("✅ تم جلب البيانات وإرسال التقرير إلى تليجرام بنجاح!")
        else:
            print("⚠️ لا توجد بيانات جديدة متاحة.")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء سحب البيانات من CryptoRank: {e}")

if __name__ == "__main__":
    fetch_and_notify()
