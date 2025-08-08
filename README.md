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



The `density_distribution.py` file is used to compute the **plume's spatial density distribution**.  
This file **requires external input files** and is mainly provided for **contextualisation** (showing where the density value used in Model 2 comes from).

If you wish to change plume density characteristics, this is the file to modify. However, it depends on custom modules described in _Dependencies_ section  **not included here**. For access, please contact **Dr. H. L. F. Huybrighs**.


---
##  Models Overview

We implement two simplified models:

- **Model 1** :
      - Confined 10×10 km deposit near the plume source  
      - Assumes uniform deposition (closed system) in a small area.

- **Model 2**:
      - Deposits at 25 km from the source to account for observational limitations.
      - Uses a realistic spatial density profile based on ballistic plume models. 

---
## Collaboration

This project was carried out in collaboration between: 

- Marina Casado-Anarte
- Dr. H. L. F. Huybrighs
- I. Ledwidg 

---

## Dependencies

To run the simulations, you will need the following libraries:

· `numpy.py`

·`matplot.lib

In order to run `density_distribution.py` you will also need: 

·`neutral_europa_input.py`

·`orbit_tools.py`

·`coordinate_transformation.py`

·`neutral_trajectories_tools.py`

·`nim_simulation.py`

·`density.py`

·`densityStorage.npy






