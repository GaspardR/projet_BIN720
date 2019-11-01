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
        self.genes = dataframe(annotation)
        self.genes = [
            Gene(
                self.genes['gene_id'][i],
                self.genes['chromosome'][i],
                self.genes['start'][i],
                self.genes['end'][i]
            )
            for i, feature in enumerate(self.genes['feature'])
            if feature=='gene'
        ]

    def get_genes_sequence(self):
        for chromo in SeqIO.parse(self.fasta, 'fasta'):
            for gene in self.genes:
                if gene.chromosome == str(chromo.id):
                    gene.sequence = chromo.seq[gene.start : gene.end + 1]
