import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as ticker

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 9

data_path = "M:/J2/dataset/timeseries_selection.csv"
output_path = "M:/J2/figures/timeseries_selection.png"

data        = pd.read_csv(data_path, skiprows=[1])
labels      = pd.read_csv(data_path, nrows=1)

# Converting the labels to a dictionary for easy access
labels = labels.to_dict(orient='records')[0]

# Converting 'timestep' to a more plot-friendly format
data['timestep'] = data['timestep'].str.replace('T', '').astype(int)

# Creating the subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16/2.54, 10/2.54), sharex=True)

# Plotting 'heat_demand' on the first subplot
data.plot(x='timestep', y='heat_demand', ax=ax1, legend=False, linewidth=0.5)
ax1.set_ylabel(labels['heat_demand'], fontweight='bold')

# Plotting 'electricity_price' on the second subplot
data.plot(x='timestep', y='electricity_price', ax=ax2, legend=False, linewidth=0.5)
ax2.set_ylabel(labels['electricity_price'], fontweight='bold')

# Plotting 'fc_availability' on the third subplot
data.plot(x='timestep', y='fc_availability', ax=ax3, legend=False, linewidth=0.5)
ax3.set_ylabel(labels['fc_availability'], fontweight='bold')

# Highlighting sections where 'selected' is 1
for i in data[data['selected'] == 1]['timestep']:
    ax1.axvspan(i - 0.5, i + 0.5, color='gray', alpha=0.05)
    ax2.axvspan(i - 0.5, i + 0.5, color='gray', alpha=0.05)
    ax3.axvspan(i - 0.5, i + 0.5, color='gray', alpha=0.05)

# Setting x-axis, only for ax2 because they are shared
ax3.set_xlabel('')
ax3.set_xlim([1, 8760])

ax3.xaxis.set_major_locator(ticker.MultipleLocator(730))
ax3.set_xticklabels([], minor=False)

ax3.xaxis.set_minor_locator(ticker.MultipleLocator(365))
ax1.tick_params(axis='x', which='minor', length=0) # I don't know why this is needed
ax2.tick_params(axis='x', which='minor', length=0) # I don't know why this is needed
ax3.tick_params(axis='x', which='minor', length=0)
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ax3.set_xticklabels(month_labels, minor=True)

# Setting first subplot y-axis
ax1.set_ylim([0, 2100])
ax1.set_yticks([0, 300, 600, 900, 1200, 1500, 1800, 2100])
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# Setting second subplot y-axis
ax2.set_ylim([-50, 300])
ax2.set_yticks([-50, 0, 50, 100, 150, 200, 250, 300])
ax2.grid(axis='y', linestyle='--', alpha=0.5)

# Setting third subplot y-axis
ax3.set_ylim([0, 1.2])
ax3.set_yticks([0, 0.5, 1])
ax3.grid(axis='y', linestyle='--', alpha=0.5)

# Adjust general layout
plt.tight_layout()
fig.align_labels()

# Save and show the plot
fig.savefig(output_path, dpi=600)
# plt.show()