import utilities as util
import pandas as pd


def process_data(CASE):
    # File paths
    data_dc_path = f"M:/J2/results/selected_weeks/{CASE}/csv/DC_NET_COST.csv"
    data_dh_path = f"M:/J2/results/selected_weeks/{CASE}/csv/DH_NET_COST.csv"

    # Read data
    data_dc = pd.read_csv(data_dc_path)
    data_dh = pd.read_csv(data_dh_path)

    # Calculate system values
    data_sys = data_dc[["scenario"]].copy()
    data_sys["value"] = data_dc["value"] + data_dh["value"]

    # Assign entities
    data_sys = data_sys.assign(entity="SYSTEM")
    data_dc = data_dc.assign(entity="DC")
    data_dh = data_dh.assign(entity="DH")

    # Concatenate and assign case
    data_all = pd.concat([data_dc, data_dh, data_sys])
    data_all = data_all.assign(case=CASE)

    # Organize and sort
    data_all = data_all[["case", "scenario", "entity", "value"]]
    data_all = data_all.sort_values(by=["case", "scenario", "entity"])

    return data_all

# ----- Data -----

CASES = ["C1", "C2"]
scaling_time = 8760 / (4 * 24 * 7)  # hours in 4 weeks per year
scaling_units = 1e-3  # €/k€

# ----- Process data -----
df = pd.concat([process_data(CASE) for CASE in CASES])
df["value"] = df["value"] * scaling_time * scaling_units

# ----- Save to csv -----
output_path = "M:/J2/results/selected_weeks/consolidated/summary_cost.csv"
df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")
