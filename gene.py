#!/usr/bin/env python3

class Gene():
    def __init__(self, gene_id, chromosome, start, end, strand, sequence=''):
        self.gene_id = gene_id
        self.chromosome = str(chromosome)
        self.start = int(start)
        self.end = int(end)
        self.strand = strand
        self.sequence = sequence

    def __len__(self):
        return self.end - self.start

    def copy(self):
        other = Gene(
            self.gene_id,
            self.chromosome,
            self.start,
            self.end,
            self.strand,
            self.sequence
        )
        return other

    def insert_sequence(self, pos, sequence):
        self.sequence = self.sequence[:pos] + sequence + self.sequence[pos:]
        self.end += len(sequence)

    def delete_sequence(self, start, end):
        self.sequence = self.sequence[:start] + self.sequence[end:]
        self.end -= end - start
