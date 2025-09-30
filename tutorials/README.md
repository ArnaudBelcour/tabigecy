# Tabigecy tutorial

An explanation of several outputs of Tabigecy and how they can be used. The tutorial also tries to explain some issues that can be encountered when using Tabigecy.

## Input

For this tutorial, semi-artificial data are used:

- `tutorial_example_affiliations.tsv`: input taxonomic affiliations.
- `tutorial_example_abundance.csv`: abundance associated with the taxonomic affiliations for 5 samples.
- `esmecata_database.zip`: esmecata precomputed database can be downloaded from this [Zenodo archive](https://doi.org/10.5281/zenodo.13354073).
- `esmecata_database_phyla.zip`: a secondary esmecata precomputed database made for phyla with fewer sequenced genomes. It can also be downloaded from another Zenodo archive.

This tutorial was made using EsMeCaTa version 0.6.6, bigecyhmm version 0.1.8 and tabigecy version 0.1.2.

The outputs were generated using these two commands:

- `nextflow run ../tabigecy.nf --infile input/tutorial_example_affiliations.tsv --inAbundfile input/tutorial_example_abundance.csv --precomputedDB ../esmecata_database.zip --outputFolder output_folder --coreBigecyhmm 35`

- `nextflow run ../tabigecy.nf --infile input/tutorial_example_affiliations.tsv --inAbundfile input/tutorial_example_abundance.csv --precomputedDB "../esmecata_database.zip ../esmecata_database_phyla.zip" --outputFolder output_folder_2 --coreBigecyhmm 35`

## EsMeCaTa coverage of the samples

A first thing to explore Tabigecy's output is to look at how well the samples are covered by EsMeCaTa.
Tabigecy produces several files that show which taxonomic ranks were used by EsMeCaTa to predict protein contents for the different taxa present in the samples.
The figure located at `output_folder/output_3_visualisation/function_abundance/barplot_esmecata_found_taxon_sample.png` illustrates this information:

![](pictures/1_barplot_esmecata_found_taxon_sample.png)

On the abscissa, each bar corresponds to a sample. The value of the ordinate corresponds to the relative abundance of the organisms present in each sample. The color indicates which taxonomic rank has been used by EsMeCaTa to predict the protein content. Here, in red the genus level and in green the family level. In this example, the four first samples were predicted mostly at the genus and family levels, except for sample 5. Sample 5 has half of its community associated with grey color (indicating that EsMeCaTa was not able to make prediction for the associated organisms).

For the missing predictions, more information can be found in the file `output_folder/output_3_visualisation/function_abundance/barplot_esmecata_missing_organism_sample.tsv`:

| Sample |Organism_name| Taxonomic rank selected by EsMeCaTa |Relative abundance|
|------------------|---------------------|------------------|---------------------|
| S1        | Gracilibacteria       | Not found        | 0.0053475935828877       |
| S3        | Gracilibacteria       | Not found        |     0.0010162601626016261   |
| S4        | Gracilibacteria            | Not found        | 0.002026342451874367            |
| S5        | Gracilibacteria       | Not found        | 0.5338809034907598       |
			
This file shows each organisms that has not been found by EsMeCaTa. In our example, it consists of `Gracilibacteria`. This means that this taxon and its associated higher taxa are not found in the precomputed database.

When using the precomputed database with EsMeCaTa, there is an additional file (located at `output_folder/output_1_esmecata/organism_not_found_in_database.tsv`) showing which organisms were not found.

Missing organisms in the precomputed database can be the result of several points:

- (1) difference between the database that has been used for the taxonomic assignment and the one used by EsMeCaTa. EsMeCaTa relies on the NCBI Taxonomy database, other databases can used different taxon names. You can find the associated taxon names in the [NCBI Taxonomy database](https://www.ncbi.nlm.nih.gov/taxonomy). 
- (2) the taxon can be old or has been replaced by a synonym. EsMeCaTa (by using ete package) should be able to handle several synonyms but not all.
- (3) incorrect version between EsMeCaTa precomputed database and the NCBI taxonomic version. The version of EsMeCaTa precomputed database used in this tutorial (v1) has been generated with NCBI Taxonomy database version `2024-10-01`.
- (4) mismatches between taxon name from NCBI Taxonomy and from UniProt Proteomes databases.
- (5) there was not enough proteomes (by default EsMeCaTa requires at least 5 proteomes) available present in UniProt Proteomes database. To do this, you can search the [UniProt proteomes database](https://www.uniprot.org/proteomes). For example, `Gracilibacteria` is associated with only two proteomes (at the moment of writing this tutorial, it can changed, look [here](https://www.uniprot.org/proteomes?query=taxonomy_name%3DGracilibacteria+AND+%28busco%3A%5B80+TO+*%5D%29)).

Issue 1 is quite difficult to solve without performing a new taxonomic assignment.
Issues 2, 3, 4 can be solved by renaming the taxon so that it matches a taxon name form the database.
Issue 5 requires to run EsMeCaTa with less stringent parameters. A small EsMeCaTa precomputed database has been generated for poorly sequenced phyla (`esmecata_database_phyla`, currently not in a public repository, I am searching a place to drop it).

In our example, there was not enough proteomes for the `Gracilibacteria` taxon so it is not present in the precomputed database. Another precomputed database specific to poorly characterised has been generated and contains this taxon. Tabigecy can combined several precomputed databases with the following command:

`nextflow run ../tabigecy.nf --infile input/tutorial_example_affiliations.tsv --inAbundfile input/tutorial_example_abundance.csv --precomputedDB "../esmecata_database.zip ../esmecata_database_phyla.zip" --outputFolder output_folder_2 --coreBigecyhmm 35`

Tabigecy uses the second database `esmecata_database_phyla` to make predictions for `Gracilibacteria` and this can be seen in the `barplot_esmecata_found_taxon_sample.png` file:

![](pictures/2_barplot_esmecata_found_taxon_sample.png)

Now, half the abundance of sample 5 is associated with phylum `Candidatus Parcubacteria`.

## Function prediction

The predicted functions for the community are present in folder `output_folder/output_2_bigecyhmm` and `output_folder/output_3_visualisation/function_occurrence`.

For major functions of bigoeochemical cycle, their presence in the input organisms are listed in `output_folder/output_3_visualisation/function_occurrence/pathway_presence_in_organism.tsv`:

| function  |C-S-01:Organic carbon oxidation| C-S-02:Carbon fixation |...|
|------------------|---------------------|------------------|---------------------|
| Halomonas        | 1       | 0        | ...       |
| Dethiosulfatibacter        | 1       | 0        |     ...   |
| Methermicoccus        | 1            | 1        | ...            |
| ...        | ...       | ...        | ...       |

There is the same file for the more precise functions in `output_folder/output_3_visualisation/function_occurrence/function_occurrence_in_organism.tsv`. Occurrence of functions are shown in files of `output_folder/output_3_visualisation/function_occurrence`.

There are cycle diagrams showing the occurrence of the functions in all the communities:

![](pictures/3_diagram_carbon_cycle.png)

*Occurence* corresponds to the number of taxa from EsMeCaTa predicted to have the functions and *Percentage* corresponds to the percentage of these taxa among all the communities. If an abundance file is given as input, the percentage is computed according to all organisms present (as row) in the abundance file. Otherwise, the percentage is computed according to the number of organisms processed by bigecyhmm (or EsMeCaTa if an esmecata output folder was given as input).

You can traceback how predictions were made through Tabigecy output files.

First, you need to map your organism name with the taxon used by EsMeCaTa. You can find this mapping in the file `output_folder/output_1_esmecata/0_proteomes/proteome_tax_id.tsv`. The column `observation_name` corresponds to your organism name (`observation_name` of your input file) and EsMeCaTa taxon is in column `tax_id_name`:

| observation_name  |name| tax_id |tax_id_name|...|
|------------------|---------------------|------------------|---------------------|--------------------|
| Halomonas        | Halomonas       | 2745        |Halomonas__taxid__2745| ...       |
| ...        | ...       | ...        | ...|...       |

`Halomonas` is associated with `Halomonas__taxid__2745`.

You can find in file `output_folder/output_2_bigecyhmm/pathway_presence_hmms.tsv` the predicted HMMs associated with major functions for the taxon selected by EsMeCaTa. And you can have the HMM results in folder `output_folder/output_2_bigecyhmm/hmm_results` by seaching for the file associated with EsMeCaTa taxon (`Halomonas__taxid__2745.tsv` for Halomonas). In this file, you have a column indicating the reference HMM and the column `protein` showing the protein ID that is matching.

**pathway_presence_hmms.tsv**:

| pathway  |Halomonas__taxid__2745| ...|
|------------------|---------------------|--------------------|
| C-S-01:Organic carbon oxidation        | K18244.hmm, TIGR00016.hmm, TIGR02717.hmm, TIGR00651.hmm, K00001.hmm, K00840.hmm, TIGR02188.hmm, K03186.hmm, TIGR02821.hmm, K01779.hmm, K00813.hmm, K00123.hmm, K00817.hmm, K22515.hmm, K03381.hmm, K11410.hmm, K02619.hmm, K06445.hmm, K00249.hmm, K00821.hmm, K09456.hmm, K00826.hmm, K09478.hmm, PF02406.hmm, K00255.hmm, K01207.hmm, K06446.hmm, K00831.hmm, K03342.hmm, K00832.hmm, K15980.hmm, K05343.hmm       | ...       |
| ...        | ...       |...       |

**output_folder/output_2_bigecyhmm/hmm_results/Halomonas__taxid__2745.tsv**:

| organism               | protein                          | HMM        | evalue                  | score             | length |
|------------------------|----------------------------------|------------|-------------------------|-------------------|--------|
| Halomonas__taxid__2745 | tr\|A0A369L3R7\|A0A369L3R7_9GAMM | K18244.hmm | 1.4526174542837772e-173 | 572.0691528320312 | 383    |
| ...                    | ...                              | ...        | ...                     | ...               | ...    |

You can find the protein sequences by searching for the protein ID in the fasta files present in `output_folder/output_1_esmecata/1_clustering/reference_proteins_consensus_fasta/`. For example, `Halomonas__taxid__2745.faa` contains all the consensus proteins predicted by EsMeCaTa for *Halomonas*.

**Halomonas__taxid__2745.faa**:

```
>tr|A0A369L3R7|A0A369L3R7_9GAMM Acyl-CoA dehydrogenase OS=Halomonas sp. DQ26W OX=2282311 GN=DU490_10250 PE=3 SV=1
MIRDPELLDQLRDAAHRFAQEELAPHAAEWDEEGHFPREVIREAGEAGFLGIYIPEEYGG
LGLSRLDASLIAEEISRGCSGYTSALTIHNNLVTWMIAHFGTPEQKQRWLPKLASGEWLG
AFALTEPGAGSDAASMKTRAVRDGDGYVLNGSKMWITNGPIADVLVVMARTDPPDSGAGG
ISAFLVPADTPGISYGKIEDKMGWRASPTREISFDDVRVPAENRLGGEEGQGFKYAMKGL
DRGRLGIAACSLGAAQAALDLARDYMLERKQFGRPLAAFQLIQFKLADMQTELDAARLMV
YQAAWRLDQGQPASTEAAMAKRFATEKAFDVADEALQLHGGYGYIREYPVERLYRDARVH
RIYEGTSEIMKLIIARRLLAEVS
```

In the folder `output_folder/output_1_esmecata/1_clustering/computed_threshold/`, you can see, for each taxon, how well conserved the protein is in the different proteomes that were used for the predictions.

**output_folder/output_1_esmecata/1_clustering/computed_threshold/Halomonas__taxid__2745.tsv**:

| representative_protein | cluster_ratio | proteomes |
|------------------------|---------------|--------------------------------------------|
| A0A369L3R7             | 1.0           | UP000235346,UP000004512,UP000327197,... |
| ...                    | ...           | ...  |

This shows that protein cluster A0A369L3R7 was generated from proteins present in all proteomes of *Halomonas*.

## Function abundance computation

The abundance associated with functions predicted by Tabigecy are presented in two ways:

**(1) absolute abundance**: this consists of summing the abundance of organisms predicted to have this function.

```math
F(f,s)=\sum_{i=0}^nA(i)
```

where:
- *F(f,s)* is the absolute abundance of the function f in sample *s*.
- *n* is the number of organisms predicted to have a function *f*.
- *A(i)* is the absolute abundance of organism *i* predicted to have function *f* in sample *s*.

The absolute abundance for each function and sample can be found in the file `output_folder/output_3_visualisation/function_abundance/cycle_abundance_sample_raw.tsv`.

**(2) relative abundance**: this consists of summing the abundance of organisms predicted to have this function and divided it by the total abundance of organisms in the sample.


```math
F(f,s)=\frac{\sum_{i=0}^nA(i)}{A(s)}
```

where:
- *F(f,s)* is the relative abundance of the function *f* in sample *s*. It goes from 0 (function absent in all organisms of the community) to 1 (function present in all organisms of the community).
- *n* is the number of organisms predicted to have function *f*.
- *A(i)* is the absolute abundance of organisms *i* predicted to have function *f*  (from your input file) in sample *s*.
- *A(s)* is the total abundance of organisms in sample *s*.

The relative abundance for each function and sample can be found in the file `output_folder/output_3_visualisation/function_abundance/cycle_abundance_sample.tsv`.

**Example**:

Input abundance file:

| observation_name | sample 1 | sample 2 | sample 3 |
|------------------|----------|----------|----------|
| Cluster_1        | 50       |  400     | 2300     |
| Cluster_2        | 1000     |   56     | 488      |
| Cluster_3        | 2000     |  597     |  20      |
| Cluster_4        | 0        |  1200    | 600      |
| Cluster_5        | 400      |  420     | 380      |
| Cluster_6        | 4858     |  2478    | 1878     |
| Cluster_7        | 1        |  24      |  75      |

Function (file `pathway_presence_in_organism.tsv`):

| observation_name | C-S-01:Organic carbon oxidation | C-S-02:Carbon fixation | C-S-03:Ethanol oxidation |
|------------------|----------|----------|----------|
| Cluster_1        | 1       |  0     | 1     |
| Cluster_2        | 1     |   0     | 1      |
| Cluster_3        | 1     |  1     |  0      |
| Cluster_4        | 0        |  0    | 1      |
| Cluster_5        | 1      |  1     | 0      |
| Cluster_6        | 1     |  1    | 0     |
| Cluster_7        | 1        |  1      |  0      |

Computation of abundance (`cycle_abundance_sample_raw.tsv`):

```
Function absolute abudnance in sample 1:
`C-S-01:Organic carbon oxidation` = 50 + 1000 + 2000 + 400 + 4858 + 1 = 8309

`C-S-02:Carbon fixation` = 2000 + 400 + 4858 + 1 = 7259

`C-S-03:Ethanol oxidation` = 50 + 1000 = 1050
```
| function | sample 1 | sample 2 | sample 3 |
|------------------|----------|----------|----------|
| C-S-01:Organic carbon oxidation        | 8309       |  3975     | 5141     |
| C-S-02:Carbon fixation        | 7259     |   3519     | 2353      |
| C-S-03:Ethanol oxidation        | 1050     |  1056     |  3388      |

Computation of relative abundance (`cycle_abundance_sample.tsv`)

```
Sum abundance:

sample 1 = 50 + 1000 + 2000 + 400 + 4858 + 1 = 8309

sample 2 = 400 + 56 + 597 + 1200 + 420 + 2478 + 24 = 5175

sample 3 = 2300 + 488 + 20 + 600 + 380 + 1878 + 75 = 5741
```
| Function | sample 1 | sample 2 | sample 3 |
|------------------|----------|----------|----------|
| C-S-01:Organic carbon oxidation        | 1       |  0.77     | 0.9     |
| C-S-02:Carbon fixation        | 0.87     |   0.68     | 0.41      |
| C-S-03:Ethanol oxidation        | 0.13     |  0.2     |  0.59      |


These different values can be seen in the diagram figures located at `output_folder/output_3_visualisation/function_abundance/cycle_diagrams_abundance/*_cycle_*.png`, for example with *Sample 1*:

![](pictures/4_S1_carbon_cycle.png)

*Abundance* corresponds to the absolute abundance associated with organisms linked to the functions. *Percentage* corresponds to the relative abundance multiplied by 100.

The relative abundance is also shown in the polar plot `output_folder/output_3_visualisation/function_abundance/polar_plot_abundance_sample_XXX.png`:
Relative abundance goes from 0 to 1 and each function is set on the angular axis.

Sample 1:
![](pictures/5_polar_plot_abundance_sample_S1.png)

Sample 2:
![](pictures/5_polar_plot_abundance_sample_S2.png)

Sample 3:
![](pictures/5_polar_plot_abundance_sample_S3.png)

Sample 4:
![](pictures/5_polar_plot_abundance_sample_S4.png)

Sample 5:
![](pictures/5_polar_plot_abundance_sample_S5.png)