import requests
import time

# --- المفاتيح والبيانات المدمجة ---
CRYPTORANK_API_KEY = "497d41132b239b213d9bdbbc038b144248324792a76ca0647c1acb4063d3"
TELEGRAM_BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending msg: {e}")

def get_main_keyboard():
    return {
        "keyboard": [
            [{"text": "🚀 مشاريع وعملات جديدة"}, {"text": "💼 صفقات التمويل والاستثمار"}],
            [{"text": "🌍 تقرير نبض السوق والسيولة"}, {"text": "🔍 مساعدة وكيفية البحث"}]
        ],
        "resize_keyboard": True
    }

def get_new_projects():
    """تحليل العملات والمشاريع الجديدة وتقييماتها"""
    try:
        url = f"https://api.cryptorank.io/v1/currencies?api_key={CRYPTORANK_API_KEY}&limit=4&sort=-rank"
        res = requests.get(url, timeout=10).json()
        
        if "data" in res and len(res["data"]) > 0:
            msg = "🚀 *دليل المشاريع والعملات الحديثة في السوق*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            
            for item in res["data"][:4]:
                name = item.get("name", "مشروع جديد")
                symbol = item.get("symbol", "")
                category = item.get("category", "Web3 / DeFi")
                
                usd_data = item.get("values", {}).get("USD", {})
                price = usd_data.get("price", 0)
                mcap = usd_data.get("marketCap", 0)
                change = usd_data.get("percentChange24h", 0)
                
                price_str = f"{price:,.4f}$" if price < 1 else f"{price:,.2f}$"
                mcap_str = f"{mcap:,.0f}$" if mcap > 0 else "قيد الاحتساب (مبكر)"
                sentiment = "📈 مشروع صاعد بزخم" if change > 0 else "⚖️ في مرحلة تجميع وبناء سيولة"
                
                msg += f"🔹 *المشروع:* `{name}` (`{symbol}`)\n"
                msg += f"🏷 *القطاع:* {category}\n"
                msg += f"💵 *السعر الحالي:* `{price_str}`\n"
                msg += f"📊 *القيمة السوقية:* `{mcap_str}`\n"
                msg += f"🎯 *الرؤية والتقييم:* {sentiment}\n"
                msg += "───────────────────\n"
            return msg
        return "⚠️ لا توجد بيانات مشاريع محدثة حالياً."
    except Exception as e:
        return f"❌ تعذر جلب المشاريع: {e}"

def get_funding_deals():
    """تحليل صفقات التمويل ورؤوس الأموال الاستثمارية"""
    try:
        url = f"https://api.cryptorank.io/v1/funding-rounds?api_key={CRYPTORANK_API_KEY}&limit=4"
        res = requests.get(url, timeout=10).json()
        
        if "data" in res and len(res["data"]) > 0:
            msg = "💼 *أحدث جولات التمويل المؤسسي والمشاريع الصاعدة*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            
            for item in res["data"][:4]:
                name = item.get("projectName", "مشروع غير معلن")
                raised = item.get("raised", 0)
                stage = item.get("stage", "Seed Round")
                category = item.get("category", "Infrastructure")
                
                raised_str = f"{raised:,.0f}$" if isinstance(raised, (int, float)) and raised > 0 else "غير معلن"
                
                msg += f"🏛 *المشروع:* `{name}`\n"
                msg += f"💰 *حجم الاستثمار المجموع:* `{raised_str}`\n"
                msg += f"📌 *مرحلة الاستثمار:* {stage}\n"
                msg += f"🏷 *مجال المشروع:* {category}\n"
                msg += f"💡 *التحليل:* دعم قوي من صناديق الاستثمار، يُنصح بمتابعة اختبارات الشبكة (Testnet).\n"
                msg += "───────────────────\n"
            return msg
        return "⚠️ لا توجد صفقات تمويل مسجلة في الساعات الأخيرة."
    except Exception as e:
        return f"❌ تعذر جلب جولات التمويل: {e}"

