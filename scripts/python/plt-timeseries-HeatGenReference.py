# import matplotlib.pyplot as plt
# import matplotlib
# import pandas as pd

# fontsize = 9

# matplotlib.rcParams['font.family'] = 'Times New Roman'
# matplotlib.rcParams['font.size'] = fontsize

# CASE = 'C2'  # C2 or C1 both work and produce the same result
# BASELINE = 'S0'  # Interested only in reference scenario
# DPI_SCREEN = 96
# DPI_PRINT = 600

# width_cm = 15
# height_cm = 5

# border_xticks_position = [0, 168, 336, 504, 671]
# middle_xticks_position = [(border_xticks_position[j] + border_xticks_position[j+1]) / 2 for j in range(len(border_xticks_position) - 1)]
# middle_xticks_label = ['Winter', 'Spring', 'Summer', 'Autumn']

# title_dict = {
#     'x_title': 'Timesteps',
#     'y_title_primary': 'Difference in heat generation [MWh] \n (Relative to scenario "S0")',
# }

# category = 'Technology type - Fuel'

# type_mapping = {
#     'HR': 'HR',
#     'HO': 'HO',
#     'BP': 'CHP',
#     'EX': 'CHP',
# }

# # Load the data from the CSV file
# file_path = f'M:/J2/results/selected_weeks/{CASE}/csv/GENERATION_HEAT.csv'
# secoond_path = r'm:\J2\results\selected_weeks\C2\MCH.csv'
# output_path = f'M:/J2/results/selected_weeks/consolidated/figures/HeatGeneration-{CASE}.png'

# data_heat = pd.read_csv(file_path)
# data_MCH = pd.read_csv(secoond_path)

# # Rename the TYPE column according to the type_mapping
# data_heat['TYPE'] = data_heat['TYPE'].replace(type_mapping)

# # Create a column that contains type - fuel combinations
# data_heat[category] = data_heat['TYPE'] + ' - ' + data_heat['F']

# data_heat = data_heat[data_heat['scenario'] == BASELINE]
# data_heat = data_heat.pivot_table(index=['T'], columns=[category], values='value', aggfunc='sum', fill_value=0)

# ax = data_heat.plot(kind='bar', stacked=True, linewidth=0, width=1, alpha=0.7, legend=False, figsize=(width_cm / 2.54, height_cm / 2.54))

# # Configure x-axis
# ax.set_xticks(border_xticks_position)   # Set xticks at the borders of the seasons
# ax.set_xticklabels([])                  # No labels for these xticks
# # ax.set_xlabel(title_dict['x_title'], fontweight='bold')
# ax.set_xticks(middle_xticks_position, minor=True)
# ax.set_xticklabels(middle_xticks_label, rotation=0, minor=True)
# ax.tick_params(axis='x', which='minor', length=0)

# # Configure y-axis
# # ax.set_ylim(0, 2100)
# # ax.set_yticks([0, 300, 600, 900, 1200, 1500, 1800, 2100])
# # 0 to 2100 every 700
# ax.set_ylim(0, 2100)
# ax.set_yticks([0, 700, 1400, 2100])

# ax.set_ylabel(title_dict['y_title_primary'])

# # Add gridlines
# ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)

# # Add legend
# handles, labels = ax.get_legend_handles_labels()
# ax.legend(handles, labels, title=category, title_fontproperties={'weight': 'bold'}, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fancybox=True, shadow=True)

# # Plot data_MCH as a line on the secondary axis
# ax2 = ax.twinx()
# data_MCH.plot(kind='line', ax=ax2, linewidth=1, alpha=0.7, legend=False, color='black')

# # config secondary yaxis
# # ticks -30 to 60, every 30
# ax2.set_ylim(-30, 90)
# ax2.set_yticks([-30, 0, 30, 60])

# # ax2.set_ylim(-20, 60)
# # ax2.set_yticks([-20, 0, 20, 40, 60])
# ax2.set_ylabel('MCH [kton]', fontweight='bold', color='black')

# plt.show()

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

save = True
show = False

