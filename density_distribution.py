import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import europa_input_neutral

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 12

# Load the data
file_path = r"/home/marina/Desktop/Dias/plume_deposit/tommy libraries/output_neutral/densityStorage.npy"
f = np.load(file_path, allow_pickle=True)

# Check the shape and size of the data
print(f"Data shape: {f.shape}")

# Splitting the file into x-y-z coordinates and density data
x, y, z = f[1], f[2], f[3]  # Adjust indices if necessary
density = f[0]  # [superparticles]

# Check the shape of coordinates and density
print(f"x shape: {x.shape}, y shape: {y.shape}, z shape: {z.shape}, density shape: {density.shape}")

# Density conversion factor
inp = europa_input_neutral.INPUT()

# Europa's radius, velocity, and area
radius = inp.rEuropa  # [m]
velocity = inp.v0[2] * -1  # [m/s]
area = (inp.gridCellDim1D) ** 2  # [m**2]

# Function to calculate index at a desired coordinate
def Index_Calculator(coord):
    initial_coord = -2995.0 * 1000  # [m]
    factor = 10 * 1000  # [m]
    index = (coord - initial_coord) / factor
    index = np.round(index).astype(int)
    return index

# Function to calculate mass flux
def MassFlux(rho, area, volume):
    m = rho * area * volume
    return m

# Function to convert years to seconds
def YearsToSeconds(years):
    leap_year = years / 4
    seconds = (years - leap_year) * (24 * 365 * 3600)
    leap_year *= 366 * 24 * 3600
    seconds += leap_year
    return seconds

def HoursToSeconds(hours):
    seconds = hours * 60 * 60
    return seconds

# Function to vary initial inputs of mass flux, eruption time, and time after eruption
def DensityChange(density_factor, eruption_time, time_post_eruption):
    density = f[0]  # [superparticles]
    density *= density_factor
    density_ppcc = density * inp.conversionFactor_density_ppcc  # [H2O particles per cm**3]

    x_slice = 300
    plt.imshow(density_ppcc[x_slice, :, :].T,
               extent=[(x.min()) / 1000, (x.max()) / 1000, (z.min()) / 1000, (z.max()) / 1000],
               origin='lower', cmap='plasma', norm=colors.LogNorm())
    plt.colorbar(label='Density [#/$cm^{3}$]')
    plt.xlabel('Y [km]', fontsize=12)
    plt.ylabel('Z [km]', fontsize=12)
    plt.title('Density [#/$cm^{3}$] of Plume Deposits on Europa', fontsize=12)
    plt.show()

# Test the function with sample parameters
DensityChange(1.0, 1.0, 1.0)
