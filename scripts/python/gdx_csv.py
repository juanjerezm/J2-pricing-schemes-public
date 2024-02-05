import gams.transfer as gt
from pathlib import Path
import pandas as pd


case = 'C2'
scenario_names = ['S0', 'S1', 'S2', 'S3', 'S4']

input_path = Path(r'results\selected_weeks')
output_path = Path(r'results\selected_weeks')

# recreate "paths" from "input_path" and "scenario_names" and "case"
paths = [input_path / case / f'selected_weeks_{case}_{scenario}.gdx' for scenario in scenario_names]

# read gdx files into containers
containers = [gt.Container(str(path)) for path in paths]

# make data a dict with scenanrio names as keys and containers as values
data_all = dict(zip(scenario_names, containers))

# get all parameters in the first container
parameters = containers[0].listParameters()
parameters[:] = [item for item in parameters if item.startswith("OUT_")]

for parameter in parameters:

    df_par = pd.DataFrame()
    for scenario, container in data_all.items():
        df = container[parameter].records #type: ignore

        # remove suffix to column names
        cols = [i[0] for i in df.columns.str.rsplit("_", n=1)]
        df.columns = cols

        # add scenario column and move it to the front
        df['scenario'] = scenario
        cols = ['scenario'] + [col for col in df.columns if col != 'scenario']
        df = df[cols]

        # append scenario data to df_par
        df_par = pd.concat([df_par, df])

    # set everything except 'value' as index
    columns = [item for item in df_par.columns.tolist() if item != 'value']
    df_par.set_index(columns, inplace=True)

    csv_name = parameter.replace('OUT_', '')

    # make directory if it does not exist
    final_path = output_path / case / 'csv'
    final_path.mkdir(parents=True, exist_ok=True)
    df_par.to_csv(final_path / f'{csv_name}.csv')

