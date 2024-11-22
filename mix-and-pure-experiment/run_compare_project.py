# run_compare_project.py

import subprocess
import sys
import os

def generate_instances():
    
    print("Generating SAT instances...")
    subprocess.run([
        sys.executable, 'generate_enhanced_sat.py', 'multiple',
        '--num_instances', '100',
        '--num_vars_min', '50',
        '--num_vars_max', '200',
        '--num_clauses_min', '200',
        '--num_clauses_max', '800',
        '--clause_length', '3',
        '--satisfiable',  # Generate strictly satisfiable instances
        '--output_dir', 'sat_instances'
    ], check=True)
    print("Enhanced SAT instances generation completed.\n")

def run_comparative_experiments():
    """
    Runs the comparative experiments using compare_experiments.py.
    """
    print("Running comparative experiments...")
    subprocess.run([
        sys.executable, 'compare_experiments.py',
        '--cnf_dir', 'sat_instances',
        '--max_flips', '10000',
        '--restart_frequency', '1000',
        '--benchmark_solver', 'minisat', 
        '--max_benchmark_time', '300',
        '--output_dir', 'results'
    ], check=True)
    print("Comparative experiments completed.\n")

def main():
    
    if not os.path.exists('generate_enhanced_sat.py'):
        print("Error: 'generate_enhanced_sat.py' not found.")
        return

    
    if not os.path.exists('compare_experiments.py'):
        print("Error: 'compare_experiments.py' not found.")
        return

    
    generate_instances()

    
    run_comparative_experiments()

    print("All comparative experiment tasks completed successfully.")

if __name__ == '__main__':
    main()
