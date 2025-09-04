import pandas as pd
from pathlib import Path

# === Load all CSV files from 'temperatures' folder ===
files = Path("temperatures").glob("*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Keep only relevant columns and clean data
df = df[["date", "station", "temp"]]
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["temp"] = pd.to_numeric(df["temp"], errors="coerce")
df = df.dropna()

# --- Assign seasons based on month ---
def get_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"

df["season"] = df["date"].dt.month.map(get_season)

# --- Calculate seasonal averages ---
season_avg = df.groupby("season")["temp"].mean()

with open("average_temp.txt", "w") as f:
    for s in ["Summer", "Autumn", "Winter", "Spring"]:
        avg = season_avg.get(s, float("nan"))
        f.write(f"{s}: {avg:.1f}°C\n")

# --- Station with largest temperature range ---
station_stats = df.groupby("station")["temp"].agg(["min", "max"])
station_stats["range"] = station_stats["max"] - station_stats["min"]
max_range = station_stats["range"].max()
winners = station_stats[station_stats["range"] == max_range]

with open("largest_temp_range_station.txt", "w") as f:
    for st, row in winners.iterrows():
        f.write(f"{st}: Range {row['range']:.1f}°C (Max {row['max']:.1f}°C, Min {row['min']:.1f}°C)\n")
stds = df.groupby("station")["temp"].std()
most_stable = stds[stds == stds.min()]
most_variable = stds[stds == stds.max()]

with open("temperature_stability_stations.txt", "w") as f:
    for st, v in most_stable.items():
        f.write(f"Most Stable: {st}: StdDev {v:.1f}°C\n")
    for st, v in most_variable.items():
        f.write(f"Most Variable: {st}: StdDev {v:.1f}°C\n")

print("Done! 3 files created.")
