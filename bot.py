import os
import time
import urllib.parse
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- تشغيل سيرفر الويب المدمج لضمان بقاء الخدمة نشطة 24/7 على Render ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("✅ Bot AI Core is Active 24/7".encode("utf-8"))

    def log_message(self, format, *args):
        return

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# --- إعدادات وتوكن البوت ---
TELEGRAM_BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# قاعدة بيانات المعرفة المالية والتقنية الموسعة
CRYPTO_DATABASE = {
    "SUI": {
        "name": "سوي (Sui Network)",
        "solutions": (
            "• **معالجة المعاملات بالتوازي (Parallel Execution):** تنفيذ آلاف المعاملات في الثانية دون اختناق الشبكة.\n"
            "• **لغة البرمجة Sui Move:** لغة آمنة ومصممة خصيصاً لمنع ثغرات العقود الذكية والقرصنة.\n"
            "• **هندسة الكائنات (Object-Centric Model):** تجعل حفظ ونقل الأصول الرقمية والألعاب فورياً وبأقل رسوم غاز.\n"
            "• **zkLogin:** تمكين المستخدمين من تسجيل الدخول وإنشاء محافظ عبر Google أو Apple دون تعقيدات."
        ),
        "outlook": "مشروع قيادي في شبكات الجيل الجديد ومنافس مباشر لسولانا، ويحظى بنمو مستمر في السيولة المقفلة (TVL)."
    },
    "SOL": {
        "name": "سولانا (Solana)",
        "solutions": (
            "• **بروتوكول إثبات التاريخ (Proof of History):** تسريع توثيق الكتل ومعالجة تفوق 65,000 عملية في الثانية.\n"
            "• **رسوم شبه مجانية:** مثالية لتطبيقات الدفع اللامركزي وتداول العملات عالية التردد.\n"
            "• **المركز الأول للسيولة الشعبية:** استقطاب أكبر حجم تداول للميم كوينز وتطبيقات الـ DeFi."
        ),
        "outlook": "العمود الفقري لتداولات التجزئة والسيولة السريعة مع توجه مؤسسي واضح لإطلاق صناديق استثمارية خاصة بها."
    },
    "BTC": {
        "name": "البيتكوين (Bitcoin)",
        "solutions": (
            "• **الذهب الرقمي:** مخزن القيمة الأول المقاوم للتضخم والتدخلات المركزية.\n"
            "• **التبني المؤسسي:** أصل مالي معتمد في كبرى الصناديق الاستثمارية العالمية (ETFs).\n"
            "• **شبكة البرق (Lightning Network):** تسهيل المدفوعات الفورية والصغيرة عالمياً."
        ),
        "outlook": "يقود السوق المالي ككل ومؤشر رئيسي لتدفقات رؤوس الأموال العالمية."
    },
    "ETH": {
        "name": "الإيثيريوم (Ethereum)",
        "solutions": (
            "• **المنصة الأم للعقود الذكية:** أضخم بيئة أمان للتطبيقات اللامركزية والمؤسسات.\n"
            "• **حلول الطبقة الثانية (Layer 2s):** مثل Arbitrum و Base لخفض الرسوم وتسريع التحويلات.\n"
            "• **التمويل اللامركزي (DeFi):** يستحوذ على الحصة الكبرى من أصول وتطبيقات التمويل عالمياً."
        ),
        "outlook": "أساس البنية التحتية للاقتصاد المشفر مع استقرار استثماري طويل المدى."
    },
    "TON": {
        "name": "تون (Toncoin)",
        "solutions": (
            "• **الدمج المباشر مع تليجرام:** إتاحة الويب 3 ومحافظ الدفع لمئات الملايين من المستخدمين بضغطة زر.\n"
            "• **التطبيقات المصغرة (Mini Apps):** بيئة متكاملة للألعاب والخدمات المصرفية داخل الدردشة.\n"
            "• **معمارية لا متناهية للتوسع (Infinite Sharding):** قدرة معالجة هائلة تناسب التبني الجماعي."
        ),
        "outlook": "مشروع استثنائي في سهولة الوصول وجذب المستخدمين غير التقنيين إلى عالم التشفير."
    },
    "NEAR": {
        "name": "نير بروتوكول (NEAR)",
        "solutions": (
            "• **دمج الذكاء الاصطناعي اللامركزي (User-Owned AI):** تمكين النماذج الذكية من العمل بحرية على البلوكشين.\n"
            "• **تجريد السلسلة (Chain Abstraction):** تتيح للمستخدم التعامل مع كل الشبكات من حساب واحد بسهولة.\n"
            "• **تقنية Nightshade للتجزئة:** معالجة فائقة السرعة برسوم منعدمة."
        ),
        "outlook": "من أقوى المشاريع الصاعدة التي تجمع بين قوة البنية التحتية ومستقبل الذكاء الاصطناعي."
    }
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
        res = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10).json()
        if not res.get("ok"):
            payload.pop("parse_mode", None)
            requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

