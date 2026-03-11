import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("google_search_trends.csv", index_col=0, parse_dates=True)

spike = {}
brands = ["Dior", "Alaia", "Givenchy", "Balenciaga", "Chanel"]
for brand in brands:
    rolling_mean = data[brand].rolling(3).mean()
    rolling_std = data[brand].rolling(3).std()
    spike[brand] = data.loc[data[brand] > rolling_mean + 1.5 * rolling_std, brand]

show_dates = {
    "Dior": "2026-03-03",
    "Alaia": "2026-03-04",
    "Givenchy": "2026-03-06",
    "Balenciaga": "2026-03-07",
    "Chanel": "2026-03-09"
}
show_dates = {k:pd.to_datetime(v) for k,v in show_dates.items()}

print("\nRunway Show Impact Analysis\n")
for brand in brands:
    show_day = show_dates[brand]
    brand_spike = spike[brand]

    if not brand_spike.empty:
        for spike_day in brand_spike.index:
            diff = abs((spike_day - show_day).days)

            if diff <= 1:
                print(f"{brand} spike on {spike_day.date()} likely caused by runway show!")
            else:
                continue

plt.figure(figsize=(10,6))

for brand in brands:
    plt.plot(data.index, data[brand], marker='o', label=brand)

for brand, show_day in show_dates.items():
    plt.axvline(show_day, linestyle='--', alpha=0.4)

plt.title("Google Search Interest – Paris Fashion Week 2026")
plt.xlabel("Date")
plt.ylabel("Search Interest")
plt.legend()
plt.grid(True)

plt.show()
