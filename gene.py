#!/usr/bin/env python3

class Gene():
    def __init__(self, gene_id, chromosome, start, end):
        self.gene_id = gene_id
        self.chromosome = str(chromosome)
        self.start = int(start)
        self.end = int(end)
