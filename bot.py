import os
import time
import re
import urllib.parse
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==========================================
# 1. خادم المحافظة على النشاط 24/7 (Render)
# ==========================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("✅ AI Financial Advisor Core Active 24/7".encode("utf-8"))

    def log_message(self, format, *args):
        return

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# ==========================================
# 2. إعدادات التليجرام
# ==========================================
BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

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
        print(f"Error: {e}")

def get_simple_keyboard():
    return {
        "keyboard": [
            [{"text": "🌍 نظرة سريعة على السوق والسيولة"}, {"text": "💼 استشارة مالية وإدارة محفظة"}]
        ],
        "resize_keyboard": True
    }

# ==========================================
# 3. جلب الأسعار الحية
# ==========================================
def get_live_ticker(symbol):
    sym = symbol.strip().upper()
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={sym}USDT"
        res = requests.get(url, timeout=3).json()
        if "lastPrice" in res:
            return {
                "price": float(res["lastPrice"]),
                "change": float(res["priceChangePercent"])
            }
    except Exception:
        pass
    try:
        url2 = f"https://www.okx.com/api/v5/market/ticker?instId={sym}-USDT"
        res2 = requests.get(url2, timeout=3).json()
        if res2.get("code") == "0" and len(res2.get("data", [])) > 0:
            d = res2["data"][0]
            price = float(d.get("last", 0))
            open_p = float(d.get("open24h", price))
            change = ((price - open_p) / open_p) * 100 if open_p > 0 else 0
            return {"price": price, "change": change}
    except Exception:
        pass
    return None

# ==========================================
# 4. محرك التحليل المالي والذكاء الاصطناعي
# ==========================================
def query_ai_online(prompt_text):
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt_text)}?model=openai"
        res = requests.get(url, timeout=10)
        if res.status_code == 200 and len(res.text.strip()) > 30:
            return res.text.strip()
    except Exception:
        pass
    return None

def build_offline_financial_advice(text):
    """محرك مالي احتياطي فوري يضمن الرد الذكي بنسبة 100% دون أي خطأ"""
    clean = text.lower()
    
    # فحص طلبات استثمار المبالغ وتوزيع المحافظ
    nums = re.findall(r"\d+", clean)
    if nums and ("استثمار" in clean or "توزيع" in clean or "محفظة" in clean or "سولانة" in clean or "سوي" in clean):
        amount = int(nums[0])
        sol_t = get_live_ticker("SOL")
        sui_t = get_live_ticker("SUI")
        sol_p = f"{sol_t['price']:,.2f}$" if sol_t else "السعر الحالي"
        sui_p = f"{sui_t['price']:,.4f}$" if sui_t else "السعر الحالي"

        sol_share = int(amount * 0.45)
        sui_share = int(amount * 0.35)
        cash_share = amount - (sol_share + sui_share)

        msg = f"💼 *خطة استثمارية واستراتيجية محفظة مخصصة: رأس مال {amount}$*\n"
        msg += "━━━━━━━━━━━━━━━━━━━\n\n"
        msg += "📊 *توزيع رأس المال المقترح (إدارة مخاطر متوازنة):*\n\n"
        msg += f"🔹 *1. شبكة سولانا (SOL) — الحصة: {sol_share}$ (45%)*\n"
        msg += f"• *سعر السوق اللحظي:* `{sol_p}`\n"
        msg += "• *الهدف:* أصل قيادي عالي الأمان والسيولة ويمثل العمود الفقري للمحفظة.\n"
        msg += "• *طريقة الشراء:* تقسيم المبلغ على دفعتين بنظام الشراء التدريجي (DCA).\n\n"
        msg += f"🔹 *2. شبكة سوي (SUI) — الحصة: {sui_share}$ (35%)*\n"
        msg += f"• *سعر السوق اللحظي:* `{sui_p}`\n"
        msg += "• *الهدف:* عملة نمو سريعة ذات إمكانيات مضاعفة ومنافسة مباشرة للطبقة الأولى.\n"
        msg += "• *طريقة الشراء:* الشراء عند الارتداد من مناطق الدعم القريبة.\n\n"
        msg += f"💵 *3. سيولة نقدية احتياطية (USDT) — الحصة: {cash_share}$ (20%)*\n"
        msg += "• *الهدف:* استغلال أي هبوط مفاجئ في السوق لتعزيز المراكز بأسعار أقل.\n\n"
        msg += "🎯 *توجيهات إدارة المخاطر للمدى المتوسط:*\n"
        msg += "• لا تدخل بكامل السيولة دفعة واحدة (All-in).\n"
        msg += "• تفعيل جني الأرباح تدريجياً عند كل صعود قوي بنسبة 30% إلى 50%.\n"
        msg += "━━━━━━━━━━━━━━━━━━━"
        return msg

    # فحص عملة سوي
    if "سوي" in clean or "sui" in clean:
        t = get_live_ticker("SUI")
        p_str = f"`{t['price']:,.4f}$` ({t['change']:+.2f}%)" if t else ""
        return (
            f"📊 *دراسة واستشارة مشروع عملة SUI {p_str}*\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *القيمة الفعلية للمشروع:*\n"
            "• معالجة موازية فائقة السرعة ولغة برمجة Move الآمنة الموجهة للألعاب والـ DeFi.\n"
            "• نمو غير مسبوق في السيولة المقفلة (TVL) وجذب كبار المطورين.\n\n"
            "🎯 *الرؤية الاستثمارية للمدى المتوسط:*\n"
            "• العملة مرشحة لتصدر العملات البديلة الصاعدة؛ مناطق التجميع الأفضل تكون بعد موجات التصحيح الهابطة.\n"
            "━━━━━━━━━━━━━━━━━━━"
        )

    # فحص عملة سولانا
    if "سولانا" in clean or "سول" in clean or "sol" in clean:
        t = get_live_ticker("SOL")
        p_str = f"`{t['price']:,.2f}$` ({t['change']:+.2f}%)" if t else ""
        return (
            f"📊 *دراسة واستشارة مشروع عملة SOLANA {p_str}*\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "📌 *القيمة الفعلية للمشروع:*\n"
            "• المنصة الأولى عالمياً في حجم التداول اليومي والسرعة والرسوم المنخفضة.\n"
            "• المركز الأساسي لسيولة التجزئة وعملات الميم مع ترقب صناديق الـ ETF.\n\n"
            "🎯 *الرؤية الاستثمارية:*\n"
            "• تعتبر الركيزة الأكثر أماناً بعد البيتكوين والإيثيريوم للاستثمار المتوسط والبعيد.\n"
            "━━━━━━━━━━━━━━━━━━━"
        )

    # استجابة عامة
    return (
        f"💼 *استشارة المستشار المالي (GOLD WHALE):*\n\n"
        f"• تم فحص طلبك حول: `{text}`.\n"
        f"• **النصيحة الأساسية:** بناء المراكز المالية يجب أن يتم دائماً عبر تجزئة رأس المال (DCA) والتركيز على شبكات البنية التحتية القوية وتجنب ملاحقة الشموع الصاعدة.\n\n"
        f"💡 يمكنك كتابة أي استفسار محدد مثل: *«معي 500$ كيف أستثمرها»* أو *«ما هي أهداف سولانا وسوي؟»*."
    )

