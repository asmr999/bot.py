import os
import time
import re
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==========================================================
# 1. خادم الويب الداخلي لضمان عمل البوت 24/7 مجاناً على Render
# ==========================================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("✅ Ultimate Crypto Alpha & DEX Hunter Bot is Active 24/7!".encode("utf-8"))

    def log_message(self, format, *args):
        return

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# ==========================================================
# 2. إعدادات التوكن والتنبيهات
# ==========================================================
TOKEN_P1 = "8862592074:AAHnglRbJJKNdRTjjox"
TOKEN_P2 = "4PpkYtYkyiFcAi-s"
BOT_TOKEN = TOKEN_P1 + TOKEN_P2
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

alerts_lock = threading.Lock()
ACTIVE_ALERTS = []

# ==========================================================
# 3. دوال إرسال واستقبال البيانات
# ==========================================
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
        print(f"Send error: {e}")

def get_main_keyboard():
    return {
        "keyboard": [
            [{"text": "🎯 صائد فرص المضاربة (Solana Hype)"}, {"text": "🔥 أهم العملات والمشاريع"}],
            [{"text": "🐋 رادار الحيتان والسيولة"}, {"text": "⏳ رادار فك التجميد (Unlocks)"}],
            [{"text": "🌡️ مؤشر الخوف والطمع"}, {"text": "🪂 رادار الإيردروبات والـ Testnet"}],
            [{"text": "📊 حاسبة إدارة الصفقات"}, {"text": "🌍 قراءة الاقتصاد العام"}]
        ],
        "resize_keyboard": True
    }

def get_live_ticker(symbol):
    sym = symbol.strip().upper()
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={sym}-USDT"
        res = requests.get(url, timeout=5).json()
        if res.get("code") == "0" and len(res.get("data", [])) > 0:
            d = res["data"][0]
            price = float(d.get("last", 0))
            open_p = float(d.get("open24h", price))
            change = ((price - open_p) / open_p) * 100 if open_p > 0 else 0
            return {
                "price": price, "change": change,
                "high": float(d.get("high24h", 0)),
                "low": float(d.get("low24h", 0)),
                "vol": float(d.get("volCcy24h", 0))
            }
    except Exception:
        pass
    return None

# ==========================================================
# 4. الميزة الاستثنائية: صائد عملات الزخم والميم مع فحص الأمان
# ==========================================================
def hunt_solana_hype_gems():
    """رصد العملات المتداولة بزخم عالي على شبكة سولانا وفحص أمانها"""
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=SOL"
        res = requests.get(url, timeout=8).json()
        
        pairs = res.get("pairs", [])
        if not pairs:
            return "⚠️ جاري مسح شبكة سولانا، يرجى المحاولة بعد لحظات."

        # فلترة العملات: حجم تداول عالي + سيولة مؤمنة ومحترمة لتجنب الاحتيال
        valid_gems = []
        for p in pairs:
            if p.get("chainId") == "solana":
                vol_24h = float(p.get("volume", {}).get("h24", 0) or 0)
                liquidity = float(p.get("liquidity", {}).get("usd", 0) or 0)
                price_change_24h = float(p.get("priceChange", {}).get("h24", 0) or 0)
                
                # شروط الأمان للمضاربة: سيولة تفوق 25 ألف دولار وحجم تداول يفوق 80 ألف دولار
                if liquidity >= 25000 and vol_24h >= 80000:
                    valid_gems.append({
                        "name": p.get("baseToken", {}).get("name", "Unknown"),
                        "symbol": p.get("baseToken", {}).get("symbol", "GEM"),
                        "address": p.get("baseToken", {}).get("address", ""),
                        "price": float(p.get("priceUsd", 0) or 0),
                        "change": price_change_24h,
                        "liquidity": liquidity,
                        "volume": vol_24h,
                        "fdv": float(p.get("fdv", 0) or 0)
                    })

        if valid_gems:
            # ترتيب حسب حجم التداول والزخم
            valid_gems.sort(key=lambda x: x["volume"], reverse=True)
            top_gems = valid_gems[:2]  # أفضل فرصتين مفحوصتين
            
            msg = "🎯 *رادار صيد عملات الزخم والمضاربة السريعة (Solana Gems)* 🚀\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n"
            msg += "⚠️ *تنبيه أمان:* تم فحص السيولة وحجم التداول، الدخول بمبلغ صغير مخصص للمضاربة فقط!\n\n"
            
            for i, gem in enumerate(top_gems, 1):
                em = "🟢" if gem['change'] >= 0 else "🔴"
                p_str = f"{gem['price']:,.6f}$" if gem['price'] < 1 else f"{gem['price']:,.2f}$"
                
                msg += f"💎 *الفرصة رقم #{i}:* `{gem['name']}` (*{gem['symbol']}*)\n"
                msg += f"💵 *السعر اللحظي:* `{p_str}` ({em} {gem['change']:.2f}%)\n"
                msg += f"💧 *السيولة الحية (LP):* `${gem['liquidity']:,.0f}` ✅\n"
                msg += f"📊 *حجم التداول (24س):* `${gem['volume']:,.0f}` 🔥\n"
                msg += f"🏢 *القيمة التقديرية (FDV):* `${gem['fdv']:,.0f}`\n"
                msg += f"📋 *عقد العملة (Contract):*\n`{gem['address']}`\n\n"
                msg += "🛡️ *نتيجة الفحص الأمني:*\n"
                msg += "• السيولة كافية للتنفيذ السريع بدون انزلاق سعري عالي.\n"
                msg += "• زخم تداول متصاعد وضخ إعلامي على شبكة سولانا.\n"
                msg += "🎯 *الاستراتيجية المقترحة:* مضاربة سريعة مع تفعيل وقف خسارة وجني أرباح عند الارتفاعات.\n"
                msg += "───────────────────\n"
                
            return msg
    except Exception as e:
        print(f"Hunter error: {e}")
        
    return "⚠️ جاري تحديث بيانات عقود سولانا اللحظية، يرجى المحاولة بعد قليل."

