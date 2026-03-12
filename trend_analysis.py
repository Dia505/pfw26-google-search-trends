import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

data = pd.read_csv("google_search_trends.csv", index_col=0, parse_dates=True)

# Calculation of spike threshold for a 3-day window period
spike = {}
brands = ["Dior", "Alaia", "Givenchy", "Balenciaga", "Chanel"]
for brand in brands:
    rolling_mean = data[brand].rolling(3).mean()
    rolling_std = data[brand].rolling(3).std()
    spike[brand] = data.loc[data[brand] > rolling_mean + 1.0 * rolling_std, brand]
    
print(f"\nPFW 26 Womenswear Fall Winter Search Spikes\n")
spike_df = pd.concat(spike, axis=0)
print(spike_df) 

show_dates = {
    "Dior": "2026-03-03",
    "Alaia": "2026-03-04",
    "Givenchy": "2026-03-06",
    "Balenciaga": "2026-03-07",
    "Chanel": "2026-03-09"
}
show_dates = {k:pd.to_datetime(v) for k,v in show_dates.items()}

# Specifies search spikes that occurred on the show day
print("\nShow Day Spikes\n")
for brand in brands:
    show_day = show_dates[brand]
    brand_spike = spike[brand]

    if not brand_spike.empty:
        for spike_day in brand_spike.index:
            diff = abs((spike_day - show_day).days)

            if diff <= 1:
                print(f"{brand} search spike detected on show date: {spike_day.date()}")
            else:
                continue

plt.figure(figsize=(10,6))

for brand in brands:
    line, = plt.plot(data.index, data[brand], marker='o', label=brand)
    color = line.get_color()
    show_day = show_dates[brand]
    plt.axvline(show_day, linestyle='--', alpha=0.4, color=color)

# Custom legend entry for dotted line which denotes the show date
runway_line = Line2D([0], [0], color='black', linestyle='--', alpha=0.4, label='Runway Show Day')
plt.legend(handles=[*plt.gca().get_legend_handles_labels()[0], runway_line])

plt.title("Google Search Interest - Paris Fashion Week 2026")
plt.xlabel("Date")
plt.ylabel("Search Interest")
plt.grid(True)
plt.show()
