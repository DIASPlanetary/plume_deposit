# Erosion Time of Plume Deposits on Europa's Surface

*How long does a deposit from a plume stay on the surface?*

This repository is dedicated to the study of the transient nature of plume deposits on Europa's surface, which is crucial for future missions like JUICE and Europa Clipper. The study investigates the hypothesis that these deposits are not permanent, as they are subjected to various erosion factors.

In this work, we focus on two primary processes: **sputtering** and **radiolysis**, as they are among the most effective erosion mechanisms on Europa.  
- **Sputtering** occurs when high-energy ions eject particles from the surface.  
- **Radiolysis** decomposes water molecules, producing oxygen (O₂) and potentially hydrogen (H₂) [1][2][3].

This code models and simulates the erosion time of plume deposits, analyzing 10 different cases depending on the plume's location and the erosion factor being considered.  
The `density_distribution.py` file is primarily used to compute the **density distribution of the plume** for this model, which is crucial for understanding how the deposits spread across Europa’s surface.

---

## Project Objectives

- **Analyze** the erosion time of plume deposits on Europa's surface.
- **Simulate** different cases of erosion based on plume location and environmental conditions.
- **Predict** how plume deposits evolve under the effects of sputtering and radiolysis.

## Collaboration

This project was carried out in collaboration between *Marina Casado-Anarte* and *Dr. H. L. F. Huybrighs*. The project is currently a work in progress.

---

## Dependencies

To run the simulations, you will need the following libraries:
`numpy.py`
In order to run `density_distribution.py` you will also need: 
`neutral_europa_input.py`
`orbit_tools.py`
`coordinate_transformation.py`
`neutral_trajectories_tools.py`
`nim_simulation.py`
`density.py`



---

## References
[1] Plainaki, C., et al. (2012). Role of sputtering and radiolysis in Europa's surface composition.
[2] Johnson, R. E. (2009). Composition and detection of Europa's atmosphere.
[3] Szalay, J. R., et al. (2024). Oxygen dynamics in Europa's exosphere.
