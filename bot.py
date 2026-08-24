import requests

# --- بياناتك المدمجة ---
CRYPTORANK_API_KEY = "497d41132b239b213d9bdbbc038b144248324792a76ca0647c1acb4063d3"
TELEGRAM_BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_CHAT_ID = "7926863163"

# نقطة النهاية المفتوحة والمدعومة بالكامل في الخطة المجانية
URL = f"https://api.cryptorank.io/v1/currencies?api_key={CRYPTORANK_API_KEY}&limit=5"

def send_telegram_message(text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(telegram_url, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        print(f"خطأ في إرسال تليجرام: {e}")
        return None

def fetch_and_notify():
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()
        
        # طباعة الاستجابة في سجلات Render للمراقبة
        print("API Status Code:", response.status_code)
        
        if "data" in data and len(data["data"]) > 0:
            message = "🚨 *تقرير المشاريع والعملات المحدثة (CryptoRank)* 🚨\n\n"
            
            for coin in data["data"]:
                name = coin.get("name", "غير معروف")
                symbol = coin.get("symbol", "")
                
                # استخراج السعر والتغير اليومي
                values = coin.get("values", {}).get("USD", {})
                price = values.get("price", 0)
                change24h = values.get("percentChange24h", 0)
                
                # تنسيق السعر
                if price >= 1:
                    price_str = f"{price:,.2f}$"
                else:
                    price_str = f"{price:.4f}$"
                    
                change_emoji = "🟢" if change24h >= 0 else "🔴"
                
                message += f"🔹 *العملة:* `{name}` ({symbol})\n"
                message += f"💵 *السعر:* `{price_str}`\n"
                message += f"{change_emoji} *تغير 24س:* `{change24h:.2f}%`\n"
                message += "-------------------------\n"
                
            send_telegram_message(message)
            print("✅ تم إرسال التقرير لتليجرام بنجاح!")
        else:
            print("⚠️ استجابة الـ API:", data)
            
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    fetch_and_notify()
