#!/usr/bin/env python3

import utils

class Cell():
    def __init__(self, chromosomes, important_genes, state):
        self.chromosomes = chromosomes
        self._cancer_genes_score = important_genes
        self.state = state


        self._original_balance = self._get_balance()
        self.balance = self._get_balance()/self._original_balance


    def _get_balance(self):
        b = self._cancer_genes_score['oncogene'] / \
            self._cancer_genes_score['tumor_suppressor']
        return b


    def copy(self):
        other = Cell(
            {k: v.copy() for k, v in self.chromosomes.items()},
            self._cancer_genes_score,
            self.state
        )
        other._original_balance = self._original_balance
        other.balance = self.balance
        return other


    def add_score(self, key, score):
        self._cancer_genes_score[key] += score


    def update_balance(self):
        self.balance = self._get_balance()/self._original_balance


    def cycle(self):
        if (self.balance < 1.2 and self.balance > 0.8):
            # Healthy
            nb_operations = 5
        elif (self.balance >=1.2 and self.balance < 1.3) or (self.balance <= 0.8 and self.balance > 0.7):
            # Moderately healthy
            nb_operations = 10
        elif (self.balance >=1.3 and self.balance < 1.5) or (self.balance <= 0.7 and self.balance > 0.5):
            # Not to healthy
            nb_operations = 20
        else:
            # Cancer
            nb_operations = 25

        ops = [utils.random_operation(self) for i in range(nb_operations)]
        self.update_balance()
        return ops


    def get_state(self):
        if (self.balance < 1.3) and (self.balance > 0.7):
            self.state = 'healthy'
        elif (self.balance >= 1.3 and self.balance < 1.5) or (self.balance <= 0.7 and self.balance > 0.5):
            self.state = 'healthy'
        elif (self.balance >=1.5) or (self.balance <= 0.5) :
            self.state = 'cancer'
        return self.state
