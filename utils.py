#!/usr/bin/env python3

import random


def get_random_interval(x):
    interval = random.sample(range(x), k=2)
    return min(interval), max(interval)


def random_delete(cell):
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene = chromo.genes[j]

    if len(gene) <= 15:
        return random_delete(cell)

    # Check gene importance and change cell state accordingly
    if gene.role == 'oncogene':
        cell.add_score(gene.role, gene.weight)
    elif gene.role == 'tumor_suppressor':
        cell.add_score(gene.role, -gene.weight)

    start, end = get_random_interval(len(gene))
    gene.delete_sequence(start, end)
    chromo.update_positions( -(end-start), j+1)
    id = gene.gene_id
    chromo = chromo.id
    return [chromo, id, start, end, '0', '0', 0, 0, 'f_DL']


def random_duplicate(cell):

    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene = chromo.genes[j]

    if len(gene) <= 15:
        return random_duplicate(cell)

    # Check gene importance and change cell state accordingly
    if gene.role == 'oncogene':
        cell.add_score(gene.role, gene.weight)
    elif gene.role == 'tumor_suppressor':
        cell.add_score(gene.role, -gene.weight)

    start, end = get_random_interval(len(gene))
    sequence = gene.sequence[start:end]
    gene.insert_sequence(end, sequence)
    chromo.update_positions( -(end-start), j+1)
    id = gene.gene_id
    chromo = chromo.id
    return [chromo, id, start, end, chromo, id, end, 0, 'f_DP']


def random_insert(cell):
    # Get a sequence
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene1 = chromo.genes[j]

    if len(gene1) <= 15:
        return random_insert(cell)
    start, end = get_random_interval(len(gene1))
    sequence = gene1.sequence[start:end]

    # Insert sequence in another gene
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene2 = chromo.genes[j]

    # Check gene importance and change cell state accordingly
    if gene2.role != '':
        cell.add_score('oncogene', gene2.weight)

    pos = random.choice(range(len(gene2)))
    gene2.insert_sequence(pos, sequence)
    chromo.update_positions( -(end-start), j+1)
    id1 = gene1.gene_id
    chromo1 = gene1.chromosome
    id2 = gene2.gene_id
    chromo2 = gene2.chromosome
    return [chromo1, id1, start, end, chromo2, id2, pos, 0, 'f_IN']


def random_move(cell):
    # Get a sequence and remove it
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene1 = chromo.genes[j]
    if len(gene1) <= 15:
        return random_move(cell)
    # Check gene importance and change cell state accordingly
    if gene1.role != '':
        cell.add_score('oncogene', gene1.weight)

    start, end = get_random_interval(len(gene1))
    sequence = gene1.sequence[start:end]
    gene1.delete_sequence(start, end)
    chromo.update_positions( -(end-start), j+1)

    # Insert sequence in another gene
    m = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[m]
    n = random.choice(range(len(chromo)))
    gene2 = chromo.genes[n]

    # Check gene importance and change cell state accordingly
    if gene2.role != '':
        cell.add_score('oncogene', gene2.weight)

    pos = random.choice(range(len(gene2)))
    gene2.insert_sequence(pos, sequence)
    chromo.update_positions( -(end-start), n+1)
    id1 = gene1.gene_id
    chromo1 = gene1.chromosome
    id2 = gene2.gene_id
    chromo2 = gene2.chromosome
    return [chromo1, id1, start, end, chromo2, id2, pos, 0, 'f_MV']


