import numpy as np
import pandas as pd

# Discount rates in real terms
RATES = {
    "0.8% SDR": 0.008,
    "3% SDR": 0.03,
    "5% SDR": 0.05,
    "5.7% WACC": 0.057
}

# Time horizon
N_YEARS = 15

# Project parameters
MACRO1 = {
    "name": "Patient-Specific Virtual Care",
    "capex": 121_900,
    "opex": 79_800,
    "benefit": 1_389_166.7,
    "hw_share": 1.0
}

MACRO2 = {
    "name": "Hospital Simulation & Education",
    "capex": 1_145_300,
    "opex": 166_000,
    "benefit": 2_876_333,
    "hw_share": (75_800 + 38_500 + 91_000) / 1_145_300  # ≈ 0.18
}


def annuity_factor(r, n):
    """Present value of €1 annuity for n years at rate r"""
    return sum(1 / (1 + r) ** t for t in range(1, n + 1))


def npv(capex, opex, benefit, rate, n=N_YEARS):
    """Calculate NPV at given discount rate"""
    ann = annuity_factor(rate, n)
    return benefit * ann - (capex + opex * ann)


def irr(capex, opex, benefit, n=N_YEARS, guess=0.1):
    """Newton-Raphson IRR calculation on equal annual net benefit"""
    r = guess
    for _ in range(100):
        pv, d_pv = -capex, 0
        for t in range(1, n + 1):
            cf = benefit - opex
            pv += cf / (1 + r) ** t
            d_pv += -t * cf / (1 + r) ** (t + 1)
        r_new = r - pv / d_pv
        if abs(r_new - r) < 1e-10:
            break
        r = r_new
    return r


def bcr(capex, opex, benefit, rate, n=N_YEARS):
    """Calculate Benefit-Cost Ratio"""
    ann = annuity_factor(rate, n)
    return (benefit * ann) / (capex + opex * ann)


def scenario_npv(macro, uptake, comp, hw, rate=0.008):
    """Calculate NPV for a scenario with specific parameters"""
    if macro == "MACRO1":
        project = MACRO1
    else:
        project = MACRO2
    
    # Adjust CAPEX for hardware factors
    if macro == "MACRO1":
        # For MACRO1, all CAPEX is hardware
        adj_capex = project["capex"] * hw
    else:
        # For MACRO2, split CAPEX into hardware vs non-hardware
        adj_capex = project["capex"] * (1 - project["hw_share"]) + project["capex"] * project["hw_share"] * hw
    
    # Adjust benefits for uptake and compliance
    adj_benefit = project["benefit"] * uptake * comp
    
    return npv(adj_capex, project["opex"], adj_benefit, rate) / 1e6  # Return in € millions


def get_scenario_data():
    """Get NPV results for the three scenarios"""
    optimistic_1 = scenario_npv("MACRO1", 1.20, 1.30, 0.75)
    optimistic_2 = scenario_npv("MACRO2", 1.20, 1.30, 0.75)
    
    expected_1 = scenario_npv("MACRO1", 1.00, 1.00, 1.00)
    expected_2 = scenario_npv("MACRO2", 1.00, 1.00, 1.00)
    
    pessimistic_1 = scenario_npv("MACRO1", 0.60, 0.50, 1.10)
    pessimistic_2 = scenario_npv("MACRO2", 0.60, 0.50, 1.10)
    
    return {
        "MACRO1": {
            "Optimistic": optimistic_1,
            "Expected": expected_1,
            "Pessimistic": pessimistic_1
        },
        "MACRO2": {
            "Optimistic": optimistic_2,
            "Expected": expected_2,
            "Pessimistic": pessimistic_2
        }
    }


def tornado_data():
    """Generate data for tornado diagram by varying each parameter individually"""
    # Base case
    base_m1 = scenario_npv("MACRO1", 1.0, 1.0, 1.0)
    base_m2 = scenario_npv("MACRO2", 1.0, 1.0, 1.0)
    
    # Parameter variations (low, high)
    variations = {
        "Uptake Rate": (0.6, 1.2),
        "Compliance Factor": (0.7, 1.3),
        "Hardware Cost Factor": (0.8, 1.2)
    }
    
    results = {"MACRO1": {}, "MACRO2": {}}
    
    for param, (low, high) in variations.items():
        # For each parameter, hold others constant at base value
        if param == "Uptake Rate":
            low_m1 = scenario_npv("MACRO1", low, 1.0, 1.0)
            high_m1 = scenario_npv("MACRO1", high, 1.0, 1.0)
            low_m2 = scenario_npv("MACRO2", low, 1.0, 1.0)
            high_m2 = scenario_npv("MACRO2", high, 1.0, 1.0)
        elif param == "Compliance Factor":
            low_m1 = scenario_npv("MACRO1", 1.0, low, 1.0)
            high_m1 = scenario_npv("MACRO1", 1.0, high, 1.0)
            low_m2 = scenario_npv("MACRO2", 1.0, low, 1.0)
            high_m2 = scenario_npv("MACRO2", 1.0, high, 1.0)
        elif param == "Hardware Cost Factor":
            low_m1 = scenario_npv("MACRO1", 1.0, 1.0, low)
            high_m1 = scenario_npv("MACRO1", 1.0, 1.0, high)
            low_m2 = scenario_npv("MACRO2", 1.0, 1.0, low)
            high_m2 = scenario_npv("MACRO2", 1.0, 1.0, high)
        
        results["MACRO1"][param] = (low_m1 - base_m1, high_m1 - base_m1)
        results["MACRO2"][param] = (low_m2 - base_m2, high_m2 - base_m2)
    
    return results, base_m1, base_m2


def monte_carlo(n_samples=10000, seed=0):
    """Run Monte Carlo simulation and return results"""
    np.random.seed(seed)
    
    results_m1 = []
    results_m2 = []
    parameters = []
    
    for _ in range(n_samples):
        # Generate random parameters using triangular and truncated normal distributions
        uptake = np.random.triangular(0.4, 0.8, 1.2)
        compliance = np.random.triangular(0.8, 1.0, 1.3)
        hw_factor = min(max(np.random.normal(1.0, 0.1), 0.7), 1.3)  # Truncated normal
        
        # Store parameters for correlation analysis
        parameters.append([uptake, compliance, hw_factor])
        
        # Calculate NPVs with these parameters
        npv_m1 = scenario_npv("MACRO1", uptake, compliance, hw_factor)
        npv_m2 = scenario_npv("MACRO2", uptake, compliance, hw_factor)
        
        results_m1.append(npv_m1)
        results_m2.append(npv_m2)
    
    param_df = pd.DataFrame(parameters, columns=["Uptake", "Compliance", "HW_Factor"])
    
    return results_m1, results_m2, param_df