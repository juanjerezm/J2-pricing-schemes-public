import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

save = True
show = False

fontsize = 8
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

plot_path = f"M:/J2/results/selected_weeks/consolidated/figures/HeatPrice-Comparison.png"

title_dict = {
    'x_title': 'Timesteps',
    'y_title_primary': 'Waste-heat price [€/MWh]',
}

map_colors = ['C0', 'C1', 'C2', 'C5']

DPI = 1200
width_cm = 14
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
    data.plot(ax=ax, linewidth=1, legend=False, color=map_colors)

    # ax.set_xlabel(title_dict['x_title'], fontweight='bold')
    ax.set_xlabel('')
    ax.set_xlim(data.index.min(), data.index.max())

    ax.set_xticks(border_xticks_position)
    ax.set_xticklabels([])
    ax.set_xticks(middle_xticks_position, minor=True)
    ax.set_xticklabels(middle_xticks_label, rotation=0, minor=True)
    ax.tick_params(axis='x', which='minor', length=0)

    # set subplot title
    dc_type = 'Small' if case == 'C1' else 'Large' if case == 'C2' else 'Error'

    ax.set_title(f'{case} - {dc_type} DC', fontweight='bold', fontsize = fontsize)

    ax.set_ylim(-20,80)
    ax.set_yticks([-20, 0, 20, 40, 60, 80])
    # set grid 
    # ax.grid(which='major', axis='both', linestyle=':', linewidth=0.5)
    ax.grid(axis='y', linestyle='--', alpha=0.5)


# Create a shared legend below the subplots
lines, labels = axes[-1].get_legend_handles_labels()
fig.legend(lines, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.5, 0.0), fancybox=True, shadow=False)


plt.tight_layout(rect=[0, 0.10, 1, 1]) # Adjust layout to make room for the legend

if save:
    plt.savefig(plot_path, dpi=DPI, bbox_inches='tight')
if show:
    plt.show()