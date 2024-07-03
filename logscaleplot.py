#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 12:37:27 2024

@author: marina

This code shows the eruption time from less than an hour up to 12 months in log-scale
It calculates and shows the mass flux in kg/s, the range of interest [1,10000]kg/s
The disappearance time is shown in terms of years for convenience for the reader
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Constants
A = 10**8  # Area of the plume source (m^2)
s_r = 3.2e13  # Sputtering rate (ptcls/sm²)
H2O = 2.987e-26  # Kg per particle of H2O 

sputtering_rate = s_r * H2O  # Sputtering conversion (kg/sm²)

seconds_per_month = 2.628e6  # Conversion factor: seconds per month
seconds_per_year = 3.154e+7 # Conversion factor: seconds per year

# Define the ranges for eruption time and mass flux
eruption_times = np.logspace(np.log10(262.800288), np.log10(3.154e+7), 1000)  # Eruption times from less than 1 month to 12 months
mass_flux_rates = np.logspace(0, 4, 1000)# Mass flux rates from 1 to 10,000 kg/s in log-space
                                       

# CALCULATIONS:
# Calculate total particles erupted
def calculate_total_particles_eruption(mass_flux_rate, t_eruption):
    N = mass_flux_rate * t_eruption  # Convert time to seconds
    return N

# Calculate maximum disappearance time
def calculate_max_disappearance_time(total_particles, sputtering_rate):
    return total_particles / (sputtering_rate * A) / seconds_per_year  # Convert time to years


# PLOTTING:
# Create a meshgrid for plotting
mass_flux_grid, eruption_time_grid = np.meshgrid(mass_flux_rates, eruption_times)

# Initialize the array for maximum disappearance times
Tmax_grid = np.zeros_like(mass_flux_grid, dtype=float)

# Calculate Tmax for each combination of mass flux rate and eruption time
for i in range(len(eruption_times)):
    for j in range(len(mass_flux_rates)):
        total_particles = calculate_total_particles_eruption(mass_flux_rates[j], eruption_times[i])
        Tmax_grid[i, j] = calculate_max_disappearance_time(total_particles, sputtering_rate)

# Plotting the "heatmap" = Tmax with contours 
# I did the labels for the contours manually because clabel( ) was not working properly 
plt.figure(figsize=(8,6))
contour = plt.contour(mass_flux_grid, eruption_time_grid, Tmax_grid, levels= [1,10e2,10e4,10e6] ,colors='black', linewidths=0.5)
plt.text (3.5, 1000, '1.0e+00' ,fontsize=8, color='black', ha='left', va='center') 
plt.text (755, 4000, '1.0e+03' ,fontsize=8, color='black', ha='left', va='center') 
plt.text (700, 450000, '1.0e+05' ,fontsize=8, color='black', ha='left', va='center') 
plt.text (3500, 1e7, '1.0e+07' ,fontsize=8, color='black', ha='left', va='center') 
plt.pcolormesh(mass_flux_grid, eruption_time_grid, Tmax_grid, shading='auto', norm=LogNorm(), cmap='viridis')
plt.colorbar(label='Max Disappearance Time (years)')


# Add the contour line for Tmax = 28 years
c28 = plt.contour(mass_flux_grid, eruption_time_grid, Tmax_grid, levels=[28], colors='white', linewidths=1.5)
plt.text(5, 20000, '28 years', color='white', ha='left', va='center')


# Highlight the specific point as this is the plume that was observed
example_mass_flux_rate = 7000  # Example mass flux rate (in kg/s)
example_eruption_time = 25200  # Eruption of 7h (converted to months)
plt.plot(example_mass_flux_rate, example_eruption_time, 'ro')  # Red point
plt.text(example_mass_flux_rate*0.4, example_eruption_time * 0.8, '(7000 kg/s, ~7h)', color='black', ha='center', va='top')


# Reference lines in the y-axis text 
plt.axhline(y = 3600, color = 'grey', linestyle='-', label = '1 h')  # 1 h reference line 
plt.text(0.8, 3600, '1 h', color='grey', ha='right', va='bottom')

plt.axhline(y = 86400, color='grey', linestyle='-', label='1 day')  # 1 day reference line 
plt.text(0.8, 60000, '1 day', color='grey', ha='right', va='bottom')

plt.axhline(y=2.628e+6, color='grey', linestyle='-', label='1 month')  # 1 month reference line 
plt.text(0.8, 2.628e+6, '1 month', color='grey', ha='right', va='bottom')

plt.axhline(y=1.577e+7, color='grey', linestyle='-', label='6 months')  # 6 months reference line 
plt.text(0.8, 1.577e+7, '6 months', color='grey', ha='right', va='bottom')

# Plotting 
plt.xlabel('Mass Flux Rate (kg/s)')
plt.ylabel('Eruption Time (seconds)', labelpad = 15)
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.xscale('log')  # Set x-axis to logarithmic scale
plt.title('Erosion Time of Particles due to Sputtering as Function of Mass Flux and Eruption Time')
plt.show()

# Example calculations for print ( i used this to check the changes I was doing along the way)
total_particles = calculate_total_particles_eruption(example_mass_flux_rate, example_eruption_time)
max_disappearance_time = calculate_max_disappearance_time(total_particles, sputtering_rate)
print(f"Total particles erupted: {total_particles:.2E} kg")
print(f"Max disappearance time: {max_disappearance_time:.2E} years")
