import matplotlib.pyplot as plt
import numpy as np
from utils import get_scenario_data

def plot_scenario_comparison():
    """Create bar chart comparing scenarios for both projects"""
    scenario_data = get_scenario_data()
    
    # Extract data
    scenarios = ["Optimistic", "Expected", "Pessimistic"]
    macro1_values = [scenario_data["MACRO1"][s] for s in scenarios]
    macro2_values = [scenario_data["MACRO2"][s] for s in scenarios]
    
    # Set up plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Width of bars and positions
    width = 0.35
    x = np.arange(len(scenarios))
    
    # Plot bars
    bars1 = ax.bar(x - width/2, macro1_values, width, label='Patient-Specific VC', 
                  color='#4472C4', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x + width/2, macro2_values, width, label='Hospital Sim & Ed', 
                  color='#ED7D31', edgecolor='black', linewidth=0.5)
    
    # Add value labels on bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            label_y_pos = max(height + 0.1, 0.3) if height > 0 else height - 0.7
            ax.text(bar.get_x() + bar.get_width()/2., label_y_pos,
                    f'€{height:.1f}m', ha='center', va='bottom', fontweight='bold')
    
    add_labels(bars1)
    add_labels(bars2)
    
    # Customize plot
    ax.set_title('NPV by Scenario (0.8% Social Discount Rate)', fontsize=14, pad=20)
    ax.set_ylabel('Net Present Value (€ millions)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=12)
    ax.legend(loc='upper right', frameon=True)
    
    # Add a horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.7, alpha=0.5)
    
    # Add grid lines
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Set y-axis limits to show negative values
    min_value = min(min(macro1_values), min(macro2_values))
    ax.set_ylim(min_value - 1 if min_value < 0 else -0.5, max(max(macro1_values), max(macro2_values)) + 1)
    
    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    # Add explanatory text
    footnote = (
        "Scenarios:\n"
        "• Optimistic: 120% uptake, 130% compliance, 75% hardware costs\n"
        "• Expected: 100% uptake, 100% compliance, 100% hardware costs\n"
        "• Pessimistic: 60% uptake, 50% compliance, 110% hardware costs"
    )
    fig.text(0.1, 0.01, footnote, fontsize=9, va='bottom', ha='left')
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    
    return fig

def plot_discount_rate_sensitivity():
    """Create line chart showing NPV sensitivity to discount rates"""
    # Discount rates to analyze
    rates = [0.001, 0.005, 0.008, 0.01, 0.02, 0.03, 0.04, 0.05, 0.057, 0.07, 0.1]
    rate_labels = [f"{r*100:.1f}%" for r in rates]
    
    # Project parameters
    from utils import MACRO1, MACRO2, npv
    
    # Calculate NPVs for each rate
    npv_m1 = [npv(MACRO1["capex"], MACRO1["opex"], MACRO1["benefit"], r) / 1e6 for r in rates]
    npv_m2 = [npv(MACRO2["capex"], MACRO2["opex"], MACRO2["benefit"], r) / 1e6 for r in rates]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot lines
    ax.plot(rate_labels, npv_m1, 'o-', color='#4472C4', linewidth=2, markersize=8, 
            label='Patient-Specific VC')
    ax.plot(rate_labels, npv_m2, 's-', color='#ED7D31', linewidth=2, markersize=8, 
            label='Hospital Sim & Ed')
    
    # Highlight specific rates
    highlight_indices = [2, 6, 8]  # 0.8%, 3%, 5.7%
    highlight_rates = [rates[i] for i in highlight_indices]
    highlight_labels = [rate_labels[i] for i in highlight_indices]
    highlight_m1 = [npv_m1[i] for i in highlight_indices]
    highlight_m2 = [npv_m2[i] for i in highlight_indices]
    
    ax.plot(highlight_labels, highlight_m1, 'o', color='#4472C4', markersize=12, markeredgecolor='black')
    ax.plot(highlight_labels, highlight_m2, 's', color='#ED7D31', markersize=12, markeredgecolor='black')
    
    # Add value labels for highlighted points
    for i, txt in enumerate(highlight_labels):
        ax.annotate(f'€{highlight_m1[i]:.1f}m', 
                    (highlight_labels[i], highlight_m1[i]), 
                    xytext=(5, 10), textcoords='offset points',
                    fontweight='bold')
        ax.annotate(f'€{highlight_m2[i]:.1f}m', 
                    (highlight_labels[i], highlight_m2[i]), 
                    xytext=(5, -15), textcoords='offset points',
                    fontweight='bold')
    
    # Customize plot
    ax.set_title('NPV Sensitivity to Discount Rate', fontsize=14, pad=20)
    ax.set_ylabel('Net Present Value (€ millions)', fontsize=12)
    ax.set_xlabel('Discount Rate', fontsize=12)
    ax.legend(loc='upper right', frameon=True)
    
    # Add a horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.7, alpha=0.5)
    
    # Add vertical lines for key rates
    for i in highlight_indices:
        ax.axvline(x=rate_labels[i], color='gray', linestyle='--', alpha=0.5)
    
    
    # Add grid lines
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    plt.tight_layout()
    
    return fig

def plot_break_even_analysis():
    """Create chart showing break-even adoption factors"""
    from utils import MACRO1, MACRO2, RATES
    
    # Calculate adoption factors required for break-even across different discount rates
    rates = [0.008, 0.03, 0.05, 0.057]
    rate_labels = ["0.8% SDR", "3% SDR", "5% SDR", "5.7% WACC"]
    
    # Function to calculate break-even adoption factor
    def adoption_threshold(capex, opex, benefit, rate):
        low, high = 0.0, 2.0
        for _ in range(60):
            mid = (low+high)/2
            from utils import npv
            if npv(capex, opex, benefit*mid, rate) > 0:
                high = mid
            else:
                low = mid
        return high
    
    # Calculate thresholds for each rate
    m1_thresholds = [adoption_threshold(MACRO1["capex"], MACRO1["opex"], MACRO1["benefit"], r) for r in rates]
    m2_thresholds = [adoption_threshold(MACRO2["capex"], MACRO2["opex"], MACRO2["benefit"], r) for r in rates]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar positions
    x = np.arange(len(rate_labels))
    width = 0.35
    
    # Plot bars
    bars1 = ax.bar(x - width/2, m1_thresholds, width, label='Patient-Specific VC', 
                  color='#4472C4', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x + width/2, m2_thresholds, width, label='Hospital Sim & Ed', 
                  color='#ED7D31', edgecolor='black', linewidth=0.5)
    
    # Add value labels
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{height:.2f}', ha='center', va='bottom', fontweight='bold')
    
    add_labels(bars1)
    add_labels(bars2)
    
    # Customize plot
    ax.set_title('Break-even Adoption Factor by Discount Rate', fontsize=14, pad=20)
    ax.set_ylabel('Minimum Required Adoption Factor', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(rate_labels, fontsize=11)
    ax.legend(loc='upper left', frameon=True)
    
    # Add a horizontal line at y=1.0 (standard adoption)
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(x[-1] + 0.5, 1.0, 'Baseline (100%)', va='center', ha='left', 
            color='red', fontweight='bold')
    
    # Add grid lines
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    # Add explanatory text
    footnote = (
        "Break-even adoption factor: The minimum percentage of expected adoption needed for NPV = 0.\n"
        "Values below 1.0 indicate the project is robust to lower-than-expected adoption rates."
    )
    fig.text(0.1, 0.01, footnote, fontsize=9, va='bottom', ha='left')
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    
    return fig