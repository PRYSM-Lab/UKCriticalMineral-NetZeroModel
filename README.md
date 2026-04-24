# UKCriticalMineral-NetZeroModel
Repository for data and code for the paper: "The Critical Bottleneck of Minerals: How Supply Constraints Pivot the UK Net-Zero Transition from Electrification to Hydrogen"
Raw Material Bottlenecks: Shaping the UK Net-Zero Transition under Critical Mineral Constraints
⸻
📌 Overview

This repository presents a multi-period mixed-integer linear programming (MILP) model for analysing the UK’s integrated energy system under critical mineral constraints.

The model co-optimises long-term investment and short-term operation of a fully integrated energy system—including electricity, hydrogen, natural gas, heating, and carbon transport and storage—under a net-zero emissions target by 2050.
⸻
🧠 Model Description

The optimisation framework:

* Simultaneously determines:

    * Investment decisions (installed capacity of technologies)
    * Operational dispatch at hourly resolution
* Objective:

    * Minimise total system cost subject to net-zero emissions constraints by 2050

Key features:

* Multi-energy system integration:

    * Electricity, gas, hydrogen, and heating sectors
* High temporal resolution:

    * Hourly operation
* Spatial resolution:

    * Captures regional heterogeneity across the UK
* Technical constraints:

    * Ramping limits of dispatchable units
    * Minimum and maximum generation capacities
    * Land-use constraints for renewables
    * System adequacy (e.g., spinning reserve)
* Sector coupling:

    * Strong focus on heating decarbonisation

📎 Full mathematical formulation is available in the Supplementary Materials (Section S.2).
⸻
⛏️ Critical Mineral Module

Material demand is quantified using a material intensity matrix covering 24 technologies along the UK decarbonisation pathway.


* Linking energy system expansion with critical mineral demand
* Identifying material bottlenecks
⸻
📂 Input Data

Main input files:

* elec_h2.xlsx 
* → Core system input data (energy system configuration)

* mineral.xlsx 
* → Critical mineral intensity data for technologies
⸻
⚙️ How to Run

1. Place input files in the project directory:

    * elec_h2.xlsx
    * mineral.xlsx

2. Run the main script:

python Multi-Objective.py


Execution steps:

* Step 1:

    * Model is solved for the baseline

* Step 2:

    * Multi-objective optimisation is performed across different scenarios
⸻
🎯 Customisation

Users can modify the final section of:

Multi-Objective.py


to:

* Focus on specific critical minerals
* Reduce computational time
* Explore targeted bottleneck scenarios
⸻
📊 Results

* Model outputs are provided based on analyses presented in the paper
* Results are available in the repository folders
⸻
📈 Figures and Plots

* All figures used in the paper are included
* Plotting scripts are available in:

/3


Users can reproduce all visualisations directly
⸻
📁 Project Structure

project/
│
├── elec_h2.xlsx          # Energy system input data
├── mineral.xlsx          # Critical mineral data
├── Multi-Objective.py    # Main optimisation model
├── results/              # Model outputs
├── 3/                    # Plotting scripts and figures
└── README.md

⸻
🧪 Reproducibility

To reproduce the results:

1. Ensure input files are correctly placed
2. Run the main script
3. Use plotting scripts to regenerate figures
⸻


📬 Contact

Mohammad Hemmati m.hemmati@ucl.ac.uk
