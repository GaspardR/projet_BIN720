#!/usr/bin/env python3

# Public modules
from Bio import SeqIO
import random

# User defined modules
from gene import Gene
import parser

class Cell():
    def __init__(self, fasta, annotation, cancer_genes_file):
        self.state = 0
        self.fasta = fasta
        # Need to do 2 times to account for 2 copies of each chromosome
        self.frame = parser.gtf(annotation)
        self.genes = [
            Gene(
                self.frame['gene_id'][i],
                self.frame['gene_name'][i],
                self.frame['chromosome'][i] + '_1',
                self.frame['start'][i],
                self.frame['end'][i],
                self.frame['strand'][i]
            )
            for i, feature in enumerate(self.frame['feature'])
            if feature=='gene'
        ]
        self.genes += [
            Gene(
                self.frame['gene_id'][i],
                self.frame['gene_name'][i],
                self.frame['chromosome'][i] + '_2',
                self.frame['start'][i],
                self.frame['end'][i],
                self.frame['strand'][i]
            )
            for i, feature in enumerate(self.frame['feature'])
            if feature=='gene'
        ]
        self.genes.sort(key=lambda gene: (gene.chromosome, gene.start))
        cancer_genes = parser.tsv(cancer_genes_file)
        for gene in self.genes:
            if gene.name in cancer_genes.keys():
                gene.role = cancer_genes[gene.name]

    def add_gene(self, gene, index=None):
        if not isinstance(gene, Gene):
            raise TypeError('gene argument passed was not a Gene()')
        if index:
            self.genes.insert(index, gene)
        else:
            # For now, but this isn't pretty at all, should find better method
            self.genes.append(gene)
            self.genes.sort(key=lambda gene: (gene.chromosome, gene.start))

    def remove_gene(self, index):
        return self.genes.pop(index)

    def get_genes_sequence(self):
        for chromo in SeqIO.parse(self.fasta, 'fasta'):
            for gene in self.genes:
                if gene.chromosome == str(chromo.id):
                    if gene.strand == '-':
                        gene.sequence = str(
                            chromo.seq[gene.start : gene.end + 1].complement()
                        )
                    else:
                        gene.sequence = str(
                            chromo.seq[gene.start : gene.end + 1]
                        )

    def update_chromosome(self, chromosome, length, index):
        while (index < len(self.genes)) and (self.genes[index].chromosome == chromosome):
            self.genes[index].start += length
            self.genes[index].end += length
            index += 1

    def copy(self):
        raise NotImplementedError()

    def get_state():
        return cell.state
