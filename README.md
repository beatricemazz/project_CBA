
# Digital twins VR/AR: Cost-Benefit Analysis Sensitivity Visualizations

This project creates comprehensive visualizations for sensitivity analysis in the context of a cost-benefit analysis for two healthcare technology investment options:

1. **Patient-Specific Virtual Care** (Macro-1)
2. **Hospital Simulation & Education Network** (Macro-2)

> ⚠️ **NB:** This project was carried out as part of the first-year Data Science curriculum, within the course Quantitative Models for Economics (QME). Our team completed a systematic review, and in this context, We focused on the statistical analysis and visualization of the data, producing charts, sensitivity analyses, and interactive outputs. You can access the full review by clicking here.

## Core Analysis Modules
- **Monte Carlo Simulation** (`monte_carlo_analysis.py`)  
  Probabilistic modeling of NPV distributions for:
- **Sensitivity Analysis** (`tornado_analysis.py`)   
- **Scenario Analysis** (`scenario_charts.py`)
## Features

The tool provides a range of visualizations to help analyze the sensitivity of economic indicators (NPV, IRR, BCR) to changes in key parameters:

- Scenario analysis (optimistic, expected, pessimistic)
- Tornado diagrams showing impact of individual parameters
- Waterfall charts showing contribution of each factor
- Monte Carlo simulation results with probability distributions
- Break-even analysis for adoption thresholds

## Getting Started

### Prerequisites

- Python 3.8+
- Required libraries: matplotlib, seaborn, pandas, numpy, plotly

### Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

### Running the Analysis

To generate all visualizations at once:

```bash
python main.py
```

This will create all charts and save them in the `output` directory.

## Project Structure

- `utils.py` - Core functions and parameters for cost-benefit calculations
- `scenario_charts.py` - Scenario comparison and break-even analysis charts
- `tornado_analysis.py` - Tornado diagrams and waterfall charts
- `monte_carlo_analysis.py` - Monte Carlo simulation visualizations
- `interactive_dashboard.py` - Combined NPV analysis and summary dashboard
- `main.py` - Script to generate all visualizations

## Key Parameters

The sensitivity analysis focuses on three key parameters:

1. **Uptake Rate** - The percentage of expected adoption (60% to 120%)
2. **Compliance Factor** - The effectiveness of implementation (50% to 130%) 
3. **Hardware Cost Factor** - Variation in hardware costs (75% to 110%)

Additionally, the analysis examines sensitivity to:

- Different discount rates (0.8% SDR to 5.7% WACC)
- Project lifetime (5 to 25 years)

## Output Examples

The visualizations include:

- Scenario comparison charts
- Tornado diagrams for sensitivity analysis
- Monte Carlo simulation distributions
- Break-even adoption factor analysis
- Interactive parameter exploration tools
