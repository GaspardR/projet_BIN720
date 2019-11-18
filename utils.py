#!/usr/bin/env python3

import random


def get_random_interval(x):
    interval = random.sample(range(x), k=2)
    return min(interval), max(interval)


def random_delete(cell):
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    if len(gene) <= 15:
        return random_delete(cell)

    # Check gene importance and change cell state accordingly
    if gene.role == 'oncogene':
        cell.state -= 1
    elif gene.role == 'tumor_suppressor':
        cell.state += 1

    start, end = get_random_interval(len(gene))
    gene.delete_sequence(start, end)
    cell.update_chromosome(gene.chromosome, -(end-start), i+1)
    id = gene.gene_id
    chromo = gene.chromosome
    return [chromo, id, start, end, '0', '0', 0, 0, 'f_DL']


def random_duplicate(cell):
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]

    # Check gene importance and change cell state accordingly
    if gene.role == 'oncogene':
        cell.state += 1
    elif gene.role == 'tumor_suppressor':
        cell.state -= 1

    start, end = get_random_interval(len(gene))
    sequence = gene.sequence[start:end]
    gene.insert_sequence(end, sequence)
    cell.update_chromosome(gene.chromosome, len(sequence), i+1)
    id = gene.gene_id
    chromo = gene.chromosome
    return [chromo, id, start, end, chromo, id, end, 0, 'f_DP']


def random_insert(cell):
    # Get a sequence
    i = random.choice(range(len(cell.genes)))
    gene1 = cell.genes[i]
    if len(gene1) <= 15:
        return random_insert(cell)
    start, end = get_random_interval(len(gene1))
    sequence = gene1.sequence[start:end]

    # Insert sequence in another gene
    j = random.choice(range(len(cell.genes)))
    gene2 = cell.genes[j]

    # Check gene importance and change cell state accordingly
    if gene2.role != '':
        cell.state += 1

    pos = random.choice(range(len(gene2)))
    gene2.insert_sequence(pos, sequence)
    cell.update_chromosome(gene2.chromosome, len(sequence), j+1)
    id1 = gene1.gene_id
    chromo1 = gene1.chromosome
    id2 = gene2.gene_id
    chromo2 = gene2.chromosome
    return [chromo1, id1, start, end, chromo2, id2, pos, 0, 'f_IN']


def random_move(cell):
    # Get a sequence and remove it
    i = random.choice(range(len(cell.genes)))
    gene1 = cell.genes[i]
    if len(gene1) <= 15:
        return random_move(cell)
    # Check gene importance and change cell state accordingly
    if gene1.role != '':
        cell.state += 1

    start, end = get_random_interval(len(gene1))
    sequence = gene1.sequence[start:end]
    gene1.delete_sequence(start, end)
    cell.update_chromosome(gene1.chromosome, -(end-start), i+1)

    # Insert sequence in another gene
    j = random.choice(range(len(cell.genes)))
    gene2 = cell.genes[j]

    # Check gene importance and change cell state accordingly
    if gene2.role != '':
        cell.state += 1

    pos = random.choice(range(len(gene2)))
    gene2.insert_sequence(pos, sequence)
    cell.update_chromosome(gene2.chromosome, len(sequence), j+1)
    id1 = gene1.gene_id
    chromo1 = gene1.chromosome
    id2 = gene2.gene_id
    chromo2 = gene2.chromosome
    return [chromo1, id1, start, end, chromo2, id2, pos, 0, 'f_MV']


def random_gene_duplication(cell):
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    gene_copy = gene.copy()

    # Check gene importance and change cell state accordingly
    if gene.role == 'oncogene':
        cell.state += 1
    elif gene.role == 'tumor_suppressor':
        cell.state -= 1

    gene_copy.start = gene.end + 1
    gene_copy.end = gene_copy.start + len(gene)
    cell.add_gene(gene_copy, index=i+1)
    cell.update_chromosome(gene_copy.chromosome, len(gene_copy), i+2)
    to_return = [
        gene.chromosome,
        gene.gene_id,
        gene.start,
        gene.end,
        gene_copy.chromosome,
        gene_copy.gene_id,
        gene_copy.start,
        gene_copy.end,
        'g_DP'
    ]
    return to_return


def random_gene_insert(cell):
    # Get random gene_copy
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    gene_copy = gene.copy()

    # Check gene importance and change cell state accordingly
    if gene.role == 'oncogene':
        cell.state += 1
    elif gene.role == 'tumor_suppressor':
        cell.state -= 1

    # Get other random gene and insert gene_copy after it
    j = random.choice(range(len(cell.genes)))
    gene2 = cell.genes[j]
    gene_copy.chromosome = gene2.chromosome
    gene_copy.start = gene2.end + 1
    gene_copy.end = gene_copy.start + len(gene)
    cell.add_gene(gene_copy, index=j+1)
    cell.update_chromosome(gene_copy.chromosome, len(gene_copy), j+2)
    to_return = [
        gene.chromosome,
        gene.gene_id,
        gene.start,
        gene.end,
        gene_copy.chromosome,
        gene_copy.gene_id,
        gene_copy.start,
        gene_copy.end,
        'g_IN'
    ]
    return to_return


def random_gene_move(cell):
    # Get random gene and remove from cell
    i = random.choice(range(len(cell.genes)))
    gene = cell.remove_gene(i)
    if gene.role == 'oncogene':
        cell.state += 1
    elif gene.role == 'tumor_suppressor':
        cell.state -= 1
    to_return = [
        gene.chromosome,
        gene.gene_id,
        gene.start,
        gene.end,
    ]
    l = len(gene)

    # Get other random gene and insert gene after it
    j = random.choice(range(len(cell.genes)))
    gene2 = cell.genes[j]
    gene.chromosome = gene2.chromosome
    gene.start = gene2.end + 1
    gene.end = gene.start + l
    cell.add_gene(gene, index=j+1)
    cell.update_chromosome(gene.chromosome, len(gene), j+2)
    to_return += [
        gene.chromosome,
        gene.gene_id,
        gene.start,
        gene.end,
        'g_MV'
    ]
    return to_return


def random_operation(cell):
    operations = [
        random_delete,
        random_duplicate,
        random_insert,
        random_move,
        random_gene_duplication,
        random_gene_insert,
        random_gene_move
    ]
    op = random.choice(operations)
    return op(cell)
