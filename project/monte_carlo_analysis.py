import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from utils import monte_carlo

def plot_monte_carlo_distribution_patient():
    """Histogram for Patient-Specific Virtual Care NPV"""
    results_m1, _, _ = monte_carlo(n_samples=10000)
    
    fig, ax = plt.subplots(figsize=(15, 6))
    
    bins = np.linspace(min(results_m1) - 1, max(results_m1) + 1, 40)
    
    sns.histplot(results_m1, bins=bins, kde=True, ax=ax, color='#4472C4', alpha=0.7)
    
    mean = np.mean(results_m1)
    p5 = np.percentile(results_m1, 5)
    p95 = np.percentile(results_m1, 95)
    prob_neg = np.mean(np.array(results_m1) < 0) * 100
    
    ax.axvline(mean, color='black', linestyle='-', linewidth=2, label=f'Mean: €{mean:.1f}m')
    ax.axvline(p5, color='red', linestyle='--', linewidth=2, label=f'5th percentile: €{p5:.1f}m')
    ax.axvline(p95, color='green', linestyle='--', linewidth=2, label=f'95th percentile: €{p95:.1f}m')
    ax.legend(fontsize=27)

    ax.axvspan(-20, 0, alpha=0.2, color='red')
    ax.text(p5 - 0.5, ax.get_ylim()[1] * 0.8, 
            f'Prob(NPV<0): {prob_neg:.1f}%', 
            color='red', fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))
    
    ax.set_title('Monte Carlo Simulation: Patient-Specific Virtual Care', fontsize=19)
    ax.set_xlabel('Net Present Value (€ millions)', fontsize=17)
    ax.set_ylabel('Frequency', fontsize=17)
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.3)
    
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    ax.set_xlim(left=0)
    return fig

def plot_monte_carlo_distribution_hospital():
    """Histogram for Hospital Simulation Network NPV"""
    _, results_m2, _ = monte_carlo(n_samples=10000)
    
    fig, ax = plt.subplots(figsize=(15, 6))
    
    bins = np.linspace(min(results_m2) - 1, max(results_m2) + 1, 40)
    
    sns.histplot(results_m2, bins=bins, kde=True, ax=ax, color='#ED7D31', alpha=0.7)
    
    mean = np.mean(results_m2)
    p5 = np.percentile(results_m2, 5)
    p95 = np.percentile(results_m2, 95)
    prob_neg = np.mean(np.array(results_m2) < 0) * 100
    
    ax.axvline(mean, color='black', linestyle='-', linewidth=2, label=f'Mean: €{mean:.1f}m')
    ax.axvline(p5, color='red', linestyle='--', linewidth=2, label=f'5th percentile: €{p5:.1f}m')
    ax.axvline(p95, color='green', linestyle='--', linewidth=2, label=f'95th percentile: €{p95:.1f}m')
    ax.legend(fontsize=27)
    ax.axvspan(-20, 0, alpha=0.2, color='red')
    ax.text(p5 - 0.5, ax.get_ylim()[1] * 0.8, 
            f'Prob(NPV<0): {prob_neg:.1f}%', 
            color='red', fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))
    
    ax.set_title('Monte Carlo Simulation: Hospital Simulation Network', fontsize=14)
    ax.set_xlabel('Net Present Value (€ millions)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.3)
    
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.set_xlim(left=0)
    return fig
