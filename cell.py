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
        self.genes = dataframe(annotation)
        self.genes = [
            Gene(
                self.genes['gene_id'][i],
                self.genes['chromosome'][i],
                self.genes['start'][i],
                self.genes['end'][i],
                self.genes['strand'][i]
            )
            for i, feature in enumerate(self.genes['feature'])
            if feature=='gene'
        ]
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

    def get_state():
        pass

    def set_state():
        pass
