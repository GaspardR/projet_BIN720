#!/usr/bin/env python3

import random


def get_random_interval(x):
    interval = random.sample(range(x), k=2)
    return min(interval), max(interval)


def random_delete(cell):
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    start, end = get_random_interval(len(gene))
    gene.delete_sequence(start, end)
    cell.update_chromosome(gene.chromosome, -(end-start), i+1)
    id = gene.gene_id
    chromo = gene.chromosome
    return [chromo, id, start, end, '0', '0', 0, 0, 'DL']


def random_duplicate(cell):
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    start, end = get_random_interval(len(gene))
    sequence = gene.sequence[start:end]
    gene.insert_sequence(end, sequence)
    cell.update_chromosome(gene.chromosome, len(sequence), i+1)
    id = gene.gene_id
    chromo = gene.chromosome
    return [chromo, id, start, end, chromo, id, end, 0, 'DP']


def random_insert(cell):
    # Get a sequence
    i = random.choice(range(len(cell.genes)))
    gene1 = cell.genes[i]
    start, end = get_random_interval(len(gene1))
    sequence = gene1.sequence[start:end]

    # Insert sequence in another gene
    j = random.choice(range(len(cell.genes)))
    gene2 = cell.genes[j]
    pos = random.choice(range(len(gene2)))
    gene2.insert_sequence(pos, sequence)
    cell.update_chromosome(gene2.chromosome, len(sequence), j+1)
    id1 = gene1.gene_id
    chromo1 = gene1.chromosome
    id2 = gene2.gene_id
    chromo2 = gene2.chromosome
    return [chromo1, id1, start, end, chromo2, id2, pos, 0, 'IN']


def random_move(cell):
    # Get a sequence and remove it
    i = random.choice(range(len(cell.genes)))
    gene1 = cell.genes[i]
    start, end = get_random_interval(len(gene1))
    sequence = gene1.sequence[start:end]
    gene1.delete_sequence(start, end)
    cell.update_chromosome(gene1.chromosome, -(end-start), i+1)

    # Insert sequence in another gene
    j = random.choice(range(len(cell.genes)))
    gene2 = cell.genes[j]
    pos = random.choice(range(len(gene2)))
    gene2.insert_sequence(pos, sequence)
    cell.update_chromosome(gene2.chromosome, len(sequence), j+1)
    id1 = gene1.gene_id
    chromo1 = gene1.chromosome
    id2 = gene2.gene_id
    chromo2 = gene2.chromosome
    return [chromo1, id1, start, end, chromo2, id2, pos, 0, 'IN']


def random_operation(cell):
    operations = [random_delete, random_duplicate, random_insert, random_move]
    op = random.choice(operations)
    return op(cell)