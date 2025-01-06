# Taxon to Biogeochemical Cycle

A nextflow workflow created to predict functions involving major biogeochemical cycles (carbon, sulfur, nitrogen) for taxonomic affiliations (that can be created from metabarcoding or metagenomic sequencing). It relies on [EsMeCata](https://github.com/AuReMe/esmecata) and [bigecyhmm](https://github.com/ArnaudBelcour/bigecyhmm).

![](tabigecy_diagram.svg)

## Requirements

- [Nextflow](https://www.nextflow.io/docs/latest/install.html): to run `workflow.nf`
- esmecata, bigecyhmm and several python packages for visualisation: this can be done with the following pip command: `pip install esmecata bigecyhmm seaborn pandas plotly kaleido`
- esmecata precomputed database: it can be downloaded from this [Zenodo archive](https://doi.org/10.5281/zenodo.13354073). This precomputed database size is 4 Gb.

## Usage

You can print the help with the following command:

`nextflow run tabigecy.nf --help`

By default, the script will be using files in the directory where the script has been launched. It uses 3 files:
- EsMeCaTa input file.
- EsMeCaTa precomputed database.

Optionally, it can take:
- Abundance file containing the abundance in different samples for the different rows of the EsMeCaTa input file.

At the end, it will create an output folder containing the output folders of EsMeCaTa, the one of bigecyhmm and the visualisation output folder.
To do this on your own file you can specify the input files with the command line:

`nextflow run tabigecy.nf --infile esmecata_input_file.tsv --inAbundfile abundance.tsv --precomputedDB esmecata_database.zip --visualisationScript create_bigecyhmm_plot.py --outputFolder output_folder --coreBigecyhmm 5`

## Output

An output folder (by default called `output_folder`) is created. It contains three subfolders:
- `output_1_esmecata`: the output folder of the `esmecata precomputed` command. For more information, look at [EsMeCaTa readme](https://github.com/AuReMe/esmecata?tab=readme-ov-file#esmecata-outputs).
- `output_2_bigecyhmm`: the output folder of `bigecyhmm` command. For more information, look at [bigecyhmm readme](https://github.com/ArnaudBelcour/bigecyhmm?tab=readme-ov-file#output).
- `output_3_visualisation`: the output folder for the visualisation of the predictions and (if given) the addition of sample abundances. 