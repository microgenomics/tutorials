# Genome annotation and Pangenome analysis

##### In this demo we will explore how to determine a pangenome from a collection of isolate genome sequences in fasta format

This demo relies on two pieces of software, *Prokka* and *Roary*, so please remember to cite them if you end up publishing results obtained with these tools

# Obtaining data

For details on obtaining Prokka and Roary, please visit their GitHub repos [here](https://github.com/tseemann/prokka/blob/master/README.md) and [here](https://github.com/sanger-pathogens/Roary/blob/master/README.md).

Assuming you have Prokka and Roary installed and in your PATH variable, go ahead and download the six *Listeria monocytogenes* genomes we are going to use for this demo. From the Terminal:
		
		wget https://raw.githubusercontent.com/CBIBUNAB/tutorials/master/genomes/GCA_000008285.1_ASM828v1_genomic.fna
		wget https://raw.githubusercontent.com/CBIBUNAB/tutorials/master/genomes/GCA_000021185.1_ASM2118v1_genomic.fna
		wget https://raw.githubusercontent.com/CBIBUNAB/tutorials/master/genomes/GCA_000026705.1_ASM2670v1_genomic.fna
		wget https://raw.githubusercontent.com/CBIBUNAB/tutorials/master/genomes/GCA_000196035.1_ASM19603v1_genomic.fna
		wget https://raw.githubusercontent.com/CBIBUNAB/tutorials/master/genomes/GCA_000168635.2_ASM16863v2_genomic.fna
		wget https://raw.githubusercontent.com/CBIBUNAB/tutorials/master/genomes/GCA_000168815.1_ASM16881v1_genomic.fna

You should see something like the following:

![genomes](https://github.com/CBIBUNAB/tutorials/blob/master/img/genomes.png)


These genomes correspond to isolates of *L. monocytogenes* reported in *Probing the pan-genome of Listeria monocytogenes: new insights into intraspecific niche expansion and genomic diversification* [PMID: 20846431](http://www.ncbi.nlm.nih.gov/pubmed/?term=20846431).

We selected the following six genomes based on their level of completeness (finished; contigs, etc) and their genotype (type I-III)

| Genome Assembly | Genome Accession |  Genotype  | Sequenced by | Status|
|:------------- | 	--------------- 	| -------------| ------------ | ------------ |
| GCA_000026705	| 	FM242711			| type I      | Institut_Pasteur| Finished|
| GCA_000008285	| 	AE017262			| type I      | TIGR| Finished|
| GCA_000168815	| 	AATL00000000		| type I      | Broad Institute| 79 contigs|
| GCA_000196035 |	AL591824			| type II     | European Consortium| Finished|
| GCA_000168635	| 	AARW00000000		| type II     | Broad Institute | 25 contigs|
| GCA_000021185	| 	CP001175			| type III    | MSU| Finished|

# Annotating genomes

By annotating the genomes we mean to add information regarding genes, their location, strandedness, and features and attributes. Now that you have the genomes, we need to annotate them to determine the location and attributes of the genes contained in them. We will use Prokka because it's extremely fast and it performs well, and also because the *features* file that produces (GFF3) is compatible with Roary.

		prokka --kingdom Bacteria --outdir prokka_GCA_000008285 --genus Listeria --locustag GCA_000008285 GCA_000008285.1_ASM828v1_genomic.fna

Make sure you annotate the six genomes by replacing the `-outdir` and `-locustag` and `fasta file` accordingly. It should take ~ 4 minutes per genome in a standard laptop computer.

You should end up with 11 files including a .gff file. 

![Prokka output](https://github.com/CBIBUNAB/tutorials/blob/master/img/prokka.png)

I'm copying a description of the output files from the Prokka documentation here, but please check with the developers for in-depth documentation.

#### Output Files

| Extension | Description |
| --------- | ----------- |
| .gff | This is the master annotation in GFF3 format, containing both sequences and annotations. It can be viewed directly in Artemis or IGV. |
| .gbk | This is a standard Genbank file derived from the master .gff. If the input to prokka was a multi-FASTA, then this will be a multi-Genbank, with one record for each sequence. |
| .fna | Nucleotide FASTA file of the input contig sequences. |
| .faa | Protein FASTA file of the translated CDS sequences. |
| .ffn | Nucleotide FASTA file of all the annotated sequences, not just CDS. |
| .sqn | An ASN1 format "Sequin" file for submission to Genbank. It needs to be edited to set the correct taxonomy, authors, related publication etc. |
| .fsa | Nucleotide FASTA file of the input contig sequences, used by "tbl2asn" to create the .sqn file. It is mostly the same as the .fna file, but with extra Sequin tags in the sequence description lines. |
| .tbl | Feature Table file, used by "tbl2asn" to create the .sqn file. |
| .err | Unacceptable annotations - the NCBI discrepancy report. |
| .log | Contains all the output that Prokka produced during its run. This is a record of what settings you used, even if the --quiet option was enabled. |
| .txt | Statistics relating to the annotated features found. |

GFF files are the input for Roary to compute the pangenome and contain all the annotations plus the genome sequence in fasta format appended at the end.

# Determining the pangenome

Let's put all the .gff files in the same folder (e.g., `./gff`) and run *Roary*
		
		roary -p -o ./demo -e -n -v ./gff/*.gff

Roary will get all the coding sequences, convert them into protein, and create clusters. Then, using BLASTP and MCL, *Roary* will create clusters, and check for paralogs. Finally, *Roary* will take every isolate and order them by presence/absence of orthologs. The summary output is present in the `summary_statistics.txt` file. In our case, the results are as follows:

Genes| Number
|----|-------|
|Core genes (99% <= strains <= 100%)|	2010|
|Soft core genes (95% <= strains < 99%)| 0|
|Shell genes (15% <= strains < 95%)| 2454|
|Cloud genes (0% <= strains < 15%)|	0|
|Total genes|	4464|

Addiotionally, *Roary* produces a `gene_presence_absence.csv` file that can be opened in any spreadsheet software to manually explore the results. In this file, you will find information such as gene name and gene annotation, and, of course, whether a gene is present in a genome or not.

We already have a phylogeny that represents the evolutionary history of this six isolates, where they form clades according to their genotype, i.e., type I isolates together, and so on.

![phylogeny](https://github.com/CBIBUNAB/tutorials/blob/master/img/core_gene_alignment.tre.png)

*Roary* comes with a python script that allows you to generate a few plots to graphically assess your analysis output. Try issuing the following command:

		python roary_plots.py core_gene_alignment.nwk gene_presence_absence.csv

You should get three files: a pangenome matrix, a frequency plot, and a pie chart. 

![matrix](https://github.com/CBIBUNAB/tutorials/blob/master/img/pangenome_matrix.png)
![frequency](https://github.com/CBIBUNAB/tutorials/blob/master/img/pangenome_frequency.png)
![pie](https://github.com/CBIBUNAB/tutorials/blob/master/img/pangenome_pie.png)





# Citation

Seemann T.  
*Prokka: rapid prokaryotic genome annotation*  
**Bioinformatics** 2014 Jul 15;30(14):2068-9.   
[PMID:24642063](http://www.ncbi.nlm.nih.gov/pubmed/24642063)  

Andrew J. Page, Carla A. Cummins, Martin Hunt, Vanessa K. Wong, Sandra Reuter, Matthew T. G. Holden, Maria Fookes, Daniel Falush, Jacqueline A. Keane, Julian Parkhill.   
*Roary: Rapid large-scale prokaryote pan genome analysis*  
**Bioinformatics** 2015 Jul 20. pii: btv421  
[PMID: 26198102](http://www.ncbi.nlm.nih.gov/pubmed/26198102)


