#sat_solver.py

import random
from collections import defaultdict
import copy

class HybridSATSolver:
    def __init__(self, clauses, num_vars, p=0.5, max_flips=10000):
        
        self.clauses = clauses
        self.num_vars = num_vars
        self.p = p
        self.max_flips = max_flips
        self.model = [random.choice([True, False]) for _ in range(num_vars + 1)]  # 1-indexed

    def is_satisfied(self):
        
        for clause in self.clauses:
            satisfied = False
            for literal in clause:
                var = abs(literal)
                val = self.model[var]
                if literal > 0 and val:
                    satisfied = True
                    break
                elif literal < 0 and not val:
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True

    def get_unsatisfied_clauses(self):
       
        unsat = []
        for clause in self.clauses:
            satisfied = False
            for literal in clause:
                var = abs(literal)
                val = self.model[var]
                if literal > 0 and val:
                    satisfied = True
                    break
                elif literal < 0 and not val:
                    satisfied = True
                    break
            if not satisfied:
                unsat.append(clause)
        return unsat

    def variable_frequency(self, unsat_clauses):
        
        freq = defaultdict(int)
        for clause in unsat_clauses:
            for literal in clause:
                var = abs(literal)
                freq[var] += 1
        return freq

    def select_variable_greedy(self, unsat_clauses):
        
        freq = self.variable_frequency(unsat_clauses)
        if not freq:
            return None
        max_freq = max(freq.values())
        candidates = [var for var, count in freq.items() if count == max_freq]
        return random.choice(candidates)

    def select_variable_random(self, unsat_clauses):
        
        variables = set()
        for clause in unsat_clauses:
            for literal in clause:
                variables.add(abs(literal))
        if not variables:
            return None
        return random.choice(list(variables))

    def flip_variable(self, var):
        
        self.model[var] = not self.model[var]

    def solve(self):
        
        for flip in range(1, self.max_flips + 1):
            if self.is_satisfied():
                return True, flip, self.model
            unsat_clauses = self.get_unsatisfied_clauses()
            if not unsat_clauses:
                return True, flip, self.model
            if random.random() < self.p:
                var = self.select_variable_greedy(unsat_clauses)
            else:
                var = self.select_variable_random(unsat_clauses)
            if var is None:
                return False, flip, None
            self.flip_variable(var)
        return False, self.max_flips, None
