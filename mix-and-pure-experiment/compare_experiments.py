# compare_experiments.py

import time
import numpy as np
import matplotlib.pyplot as plt
from enhanced_sat_solver import EnhancedHybridSATSolver
from enhanced_utils import load_sat_instances
import os
import copy
import subprocess
from collections import defaultdict

def run_pure_random_experiment(instances, max_flips=10000, restart_frequency=1000):
    
    #Runs the purely random SAT solver (p=0.0) on all instances.
    
    p = 0.0
    results = {'success': 0, 'flips': [], 'time': []}
    print("Running Purely Random Solver (p=0.0)...")
    for idx, instance in enumerate(instances):
        clauses = instance['clauses']
        num_vars = instance['num_vars']
        filename = instance['filename']
        print(f"Random Solver: Solving instance {idx+1}/{len(instances)}: {filename}")
        solver = EnhancedHybridSATSolver(
            copy.deepcopy(clauses),
            num_vars,
            p=p,
            max_flips=max_flips,
            restart_frequency=restart_frequency,
            adaptive_p=False  # No adaptive p for purely random
        )
        start_time = time.time()
        status, flips, model = solver.solve()
        end_time = time.time()
        if status:
            results['success'] += 1
            results['flips'].append(flips)
            results['time'].append(end_time - start_time)
        else:
            results['flips'].append(max_flips)
            results['time'].append(end_time - start_time)
    return results

def run_pure_greedy_experiment(instances, max_flips=10000, restart_frequency=1000, adaptive_p=False):
    
    #Runs the purely greedy SAT solver (p=1.0) on all instances.
    
    p = 1.0
    results = {'success': 0, 'flips': [], 'time': []}
    print("Running Purely Greedy Solver (p=1.0)...")
    for idx, instance in enumerate(instances):
        clauses = instance['clauses']
        num_vars = instance['num_vars']
        filename = instance['filename']
        print(f"Greedy Solver: Solving instance {idx+1}/{len(instances)}: {filename}")
        solver = EnhancedHybridSATSolver(
            copy.deepcopy(clauses),
            num_vars,
            p=p,
            max_flips=max_flips,
            restart_frequency=restart_frequency,
            adaptive_p=adaptive_p  #  Can enable adaptive p
        )
        start_time = time.time()
        status, flips, model = solver.solve()
        end_time = time.time()
        if status:
            results['success'] += 1
            results['flips'].append(flips)
            results['time'].append(end_time - start_time)
        else:
            results['flips'].append(max_flips)
            results['time'].append(end_time - start_time)
    return results

def benchmark_minisat(instances, solver='minisat', max_time=300):
    
    #Runs MiniSAT on all instances and records performance.
    
    benchmark_results = {
        'success': 0,
        'timeouts': 0,
        'time': []
    }
    print("Benchmarking MiniSAT Solver...")
    for idx, instance in enumerate(instances):
        cnf_file = os.path.join('sat_instances', instance['filename'])
        print(f"MiniSAT: Solving instance {idx+1}/{len(instances)}: {instance['filename']}")
        start_time = time.time()
        try:
            
            result = subprocess.run(
                [solver, cnf_file],
                capture_output=True,
                text=True,
                timeout=max_time
            )
            end_time = time.time()
            output = result.stdout
            if 'UNSAT' in output:
                status = False
            else:
                # MiniSAT outputs 'SATISFIABLE' / 'UNSATISFIABLE'
                if 'SATISFIABLE' in output:
                    status = True
                elif 'UNSATISFIABLE' in output:
                    status = False
                else:
                    status = None  # Indeterminate/Undecided
        except subprocess.TimeoutExpired:
            status = None  # timeout
            end_time = time.time()
        if status is True:
            benchmark_results['success'] += 1
        elif status is False:
            pass  
        elif status is None:
            benchmark_results['timeouts'] += 1
        benchmark_results['time'].append(end_time - start_time)
    return benchmark_results

