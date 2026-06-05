import yfinance as yf
import pandas as pd
import nltk

# Download a tiny bit of data to test
print("Testing yfinance...")
data = yf.download("BTC-USD", period="5d", interval="1d")
print(data.head())

# Download NLTK data for sentiment
print("\nDownloading NLTK VADER lexicon...")
nltk.download('vader_lexicon')

print("\nSetup Complete! You are ready to research.")

