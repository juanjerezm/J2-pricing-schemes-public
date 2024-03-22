import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 8


save = True
show = False

DPI = 1200
width = 8.5
height = 8

# Output path
plot_path = f"M:/J2/results/selected_weeks/consolidated/figures/elecindexed-price.png"

# Day-ahead electricity prices
file_path = "datasets/timeseries-selected_weeks/selected_weeks_ts-electricity-price.csv"


# Linear relationship factors
m = {"C1": 0.3, "C2": -0.6}

c = {"C1": 6.0, "C2": 19.8}

# Define the x values
x = np.linspace(0, 70, 71)

line = {"C1": m["C1"] * x + c["C1"], "C2": m["C2"] * x + c["C2"]}


seasons = ["Wi.", "Sp.", "Su.", "Au."]
colors = {"Wi.": "b", "Sp.": "g", "Su.": "r", "Au.": "y"}

# Load day-ahead prices and calculate daily averages
day_ahead = pd.read_csv(file_path, usecols=[1], names=["electricity"])
daily_prices = day_ahead.groupby(np.arange(len(day_ahead)) // 24).mean()  # type ignore


# add column indicating the season of each row. Every 7 days is a new season (Winter, Spring, Summer, Autumn)
daily_prices["season"] = [seasons[i // 7] for i in range(len(daily_prices))]

# Create a grid layout
gs = gridspec.GridSpec(
    2, 1, height_ratios=[3, 1]
)  # 5:1 ratio for main plot to rug plot

plt.gcf().set_size_inches(width / 2.54, height / 2.54)

# Create the main plot for the lines
ax0 = plt.subplot(gs[0])
ax0.plot(x, line["C1"], label="C1")
ax0.plot(x, line["C2"], label="C2")

plt.text(x[0], line["C2"][0], r"$\alpha_0$", fontsize=7, verticalalignment="bottom")


rotation_angle = np.degrees(np.arctan(m["C2"]))

plt.text(
    x[10],
    line["C2"][10],
    r"$\alpha_1$",
    fontsize=7,
    verticalalignment="bottom",
    rotation=rotation_angle,
)

# ensure the xaxis goes from 0 to 70
ax0.set_xlim(0, 65)
ax0.set_ylim(-20, 30)

# grid lines every 10
ax0.grid(which="both", linestyle="--", linewidth=0.5)

ax0.set_ylabel("Waste-heat price (S4) \n [€/MWh]", fontweight="bold")
ax0.legend(loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2, fancybox=True)

# Turn off x-ticks for the top plot
ax0.set_xticks([])

# Create the rug plot in a separate subplot
ax1 = plt.subplot(gs[1])
ax1.set_xlim(ax0.get_xlim())  # Ensure the x-axis is the same as the main plot

# Adding the rug plots by plotting vertical lines at each x position
for season in seasons:
    ax1.plot(
        daily_prices[daily_prices["season"] == season]["electricity"],
        [-8] * len(daily_prices[daily_prices["season"] == season]["electricity"]),
        "|",
        color=colors[season],
        markersize=10,
        markeredgewidth=1,
    )

ax1.set_ylim(-30, 0)

ax1.yaxis.set_tick_params(color="none")
for label in ax1.get_yticklabels():
    label.set_color("none")

ax1.set_ylabel("Occurences\n ", fontweight="bold")
ax1.set_xlabel("Daily mean electricity price [€/MWh]", fontweight="bold")

# add legend to rugplot
ax1.legend(
    seasons,
    loc="lower center",
    bbox_to_anchor=(0.5, 0),
    ncol=len(seasons),
    handlelength=0.5,
    handletextpad=0.5,
    fancybox = True
)

# Show the combined plot with the rug plot in a separate box below
plt.tight_layout()  # Adjust layout for better fit

if save:
    plt.savefig(plot_path, dpi=DPI, bbox_inches="tight")
if show:
    plt.show()
