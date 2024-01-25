import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import europa_input_neutral 

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 12
#the following code is used to load the densityStorage.npy file
#the path file will need to be changed if run on another device. 
f = np.load(r"C:\Users\Isabelle\Documents\europa_tommy_100\input\densityStorage.npy", allow_pickle=True)
#splitting the file into x-y-z coordinates and density data
x, y, z = f[1]      #[m]
density = f[0]      #[superparticles]

#density is expressed as 'superparticles' (packages of particles)
#to get a density output of individual particles we must factorise
#import europa_input_neutral.py and extract the INPUT() func to do this
inp = europa_input_neutral.INPUT()
#if the above code doesn't work, ensure all necessary files downloaded
#and are in the same directory

#europa's radius can be extracted from europa_input_neutral as below
radius = (inp.rEuropa)     #[m]
velocity = inp.v0[2] * -1    #[m/s]
area = (((inp.gridCellDim1D))**2)    #[m**2]

#the following function calculates what the index is at a desired coordinate 
#using numpy func to round the index up/down and astype(int) to convert float to integer values
def Index_Calculator(coord):
    initial_coord = -2995. *1000      #[m]
    factor = 10 * 1000      #[m]
    index = ((coord-initial_coord)/factor)
    index = np.round(index).astype(int)
    return (index)

#then we can use the formula for mass flux to get the flux of each surface cell
def MassFlux(rho,area,volume):
    m = rho*area*volume
    return m

#this function converts from years to seconds
def YearsToSeconds(years):
    leap_year = (years/4)
    seconds = (years-leap_year) * (24*365*3600)
    leap_year *= (366*24*3600)
    seconds += leap_year
    return seconds

def HoursToSeconds(hours):
    seconds = hours * (60 *60)
    return seconds
#create a func to vary initial inputs of mass flux, eruption time, and time after eruption
#this func outputs the densities, mass fluxes, and particle numbers on europa's surface
#both during and after an eruption.
def DensityChange(density_factor,eruption_time,time_post_eruption):
    density = f[0]      #[superparticles]
    density *= density_factor
    density_ppcc = density * inp.conversionFactor_density_ppcc      #[H2O particles per cm**3]

#the code below attempts to replicate the given figure 8bb from tommy's output
#in this case the yz axes are being plotted while the x-axis is being sliced
#density_ppcc[ x_slice,:,  :].T tells the code to return the density data in #/cc when the x axis is sliced at point x_slice
#extent tells the code what the axis parameters should be
#origin is automatically set to 'upper' so it is manually set to 'lower' 
#x_slice is set to 300 because it will view europa at the exact centre
    x_slice = 300
    plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[(x.min())/1000,(x.max())/1000,(z.min())/1000,(z.max())/1000],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
    plt.colorbar(label='Density [#/$cm^{3}$]')
    plt.xlabel('Y [km]',fontsize=12)
    plt.ylabel('Z [km]',fontsize=12)
    plt.title('Density [#/$cm^{3}$] of Plume Deposits on Europa',fontsize=12)
    plt.show()

#now trying to determine surface cells
#the surface of europa is shaped like a circle 
#so there will be a coordinate at z[radius],[-radius],y[radius],[-radius]
#we want to get all the points of the surface between these indexes
#to do that, we take the index for each quadrant: 0 - radius, radius - 0, 0 - -radius, -radius - 0

#initialising empty lists
#these are to store the z and y coordinates of the surface cells for each quadrant of the circle
    z_coordinates = []
    SecondQuad_z = []
    ThirdQuad_z = []
    LastQuad_z = []

    y_coordinates = []
    SecondQuad_y = []
    ThirdQuad_y = []
    LastQuad_y = []

    print(f"The index for the positive radius coordinate is {Index_Calculator(radius)}")
    print(f"The index for the negative radius coordinate is {Index_Calculator(-radius)}")
    print(f"The index for the zero coordinate is {Index_Calculator(0)}")   
#using the index calculator, i=300 is coord=0, i=456 coord=radius, i=143 coord=-radius
#so the index for each quadrant is from 300-456,456-300,300-143,143-300
#in the case of 456-300 and 300-143, python outputs zero
#to fix this we get the list from 300-456, 143-300, then reverse the list later

#adding these coords to the empty lists by using for loops
    for i in range(300,457):
        z_coordinates.append(z[i])
#using range 300-457 and 300-456 ensures z[456] isn't repeated
    for i in range(300,456):
        SecondQuad_z.append(z[i])
#using range 143-301 and 144-300 ensures z[143] isn't repeated
    for n in range(143,301):
        LastQuad_z.append(z[n])
    for n in range(144,300):
        ThirdQuad_z.append(z[n])