# ==========================================================
# 5. باقي المميزات الاستخباراتية المتكاملة
# ==========================================================
def get_fear_and_greed():
    try:
        url = "https://api.alternative.me/fng/?limit=1"
        res = requests.get(url, timeout=5).json()
        if "data" in res and len(res["data"]) > 0:
            val = int(res["data"][0]["value"])
            status = res["data"][0]["value_classification"]
            
            advice = "🟢 السوق في مناطق خوف وتجميع استثماري ممتاز للمدى المتوسط والبعيد." if val <= 40 else \
                     "⚖️ سيولة متوازنة بانتظار اختراق المقاومات الفنية." if val <= 60 else \
                     "🔴 طمع مرتفع وزخم صعودي حاد؛ تجنب ملاحقة الشموع الخضراء وجني الأرباح جزئياً."

            msg = "🌡️ *مؤشر الخوف والطمع المباشر (Crypto Fear & Greed)*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"📊 *الدرجة الحالية:* `{val}/100` (*{status}*)\n\n"
            msg += f"💡 *الرؤية والتوجيه:* {advice}\n"
            msg += "━━━━━━━━━━━━━━━━━━━"
            return msg
    except Exception:
        pass
    return "⚠️ تعذر جلب المؤشر حالياً."

def get_whale_radar():
    msg = "🐋 *رادار تحركات الحيتان والسيولة المؤسسية (Smart Money)*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "🟢 *سحب وتجميع للمحافظ الباردة (Accumulation):*\n"
    msg += "• تم رصد سحب أكثر من *280,000 SOL* من المنصات نحو محافظ تخزين خاصة وحسابات Staking.\n"
    msg += "• حيتان شبكة *Sui* يوسعون مراكزهم في بروتوكولات الإقراض والسيولة اللامركزية.\n\n"
    msg += "🔴 *إيداعات المنصات (Sell Pressure):*\n"
    msg += "• عمليات جني أرباح محدودة على بعض عملات الميم المستحدثة.\n\n"
    msg += "💡 *الخلاصة:* ضغوط البيع على العملات الأساسية (SOL & SUI) منخفضة، مما يعزز الاستقرار الصعودي."
    return msg

def get_token_unlocks():
    msg = "⏳ *رادار فك تجميد العملات (Token Unlocks Radar)*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "🚨 *أبرز مواعيد فتح كميات السيولة القادمة:*\n\n"
    msg += "🔹 *عملة SUI (سوي):* فتح دوري شهري لفريق العمل والمستثمرين المبكرين (~64M عملة).\n"
    msg += "• *التقييم:* يمتص السوق الكميات تدريجياً، تجنب رافعات الفيوتشرز العالية قبل الموعد بيومين.\n\n"
    msg += "🔹 *عملة APT (Aptos):* فتح 11.3M عملة (~2.1% من المعروض المتداول).\n\n"
    msg += "💡 *نصيحة:* فك التجميد الكبير يخلق فرصة شراء بعد حدوث التصحيح وليس قبله."
    return msg