def get_main_keyboard():
    return {
        "keyboard": [
            [{"text": "🔥 أهم العملات والمشاريع الواعدة"}, {"text": "💼 صفقات التمويل والاستثمار"}],
            [{"text": "🌍 قراءة وتحليل الاقتصاد العام"}, {"text": "💡 تعليمات وكيفية البحث"}]
        ],
        "resize_keyboard": True
    }

def get_live_price(symbol):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol.upper()}-USDT"
        res = requests.get(url, timeout=5).json()
        if res.get("code") == "0" and len(res.get("data", [])) > 0:
            d = res["data"][0]
            price = float(d.get("last", 0))
            open_p = float(d.get("open24h", price))
            change = ((price - open_p) / open_p) * 100 if open_p > 0 else 0
            high = float(d.get("high24h", 0))
            low = float(d.get("low24h", 0))
            vol = float(d.get("volCcy24h", 0))
            return {"price": price, "change": change, "high": high, "low": low, "vol": vol}
    except Exception:
        pass
    return None

def query_online_ai(prompt):
    """استعلام مباشر وسريع عبر محرك الذكاء الاصطناعي الحر"""
    try:
        encoded = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded}?model=mistral"
        res = requests.get(url, timeout=12)
        if res.status_code == 200 and len(res.text.strip()) > 20:
            return res.text.strip()
    except Exception:
        pass
    return None

def analyze_user_query(text):
    clean = text.lower().strip()
    
    # التعرف على العملة المطلوبة
    matched_sym = None
    if "sui" in clean or "سوي" in clean:
        matched_sym = "SUI"
    elif "sol" in clean or "سولانا" in clean or "سول" in clean:
        matched_sym = "SOL"
    elif "btc" in clean or "بيتكوين" in clean or "بتكوين" in clean:
        matched_sym = "BTC"
    elif "eth" in clean or "ايثيريوم" in clean or "اثيريوم" in clean:
        matched_sym = "ETH"
    elif "ton" in clean or "تون" in clean:
        matched_sym = "TON"
    elif "near" in clean or "نير" in clean:
        matched_sym = "NEAR"
        
    # في حال كانت العملة موجودة في قاعدة المعرفة
    if matched_sym and matched_sym in CRYPTO_DATABASE:
        data = CRYPTO_DATABASE[matched_sym]
        ticker = get_live_price(matched_sym)
        
        msg = f"📊 *تقرير ودراسة شاملة: {data['name']}*\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n\n"
        
        if ticker:
            em = "🟢" if ticker['change'] >= 0 else "🔴"
            p_str = f"{ticker['price']:,.4f}$" if ticker['price'] < 1 else f"{ticker['price']:,.2f}$"
            msg += "💵 *الأرقام والسيولة اللحظية:*\n"
            msg += f"• *السعر الحالي:* `{p_str}` ({em} {ticker['change']:.2f}%)\n"
            msg += f"• *نطاق اليوم:* أدنى `{ticker['low']:,.2f}$` | أعلى `{ticker['high']:,.2f}$`\n"
            msg += f"• *حجم التداول اليومي:* `{ticker['vol']:,.0f}$`\n\n"
            
        msg += "💡 *أبرز الحلول التقنية والقيمة المضافة:*\n"
        msg += f"{data['solutions']}\n\n"
        msg += "🎯 *الرؤية والتقييم الاستثماري:*\n"
        msg += f"{data['outlook']}\n"
        msg += "━━━━━━━━━━━━━━━━━━━"
        return msg

    # في حال كان سؤالاً عاماً أو عملة أخرى، استدعاء الذكاء الاصطناعي
    ai_prompt = f"أجب باللغة العربية كخبير اقتصادي ومحلل كريبتو محترف دون روابط عن السؤال التالي: {text}"
    ai_response = query_online_ai(ai_prompt)
    
    if ai_response:
        return ai_response

    # تحليل افتراضي ذكي إذا تعذر الاتصال الخارجي
    return (
        f"🔍 *تحليل الاستفسار:*\n\n"
        f"• تم فحص طلبك بخصوص: `{text}`.\n"
        f"• **القراءة الفنية والاقتصادية:** يُنصح بالتركيز على المشاريع ذات القيمة الفعلية ومتابعة أحجام التداول والسيولة الداخلة وتجنب الدخول العشوائي عند القمم السعرية.\n\n"
        f"💡 *يمكنك كتابة اسم أي عملة محددة مثل (سوي، سولانا، بيتكوين، تون) للحصول على تقريرها الفوري.*"
    )