#using range 143-301 and 144-300 ensures y[143] isn't repeated
    for n in range(143,301):
        y_coordinates.append(y[n])
#using range 301-457 and 301-456 ensures y[456] isn't repeated
    for i in range(301, 457):
        SecondQuad_y.append(y[i])
    for i in range(301,456):
        ThirdQuad_y.append(y[i])
    for i in range(144,300):
        LastQuad_y.append(y[i])

#we then use [::-1] which tells python to reverse the list where necessary
#using np.array, the lists are converted to arrays
#the four arrays are combined to a single array using np.append

    z_coordinates = np.array(z_coordinates)
    SecondQuad_z = (SecondQuad_z)[::-1]
    z_coordinates = np.append(z_coordinates,SecondQuad_z)
    LastQuad_z = (np.array(LastQuad_z))
    ThirdQuad_z = (np.array(ThirdQuad_z))[::-1]
    LastQuad_z = np.append(ThirdQuad_z,LastQuad_z)
    z_coordinates = np.append(z_coordinates,LastQuad_z)     #[m]

    y_coordinates = np.array(y_coordinates)
    LastQuad_y = (y_coordinates[::-1])
    ThirdQuad_y = ((ThirdQuad_y)[::-1])
    ThirdQuad_y = np.append(ThirdQuad_y,LastQuad_y)
    SecondQuad_y = np.append(SecondQuad_y,ThirdQuad_y)
    y_coordinates = np.append(y_coordinates,SecondQuad_y)       #[m]

#we now have two arrays for the y and z coordinates of europa's surface, respectively
    print(len(y_coordinates),len(z_coordinates))
#to plot the surface cells on the density map 
#first create a meshgrid from the y and z coordinates
#numpy meshgrid takes the two coordinate vectors and makes a coordinate matrix
#then use the equation of a circle x**2 + y**2 = r**2 to get the circumference of europa's midsection
#this ensures surface cells are connected circularly
    YC,ZC = np.meshgrid(y_coordinates,z_coordinates)
    circumference = YC ** 2 + ZC ** 2 - radius ** 2     #[m]

#plt contour is used to overlay the surface cells on the plot
    ax = plt.contour(YC,ZC,circumference, [0])
    plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
    plt.colorbar(label='Density [#/m**3]')
    plt.xlabel('Y [m]',fontsize=12)
    plt.ylabel('Z [m]',fontsize=12)
    plt.title('Density [#/$cm^{3}$] of Plume Deposits on Europa with Surface Cells Outlined',fontsize=12)
    plt.show()

#we have the y + z coords of each cell
#but they don't take the circular shape of europa into account
#allsegs is a func which returns the points of a contour line
#below array_split splits line 1 ([0] aka the only line)
#into 2 arrays. axis=0 means rows, axis=1 means columns
    coordinates = np.array_split(ax.allsegs[0][0],2,axis = 1)
    z_coordinates = np.array(coordinates[0])
    surface_ycoords= np.array(coordinates[1])
    z_coordinates_transposed = z_coordinates * -1
    y_coordinates_transposed = surface_ycoords *-1
    SurfaceCoordinates_z = np.append(z_coordinates,z_coordinates_transposed)
    SurfaceCoordinates_y = np.append(surface_ycoords,y_coordinates_transposed)

#using the index calculator all indexes can be found 
    SurfaceIndex_y = Index_Calculator(SurfaceCoordinates_y)
    SurfaceIndex_z = Index_Calculator(SurfaceCoordinates_z)

#this code creates a colour plot of the density 
#and a scatter plot of the surface simultaneously
    plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
    plt.colorbar(label='Density [#/$cm^{3}$]')
    plt.xlabel('Y [m]',fontsize=12)
    plt.ylabel('Z [m]',fontsize=12)
    plt.title('Density [#/$cm^{3}$] of Plume Deposits on Europa with Surface Cells as Scattered Points',fontsize=12)
    plt.scatter(SurfaceCoordinates_y,SurfaceCoordinates_z,0.5, c='midnightblue')
    plt.show()

#creating an array corresponding to the km of each cell from the source
    sd = density_ppcc[300,SurfaceIndex_y,SurfaceIndex_z]
    x_axis = []
    for i in range(624):
        km = i * 10
        x_axis.append(km)
    reverse = (x_axis)[::-1]
    x_axis = np.append(x_axis, reverse)
