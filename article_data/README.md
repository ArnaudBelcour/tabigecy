# Perform article experiment

The input files used for the article experiments are available in this folder.

`nextflow run tabigecy.nf --infile schwab_et_al_2022.tsv --inAbundfile schwab_et_al_2022_abundance.tsv --coreBigecyhmm xx --precomputedDB /path/to/esmecata_database.zip --outputFolder output_folder_schwab_et_al_2022`

To decrease the runtimes of the workflow, it is advised to give severail cores to `--coreBigecyhmm xx`.