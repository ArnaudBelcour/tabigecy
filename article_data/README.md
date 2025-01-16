# Perform article experiment

The input files used for the article experiments are available in this folder.

## Dataset from Bordenave et al.

A first dataset from the article of [Bordenave et al. (2013)](https://www.sciencedirect.com/science/article/pii/S0964830512002090) was used. The data comes from the Table 2 (a csv file representing this table is available at `original_data/bordenave_et_al_2013_data.csv`).

## Dataset from Schwab et al.

A second dataset was considered from the article of [Schwab et al. (2022)](https://www.sciencedirect.com/science/article/pii/S0360319922017426). To obtain teh taxonomic affiliations, a new taxonomic assignment was made using the reads deposit on the EBI with FROGs pipeline. The full results of FROGS are present in file `original_data/schwab_et_al_2022_data_frogs.tsv`.

## Usage

Each dataset can be used by giving the esmecata input file (either `bordenave_et_al_2013.tsv` or `schwab_et_al_2022.tsv `) to the parameter `--infile` and the abundance file (either `bordenave_et_al_2013_abundance.csv` or `schwab_et_al_2022_abundance.tsv`) to the parameter `--inAbundfile`. The precomputed database is required and can be given with the parameter `--precomputedDB`.

`nextflow run ArnaudBelcour/tabigecy --infile article_data/schwab_et_al_2022.tsv --inAbundfile article_data/schwab_et_al_2022_abundance.tsv --coreBigecyhmm xx --precomputedDB /path/to/esmecata_database.zip --outputFolder output_folder_schwab_et_al_2022`

To decrease the runtimes of the workflow, it is advised to give severail cores to `--coreBigecyhmm xx`. With 5 cores, the runtime of the workflow was around 13 minutes.