"""
@author: marina

This is a python script for Figure 8 in Marina et al. 2025.

It shows the combined effect of radiolysis and ion sputtering on the erosion of a plume
deposit located 25 km from the source in its most extremem and mininal effect.
This is evaluated  across a range of plume eruption durations and mass fluxes.

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec

# Shared constants
A = 1e8  # Area of the box in m³
v_avg = 460  # Average particle velocity (m/s²)
density_ppcc = 3.3e10 / 7000  # Ptc/cm³ for a plume of m = 1 kg/s
H2O = 2.987e-26  # Kg per particle of H2O
O2 = 5.3137E-26   # Kg per particle of O2
H2 = 3.3543E-27  # Kg per particle of H2
distance_conversion = 1e6
rho = density_ppcc * H2O * distance_conversion
seconds_per_year = 3.154e+7

# Red dot (HST-typle Plume)
example_mass_flux_rate = 7000
example_eruption_time = 25200

# Parameter grid
eruption_times = np.logspace(np.log10(262.800288), np.log10(3.154e+7), 1000)
mass_flux_rates = np.logspace(0, 4, 1000)
mass_flux_grid, eruption_time_grid = np.meshgrid(mass_flux_rates, eruption_times)

# Functions
def calculate_density(rho, mass_flux_rates):
    return rho * mass_flux_rates

def calculate_mass_flux_falling(rho_step, A, v_avg):
    return rho_step * A * v_avg

def calculate_total_particles_eruption(massflux_f, t_eruption):
    return massflux_f * t_eruption

def calculate_max_disappearance_time(total_particles, erosion):
    return total_particles / (erosion * A) / seconds_per_year

def compute_tmax_grid(radrate_O2, radrate_H2, srate):
    radiolysis_O2 = radrate_O2 * O2
    radiolysis_H2 = radrate_H2 * H2
    radiolysis = radiolysis_O2 + radiolysis_H2
    s_r = srate * H2O
    erosion = radiolysis + s_r

    Tmax_grid = np.zeros_like(mass_flux_grid, dtype=float)
    for i in range(len(eruption_times)):
        for j in range(len(mass_flux_rates)):
            rho_step = calculate_density(rho, mass_flux_rates[j])
            massflux_f = calculate_mass_flux_falling(rho_step, A, v_avg)
            total_particles = calculate_total_particles_eruption(massflux_f, eruption_times[i])
            Tmax_grid[i, j] = calculate_max_disappearance_time(total_particles, erosion)

    # Red dot value
    rho_step_dot = calculate_density(rho, example_mass_flux_rate)
    massflux_f_dot = calculate_mass_flux_falling(rho_step_dot, A, v_avg)
    total_particles_dot = calculate_total_particles_eruption(massflux_f_dot, example_eruption_time)
    Tmax_dot = calculate_max_disappearance_time(total_particles_dot, erosion)

    return Tmax_grid, Tmax_dot

# Compute both grids
Tmax_max, Tmax_dot_max = compute_tmax_grid(radrate_O2=2.714e16, radrate_H2=6.23e14, srate=2.251e15)
Tmax_min, Tmax_dot_min = compute_tmax_grid(radrate_O2=1.1863e16, radrate_H2=1.498e14, srate=3.621e14)

# Print values at red dot
print(f"[LEFT] Maximum case: Tmax at (7000 kg/s, 25200 s) = {Tmax_dot_max:.2e} years")
print(f"[RIGHT] Minimum case: Tmax at (7000 kg/s, 25200 s) = {Tmax_dot_min:.2e} years")

# Plotting Section
fig = plt.figure(figsize=(15, 6))
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 0.05], wspace=0.15)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1, sharey=ax1)
cax = fig.add_subplot(gs[2])

axes = [ax1, ax2]
grids = [Tmax_max, Tmax_min]
titles = [
    'Maximum Case: Erosion Time of Deposit 25 km from Plume Source',
    'Minimum Case: Erosion Time of Deposit 25 km from Plume Source'
]

# Contour levels for black lines
contour_levels = [10**i for i in range(-6, 5)]

for idx, (ax, Tmax, title) in enumerate(zip(axes, grids, titles)):
    pcm = ax.pcolormesh(mass_flux_grid, eruption_time_grid, Tmax,
                        shading='auto', norm=LogNorm(), cmap='viridis')

    # Black contours 
    contour = ax.contour(mass_flux_grid, eruption_time_grid, Tmax,
                         levels=contour_levels, colors='black', linewidths=0.5)

    # Grey reference lines and labels
    ax.axhline(y=3600, color='grey', linestyle='-')
    ax.axhline(y=86400, color='grey', linestyle='-')
    ax.axhline(y=2.628e+6, color='grey', linestyle='-')
    ax.axhline(y=1.577e+7, color='grey', linestyle='-')

    if idx == 0:  # Only label on left panel
        ax.text(1, 3600, '1 h', color='grey', ha='right', va='bottom')
        ax.text(1, 60000, '1 day', color='grey', ha='right', va='bottom')
        ax.text(1, 2.628e+6, '1 month', color='grey', ha='right', va='bottom')
        ax.text(1, 1.577e+7, '6 months', color='grey', ha='right', va='bottom')

    # Manual black contour labels
    if idx == 0:  # Left panel
        ax.text(2, 7e2, '1.0e-06', fontsize=8, color='black', ha='left', va='center')
        ax.text(14, 8e3, '1.0e-04', fontsize=8, color='black', ha='left', va='center')
        ax.text(80, 1.2e5, '1.0e-02', fontsize=8, color='black', ha='left', va='center')
        ax.text(700, 1.1e6, '1.0e+00', fontsize=8, color='black', ha='left', va='center')

    elif idx == 1:  # Right panel
      #  ax.text(1.5, 5e2, '1.0e-04', fontsize=8, color='black', ha='left', va='center')
        ax.text(35, 2000, '1.0e-04', fontsize=8, color='black', ha='left', va='center')
        ax.text(180, 35000, '1.0e-02', fontsize=8, color='black', ha='left', va='center')
        ax.text(550, 1e6, '1.0e+00', fontsize=8, color='black', ha='left', va='center')

    # Red dot
    ax.plot(example_mass_flux_rate, example_eruption_time, 'o', color='#D41159')
    ax.text(8e2, 2e4, '7000 kg/s, ~7 h',
            color='#D41159', fontsize=9, ha='left', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')

# Manual 28-year white contour 
white_contour1 = ax1.contour(mass_flux_grid, eruption_time_grid, Tmax_max,
                             levels=[28], colors='white', linewidths=1.5)
ax1.clabel(white_contour1, inline=True, fontsize=10, fmt='28 yr',
           manual=[(5e2, 1e5)])

white_contour2 = ax2.contour(mass_flux_grid, eruption_time_grid, Tmax_min,
                             levels=[28], colors='white', linewidths=1.5)
ax2.clabel(white_contour2, inline=True, fontsize=10, fmt='28 yr',
           manual=[(5e2, 1e5)])

# Shared axis labels
fig.supxlabel('Mass Flux Rate (kg/s)', fontsize=12)
fig.supylabel('Eruption Time (seconds)', fontsize=12)

# Colorbar
fig.colorbar(pcm, cax=cax, label='Erosion Time (years)')

plt.show()
