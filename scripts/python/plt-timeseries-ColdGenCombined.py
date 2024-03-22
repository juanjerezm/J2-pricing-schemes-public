import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from pathlib import Path

# save = False
save = True
# show = True
show = False
fontsize = 8
DPI = 1200

width = 15  # cm
height = 14.5  # cm

dir_output              = Path(f'M:/J2/results/selected_weeks/consolidated/figures')
filename_output         = f'ColdGeneration-Combined.png'

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

border_xticks_position  = [0, 168, 336, 504, 671]
middle_xticks_position  = [(border_xticks_position[j] + border_xticks_position[j+1]) / 2 for j in range(len(border_xticks_position) - 1)]
middle_xticks_label     = ['Winter', 'Spring', 'Summer', 'Autumn']

titles_dict = {
    'x_title': 'Timesteps',
    'y_title_primary': 'DC cooling generation [MWh]',
    'y_title_secondary': 'Waste-heat price [€/MWh]',
}

tech_names_mapping = {
    'FC': 'Free cooling',
    'EC': 'Electric chiller',
    'HP_EHR': 'Heat pump'
}

colors = {
    'Free cooling': 'blue',
    'Electric chiller': 'green',
    'Heat pump': 'orange'
}

cases = ['C1', 'C2']

# Create a figure with subplots
num_scenarios = 0  # This will be updated based on the data
for case in cases:

    path_ColdGeneration     = Path(f'M:/J2/results/selected_weeks/{case}/csv/GENERATION_COLD.csv')
    path_WasteHeatPrice     = Path(f'M:/J2/results/selected_weeks/{case}/csv/EHR_PRICE.csv')

    data_ColdGeneration = pd.read_csv(path_ColdGeneration)
    data_WasteHeatPrice = pd.read_csv(path_WasteHeatPrice)

    scenarios = data_ColdGeneration['scenario'].unique()
    num_scenarios = max(num_scenarios, len(scenarios))

fig, axes = plt.subplots(num_scenarios, len(cases), figsize=(width/2.54, height/2.54), dpi=DPI)

handles, labels = [], []
line_handle = []

for case_idx, case in enumerate(cases):

    path_ColdGeneration     = Path(f'M:/J2/results/selected_weeks/{case}/csv/GENERATION_COLD.csv')
    path_WasteHeatPrice     = Path(f'M:/J2/results/selected_weeks/{case}/csv/EHR_PRICE.csv')

    data_ColdGeneration = pd.read_csv(path_ColdGeneration)
    data_WasteHeatPrice = pd.read_csv(path_WasteHeatPrice)
    data_ColdGeneration['TECH'] = data_ColdGeneration['TECH'].replace(tech_names_mapping)

    scenarios = data_ColdGeneration['scenario'].unique()

    for row_idx, scenario in enumerate(scenarios):
        ax = axes[row_idx, case_idx] if num_scenarios > 1 else axes[case_idx]

        ScenarioGeneration = data_ColdGeneration[data_ColdGeneration['scenario'] == scenario]
        ScenarioGeneration = ScenarioGeneration.pivot_table(index='T', columns='TECH', values='value', aggfunc='sum', fill_value=0)
        techs = ScenarioGeneration.columns
        color_list = [colors[tech] if tech in colors else 'gray' for tech in techs]

        ScenarioGeneration.plot(kind='bar', stacked=True, color=color_list, linewidth=0, width=1, alpha=0.7, ax=ax, legend=False)
        ax.set_title(f"{case}-{scenario}", fontweight='bold', fontsize=fontsize)
        ax.set_xticks(border_xticks_position)

        # Set y-axis limits and ticks based on the case
        if case == 'C1':
            ax.set_ylim([0, 1])
            ax.set_yticks([0, 0.5, 1])
        elif case == 'C2':
            ax.set_ylim([0, 50])
            ax.set_yticks([0, 25, 50])
        else:
            raise Exception('Invalid case name')

        ax.set_xticklabels([])

        if row_idx != num_scenarios - 1:
            ax.set_xlabel('')
        else:
            # ax.set_xlabel(titles_dict['x_title'], fontweight='bold')
            ax.set_xlabel('')
            ax.set_xticks(middle_xticks_position, minor=True)
            ax.set_xticklabels(middle_xticks_label, minor=True)
            ax.tick_params(axis='x', which='minor', length=0)

        price_data = data_WasteHeatPrice[data_WasteHeatPrice['scenario'] == scenario]

        if scenario != 'S0':
            ax2 = ax.twinx()
            line_handle, = ax2.plot(price_data['T'], price_data['value'], color='black', label='Waste-heat price', linewidth=0.8)

            if case == 'C1':
                ax2.set_ylim([-20, 80])
                ax2.set_yticks([-20, 0, 40, 80])
            elif case == 'C2':
                ax2.set_ylim([-20, 80])
                ax2.set_yticks([-20, 0, 40, 80])

            ax2.grid(axis='y', linestyle='--', alpha=0.6)

        # if last row_id and case_idx, add legend
        if row_idx == num_scenarios - 1 and case_idx == len(cases) - 1:
            handles, labels = ax.get_legend_handles_labels()
            handles.append(line_handle)
            labels.append(line_handle.get_label()) # type: ignore


fig.text(0.00, 0.5, s=titles_dict['y_title_primary'], va='center', ha='center', rotation='vertical', fontweight='bold')
fig.text(1.00, 0.5, s=titles_dict['y_title_secondary'], va='center', ha='center', rotation='vertical', fontweight='bold')

fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.0), ncol=4, fancybox=True, shadow=False)

# Adjust layout and save the figure
plt.tight_layout(rect=[0, 0.04, 1, 1])

if save:
    fig.savefig(str(dir_output/filename_output), dpi=DPI, bbox_inches='tight')
    print(f' >> Combined plot for C1 and C2 saved to {dir_output/filename_output}')
if show:
    plt.show()