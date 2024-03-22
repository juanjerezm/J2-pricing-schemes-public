import utilities as util
import pandas as pd

def process_data(filepath):
    # Process data
    df = pd.read_csv(filepath)
    df = util.rename_columns(df, names_columns)
    df = util.rename_values(df, names_values)
    df = util.aggregate_data(df, ["Scenario", "Entity"], "Value")
    df = df.reset_index()

    # Calculate system values
    df_system = util.aggregate_data(df, ["Scenario"], "Value").to_frame().reset_index()
    df_system = df_system.assign(Entity="SYSTEM")[["Scenario", "Entity", "Value"]]

    # join the two dataframes
    df = pd.concat([df, df_system])
    df = df.sort_values(by=["Scenario", "Entity"])

    return df


filepath_C1 = "M:/J2/results/selected_weeks/C1/csv/CARBON_EMISSIONS.csv"
filepath_C2 = "M:/J2/results/selected_weeks/C2/csv/CARBON_EMISSIONS.csv"
output_path = "M:/J2/results/selected_weeks/consolidated/summary_carbon.csv"

scaling_time = 8760 / (4 * 24 * 7)  # hours in 4 weeks per year
scaling_units = 1e-6  # kgs/ktons

names_columns = {
    "scenario": "Scenario",
    "T": "Timestep",
    "TECH": "Technology name",
    "TYPE": "Entity",
    "F": "Fuel",
    "value": "Value",
}

names_values = {
    "Entity": {
        "HR": "DC",
        "HO": "DH",
        "BP": "DH",
        "EX": "DH",
        "CO": "DC",
    },
}

df_1 = process_data(filepath_C1)
df_2 = process_data(filepath_C2)

df_1["Case"] = "C1"
df_2["Case"] = "C2"
df = pd.concat([df_1, df_2])
df = df[["Case", "Scenario", "Entity", "Value"]]

# scale the values
df["Value"] = df["Value"] * scaling_time * scaling_units

# to csv
df.to_csv(output_path, index=False)
print(f"Data processed and saved to {output_path}")