#!/usr/bin/env python3

class Chromosome():
    def __init__(self, id, sequence):
        self.id = id
        self.sequence = sequence
        self.start = 0
        self.end = len(self.sequence)-1
