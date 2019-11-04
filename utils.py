#!/usr/bin/env python3

import random


def delete(cell):
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    temp1, temp2 = random.sample(range(len(gene)), k=2)
    start = min(temp1, temp2)
    end = max(temp1, temp2)
    gene.sequence = gene.sequence[:start] + gene.sequence[end:]
    deleted_length = end - start
    gene.end -= deleted_length
    if i == len(cell.genes)-1:
        return cell
    i += 1
    while cell.genes[i].chromosome == gene.chromosome:
        cell.genes[i].start -= deleted_length
        cell.genes[i].end -= deleted_length
        if i == len(cell.genes)-1:
            return cell
        i += 1
    return cell

def duplicate(cell):
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    temp1, temp2 = random.sample(range(len(gene)), k=2)
    start = min(temp1, temp2)
    end = max(temp1, temp2)
    gene.sequence = gene.sequence[:start] + gene.sequence[start:end] + gene.sequence[start:end] + gene.sequence[end:]
    added_length = start + end
    gene.end += added_length
    if i == len(cell.genes)-1:
        return cell
    i += 1
    while cell.genes[i].chromosome == gene.chromosome:
        cell.genes[i].start += added_length
        cell.genes[i].end += added_length
        if i == len(cell.genes)-1:
            return cell
        i += 1
    return cell


def insert(cell):
    """
    Probably doesn't work, needs fixing
    """
    # Get a sequence
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    temp1, temp2 = random.sample(range(len(gene)), k=2)
    start = min(temp1, temp2)
    end = max(temp1, temp2)
    to_insert = gene.sequence[start:end]

    # Insert sequence in another gene
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    temp1, temp2 = random.sample(range(len(gene)), k=2)
    start = min(temp1, temp2)
    end = max(temp1, temp2)
    gene.sequence = gene.sequence[:start] + to_insert + gene.sequence[end:]
    gene.end += len(sequence)
    if i == len(cell.genes)-1:
        return cell
    i += 1
    while cell.genes[i].chromosome == gene.chromosome:
        cell.genes[i].start += added_length
        cell.genes[i].end += added_length
        if i == len(cell.genes)-1:
            return cell
        i += 1
    return cell

def move(cell):
    """
    Probably doesn't work, needs fixing
    """
    # Get sequence and remove it from first gene
    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    temp1, temp2 = random.sample(range(len(gene)), k=2)
    start = min(temp1, temp2)
    end = max(temp1, temp2)
    to_move = gene.sequence[start:end]
    gene.sequence = gene.sequence[:start] + gene.sequence[end:]
    deleted_length = end - start
    gene.end -= deleted_length
    if i == len(cell.genes)-1:
        return cell
    i += 1
    while cell.genes[i].chromosome == gene.chromosome:
        cell.genes[i].start -= deleted_length
        cell.genes[i].end -= deleted_length
        if i == len(cell.genes)-1:
            return cell
        i += 1

    i = random.choice(range(len(cell.genes)))
    gene = cell.genes[i]
    temp1, temp2 = random.sample(range(len(gene)), k=2)
    start = min(temp1, temp2)
    end = max(temp1, temp2)
    gene.sequence = gene.sequence[:start] + to_insert + gene.sequence[end:]
    gene.end += len(sequence)
    if i == len(cell.genes)-1:
        return cell
    i += 1
    while cell.genes[i].chromosome == gene.chromosome:
        cell.genes[i].start += added_length
        cell.genes[i].end += added_length
        if i == len(cell.genes)-1:
            return cell
        i += 1
    return cell
