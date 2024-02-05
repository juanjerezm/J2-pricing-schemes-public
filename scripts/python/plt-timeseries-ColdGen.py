import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from pathlib import Path

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 9


case = 'C2'
border_xticks_position  = [0, 168, 336, 504, 671]
middle_xticks_position  = [(border_xticks_position[j] + border_xticks_position[j+1]) / 2 for j in range(len(border_xticks_position) - 1)]
middle_xticks_label     = ['Winter', 'Spring', 'Summer', 'Autumn']

# global_xticks_label     = ['T0841', 'T3025', 'T5209', 'T7393', 'T7560']

titles_dict = {
    'x_title':              'Timesteps',
    'y_title_primary':      'DC cooling generation [MWh]',
    'y_title_secondary':    'Waste-heat price [€/MWh]',
}

DPI                     = 96
width_cm                = 15
height_cm               = 2.5

tech_names_mapping = {
    'FC':       'Free cooling',
    'EC':       'Electric chiller',
    'HP_EHR':   'Heat pump'
}

colors = {
    'Free cooling':     'blue',
    'Electric chiller': 'green',
    'Heat pump':        'orange'
}

path_ColdGeneration     = Path(f'M:/J2/results/selected_weeks/{case}/csv/GENERATION_COLD.csv')
path_WasteHeatPrice     = Path(f'M:/J2/results/selected_weeks/{case}/csv/EHR_PRICE.csv')
dir_output              = Path(f'M:/J2/results/selected_weeks/consolidated/figures')
filename_output         = f'ColdGeneration-{case}.png'

# Read data
data_ColdGeneration = pd.read_csv(path_ColdGeneration)
data_WasteHeatPrice = pd.read_csv(path_WasteHeatPrice)

# Rename technology names to be more readable
data_ColdGeneration['TECH'] = data_ColdGeneration['TECH'].replace(tech_names_mapping)

# Determine the number of scenarios
scenarios = data_ColdGeneration['scenario'].unique()
num_scenarios = len(scenarios)

# Create empty lists for the legend
handles, labels = [], []

# Create subplots
fig, axes = plt.subplots(num_scenarios, 1, figsize=(width_cm/2.54, height_cm*num_scenarios/2.54), dpi=96)

for ax, scenario in zip(axes, scenarios):
    # Filter generation data for the scenario and pivot the data for the bar plot
    ScenarioGeneration = data_ColdGeneration[data_ColdGeneration['scenario'] == scenario]
    ScenarioGeneration = ScenarioGeneration.pivot_table(index='T', columns='TECH', values='value', aggfunc='sum', fill_value=0)

    # Create a color list in the same order as the technologies in the pivot table
    techs = ScenarioGeneration.columns
    color_list = [colors[tech] if tech in colors else 'gray' for tech in techs]

    # Plot the bar plot and stack the bars
    ScenarioGeneration.plot(kind='bar', stacked=True, color=color_list, linewidth=0, width=1, alpha=0.7, ax=ax, legend=False)

    # Set titles and labels
    ax.set_title(f"Scenario: {scenario}", fontweight='bold', fontsize=9)
    ax.set_xticks(border_xticks_position)

    # Set y-axis limits and ticks
    if case == 'C1':
        ax.set_ylim([0, 1])
        ax.set_yticks([0, 0.5, 1])
        # ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])

    elif case == 'C2':
        ax.set_ylim([0, 50])
        ax.set_yticks([0, 25, 50])
        # ax.set_yticks([0, 10, 20, 30, 40, 50])
    else:
        raise Exception('Invalid case name')

    # Configure x-axis ticks and labels
    ax.set_xticklabels([])  # Hide tick labels

    if ax != axes[-1]:
        ax.set_xlabel('')   # Hide x.axis title for all but the last subplot
    else:
        ax.set_xlabel(titles_dict['x_title'], fontweight='bold')
        ax.set_xticks(middle_xticks_position, minor=True)   # Set minor ticks at the middle of the seasons
        ax.set_xticklabels(middle_xticks_label, minor=True) # Set labels for the minor ticks
        ax.tick_params(axis='x', which='minor', length=0)   # Make minor ticks invisible

    # Plotting the waste-heat price
    # Filter data for price corresponding to the scenario
    price_data = data_WasteHeatPrice[data_WasteHeatPrice['scenario'] == scenario]

    # if scenario = 'S0', skip the next part of the for loop
    if scenario == 'S0':
        continue

    # Plot the price data
    ax2 = ax.twinx()
    line_handle,  = ax2.plot(price_data['T'], price_data['value'], color='black', label='Waste-heat price')

    if case == 'C1':
        # ax2.set_ylim([0, 60])                       #C1
        # ax2.set_yticks([0, 30, 60])                 #C1
        ax2.set_ylim([0, 50])                       #C1
        ax2.set_yticks([0, 25, 50])                 #C1
        # ax2.set_yticks([0, 10, 20, 30, 40, 50])     #C1
    elif case == 'C2':
        # ax2.set_ylim([-30, 60])                     #C2
        # ax2.set_yticks([-30, 0, 30, 60])    #C2
        ax2.set_ylim([-20, 80])                     #C2
        ax2.set_yticks([-20, 0, 40, 80])    #C2
        # ax2.set_yticks([-20, 0, 20, 40, 60, 80])    #C2


    if case =='C1':
        plot_idx = 1
    elif case == 'C2':
        plot_idx = -1
    else:
        raise Exception('Invalid case name')

    ax2.grid(axis='y', linestyle='--', alpha=0.5)   # Add grid to secondary y-axis

    # Get the legends from the last plot (if not all elements present, it doesn't work)
    if ax == axes[plot_idx]:
        handles, labels = axes[plot_idx].get_legend_handles_labels()   # Get the handles and labels from the first plot
        handles.append(line_handle)                             # Add the line handle
        labels.append(line_handle.get_label())                  # Add the line label


# Set y-axis titles
fig.text(0.00, 0.5, s=titles_dict['y_title_primary'], va='center', ha='center', rotation='vertical', fontweight='bold')
fig.text(1.00, 0.5, s=titles_dict['y_title_secondary'], va='center', ha='center', rotation='vertical', fontweight='bold')

# Place the legend below the last x axis in the figure
# fig.legend(handles, labels, loc='upper center', ncols=4, bbox_to_anchor=(0.5, 0.0), fancybox=True, shadow=True)
# fig.legend(handles, labels, title_fontproperties={'weight': 'bold'}, loc='center left', bbox_to_anchor=(1.01, 0.5), ncol=1, fancybox=True, shadow=True)
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=4, fancybox=True, shadow=True)

# Adjust the layout
plt.tight_layout()

# Save and show the plot
fig.savefig(str(dir_output/filename_output), dpi=600, bbox_inches='tight')
# plt.show()

print(f' >> {case} Finished!')
print( ' >> ------------------------------------')