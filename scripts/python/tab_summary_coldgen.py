import utilities as util
import pandas as pd

def process_data(filepath):
    # Process data
    df = pd.read_csv(filepath)
    df = util.rename_columns(df, names_columns)
    df = util.rename_values(df, names_values)
    df = util.aggregate_data(df, ["Scenario", "Technology name"], "Value")
    df = df.reset_index()

    df = df.sort_values(by=["Scenario", "Technology name"])

    return df


filepath_C1   = f'M:/J2/results/selected_weeks/C1/csv/GENERATION_COLD.csv'
filepath_C2   = f'M:/J2/results/selected_weeks/C2/csv/GENERATION_COLD.csv'
output_path   = f'M:/J2/results/selected_weeks/consolidated/summary_coldgeneration.csv'

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
    "Fuel": {
        "EC": "Electric chiller",
        "FC": "Free cooling",
        "HP_EHR": "Heat pump",
    },
}

scaling_time = 8760 / (4 * 24 * 7)  # hours in 4 weeks per year
scaling_units = 1e-3  # MWh/GWh

df_1 = process_data(filepath_C1)
df_2 = process_data(filepath_C2)

df_1 = df_1.assign(Case="C1")
df_2 = df_2.assign(Case="C2")

df = pd.concat([df_1, df_2])
df = df[["Case", "Scenario", "Technology name", "Value"]]
df = df.sort_values(by=["Case", "Scenario", "Technology name"])
df['Value'] = df['Value'] * scaling_time * scaling_units


df.to_csv(output_path, index=False)
print(f"Data processed and saved to {output_path}")