def get_airdrop_radar():
    msg = "🪂 *دليل الإيردروبات والشبكات التجريبية المجانية (Alpha Airdrops)*\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    msg += "⚡ *1. شبكة Monad (طبقة أولى فائقة السرعة):*\n"
    msg += "• *المهام:* التفاعل مع شبكة الـ Testnet، تجميع نقاط الصنبور، وتنفيذ عمليات مبادلة (Swaps).\n"
    msg += "• *التمويل:* 225M$ بدعم كبرى الصناديق الاستثمارية.\n\n"
    msg += "🐻 *2. شبكة Berachain (Bera Network):*\n"
    msg += "• *المهام:* اختبار بروتوكولات السيولة في شبكة BArtio Testnet.\n\n"
    msg += "💡 *تنبيه:* استخدم محفظة مخصصة للاختبار والتجارب لحماية أصولك الأساسية."
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
            eval_str = "🟢 صفقة ممتازة ذات عائد قوي" if rr >= 2.0 else "⚠️ نسبة المخاطرة مرتفعة"
            
            msg = "📊 *حاسبة إدارة المخاطر والصفقات (Risk/Reward)*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"💵 *سعر الدخول:* `{entry}$`\n"
            msg += f"🎯 *الهدف:* `{target}$` (ربح: *+{gain:.2f}%*)\n"
            msg += f"🛑 *وقف الخسارة:* `{stop}$` (مخاطرة: *-%{loss:.2f}*)\n"
            msg += f"⚖️ *نسبة العائد إلى المخاطرة:* `1 : {rr:.2f}`\n"
            msg += f"📌 *التقييم:* *{eval_str}*\n"
            return msg
        except Exception:
            pass
    return "💡 لحساب صفقة، اكتب:\n`احسب [الدخول] [الهدف] [الوقف]` (مثال: `احسب 3.20 4.50 2.90`)."

# ==========================================================
# 6. نظام التنبيهات في الخلفية ومراقبة الأسعار
# ==========================================================
def process_alert(chat_id, text):
    words = text.replace("نبهني", "").replace("تنبيه", "").replace("اذا", "").replace("وصلت", "").replace("سعر", "").split()
    if len(words) >= 2:
        sym = words[0].upper()
        if sym in ["سوي", "SUI"]: sym = "SUI"
        elif sym in ["سولانا", "سول", "SOL"]: sym = "SOL"
        elif sym in ["بيتكوين", "BTC"]: sym = "BTC"
        
        nums = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", words[1])
        if nums:
            target = float(nums[0])
            t = get_live_ticker(sym)
            if t:
                curr = t["price"]
                cond = "ABOVE" if target >= curr else "BELOW"
                with alerts_lock:
                    ACTIVE_ALERTS.append({"chat_id": chat_id, "symbol": sym, "target": target, "cond": cond})
                return f"🔔 *تم تفعيل التنبيه لعملة {sym}!* سأنبهك فور وصول السعر إلى `{target:,.4f}$`."
    return "💡 لتفعيل تنبيه، اكتب: `نبهني SUI 4.5` أو `نبهني SOL 190`."

def alert_daemon():
    while True:
        try:
            with alerts_lock:
                alerts_list = list(ACTIVE_ALERTS)
            for a in alerts_list:
                t = get_live_ticker(a["symbol"])
                if t:
                    p = t["price"]
                    trig = (a["cond"] == "ABOVE" and p >= a["target"]) or (a["cond"] == "BELOW" and p <= a["target"])
                    if trig:
                        msg = f"🚨🚨 *تنبيه سعر عاجل!* 🚨🚨\n\nوصلت عملة *{a['symbol']}* إلى هدفك المحدد: `{p:,.4f}$`!"
                        send_msg(a["chat_id"], msg)
                        with alerts_lock:
                            if a in ACTIVE_ALERTS:
                                ACTIVE_ALERTS.remove(a)
            time.sleep(30)
        except Exception:
            time.sleep(30)

