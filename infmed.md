# Laboratorio de Genómica para Informática Médica
-
La actividad del día de hoy consiste en ganar experiencia directa con datos de secuenciamiento masivo y algunos pasos básicos para transformar esos datos en información biológica útil.  

Vamos a trabajar directamente con reads producidas en un equipo Illumina [HiSeq 2500](http://www.illumina.com/systems/hiseq_2500_1500.html). Las reads corresponden a un genoma de *Escherichia coli* aislado de un paciente con una infección del tracto urinario. Un punto esencial para tratar este tipo de infección, es saber si existen genes de resistencia a antibióticos presentes en el genoma y en contra de qué antibióticos actuan.  

Échemos un vistazo a la estructura del genoma de [*E. coli*](http://www.ncbi.nlm.nih.gov/genome/?term=escherichia%20coli).  

		¿Cuántos genes tiene?
		¿Cuál es la longitud del genoma?
		¿Cuál es el %GC?

Éstas estadísticas nos van a ayudar a comparar nuestro genoma una vez ensamblado con "lo que deberíamos obtener". Ahora, en resumen lo que vamos a hacer hoy es:  

* Descargar y comprobar la calidad de las reads usando el programa [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/download.html).  
* Ensamblar el genoma usando el método de [De Bruijn Graphs](http://www.nature.com/nbt/journal/v29/n11/pdf/nbt.2023.pdf) implementado en el programa [SPAdes](http://bioinf.spbau.ru/spades).  
* Evaluar y comparar el ensamble al genoma de referencia de *E. coli* usando el servidor web [QUAST](http://quast.bioinf.spbau.ru).
* Navegar a través de los contigs y anotaciones para buscar un gen de resistencia a Beta Lactamas o betalatamasas (penicilinas, cefalosporinas, carbapenemas, y monobactamos) en el visualizador [GeneiousBasic](http://www.geneious.com/download).
* Finalmente, haremos una exploración de la estructura tridimensional de una beta lactamasa y cómo su estructura es similar en diferentes organismos.   

Para empezar, descarguemos las reads tal cual son entregadas por el secuenciador ([aquí](https://www.dropbox.com/s/7gh1343s4yk0rsf/reads.zip?dl=0)). Alternativamente, las pueden encontrar en sus estaciones de trabajo (en el Escritorio en el directorio **CURSO_22SEPT**).

Exploremos la calidad de las reads en FastQC

![fastqc](https://github.com/microgenomics/tutorials/raw/master/img/Screenshot%202016-09-21%2023.00.22.png)  

		Explora el significado del gráfico y qué es lo que está expresado en el eje Y.  
		¿Qué indica la información en "overrrepresented sequences" o "Kmer content"?

En general, un investigador tomaría una desición con respecto a cómo cortar y/o filtrar las reads que no se ajusten a algún estándar. Esta decisión es muchas veces arbitraria y depende de qué tan bien se siente el investigador trabajando sobre el conjunto de reads que pasaron el control de calidad.  

Ahora, necesitamos usar la línea de comandos para poder ensamblar este genoma. Observen que las reads vienen en dos archivos porque corresponden a `Paired-end reads`. Busquen en la Mac el ícono de la Terminal. Al ejecutar la Terminal deberán ver una ventana como la siguiente:  

![terminal](https://github.com/microgenomics/tutorials/raw/master/img/term.png)

Si no están familiarizados con la Terminal, les recomiendo revisar las lecciones del sitio web de [Data Carpentry](http://www.datacarpentry.org), en particular la lección sobre el [Shell](http://www.datacarpentry.org/shell-genomics/lessons/01_the_filesystem.html).

Ahora, al escribir `spades.py` debería ejecutarse el ensamblador SPAdes y mostrarnos el menú de ayuda:

![spades](https://github.com/microgenomics/tutorials/raw/master/img/spades.png)

Inspeccionemos las opciones. Como mínimo, necesitamos entregarle el nombre y ubicación de los archivos de entrada (las reads), donde dejar los resultados (output directory) y cómo proceder con el ensamblaje.

		spades.py -o ensamblaje -1 Escherichia_coli_GW_UTI_007_TCTCTTCA-TAACGCTG_L005_R1_001.fastq -2 Escherichia_coli_GW_UTI_007_TCTCTTCA-TAACGCTG_L005_R2_001.fastq -t 8 -m 4 --cov-cutoff auto

El ensamblaje en total debería tomar aproximadamente 5 a 10 minutos. El archivo resultante que nos interesa se llama `contigs.fasta` el cual es un archivo de texto plano en [formato fasta](https://en.wikipedia.org/wiki/FASTA_format) que contiene secuencias contiguas que fueron formadas a partir de sobreponer las reads unas con otras.

Veamos cuántos contigs se formaron y cuál fue la longitud total del genoma ensamblado. Vamos a la página de [QUAST](http://quast.bioinf.spbau.ru) y subamos nuestro archivo `contigs.fasta`.

![quast](https://github.com/microgenomics/tutorials/raw/master/img/quast.png)

La ejecución de QUAST debería tomar 10 minutos aproximadamente. Una vez finalizado, inspecciona la página de resultados.

		¿Qué es el N50?
		¿Cuál es la longitud de nuestro genoma?
		¿Cuántos genes tiene en comparación con la referencia? ¿Su contenido GC?

Una vez finalizado QUAST y la inspección de los resultados, podemos continuar con la anotación del genoma. Anotar un genoma tiene que ver con identificar dónde están los genes, qué hacen, y en qué proceso metabólico están involucrados. Vamos a usar un programa que usa una combinación de búsquedas por similitud y *ab initio*. El programa se llama [Prokka](https://github.com/tseemann/prokka) y fue desarrollado por un investigador australiano, [Torsten Seemann](https://twitter.com/torstenseemann).

Desde la Terminal ejecutemos Prokka al escribir `prokka`

![prokka](https://github.com/microgenomics/tutorials/raw/master/img/prokkaterm.png)

Al igual que con SPAdes, necesitamos indicarle a prokka cómo procesar nuestro archivo con contigs, qué bases de datos usar, y como realizar los cálculos.

		prokka --outdir anotación --prefix EColi --addgenes --locustag Ecoli --genus Escherichia --species coli --kingdom Bacteria --gram neg --cpus 16 --evalue 1e-5 contigs.fasta

El proceso completo debería tomar 10 minutos aproximadamente. Una vez terminado, Prokka va a haber generado 11 archivos de salida, e.g., .gbk, .fna, .faa, .ffn, etc.

		¿Qué información contienen estos archivos?

Ahora carguemos el archivo .gbk en Geneious. Deberíamos ver algo como la siguiente imagen:

![geneious](https://github.com/microgenomics/tutorials/raw/master/img/geneious.png)

Geneious es una herramienta muy poderosa donde podemos explorar de manera gráfica los resultados del proceso de anotación genómica. Exploremos de manera libre las herramientas y opciones que provee Geneious. En la esquina superior derecha pueden escoger e ir navegando contig por contig y explorando las anotaciones que fueron agregadas a la secuencia de DNA.

Vayamos a la pestaña de Annotations y seleccionemos All Sequences en la esquina superior izquierda. Luego podemos buscar anotaciones específicas a través de todos los contigs. Probemos con "Lactam"

![lactam](https://github.com/microgenomics/tutorials/raw/master/img/lactam.png)

En el contig 74 (NODE_74) hay una secuencia codificante *bla 1 CDS* de 876 nucleótidos de longitud que está codificada en la posición Reverse de la secuencia. Seleccionemos este resultado y vayamos a Sequence View de nuevo.

![lactam2](https://github.com/microgenomics/tutorials/raw/master/img/lactam2.png)

El producto génico de esta CDS es una "Beta-lactamase OXA-1 precursor". Vamos a la sección Structure y busquemos las palabras clave "Beta-lactamase OXA-1".

![struc](https://github.com/microgenomics/tutorials/raw/master/img/struc.png)

La búsqueda nos retorna cinco resultados. Si hacemos clic en alguno, podemos acceder a la estructura cristalina de la proteína codificada por el gen.

		¿Qué otra especie posee está proteína?
		¿Cuántas cadenas tiene la proteína?
		¿Cuál es el sitio activo?

## Referencias

Seemann T.  
*Prokka: rapid prokaryotic genome annotation*  
**Bioinformatics** 2014 Jul 15;30(14):2068-9.   
[PMID:24642063](http://www.ncbi.nlm.nih.gov/pubmed/24642063)  

Bankevich, A. et al.  
*SPAdes: a new genome assembly algorithm and its applications to single-cell sequencing*  
**Journal of Computational Biology** 2012 19.5 (2012): 455-477.  
[PMID:22506599](https://www.ncbi.nlm.nih.gov/pubmed/22506599)  

Gurevich, A et al.  
*QUAST: quality assessment tool for genome assemblies*  
**Bioinformatics** 29.8 (2013): 1072-1075  
[PMID:23422339](https://www.ncbi.nlm.nih.gov/pubmed/23422339)  

Kearse, M, et al.  
*Geneious Basic: an integrated and extendable desktop software platform for the organization and analysis of sequence data*  
**Bioinformatics** 28.12 (2012): 1647-1649.  
[PMID:22543367](https://www.ncbi.nlm.nih.gov/pubmed/22543367)  

**FastQC**
[http://www.bioinformatics.babraham.ac.uk/projects/fastqc/](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
