import os
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- تشغيل سيرفر وهمي لتجاوز فحص Port في Render مجاناً ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("✅ Bot is active and running 24/7!".encode("utf-8"))

    def log_message(self, format, *args):
        return  # كتم سجلات فحص السيرفر للحفاظ على نظافة الـ Logs

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# --- إعدادات ومفاتيح البوت ---
CRYPTORANK_API_KEY = "497d41132b239b213d9bdbbc038b144248324792a76ca0647c1acb4063d3"
TELEGRAM_BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# قاموس ترجمة أسماء العملات بالعربي
ARABIC_COINS = {
    "سولانا": "SOL", "سول": "SOL", "solana": "SOL",
    "سوي": "SUI", "sui": "SUI",
    "بيتكوين": "BTC", "بتكوين": "BTC", "bitcoin": "BTC",
    "ايثيريوم": "ETH", "اثيريوم": "ETH", "ethereum": "ETH",
    "ريبل": "XRP", "ripple": "XRP",
    "تون": "TON", "ton": "TON",
    "نير": "NEAR", "near": "NEAR",
    "افالانش": "AVAX", "avax": "AVAX",
    "كاردانو": "ADA", "ada": "ADA",
    "دوج": "DOGE", "دوجكوين": "DOGE", "doge": "DOGE",
    "بينانس": "BNB", "bnb": "BNB",
    "بيبي": "PEPE", "pepe": "PEPE",
    "شيبا": "SHIB", "shib": "SHIB",
    "لينك": "LINK", "link": "LINK",
    "ابتوس": "APT", "aptos": "APT",
    "كاسبا": "KAS", "kaspa": "KAS",
    "فيتش": "FET", "fet": "FET",
    "رندر": "RENDER", "rndr": "RENDER"
}

# نبذة تحليلية لمشاريع العملات
PROJECT_INFO = {
    "SOL": {"name": "سولانا (Solana)", "desc": "شبكة طبقة أولى فائقة السرعة ومنخفضة الرسوم، تُعد المركز الأول لسيولة التداول وعملات الميم والـ DeFi.", "outlook": "مشروع قيادي مرشح لمواصلة جذب السيولة وتوسيع الشراكات المؤسسية."},
    "SUI": {"name": "سوي (Sui Network)", "desc": "شبكة طبقة أولى مبنية بلغة Move المطورة في ميتا سابقاً، وتتميز بمعالجة المعاملات الفورية وألعاب الويب 3.", "outlook": "من أسرع الشبكات نمواً في السيولة المقفلة (TVL) ولديها زخم قوي للمنافسة."},
    "BTC": {"name": "البيتكوين (Bitcoin)", "desc": "الذهب الرقمي والعملة الأساسية لسوق الكريبتو ككل ومخزن القيمة الأول للمؤسسات وصناديق الـ ETF.", "outlook": "يقود اتجاه السوق العام مع استمرار دخول السيولة الاستثمارية طويلة الأجل."},
    "ETH": {"name": "الإيثيريوم (Ethereum)", "desc": "العمود الفقري للعقود الذكية والتمويل اللامركزي (DeFi) وأكبر شبكة من حيث الأمان وتطبيقات المؤسسات.", "outlook": "يبقى الركيزة الأساسية للسوق مع توسع حلول الطبقة الثانية لخفض الرسوم."},
    "TON": {"name": "تون (Toncoin)", "desc": "شبكة البلوكشين المرتبطة بتطبيق تليجرام، وتتيح الدفع وتطبيقات الويب 3 لمئات ملايين المستخدمين مباشرة.", "outlook": "تعتمد قوتها على تبني قاعدة مستخدمي تليجرام الضخمة وإطلاق الألعاب المصغرة."},
    "NEAR": {"name": "نير (NEAR Protocol)", "desc": "شبكة تدمج حلول التجزئة (Sharding) مع التركيز الكامل على بنية الذكاء الاصطناعي (AI) وسهولة الاستخدام.", "outlook": "مشروع رائد يجمع بين البنية التحتية القوية وسردية الذكاء الاصطناعي الصاعدة."}
}

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
        print(f"Send error: {e}")

def get_main_keyboard():
    return {
        "keyboard": [
            [{"text": "🔥 أهم العملات الواعدة"}, {"text": "💼 صفقات واستثمارات الكريبتو"}],
            [{"text": "🌍 نبض السوق والسيولة العامة"}, {"text": "💡 تعليمات وكيفية البحث"}]
        ],
        "resize_keyboard": True
    }

