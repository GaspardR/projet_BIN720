#!/usr/bin/env python3

from bisect import bisect_right

class Chromosome():
    def __init__(self, id, genes):
        self.id = id
        self.genes = genes

    def __len__(self):
        return len(self.genes)

    def copy(self):
        return Chromosome(self.id, [g.copy() for g in self.genes])

    def add_gene(self, gene, index=None):
        if not index:
            index = bisect_right(self.genes, gene)
        self.genes.insert(index, gene)

    def remove_gene(self, index):
        return self.genes.pop(index)

    def update_positions(self, length, index):
        while index < len(self.genes):
            self.genes[index].start += length
            self.genes[index].end += length
            index += 1
