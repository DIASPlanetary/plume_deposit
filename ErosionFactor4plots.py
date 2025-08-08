"""
@author: marina

This is the script for Figure 8 in Casado-anarte et al. 2025. 

It calculates the eosion time of a plume deposit located 25 km away from the source, evaluated
under varying plume mass flux and eruption durations. Each panel isolates the effect of a
single erosion factor, either ion sputtering or radiolysis, under specific surface conditions
representative of different regions on Europa.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

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

# Axes
eruption_times = np.logspace(np.log10(262.8), np.log10(seconds_per_year), 1000)
mass_flux_rates = np.logspace(0, 4, 1000)
mass_flux_grid, eruption_time_grid = np.meshgrid(mass_flux_rates, eruption_times)

# Functions
def calculate_density(rho, mass_flux_rates):
    return rho * mass_flux_rates

def calculate_mass_flux_falling(rho_step, A, v_avg):
    return rho_step * A * v_avg

def calculate_total_particles_eruption(massflux_f, t_eruption):
    return massflux_f * t_eruption

def calculate_max_disappearance_time(total_particles, process_rate):
    return total_particles / (process_rate * A) / seconds_per_year

def compute_grid(process_type, param1, param2):
    if process_type == 'radiolysis':
        rate = param1 * O2 + param2 * H2
    elif process_type == 'sputtering':
        rate = param1 * H2O

    Tmax_grid = np.zeros_like(mass_flux_grid, dtype=float)
    for i in range(len(eruption_times)):
        for j in range(len(mass_flux_rates)):
            rho_step = calculate_density(rho, mass_flux_rates[j])
            massflux_f = calculate_mass_flux_falling(rho_step, A, v_avg)
            total_particles = calculate_total_particles_eruption(massflux_f, eruption_times[i])
            Tmax_grid[i, j] = calculate_max_disappearance_time(total_particles, rate)

    # Red dot value
    rho_step_dot = calculate_density(rho, example_mass_flux_rate)
    massflux_f_dot = calculate_mass_flux_falling(rho_step_dot, A, v_avg)
    total_particles_dot = calculate_total_particles_eruption(massflux_f_dot, example_eruption_time)
    Tmax_dot = calculate_max_disappearance_time(total_particles_dot, rate)

    return Tmax_grid, Tmax_dot

# Compute Tmax grids
T_H_grid, Tmax_T_H = compute_grid('sputtering', 2.251e15 , None)
L_H_grid, Tmax_L_H = compute_grid('sputtering', 1.2e14 + 2.4e14 + 2.1e12, None)
SSP_grid, Tmax_SSP = compute_grid('radiolysis', 9.0e15 + 1.8e16 + 1.4e14 , 2.1e14 + 4.1e14 + 3.3e12)
ASP_grid, Tmax_ASP = compute_grid('radiolysis', 4e15 + 7.8e15 + 6.3e13, 5e13 + 9.9e13 + 8e11)

# Combine grids and compute global min/max
grids = [T_H_grid, L_H_grid, SSP_grid, ASP_grid]
masked_grids = [np.ma.masked_less_equal(g, 0) for g in grids]
global_min = min(np.min(g) for g in masked_grids)
global_max = max(np.max(g) for g in masked_grids)
norm = LogNorm(vmin=global_min, vmax=global_max)
cmap = 'viridis'

# Plotting
fig, axes = plt.subplots(2, 2, figsize=(13, 10), sharex=True, sharey=True)
titles = ['(a) Sputtering at T.H.', '(b) Sputtering at L.H.',
          '(c) Radiolysis at S.S.P.', '(d) Radiolysis at A.S.P.']
Tmax_values = [Tmax_T_H, Tmax_L_H, Tmax_SSP, Tmax_ASP]
grids = [T_H_grid, L_H_grid, SSP_grid, ASP_grid]

# Shared contour levels per row
contour_levels_top = [10**i for i in range(-6, 5)]
contour_levels_bottom = [10**i for i in range(-6, 5)]

for i, (ax, grid, title) in enumerate(zip(axes.flat, grids, titles)):
    pcm = ax.pcolormesh(mass_flux_grid, eruption_time_grid, grid,
                        shading='auto', norm=norm, cmap=cmap)

    # Manual Labels for each plot 
    if i in [0]:  # Top row
        contour = ax.contour(mass_flux_grid, eruption_time_grid, grid,
                             levels=contour_levels_top, colors='black', linewidths=0.5)
        # Manual labels for top panel
        ax.text(6, 7e2, '1.0e-04', fontsize=8, color='black', ha='left', va='center')
        ax.text(22, 2e4, '1.0e-02', fontsize=8, color='black', ha='left', va='center')
        ax.text(180, 1.9e5, '1.0e+00', fontsize=8, color='black', ha='left', va='center')
        ax.text(700, 5e6, '1.0e+02',  fontsize=8, color='black', ha='left', va='center')
        
    elif i in [1]:
        contour = ax.contour(mass_flux_grid, eruption_time_grid, grid,
                             levels=contour_levels_top, colors='black', linewidths=0.5)
        # Manual labels for top panel
        ax.text(1.5, 5e2, '1.0e-04', fontsize=8, color='black', ha='left', va='center')
        ax.text(35, 2000, '1.0e-02', fontsize=8, color='black', ha='left', va='center')
        ax.text(180, 35000, '1.0e+00', fontsize=8, color='black', ha='left', va='center')
        ax.text(550, 1e6, '1.0e+02',  fontsize=8, color='black', ha='left', va='center')

    elif i in [2]:  # Bottom row
        contour = ax.contour(mass_flux_grid, eruption_time_grid, grid,
                             levels=contour_levels_bottom, colors='black', linewidths=0.5)
        # Manual labels for bottom panel
        ax.text(22, 5e2, '1.0e-04', fontsize=8, color='black', ha='left', va='center')
        ax.text(240, 35000, '1.0e-02', fontsize=8, color='black', ha='left', va='center')
        ax.text(700, 1e6, '1.0e+00', fontsize=8, color='black', ha='left', va='center')
        
    elif i in [3]:  # Bottom row
        contour = ax.contour(mass_flux_grid, eruption_time_grid, grid,
                             levels=contour_levels_bottom, colors='black', linewidths=0.5)
        # Manual labels for bottom panel
        ax.text(22, 2000, '1.0e-04', fontsize=8, color='black', ha='left', va='center')
        ax.text(98, 35000, '1.0e-02', fontsize=8, color='black', ha='left', va='center')
        ax.text(400, 1e6, '1.0e+00', fontsize=8, color='black', ha='left', va='center')
        
        

    # White 28-year contour and label
    white_contour = ax.contour(mass_flux_grid, eruption_time_grid, grid,
                               levels=[28], colors='white', linewidths=1.5)
    ax.clabel(white_contour, inline=True, fontsize=9, fmt='28 yr',
              manual=[(5e2, 1e5)])

    # Grey horizontal reference lines
    ax.axhline(y=3600, color='grey', linestyle='-')
    ax.axhline(y=86400, color='grey', linestyle='-')
    ax.axhline(y=2.628e6, color='grey', linestyle='-')
    ax.axhline(y=1.577e7, color='grey', linestyle='-')

    # Grey labels only on left column
    if ax in (axes[0, 0], axes[1, 0]):
        ax.text(1, 3600, '1 h', color='grey', ha='right', va='bottom')
        ax.text(1, 86400, '1 day', color='grey', ha='right', va='bottom')
        ax.text(1, 2.628e6, '1 month', color='grey', ha='right', va='bottom')
        ax.text(1, 1.577e7, '6 months', color='grey', ha='right', va='bottom')

    # Red dot and annotation
    ax.plot(example_mass_flux_rate, example_eruption_time, 'o', color='#D41159')
    ax.text(5e2, 8e3, '7000 kg/s, ~7 h',
            color='#D41159', fontsize=9, ha='left', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')

# Print Tmax values at red dot
print(f"[a] Sputtering at T.H.: Tmax at (7000 kg/s, 25200 s) = {Tmax_T_H:.2f} years")
print(f"[b] Sputtering at L.H. : Tmax at (7000 kg/s, 25200 s) = {Tmax_L_H:.2f} years")
print(f"[c] Radiolysis at S.S.P. : Tmax at (7000 kg/s, 25200 s) = {Tmax_SSP:.2f} years")
print(f"[d] Radiolysis at A.S.P. : Tmax at (7000 kg/s, 25200 s) = {Tmax_ASP:.2f} years")

# Shared labels
fig.supxlabel('Mass Flux Rate (kg/s)', fontsize=14)
fig.supylabel('Eruption Time (seconds)', fontsize=14)

# Shared colorbar
cbar = fig.colorbar(pcm, ax=axes.ravel().tolist(), shrink=0.95)
cbar.set_label('Erosion Time (years)', fontsize=12)

plt.show()
