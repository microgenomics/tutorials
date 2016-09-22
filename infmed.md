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



### Los siguientes pasos los vamos a seguir durante la clase en la medida que el profesor los vaya demostrando. 





 
