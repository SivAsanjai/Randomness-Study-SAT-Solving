# experiments.py

import time
import numpy as np
import matplotlib.pyplot as plt
from sat_solver import HybridSATSolver
from utils import load_sat_instances
import os
import copy 

def run_experiment(instances, p_values, max_flips=10000):

    results = {p: {'success': 0, 'flips': [], 'time': []} for p in p_values}

    for idx, instance in enumerate(instances):
        clauses = instance['clauses']
        num_vars = instance['num_vars']
        filename = instance['filename']
        print(f"Solving instance {idx+1}/{len(instances)}: {filename} with {num_vars} variables and {len(clauses)} clauses.")
        for p in p_values:
            solver = HybridSATSolver(copy.deepcopy(clauses), num_vars, p=p, max_flips=max_flips)
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
    avg_flips = [np.mean(results[p]['flips']) for p in p_values]
    avg_time = [np.mean(results[p]['time']) for p in p_values]

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
    plot_path = os.path.join(output_dir, 'experiment_results.png')
    plt.savefig(plot_path)
    plt.show()
    print(f'Results saved to {plot_path}')

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Run experiments on SAT solvers with varying randomness.')
    parser.add_argument('--cnf_dir', type=str, default='sat_instances', help='Directory containing CNF files.')
    parser.add_argument('--p_start', type=float, default=0.0, help='Starting value of p.')
    parser.add_argument('--p_end', type=float, default=1.0, help='Ending value of p.')
    parser.add_argument('--p_step', type=float, default=0.1, help='Step size for p.')
    parser.add_argument('--max_flips', type=int, default=10000, help='Maximum number of flips per solver run.')
    parser.add_argument('--output_dir', type=str, default='results', help='Directory to save results.')

    args = parser.parse_args()

    # Defining p values
    p_values = np.arange(args.p_start, args.p_end + args.p_step, args.p_step)
    p_values = np.round(p_values, decimals=2)  

    
    instances = load_sat_instances(args.cnf_dir)
    total_instances = len(instances)
    print(f"Loaded {total_instances} SAT instances from '{args.cnf_dir}'.")

    if total_instances == 0:
        print(f"No CNF files found in '{args.cnf_dir}'. Please generate SAT instances first.")
        return

    
    results = run_experiment(instances, p_values, max_flips=args.max_flips)

    
    analyze_results(results, total_instances, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
