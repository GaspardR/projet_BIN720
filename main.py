#!/usr/bin/env python3

from cell import Cell


def main(fasta, gtf):
    my_cell = Cell(fasta, gtf)
    my_cell.get_genes_sequence()


if __name__ in "__main__":
    fasta = "data/chromosome/Homo_sapiens.GRCh38.dna.chromosome.21.fa"
    gtf = "data/Homo_sapiens_chr21.GRCh38.98.gtf"
    big_fasta = "data/chromosome/all_chromosome.fa"
    big_gtf = "data/genes.gtf"
    main(big_fasta, big_gtf)
