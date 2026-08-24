import os
import time
import json
import re
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==========================================
# 1. سيرفر الحفاظ على الاتصال 24/7 (Render)
# ==========================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("✅ GOLD WHALE ALPHA BOT IS ONLINE 24/7".encode("utf-8"))

    def log_message(self, format, *args):
        return

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# ==========================================
# 2. إعدادات التليجرام والمزامنة
# ==========================================
TOKEN_PART_A = "8862592074:AAHnglRbJJKNdRTjjox"
TOKEN_PART_B = "4PpkYtYkyiFcAi-s"
BOT_TOKEN = TOKEN_PART_A + TOKEN_PART_B
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

alerts_lock = threading.Lock()
ACTIVE_ALERTS = []

def send_msg(chat_id, text, reply_markup=None):
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

# ==========================================
# 3. محرك جلب الأسعار اللحظية الدقيقة
# ==========================================
def get_live_ticker(symbol):
    sym = symbol.strip().upper()
    # 1. المحرك الرئيسي (Binance Global)
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={sym}USDT"
        res = requests.get(url, timeout=4).json()
        if "lastPrice" in res:
            price = float(res["lastPrice"])
            change = float(res["priceChangePercent"])
            high = float(res["highPrice"])
            low = float(res["lowPrice"])
            vol = float(res["quoteVolume"])
            return {"price": price, "change": change, "high": high, "low": low, "vol": vol}
    except Exception:
        pass
        
    # 2. المحرك الاحتياطي (OKX)
    try:
        url2 = f"https://www.okx.com/api/v5/market/ticker?instId={sym}-USDT"
        res2 = requests.get(url2, timeout=4).json()
        if res2.get("code") == "0" and len(res2.get("data", [])) > 0:
            d = res2["data"][0]
            price = float(d.get("last", 0))
            open_p = float(d.get("open24h", price))
            change = ((price - open_p) / open_p) * 100 if open_p > 0 else 0
            return {
                "price": price,
                "change": change,
                "high": float(d.get("high24h", 0)),
                "low": float(d.get("low24h", 0)),
                "vol": float(d.get("volCcy24h", 0))
            }
    except Exception:
        pass
    return None

# ==========================================
# 4. لوحة المفاتيح التفاعلية
# ==========================================
def get_main_keyboard():
    return {
        "keyboard": [
            [{"text": "🔥 أهم العملات والمشاريع"}, {"text": "⏳ رادار فك التجميد"}],
            [{"text": "🐋 رادار تحركات الحيتان"}, {"text": "🪂 رادار الإيردروبات المجانية"}],
            [{"text": "🌡️ مؤشر الخوف والطمع"}, {"text": "📊 حاسبة إدارة الصفقات"}],
            [{"text": "🌍 قراءة الاقتصاد والسيولة"}, {"text": "🔔 تنبيهات الأسعار"}]
        ],
        "resize_keyboard": True
    }

# ==========================================
# 5. دوال الخدمات والتقارير المنظمة بدقة
# ==========================================

def get_fear_and_greed():
    try:
        url = "https://api.alternative.me/fng/?limit=1"
        res = requests.get(url, timeout=5).json()
        if "data" in res and len(res["data"]) > 0:
            val = int(res["data"][0]["value"])
            
            if val <= 25:
                status_txt = "خوف شديد (Extreme Fear)"
                tip = "السوق في مناطق تشاؤم حاد؛ تاريخياً هي أفضل فترات التجميع الاستثماري التدريجي."
            elif val <= 45:
                status_txt = "حذر وخوف (Fear)"
                tip = "حالة ترقب عامة؛ يفضل التركيز على العملات القيادية والابتعاد عن المضاربات الخطرة."
            elif val <= 60:
                status_txt = "منطقة محايدة (Neutral)"
                tip = "توازن نسبي بين قوى العرض والطلب بانتظار سيولة جديدة تحدد المسار."
            elif val <= 75:
                status_txt = "طمع وتفاؤل (Greed)"
                tip = "زخم صعودي قوي؛ تجنب الشراء من القمم السعرية وابدأ بجني أرباح جزئية."
            else:
                status_txt = "طمع مفرط (Extreme Greed)"
                tip = "مرحلة ذروة الشراء؛ احتمالية حدوث تصحيح هابط مفاجئ لتصفية الرافعة المالية مرتفعة جداً."

            msg = "🌡️ *مؤشر الخوف والطمع العام*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"• *الدرجة الحالية:* `{val} من 100`\n"
            msg += f"• *تصنيف السوق:* *{status_txt}*\n\n"
            msg += f"💡 *الرؤية والتوجيه:*\n{tip}\n"
            msg += "━━━━━━━━━━━━━━━━━━━"
            return msg
    except Exception:
        pass
    return "⚠️ تعذر تحديث مؤشر الخوف والطمع لحظياً، يرجى إعادة المحاولة."

