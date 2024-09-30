#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 12:50:01 2024

@author: marina

This code is for calculating and showing everything in terms of kg/s 
This could be changed later to hours/monts/years 
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Constants
A = 10**8  # Area of the plume source (m^2)
s_r = 3.2e13  # Sputtering rate (ptcls/sm²)
H2O = 2.987e-26  # Kg per particle of H2O 

sputtering_rate = s_r * H2O  # Sputtering (kg/sm²)


# Define the ranges for eruption time and mass flux
eruption_times = np.linspace(1, 30000, 100)  # Eruption times from 1 to 30,000 seconds
mass_flux_rates = np.arange(1, 10000 + 1, 10)  # Mass flux rates from 10 to 10,000 kg/s
    
# CALCULATIONS:
# Calculate total particles erupted
def calculate_total_particles_eruption(mass_flux_rate, t_eruption):
    N = mass_flux_rate * t_eruption
    return N


# Calculate maximum disappearance time
def calculate_max_disappearance_time(total_particles, sputtering_rate):
    return total_particles / (sputtering_rate * A)


# PLOTTING:
# Create a meshgrid for plotting
mass_flux_grid, eruption_time_grid = np.meshgrid(mass_flux_rates, eruption_times)

# Initialize the array for maximum disappearance times
Tmax_grid = np.zeros_like(mass_flux_grid, dtype=float)


# Plotting the heatmap with contours
# Calculate Tmax for each combination of mass flux rate and eruption time
for i in range(len(eruption_times)):
    for j in range(len(mass_flux_rates)):
        total_particles = calculate_total_particles_eruption(mass_flux_rates[j], eruption_times[i])
        Tmax_grid[i, j] = calculate_max_disappearance_time(total_particles, sputtering_rate)

# Plotting the heatmap with contours
plt.figure(figsize=(8, 6))
contour = plt.contour(mass_flux_grid, eruption_time_grid, Tmax_grid, colors='black', linewidths=0.5)
plt.clabel(contour, inline=True, fontsize=8, fmt='%1.1e')
plt.pcolormesh(mass_flux_grid, eruption_time_grid, Tmax_grid, shading='auto', norm=LogNorm(), cmap='viridis')
plt.colorbar(label='Max Disappearance Time (s)')

# Highlight the specific point as this is the plume that was observed 
example_mass_flux_rate = 7000  # Example mass flux rate
example_eruption_time = 25000  # Example eruption time
plt.plot(example_mass_flux_rate, example_eruption_time, 'ro')  # Red point
plt.text(example_mass_flux_rate, example_eruption_time, '  (7000, 25000)', color='black')

plt.xlabel('Mass Flux Rate (kg/s)')
plt.ylabel('Eruption Time (s)')
plt.title('Max Disappearance Time as Function of Mass Flux Rate and Eruption Time')
plt.show()

# Example calculations for print
total_particles = calculate_total_particles_eruption(example_mass_flux_rate, example_eruption_time)
max_disappearance_time = calculate_max_disappearance_time(total_particles, sputtering_rate)
print(f"Total particles erupted: {total_particles:.2E} kg")
print(f"Max disappearance time: {max_disappearance_time:.2E} seconds")
