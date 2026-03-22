import random
import time

from pytrends.request import TrendReq

# Random user agents to reduce blocking
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
]

# Initialize pytrends
pytrends = TrendReq(
    hl='en-US',
    tz=360,
    retries=3,
    backoff_factor=1,
    requests_args={'headers': {'User-Agent': random.choice(user_agents)}}
)

brands = ["Dior", "Alaia", "Chanel", "Balenciaga"]

timeframe = '2026-03-02 2026-03-14'

def fetch_trends(keywords, timeframe):
    """Fetch Google Trends with retry logic"""
    
    for attempt in range(5):

        try:
            print(f"Attempt {attempt+1}...")

            pytrends.build_payload(keywords, timeframe=timeframe)
            data = pytrends.interest_over_time()

            if not data.empty:
                print("Data fetched successfully")
                return data

        except Exception as e:
            print("Error:", e)

        sleep_time = random.randint(60, 120)
        print(f"Sleeping {sleep_time}s before retry...")
        time.sleep(sleep_time)

    print("Failed after multiple attempts.")
    return None


data = fetch_trends(brands, timeframe)

if data is not None:

    # Remove partial column
    if 'isPartial' in data.columns:
        data = data.drop(columns=['isPartial'])

    print(data.head())

    data.to_csv("google_search_trends.csv")

else:
    print("No data retrieved.")