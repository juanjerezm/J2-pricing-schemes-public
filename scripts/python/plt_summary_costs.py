import utilities as util
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ----- Matplotlib configuration -----
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 8


# ----- Functions -----
def process_data(case):
    # File paths
    data_dc_path = f"M:/J2/results/selected_weeks/{case}/csv/DC_NET_COST.csv"
    data_dh_path = f"M:/J2/results/selected_weeks/{case}/csv/DH_NET_COST.csv"

    # Read data
    data_dc = pd.read_csv(data_dc_path)
    data_dh = pd.read_csv(data_dh_path)

    # Assign entities
    data_dc = data_dc.assign(entity="DC")
    data_dh = data_dh.assign(entity="DH")

    # Concatenate and assign case
    data_all = pd.concat([data_dc, data_dh])
    data_all = data_all.assign(case=case)

    # Organize and sort
    data_all = data_all[["case", "scenario", "entity", "value"]]
    data_all = data_all.sort_values(by=["case", "scenario", "entity"])

    return data_all


def build_subplot(df, case, ax):
    # Filter data for relevant case and calculate totals
    data_case = df[df["case"] == case].pivot(
        index="scenario", columns="entity", values="value"
    )
    data_syst = data_case.sum(axis=1)

    # Make subplots (bars and total's marker)
    data_case.plot(kind="bar", stacked=True, ax=ax, color=map_color, legend=False)
    (marker,) = ax.plot(
        data_syst.index, data_syst, marker="o", linestyle="None", color=map_color["Net"]
    )

    # Formatting configuration
    dc_type = "Small" if case == "C1" else "Large" if case == "C2" else "Error"
    dc_scale = 1 if case == "C1" else 50 if case == "C2" else 0
    y_range = [-0.300, 0]
    y_ticks = np.arange(-0.300, 0.00001, 0.05)

    # Formatting
    if case == "C1":
        ax.set_ylabel(
            f"Annual change in operating cost \n [M€], relative to S0", fontweight="bold"
        )

    ax.set_title(f"{case} - {dc_type} DC", fontweight="bold", fontsize=9)
    ax.set_xlabel("Scenario", fontweight="bold")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_ylim([y * dc_scale for y in y_range])
    ax.set_yticks([y * dc_scale for y in y_ticks])
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

    return marker


# ----- Data -----
# option_save = False
# option_show = True

DPI = 1200
width = 14 # cm
height = 7 # cm

option_save = True
option_show = False

CASES = ["C1", "C2"]
filepath_plot = "M:/J2/results/selected_weeks/consolidated/figures/SummaryCost.png"

map_color = {"DC": "#94caec", "DH": "#dcce7d", "Net": "#EE6677"}
scaling_time = 8760 / (4 * 24 * 7)  # hours in 4 weeks per year
scaling_units = 1e-6  # €/M€


# ----- Process data -----
df = pd.concat([process_data(CASE) for CASE in CASES])
df["value"] = df["value"] * scaling_time * scaling_units
df = df.set_index(["case", "scenario", "entity"])
df = util.diff_from(df, "scenario", "S0").reset_index()

# ----- Make plot -----
fig, axs = plt.subplots(1, 2, figsize=(width / 2.54, height / 2.54), sharey=False)

marker1 = build_subplot(df, "C1", axs[0])
marker2 = build_subplot(df, "C2", axs[1])

# Collect legend handles and labels (based on first subplot)
handles, labels = axs[0].get_legend_handles_labels()
handles.append(marker1)
labels.append("Net change")

# Build legend and adjust space
fig.legend(
    handles,
    labels,
    loc="center right",
    ncol=1,
    title="Entity",
    title_fontproperties={"weight": "bold"},
    fancybox=True,
    shadow=False,
)
plt.tight_layout(rect=[0, 0, 0.82, 1])


# ----- Show and save the plot -----
if option_save == True:
    plt.savefig(filepath_plot, dpi=DPI, bbox_inches="tight")
    print(f"Plot saved to {filepath_plot}")

if option_show == True:
    plt.show()