import requests

# --- المفاتيح والبيانات المدمجة ---
CRYPTORANK_API_KEY = "497d41132b239b213d9bdbbc038b144248324792a76ca0647c1acb4063d3"
TELEGRAM_BOT_TOKEN = "8862592074:AAHnglRbJJKNdRTjjox4PpkYtYkyiFcAi-s"
TELEGRAM_CHAT_ID = "7926863163"

# كميات محفظتك
SUI_AMOUNT = 900
SOL_AMOUNT = 3

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return None

def get_crypto_prices():
    """جلب أسعار SUI و SOL المباشرة وحساب قيمة المحفظة"""
    try:
        sui_res = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=SUIUSDT", timeout=10).json()
        sol_res = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=SOLUSDT", timeout=10).json()
        
        sui_price = float(sui_res.get("lastPrice", 0))
        sui_change = float(sui_res.get("priceChangePercent", 0))
        
        sol_price = float(sol_res.get("lastPrice", 0))
        sol_change = float(sol_res.get("priceChangePercent", 0))
        
        total_sui_val = sui_price * SUI_AMOUNT
        total_sol_val = sol_price * SOL_AMOUNT
        total_portfolio = total_sui_val + total_sol_val
        
        return {
            "sui_price": sui_price, "sui_change": sui_change, "sui_total": total_sui_val,
            "sol_price": sol_price, "sol_change": sol_change, "sol_total": total_sol_val,
            "portfolio_total": total_portfolio
        }
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None

def get_funding_deals():
    """جلب أحدث صفقات التمويل والمشاريع الجديدة من CryptoRank"""
    try:
        url = f"https://api.cryptorank.io/v1/funding-rounds?api_key={CRYPTORANK_API_KEY}&limit=3"
        res = requests.get(url, timeout=10).json()
        deals = []
        if "data" in res and len(res["data"]) > 0:
            for item in res["data"][:3]:
                name = item.get("projectName", "مشروع غير معروف")
                raised = item.get("raised", "غير محدد")
                category = item.get("category", "عام")
                stage = item.get("stage", "Seed")
                raised_str = f"{raised:,.0f}$" if isinstance(raised, (int, float)) else str(raised)
                deals.append(f"• `{name}` | تمويل: *{raised_str}* ({category} - {stage})")
        return deals
    except Exception as e:
        print(f"Error fetching deals: {e}")
        return []

def get_global_news():
    """جلب أحدث الأخبار الاقتصادية وحركة السوق العالمية"""
    try:
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://cointelegraph.com/rss"
        res = requests.get(url, timeout=10).json()
        news = []
        if res.get("status") == "ok" and "items" in res:
            for item in res["items"][:3]:
                title = item.get("title", "")
                link = item.get("link", "")
                news.append(f"• [{title}]({link})")
        return news
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def generate_and_send_report():
    prices = get_crypto_prices()
    deals = get_funding_deals()
    news = get_global_news()
    
    msg = "🌐 *التقرير الدوري الشامل للسوق والمحفظة* 🌐\n"
    msg += "━━━━━━━━━━━━━━━━━━━\n\n"
    
    # 1. قسم المحفظة وعملاتك
    if prices:
        sui_emoji = "🟢" if prices["sui_change"] >= 0 else "🔴"
        sol_emoji = "🟢" if prices["sol_change"] >= 0 else "🔴"
        
        msg += "📊 *حالة محفظتك وعملاتك الأساسية:*\n"
        msg += f"🔹 *SUI:* `{prices['sui_price']:.4f}$` ({sui_emoji} {prices['sui_change']:.2f}%)\n"
        msg += f"   ▫️ قيمة 900 حبة: *{prices['sui_total']:.2f}$*\n"
        msg += f"🔹 *SOL:* `{prices['sol_price']:.2f}$` ({sol_emoji} {prices['sol_change']:.2f}%)\n"
        msg += f"   ▫️ قيمة 3 حبات: *{prices['sol_total']:.2f}$*\n"
        msg += f"💰 *إجمالي قيمة المحفظة اللحظية:* `{prices['portfolio_total']:.2f}$`\n\n"
    
    # 2. قسم صفقات التمويل المؤسسي
    msg += "💼 *أحدث صفقات التمويل والمشاريع (CryptoRank):*\n"
    if deals:
        msg += "\n".join(deals) + "\n\n"
    else:
        msg += "• لا توجد جولات تمويل مسجلة حديثاً.\n\n"
        
    # 3. قسم أخبار الاقتصاد والسوق العالمية
    msg += "🌍 *أبرز أخبار السوق والاقتصاد العالمي:*\n"
    if news:
        msg += "\n".join(news) + "\n\n"
    else:
        msg += "• جاري متابعة تطورات السوق لحظة بلحظة.\n\n"
        
    msg += "━━━━━━━━━━━━━━━━━━━\n"
    msg += "🤖 _تم التحديث والإرسال تلقائياً_"
    
    send_telegram_message(msg)
    print("✅ تم إرسال التقرير الشامل بنجاح!")

if __name__ == "__main__":
    generate_and_send_report()
