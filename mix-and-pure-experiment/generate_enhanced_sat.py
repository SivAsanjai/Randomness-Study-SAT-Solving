# generate_enhanced_sat.py

import os
import random

def generate_random_cnf(num_vars, num_clauses, clause_length=3, output_dir='sat_instances', filename=None):
    """
    Generates a random CNF SAT instance in DIMACS format.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if filename is None:
        filename = f'random_instance_k{clause_length}_v{num_vars}_c{num_clauses}.cnf'
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        # Write the problem line
        f.write(f'p cnf {num_vars} {num_clauses}\n')
        
        for _ in range(num_clauses):
            clause = []
            for _ in range(clause_length):
                var = random.randint(1, num_vars)
                sign = random.choice([True, False])
                literal = var if sign else -var
                clause.append(str(literal))
            clause.append('0')  # Clause termination
            f.write(' '.join(clause) + '\n')
    
    print(f'Generated CNF file: {filepath}')
    return filepath

def generate_satisfiable_cnf(num_vars, num_clauses, clause_length=3, output_dir='sat_instances', filename=None):
    """
    Generates a satisfiable CNF SAT instance by ensuring all clauses are satisfied by a random model.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if filename is None:
        filename = f'sat_instance_k{clause_length}_v{num_vars}_c{num_clauses}.cnf'
    
    filepath = os.path.join(output_dir, filename)
    
    # Generate a random model
    model = {var: random.choice([True, False]) for var in range(1, num_vars + 1)}
    
    with open(filepath, 'w') as f:
        # Write the problem line
        f.write(f'p cnf {num_vars} {num_clauses}\n')
        
        for _ in range(num_clauses):
            clause = []
            literals = []
            for _ in range(clause_length):
                var = random.randint(1, num_vars)
                # Ensure at least one literal satisfies the clause
                if random.random() < 1 / clause_length:
                    # Align with the model
                    literal = var if model[var] else -var
                else:
                    # Randomly assign opposite to model to add diversity
                    literal = var if not model[var] else -var
                literals.append(literal)
            # Ensure at least one literal satisfies the clause
            satisfied = False
            for lit in literals:
                var = abs(lit)
                if (lit > 0 and model[var]) or (lit < 0 and not model[var]):
                    satisfied = True
                    break
            if not satisfied:
                # Randomly flip one literal to satisfy the clause
                idx = random.randint(0, clause_length - 1)
                lit = literals[idx]
                literals[idx] = abs(lit) if model[abs(lit)] else -abs(lit)
            clause = [str(lit) for lit in literals]
            clause.append('0')
            f.write(' '.join(clause) + '\n')
    
    print(f'Generated satisfiable CNF file: {filepath}')
    print(f'Satisfying assignment: {model}')
    return filepath, model

