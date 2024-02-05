#%%
import pandas as pd
import pathlib
import os

# Set cwd to the root of the project using pathlib
root = pathlib.Path(__file__).parent.parent.parent
os.chdir(root)

# Constants
CASE = 'C2'
BASELINE = 'S0'
MULTIPLIER = 4
DIVISOR = 1
TYPE = 'CARBON'

if CASE == 'C1' and TYPE == 'CARBON':
    decimal_baseline = 1
    decimal_absolute = 1
    decimal_relative = 2
elif CASE == 'C2' and TYPE == 'CARBON':
    decimal_baseline = 0
    decimal_absolute = 0
    decimal_relative = 2
elif TYPE == 'COST':
    decimal_baseline = 0
    decimal_absolute = 0
    decimal_relative = 2
else:
    raise ValueError(f'Invalid CASE OR TYPE')

# File paths
if TYPE == 'COST':
    DIVISOR = 1
    data_dc_path    = f'M:/J2/results/selected_weeks/{CASE}/csv/DC_NET_COST.csv'
    data_dh_path    = f'M:/J2/results/selected_weeks/{CASE}/csv/DH_NET_COST.csv'
    output_path     = f'M:/J2/results/selected_weeks/consolidated/SUMMARY_COST_{CASE}'

elif TYPE == 'CARBON':
    DIVISOR = 1000
    data_dc_path    = f"M:/J2/results/selected_weeks/{CASE}/csv/CARBON_EMISSIONS_DC_TOTAL.csv"
    data_dh_path    = f"M:/J2/results/selected_weeks/{CASE}/csv/CARBON_EMISSIONS_DH_TOTAL.csv"
    output_path     = f'M:/J2/results/selected_weeks/consolidated/SUMMARY_CARBON_{CASE}'

else:
    raise ValueError(f'Invalid TYPE: {TYPE}')


# Read data
data_dc = pd.read_csv(data_dc_path)
data_dh = pd.read_csv(data_dh_path)

# Rename columns
data_dc = data_dc.rename(columns={'value': 'DC'})
data_dh = data_dh.rename(columns={'value': 'DH'})

# Merge dataframes
data_all = pd.merge(data_dc, data_dh, on=['scenario'])
data_all['TOTAL'] = data_all['DC'] + data_all['DH']
data_all = data_all.set_index('scenario')
data_all = (data_all * MULTIPLIER) / DIVISOR

# Extract baseline data
baseline = data_all.loc[BASELINE]
baseline_data = data_all.loc[[BASELINE]]

# Calculate absolute and relative differences
abs_difference = data_all.sub(baseline, axis='columns').drop(BASELINE)
rel_difference = (data_all - baseline) / (baseline + 1e-9) * 100
rel_difference = rel_difference.drop(BASELINE)

# Define formatting functions
def format_baseline(x, decimals=2):
    return f'{x:.{decimals}f}' if isinstance(x, (int, float)) else x

def format_difference(x, decimals=1, is_relative=False):
    if isinstance(x, (int, float)):
        sign = '+' if x > 0 else ''
        if is_relative:
            return f'{sign}{x:.{decimals}f}%'
        return f'{sign}{x:.{decimals}f}'
    return x

# Apply formatting
baseline_columns = baseline_data.columns
abs_difference[baseline_columns] = abs_difference[baseline_columns].applymap(lambda x: format_difference(x, decimal_absolute))
rel_difference[baseline_columns] = rel_difference[baseline_columns].applymap(lambda x: format_difference(x, decimal_relative, is_relative=True))
baseline_data[baseline_columns] = baseline_data[baseline_columns].applymap(lambda x: format_baseline(x, decimal_baseline))

# Set 'Measure' levels
baseline_data['Measure'] = 'Baseline'
abs_difference['Measure'] = 'Abs. change'
rel_difference['Measure'] = 'Rel. change'

# Combine Measure column and index
baseline_data.set_index('Measure', append=True, inplace=True)
abs_difference.set_index('Measure', append=True, inplace=True)
rel_difference.set_index('Measure', append=True, inplace=True)

# Concatenate dataframes
combined_table = pd.concat([baseline_data, abs_difference, rel_difference])

# Reorder index levels
combined_table = combined_table.reorder_levels(['Measure', 'scenario'])

# Rename index
combined_table.index = combined_table.index.set_names('Scenario', level='scenario')

# Export to CSV
# combined_table.to_csv(output_path + '.csv')

# Export to excel
combined_table.to_excel(output_path + '.xlsx')

# View resulting DataFrame
# combined_table

