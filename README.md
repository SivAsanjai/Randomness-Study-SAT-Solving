# Randomness-Study-SAT-Solving
This repository contains the codebase containing base level implementation of random and greedy strategies for the study of randomness in SAT solving. 

---

### 1. Fixed p Experiment

**Purpose:**  
Investigates the role of randomness in SAT-solving by implementing purely random and purely greedy strategies. 

**Components:**
-  **`sat_solver.py`**: Implements the hybrid SAT solver with random and greedy strategies.
-  `generate_sat.py`: Machine generated to generate SAT instances in DIMACS CNF format.
- `utils.py`: Utility functions for loading and managing SAT instances.
- `experiments.py`: experiment code where we can vary the p values as needed.
- `sat_instances/`: Directory containing generated CNF files.
- `results/`: Directory where experiment results and plots are saved.

---

### 2. Mixed and Variable Experiment

**Directory:** `enhanced_sat_experiment/`

**Purpose:**  
Introducing additional randomness strategies, and mixed random-greedy approaches.

**Components:**

- **`enhanced_sat_solver.py`**: Enhanced solver incorporating random restarts and adaptive probability adjustments.
- `generate_enhanced_sat.py`: Similar to prev exp.
- `enhanced_utils.py`: Similar to prev exp
- `enhanced_experiments.py`: Similar to prev exp
- `compare_experiments.py`: Compares purely random, purely greedy, and MiniSAT solvers.
- `sat_instances/`: Similar to prev exp
- `results/`: Similar to prev exp

---