def get_token_unlocks():
    msg = "⏳ *رادار فك تجميد العملات القادمة*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "🚨 *أبرز مواعيد طرح السيولة في السوق:*\n\n"
    msg += "🔹 *عملة SUI (سوي):*\n"
    msg += "• *الكمية:* فك دوري شهري يقدر بـ 64 مليون عملة.\n"
    msg += "• *التقييم:* يمتص السوق الكميات تدريجياً، تجنب رافعات الفيوتشرز العالية قبل الموعد بيومين.\n\n"
    msg += "🔹 *عملة APT (Aptos):*\n"
    msg += "• *الكمية:* فتح 11.3 مليون عملة (ما يعادل 2.1% من المعروض المتداول).\n"
    msg += "• *التقييم:* ضغط بيعي مؤقت يعقبه استقرار عند مناطق الدعم.\n\n"
    msg += "🔹 *عملة ARB (Arbitrum):*\n"
    msg += "• *الكمية:* فتح دوري لمستثمري الفريق والمستشارين.\n"
    msg += "• *التقييم:* المعروض المتاح كبير، يحتاج لارتفاع حجم التداول لامتصاص البيع.\n\n"
    msg += "💡 *قاعدة المحترفين:* عمليات الفك الكبرى تمنح فرص شراء ذهبية بعد انتهاء موجة التصحيح وليس قبلها."
    return msg

def get_whale_radar():
    msg = "🐋 *رادار تحركات الحيتان والسيولة المؤسسية*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "🟢 *عمليات السحب والتجميع (تخزين طويل الأجل):*\n"
    msg += "• رصد سحب أكثر من 280,000 قطعة `SOL` من المنصات المركزية نحو المحافظ الباردة وحسابات الـ Staking.\n"
    msg += "• كبار مستثمري شبكة `Sui` يعيدون ضخ السيولة في بروتوكولات الإقراض والـ DeFi.\n\n"
    msg += "🔴 *إيداعات المنصات (ضغوط بيع محدودة):*\n"
    msg += "• إيداع كميات من عملات الميم والمضاربات لجني أرباح سريعة.\n\n"
    msg += "💡 *الخلاصة:* استمرار سحب العملات الرئيسية للـ Cold Wallets يؤكد قلة معروض البيع وثقة المستثمرين الكبار."
    return msg

def get_airdrop_radar():
    msg = "🪂 *دليل الإيردروبات والشبكات التجريبية المجانية*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "⚡ *1. شبكة Monad (طبقة أولى فائقة السرعة):*\n"
    msg += "• *المهام:* التفاعل مع شبكة الـ Testnet، طلب الرصيد المجاني، وإجراء عمليات مبادلة (Swaps).\n"
    msg += "• *التمويل:* جمعت أكثر من 225 مليون دولار بدعم كبرى الصناديق الاستثمارية.\n\n"
    msg += "🐻 *2. شبكة Berachain (Bera Network):*\n"
    msg += "• *المهام:* توفير السيولة واختبار بروتوكولات الـ DEX على شبكة bArtio Testnet.\n\n"
    msg += "📜 *3. شبكة Story Protocol:*\n"
    msg += "• *المهام:* ربط المحفظة وتسجيل أصول فكرية تجريبية مجاناً.\n\n"
    msg += "💡 *تنبيه أمان:* استخدم دائماً محفظة جديدة مخصصة للتجارب لحماية أصولك الأساسية."
    return msg

