# Water Plume Deposit Erosion Models 

*How long does a deposit from a plume stay on the surface?*

This repository is dedicated to the study of the transient nature of plume deposits on Europa's surface, which is crucial for future missions like JUICE and Europa Clipper. The study investigates the hypothesis that these deposits are not permanent, as they are subjected to various erosion factors.

In this work, we focus on two primary processes: **sputtering** and **radiolysis**, as they are among the most effective erosion mechanisms on Europa.  
To account for variability in erosion factors across Europa’s surface, we simulate each model under three representative location cases:

| Case         | Description                                                              
|--------------|-----------------------------------------------------------------------------------------|
| **Maximum**  | Most erosive: highest sputtering and radiolysis rates  (erodes quicker)                 | 
| **Average**  | Global average values                                                                   | 
| **Minimum**  | Least erosive: best for deposit preservation                                            |


---
##  Models Overview

We implement two simplified models:

- **Model 1** :
  - Confined 10×10 km deposit near the plume source
  -  Assumes uniform deposition (closed system) in a small area.

- **Model 2**:
  - Deposits at 25 km from the source to account for observational limitations.
  - Uses a realistic spatial density profile based on ballistic plume models. 

---
## Collaboration

This project was carried out in collaboration between: 

- Marina Casado-Anarte
- Dr. H. L. F. Huybrighs
- I. Ledwidge

---

## Dependencies

To run the simulations, you will need the following libraries:

- `numpy.py`

- `matplot.lib`

The `density_distribution.py` file is used to compute the plume's spatial density distribution used in model 2, but is not required to run the scripts for the key figures in the paper. These scripts use the density value obtained with `density_distribution.py` for a 1 kg/s plume at 25 km, which is 4.71e+06 Particles per cm³ . If you wish to extract plume density values at different locations then `density_distribution.py` should be modified accordingly.  `density_distribution.py` requires external input files not included here, they are listed below.  For access to these dependencies, please contact **Dr. H. L. F. Huybrighs**.

- `neutral_europa_input.py`

- `orbit_tools.py`

- `coordinate_transformation.py`

- `neutral_trajectories_tools.py`

- `nim_simulation.py`

- `density.py`

- `densityStorage.npy`





