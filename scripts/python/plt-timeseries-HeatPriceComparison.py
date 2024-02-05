import matplotlib.pyplot as plt
import matplotlib
import pandas as pd


fontsize = 9
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

output_path = f"M:/J2/results/selected_weeks/consolidated/figures/HeatPrice-Comparison.png"

title_dict = {
    'x_title': 'Timesteps',
    'y_title_primary': 'Waste-heat price [€/MWh]',
}

DPI = 96
width_cm = 15
height_cm = 5.5

border_xticks_position = [0, 168, 336, 504, 671]
middle_xticks_position = [(border_xticks_position[j] + border_xticks_position[j+1]) / 2 for j in range(len(border_xticks_position) - 1)]
middle_xticks_label = ['Winter', 'Spring', 'Summer', 'Autumn']

cases = ['C1', 'C2']
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(width_cm / 2.54, height_cm / 2.54), sharex=True, sharey=True)

for i, case in enumerate(cases):
    file_path = f'results/selected_weeks/{case}/csv/EHR_PRICE.csv'
    data = pd.read_csv(file_path)
    data = data.pivot_table(index=['T'], columns=['scenario'], values='value', aggfunc='sum', fill_value=0)
    # remove scenario S0
    data = data.drop('S0', axis=1)

    ax = axes[i]
    data.plot(ax=ax, linewidth=1, legend=False)

    # ax.set_xlabel(title_dict['x_title'], fontweight='bold')
    ax.set_xlabel('')
    ax.set_xlim(data.index.min(), data.index.max())

    ax.set_xticks(border_xticks_position)
    ax.set_xticklabels([])
    ax.set_xticks(middle_xticks_position, minor=True)
    ax.set_xticklabels(middle_xticks_label, rotation=0, minor=True)
    ax.tick_params(axis='x', which='minor', length=0)

    # set subplot title
    ax.set_title(f'Case: {case}', fontweight='bold', fontsize = fontsize)

    # ax.set_ylabel(title_dict['y_title_primary'], fontweight='bold')

    # if case == 'C1':
    #     ax.set_ylim(0, 50)
    #     ax.set_yticks([0, 10, 20, 30, 40, 50])
    # elif case == 'C2':
    #     ax.set_ylim(-20, 80)
    #     ax.set_yticks([-20, 0, 20, 40, 60, 80])

    ax.set_ylim(-20,80)
    ax.set_yticks([-20, 0, 20, 40, 60, 80])
    # set grid 
    # ax.grid(which='major', axis='both', linestyle=':', linewidth=0.5)
    ax.grid(axis='y', linestyle='--', alpha=0.5)


fig.text(0.00, 0.5, s=title_dict['y_title_primary'], va='center', ha='center', rotation='vertical', fontweight='bold')


# Create a shared legend below the subplots
lines, labels = axes[-1].get_legend_handles_labels()
# fig.legend(lines, labels, title='Scenario', loc='upper center', ncol=4, bbox_to_anchor=(0.5, 0.0), fancybox=True, shadow=True, title_fontproperties={'weight': 'bold'})
# fig.legend(lines, labels, loc='upper center', ncol=4, bbox_to_anchor=(0.5, 0.0), fancybox=True, shadow=True, title_fontproperties={'weight': 'bold'})
fig.legend(lines, labels, loc='upper center', ncol=4, bbox_to_anchor=(0.5, 0.0), fancybox=True, shadow=True, title_fontproperties={'weight': 'bold'})


# make room for the legend
# fig.subplots_adjust(bottom=0.2)

# Adjust layout
plt.tight_layout()

# Save and show the figure
plt.savefig(output_path, dpi=600, bbox_inches='tight')
# plt.show()