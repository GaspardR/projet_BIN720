#!/usr/bin/env python3

# Public modules
from Bio import SeqIO

# User defined modules
from gene import Gene
from gtf import dataframe

class Cell():
    def __init__(self, fasta, annotation):
        self.state = 'healthy'
        self.fasta = fasta
        # Need to do 2 times to account for 2 copies of each chromosome
        self.frame = dataframe(annotation)
        self.genes = [
            Gene(
                self.frame['gene_id'][i],
                self.frame['chromosome'][i],
                self.frame['start'][i],
                self.frame['end'][i],
                self.frame['strand'][i]
            )
            for i, feature in enumerate(self.frame['feature'])
            if feature=='gene'
        ]
        self.genes.sort(key=lambda gene: (gene.chromosome, gene.start))

    def add_gene(self, gene, index=None):
        if not isinstance(gene, Gene):
            raise TypeError('gene argument passed was not a Gene()')
        if index:
            self.genes.insert(index, gene)
        else:
            # For now, but this isn't pretty at all, should find better method
            self.genes.append(gene)
            self.genes.sort(key=lambda gene: (gene.chromosome, gene.start))

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

    def get_state():
        pass

    def set_state():
        pass