#now we can plot the density distributions
#the x axis corresponds to the point on the surface
#starting at 0 (plume source) and going anticlockwise
#the y axis corresponds to the density at that point

    plt.annotate("Plume Source", xy=(1, sd[0]),  xycoords='data',
            bbox=dict(boxstyle="round", fc="none", ec="gray"),
            xytext=(70, 0), textcoords='offset points', ha='center',
            arrowprops=dict(arrowstyle="->"))
    plt.annotate("North Pole", xy=(x_axis[624],sd[624]),  xycoords='data',
            bbox=dict(boxstyle="round", fc="none", ec="gray"),
            xytext=(-70, 5), textcoords='offset points', ha='center',
            arrowprops=dict(arrowstyle="->"))
    plt.plot(x_axis, density_ppcc[300,SurfaceIndex_y,SurfaceIndex_z], marker='.', c="darkorange")
    plt.title("Density of particles on Europa's Surface",fontsize=12)
    plt.ylabel("Density on a Log Scale",fontsize=12)
    plt.xlabel("Distance from the Plume Source [km]",fontsize=12)
    plt.yscale("log")
    
    plt.grid(True)
    plt.show()
    print(len(density_ppcc[300,SurfaceIndex_y,SurfaceIndex_z]))
    surface_densities = density_ppcc[x_slice,SurfaceIndex_y,SurfaceIndex_z]     #[H2O/cm**3]
    cell_flux = MassFlux(surface_densities,(area*10000),(velocity*1000))       #[H2O/cm**3] * [cm**2] * [cm/s] = [H2O/s]

    plt.plot(cell_flux,marker='.')
    plt.title("Mass Flux on the Surface starting at Europa's South Pole and progressing anti-clockwise",fontsize=12)
    plt.ylabel("Mass Flux on a SymLog Scale",fontsize=12)
    plt.xlabel("Point on Europa's Surface",fontsize=12)
    plt.yscale("log")
    plt.annotate("North Pole",(624,cell_flux[624]),textcoords="offset points", xytext=(0,10),ha='center')
    plt.annotate("South Pole",(1247,cell_flux[1247]),textcoords="offset points", xytext=(0,10),ha='center')
    plt.annotate("Plume Source",(0,cell_flux[0]),textcoords="offset points", xytext=(0,10),ha='center')
    plt.grid(True)
    plt.show()

#the cell flux is in units of particle number per second
#to convert to particle number, multiply by time
    particle_number = cell_flux * eruption_time     #[H2O]
    plt.plot(particle_number,marker='.',c="darkorange")
    plt.title("Particles on the Surface starting at Europa's South Pole and progressing anti-clockwise",fontsize=12)
    plt.ylabel("Particles on a Log Scale",fontsize=12)
    plt.xlabel("Point on Europa's Surface",fontsize=12)
    plt.yscale("log")
    plt.annotate("North Pole",(624,particle_number[624]),textcoords="offset points", xytext=(0,10),ha='center')
    plt.annotate("South Pole",(1247,particle_number[1247]),textcoords="offset points", xytext=(0,10),ha='center')
    plt.annotate("Plume Source",(0,particle_number[0]),textcoords="offset points", xytext=(0,10),ha='center')
    plt.grid(True)
    plt.show()

#from Plainaki 2009, the rate of particles sputtering from Europa's surface is 3.2e13 per second
#multiplying this by the time post-eruption, we can subtract it from the particle numbers
#to find out how many particles remain on the surface (particles_pe = particles post eruption)
    sputter_rate = (3.2e13)     #[H2O/s/m**2]
    print(sputter_rate*area)
    print(SurfaceCoordinates_y[332],SurfaceCoordinates_z[332])
    particle_loss = (sputter_rate)*(time_post_eruption)*(area)        #[H2O]
    particles_pe = (particle_number) - particle_loss        #[H2O]
    plt.plot(x_axis,particles_pe,marker='.',c="yellowgreen")
    plt.title("Particles left on the Surface after 20 years",fontsize=12)
    plt.ylabel("Number of Particles on a Log Scale",fontsize=12)
    plt.xlabel("Distance from Plume Source [km]",fontsize=12)
    plt.yscale("symlog")
    plt.annotate("Plume Source", xy=(1, particles_pe[0]),  xycoords='data',
            bbox=dict(boxstyle="round", fc="none", ec="gray"),
            xytext=(70, 0), textcoords='offset points', ha='center',
            arrowprops=dict(arrowstyle="->"))
    plt.annotate("North Pole", xy=(x_axis[624],particles_pe[624]),  xycoords='data',
            bbox=dict(boxstyle="round", fc="none", ec="gray"),
            xytext=(-70, 5), textcoords='offset points', ha='center',
            arrowprops=dict(arrowstyle="->"))
    plt.grid(True)
    plt.show()
