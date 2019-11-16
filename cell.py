#!/usr/bin/env python3

# Public modules
from Bio import SeqIO
import random

# User defined modules
from gene import Gene
from gtf import dataframe

class Cell():
    def __init__(self, fasta, annotation):
        self.state = 0
        self.fasta = fasta
        # Need to do 2 times to account for 2 copies of each chromosome
        self.frame = dataframe(annotation)
        self.genes = [
            Gene(
                self.frame['gene_id'][i],
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
                self.frame['chromosome'][i] + '_2',
                self.frame['start'][i],
                self.frame['end'][i],
                self.frame['strand'][i]
            )
            for i, feature in enumerate(self.frame['feature'])
            if feature=='gene'
        ]
        self.genes.sort(key=lambda gene: (gene.chromosome, gene.start))
        self.cancer_genes = self._random_gene_cancer_set()

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

    def get_state():
        pass

    def set_state():
        pass

    def is_important(self, gene):
        if not isinstance(gene, Gene):
            raise TypeError('gene argument passed was not a Gene()')
        for c_gene in self.cancer_genes:
            if gene == c_gene:
                return True
        return False

    def _random_gene_cancer_set(self):
        # random.seed(5)
        cancer_genes = random.sample(range(len(self.genes)), k=50)
        return [self.genes[i] for i in cancer_genes]
