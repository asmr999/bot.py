import requests
import json

# --- بياناتك ومفاتيحك الرسمية ---
CRYPTORANK_API_KEY = "497d41132b239b213d9bdbbc038b144248324792a76ca0647c1acb4063d3"
TELEGRAM_BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_CHAT_ID = "7926863163"

def send_telegram(text):
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
        print(f"Error sending to Telegram: {e}")
        return None

def fetch_and_notify():
    # نقطة النهاية المباشرة للعملات والمشاريع
    url = f"https://api.cryptorank.io/v1/currencies?api_key={CRYPTORANK_API_KEY}&limit=5"
    
    try:
        res = requests.get(url, timeout=15)
        print("API Status Code:", res.status_code)
        data = res.json()
        
        if "data" in data and len(data["data"]) > 0:
            msg = "🚨 *تقرير المشاريع والعملات المحدثة (CryptoRank)* 🚨\n\n"
            for item in data["data"][:5]:
                name = item.get("name", "غير معروف")
                symbol = item.get("symbol", "")
                
                values = item.get("values", {}).get("USD", {})
                price = values.get("price", 0)
                change24h = values.get("percentChange24h", 0)
                
                price_str = f"{price:,.4f}$" if price < 1 else f"{price:,.2f}$"
                emoji = "🟢" if change24h >= 0 else "🔴"
                
                msg += f"🔹 *الاسم:* `{name}` ({symbol})\n"
                msg += f"💵 *السعر:* `{price_str}`\n"
                msg += f"{emoji} *تغير 24س:* `{change24h:.2f}%`\n"
                msg += "-------------------------\n"
                
            send_res = send_telegram(msg)
            print("Telegram Send Result:", send_res)
            print("✅ تم إرسال التقرير لتليجرام بنجاح!")
        else:
            print("API Output:", json.dumps(data)[:200])
            send_telegram("⚠️ لا توجد بيانات جديدة من CryptoRank حالياً.")
            
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
        send_telegram(f"❌ خطأ أثناء التشغيل: {e}")

if __name__ == "__main__":
    fetch_and_notify()
