#!/usr/bin/env python3

class Gene():
    def __init__(self, gene_id, name, chromosome, start, end, strand, sequence='', role=''):
        self.gene_id = gene_id
        self.name = name
        self.chromosome = str(chromosome)
        self.start = int(start)
        self.end = int(end)
        self.strand = strand
        self.sequence = sequence
        self.role = role

    def __len__(self):
        return self.end - self.start

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.gene_id == other.gene_id and
                self.sequence == other.sequence)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        other = Gene(
            self.gene_id,
            self.name,
            self.chromosome,
            self.start,
            self.end,
            self.strand,
            self.sequence
        )
        other.role = self.role
        return other


    def delete_sequence(self, start, end):
        self.sequence = self.sequence[:start] + self.sequence[end:]
        self.end -= end - start

    def insert_sequence(self, pos, sequence):
        self.sequence = self.sequence[:pos] + sequence + self.sequence[pos:]
        self.end += len(sequence)
