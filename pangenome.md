# Genome annotation and Pangenome analysis

##### In this demo we will explore how to determine a pangenome from a collection of isolate genome sequences in fasta format

This demo relies on two pieces of software, *Prokka* and *Roary*, so please remember to cite them if you end up publishing results obtained with these tools

# Obtaining data

For details on obtaining Prokka and Roary, please visit their GiHub repos [here](https://github.com/tseemann/prokka/blob/master/README.md) and [here](https://github.com/sanger-pathogens/Roary/blob/master/README.md).

Assuming you have Prokka and Roary installed and in your PATH variable, go ahead and download the six *Listeria monocytogenes* genomes we are going to use for this demo. From the Terminal:

		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000008285.1_ASM828v1_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000021185.1_ASM2118v1_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000026705.1_ASM2670v1_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000196035.1_ASM19603v1_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000168635.2_ASM16863v2_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000168815.1_ASM16881v1_genomic.fna

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

By annotsating the genomes we mean to add information regarding genes, their location, strandedness, and features and attributes. Now that you have the genomes, we need to annotate them to determine the location and attributes of the genes contained in them. We will use Prokka because it's extremely fast and it performs well, and also becasue the *features* file that produces (GFF3) is compatible with Roary.

		prokka --kingdom Bacteria --outdir prokka_GCA_000008285 --genus Listeria --locustag GCA_000008285 GCA_000008285.1_ASM828v1_genomic.fna

Make sure you annotate the six genomes by replacing the `-outdir` and `-locustag` and `fasta file` accordingly. It should take ~ 4 minutes per genome in a standard laptop computer.

You should end up with 11 files including a .gff file. 

![Prokka output](https://github.com/CBIBUNAB/tutorials/blob/master/img/prokka.png)

GFF files are the input for Roary to compute the pangenome and contain all the annotations plus the genome sequence in fasta format appended at the end.

# Determining the pangenome

Let's put all the .gff files in the same folder (e.g., `./gff`)
		
		roary -p -o ./demo -e -n -v ./gff/*.gff

We already have a phylogeny that represents the evolutionary history of this six isolates

![phylogeny]()

Roary comes with a python script that allows you to generate a few plots to graphically assess your analysis output. Try issuing the following command:

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