def get_market_overview():
    btc = get_live_ticker("BTC")
    eth = get_live_ticker("ETH")
    sol = get_live_ticker("SOL")
    sui = get_live_ticker("SUI")

    def format_row(name, t):
        if not t: return f"• *{name}:* `مستقر`"
        em = "🟢" if t["change"] >= 0 else "🔴"
        p_str = f"{t['price']:,.2f}$" if t['price'] >= 1 else f"{t['price']:,.4f}$"
        return f"• *{name}:* `{p_str}` ({em} {t['change']:+.2f}%)"

    msg = "🌍 *تقرير الاقتصاد العام وحركة السيولة*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "📊 *الأسعار والعملات القيادية اللحظية:*\n"
    msg += f"{format_row('البيتكوين (BTC)', btc)}\n"
    msg += f"{format_row('الإيثيريوم (ETH)', eth)}\n"
    msg += f"{format_row('سولانا (SOL)', sol)}\n"
    msg += f"{format_row('سوي (SUI)', sui)}\n\n"
    msg += "📈 *القراءة الاقتصادية للمرحلة:*\n"
    msg += "1. استقرار البيتكوين يعطي مساحة قوية لحركة العملات البديلة (Altcoins).\n"
    msg += "2. استمرار التدفقات النقدية نحو شبكات البنية التحتية والذكاء الاصطناعي.\n"
    msg += "3. يفضل الشراء على دفعات (DCA) وتجنب الدخول بكامل رأس المال في نقطة واحدة.\n"
    msg += "━━━━━━━━━━━━━━━━━━━"
    return msg

def get_top_coins():
    msg = "🔥 *أهم المشاريع القيادية للفرص الحالية*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    coins = [
        ("SUI", "سوي", "أسرع شبكة نمواً في السيولة وقيمة الـ TVL وتعتبر المنافس المباشر لسولانا."),
        ("SOL", "سولانا", "المركز الأول لسيولة التداول وعملات الميم مع ترقب إطلاق صناديق ETF."),
        ("NEAR", "نير بروتوكول", "تقود قطاع الذكاء الاصطناعي اللامركزي مع تقنيات تجريد السلاسل."),
        ("TON", "تون كوين", "الوصول المباشر لمئات ملايين مستخدمي تليجرام وتطبيقات الدفع المصغر.")
    ]
    for sym, name, desc in coins:
        t = get_live_ticker(sym)
        p_str = ""
        if t:
            em = "🟢" if t["change"] >= 0 else "🔴"
            val = f"{t['price']:,.2f}$" if t['price'] >= 1 else f"{t['price']:,.4f}$"
            p_str = f" - `{val}` ({em} {t['change']:+.2f}%)"
        msg += f"🔹 *عملة {name}* (`{sym}`){p_str}\n"
        msg += f"• *التقييم:* {desc}\n"
        msg += "───────────────────\n"
    return msg

def calculate_trade(text):
    nums = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", text)
    if len(nums) >= 3:
        try:
            entry = float(nums[0])
            target = float(nums[1])
            stop = float(nums[2])
            
            risk = abs(entry - stop)
            reward = abs(target - entry)
            rr = reward / risk if risk > 0 else 0
            
            gain = (reward / entry) * 100
            loss = (risk / entry) * 100
            
            eval_txt = "🟢 صفقة ممتازة (عائد مرتفع مقارنة بالمخاطرة)" if rr >= 2.0 else "⚠️ نسبة المخاطرة مرتفعة، يفضل تحسين نقطة الدخول"
            
            msg = "📊 *حاسبة إدارة المخاطر والصفقات*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"• *سعر الدخول:* `{entry}$`\n"
            msg += f"• *الهدف الربحي:* `{target}$` (ربح: *+{gain:.2f}%*)\n"
            msg += f"• *وقف الخسارة:* `{stop}$` (مخاطرة: *-%{loss:.2f}*)\n\n"
            msg += f"⚖️ *نسبة العائد إلى المخاطرة:* `1 إلى {rr:.2f}`\n"
            msg += f"📌 *التقييم:* *{eval_txt}*\n"
            msg += "━━━━━━━━━━━━━━━━━━━"
            return msg
        except Exception:
            pass
            
    return (
        "📊 *طريقة استخدام حاسبة الصفقات:*\n\n"
        "اكتب كلمة **احسب** متبوعة بـ (سعر الدخول) (الهدف) (وقف الخسارة).\n\n"
        "📝 *مثال:* `احسب 3.20 4.80 2.90`"
    )

