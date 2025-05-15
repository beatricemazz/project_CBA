import matplotlib.pyplot as plt
import numpy as np
from utils import tornado_data

def plot_tornado(project="MACRO1"):
    """Create tornado diagram for sensitivity analysis of the given project"""
    results, base_m1, base_m2 = tornado_data()
    
    # Get data for the selected project
    project_data = results[project]
    base_npv = base_m1 if project == "MACRO1" else base_m2
    project_name = "Patient-Specific VC" if project == "MACRO1" else "Hospital Sim & Ed"
    
    # Sort parameters by impact range
    parameters = []
    low_values = []
    high_values = []
    
    for param, (low_impact, high_impact) in project_data.items():
        parameters.append(param)
        low_values.append(low_impact)
        high_values.append(high_impact)
    
    # Sort by total impact (absolute sum of low and high impacts)
    impact_ranges = [abs(low) + abs(high) for low, high in zip(low_values, high_values)]
    sorted_indices = np.argsort(impact_ranges)[::-1]  # Sort in descending order
    
    parameters = [parameters[i] for i in sorted_indices]
    low_values = [low_values[i] for i in sorted_indices]
    high_values = [high_values[i] for i in sorted_indices]
    
    # Create plot with larger size
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Set up y-axis
    y_pos = np.arange(len(parameters))
    
    # Plot horizontal bars
    ax.barh(y_pos, high_values, left=0, height=0.4, color='#4CAF50', alpha=0.7, label='Positive Impact')
    ax.barh(y_pos, low_values, left=0, height=0.4, color='#F44336', alpha=0.7, label='Negative Impact')
    
    # Add parameter labels with larger font
    ax.set_yticks(y_pos)
    ax.set_yticklabels(parameters, fontsize=12)
    
    # Add value labels on bars with larger font
    for i, (low, high) in enumerate(zip(low_values, high_values)):
        # Format the values with 2 decimal places
        if low < 0:
            ax.text(low - 0.05, i, f'{low:.2f}', ha='right', va='center', 
                   color='black', fontweight='bold', fontsize=12)
        if high > 0:
            ax.text(high + 0.05, i, f'+{high:.2f}', ha='left', va='center', 
                   color='black', fontweight='bold', fontsize=12)
    
    # Add vertical line at zero (base case)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.7, linewidth=1)
    
    # Add base case value with larger font
    ax.text(0, len(parameters) + 0.5, f'Base Case NPV: €{base_npv:.2f}m', 
            ha='center', va='center', fontweight='bold', fontsize=12,
            bbox=dict(facecolor='white', alpha=0.7))
    
    # Customize plot with larger fonts
    ax.set_title(f'Tornado Diagram - NPV Sensitivity ({project_name})', 
                 fontsize=16, pad=20)
    ax.set_xlabel('Change in NPV (€ millions)', fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    
    # Determine xlim based on data
    max_abs_impact = max(max(abs(min(low_values)), abs(max(high_values))), 0.5)
    ax.set_xlim(-max_abs_impact * 1.2, max_abs_impact * 1.2)
    
    # Legend with larger font
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    
    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    plt.tight_layout()
    print(results["MACRO1"]["Uptake Rate"])  # Dovrebbe restituire una tupla (es. (-3.91, +3.91))
    return fig

def plot_waterfall_chart(project="MACRO1"):
    """Create waterfall chart showing contribution of each factor to NPV"""
    from utils import MACRO1, MACRO2, scenario_npv
    
    if project == "MACRO1":
        project_data = MACRO1
        project_name = "Patient-Specific VC"
    else:
        project_data = MACRO2
        project_name = "Hospital Sim & Ed"
    
    # Baseline with minimal values
    base_npv = scenario_npv(project, 0.6, 0.7, 1.2)  # Pessimistic starting point
    
    # Incremental improvements
    uptake_impact = scenario_npv(project, 1.0, 0.7, 1.2) - base_npv  # Improve uptake to 100%
    compliance_impact = scenario_npv(project, 1.0, 1.0, 1.2) - scenario_npv(project, 1.0, 0.7, 1.2)  # Improve compliance to 100%
    hw_impact = scenario_npv(project, 1.0, 1.0, 1.0) - scenario_npv(project, 1.0, 1.0, 1.2)  # Improve HW cost to 100%
    
    # Final optimistic impact - extra uptake and compliance
    extra_impact = scenario_npv(project, 1.2, 1.3, 0.75) - scenario_npv(project, 1.0, 1.0, 1.0)
    
    # Create plot with larger size
    fig, ax = plt.subplots(figsize=(20, 12))
    
    # Data for waterfall chart
    categories = ['Base Case', 'Uptake\nImprovement', 'Compliance\nImprovement', 
                  'Hardware Cost\nReduction', 'Additional\nOptimistic Factors', 'Optimistic\nOutcome']
    values = [base_npv, uptake_impact, compliance_impact, hw_impact, extra_impact, 0]  # Last value is a placeholder
    
    # Calculate positions and bottom offsets
    cumulative = base_npv
    bottoms = [0]
    for i in range(1, len(values)-1):
        bottoms.append(cumulative)
        cumulative += values[i]
    
    bottoms.append(0)  # Final bar starts at 0
    
    # Colors for different factors
    colors = ['#F44336', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#3F51B5']
    
    # Create bars with larger width
    bar_width = 0.6
    for i in range(len(values)-1):
        ax.bar(categories[i], values[i], bottom=bottoms[i], color=colors[i], 
               width=bar_width, edgecolor='black', linewidth=0.5)
    
    # Final bar (total)
    final_value = base_npv + uptake_impact + compliance_impact + hw_impact + extra_impact
    ax.bar(categories[-1], final_value, bottom=0, color=colors[-1], 
          width=bar_width, edgecolor='black', linewidth=0.5)
    
    # Add value labels on bars with larger font
    for i, v in enumerate(values[:-1]):
        label_text = f'€{v:.1f}m' if i == 0 else (f'+€{v:.1f}m' if v > 0 else f'€{v:.1f}m')
        y_pos = bottoms[i] + v / 2
        label_color = 'white' if abs(v) > 0.5 else 'black'
        ax.text(i, y_pos, label_text, ha='center', va='center', 
                fontweight='bold', color=label_color, fontsize=16)  # Increased font size
    
    # Add final value label with larger font
    ax.text(len(values)-1, final_value / 2, f'€{final_value:.1f}m', 
            ha='center', va='center', fontweight='bold', color='white', fontsize=16)  # Increased font size
    
    # Connect bars with lines
    prev_height = base_npv
    for i in range(1, len(values)-1):
        # Horizontal line from previous bar to current
        ax.plot([i-1+bar_width/2, i-bar_width/2], [prev_height, bottoms[i]], 'k-', linewidth=1, alpha=0.5)
        prev_height = bottoms[i] + values[i]
    
    # Line from last factor to final bar
    ax.plot([len(values)-2+bar_width/2, len(values)-1-bar_width/2], [prev_height, final_value], 'k-', linewidth=1, alpha=0.5)
    
    # Customize plot with larger fonts
    ax.set_title(f'Waterfall Chart - NPV Contributions ({project_name})', 
                 fontsize=24, pad=20)  # Increased font size
    ax.set_ylabel('Net Present Value (€ millions)', fontsize=18)  # Increased font size
    ax.tick_params(axis='y', labelsize=16)  # Increased font size
    ax.tick_params(axis='x', labelsize=16)  # Increased font size
    
    # Set y-axis limits with some padding
    min_val = min(min(values[:-1]), 0)
    max_val = max(final_value, base_npv + sum(values[1:-1]))
    y_range = max_val - min_val
    ax.set_ylim(min_val - 0.1 * y_range, max_val + 0.1 * y_range)
    
    # Add a horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.7, alpha=0.5)
    
    # Add grid lines
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Customize spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    
    plt.tight_layout(rect=[0, 0.08, 1, 0.98])
    
    return fig
