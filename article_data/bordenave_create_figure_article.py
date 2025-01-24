import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

plt.rcParams['figure.figsize'] = [40, 20]
plt.rc('font', size=30)

input_folder = 'output_bordenave'
input_data_df = pd.read_csv('bordenave_et_al_2013_abundance.csv')
proteome_tax_id_file = os.path.join(input_folder, 'output_1_esmecata', '0_proteomes', 'proteome_tax_id.tsv')
bigecyhmm_output = os.path.join(input_folder, 'output_2_bigecyhmm')

observation_names_tax_id_names = {}
observation_names_tax_ids = {}
df_proteome_tax_id = pd.read_csv(proteome_tax_id_file, sep='\t')

for index, row in df_proteome_tax_id.iterrows():
    observation_names_tax_id_names[row['observation_name']] = row['tax_id_name']
    if row['tax_id'] not in observation_names_tax_ids:
        observation_names_tax_ids[row['tax_id']] = [row['observation_name']]
    else:
        observation_names_tax_ids[row['tax_id']].append(row['observation_name'])

input_data_df.set_index('observation_name', inplace=True)
sample_abundance = {}
for col in input_data_df.columns:
    if 'SC' in col:
        sample_abundance[col] = input_data_df[col].to_dict()

abundance_data = {}
sample_tot_abundance = {}
for col in sample_abundance:
    for observation_name in sample_abundance[col]:
        if observation_name in observation_names_tax_id_names:
            tax_id_name = observation_names_tax_id_names[observation_name]
            if col not in abundance_data:
                abundance_data[col] = {}
            if tax_id_name not in abundance_data[col]:
                abundance_data[col][tax_id_name] = float(sample_abundance[col][observation_name])
            else:
                abundance_data[col][tax_id_name] = float(sample_abundance[col][observation_name]) + float(abundance_data[col][tax_id_name])
        tot_abundance = input_data_df[col].sum()
        sample_tot_abundance[col] = tot_abundance

tmp_df = []
cycle_tmp_df = []
data_seaborn = []
data_seaborn_abundance = []
data_stat = {}
annot_folder = 'results'
annot_table_path = os.path.join(bigecyhmm_output, 'function_presence.tsv')
df = pd.read_csv(annot_table_path, sep='\t')
df.set_index('function', inplace=True)
df[annot_folder] = df.sum(axis=1)
df = df[[annot_folder]]
tmp_df.append(df)
cycle_path = os.path.join(bigecyhmm_output, 'Total.R_input.txt')
cycle_df = pd.read_csv(cycle_path, sep='\t', index_col=0, header=None)
cycle_df.columns = ['genome', annot_folder]
for index, row in cycle_df.iterrows():
    if index not in data_stat:
        data_stat[index] = {}
        if annot_folder not in data_stat[index]:
            data_stat[index][annot_folder] = [row[annot_folder]]
        else:
            data_stat[index][annot_folder].append(row[annot_folder])
    else:
        if annot_folder not in data_stat[index]:
            data_stat[index][annot_folder] = [row[annot_folder]]
        else:
            data_stat[index][annot_folder].append(row[annot_folder])
cycle_df = cycle_df[annot_folder]
cycle_tmp_df.append(cycle_df)
for sample in abundance_data:
    function_abundance = {}
    all_tax_ids = []
    tax_id_function = {}
    for tax_id_name in abundance_data[sample]:
        tax_id_name_cycle_path = os.path.join(bigecyhmm_output, 'diagram_input', tax_id_name+'.R_input.txt')
        cycle_df = pd.read_csv(tax_id_name_cycle_path, sep='\t', index_col=0, header=None)
        cycle_df.columns = ['genome']
        if abundance_data[sample][tax_id_name] > 0:
            all_tax_ids.append(tax_id_name)
        for index, row in cycle_df.iterrows():
            if index not in function_abundance:
                function_abundance[index] = row['genome']*abundance_data[sample][tax_id_name]
            else:
                function_abundance[index] = row['genome']*abundance_data[sample][tax_id_name] + function_abundance[index]
            if row['genome']*abundance_data[sample][tax_id_name] > 0:
                if index not in tax_id_function:
                    tax_id_function[index] = [tax_id_name]
                else:
                    if tax_id_name not in tax_id_function[index]:
                        tax_id_function[index].append(tax_id_name)

    for index in function_abundance:
        data_seaborn_abundance.append([index, function_abundance[index]/sample_tot_abundance[sample], sample])
        if index in tax_id_function:
            data_seaborn.append([index, len(tax_id_function[index])/len(all_tax_ids), sample])
        else:
            data_seaborn.append([index, 0, sample])

