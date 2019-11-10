#!/usr/bin/env python3

from cell import Cell
import utils


def main(fasta, gtf):
    my_cell = Cell(fasta, gtf)
    my_cell.get_genes_sequence()
    # print(type(my_cell.genes[0].sequence))
    # for i in range(0, 20):
    #     print(my_cell.genes[i].chromosome, my_cell.genes[i].start)
    a = [my_cell.genes[i].start for i in range(850, 870)]
    # print(a)
    for i in range(10):
        c = utils.random_operation(my_cell)
        # b = [my_cell.genes[i].start for i in range(850, 870)]
        # for i in range(len(a)):
        #     print(a[i], b[i])
        print(c)

if __name__ in "__main__":
    fasta = "data/chromosome/Homo_sapiens.GRCh38.dna.chromosome.21.fa"
    gtf = "data/chr21_genes.gtf"
    big_fasta = "data/chromosome/all_chromosome.fa"
    big_gtf = "data/genes.gtf"
    main(big_fasta, big_gtf)
