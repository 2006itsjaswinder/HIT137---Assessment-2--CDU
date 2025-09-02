import os
import pandas as pd
from pathlib import Path

# Paths
base_path = Path(__file__).parent
data_folder = base_path / "temperatures"
output_folder = base_path / "q2_output"

# Create output folder if it doesn't exist
output_folder.mkdir(exist_ok=True)

# Check if temperatures folder exists
if not data_folder.exists():
    raise FileNotFoundError(f"Temperatures folder not found: {data_folder}")


# Function to map month number to season
def get_season(month_num):
    if month_num in [12, 1, 2]:
        return "Summer"  # Southern Hemisphere assumption
    elif month_num in [3, 4, 5]:
        return "Autumn"
    elif month_num in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"


all_data = []

# Read all CSV files in the folder
for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(data_folder, file)
        df = pd.read_csv(file_path)

        # Reshape data: Convert months columns into rows
        df_melted = df.melt(
            id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
            var_name="Month",
            value_name="Temperature"
        )

        # Convert month names to numbers
        month_order = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        df_melted["Month_Num"] = df_melted["Month"].map(month_order)

        # Add season column
        df_melted["Season"] = df_melted["Month_Num"].apply(get_season)

        all_data.append(df_melted)

# Combine all data
data = pd.concat(all_data)

# 1. Average temperature per season across all stations
avg_temp_season = data.groupby("Season")["Temperature"].mean().reset_index()
avg_temp_season.to_csv(output_folder / "avg_temp_season.txt", index=False)

# 2. Station with largest temperature range (max - min across all months)
station_range = data.groupby("STATION_NAME")["Temperature"].agg(lambda x: x.max() - x.min())
largest_station = station_range.idxmax()
largest_value = station_range.max()
with open(output_folder / "largest_range.txt", "w") as f:
    f.write(f"{largest_station},{largest_value:.2f}")

# 3. Most stable station (lowest standard deviation across months)
station_std = data.groupby("STATION_NAME")["Temperature"].std()
stable_station = station_std.idxmin()
stable_value = station_std.min()
with open(output_folder / "most_stable.txt", "w") as f:
    f.write(f"{stable_station},{stable_value:.2f}")

print(f"Processing complete. Results saved in: {output_folder}")