def get_live_ticker(symbol):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT"
        res = requests.get(url, timeout=6).json()
        if res.get("code") == "0" and len(res.get("data", [])) > 0:
            d = res["data"][0]
            price = float(d.get("last", 0))
            open_p = float(d.get("open24h", price))
            change = ((price - open_p) / open_p) * 100 if open_p > 0 else 0
            high = float(d.get("high24h", 0))
            low = float(d.get("low24h", 0))
            vol = float(d.get("volCcy24h", 0))
            return {"price": price, "change": change, "high": high, "low": low, "vol": vol}
    except Exception as e:
        print(f"Ticker error: {e}")
    return None

def analyze_coin(user_input):
    clean_input = user_input.strip().lower()
    symbol = ARABIC_COINS.get(clean_input, clean_input.upper())
    
    ticker = get_live_ticker(symbol)
    if not ticker:
        return f"⚠️ لم يتم العثور على بيانات لعملة `{user_input}`.\n\nجرّب كتابة رمز العملة مثل: `SOL`, `SUI`, `BTC`, `ETH` أو اسمها بالعربي مثل: `سولانا` أو `سوي`."
    
    info = PROJECT_INFO.get(symbol, {
        "name": f"مشروع {symbol}",
        "desc": "مشروع رقمي مدرج للتداول الفوري في الأسواق المركزية واللامركزية.",
        "outlook": "يخضع لحركة السيولة العامة؛ التداول الفني مرتبط باختراق مناطق الدعم والمقاومة."
    })
    
    emoji = "🟢" if ticker["change"] >= 0 else "🔴"
    price_fmt = f"{ticker['price']:,.4f}$" if ticker['price'] < 1 else f"{ticker['price']:,.2f}$"
    
    msg = f"📊 *تقرير تحليلي شامل: {info['name']}*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "📌 *نبذة عن المشروع وطبيعته:*\n"
    msg += f"{info['desc']}\n\n"
    msg += "💵 *الأرقام والسيولة اللحظية:*\n"
    msg += f"• *السعر الحالي:* `{price_fmt}` ({emoji} {ticker['change']:.2f}%)\n"
    msg += f"• *أعلى سعر (24 ساعة):* `{ticker['high']:,.2f}$`\n"
    msg += f"• *أدنى سعر (24 ساعة):* `{ticker['low']:,.2f}$`\n"
    msg += f"• *حجم التداول اليومي:* `{ticker['vol']:,.0f}$`\n\n"
    msg += "🎯 *الرؤية والتقييم الاستثماري:*\n"
    msg += f"{info['outlook']}\n"
    msg += "━━━━━━━━━━━━━━━━━━━"
    return msg

def get_market_pulse():
    btc = get_live_ticker("BTC")
    eth = get_live_ticker("ETH")
    sol = get_live_ticker("SOL")
    
    if not btc:
        return "⚠️ جاري تحديث بيانات السوق..."
    
    btc_emoji = "🟢" if btc["change"] >= 0 else "🔴"
    eth_emoji = "🟢" if eth["change"] >= 0 else "🔴"
    sol_emoji = "🟢" if sol["change"] >= 0 else "🔴"
    
    trend = "نشاط شرائي وتدفق إيجابي للسيولة" if btc["change"] >= 0 else "حذر وتجميع مع ضغوط بيعية مؤقتة"
    
    msg = "🌍 *تقرير نبض الاقتصاد وحركة السيولة العالمية*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "📊 *أداء المؤشرات والعملات القيادية:*\n"
    msg += f"• *البيتكوين (BTC):* `{btc['price']:,.2f}$` ({btc_emoji} {btc['change']:.2f}%)\n"
    msg += f"• *الإيثيريوم (ETH):* `{eth['price']:,.2f}$` ({eth_emoji} {eth['change']:.2f}%)\n"
    msg += f"• *سولانا (SOL):* `{sol['price']:,.2f}$` ({sol_emoji} {sol['change']:.2f}%)\n\n"
    msg += f"📈 *الاتجاه العام للسوق:* {trend}\n\n"
    msg += "🧠 *القراءة الاقتصادية للمرحلة:*\n"
    msg += "1. استقرار حركة البيتكوين يمنح العملات البديلة (Altcoins) مساحة لتحقيق صعود سريع.\n"
    msg += "2. تركيز رؤوس الأموال على شبكات الطبقة الأولى السريعة ومشاريع الذكاء الاصطناعي.\n"
    msg += "3. يُنصح بإدارة المخاطر والاعتماد على الشراء في مناطق الدعم بدلاً من ملاحقة الشموع الخضراء.\n"
    msg += "━━━━━━━━━━━━━━━━━━━"
    return msg

