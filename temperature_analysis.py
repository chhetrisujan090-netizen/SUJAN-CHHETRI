import pandas as pd
from pathlib import Path

# --- Load all CSV files ---
files = Path("temperatures").glob("*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Keep only needed columns
df = df[["date", "station", "temp"]]
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["temp"] = pd.to_numeric(df["temp"], errors="coerce")
df = df.dropna()

# --- Seasonal Average ---
def season(m):
    if m in [12, 1, 2]: return "Summer"
    if m in [3, 4, 5]: return "Autumn"
    if m in [6, 7, 8]: return "Winter"
    return "Spring"

df["season"] = df["date"].dt.month.map(season)
season_avg = df.groupby("season")["temp"].mean()

with open("average_temp.txt", "w") as f:
    for s in ["Summer", "Autumn", "Winter", "Spring"]:
        if s in season_avg:  # avoid KeyError
            f.write(f"{s}: {season_avg[s]:.1f}°C\n")

# --- Largest Temp Range ---
stats = df.groupby("station")["temp"].agg(["min", "max"])
stats["range"] = stats["max"] - stats["min"]
max_range = stats["range"].max()
winners = stats[stats["range"] == max_range]

with open("largest_temp_range_station.txt", "w") as f:
    for st, row in winners.iterrows():
        f.write(
            f"{st}: Range {row['range']:.1f}°C "
            f"(Max {row['max']:.1f}°C, Min {row['min']:.1f}°C)\n"
        )

# --- Temperature Stability ---
stds = df.groupby("station")["temp"].std().dropna()
stable = stds[stds == stds.min()]
variable = stds[stds == stds.max()]

with open("temperature_stability_stations.txt", "w") as f:
    for st, v in stable.items():
        f.write(f"Most Stable: {st}: StdDev {v:.1f}°C\n")
    for st, v in variable.items():
        f.write(f"Most Variable: {st}: StdDev {v:.1f}°C\n")

print("Done! 3 files created.")
