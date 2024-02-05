import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

fontsize = 9
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = fontsize

# Load the data
file_path = 'M:/J2/results/selected_weeks/C1/csv/CARBON_EMISSIONS.csv'
data = pd.read_csv(file_path)

# Constants
BASELINE = 'S0'
MULTIPLIER = 4
DIVISOR = 1000

type_mapping = {
    'HR':   'HR',
    'HO':   'HO',
    'BP':   'CHP',
    'EX':   'CHP',
}

width_cm = 15
height_cm = 7

data['value'] = data['value']*(MULTIPLIER/DIVISOR)

# Rename the TYPE column to according to the type_mapping
data['TYPE'] = data['TYPE'].replace(type_mapping)


# Combine 'TYPE' (technology type) and 'F' (fuel) into a single column
data['F_TYPE'] = data['TYPE'] + " - " + data['F']

# Get a list of all unique fuel-technology type combinations
all_f_type_combinations = data['F_TYPE'].unique()

# Create a DataFrame for baseline with all combinations, filled with zeros and dtype set to float64
baseline_all_combinations = pd.DataFrame(index=all_f_type_combinations, columns=['value']).fillna(0.0).astype('float64')

# Update the baseline values for combinations that exist in the baseline scenario
baseline_existing_values = data[data['scenario'] == BASELINE].groupby('F_TYPE')['value'].sum()
baseline_all_combinations.loc[baseline_existing_values.index, 'value'] = baseline_existing_values

# Group by scenario and fuel-technology type, then sum the values
grouped_data = data.groupby(['scenario', 'F_TYPE'])['value'].sum()

# Compute the differences compared to the baseline for each scenario and fuel-technology type
diff_from_baseline = grouped_data.unstack().fillna(0).sub(baseline_all_combinations['value'], axis=1)

# Remove baseline scenario from the data to be plotted
diff_from_baseline = diff_from_baseline.drop(BASELINE, axis=0)

# Plotting
diff_from_baseline.plot(kind='bar', stacked=True, figsize=(width_cm/2.54, height_cm/2.54))

plt.xlabel('Scenario', fontweight='bold')
plt.ylabel('Difference in Carbon Emissions [kton]', fontweight='bold')
plt.legend(title='Technology Type - Fuel', title_fontproperties={'weight': 'bold'}, bbox_to_anchor=(1.01, 0.5), loc='center left', fancybox=True, shadow=True)
plt.xticks(rotation=0)
plt.tight_layout()

# Add y grid
plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)

# Show and save the plot
plt.show()
plt.savefig('M:/J2/results/selected_weeks/consolidated/plot.png')