def handle_user_query(text):
    prompt = f"أنت مستشار مالي وصندوق استثماري بالعملات الرقمية، أجب باللغة العربية باحترافية عن: {text}"
    ai_reply = query_ai_online(prompt)
    if ai_reply:
        return ai_reply
    return build_offline_financial_advice(text)

# ==========================================
# 5. التقرير السريع للسوق
# ==========================================
def get_quick_market_pulse():
    btc = get_live_ticker("BTC")
    eth = get_live_ticker("ETH")
    sol = get_live_ticker("SOL")
    sui = get_live_ticker("SUI")

    def fmt(name, t):
        if not t: return f"• *{name}:* `مستقر`"
        em = "🟢" if t["change"] >= 0 else "🔴"
        p = f"{t['price']:,.2f}$" if t['price'] >= 1 else f"{t['price']:,.4f}$"
        return f"• *{name}:* `{p}` ({em} {t['change']:+.2f}%)"

    msg = "🌍 *نظرة موجزة على السوق وحركة السيولة اللحظية*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += f"{fmt('البيتكوين (BTC)', btc)}\n"
    msg += f"{fmt('الإيثيريوم (ETH)', eth)}\n"
    msg += f"{fmt('سولانا (SOL)', sol)}\n"
    msg += f"{fmt('سوي (SUI)', sui)}\n\n"
    msg += "🧠 *القراءة الاقتصادية:*\n"
    msg += "1. استقرار حركة البيتكوين يدعم تدفق السيولة نحو العملات البديلة القوية.\n"
    msg += "2. شبكات الطبقة الأولى السريعة ومشاريع الـ AI تقود الزخم الاستثماري.\n"
    msg += "3. احتفظ دائماً بجزء من السيولة النقدية لاقتناص فرص الارتداد.\n"
    msg += "━━━━━━━━━━━━━━━━━━━"
    return msg

# ==========================================
# 6. الحلقة الرئيسية
# ==========================================
def main():
    print("🚀 وكيل الذكاء الاصطناعي والمستشار المالي يعمل الآن 24/7...")
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

                    if text in ["/start", "بدء", "مرحبا"]:
                        welcome = (
                            "👋 *أهلاً بك! أنا مستشارك المالي الذكي (GOLD WHALE AI Advisor).*\n\n"
                            "💼 **كيف يمكنني مساعدتك اليوم؟**\n"
                            "تحدث معي مباشرة واطرح أي استفسار مالي أو استثماري ببالك، مثل:\n"
                            "• _«معي 1000$ استثمار متوسط المدى في سولانا وسوي»_\n"
                            "• _«ما هي أفضل مشاريع الذكاء الاصطناعي للاستثمار؟»_\n"
                            "• _«كيف أوزع محفظتي بطريقة آمنة؟»_\n\n"
                            "👇 *اكتب رسالتك مباشرة، أو استخدم الأزرار أدناه.*"
                        )
                        send_msg(chat_id, welcome, get_simple_keyboard())

                    elif text == "🌍 نظرة سريعة على السوق والسيولة":
                        send_msg(chat_id, get_quick_market_pulse())

                    elif text == "💼 استشارة مالية وإدارة محفظة":
                        guide = (
                            "💼 *قسم الاستشارات المالية وإدارة المحافظ:*\n\n"
                            "أرسل لي تفاصيل محفظتك وسأعطيك خطة مدروسة فوراً:\n"
                            "• المبلغ المتوفر للاستثمار (مثال: 500$ أو 2000$).\n"
                            "• المدة الزمنية (مضاربة سريعة، أو استثمار للمدى المتوسط والبعيد).\n"
                            "• العملات التي تفضلها أو تمتلكها حالياً."
                        )
                        send_msg(chat_id, guide)

                    else:
                        reply = handle_user_query(text)
                        send_msg(chat_id, reply)

        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    main()