def analyze_comparative_results(random_results, greedy_results, minisat_results, total_instances, output_dir='results'):
    
    
    os.makedirs(output_dir, exist_ok=True)

    
    methods = ['Pure Random', 'Pure Greedy', 'MiniSAT']
    success_rates = [
        (random_results['success'] / total_instances) * 100,
        (greedy_results['success'] / total_instances) * 100,
        (minisat_results['success'] / total_instances) * 100
    ]
    avg_flips = [
        np.mean(random_results['flips']) if random_results['flips'] else 0,
        np.mean(greedy_results['flips']) if greedy_results['flips'] else 0,
        None  # NA for MiniSAT
    ]
    avg_time = [
        np.mean(random_results['time']) if random_results['time'] else 0,
        np.mean(greedy_results['time']) if greedy_results['time'] else 0,
        np.mean(minisat_results['time']) if minisat_results['time'] else 0
    ]

    # Success Rates
    plt.figure(figsize=(10, 6))
    plt.bar(methods, success_rates, color=['skyblue', 'salmon', 'lightgreen'])
    plt.ylabel('Success Rate (%)')
    plt.title('Success Rate Comparison')
    plt.ylim(0, 100)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'success_rate_comparison.png'))
    plt.show()
    print(f'Success rate comparison plot saved to {os.path.join(output_dir, "success_rate_comparison.png")}')

    # Avrg Flips
    plt.figure(figsize=(10, 6))
    plt.bar(methods[:-1], avg_flips[:-1], color=['skyblue', 'salmon'])
    plt.ylabel('Average Number of Flips')
    plt.title('Average Number of Flips Comparison')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'avg_flips_comparison.png'))
    plt.show()
    print(f'Average flips comparison plot saved to {os.path.join(output_dir, "avg_flips_comparison.png")}')

    # Avrg Time
    plt.figure(figsize=(10, 6))
    plt.bar(methods, avg_time, color=['skyblue', 'salmon', 'lightgreen'])
    plt.ylabel('Average Solving Time (s)')
    plt.title('Average Solving Time Comparison')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'avg_time_comparison.png'))
    plt.show()
    print(f'Average solving time comparison plot saved to {os.path.join(output_dir, "avg_time_comparison.png")}')

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Compare Pure Random, Pure Greedy, and MiniSAT solvers on SAT instances.')
    parser.add_argument('--cnf_dir', type=str, default='sat_instances', help='Directory containing CNF files.')
    parser.add_argument('--max_flips', type=int, default=10000, help='Maximum number of flips per solver run.')
    parser.add_argument('--restart_frequency', type=int, default=1000, help='Number of flips after which to restart.')
    parser.add_argument('--benchmark_solver', type=str, default='minisat', help='Standard SAT solver executable name.')
    parser.add_argument('--max_benchmark_time', type=int, default=300, help='Maximum time per benchmark solver run in seconds.')
    parser.add_argument('--output_dir', type=str, default='results', help='Directory to save results.')
    args = parser.parse_args()

    # Load SAT instances
    instances = load_sat_instances(args.cnf_dir)
    total_instances = len(instances)
    print(f"Loaded {total_instances} SAT instances from '{args.cnf_dir}'.")
    if total_instances == 0:
        print(f"No CNF files found in '{args.cnf_dir}'. Please generate SAT instances first.")
        return

    # Run Purely Random Experiment
    random_results = run_pure_random_experiment(
        instances,
        max_flips=args.max_flips,
        restart_frequency=args.restart_frequency
    )

    # Run Purely Greedy Experiment
    greedy_results = run_pure_greedy_experiment(
        instances,
        max_flips=args.max_flips,
        restart_frequency=args.restart_frequency,
        adaptive_p=False  # Set to True if you want adaptive p in greedy
    )

    # Run MiniSAT Benchmark
    minisat_results = benchmark_minisat(
        instances,
        solver=args.benchmark_solver,
        max_time=args.max_benchmark_time
    )

    # Analyze and Plot 
    analyze_comparative_results(
        random_results,
        greedy_results,
        minisat_results,
        total_instances,
        output_dir=args.output_dir
    )

    #save 
    import json
    raw_data = {
        'Pure Random': random_results,
        'Pure Greedy': greedy_results,
        'MiniSAT': minisat_results
    }
    with open(os.path.join(args.output_dir, 'comparative_experiment_raw_data.json'), 'w') as f:
        json.dump(raw_data, f, indent=4)
    print(f'Raw experiment data saved to {os.path.join(args.output_dir, "comparative_experiment_raw_data.json")}')

if __name__ == "__main__":
    main()
