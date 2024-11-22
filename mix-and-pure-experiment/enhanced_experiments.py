# enhanced_experiments.py

import time
import numpy as np
import matplotlib.pyplot as plt
from enhanced_sat_solver import EnhancedHybridSATSolver
from enhanced_utils import load_sat_instances
import os
import copy
import subprocess
from collections import defaultdict

def run_experiment(instances, p_values, max_flips=10000, adaptive_p=False, restart_frequency=1000):

    results = {p: {'success': 0, 'flips': [], 'time': []} for p in p_values}

    for idx, instance in enumerate(instances):
        clauses = instance['clauses']
        num_vars = instance['num_vars']
        filename = instance['filename']
        print(f"Solving instance {idx+1}/{len(instances)}: {filename} with {num_vars} variables and {len(clauses)} clauses.")
        for p in p_values:
            solver = EnhancedHybridSATSolver(
                copy.deepcopy(clauses),
                num_vars,
                p=p,
                max_flips=max_flips,
                restart_frequency=restart_frequency,
                adaptive_p=adaptive_p
            )
            start_time = time.time()
            status, flips, model = solver.solve()
            end_time = time.time()
            if status:
                results[p]['success'] += 1
                results[p]['flips'].append(flips)
                results[p]['time'].append(end_time - start_time)
            else:
                results[p]['flips'].append(max_flips)
                results[p]['time'].append(end_time - start_time)
    return results

def analyze_results(results, total_instances, output_dir='results'):
  
   
    os.makedirs(output_dir, exist_ok=True)

    p_values = sorted(results.keys())
    success_rates = [results[p]['success'] / total_instances * 100 for p in p_values]
    avg_flips = [np.mean(results[p]['flips']) if results[p]['flips'] else 0 for p in p_values]
    avg_time = [np.mean(results[p]['time']) if results[p]['time'] else 0 for p in p_values]

    plt.figure(figsize=(18, 5))

    # Success Rate vs. p
    plt.subplot(1, 3, 1)
    plt.plot(p_values, success_rates, marker='o')
    plt.title('Success Rate vs. p')
    plt.xlabel('p (Probability of Greedy Move)')
    plt.ylabel('Success Rate (%)')
    plt.grid(True)

    # Average Flips vs. p
    plt.subplot(1, 3, 2)
    plt.plot(p_values, avg_flips, marker='o', color='orange')
    plt.title('Average Flips vs. p')
    plt.xlabel('p (Probability of Greedy Move)')
    plt.ylabel('Average Number of Flips')
    plt.grid(True)

    # Average Time vs. p
    plt.subplot(1, 3, 3)
    plt.plot(p_values, avg_time, marker='o', color='green')
    plt.title('Average Time vs. p')
    plt.xlabel('p (Probability of Greedy Move)')
    plt.ylabel('Average Time (s)')
    plt.grid(True)

    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'enhanced_experiment_results.png')
    plt.savefig(plot_path)
    plt.show()
    print(f'Results saved to {plot_path}')

def benchmark_standard_solver(instances, solver='minisat', max_time=300):
  
    benchmark_results = {
        'success': 0,
        'timeouts': 0,
        'time': []
    }

    for idx, instance in enumerate(instances):
        cnf_file = os.path.join('sat_instances', instance['filename'])
        print(f"Benchmarking solver on instance {idx+1}/{len(instances)}: {instance['filename']}")
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
                status = True
        except subprocess.TimeoutExpired:
            status = None  # Indicate timeout
            end_time = time.time()
        if status is True:
            benchmark_results['success'] += 1
        elif status is False:
            pass  # Explicitly unsatisfiable; already considered a run
        elif status is None:
            benchmark_results['timeouts'] += 1
        benchmark_results['time'].append(end_time - start_time)
    return benchmark_results

def benchmark_and_compare(instances, solver='minisat', max_time=300, output_dir='results'):
    
    print("Starting comparative benchmarking with standard SAT solver...")
    benchmark_results = benchmark_standard_solver(instances, solver=solver, max_time=max_time)

    # Plot 
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10, 5))

    # Success Rate
    success_rate = benchmark_results['success'] / len(instances) * 100
    plt.bar(['Standard Solver'], [success_rate], color='blue')
    plt.ylabel('Success Rate (%)')
    plt.title('Standard Solver Success Rate')
    plt.ylim(0, 100)
    plt.grid(axis='y')
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'standard_solver_success_rate.png')
    plt.savefig(plot_path)
    plt.show()
    print(f'Standard solver success rate saved to {plot_path}')

    # Average Time
    avg_time = np.mean(benchmark_results['time']) if benchmark_results['time'] else 0
    plt.figure(figsize=(6, 5))
    plt.bar(['Standard Solver'], [avg_time], color='blue')
    plt.ylabel('Average Time (s)')
    plt.title('Standard Solver Average Time')
    plt.grid(axis='y')
    plt.tight_layout()
    plot_path = os.path.join(output_dir, 'standard_solver_avg_time.png')
    plt.savefig(plot_path)
    plt.show()
    print(f'Standard solver average time saved to {plot_path}')

    return benchmark_results



def main():
    import argparse

    parser = argparse.ArgumentParser(description='Run enhanced experiments on SAT solvers with varying randomness.')
    parser.add_argument('--cnf_dir', type=str, default='sat_instances', help='Directory containing CNF files.')
    parser.add_argument('--p_start', type=float, default=0.0, help='Starting value of p.')
    parser.add_argument('--p_end', type=float, default=1.0, help='Ending value of p.')
    parser.add_argument('--p_step', type=float, default=0.1, help='Step size for p.')
    parser.add_argument('--max_flips', type=int, default=10000, help='Maximum number of flips per solver run.')
    parser.add_argument('--adaptive_p', action='store_true', help='Enable adaptive p in the solver.')
    parser.add_argument('--restart_frequency', type=int, default=1000, help='Number of flips after which to restart.')
    parser.add_argument('--benchmark_solver', type=str, default='minisat', help='Standard SAT solver executable name.')
    parser.add_argument('--max_benchmark_time', type=int, default=300, help='Maximum time per benchmark solver run in seconds.')
    parser.add_argument('--output_dir', type=str, default='results', help='Directory to save results.')
    parser.add_argument('--stat_analysis', action='store_true', help='Perform statistical analysis comparing hybrid and standard solvers.')

    args = parser.parse_args()

    # Define p values
    p_values = np.arange(args.p_start, args.p_end + args.p_step, args.p_step)
    p_values = np.round(p_values, decimals=2)  # Avoid floating point precision issues

    # Load SAT instances
    instances = load_sat_instances(args.cnf_dir)
    total_instances = len(instances)
    print(f"Loaded {total_instances} SAT instances from '{args.cnf_dir}'.")

    if total_instances == 0:
        print(f"No CNF files found in '{args.cnf_dir}'. Please generate SAT instances first.")
        return

    
    print("Running hybrid solver experiments...")
    hybrid_results = run_experiment(
        instances,
        p_values,
        max_flips=args.max_flips,
        adaptive_p=args.adaptive_p,
        restart_frequency=args.restart_frequency
    )
    print("Hybrid solver experiments completed.\n")

    
    analyze_results(hybrid_results, total_instances, output_dir=args.output_dir)

    
    if args.benchmark_solver:
        benchmark_results = benchmark_and_compare(
            instances,
            solver=args.benchmark_solver,
            max_time=args.max_benchmark_time,
            output_dir=args.output_dir
        )

       

if __name__ == "__main__":
    main()
