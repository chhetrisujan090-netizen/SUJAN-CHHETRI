import os
import pandas as pd

def load_all_data(folder="temperatures"):
    all_data = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))
            all_data.append(df)
    return pd.concat(all_data, ignore_index=True)

def calculate_seasonal_average(df):
    seasons = {
        "Summer": [12, 1, 2],
        "Autumn": [3, 4, 5],
        "Winter": [6, 7, 8],
        "Spring": [9, 10, 11]
    }
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    results = {}
    for season, months in seasons.items():
        season_data = df[df['Month'].isin(months)]['Temperature'].dropna()
        results[season] = season_data.mean()
    with open("average_temp.txt", "w") as f:
        for k, v in results.items():
            f.write(f"{k}: {v:.1f}°C\n")

def calculate_temp_range(df):
    results = []
    for station, group in df.groupby("Station"):
        max_t = group['Temperature'].max()
        min_t = group['Temperature'].min()
        rng = max_t - min_t
        results.append((station, rng, max_t, min_t))
    max_range = max(r[1] for r in results)
    with open("largest_temp_range_station.txt", "w") as f:
        for station, rng, max_t, min_t in results:
            if rng == max_range:
                f.write(f"{station}: Range {rng:.1f}°C (Max: {max_t:.1f}°C, Min: {min_t:.1f}°C)\n")

def calculate_stability(df):
    results = []
    for station, group in df.groupby("Station"):
        std_dev = group['Temperature'].std()
        results.append((station, std_dev))
    min_std = min(r[1] for r in results)
    max_std = max(r[1] for r in results)
    with open("temperature_stability_stations.txt", "w") as f:
        for station, std_dev in results:
            if std_dev == min_std:
                f.write(f"Most Stable: {station}: StdDev {std_dev:.1f}°C\n")
        for station, std_dev in results:
            if std_dev == max_std:
                f.write(f"Most Variable: {station}: StdDev {std_dev:.1f}°C\n")

if __name__ == "__main__":
    df = load_all_data()
    calculate_seasonal_average(df)
    calculate_temp_range(df)
    calculate_stability(df)
    print("✅ Temperature analysis complete! Results saved to text files.")
