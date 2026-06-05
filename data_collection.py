import os
import yfinance as yf

# Get script directory (scripts/)
script_dir = os.path.dirname(os.path.abspath(__file__))


project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Define data folder path
data_dir = os.path.join(project_root, "data")

# Create data directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def download_crypto_data(ticker="BTC-USD", start="2023-01-01", end="2024-01-01"):
    print(f"Downloading data for {ticker}...")
    
    df = yf.download(ticker, start=start, end=end)
    
    # Save file correctly
    file_path = os.path.join(data_dir, f"{ticker}_historical.csv")
    df.to_csv(file_path)
    
    print(f"Success! Saved to {file_path}")
    return df

if __name__ == "__main__":
    crypto_df = download_crypto_data()
    print(crypto_df.head())