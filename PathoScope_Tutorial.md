# PathoScope Tutorial
-------------------------

![banner](https://raw.githubusercontent.com/ecastron/PS_demo/master/img/banner.png)

##### In this demo we will explore how to get a taxonomic profile from a metagenomic experiment using PathoScope 2.0. A more in-depth tutorial can be found in the **PathoScope** repo [here](https://github.com/PathoScope/PathoScope/raw/master/pathoscope2.0_v0.02_tutorial.pdf)

### What PathoScope can do for you
**PathoScope** is a modular piece of software that will allow you to go all the way from a fastq file to a text file (typically tab-delimited) with columns representing genomes, their proportions, etc.  
There are 6 **PathoScope modules**, however, for this demo we will focus on the three most important ones:
- ***PathoLib*** - Allows user to automatically generate custom reference genome libraries for specific scenarios or datasets
- ***PathoMap*** - Aligns reads to target reference genome library and removes sequences that align to the filter and host libraries
- ***PathoID*** - Reassigns ambiguous reads, identifies microbial strains present in the sample, and estimates proportions of reads from each genome  

Once you run your samples through **PathoScope**, you can easily import the outputfiles into R for downstream exploratory data analysis and statistical inferences.

### PathoScope Dependencies
The only dependencies for **PathoScope** are [*Bowtie2*](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) and [python](https://www.python.org) *2.7.3* or higher. Make sure that both are in your PATH by issuing something like `echo $PATH`

### Installing PathoScope and PS_demo
PathoScope is now hosted in GitHub so you can easily get it by issuing the following command from the Terminal  

		git clone https://github.com/PathoScope/PathoScope.git

And PS_demo

		git clone https://github.com/ecastron/PS_demo.git

### Get data and get reference genomes
We are going to use data from a study exploring microbiome diversity in oropharingeal swabs from schizophrenia patients and healthy controls. The SRA accession number is `SRR1519057`. 

![SRA](https://github.com/ecastron/PS_demo/raw/master/img/img01.png)

This file is probably too big for a demo so I randomly subsampled the reads down to a more manageable size (~40 M to 40 K reads)  
- Go ahead and download the data [here](https://raw.githubusercontent.com/ecastron/PS_demo/master/ES_211.fastq)
- Now you need at least two files, one to be used as target library (where your reads are going to be mapped) and another one to be used as filter library (internal controls, host genome, contaminants, etc. that you want to remove)

As target library, you can use any multi fasta file containing full or draft genomes, or even nucleotide entries from NCBI, and combinations of both. The only condition is that the fasta entries start with the taxonomy ID from NCBI as follows:

Originally:  
\>gi|40555938|ref|NC_005309.1| Canarypox virus, complete genome  

but PathoScope likes:  
\>ti|44088|gi|40555938|ref|NC_005309.1| Canarypox virus, complete genome  

You could do this very easily in **PathoLib**:

		python pathoscope.py LIB -genomeFile my_file.fasta -outPrefix target_library

Alternatively, we provide the entire NCBI nucleotide database already formatted [here] (ftp://pathoscope.bumc.bu.edu/data/nt_ti.fa.gz) (10 GB file). You could also use **PathoLib** to subsample this big file (50 GB uncompressed) and select only the taxa that you want. For instance, obtaining all the virus entries in nt_ti.fa (virus taxonomy ID = 10239)

		python pathoscope.py -LIB python pathoscope.py LIB -genomeFile nt_ti.fa -taxonIds 10239 --subTax -outPrefix virus

Or in order to create a filter library, say all human sequences:
		
		python  pathoscope.py -LIB python pathoscope.py LIB -genomeFile nt_ti.fa -taxonIds 9606 --subTax -outPrefix human

However, I'm providing a target and filter library already formatted that you can download [here](https://www.dropbox.com/sh/3kjvec5lizwmo9l/AAAQmHEAwAfDixGtKC6eTeN1a?dl=0) and [here](https://www.dropbox.com/sh/2gzurlubxkzku0p/AADEIiGDig00FhNpu6XZ2iYaa?dl=0). The target library is a collection of genomes from the reference library of the Human Microbiome Project (description [here](http://hmpdacc.org/HMREFG/)), and the filter library is simply the human genome (hg19). We are also going to use another filter library as well ([phix174](https://www.dropbox.com/sh/9mt2a2v2xdqpj6x/AABgKTPNfwPNO7DpKjo56gdpa?dl=0)) to get rid of all the reads mapping to the Illumina internal control sequence that is sometimes added to sequencing experiments.

### Let's map the reads
Once you have your data and target and filter libraries, we are ready to go ahead with the mapping step. For this we use bowtie2 so we will need to tell **PathoMap** where the bowtie2 indices are. If you don't have bowtie2 indices, not a problem, **PathoMap** will create them for you. And if your fasta files are larger than 4.6 GB (Bowtie2 limit), not a problem either, **PathoMap** will split your fasta files and create indices for each one of the resulting files.

If you have fasta files and not bowtie2 indices:

		python pathoscope.py MAP -U ES_211.fastq -targetRefFiles HMP_ref_ti_0.fa,HMP_ref_ti_1.fa -filterRefFiles human.fa,phix174.fa  -outDir . -outAlign ES_211.sam  -expTag DAV_demo

But if you already have Bowtie2 indices (our case), you can issue the following command:

		python pathoscope.py MAP -U ES_211.fastq -targetIndexPrefixes HMP_ref_ti_0,HMP_ref_ti_1 -filterIndexPrefixes genome,phix174  -outDir . -outAlign ES_211.sam  -expTag DAV_demo

Let's give it a try...

![map](https://github.com/ecastron/PS_demo/raw/master/img/pathomap.png)

So that should have taken ~3 minutes to run. Now you have a number of things that were printed to the screen as well as files that were created. The summary of the STDOUT is:

| Reads Mapped  | Library  | 
|:------------- | ---------------:|
| 1053      | HMP\_ref\_ti\_0 |
| 1132      | HMP\_ref\_ti\_0 |
| 916 | genome |
| 0 | phix174 |

And you should have one .sam file per library, plus another file containing the reads mapped to all target libraries (DAV\_demo-appendAlign.sam), a fastq file of the reads mapping to all targets (DAV\_demo-appendAlign.fq), and the file you most care about: ES_211.sam

![mapout](https://github.com/ecastron/PS_demo/raw/master/img/mapout.png)

### Let's get a taxonomic profile from our .sam file
The last step in our demo is to obtain a taxonomic profile from ES_211.sam using the read reassignment model implemented in **PathoID**

		python pathoscope.py ID -alignFile ES_211.sam -fileType sam -outDir . -expTag DAV -thetaPrior 1000000

After running the command line above, you should get a tab-delimited file with **PathoScope's** output, and an updated .sam file representing an alignment after **PathoScope's** reassignment model was applied.  
If you want to see all the output files you should get, check out the *output_files* directory in the PS\_demo repo.

### Output TSV file format

At the top of the file in the first row, there are two fields called "Total Number of Aligned Reads" and "Total Number of Mapped Genomes". They represent the total number of reads that are aligned and the total number of genomes to which those reads align to in the given alignment file.

Columns in the TSV file:

1. **Genome:**  
This is the name of the genome found in the alignment file.
2. **Final Guess:**  
This represent the percentage of reads that are mapped to the genome in Column 1 (reads aligning to multiple genomes are assigned proportionally) after pathoscope reassignment is performed.
3. **Final Best Hit:**  
This represent the percentage of reads that are mapped to the genome in Column 1 after assigning each read uniquely to the genome with the highest score and after pathoscope reassignment is performed.
4. **Final Best Hit Read Numbers:**  
This represent the number of best hit reads that are mapped to the genome in Column 1 (may include a fraction when a read is aligned to multiple top hit genomes with the same highest score) and after pathoscope reassignment is performed.
5. **Final high confidence hits:**  
This represent the percentage of reads that are mapped to the genome in Column 1 with an alignment hit score of 50%-100% to this genome and after pathoscope reassignment is performed.
6. **Final low confidence hits:**  
This represent the percentage of reads that are mapped to the genome in Column 1 with an alignment hit score of 1%-50% to this genome and after pathoscope reassignment is performed.
7. **Initial Guess:**  
This represent the percentage of reads that are mapped to the genome in Column 1 (reads aligning to multiple genomes are assigned proportionally) before pathoscope reassignment is performed.
8. **Initial Best Hit:**  
This represent the percentage of reads that are mapped to the genome in Column 1 after assigning each read uniquely to the genome with the highest score and before pathoscope reassignment is performed.
9. **Initial Best Hit Read Numbers:**  
This represent the number of best hit reads that are mapped to the genome in Column 1 (may include a fraction when a read is aligned to multiple top hit genomes with the same highest score) and before pathoscope reassignment is performed.
10. **Initial high confidence hits:**  
This represent the percentage of reads that are mapped to the genome in Column 1 with an alignment hit score of 50%-100% to this genome and before pathoscope reassignment is performed.
11. **Initial low confidence hits:**  
This represent the percentage of reads that are mapped to the genome in Column 1 with an alignment hit score of 1%-50% to this genome and before pathoscope reassignment is performed.

### Ready for the next demo?

Let's see an example analysis on data generated in **PathoScope** [here](https://github.com/ecastron/PS_demo/blob/master/demo02.md)