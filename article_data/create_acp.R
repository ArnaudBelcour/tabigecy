library(ade4)
library(corrplot)
library(factoextra)

create_plot_pca <- function(cycle_abundance_path, output_biplot_path, output_corrplot_path, group_filepath){
	# cycle_abundance_path is the "cycle_abundance_samples.tsv" file created by Tabigecy in output_3_visualisation/function_abundance folder.
	cycle_abundance_dataframe <- read.csv(cycle_abundance_path, header=TRUE, sep="\t", row.names="name")

	# Group file.
	group_dataframe <- read.csv(group_filepath, header=TRUE, sep="\t", row.names="sample")

	# Filter cycle pathways by keeping only the one with at least a median of 0.05 in the different samples.
	cycle_abundance_dataframe$median <- apply(cycle_abundance_dataframe, 1, median, na.rm=T)
	cycle_abundance_dataframe <- subset(cycle_abundance_dataframe, as.numeric(median) >= 0.05)
	cycle_abundance_dataframe <- subset(cycle_abundance_dataframe, select = -c(median))

	# Transpose dataframe for PCA.
	cycle_abundance_dataframe_t <- t(cycle_abundance_dataframe)

	# PCA with ade4.
	pca = dudi.pca(cycle_abundance_dataframe_t, scannf = F, nf = 20)

	# Create biplot figure with factoextra.
	g1 <- fviz_pca_biplot(pca,
                col.ind = group_dataframe$group, palette = c('#5ec962', '#440154'),
				col.var = "#2E9FDF", # Variables color
				reple=TRUE,
				labelsize=6,
				mean.point=FALSE
				) +
	theme(text = element_text(size=15),
		axis.title = element_text(size=15),
		axis.text = element_text(size=15))

	ggsave(filename=output_biplot_path, width=15, height=12, g1)

	# Create matrix for corrplot containing the squared coordinates for the cycle functions on the factor map (according to dimensions).
	var <- get_pca_var(pca)
	data_matrix <- matrix(unlist(var$cos2), nrow=length(var$cos2), byrow=TRUE)
	rownames(data_matrix) <- names(var$cos2)
	colnames(data_matrix) <- colnames(cycle_abundance_dataframe_t)

	# Create the correlation plot between PCA dimension and cycle functions.
	png(filename=output_corrplot_path, width=1600, height=1000)
	corrplot(data_matrix)
	dev.off()
}

# Create plot for Bordenave dataset.
print('Create plot for Bordenave dataset')
cycle_abundance_path <- file.path("output_bordenave", "output_3_visualisation", "function_abundance", "cycle_abundance_samples.tsv")
group_filepath <- "bordenave_et_al_2013_group.tsv"
output_biplot_path <- "bordenave_biplot_pca.svg"
output_corrplot_path <- "bordenave_corrplot.png"
create_plot_pca(cycle_abundance_path, output_biplot_path, output_corrplot_path, group_filepath)

# Create plot for Schwab dataset.
print('Create plot for Schwab dataset')
cycle_abundance_path <- file.path("output_schwab", "output_3_visualisation", "function_abundance", "cycle_abundance_samples.tsv")
group_filepath <- "schwab_et_al_2022_sample_grouping.tsv"
output_biplot_path <- "schwab_biplot_acp.svg"
output_corrplot_path <- "schwab_corrplot.png"
create_plot_pca(cycle_abundance_path, output_biplot_path, output_corrplot_path, group_filepath)