def get_market_overview():
    """تقرير اقتصادي لحالة السوق والسيولة"""
    try:
        btc_res = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT", timeout=10).json()
        btc_price = float(btc_res.get("lastPrice", 0))
        btc_change = float(btc_res.get("priceChangePercent", 0))
        
        trend = "🟢 سيطرة شرائية ومؤشرات إيجابية" if btc_change >= 0 else "🔴 ضغوط بيعية وحذر في السيولة"
        
        msg = "🌍 *تقرير حركة الاقتصاد والسيولة العامة للسوق*\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n\n"
        msg += f"🪙 *مؤشر البيتكوين العام:* `{btc_price:,.2f}$` ({btc_change:.2f}%)\n"
        msg += f"📊 *اتجاه السيولة الإجمالي:* {trend}\n\n"
        msg += "🧠 *القراءة الاقتصادية للمرحلة:*\n"
        msg += "• ترقب وتدوير سيولة تدريجي بين المشاريع الكبرى وعملات البنية التحتية.\n"
        msg += "• زيادة في وتيرة تمويل مشاريع الذكاء الاصطناعي وشبكات الطبقة الأولى الجديدة.\n"
        msg += "• يُفضل التركيز على الاكتتابات ذات التقييم المنخفض وتجنب الشراء عند القمم السعرية.\n"
        return msg
    except Exception as e:
        return f"❌ تعذر تحليل السوق: {e}"

def search_coin(query):
    """البحث الفوري عن أي عملة يطلبها المستخدم"""
    symbol = query.upper().strip()
    try:
        res = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT", timeout=8).json()
        if "lastPrice" in res:
            price = float(res["lastPrice"])
            change = float(res["priceChangePercent"])
            high = float(res["highPrice"])
            low = float(res["lowPrice"])
            volume = float(res["quoteVolume"])
            
            emoji = "🟢" if change >= 0 else "🔴"
            price_str = f"{price:,.4f}$" if price < 1 else f"{price:,.2f}$"
            
            msg = f"🔍 *تقرير تحليلي للعملة:* `{symbol}`\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n"
            msg += f"💵 *السعر اللحظي:* `{price_str}` ({emoji} {change:.2f}%)\n"
            msg += f"📈 *أعلى سعر (24س):* `{high:,.2f}$`\n"
            msg += f"📉 *أدنى سعر (24س):* `{low:,.2f}$`\n"
            msg += f"📊 *حجم التداول اليومي:* `{volume:,.0f}$`\n\n"
            msg += "💡 *التقييم الفني:* تداول نشط، راقب مناطق الدعم والكسر قبل فتح الصفقات.\n"
            return msg
    except Exception:
        pass
    return f"⚠️ لم يتم العثور على بيانات مباشرة لعملة `{symbol}`. تأكد من كتابة رمز العملة بشكل صحيح (مثال: BTC, ETH, SUI, SOL)."

def main_loop():
    print("🚀 البوت يعمل الآن ويستمع لجميع رسائلك في تليجرام...")
    offset = 0
    while True:
        try:
            updates = requests.get(f"{TELEGRAM_API}/getUpdates?offset={offset}&timeout=30", timeout=35).json()
            if "result" in updates:
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "").strip()
                    
                    if not chat_id or not text:
                        continue
                    
                    if text in ["/start", "بدء", "قائمة"]:
                        welcome = (
                            "👋 *أهلاً بك! أنا مساعدك الذكي لتحليل الأسواق والعملات.*\n\n"
                            "اختر من الأزرار بالأسفل، أو **اكتب اسم أي عملة مباشرة** (مثل BTC, SOL, SUI) لأقوم بتحليلها لك فوراً دون روابط."
                        )
                        send_message(chat_id, welcome, get_main_keyboard())
                        
                    elif text == "🚀 مشاريع وعملات جديدة":
                        send_message(chat_id, get_new_projects())
                        
                    elif text == "💼 صفقات التمويل والاستثمار":
                        send_message(chat_id, get_funding_deals())
                        
                    elif text == "🌍 تقرير نبض السوق والسيولة":
                        send_message(chat_id, get_market_overview())
                        
                    elif text == "🔍 مساعدة وكيفية البحث":
                        help_msg = (
                            "📌 *طريقة الاستخدام:*\n\n"
                            "1️⃣ اضغط على الأزرار السريعة لجلب تقارير فورية عن المشاريع والصفقات والسيولة.\n"
                            "2️⃣ اكتب رمز أي عملة تريد تحليلها مباشرة في المحادثة (مثال: `ETH` أو `SOL` أو `NEAR`)."
                        )
                        send_message(chat_id, help_msg)
                        
                    else:
                        send_message(chat_id, search_coin(text))
                        
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main_loop()
