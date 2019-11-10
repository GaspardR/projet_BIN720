#!/usr/bin/env python3

class Gene():
    def __init__(self, gene_id, chromosome, start, end, strand):
        self.gene_id = gene_id
        self.chromosome = str(chromosome)
        self.start = int(start)
        self.end = int(end)
        self.strand = strand

    def __len__(self):
        return self.end - self.start

    def insert_sequence(self, pos, sequence):
        self.sequence = self.sequence[:pos] + sequence + self.sequence[pos:]
        self.end += len(sequence)

    def delete_sequence(self, start, end):
        self.sequence = self.sequence[:start] + self.sequence[end:]
        self.end -= end - start
