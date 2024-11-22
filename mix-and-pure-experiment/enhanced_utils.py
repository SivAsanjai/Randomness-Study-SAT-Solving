# enhanced_utils.py

import os

def load_cnf_file(filepath):
    #Loads a single CNF file.
    clauses = []
    num_vars = 0
    num_clauses = 0
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):
                continue  
            if line.startswith('p'):
                parts = line.split()
                if len(parts) >= 4 and parts[1] == 'cnf':
                    num_vars = int(parts[2])
                    num_clauses = int(parts[3])
                continue
            # Parse 
            clause = list(map(int, line.split()))[:-1] 
            clauses.append(clause)
    return clauses, num_vars, num_clauses

def load_sat_instances(directory):
    
    #Loads all SAT instances from a directory.
    
    instances = []
    for filename in os.listdir(directory):
        if filename.endswith(".cnf"):
            filepath = os.path.join(directory, filename)
            clauses, num_vars, num_clauses = load_cnf_file(filepath)
            instance = {
                'filename': filename,
                'clauses': clauses,
                'num_vars': num_vars,
                'num_clauses': num_clauses
            }
            instances.append(instance)
    return instances