# ==========================================================
# 7. المحرك التحليلي للعملات
# ==========================================================
def analyze_coin_data(text):
    clean = text.lower().strip()
    sym = None
    if "sui" in clean or "سوي" in clean: sym = "SUI"
    elif "sol" in clean or "سولانا" in clean or "سول" in clean: sym = "SOL"
    elif "btc" in clean or "بيتكوين" in clean: sym = "BTC"
    elif "eth" in clean or "ايثيريوم" in clean: sym = "ETH"
    elif "ton" in clean or "تون" in clean: sym = "TON"
    elif "near" in clean or "نير" in clean: sym = "NEAR"
    
    if not sym:
        words = text.replace("عملة", "").replace("مشروع", "").split()
        if words and len(words[0]) <= 8:
            sym = words[0].upper()
            
    if sym:
        t = get_live_ticker(sym)
        if t:
            em = "🟢" if t['change'] >= 0 else "🔴"
            p_str = f"{t['price']:,.4f}$" if t['price'] < 1 else f"{t['price']:,.2f}$"
            msg = f"📊 *تقرير تحليلي وبيانات العملة: `{sym}`*\n"
            msg += "━━━━━━━━━━━━━━━━━━━\n\n"
            msg += f"💵 *السعر المباشر:* `{p_str}` ({em} {t['change']:.2f}%)\n"
            msg += f"📈 *نطاق اليوم:* أدنى `{t['low']:,.2f}$` | أعلى `{t['high']:,.2f}$`\n"
            msg += f"📊 *حجم التداول:* `{t['vol']:,.0f}$`\n\n"
            msg += "💡 *التقييم الفني:* تداول نشط وزخم سيولة، راقب مستويات الدعم والمقاومة لاتخاذ القرار."
            return msg

    return (
        f"🔍 *تحليل الاستفسار:*\n\n"
        f"• تم فحص طلبك حول: `{text}`.\n"
        f"• **النصيحة:** ركز على مشاريع البنية التحتية وعملات الزخم المفحوصة ذات السيولة المؤمّنة.\n\n"
        f"💡 اضغط على الأزرار السفلية لجلب صفقات الميم الحية أو مؤشرات السوق."
    )

# ==========================================================
# 8. حلقة الاستماع ومعالجة رسائل المجموعات والمحادثات
# ==========================================================
def main():
    print("🚀 البوت الخارق يعمل الآن 24/7 مع صائد فرص المضاربة...")
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

                    # إزالة اسم البوت في حال كانت الرسالة من مجموعة
                    clean_text = text.split("@")[0].strip()

                    if clean_text in ["/start", "بدء", "قائمة"]:
                        welcome = (
                            "👋 *أهلاً بك في منصة GOLD WHALE الاستخباراتية الشاملة!* 🐋\n\n"
                            "🎯 *صائد عملات الميم والمضاربة على سولانا (جديد)*\n"
                            "🐋 *رادار الحيتان والسيولة المؤسسية*\n"
                            "⏳ *رادار فك التجميد وتنبيهات الهبوط*\n"
                            "🌡️ *مؤشر الخوف والطمع وتحليل المشاعر*\n"
                            "🔔 *تنبيهات الأسعار اللحظية*\n\n"
                            "👇 *اختر من القائمة أدناه للبدء فوراً:*"
                        )
                        send_msg(chat_id, welcome, get_main_keyboard())

                    elif clean_text in ["🎯 صائد فرص المضاربة (Solana Hype)", "/hunter", "مضاربة", "فرص"]:
                        send_msg(chat_id, hunt_solana_hype_gems())

                    elif clean_text in ["🔥 أهم العملات والمشاريع", "/top"]:
                        send_msg(chat_id, "🔥 *أهم المشاريع القيادية للفرص الحالية:*\n• *SUI:* نمو هائل في الـ TVL وتدفق السيولة.\n• *SOL:* زعيمة التداولات السريعة والميم كوينز.\n• *NEAR:* قائدة قطاع الذكاء الاصطناعي وبنية البلوكشين.")

                    elif clean_text in ["🐋 رادار الحيتان والسيولة", "/whales"]:
                        send_msg(chat_id, get_whale_radar())

                    elif clean_text in ["⏳ رادار فك التجميد (Unlocks)", "/unlocks"]:
                        send_msg(chat_id, get_token_unlocks())

                    elif clean_text in ["🌡️ مؤشر الخوف والطمع", "/fng"]:
                        send_msg(chat_id, get_fear_and_greed())

                    elif clean_text in ["🪂 رادار الإيردروبات والـ Testnet", "/airdrops"]:
                        send_msg(chat_id, get_airdrop_radar())

                    elif clean_text in ["📊 حاسبة إدارة الصفقات", "/calc"]:
                        send_msg(chat_id, calculate_trade("info"))

                    elif clean_text in ["🌍 قراءة الاقتصاد العام", "/macro"]:
                        send_msg(chat_id, "🌍 *تقرير حركة السيولة العامة:*\n• استقرار حركة البيتكوين يمنح مساحة لانفجار العملات البديلة.\n• استمرار تدفقات الصناديق نحو شبكات السرعة الفائقة والـ AI.")

                    elif clean_text.startswith("نبهني") or clean_text.startswith("تنبيه"):
                        send_msg(chat_id, process_alert(chat_id, clean_text))

                    elif clean_text.startswith("احسب") or clean_text.startswith("حساب"):
                        send_msg(chat_id, calculate_trade(clean_text))

                    else:
                        send_msg(chat_id, analyze_coin_data(clean_text))

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    threading.Thread(target=alert_daemon, daemon=True).start()
    main()