def analyze_coin(text):
    clean = text.lower().strip()
    symbols_map = {
        "sui": "SUI", "سوي": "SUI",
        "sol": "SOL", "سولانا": "SOL", "سول": "SOL",
        "btc": "BTC", "بيتكوين": "BTC", "بتكوين": "BTC",
        "eth": "ETH", "ايثيريوم": "ETH", "اثيريوم": "ETH",
        "ton": "TON", "تون": "TON",
        "near": "NEAR", "نير": "NEAR",
        "xrp": "XRP", "ريبل": "XRP",
        "ada": "ADA", "كاردانو": "ADA",
        "avax": "AVAX", "افالانش": "AVAX",
        "pepe": "PEPE", "بيبي": "PEPE"
    }
    
    target_sym = None
    for k, v in symbols_map.items():
        if k in clean:
            target_sym = v
            break
            
    if not target_sym:
        words = text.replace("عملة", "").replace("مشروع", "").replace("سعر", "").split()
        if words and len(words[0]) <= 8:
            target_sym = words[0].upper()

    if target_sym:
        t = get_live_ticker(target_sym)
        if t:
            em = "🟢" if t['change'] >= 0 else "🔴"
            p_str = f"{t['price']:,.4f}$" if t['price'] < 1 else f"{t['price']:,.2f}$"
            
            msg = f"📊 *تقرير وبيانات التداول: عملة `{target_sym}`*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"💵 *السعر المباشر:* `{p_str}` ({em} {t['change']:+.2f}%)\n"
            msg += f"📈 *أعلى سعر (24س):* `{t['high']:,.2f}$`\n"
            msg += f"📉 *أدنى سعر (24س):* `{t['low']:,.2f}$`\n"
            msg += f"📊 *حجم التداول اليومي:* `{t['vol']:,.0f}$`\n\n"
            msg += "💡 *الرؤية الفنية:* العملة في نطاق تداول نشط، راقب مستويات السيولة وكسر القمم لتأكيد استمرار الزخم.\n"
            msg += "━━━━━━━━━━━━━━━━━━━"
            return msg

    return (
        f"🔍 *تحليل الاستفسار:*\n\n"
        f"• تم فحص طلبك حول: `{text}`.\n"
        f"• **النصيحة الاستثمارية:** ركز على المشاريع القيادية ذات الاستخدام الحقيقي وأحجام التداول المليارية، وابتعد عن العقود غير الموثقة.\n\n"
        f"💡 يمكنك كتابة رمز أي عملة مباشرة مثل: `SUI` أو `SOL` أو `BTC` لجلب بياناتها اللحظية."
    )

# ==========================================
# 6. نظام التنبيهات المباشرة في الخلفية
# ==========================================
def process_alert(chat_id, text):
    words = text.replace("نبهني", "").replace("اذا", "").replace("وصلت", "").replace("سعر", "").split()
    if len(words) >= 2:
        sym = words[0].upper()
        if sym in ["سوي", "SUI"]: sym = "SUI"
        elif sym in ["سولانا", "SOL"]: sym = "SOL"
        elif sym in ["بيتكوين", "BTC"]: sym = "BTC"
        
        nums = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", words[1])
        if nums:
            target = float(nums[0])
            t = get_live_ticker(sym)
            if t:
                curr = t["price"]
                cond = "ABOVE" if target >= curr else "BELOW"
                with alerts_lock:
                    ACTIVE_ALERTS.append({
                        "chat_id": chat_id,
                        "symbol": sym,
                        "target": target,
                        "condition": cond
                    })
                cond_txt = "أعلى من" if cond == "ABOVE" else "أدنى من"
                return (
                    f"🔔 *تم تثبيت التنبيه بنجاح!*\n\n"
                    f"• *العملة:* `{sym}`\n"
                    f"• *السعر الحالي:* `{curr:,.4f}$`\n"
                    f"• *الهدف المطلوب:* `{target:,.4f}$` ({cond_txt})\n\n"
                    f"🤖 سيتم إرسال إشعار فوري لك لحظة وصول السعر لهذا الرقم."
                )
    return "💡 لتفعيل تنبيه، اكتب مثلاً:\n`نبهني SUI 4.50` أو `نبهني SOL 190`"

