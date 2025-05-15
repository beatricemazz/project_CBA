import matplotlib.pyplot as plt
import os

# Create output directory if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

# Import visualization modules
from scenario_charts import (
    plot_scenario_comparison,
    plot_discount_rate_sensitivity,
    plot_break_even_analysis
)
from tornado_analysis import plot_tornado, plot_waterfall_chart
from monte_carlo_analysis import (
    plot_monte_carlo_distribution_patient,
    plot_monte_carlo_distribution_hospital)


# Set Matplotlib style for consistent, professional look
plt.style.use('seaborn-whitegrid')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'axes.titlesize': 20,        # Titolo del grafico
    'axes.labelsize': 18,        # Etichette assi
    'xtick.labelsize': 16,       # Etichette asse X
    'ytick.labelsize': 16,       # Etichette asse Y
    'legend.fontsize': 16,       # Legenda
    'figure.figsize': (10, 7),
    'figure.dpi': 100
})


def generate_all_visualizations():
    """Generate all visualizations and save them to the output directory"""
    print("Generating sensitivity analysis visualizations...")
    
    # 1. Scenario comparison chart
    fig = plot_scenario_comparison()
    fig.savefig('output/scenario_comparison.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Scenario comparison chart")
    
    # 2. Discount rate sensitivity chart
    fig = plot_discount_rate_sensitivity()
    fig.savefig('output/discount_rate_sensitivity.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Discount rate sensitivity chart")
    
    # 3. Break-even analysis chart
    fig = plot_break_even_analysis()
    fig.savefig('output/break_even_analysis.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Break-even analysis chart")
    
    # 4. Tornado diagrams for both projects
    fig = plot_tornado("MACRO1")
    fig.savefig('output/tornado_macro1.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    fig = plot_tornado("MACRO2")
    fig.savefig('output/tornado_macro2.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Tornado diagrams")

    
    # 5. Waterfall charts for both projects
    fig = plot_waterfall_chart("MACRO1")
    fig.savefig('output/waterfall_macro1.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    fig = plot_waterfall_chart("MACRO2")
    fig.savefig('output/waterfall_macro2.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Waterfall charts")
    
    fig1 = plot_monte_carlo_distribution_patient()
    fig1.savefig("monte_carlo_patient.png", dpi=300, bbox_inches='tight')

    fig2 = plot_monte_carlo_distribution_hospital()
    fig2.savefig("monte_carlo_hospital.png", dpi=300, bbox_inches='tight')
    
    
    print("\nAll visualizations generated successfully!")
    print(f"Output files saved to the 'output' directory")

if __name__ == "__main__":
    generate_all_visualizations()