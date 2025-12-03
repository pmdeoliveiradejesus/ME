"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.optimize import linprog

def solve_auction(scenario_name, cap_A, cap_B):
    # 1. Setup Data
    # Cost vector c = [Price_A, Price_B]
    c = [20, 80]
    
    # Equality Constraint: 1*A + 1*B = 100 (Demand)
    A_eq = [[1, 1]]
    b_eq = [100]
    
    # Bounds: 0 <= A <= cap_A, 0 <= B <= cap_B
    bounds = [(0, cap_A), (0, cap_B)]
    
    # 2. Solve LP
    # method='highs' is recommended for modern scipy versions
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    
    # 3. Extract Results
    gen_A = res.x[0]
    gen_B = res.x[1]
    
    # The Clearing Price is the dual value (shadow price) of the equality constraint.
    # Note: Scipy's 'highs' method stores equality duals in res.ineqlin.marginals or eqlin.marginals
    # but strictly it's often easier to inspect the logic or use the specific field:
    if hasattr(res, 'eqlin'): 
         # Negative sign convention sometimes used in optimization packages, taking absolute
        clearing_price = abs(res.eqlin.marginals[0])
    else:
        # Fallback for older scipy versions
        clearing_price = abs(res.con[0] if res.con else 0)

    # Output
    print(f"--- {scenario_name} ---")
    print(f"Capacity A: {cap_A} MW | Capacity B: {cap_B} MW")
    print(f"Dispatch:   Plant A = {gen_A:.1f} MW, Plant B = {gen_B:.1f} MW")
    print(f"Total Cost: ${res.fun:.2f}")
    print(f"Clearing Price (Shadow Price): ${clearing_price:.2f}/MWh")
    print("-" * 30)

# Run Scenario 1: Plant A limited to 50 MW
solve_auction("Scenario 1 (Scarcity)", 50, 100)

# Run Scenario 2: Plant A has full 100 MW (plus epsilon to resolve tie-break favoring low price)
solve_auction("Scenario 2 (Abundance)", 100.001, 100)