fontsize = 8
width = 14  # cm
height = 9 # cm # Increased to accommodate two plots


matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

CASE = 'C2'  # C2 or C1 both work and produce the same result
BASELINE = 'S0'  # Interested only in reference scenario
DPI = 1200

border_xticks_position = [0, 168, 336, 504, 671]
middle_xticks_position = [(border_xticks_position[j] + border_xticks_position[j+1]) / 2 for j in range(len(border_xticks_position) - 1)]
middle_xticks_label = ['Winter', 'Spring', 'Summer', 'Autumn']

title_dict = {
    'x_title': 'Timesteps',
    'y_title_primary': 'DH generation \n [MWh]',
    'y_title_secondary': 'DH marginal cost \n [€/MWh]'
}

category = 'Technology type - Fuel'

type_mapping = {
    'HR': 'HR',
    'HO': 'HO',
    'BP': 'CHP',
    'EX': 'CHP',
}

# Load the data from the CSV file
file_path = f'M:/J2/results/selected_weeks/{CASE}/csv/GENERATION_HEAT.csv'
secoond_path = r'm:\J2\results\selected_weeks\C2\MCH.csv'
plot_path = f'M:/J2/results/selected_weeks/consolidated/figures/HeatGenerationReference.png'

data_heat = pd.read_csv(file_path)
data_MCH = pd.read_csv(secoond_path)

# Rename the TYPE column according to the type_mapping
data_heat['TYPE'] = data_heat['TYPE'].replace(type_mapping)

# Create a column that contains type - fuel combinations
data_heat[category] = data_heat['TYPE'] + ' - ' + data_heat['F']

data_heat = data_heat[data_heat['scenario'] == BASELINE]
data_heat = data_heat.pivot_table(index=['T'], columns=[category], values='value', aggfunc='sum', fill_value=0)

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(width / 2.54, height / 2.54), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# Plotting the heat generation data
data_heat.plot(kind='bar', stacked=True, linewidth=0, width=1, alpha=0.7, legend=False, ax=ax1)

# Configure x-axis for top plot (ax1)
ax1.set_xticks(border_xticks_position)  # Set xticks at the borders of the seasons
ax1.set_xticklabels([])  # No labels for these xticks
ax1.set_xticks(middle_xticks_position, minor=True)
ax1.set_xticklabels(middle_xticks_label, rotation=0, minor=True)
ax1.tick_params(axis='x', which='minor', length=0)
ax1.set_ylabel(title_dict['y_title_primary'], fontweight='bold')

# Configure y-axis for top plot
ax1.set_ylim(0, 2100)
ax1.set_yticks([0, 700, 1400, 2100])
ax1.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)

# Add legend to the top plot
handles, labels = ax1.get_legend_handles_labels()

# Plotting the data_MCH in the bottom plot (ax2)
data_MCH.plot(kind='line', ax=ax2, linewidth=1, legend=False, color='black')

# Configure x-axis for bottom plot (ax2)
ax2.set_xticks(border_xticks_position)  # Set xticks at the borders of the seasons
# ax2.set_xticklabels(middle_xticks_label, rotation=0)
# ax2.set_xlabel(title_dict['x_title'], fontweight='bold')
ax2.set_xlabel('')

# Configure y-axis for bottom plot
ax2.set_ylim(-35, 70)
ax2.set_yticks([-35, 0, 35, 70])
ax2.set_ylabel(title_dict['y_title_secondary'], fontweight='bold')
ax2.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)

#fig.legend(handles, labels, title=category, title_fontproperties={'weight': 'bold'}, loc='lower center', bbox_to_anchor=(0.5, 0), ncol=3, fancybox=True, shadow=True)
fig.legend(handles, labels, title=category, title_fontproperties={'weight': 'bold'}, loc='lower center', bbox_to_anchor=(0.55, 0), ncol=3, fancybox=True, shadow=False)

plt.tight_layout(rect=[0, 0.20, 1, 1]) # Adjust layout to make room for the legend

if save:
    plt.savefig(plot_path, dpi=DPI, bbox_inches='tight')
if show:
    plt.show()
