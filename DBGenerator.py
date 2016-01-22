#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
from glob import glob
from operator import itemgetter
from multiprocessing import Process
from sys import argv


def get_genomas_locus():
    out_csv = open('genomas_locus.csv', 'w')
    print('Starting get_genomas_locus')
    genomas_locus = [tuple(filter(None, tuple(map(itemgetter(i), lista))))  # obtiene la columna de todos los locus de cada genoma
                     for i in range(14, len(lista[0]))]
    for genoma in genomas_locus:  # para cada columna haz
        for locus in genoma[1:]:  # genoma[0] es el nombre del genoma y lo demas son los locus
            locus = locus.split()  # corta los espacios en blanco
            if len(locus) == 1:  # revisa que solo tenga un locus
                locus = locus[0]
                print('{}|{}'.format(genoma[0], locus), file=out_csv)
            else:  # tiene mas de un locus en esa celda
                for locus in loci:  # separalos!
                    print('{}|{}'.format(genoma[0], locus), file=out_csv)
    out_csv.close()
    print('END get_genomas_locus')


def get_pangenoma():  # parsea el gene_presence_absence.csv
    out_csv = open('pangenoma.csv', 'w')
    print('Starting get_pangenoma')
    for row in lista[1:]:
        Gene = row[0]
        Non_unique_Gene_name = row[1]
        Annotation = row[2]
        No_isolates = row[3]
        No_sequences = row[4]
        Avg_sequences_per_isolate = row[5]
        Genome_Fragment = row[6]
        Order_within_Fragment = row[7]
        Accessory_Fragment = row[8]
        Accessory_Order_with_Fragment = row[9]
        QC = row[10]
        Min_group_size_nuc = row[11]
        Max_group_size_nuc = row[12]
        Avg_group_size_nuc = row[13]
        print('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(Gene,
            Non_unique_Gene_name, Annotation, No_isolates, No_sequences,
            Avg_sequences_per_isolate, Genome_Fragment, Order_within_Fragment,
            Accessory_Fragment, Accessory_Order_with_Fragment, QC,
            Min_group_size_nuc, Max_group_size_nuc, Avg_group_size_nuc), file=out_csv)
    out_csv.close()
    print('END get_pangenoma')


def get_pangenoma_locus():
    out_csv = open('pangenoma_locus.csv', 'w')
    print('Starting get_pangenoma_locus')
    for row in lista[1:]:  # como la lista tiene encabezados hay que partri del segundo
        Gene = row[0]  # getea el nombre del gen
        loci = row[14:]  # y de los locis
        for locus in loci:
            locus = locus.split()
            if len(locus) == 1:  # tiene solo un locus
                locus = locus[0]
                print('{}|{}'.format(Gene, locus), file=out_csv)
            else:  # tiene mas de un locus
                for l in locus:
                    print('{}|{}'.format(Gene, l), file=out_csv)
    out_csv.close()
    print('END get_pangenoma_locus')


def get_locus_sequence():
    out_csv = open('locus_sequence.csv', 'w')
    print('Starting get_locus_sequence')
    ffns = glob('{}/*.ffn'.format(argv[1]))  # genera la lista de todos los ffn entregados por PROKKA, prokka_ es el prefijo de los directorios anotados por prokka
    p = re.compile(r'>(\w+).*')  # regex para encontrar los locus en formato fasta
    genomas_locus = open('genomas_locus.csv')  # es necesario tener el csv listo
    reader = csv.reader(genomas_locus, delimiter='|')
    lista_genomas_locus = [row for row in reader]  # lista de TODOS los locus

    for ffn in ffns:  # por cada archivo de secuencia
        archivo = open(ffn)
        reader = archivo.readlines()
        parsed = []
        codigo = ffn.split('/')[-1].split('.')[0]  # es el codigo del archivo ffn
        db = [x[1] for x in lista_genomas_locus if codigo in x[0]]  # todos los locus con el hash unico dado por roary del genoma espesifico si el codigo del archivo fnn es el codigo del genoma del locus, agregalo
        # todo este bloque es para obtener la secuencia sin saltos de linea
        # y solo un saldo de linea antes del > en el fasta
        for linea in reader:
            if '>' in linea:
                parsed.append(linea)
            else:
                parsed.append(linea.strip())
        string = p.sub(r'\n>\1', ''.join(parsed))
        # fin del bloque magico
        lista_locus = string.split('>')  # lista de los locus y su secuencia
        lista_locus = [x.split() for x in lista_locus]  # lista de la forma [[locus, secuencia],...]
        for locus in lista_locus[1:]:  # para cada uno de todos los locus (se usa [1:] para saltar la cabecera del csv)
            codp = re.compile(locus[0])  # regex para buscar el hash asociado al locus de roary
            search = [codp.search(x) for x in db]
            search = tuple(filter(None, search))  # elimina los None
            if len(search) == 1:  # si hay una coincidencia, es que se encontro
                search = search[0].string
                print('{}|{}'.format(search, locus[-1]), file=out_csv)
            elif len(search) == 0:
                pass  # no hay resultados del locus en la db
            else:
                print(locus)
                raise
    out_csv.close()
    print('END get_locus_sequence')


if __name__ == '__main__':
    if not argv[1]:
        print('Se necesita pasar el directorio de los ffns como primer y unico argumento')
        exit()
    csvfile = open('gene_presence_absence.csv')
    reader = csv.reader(csvfile)
    lista = [row for row in reader]
    LISTA_GENOMAS = tuple(lista[0][14:])
    APIGFF = 'https://www.patricbrc.org/portal/portal/patric/Genome?cType=genome&cId={}'

    process_get_genomas_locus = Process(target=get_genomas_locus)
    process_get_pangenoma = Process(target=get_pangenoma)
    process_get_pangenoma_locus = Process(target=get_pangenoma_locus)
    process_get_locus_sequence = Process(target=get_locus_sequence)

    process_get_pangenoma.start()
    process_get_pangenoma_locus.start()
    process_get_genomas_locus.start()
    process_get_genomas_locus.join()
    # espero a que termine el proceso para que tenga listo el csv para correr las demas funciones que dependen del csv
    process_get_locus_sequence.start()
