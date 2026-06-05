import streamlit as st
import requests
import yfinance as yf
import pandas as pd
# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8092323127:AAEsSJ9RdctQCmAbfSihttpVP9gI7BWOHsI"
CHAT_ID = "1086415973"
NEWS_API_KEY = "8edab4cd890b4fd8a35d9c76137bd3ee"



def get_crypto_data():
    df = yf.download("BTC-USD", period="2d", interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    current_price = df['Close'].iloc[-1]
    change = current_price - df['Close'].iloc[-2]
    return current_price, change

def get_latest_news():
    """Fetches top 5 headlines using NewsAPI.org."""
    url = (f"https://newsapi.org/v2/everything?"
           f"q=bitcoin&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}")
    try:
        response = requests.get(url).json()
        return response.get('articles', [])
    except:
        return []

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    return requests.post(url, data=payload).ok

# --- STREAMLIT UI ---
st.set_page_config(page_title="Crypto AI Monitor", layout="wide")
st.title("🛡️ Crypto Research & Alert Dashboard")

col1, col2, col3 = st.columns(3)

# BOX 1: LIVE PRICE
with col1:
    st.subheader("📊 Market Price")
    price, change = get_crypto_data()
    st.metric(label="Bitcoin (BTC)", value=f"${price:,.2f}", delta=f"${change:,.2f}")

# BOX 2: RESEARCH CONTROL
with col2:
    st.subheader("🧠 Research Control")
    fear_rate = st.slider("Simulate Fear/Greed", 0, 100, 14)
    if fear_rate <= 25:
        st.error(f"ZONE: EXTREME FEAR")
    elif fear_rate >= 75:
        st.success(f"ZONE: EXTREME GREED")
    else:
        st.info("ZONE: NEUTRAL")

# BOX 3: GLOBAL NEWS FEED (NewsAPI Version)
with col3:
    st.subheader("📰 Global Bitcoin News")
    articles = get_latest_news()
    if articles:
        for art in articles:
            st.markdown(f"**[{art['title']}]({art['url']})**")
            st.caption(f"Source: {art['source']['name']} | 📅 {art['publishedAt'][:10]}")
    else:
        st.write("Enter NewsAPI key to see live feed.")

st.divider()

if st.button("🚀 Send Research Alert to Telegram", use_container_width=True):
    latest_title = articles[0]['title'] if articles else "N/A"
    msg = (f"🛡️ *DASHBOARD RESEARCH ALERT*\n\n"
           f"**Price:** ${price:,.2f}\n"
           f"**Sentiment Rate:** {fear_rate}\n"
           f"**Top News:** {latest_title}")
    
    if send_telegram_msg(msg):
        st.balloons()
        st.success("Alert Sent!")