def get_market_overview():
    btc = get_live_price("BTC")
    eth = get_live_price("ETH")
    sol = get_live_price("SOL")
    
    btc_str = f"{btc['price']:,.2f}$" if btc else "مستقر"
    eth_str = f"{eth['price']:,.2f}$" if eth else "مستقر"
    sol_str = f"{sol['price']:,.2f}$" if sol else "مستقر"
    
    msg = "🌍 *تقرير حركة الاقتصاد والسيولة العامة للسوق*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "📊 *أداء المؤشرات والعملات القيادية:*\n"
    msg += f"• *البيتكوين (BTC):* `{btc_str}`\n"
    msg += f"• *الإيثيريوم (ETH):* `{eth_str}`\n"
    msg += f"• *سولانا (SOL):* `{sol_str}`\n\n"
    msg += "📈 *القراءة الاقتصادية للمرحلة:*\n"
    msg += "1. **تدوير السيولة:** تحركات إيجابية واستقرار يدعم صعود العملات البديلة القوية.\n"
    msg += "2. **توجه الصناديق:** تركيز السيولة الاستثمارية على قطاعات البنية التحتية والذكاء الاصطناعي اللامركزي.\n"
    msg += "3. **إدارة المخاطر:** الشراء من مناطق الدعم هو الاستراتيجية الأكثر أماناً.\n"
    msg += "━━━━━━━━━━━━━━━━━━━"
    return msg

def get_featured():
    msg = "🔥 *دليل أهم العملات والمشاريع ذات القوة الفعلية*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    for sym in ["SUI", "SOL", "NEAR", "TON"]:
        item = CRYPTO_DATABASE.get(sym)
        t = get_live_price(sym)
        p_str = f"`{t['price']:,.2f}$`" if t else ""
        msg += f"🔹 *{item['name']}* {p_str}\n"
        msg += f"• *التقييم:* {item['outlook']}\n"
        msg += "───────────────────\n"
    return msg

def get_deals():
    msg = "💼 *أحدث جولات الاستثمار والتمويل المؤسسي (Crypto VCs)*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "🏛 *1. قطاع الذكاء الاصطناعي والحوسبة الموزعة (AI & DePIN)*\n"
    msg += "• يستحوذ على أعلى حصة تمويل من كبرى الصناديق (أكثر من 200M$ في الربع الأخير).\n\n"
    msg += "⚡ *2. شبكات المعالجة المتوازية (Parallel Execution)*\n"
    msg += "• تركيز استثماري ضخم على تقنيات Move وشبكات السرعة الفائقة لخدمة الألعاب والتطبيقات المالية.\n\n"
    msg += "💡 *الفرصة:* متابعة الاكتتابات والمشاريع التي تجذب صناديق الفئة الأولى (Tier 1) قبل إدراجها الرسمي.\n"
    msg += "━━━━━━━━━━━━━━━━━━━"
    return msg

def main():
    print("🚀 البوت الذكي يعمل الآن 24/7 دون أي أخطاء...")
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
                            "👋 *أهلاً بك! أنا مستشارك وخبيرك الاقتصادي لأسواق الكريبتو.*\n\n"
                            "🤖 **كيف يمكنني خدمتك؟**\n"
                            "• اسألني عن **أي عملة أو مشروع أو حلول تقنية** (مثال: _ما هي حلول sui؟_ أو _شو توقعات عملة سوي؟_).\n"
                            "• أو اختر من **الأزرار السريعة بالأسفل** لجلب التقارير فوراً."
                        )
                        send_message(chat_id, welcome, get_main_keyboard())

                    elif text == "🔥 أهم العملات والمشاريع الواعدة":
                        send_message(chat_id, get_featured())

                    elif text == "💼 صفقات التمويل والاستثمار":
                        send_message(chat_id, get_deals())

                    elif text == "🌍 قراءة وتحليل الاقتصاد العام":
                        send_message(chat_id, get_market_overview())

                    elif text == "💡 تعليمات وكيفية البحث":
                        guide = (
                            "📌 *طريقة الاستخدام:*\n\n"
                            "1️⃣ اكتب أي سؤال تريده (مثال: `ما هي حلول sui` أو `توقعات سولانا` أو `سعر البيتكوين`).\n"
                            "2️⃣ استخدم الأزرار السفلية لجلب دراسات فورية عن السوق والصفقات."
                        )
                        send_message(chat_id, guide)

                    else:
                        reply = analyze_user_query(text)
                        send_message(chat_id, reply)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    main()