def generate_structured_cnf(num_vars, num_clauses, clause_length=3, structure='graph_coloring', output_dir='sat_instances', filename=None):
    """
    Generates structured CNF SAT instances based on specific problem domains.
    Currently supports 'graph_coloring'. Can be extended for other structures.
    """
    if structure == 'graph_coloring':
        # Example: Generate graph coloring problems
        # This is a placeholder. Implement actual graph coloring CNF generation as needed.
        # For simplicity, we'll generate random CNFs similar to the random generator.
        return generate_random_cnf(num_vars, num_clauses, clause_length, output_dir, filename)
    else:
        raise NotImplementedError(f"Structure '{structure}' is not supported yet.")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate diverse SAT instances in DIMACS CNF format.')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Sub-parser for generating a single random CNF
    parser_random = subparsers.add_parser('random', help='Generate a random CNF SAT instance.')
    parser_random.add_argument('--num_vars', type=int, required=True, help='Number of variables.')
    parser_random.add_argument('--num_clauses', type=int, required=True, help='Number of clauses.')
    parser_random.add_argument('--clause_length', type=int, default=3, help='Number of literals per clause.')
    parser_random.add_argument('--output_dir', type=str, default='sat_instances', help='Output directory.')
    parser_random.add_argument('--filename', type=str, default=None, help='Output filename.')

    # Sub-parser for generating a single satisfiable CNF
    parser_sat = subparsers.add_parser('satisfiable', help='Generate a satisfiable CNF SAT instance.')
    parser_sat.add_argument('--num_vars', type=int, required=True, help='Number of variables.')
    parser_sat.add_argument('--num_clauses', type=int, required=True, help='Number of clauses.')
    parser_sat.add_argument('--clause_length', type=int, default=3, help='Number of literals per clause.')
    parser_sat.add_argument('--output_dir', type=str, default='sat_instances', help='Output directory.')
    parser_sat.add_argument('--filename', type=str, default=None, help='Output filename.')

    # Sub-parser for generating structured CNF
    parser_structured = subparsers.add_parser('structured', help='Generate a structured CNF SAT instance.')
    parser_structured.add_argument('--num_vars', type=int, required=True, help='Number of variables.')
    parser_structured.add_argument('--num_clauses', type=int, required=True, help='Number of clauses.')
    parser_structured.add_argument('--clause_length', type=int, default=3, help='Number of literals per clause.')
    parser_structured.add_argument('--structure', type=str, default='graph_coloring', help='Type of structure to generate.')
    parser_structured.add_argument('--output_dir', type=str, default='sat_instances', help='Output directory.')
    parser_structured.add_argument('--filename', type=str, default=None, help='Output filename.')

    # Sub-parser for generating multiple CNFs
    parser_multiple = subparsers.add_parser('multiple', help='Generate multiple CNF SAT instances.')
    parser_multiple.add_argument('--num_instances', type=int, required=True, help='Number of CNF instances to generate.')
    parser_multiple.add_argument('--num_vars_min', type=int, required=True, help='Minimum number of variables.')
    parser_multiple.add_argument('--num_vars_max', type=int, required=True, help='Maximum number of variables.')
    parser_multiple.add_argument('--num_clauses_min', type=int, required=True, help='Minimum number of clauses.')
    parser_multiple.add_argument('--num_clauses_max', type=int, required=True, help='Maximum number of clauses.')
    parser_multiple.add_argument('--clause_length', type=int, default=3, help='Number of literals per clause.')
    parser_multiple.add_argument('--structure', type=str, default=None, help='Type of structure to generate (e.g., graph_coloring).')
    parser_multiple.add_argument('--satisfiable', action='store_true', help='Generate only satisfiable instances.')
    parser_multiple.add_argument('--output_dir', type=str, default='sat_instances', help='Output directory.')

    args = parser.parse_args()

    if args.command == 'random':
        generate_random_cnf(
            num_vars=args.num_vars,
            num_clauses=args.num_clauses,
            clause_length=args.clause_length,
            output_dir=args.output_dir,
            filename=args.filename
        )
    elif args.command == 'satisfiable':
        generate_satisfiable_cnf(
            num_vars=args.num_vars,
            num_clauses=args.num_clauses,
            clause_length=args.clause_length,
            output_dir=args.output_dir,
            filename=args.filename
        )
    elif args.command == 'structured':
        generate_structured_cnf(
            num_vars=args.num_vars,
            num_clauses=args.num_clauses,
            clause_length=args.clause_length,
            structure=args.structure,
            output_dir=args.output_dir,
            filename=args.filename
        )
    elif args.command == 'multiple':
        for i in range(1, args.num_instances + 1):
            num_vars = random.randint(args.num_vars_min, args.num_vars_max)
            num_clauses = random.randint(args.num_clauses_min, args.num_clauses_max)
            if args.structure:
                filename = f'structured_instance_{i}_k{args.clause_length}_v{num_vars}_c{num_clauses}.cnf'
                generate_structured_cnf(
                    num_vars=num_vars,
                    num_clauses=num_clauses,
                    clause_length=args.clause_length,
                    structure=args.structure,
                    output_dir=args.output_dir,
                    filename=filename
                )
            elif args.satisfiable:
                filename = f'sat_instance_{i}_k{args.clause_length}_v{num_vars}_c{num_clauses}.cnf'
                generate_satisfiable_cnf(
                    num_vars=num_vars,
                    num_clauses=num_clauses,
                    clause_length=args.clause_length,
                    output_dir=args.output_dir,
                    filename=filename
                )
            else:
                filename = f'random_instance_{i}_k{args.clause_length}_v{num_vars}_c{num_clauses}.cnf'
                generate_random_cnf(
                    num_vars=num_vars,
                    num_clauses=num_clauses,
                    clause_length=args.clause_length,
                    output_dir=args.output_dir,
                    filename=filename
                )
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
