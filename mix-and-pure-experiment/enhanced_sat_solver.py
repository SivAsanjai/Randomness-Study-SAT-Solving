# enhanced_sat_solver.py

import random
from collections import defaultdict

class EnhancedHybridSATSolver:
    def __init__(self, clauses, num_vars, p=0.5, max_flips=10000, restart_frequency=1000, adaptive_p=False):
        
        #Initializes the enhanced hybrid SAT solver with random restarts and adaptive p.
        
        self.clauses = clauses
        self.num_vars = num_vars
        self.p = p
        self.max_flips = max_flips
        self.restart_frequency = restart_frequency
        self.adaptive_p = adaptive_p
        self.model = [random.choice([True, False]) for _ in range(num_vars + 1)]  # 1-indexed
        self.flips_since_restart = 0

    def is_satisfied(self):
       
        for clause in self.clauses:
            satisfied = False
            for literal in clause:
                var = abs(literal)
                val = self.model[var]
                if (literal > 0 and val) or (literal < 0 and not val):
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
                if (literal > 0 and val) or (literal < 0 and not val):
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

    def restart(self):
       
        self.model = [random.choice([True, False]) for _ in range(self.num_vars + 1)]

    def adjust_p(self):
        
        num_unsat = len(self.get_unsatisfied_clauses())
        if num_unsat > self.num_vars * 0.3:
            # Increase randomness
            self.p = min(self.p + 0.05, 1.0)
        elif num_unsat < self.num_vars * 0.1:
            # Decrease randomness
            self.p = max(self.p - 0.05, 0.0)
        

    def solve(self):
        
        for flip in range(1, self.max_flips + 1):
            if self.is_satisfied():
                return True, flip, self.model
            unsat_clauses = self.get_unsatisfied_clauses()
            if not unsat_clauses:
                return True, flip, self.model
            if self.adaptive_p:
                self.adjust_p()
            if random.random() < self.p:
                var = self.select_variable_greedy(unsat_clauses)
            else:
                var = self.select_variable_random(unsat_clauses)
            if var is None:
                return False, flip, None
            self.flip_variable(var)
            self.flips_since_restart += 1

            # Check for restart
            if self.flips_since_restart >= self.restart_frequency:
                self.restart()
                self.flips_since_restart = 0

        return False, self.max_flips, None
