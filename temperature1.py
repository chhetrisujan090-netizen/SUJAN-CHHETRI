import os, glob, csv, statistics
from collections import defaultdict

TEMPS_FOLDER = "temperatures"
SEASON_FILE = "average_temp.txt"
RANGE_FILE = "largest_temp_range_station.txt"
STABILITY_FILE = "temperature_stability_stations.txt"

SEASONS = {
    'Summer': [12, 1, 2],
    'Autumn': [3, 4, 5],
    'Winter': [6, 7, 8],
    'Spring': [9, 10, 11],
}

def month_to_season(m):
    for s, ms in SEASONS.items():
        if m in ms: return s

def parse_csv(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows

def main():
    if not os.path.isdir(TEMPS_FOLDER): return
    files = sorted(glob.glob(os.path.join(TEMPS_FOLDER, "*.csv")))
    if not files: return
    seasonal, stations = defaultdict(list), defaultdict(list)
    for p in files:
        rows = parse_csv(p)
        station_name = os.path.splitext(os.path.basename(p))[0]
        for r in rows:
            temp = None
            for k,v in r.items():
                kl = k.lower()
                if any(x in kl for x in ['temp','temperature','air']):
                    try: temp = float(v)
                    except: temp = None
                    break
            if temp is None: continue
            date_val = None
            for k,v in r.items():
                kl = k.lower()
                if any(x in kl for x in ['date','time']):
                    try:
                        parts = v.replace("-","/").replace(".","/").split("/")
                        nums = [int(x) for x in parts if x.isdigit()]
                        if len(nums)>=2: date_val = nums[1] if nums[0]>31 else nums[0]
                    except: pass
                    break
            if date_val: 
                s = month_to_season(date_val)
                if s: seasonal[s].append(temp)
            stations[station_name].append(temp)
    with open(SEASON_FILE,'w') as f:
        for s in ['Summer','Autumn','Winter','Spring']:
            vals = seasonal.get(s,[])
            f.write(f"{s}: {statistics.mean(vals):.1f}°C\n" if vals else f"{s}: NaN\n")
    ranges = {st:(max(v)-min(v),max(v),min(v)) for st,v in stations.items() if v}
    if ranges:
        mx = max(r[0] for r in ranges.values())
        winners = [(st,r) for st,r in ranges.items() if abs(r[0]-mx)<1e-9]
    else: winners=[]
    with open(RANGE_FILE,'w') as f:
        if winners:
            for st,(r,mx,mn) in winners:
                f.write(f"Station {st}: Range {r:.1f}°C (Max: {mx:.1f}°C, Min: {mn:.1f}°C)\n")
        else: f.write("No station data available\n")
    stds = {st:statistics.pstdev(v) for st,v in stations.items() if v}
    if stds:
        mn, mx = min(stds.values()), max(stds.values())
        stables = [(st,s) for st,s in stds.items() if abs(s-mn)<1e-9]
        variables = [(st,s) for st,s in stds.items() if abs(s-mx)<1e-9]
    else: stables=variables=[]
    with open(STABILITY_FILE,'w') as f:
        for st,s in stables: f.write(f"Most Stable: Station {st}: StdDev {s:.1f}°C\n")
        for st,s in variables: f.write(f"Most Variable: Station {st}: StdDev {s:.1f}°C\n")

if __name__ == '__main__':
    main()

