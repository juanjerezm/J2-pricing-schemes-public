import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def process_data(file_path):
    data = pd.read_csv(file_path)
    
    # Constants
    BASELINE = 'S0'
    MULTIPLIER = 4
    DIVISOR = 1000

    type_mapping = {
        'HR': 'HR',
        'HO': 'HO',
        'BP': 'CHP',
        'EX': 'CHP',
    }

    data['value'] = data['value'] * (MULTIPLIER / DIVISOR)

    # Rename the TYPE column according to the type_mapping
    data['TYPE'] = data['TYPE'].replace(type_mapping)

    # Combine 'TYPE' (technology type) and 'F' (fuel) into a single column
    data['F_TYPE'] = data['TYPE'] + " - " + data['F']

    # Process data for plotting
    all_f_type_combinations = data['F_TYPE'].unique()
    baseline_all_combinations = pd.DataFrame(index=all_f_type_combinations, columns=['value']).fillna(0.0).astype('float64')
    baseline_existing_values = data[data['scenario'] == BASELINE].groupby('F_TYPE')['value'].sum()
    baseline_all_combinations.loc[baseline_existing_values.index, 'value'] = baseline_existing_values
    grouped_data = data.groupby(['scenario', 'F_TYPE'])['value'].sum()
    diff_from_baseline = grouped_data.unstack().fillna(0).sub(baseline_all_combinations['value'], axis=1).drop(BASELINE, axis=0)

    return diff_from_baseline

# Set font parameters
fontsize = 9
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

output_path = 'M:/J2/results/selected_weeks/consolidated/figures/SummaryCarbon.png'

# Load and process the data for C1 and C2
file_path_C1 = 'M:/J2/results/selected_weeks/C1/csv/CARBON_EMISSIONS.csv'
file_path_C2 = 'M:/J2/results/selected_weeks/C2/csv/CARBON_EMISSIONS.csv'

diff_from_baseline_C1 = process_data(file_path_C1)
diff_from_baseline_C2 = process_data(file_path_C2)

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(15/2.54, 7.5/2.54))

# Plot for C1
diff_from_baseline_C1.plot(kind='bar', stacked=True, ax=axes[0], legend=False)
axes[0].set_title('Case: C1', fontweight='bold', fontsize=fontsize)
axes[0].set_xlabel('Scenario', fontweight='bold')
axes[0].set_ylabel('Change in Carbon Emissions [kton] \n (Relative to S0)', fontweight='bold')
axes[0].set_ylim([-400, 100])
axes[0].grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)

# Plot for C2
diff_from_baseline_C2.plot(kind='bar', stacked=True, ax=axes[1], legend=False)
axes[1].set_title('Case: C2', fontweight='bold', fontsize=fontsize)
axes[1].set_xlabel('Scenario', fontweight='bold')
axes[1].set_ylim([-20000, 5000])
axes[1].grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

# Add a shared legend
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, title='Technology Type - Fuel', title_fontproperties={'weight': 'bold'}, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.0))
plt.tight_layout(rect=[0, 0.2, 1, 1]) # Adjust layout to make room for the legend

# Show and save the plot
plt.savefig(output_path, dpi=600)
# plt.show()