def get_featured_projects():
    msg = "🔥 *دليل أهم العملات والمشاريع ذات الزخم العالي*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    
    coins_to_show = ["SUI", "SOL", "NEAR", "TON"]
    for sym in coins_to_show:
        t = get_live_ticker(sym)
        p_info = PROJECT_INFO.get(sym, {})
        if t:
            em = "🟢" if t["change"] >= 0 else "🔴"
            p_str = f"{t['price']:,.4f}$" if t['price'] < 1 else f"{t['price']:,.2f}$"
            msg += f"🔹 *{p_info.get('name', sym)}* (`{sym}`)\n"
            msg += f"💵 *السعر:* `{p_str}` ({em} {t['change']:.2f}%)\n"
            msg += f"📝 *طبيعة المشروع:* {p_info.get('desc', '')}\n"
            msg += f"🎯 *التوقع:* {p_info.get('outlook', '')}\n"
            msg += "───────────────────\n"
    return msg

def get_investments():
    msg = "💼 *أحدث جولات الاستثمار والتمويل المؤسسي في الكريبتو*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "🏛 *1. مشاريع الذكاء الاصطناعي اللامركزي (Decentralized AI)*\n"
    msg += "• *التركيز:* جذب جولات تمويل تفوق 50 مليون دولار لبناء بنية تحتية ومعالجات موزعة.\n"
    msg += "• *التقييم:* قطاع واعد يحظى بأكبر زخم استثماري.\n\n"
    msg += "⚡ *2. شبكات الطبقة الأولى التفرعية (Parallel EVM & Move)*\n"
    msg += "• *التركيز:* استثمار صناديق رأس المال في تسريع المعاملات الفورية (مثل Monad و Sui).\n"
    msg += "• *التقييم:* مشاريع مرشحة لتصدر تدفقات السيولة القادمة.\n\n"
    msg += "💡 *توجيه استثماري:* تتبع المشاريع المدعومة من صناديق الفئة الأولى وشارك في شبكاتها التجريبية (Testnets).\n"
    msg += "━━━━━━━━━━━━━━━━━━━"
    return msg

def main():
    print("🚀 البوت يعمل الآن ويستمع لكافة رسائلك في تليجرام 24/7...")
    offset = 0
    while True:
        try:
            res = requests.get(f"{TELEGRAM_API}/getUpdates?offset={offset}&timeout=25", timeout=30).json()
            if "result" in res:
                for update in res["result"]:
                    offset = update["update_id"] + 1
                    msg = update.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    text = msg.get("text", "").strip()
                    
                    if not chat_id or not text:
                        continue
                    
                    if text in ["/start", "بدء", "قائمة"]:
                        welcome = (
                            "👋 *أهلاً بك في منصتك التحليلية للعملات الرقمية!*\n\n"
                            "اختر من القائمة بالأسفل، أو **اكتب اسم أي عملة بالعربي أو الإنجليزي** (مثل: `سولانا`، `سوي`، `BTC`، `ETH`) وسأعطيك تحليلاً فورياً شاملاً."
                        )
                        send_message(chat_id, welcome, get_main_keyboard())
                        
                    elif text == "🔥 أهم العملات الواعدة":
                        send_message(chat_id, get_featured_projects())
                        
                    elif text == "🌍 نبض السوق والسيولة العامة":
                        send_message(chat_id, get_market_pulse())
                        
                    elif text == "💼 صفقات واستثمارات الكريبتو":
                        send_message(chat_id, get_investments())
                        
                    elif text == "💡 تعليمات وكيفية البحث":
                        guide = (
                            "📌 *كيف تستخدم البوت؟*\n\n"
                            "1️⃣ اضغط على الأزرار السريعة لجلب حالة السوق، المشاريع، أو التمويلات.\n"
                            "2️⃣ اكتب اسم أي عملة مباشرة (مثال: `سوي`، `سولانا`، `BTC`، `NEAR`، `TON`) وستحصل على السعر اللحظي، نبذة المشروع، وتحليل فني وتوقعات."
                        )
                        send_message(chat_id, guide)
                        
                    else:
                        send_message(chat_id, analyze_coin(text))
                        
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في مسار فرعي ليرى Render أن المنفذ مفتوح
    threading.Thread(target=start_health_server, daemon=True).start()
    main()
