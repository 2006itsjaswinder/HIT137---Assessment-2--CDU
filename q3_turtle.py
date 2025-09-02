import os
import pandas as pd

data_folder = "temperatures"

# Define seasons for months
seasons = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

all_avg = []
all_stations = []

for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        year = ''.join([c for c in file if c.isdigit()]) or "Unknown"
        filepath = os.path.join(data_folder, file)
        
        df = pd.read_csv(filepath)
        
        # Calculate seasonal averages for each station
        for _, row in df.iterrows():
            station = row["STATION_NAME"]
            season_avgs = {}
            for season, months in seasons.items():
                season_avgs[season] = row[months].mean()
            
            all_avg.append({"Year": year, "Station": station, **season_avgs})
            
            # For range and stability
            temps = row[list(seasons["Summer"] + seasons["Autumn"] + seasons["Winter"] + seasons["Spring"])]
            station_range = temps.max() - temps.min()
            station_std = temps.std()
            all_stations.append({"Station": station, "Range": station_range, "StdDev": station_std})

# Convert to DataFrame
avg_df = pd.DataFrame(all_avg)
avg_df.to_csv("avg_temp_season.txt", index=False)

stations_df = pd.DataFrame(all_stations)

# Largest range
largest_station = stations_df.loc[stations_df["Range"].idxmax()]
with open("largest_range.txt", "w") as f:
    f.write(f"{largest_station['Station']},{largest_station['Range']:.2f}")

# Most stable station
stable_station = stations_df.loc[stations_df["StdDev"].idxmin()]
with open("most_stable.txt", "w") as f:
    f.write(f"{stable_station['Station']},{stable_station['StdDev']:.2f}")

print("avg_temp_season.txt, largest_range.txt, and most_stable.txt generated.")
