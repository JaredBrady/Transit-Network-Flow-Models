# Network Flow Models for Transit Planning

This project uses maximum-flow and minimum-cost flow models to analyze passenger movement through a simplified Vancouver transit network. The models are used to estimate network capacity, evaluate cost-efficient routing, and test whether targeted infrastructure changes improve system performance.

Python is used to run GLPK models, read solver outputs, and plot passenger-flow patterns across the network.

## Project Overview

The analysis is organized around a sequence of optimization models:

1. **Baseline Maximum-Flow Analysis**  
   Estimates how much passenger flow the existing bus network can support.

2. **Maximum-Flow with Rail Expansion**  
   Adds high-capacity rail connections and compares the expanded network against the baseline case.

3. **Minimum-Cost Routing to UBC**  
   Routes a fixed level of UBC-bound passenger demand at minimum transportation cost.

4. **Multi-Destination Minimum-Cost Routing**  
   Routes Downtown-bound and UBC-bound passenger demand simultaneously through the shared transit network.

5. **Targeted Route Improvement**  
   Uses sensitivity analysis to guide a targeted route change and evaluates how the change affects total routing cost.

## Key Results

The maximum-flow models show how added rail infrastructure can substantially increase downtown-bound passenger capacity. In the baseline network, the model routes 2,900 passengers per hour into Downtown. After adding rail connections, downtown-bound flow increases to 10,100 passengers per hour.

The minimum-cost models shift the focus from capacity to efficiency. These models route fixed passenger-demand levels at minimum cost, helping to identify how routing choices and capacity limits affect overall transportation cost.

Sensitivity analysis identifies the connection from `MarineGranville` to `Marine41st` as a promising location for added capacity. A targeted route modification using this connection reduces total transportation cost from approximately **$10,826 per hour** to approximately **$10,655 per hour**, a savings of about **$170 per hour** under the same demand assumptions.

## Repository Structure

```text
transit-network-flow-models/
├── transit-network-flow-models.ipynb
├── README.md
├── requirements.txt
├── data/
│   ├── Vancouver_graph.png
│   ├── nodes.txt
│   ├── maxflow_baseline.dat
│   ├── maxflow_expansion.dat
│   ├── mincost_ubc.dat
│   ├── mincost_multi_destination.dat
│   └── mincost_improved_route.dat
├── models/
│   ├── maxflow.mod
│   ├── mincost_ubc.mod
│   └── mincost_multi_destination.mod
├── outputs/
│   ├── sol_maxflow_baseline.txt
│   ├── sol_maxflow_expansion.txt
│   ├── sol_mincost_ubc.txt
│   ├── sol_mincost_multi_destination.txt
│   └── sol_mincost_improved_route.txt
└── src/
    ├── __init__.py
    ├── solve.py
    └── plot.py
```

## Methods and Tools

- Linear optimization
- Maximum-flow models
- Minimum-cost flow models
- Multi-destination network routing
- Sensitivity analysis using dual values
- Python
- GLPK
- Pandas
- Matplotlib

## How to Run

This project requires Python and GLPK.

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

GLPK must also be installed separately so that the `glpsol` command is available from the terminal. On Ubuntu or WSL, it can typically be installed with:

```bash
sudo apt install glpk-utils
```

After the dependencies are installed, open and run:

```text
transit-network-flow-models.ipynb
```

The notebook calls GLPK through helper functions in `src/solve.py` and uses plotting functions in `src/plot.py`.

## Notes

The network is a simplified representation of selected Vancouver transit corridors. Passenger flow is modeled as an hourly rate moving through a directed network. The models are designed for scenario comparison and planning interpretation rather than detailed transit scheduling. Transfer wait times, individual bus schedules, and boarding behavior are not included.

## Acknowledgment

The original concept for this project, along with some raw GLPK model/data files, came from a graduate-level linear programming course. This repository expands that starting point into a complete transit-network analysis focused on scenario comparison, sensitivity analysis, and planning-oriented interpretation.
