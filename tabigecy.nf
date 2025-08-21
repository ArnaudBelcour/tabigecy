params.str = 'EsMeCaTa + bigecyhmm + visualisation'

// Set input variables
params.help = false
params.infile = false
params.precomputedDB = false
params.outputFolder = false
params.inAbundfile = false
params.coreBigecyhmm = 1

// Help message
if (params.help) {
    help = """tabigecy.nf version ${params.manifest.version}: ${params.manifest.description}
             |Required arguments:
             |  --infile  Location of the input file. [default: ${params.infile}]
             |  --precomputedDB  Location of esmecata precomputed database (multiple path can be given separated by a space and enclosed by ", for example "path/database_1 path/database_2"). [default: ${params.precomputedDB}]
             |  --outputFolder  Location of the output folder. [default: ${params.outputFolder}]
             |
             |Optional arguments:
             |  --inAbundfile  Location of the abundance file. [default: ${params.inAbundfile}]
             |  --coreBigecyhmm  Number of core for bigecyhmm. [default: ${params.coreBigecyhmm}]
             |  -w            The NextFlow work directory. Delete the directory once the process
             |                is finished [default: ${workDir}]""".stripMargin()
    // Print the help with the stripped margin and exit
    println(help)
    exit(0)
}
else {
    println("""Launch tabigecy version ${params.manifest.version}.""")
}

// Check input required argument.
if (params.infile) {
    input_file_path = Channel.fromPath(params.infile)
}
else{
    println("Missing --infile argument. Add the path to the input file for esmecata. You can see the help with --help for more information.")
    exit(0)
}

if (params.precomputedDB) {
    // Split database paths if there are several and collect them.
    database_paths = params.precomputedDB.split(' ').collect()
    // Create channel for each path and collect them.
    precomputedDB_path = Channel.fromPath(database_paths).collect()
}
else{
    println("Missing --precomputedDB argument. Add the path to esmecata precomputed database. You can see the help with --help for more information.")
    exit(0)
}

if (params.outputFolder) {
    outputFolder_path = Channel.fromPath(params.outputFolder)
}
else{
    println("Missing --outputFolder argument. Add the path to the output folder. You can see the help with --help for more information.")
    exit(0)
}

// Run esmecata on the input file using the precomputed database.
process esmecata {
    input:
        path input_esmecata
        path esmecata_precomputed_db
    output:
        path 'output_1_esmecata', emit: output_1_esmecata, type: "dir"

    publishDir "${params.outputFolder}", mode: 'copy'

    script:
    """
    esmecata precomputed -i ${input_esmecata} -d ${esmecata_precomputed_db} -o output_1_esmecata
    """
}

// Run bigecyhmm on the predictions made by esmecata.
process bigecyhmm {
    input:
        path esmecata_output_folder
        val core_bigecyhmm

    output:
        path 'output_2_bigecyhmm', emit: output_2_bigecyhmm, type: "dir"

    publishDir "${params.outputFolder}", mode: 'copy'

    script:
    """
    bigecyhmm  -i ${esmecata_output_folder}/1_clustering/reference_proteins_consensus_fasta -o output_2_bigecyhmm -c ${core_bigecyhmm}
    """
}

// Create figures from esmecata and bigecyhmm output folders.
process visualisation{
    input:
        val input_abundance_file_path
        path esmecata_output_folder
        path bigecyhmm_output_folder

    output:
        path 'output_3_visualisation', emit: output_3_visualisation, type: "dir"

    publishDir "${params.outputFolder}", mode: 'copy'

    script:
    """
    bigecyhmm_visualisation esmecata --abundance-file ${input_abundance_file_path} --esmecata ${esmecata_output_folder} --bigecyhmm ${bigecyhmm_output_folder} -o output_3_visualisation
    """
}

workflow {
    esmecata(input_file_path, precomputedDB_path)
    bigecyhmm(esmecata.out.output_1_esmecata, params.coreBigecyhmm)

    // Check the presence of abundance file (by default no such file).
    if (params.inAbundfile) {
        input_abundance_file_path = Channel.fromPath(params.inAbundfile)
    }
    else {
        input_abundance_file_path = false
    }

    visualisation(input_abundance_file_path, esmecata.out.output_1_esmecata, bigecyhmm.out.output_2_bigecyhmm)
}