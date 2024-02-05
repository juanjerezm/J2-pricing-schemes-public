import pandas as pd
from pathlib import Path

def process_timeseries(timesteps, nickname):
    # Validate input
    if not isinstance(timesteps, list) or not all(isinstance(t, int) for t in timesteps):
        print("Invalid timesteps input. Provide a list of integers.")
        return
    
    # Determine the input and output directories based on cwd and the provided logic
    cwd = Path.cwd()
    bottom_dir_name = 'timeseries-' + nickname
    # input_dir = cwd / "new_data" / "master_timeseries"
    input_dir = cwd / "datasets" / "master-timeseries"
    output_dir = cwd / "datasets" / bottom_dir_name

    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each CSV file in the input directory
    for file_path in input_dir.glob("*.csv"):
        # Attempt to read the CSV with headers first
        df = pd.read_csv(file_path)
        
        # If the first cell is "T0001", we assume the file has headers
        if df.iloc[0, 0] == "T0001":
            df = df.iloc[1:]  # Skip the "T0001" row
            header_included = True
        else:
            # If the CSV does not start with "T0001", we assume it does not have headers
            df = pd.read_csv(file_path, header=None)
            header_included = False
        
        # If the header of the first column is "Unnamed: 0", replace it with an empty string
        if header_included and df.columns[0] == "Unnamed: 0":
            df.columns = [""] + list(df.columns[1:])
        
        # Filter rows based on the timesteps values in the first column
        selected_rows = df[df.iloc[:, 0].isin([f"T{i:04}" for i in timesteps])]
        
        # Save the processed data to the output directory with the given nickname
        output_file = output_dir / f"{nickname}_{file_path.name}"
        selected_rows.to_csv(output_file, index=False, header=header_included)
        print(f"Processed {file_path.name} -> {output_file}")


# Generate lists of timesteps for each season, each of length 168

def generate_timesteps(start, length=168):
    """Generate a list of timesteps starting from a specific timestep with a given length."""
    return list(range(start, start + length))

def generate_days(timesteps, nickname):
    # Calculate the interval for days based on the number of hours in a day (24)
    day_length = 24
    day_starts = [i for i in range(1, 8761, day_length)]  # Starting from 1 as timesteps start from T0001
    
    # Determine which days have at least one selected timestep
    selected_days = [f"D{i//day_length + 1:03}" for i in day_starts if any(timestep in timesteps for timestep in range(i, i + day_length))]

    # Save the selected days to a file
    output_dir = Path.cwd() / "new_data" / nickname
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{nickname}_days.csv"
    print(f"Saving selected days to {output_file}")
    with open(output_file, 'w') as f:
        for day in selected_days:
            f.write(f"{day}\n")
    
    return output_file

# Define the starting timesteps for each season
season_starts = {
    "winter": 841,
    "spring": 3025,
    "summer": 5209,
    "fall": 7393
}

# Generate the lists of timesteps for each season
season_timesteps = {season: generate_timesteps(start) for season, start in season_starts.items()}

all_seasons_timesteps = []
for timesteps in season_timesteps.values():
    all_seasons_timesteps.extend(timesteps)

# generate_days(all_seasons_timesteps, "all_seasons")
process_timeseries(all_seasons_timesteps, "selected_weeks")

# for season in season_timesteps.keys():
#     generate_days(season_timesteps[season], f"{season}")
#     process_timeseries(season_timesteps[season], f"{season}")
