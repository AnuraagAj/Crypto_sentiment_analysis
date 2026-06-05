import requests
import pandas as pd
import yfinance as yf
import time

# --- CONFIGURATION ---
TOKEN = "8092323127:AAEsSJ9RdctQCmAbfSihttpVP9gI7BWOHsI"
CHAT_ID = "1086415973"

def send_telegram_msg(text):
    """Sends a formatted Markdown message to your Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": text, 
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")

def monitor_market():
    print("--- 🚀 Starting Market Monitor ---")
    
    # 1. Fetch Price Data (1 month to ensure enough data for rolling metrics)
    try:
        ticker = "BTC-USD"
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        
        # FIX: Flatten MultiIndex columns if yfinance returns them
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        if 'Close' not in df.columns:
            print(f"❌ Error: 'Close' column not found. Columns available: {df.columns.tolist()}")
            return

        # 2. Calculate Research Metrics
        df['Returns'] = df['Close'].pct_change()
        # 7-Day Rolling Volatility
        current_vol = df['Returns'].rolling(window=7).std().iloc[-1]
        current_price = df['Close'].iloc[-1]
        
    except Exception as e:
        print(f"❌ Error fetching Financial Data: {e}")
        return

    # 3. Fetch Sentiment Data
    try:
        fng_res = requests.get("https://api.alternative.me/fng/").json()
        current_fng = int(fng_res['data'][0]['value'])
        fng_status = fng_res['data'][0]['value_classification']
    except Exception as e:
        print(f"❌ Error fetching Sentiment Data: {e}")
        return

    # 4. Alert Logic & Messaging
    print(f"📊 Stats: Price=${current_price:.2f} | FNG={current_fng} ({fng_status}) | Vol={current_vol:.4f}")

    # SCENARIO A: Critical Alert (High Greed + Rising Volatility)
    # Based on your research results where high sentiment moves correlate with volatility
    if current_fng > 70 and current_vol > 0.025:
        msg = (f"🚨 *CRITICAL SENTIMENT ALERT*\n\n"
               f"**Bitcoin Price:** ${current_price:,.2f}\n"
               f"**Market Sentiment:** {fng_status} ({current_fng})\n"
               f"**7-Day Volatility:** {current_vol:.4f}\n\n"
               f"⚠️ *Research Warning:* High greed levels are currently coinciding with elevated volatility. "
               f"This alignment historically precedes significant price corrections.")
        send_telegram_msg(msg)
        print("✅ Critical alert sent!")

    # SCENARIO B: Extreme Fear (Potential Buying Opportunity)
    elif current_fng < 25:
        msg = (f"📉 *EXTREME FEAR DETECTED*\n\n"
               f"**Market Sentiment:** {fng_status} ({current_fng})\n"
               f"**Volatility:** {current_vol:.4f}\n\n"
               f"Sentiment has dropped into the 'Extreme Fear' zone. In behavioral finance, "
               f"this is often viewed as a potential market bottom.")
        send_telegram_msg(msg)
        print("✅ Fear alert sent!")

    else:
        print("😴 Market is within normal research parameters. No alert sent.")

if __name__ == "__main__":
    monitor_market()