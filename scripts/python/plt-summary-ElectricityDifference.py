import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def process_data(file_path):
    data = pd.read_csv(file_path)
    
    # Constants
    BASELINE = 'S0'
    MULTIPLIER = 4
    DIVISOR = 1000

    data['value'] = data['value'] * (MULTIPLIER / DIVISOR)

    # Process data for plotting
    all_f_type_combinations = data['F'].unique()
    baseline_all_combinations = pd.DataFrame(index=all_f_type_combinations, columns=['value']).fillna(0.0).astype('float64')
    baseline_existing_values = data[data['scenario'] == BASELINE].groupby('F')['value'].sum()
    baseline_all_combinations.loc[baseline_existing_values.index, 'value'] = baseline_existing_values
    grouped_data = data.groupby(['scenario', 'F'])['value'].sum()
    diff_from_baseline = grouped_data.unstack().fillna(0).sub(baseline_all_combinations['value'], axis=1).drop(BASELINE, axis=0)

    return diff_from_baseline

# Set font parameters
fontsize = 9
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

output_path = 'M:/J2/results/selected_weeks/consolidated/figures/SummaryElec.png'

# Load and process the data for C1 and C2
file_path_C1 = 'M:/J2/results/selected_weeks/C1/csv/GENERATION_ELEC.csv'
file_path_C2 = 'M:/J2/results/selected_weeks/C2/csv/GENERATION_ELEC.csv'

diff_from_baseline_C1 = process_data(file_path_C1)
diff_from_baseline_C2 = process_data(file_path_C2)

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(15/2.54, 7.5/2.54))

# Plot for C1
diff_from_baseline_C1.plot(kind='bar', stacked=True, ax=axes[0], legend=False)
axes[0].set_title('Case: C1', fontweight='bold', fontsize=fontsize)
# axes[0].set_xlabel('Scenario', fontweight='bold')
axes[0].set_xlabel('')
axes[0].set_ylabel('Electricity production change, \n relative to S0 [GWh/year]', fontweight='bold')
axes[0].set_ylim([-1, 0])
axes[0].grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)

# Plot for C2
diff_from_baseline_C2.plot(kind='bar', stacked=True, ax=axes[1], legend=False)
axes[1].set_title('Case: C2', fontweight='bold', fontsize=fontsize)
# axes[1].set_xlabel('Scenario', fontweight='bold')
axes[1].set_xlabel('')
axes[1].set_ylim([-50, 0])
axes[1].grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

# Add a shared legend
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, fancybox=True, shadow=True, bbox_to_anchor=(0.5, 0.0))
plt.tight_layout(rect=[0, 0.1, 1, 1]) # Adjust layout to make room for the legend

# Show and save the plot
plt.savefig(output_path, dpi=600)
# plt.show()