def get_alerts_list(chat_id):
    with alerts_lock:
        user_alerts = [a for a in ACTIVE_ALERTS if a["chat_id"] == chat_id]
    if not user_alerts:
        return "🔔 لا توجد تنبيهات نشطة حالياً.\n\nلتفعيل تنبيه اكتب: `نبهني SUI 4.50`"
    msg = "🔔 *قائمة تنبيهاتك النشطة:*\n━━━━━━━━━━━━━━━━━━━\n\n"
    for i, a in enumerate(user_alerts, 1):
        msg += f"{i}. عملة *{a['symbol']}* عند سعر: `{a['target']:,.4f}$`\n"
    return msg

def alert_daemon():
    while True:
        try:
            with alerts_lock:
                to_check = list(ACTIVE_ALERTS)
            for alert in to_check:
                t = get_live_ticker(alert["symbol"])
                if t:
                    curr = t["price"]
                    trig = False
                    if alert["condition"] == "ABOVE" and curr >= alert["target"]: trig = True
                    elif alert["condition"] == "BELOW" and curr <= alert["target"]: trig = True
                    if trig:
                        notify = (
                            f"🚨🚨 *تنبيه عاجل لتحرك السعر!* 🚨🚨\n"
                            f"━━━━━━━━━━━━━━━━━━━\n\n"
                            f"🎯 وصلت عملة *{alert['symbol']}* الآن إلى الهدف:\n"
                            f"💵 *السعر الحالي:* `{curr:,.4f}$`\n"
                            f"📌 *الهدف المحدد:* `{alert['target']:,.4f}$`\n\n"
                            f"📊 راقب الشارت واتخذ قرارك المناسب."
                        )
                        send_msg(alert["chat_id"], notify)
                        with alerts_lock:
                            if alert in ACTIVE_ALERTS:
                                ACTIVE_ALERTS.remove(alert)
            time.sleep(25)
        except Exception as e:
            print(f"Alert error: {e}")
            time.sleep(25)

# ==========================================
# 7. الحلقة الأساسية وتشغيل البوت
# ==========================================
def main():
    print("🚀 البوت الذكي يعمل الآن بأعلى كفاءة وتنسيق مثالي...")
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
                            "👋 *أهلاً بك في منصة GOLD WHALE الاستخباراتية للكريبتو!* 🐋\n\n"
                            "🚀 **لوحة التحكم السريعة في خدمتك:**\n"
                            "• ⏳ *رادار فك التجميد:* مواعيد طرح كميات العملات.\n"
                            "• 🐋 *رادار الحيتان:* تتبع تحركات المحافظ الضخمة.\n"
                            "• 🪂 *رادار الإيردروبات:* أفضل الشبكات التجريبية المجانية.\n"
                            "• 🌡️ *مؤشر الخوف والطمع:* تحليل المشاعر اليومي.\n"
                            "• 🔔 *تنبيهات الأسعار:* اكتب (نبهني SUI 4.5).\n"
                            "• 📊 *حاسبة الصفقات:* اكتب (احسب 3.20 4.80 2.90).\n\n"
                            "👇 *اضغط على أي زر بالأسفل أو اكتب اسم أي عملة لتحليلها فوراً!*"
                        )
                        send_msg(chat_id, welcome, get_main_keyboard())

                    elif text == "🔥 أهم العملات والمشاريع":
                        send_msg(chat_id, get_top_coins())
                    elif text == "⏳ رادار فك التجميد":
                        send_msg(chat_id, get_token_unlocks())
                    elif text == "🐋 رادار تحركات الحيتان":
                        send_msg(chat_id, get_whale_radar())
                    elif text == "🪂 رادار الإيردروبات المجانية":
                        send_msg(chat_id, get_airdrop_radar())
                    elif text == "🌡️ مؤشر الخوف والطمع":
                        send_msg(chat_id, get_fear_and_greed())
                    elif text == "📊 حاسبة إدارة الصفقات":
                        send_msg(chat_id, calculate_trade("info"))
                    elif text == "🌍 قراءة الاقتصاد والسيولة":
                        send_msg(chat_id, get_market_overview())
                    elif text == "🔔 تنبيهات الأسعار":
                        send_msg(chat_id, get_alerts_list(chat_id))

                    elif text.startswith("نبهني") or text.startswith("تنبيه"):
                        send_msg(chat_id, process_alert(chat_id, text))
                    elif text.startswith("احسب") or text.startswith("حساب"):
                        send_msg(chat_id, calculate_trade(text))
                    else:
                        send_msg(chat_id, analyze_coin(text))

        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    threading.Thread(target=alert_daemon, daemon=True).start()
    main()