def random_gene_duplication(cell):
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene = chromo.genes[j]
    gene_copy = gene.copy()

    # Check gene importance and change cell state accordingly
    if gene.role != '':
        cell.add_score(gene.role, gene.weight)

    gene_copy.end = gene.end + 1 + len(gene_copy)
    gene_copy.start = gene.end + 1
    chromo.add_gene(gene_copy, index=j+1)
    chromo.update_positions(len(gene_copy), j+2)
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
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene = chromo.genes[j]
    gene_copy = gene.copy()

    # Check gene importance and change cell state accordingly
    if gene.role != '':
        cell.add_score(gene.role, gene.weight)

    # Get other random gene and insert gene_copy after it
    m = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[m]
    n = random.choice(range(len(chromo)))
    gene2 = chromo.genes[n]

    gene_copy.chromosome = gene2.chromosome
    gene_copy.start = gene2.end + 1
    gene_copy.end = gene_copy.start + len(gene)
    chromo.add_gene(gene_copy, index=n+1)
    chromo.update_positions(len(gene_copy), n+2)
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
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    j = random.choice(range(len(chromo)))
    gene = chromo.genes[j]
    chromo.remove_gene(j)

    if gene.role != '':
        cell.add_score(gene.role, gene.weight)

    to_return = [
        gene.chromosome,
        gene.gene_id,
        gene.start,
        gene.end,
    ]
    l = len(gene)

    # Get other random gene and insert gene after it
    m = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[m]
    n = random.choice(range(len(chromo)))
    gene2 = chromo.genes[n]
    gene.chromosome = gene2.chromosome
    gene.start = gene2.end + 1
    gene.end = gene.start + l
    chromo.add_gene(gene, index=n+1)
    chromo.update_positions(len(gene), n+2)

    to_return += [
        gene.chromosome,
        gene.gene_id,
        gene.start,
        gene.end,
        'g_MV'
    ]
    return to_return


def chromothripsis(cell):
    """
    Here, a region is defined as a gene
    For the purpose of our system, the selection of regions and the shuffle
    of the different elements as well as the deletion and amplification
    wil be done on genes
    """
    # Get random chromosome
    # Get random start region for chromothripsis operation
    # Get random end region for operation
    i = random.choice(list(cell.chromosomes.keys()))
    chromo = cell.chromosomes[i]
    region_start = random.choice(range(len(chromo))) # number of gene in chr
    step = random.choice(range(100,1000))
    if (region_start+step >= len(chromo)-1):
        region_end = len(chromo)-1
    else:
        region_end = random.choice(range(region_start, len(chromo)-1, step))
        while region_end == region_start:
            region_end = random.choice(range(region_start, len(chromo)-1, step))
    region = chromo.genes[region_start:region_end]


    # All selected genes in the region are shuffled
    # For each gene, apply a choice and append the result to new_region
    new_region = list()
    choices = ['nothing', 'duplicate', 'delete']
    prob_not = random.choice(range(800, 1000, 1))
    prob_dup_del = 1000 - prob_not
    prob_dup = random.choice(range(0, prob_dup_del, 1))
    prob_del = (prob_dup_del - prob_dup)/1000
    prob_not /= 1000
    prob_dup /= 1000
    choices_weights = [prob_not, prob_dup, prob_del]
    ref_gene = chromo.genes[region_start-1]
    random.shuffle(region)
    for i, gene in enumerate(region):
        choice = random.choices(choices, weights=choices_weights, k=1)[0]
        if choice == 'delete':
            if gene.role != '':
                cell.add_score(gene.role, -gene.weight)
            continue

        elif choice == 'duplicate':
            if gene.role != '':
                cell.add_score(gene.role, gene.weight)
            gene_copy = gene.copy()
            gene_copy.end = ref_gene.end+1 + len(gene_copy)
            gene_copy.start = ref_gene.end+1
            ref_gene = gene_copy
            new_region.append(gene_copy)
        gene.end = ref_gene.end+1 + len(gene)
        gene.start = ref_gene.end+1
        ref_gene = gene
        new_region.append(gene)

    # If lots of genes were added, the position of each subsequent gene might
    # need to be incremented accordingly
    if ref_gene.end > chromo.genes[region_end].start:
        length = ref_gene.end - chromo.genes[region_end].start
        chromo.update_positions(length, region_end)
    chromo.genes = chromo.genes[:region_start]+new_region+chromo.genes[region_end:]


def random_operation(cell):
    operations = [
        random_delete,
        random_duplicate,
        random_insert,
        random_move,
        random_gene_duplication,
        random_gene_insert,
        random_gene_move,
    ]
    if cell.balance >= 1.3:
        operations += [chromothripsis]
    random.shuffle(operations)
    op = random.choice(operations)
    return op(cell)
