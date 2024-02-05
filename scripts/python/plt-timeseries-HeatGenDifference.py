import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

fontsize = 9

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

CASE = 'C2'
BASELINE = 'S0'
DPI_SCREEN = 96

width_cm = 15 
height_cm = 2.5

border_xticks_position  = [0, 168, 336, 504, 671]
middle_xticks_position  = [(border_xticks_position[j] + border_xticks_position[j+1]) / 2 for j in range(len(border_xticks_position) - 1)]
middle_xticks_label     = ['Winter', 'Spring', 'Summer', 'Autumn']

title_dict = {
    'x_title':              'Timesteps',
    'y_title_primary':      'Difference in heat generation [MWh] \n (Relative to scenario "S0")',
}

## Add modifying data here
category = 'Technology type - Fuel'

type_mapping = {
    'HR':   'HR',
    'HO':   'HO',
    'BP':   'CHP',
    'EX':   'CHP',
}

# Load the data from the CSV file
file_path   = f'M:/J2/results/selected_weeks/{CASE}/csv/GENERATION_HEAT.csv'
output_path = f'M:/J2/results/selected_weeks/consolidated/figures/HeatGeneration-{CASE}.png'

data = pd.read_csv(file_path)

# Rename the TYPE column to according to the type_mapping
data['TYPE'] = data['TYPE'].replace(type_mapping)

# Create a column that contains type - fuel combinations
data[category] = data['TYPE'] + ' - ' + data['F']

pivoted_data = data.pivot_table(index=['scenario', 'T'], columns=[category], values='value', aggfunc='sum', fill_value=0)

reference_data = pivoted_data.loc['S0']
data = pivoted_data.drop('S0')

# Calculate the difference between the rest_data and reference_data
difference_data = data - reference_data

# Get the unique scenarios from the difference_data
scenarios = difference_data.index.get_level_values('scenario').unique()

# Create a figure with subplots for each scenario
fig, axes = plt.subplots(len(scenarios), 1, figsize=(width_cm/2.54, height_cm*len(scenarios)/2.54), dpi=DPI_SCREEN, sharey=True)

unique_categories = []

# Iterate over each scenario and plot the stacked bar chart
for ax, scenario in zip(axes, scenarios):
    # Get the data for the current scenario
    scenario_data = difference_data.loc[scenario]

    # store in list the unique values of 'Type-F'
    unique_categories.append(scenario_data.columns.get_level_values(category).unique())

    scenario_data.plot(kind='bar', stacked=True, ax=ax, linewidth=0, width=1, alpha=0.7, legend=False)

    # Configure title
    ax.set_title(f"Scenario: {scenario}", fontweight='bold', fontsize=fontsize)

    # Configure x-axiws
    ax.set_xticks(border_xticks_position)   # Set xticks at the borders of the seasons
    ax.set_xticklabels([])                  # No labels for these xticks
    if scenario != scenarios[-1]:
        ax.set_xlabel('')
    else:
        ax.set_xlabel(title_dict['x_title'], fontweight='bold')
        ax.set_xticks(middle_xticks_position, minor=True)   
        ax.set_xticklabels(middle_xticks_label, rotation = 0, minor=True)
        ax.tick_params(axis='x', which='minor', length=0)

# configure y-axis
if CASE == 'C1':
    axes[-1].set_ylim([-1.6, 1.6])
    axes[-1].set_yticks([-1.6, -0.8, 0.0, 0.8, 1.6])
elif CASE == 'C2':
    axes[-1].set_ylim([-80, 80])
    axes[-1].set_yticks([-80, -40, 0, 40, 80])

fig.text(0.00, 0.5, s=title_dict['y_title_primary'], va='center', ha='center', rotation='vertical', fontweight='bold')

# Add a legend
# Check if all Index objects are identical. If so, the legend items of each subplot are identical and the legend of any subplot can be used.
# If this is not the case, good luck with creating a legend.
identical_legends = all(unique_categories[0].equals(index) for index in unique_categories)
if identical_legends:
    print(' >> Legends are identical, using the legend of the first subplot')
else:
    raise Exception(' >> Legends are not identical, cannot create a legend') 

handles, labels = axes[0].get_legend_handles_labels()

# fig.legend(handles, labels, title=category, title_fontproperties={'weight': 'bold'}, loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=3, fancybox=True, shadow=True)
fig.legend(handles, labels, title=category, title_fontproperties={'weight': 'bold'}, loc='center left', bbox_to_anchor=(1.0, 0.5), ncol=1, fancybox=True, shadow=True)


# Adjust the spacing between subplots
plt.tight_layout()

# Save and show the figure
plt.savefig(output_path, dpi=600, bbox_inches='tight')
# plt.show()

print(f' >> {CASE} Finished!')
print( ' >> ------------------------------------')