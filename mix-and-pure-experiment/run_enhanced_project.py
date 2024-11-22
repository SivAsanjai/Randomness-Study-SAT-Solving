# run_enhanced_project.py

import subprocess
import sys
import os

def generate_enhanced_instances():
    
    print("Generating SAT instances...")
    
    subprocess.run([
        sys.executable, 'generate_enhanced_sat.py', 'multiple',
        '--num_instances', '100',
        '--num_vars_min', '50',
        '--num_vars_max', '200',
        '--num_clauses_min', '200',
        '--num_clauses_max', '800',
        '--clause_length', '3',
        # '--satisfiable',  # Uncomment to generate only satisfiable instances
        '--output_dir', 'sat_instances'
    ], check=True)
    print("Enhanced SAT instances generation completed.\n")

def run_enhanced_experiments():
    
    print("Running experiments...")
    subprocess.run([
        sys.executable, 'enhanced_experiments.py',
        '--cnf_dir', 'sat_instances',
        '--p_start', '0.0',
        '--p_end', '1.0',
        '--p_step', '0.1',
        '--max_flips', '10000',
        '--adaptive_p',        # Enable adaptive p
        '--restart_frequency', '1000',
        '--benchmark_solver', 'minisat',  # Ensure MiniSAT is installed and in PATH
        '--max_benchmark_time', '300',
        '--output_dir', 'results',
        '--stat_analysis'      # Enable statistical analysis
    ], check=True)
    print("Enhanced experiments completed.\n")

def main():
    
    if not os.path.exists('generate_enhanced_sat.py'):
        print("Error: 'generate_enhanced_sat.py' not found.")
        return

    
    if not os.path.exists('enhanced_experiments.py'):
        print("Error: 'enhanced_experiments.py' not found.")
        return

    
    generate_enhanced_instances()

    
    run_enhanced_experiments()

    print("All enhanced experiment tasks completed successfully.")

if __name__ == '__main__':
    main()
