# Laboratorio de Genómica para Informática Médica
-
La actividad del día de hoy consiste en ganar experiencia directa con datos de secuenciamiento masivo y algunos pasos básicos para transformar esos datos en información biológica.  

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
* Finalmente, haremos un blast con la secuencia de la betalactamasa seleccionada e inspeccionaremos su estructura secundaria.  

Para empezar, descarguemos las reads tal cual son entregadas por el secuenciador ([aquí](https://www.dropbox.com/s/7gh1343s4yk0rsf/reads.zip?dl=0)). Alternativamente, las pueden encontrar en sus estaciones de trabajo (más rápido).

Exploremos la calidad de las reads en FastQC

![fastqc](https://github.com/microgenomics/tutorials/raw/master/img/Screenshot%202016-09-21%2023.00.22.png)  

		Explora el significado del gráfico y qué es lo que está expresado en el eje Y.  

En general, un investigador tomaría una desición con respecto a cómo cortar y/o filtrar las reads que no se ajusten a algún estándar. Esta decisión es muchas veces arbitraría y depende de qué tan bien se siente el investigador trabajando sobre el conjunto de reads que pasaron el control de calidad.  

Ahora, necesitamos usar la línea de comandos para poder ensamblar este genoma. Observen que las reads vienen en dos archivos porque corresponden a `Paired-end reads`. Busquen en la Mac el ícono de la Terminal. Al ejecutar la Terminal deberán ver una ventana como la siguiente:  

![terminal](https://github.com/microgenomics/tutorials/raw/master/img/term.png)

### Los siguientes pasos los vamos a seguir durante la clase en la medida que el profesor los vaya demostrando. 





 
