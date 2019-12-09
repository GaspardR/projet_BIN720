#!/usr/bin/env python3

import argparse
import os
import sys

from collections import defaultdict

import parse_file
import utils

from cell import Cell
from chromosome import Chromosome
from gene import Gene



def preprocess(annotation, cancer_genes_file):

    # Initial values
    balance = {'tumor_suppressor': 0, 'oncogene': 0}
    chromosomes = defaultdict(list)

    # Process files
    frame = parse_file.gtf(annotation)
    cancer_genes = parse_file.tsv(cancer_genes_file)

    for allele in ['_1', '_2']:
        for i, feature in enumerate(frame['feature']):
            if feature == 'gene':
                if frame['chromosome'][i] in ['MT', 'Y', 'X']:
                    chromo = frame['chromosome'][i]
                else:
                    chromo = frame['chromosome'][i] + allele
                gene = Gene(
                    frame['gene_id'][i],
                    frame['gene_name'][i],
                    chromo,
                    frame['start'][i],
                    frame['end'][i],
                    frame['strand'][i]
                )
                if gene.name in cancer_genes.keys():
                    gene.role = cancer_genes[gene.name][0]
                    gene.weight = cancer_genes[gene.name][1]
                    balance[gene.role] += 1
                chromosomes[gene.chromosome].append(gene)

    for key, value in chromosomes.items():
        value.sort(key=lambda gene: (gene.start))
        chromosomes[key] = Chromosome(key, value)

    return chromosomes, balance



def run(gtf, cancer_genes_file, nb_cells, nb_cycle):
    nb_cancer = 0
    nb_healthy = 0

    chromosomes, important_genes = preprocess(gtf, cancer_genes_file)
    my_cell = Cell(chromosomes, important_genes, state='healthy')
    for i in range(nb_cells):
        cell = my_cell.copy()

        for cycle in range(nb_cycle):
            cell_cpt = 0
            cell.cycle()
            cell_cpt += 1
        if cell.get_state() == 'cancer':
            nb_cancer += 1
        else:
            nb_healthy += 1
    return nb_cancer, nb_healthy


if __name__ in "__main__":
    print('\nStarting\n')
    parser = argparse.ArgumentParser()

    parser.add_argument('annotation', help="annotation file in .gtf format")
    parser.add_argument(
        'cancer_genes',
        help="""cancer_genes file in .tsv format.
        Needs the columns 'gene_normalized' as the gene_name and 'role' as the
        role of that gene, where role={oncogene, tumor_suppressor}"""
    )
    parser.add_argument(
        'cell_population',
        type=int,
        help='number of cells that compose the population to simulate on'
    )
    parser.add_argument(
        'cycles',
        type=int,
        help='number of cell cycles for simulation'
    )


    args = parser.parse_args()
    annotation = os.path.realpath(args.annotation)
    cancer_genes = os.path.realpath(args.cancer_genes)
    cell_population = args.cell_population
    number_of_cycles = args.cycles


    nb_cancer, nb_healthy  = run(
        annotation,
        cancer_genes,
        cell_population,
        number_of_cycles
    )
    print(nb_cancer, nb_healthy)
