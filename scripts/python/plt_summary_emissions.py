import utilities as util
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ----- Matplotlib configuration -----
plt.rcParams["hatch.linewidth"] = 0.25
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 8

# ----- Functions -----
def summarize_emissions(filepath, levels):
    scaling_time = 8760 / (4 * 24 * 7)  # hours in 4 weeks per year
    scaling_units = 1e-6  # kgs/ktons

    data = pd.read_csv(filepath)
    data = util.rename_columns(data, names_columns)
    data = util.rename_values(data, names_values)
    data = util.aggregate_data(data, levels, ["Value"])
    data = util.diff_from(data, "Scenario", "S0")

    data["Value"] = data["Value"] * scaling_units * scaling_time
    data["Value"] = data["Value"].round(3)
    data = data.reset_index()
    return data


def build_subplot(df, df_net, bars, categories, values, ax):
    # Plots the bars
    df = df.pivot_table(index=bars, columns=categories, values=values)
    df.plot(kind="bar", stacked=True, ax=ax, legend=False, edgecolor="red")

    # Plots the net change as markers on top of the bars
    df_net = df_net.set_index(["Scenario"])
    (marker,) = ax.plot(
        df_net.index,
        df_net,
        marker="o",
        linestyle="None",
        color=map_color["Net"],
        markersize=4,
    )

    # Collects the bar labels for the legend, and sets the bar properties
    for container in ax.containers:  # type: ignore
        label = container.get_label()
        entity, fuel = (
            label.replace("(", "").replace(")", "").replace("'", "").split(", ")
        )

        if (entity, fuel) not in bar_labels:
            bar_labels.append((entity, fuel))
        for bar in container:
            bar.set_linewidth(0.3)  # Set bar edge linewidht
            bar.set_color(map_color[entity])  # Set the color
            bar.set_edgecolor("black")  # Set hatch color (needed)
            bar.set_hatch(map_hatch[fuel])  # Set the hatch pattern

    return marker


# ----- Data -----

option_save = True  # Set to True to save the plot
option_show = False # Set to True to show the plot

width = 14 # cm
heigth = 7 # cm 
DPI = 1200

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
        "municipal waste": "mun. waste",
    },
}

map_color = {"DC": "#94caec", "DH": "#dcce7d", "Net": "#EE6677"}
map_hatch = {"electricity": "///", "mun. waste": "xxx", "natural gas": "..."}

filepath_C1 = "M:/J2/results/selected_weeks/C1/csv/CARBON_EMISSIONS.csv"
filepath_C2 = "M:/J2/results/selected_weeks/C2/csv/CARBON_EMISSIONS.csv"
filepath_plot = "M:/J2/results/selected_weeks/consolidated/figures/SummaryCarbon.png"

# ----- Data processing -----

data_1 = summarize_emissions(filepath_C1, ["Scenario", "Entity", "Fuel"])
data_2 = summarize_emissions(filepath_C2, ["Scenario", "Entity", "Fuel"])

net_1 = summarize_emissions(filepath_C1, ["Scenario"])
net_2 = summarize_emissions(filepath_C2, ["Scenario"])


# ----- Plotting -----
bar_labels = []
fig, axes = plt.subplots(1, 2, figsize=(width/2.54, heigth/2.54))

marker = build_subplot(data_1, net_1, ["Scenario"], ["Entity", "Fuel"], "Value", axes[0])
marker = build_subplot(data_2, net_2, ["Scenario"], ["Entity", "Fuel"], "Value", axes[1])


# ----- Legend -----
## Add handle for each entity-fuel combination (by creating a patch)
legend_handles = [
    patches.Rectangle((0, 0), 1, 1, fc=map_color[entity], hatch=map_hatch[fuel])
    for entity, fuel in bar_labels
]

## Add handle (marker) for "net change"
legend_handles.append(marker)

# Create legend labels
legend_labels = [f"{entity} -\n{fuel}" for entity, fuel in bar_labels]
legend_labels.append("Net change")

# Add the legend to the plot
fig.legend(
    legend_handles,
    legend_labels,
    loc="center right",
    ncol=1,
    title="Entity - Fuel",
    title_fontproperties={"weight": "bold"},
    fancybox=True,
    # frameon=False,
)

# ----- Plot formatting -----
axes[0].set_ylabel(
    "Annual carbon emissions change \n relative to S0 - [kton]", fontweight="bold"
)

axes[0].set_title("C1 - Small DC", fontweight="bold", fontsize=9)
axes[1].set_title("C2 - Large DC", fontweight="bold", fontsize=9)

axes[0].set_xlabel("Scenario", fontweight="bold")
axes[1].set_xlabel("Scenario", fontweight="bold")

axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

axes[0].set_ylim([-1.2, 0.3])
axes[1].set_ylim([-60.0, 15])

axes[0].set_yticks(np.arange(0.3, -1.21, -0.3))
axes[1].set_yticks(np.arange(15.0, -60.10, -15.0))

axes[0].grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5)
axes[1].grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

plt.tight_layout(rect=[0, 0, 0.82, 1])  # Adjust layout to make room for the legend

# ----- Show and save the plot -----
if option_save == True:
    plt.savefig(filepath_plot, dpi=DPI, bbox_inches="tight")
    print(f"Plot saved to {filepath_plot}")

if option_show == True:
    plt.show()