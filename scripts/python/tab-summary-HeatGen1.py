import pandas as pd

CASE = 'C2'
BASELINE = 'S0'
MULTIPLIER = 4

rename_type = {
    'HR': 'Waste-heat recovery',
    'HO': 'Heat-only',
    'BP': 'Cogeneration',
    'EX': 'Cogeneration',
}

# load data
file_path   = f'M:/J2/results/selected_weeks/{CASE}/csv/GENERATION_HEAT.csv'
output_path = f'M:/J2/results/selected_weeks/consolidated/Summary_HeatGen_{CASE}.xlsx'
data_all    = pd.read_csv(file_path)

# Rename and sort the TYPE column
data_all['TYPE'] = data_all['TYPE'].replace(rename_type)
data_all['TYPE'] = pd.Categorical(data_all['TYPE'], categories=["Waste-heat recovery", "Cogeneration", "Heat-only"], ordered=True)
data_all.sort_values(by=['TYPE'], inplace=True)

# Pivot the table
data_all = data_all.pivot_table(index=['scenario'], columns=['F', 'TYPE'], values='value', aggfunc='sum', fill_value=0)*MULTIPLIER

# Calculate diffferences
data_baseline   = data_all.loc[BASELINE]
data_diff       = data_all - data_baseline
data_diff       = data_diff.drop(BASELINE)

# Transpose and rename indexes
data_diff = data_diff.transpose()
data_diff.index.names = ['Fuel', 'Technology type']

# Include the baseline as the first column
data_diff = pd.concat([data_baseline.transpose(), data_diff], axis=1)

# Remove rows with all zeros and round values
data_diff = data_diff.loc[(data_diff != 0).any(axis=1)]
data_diff = data_diff.round(0)

# capitalise the first letter of the first level of multiindex
data_diff.index = data_diff.index.set_levels(data_diff.index.levels[0].str.capitalize(), level=0) # type: ignore

# Add upper column level to highlight references and differences
data_diff.columns = pd.MultiIndex.from_tuples([('Reference [MWh]', BASELINE)] + [('Difference [MWh]', col) for col in data_diff.columns[1:]])

print(data_diff.head(10))  # Display the first few rows of the modified table

# save to excel
data_diff.to_excel(output_path)

