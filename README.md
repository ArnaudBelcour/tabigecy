# TAxon to BIoGEOchemicalCYcle

This is a workflow made to perform a run of EsMeCata, bigecyhmm and visualisation creation using Nextflow.

![](tabigecy_diagram.svg)

## Requirements

- [Nextflow](https://www.nextflow.io/docs/latest/install.html): to run `workflow.nf`
- esmecata, bigecyhmm and visualisation dependencies: this can be done with the following pip command: `pip install esmecata bigecyhmm seaborn pandas plotly kaleido`
- esmecata precomputed database: it can be downloaded from this [Zenodo archive](https://doi.org/10.5281/zenodo.13354073).

## Usage

You can print the help with the following command:

`nextflow run tabigecy.nf --help`

Run the following command:

`nextflow run tabigecy.nf`

By default, the script will be using files in the directory where the script has been launched. It uses 3 files:
- EsMeCaTa input file.
- EsMeCaTa precomputed database.
- Visualisation script (`create_bigecyhmm_plot.py`, that you can find in this repository).

Optionally, it can take:
- Abundance file containing the abundance in different samples for the different rows of the EsMeCaTa input file.

At the end, it will create an output folder in this directory containing the output folders of EsMeCaTa, the one of bigecyhmm and the visualisation output folder.
To do this on your own file you have to modified the associated lines in the nextflow file or you can also specified the input file with the command line:

`nextflow run tabigecy.nf --infile esmecata_input_file.tsv --inAbundfile abundance.tsv --precomputedDB esmecata_database.zip --visualisationScript create_bigecyhmm_plot.py --outputFolder output_folder`

