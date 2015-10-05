# Genome annotation and Pangenome analysis

##### In this demo we will explore how to determine a pangenome from a collection of isolate sequences in fasta format

This demo relies on two pieces of software, Prokka and Roary, so please remember to cite them if you publish results obtained from these tools

# Obtaining data

For details on obtaining Prokka and Roary, please visit their GiHub repos [here](https://github.com/tseemann/prokka/blob/master/README.md) and [here](https://github.com/sanger-pathogens/Roary/blob/master/README.md).

Assuming you have Prokka and Roary installed and in your PATH variable, go ahead and download the four *Listeria monocitogenes* genomes we are going to use for this demo. From the Terminal:

		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000008285.1_ASM828v1_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000021185.1_ASM2118v1_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000026705.1_ASM2670v1_genomic.fna
		wget https://github.com/CBIBUNAB/tutorials/blob/master/genomes/GCA_000196035.1_ASM19603v1_genomic.fna

You should see something like the following:

![genomes](https://github.com/CBIBUNAB/tutorials/blob/master/img/genomes.png)

# Annotating genomes

Now that you have the genomes, we need to annotate them to determine the location and attributes of the genes contained in them. We will use Prokka because it's extremely fast and it performs well, and also becasue the *features* file that produces (GFF3) is compatible with Roary.

		prokka --kingdom Bacteria --outdir prokka_GCA_000008285 --genus Listeria --locustag GCA_000008285 GCA_000008285.1_ASM828v1_genomic.fna

Make sure you annotate the four genomes by replace the -outdir and -locustag and fasta file accordingly. It should take ~ 4 minutes per genome in a standard laptop computer.

# Citation

Seemann T.  
*Prokka: rapid prokaryotic genome annotation*  
**Bioinformatics** 2014 Jul 15;30(14):2068-9.   
[PMID:24642063](http://www.ncbi.nlm.nih.gov/pubmed/24642063)  

Andrew J. Page, Carla A. Cummins, Martin Hunt, Vanessa K. Wong, Sandra Reuter, Matthew T. G. Holden, Maria Fookes, Daniel Falush, Jacqueline A. Keane, Julian Parkhill.   
*Roary: Rapid large-scale prokaryote pan genome analysis*  
**Bioinformatics** 2015 Jul 20. pii: btv421  
[PMID: 26198102](http://www.ncbi.nlm.nih.gov/pubmed/26198102)