import plotly.express as px
import pandas as pd


df_seaborn_abundance = pd.DataFrame(data_seaborn_abundance, columns=['name', 'ratio',  'sample'])
print(df_seaborn_abundance)

from plotly.subplots import make_subplots
import plotly.graph_objects as go

specs = [[{'type': 'polar'}]*2]*2
fig = make_subplots(rows=2, cols=2, specs=specs)

removed_functions = ['N-S-10:Nitric oxide dismutase', 'O-S-04:Arsenite oxidation', 'S-S-10:Polysulfide reduction', 'O-S-03:Arsenate reduction', 'O-S-05:Selenate reduction']

kept_functions = [name for name in df_seaborn_abundance['name']
                    if df_seaborn_abundance[df_seaborn_abundance['name']==name]['ratio'].max()>0.1]
row = 1
col = 1
color = ['red', 'blue', 'green', 'purple', 'black']
for sample in sorted(df_seaborn_abundance['sample'].unique()):
    tmp_df_seaborn_abundance = df_seaborn_abundance[df_seaborn_abundance['sample']==sample]
    tmp_df_seaborn_abundance = tmp_df_seaborn_abundance.sort_values(['name'], ascending=False)
    # Remove function
    tmp_df_seaborn_abundance = tmp_df_seaborn_abundance[~tmp_df_seaborn_abundance['name'].isin(removed_functions)]
    tmp_df_seaborn_abundance = tmp_df_seaborn_abundance[tmp_df_seaborn_abundance['name'].isin(kept_functions)]

    # Keep only name of function
    tmp_df_seaborn_abundance['name'] = tmp_df_seaborn_abundance['name'].apply(lambda x: x.split(':')[1])
    #tmp_df_seaborn_abundance = tmp_df_seaborn_abundance[tmp_df_seaborn_abundance['ratio']>0.05]

    fig.add_trace(go.Scatterpolar(
        name = sample,
        r = tmp_df_seaborn_abundance["ratio"],
        theta = tmp_df_seaborn_abundance["name"],
        ), row, col)
    if col < 2:
        col = col + 1
    else:
        col = 1
        row = row + 1

#fig.update_traces(fill='toself')
fig.update_polars(radialaxis=dict(range=[0,1]))
fig.write_image("bordenave_hmm_polar_chart.png", scale=1, width=1600, height=1200)
fig.write_html("bordenave_hmm_polar_chart.html")

kept_functions = [name for name in df_seaborn_abundance['name']
                    if df_seaborn_abundance[df_seaborn_abundance['name']==name]['ratio'].median()>0.1]
kept_df = df_seaborn_abundance[df_seaborn_abundance['sample']=='SC02']
kept_functions = kept_df[kept_df['ratio']>=0.1]['name'].tolist()
kept_df = df_seaborn_abundance[df_seaborn_abundance['sample']=='SC03']
kept_functions.extend(kept_df[kept_df['ratio']>=0.1]['name'].tolist())

df_seaborn_abundance = df_seaborn_abundance.sort_values(['sample', 'name'], ascending=True)
kept_samples = ['SC02', 'SC03']
df_seaborn_abundance = df_seaborn_abundance[df_seaborn_abundance['sample'].isin(kept_samples)]
df_seaborn_abundance = df_seaborn_abundance[df_seaborn_abundance['name'].isin(kept_functions)]
df_seaborn_abundance['name'] = df_seaborn_abundance['name'].apply(lambda x: x.split(':')[1])

fig = px.line_polar(df_seaborn_abundance, r="ratio", theta="name", color="sample", line_close=True)
fig.write_image("bordenave_hmm_polar_chart_line.svg", scale=1, width=1400, height=1200)
