import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from collections import Counter


#the following code is used to load the densityStorage.npy file
#the path file will need to be changed if run on another device. 
f = np.load(r"C:\Users\Isabelle\Documents\europa_tommy_100\input\densityStorage.npy", allow_pickle=True)
#splitting the file into x-y-z coordinates and density data
x, y, z = f[1]
density = f[0]
#density *= 1000
#x-y-z are given in meters and are converted to kilometers below
x /= 1000
y /= 1000
z /= 1000

#density is expressed as 'superparticles' (packages of particles)
#to get a density output of individual particles we must factorise
#import europa_input_neutral.py and extract the INPUT() func to do this
import europa_input_neutral 
inp = europa_input_neutral.INPUT()
#if the above code doesn't work, ensure all necessary files dowloaded
#and are in the same directory
#density can be expressed in particles per cubic centimeter or kg per m^3
#print(inp.conversionFactor_density_ppcc)
def DensityChange(d,t,pt):
    density = f[0]
    density *= d
    density_ppcc = density * inp.conversionFactor_density_ppcc

#this code replicates the given figure 3 from tommy's output.
#the graph shows the xy axes, which will correspond to a singular point on the z axis
#the singular point z_slice can be changed to see how xy changes along the z axis
#z has a len of 600 so z_slice can be any integer between 0-600
    z_slice = 100
#density_ppcc[:,:,100] tells the code to return the density data in #/cc when the z axis is sliced at point z_slice
#extent tells the code what the axis parameters should be
#origin is automatically set to 'upper' so it is manually set to 'lower' below
    plt.imshow(density_ppcc[:, :, z_slice], extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='magma')
    plt.colorbar(label='Density [#/cc]')
    plt.xlim(-600,600)
    plt.ylim(-600,600)
    plt.xlabel('X [km]')
    plt.ylabel('Y [km]')
    plt.title(f'Density [#/cc] in XY plane with z coordinate: {z[100]}km')
    plt.show()

#the code below attempts to replicate the given figure 8bb from tommy's output
#in this case the yz axes are being plotted while the x-axis is being sliced
#density_mks[y_slice, :, :].T will transpose the data in kg/m^3 so that the z-coords are now on the y-axis
#density # per cc is converted to # per m**3 as density_ppm
    x_slice = 300
    plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
    plt.colorbar(label='Density [#/m**3]')
    plt.xlabel('Y [km]',fontsize=12)
    plt.ylabel('Z [km]',fontsize=12)
    plt.title('Density [#/m**3] of Europas Atmosphere',fontsize=12)
    plt.show()

#now trying to determine surface cells
#europa's radius can be extracted from europa_input_neutral as below
    radius = (inp.rEuropa)/1000 #converts to [km]
#there will be a surface at z[radius],[-radius],y[radius],[-radius]

#the following function calculates what the index is at a desired coordinate 
    def Index_Calculator(coord):
        initial_coord = -2995.
        factor = 10
        index = ((coord-initial_coord)/factor)
        index = np.round(index).astype(int)
        return (index)

#initialising empty lists
#these are to store the z and y coordinates of the surface cells for each quadrant of the circle
    zc = []
    secondzc = []
    lastzc = []
    thirdzc = []

    yc = []
    second_yq = []
    third_yq = []
    last_yq = []
    zfi = []
    zsi = []
    zti = []
    zli = []

    yfi = []
    ysi = []
    yti = []
    yli = []
#using the index calculator, i=300 is coord=0, i=456 coord=radius, i=143 coord=-radius
#so we want every coordinate between 300-456,456-300,300-143,143-300
#adding these coords to the y and z axis respectively
#by using for loops, ensuring no repitition of the values.
    for i in range(300,457):
        zc.append(z[i])
    for i in range(300,456):
        secondzc.append(z[i])
    for n in range(143,301):
        lastzc.append(z[n])
    for n in range(144,300):
        thirdzc.append(z[n])

    for i in range(300,457):
        zfi.append(i)
    for i in range(300,456):
        zsi.append(i)
    for n in range(143,301):
        zli.append(n)
    for n in range(144,300):
        zti.append(n)
    zfi = np.array(zfi)
    zsi = (zsi)[::-1]
    zfi = np.append(zfi,zsi)
    zli = (np.array(zli))#[::-1]
    zti = (np.array(zti))[::-1]
    zli = np.append(zti,zli)
    zfi = np.append(zfi,zli)

    for n in range(143,301):
        yc.append(y[n])
    for i in range(301, 457):
        second_yq.append(y[i])
    for i in range(301,456):
        third_yq.append(y[i])
    for i in range(144,300):
        last_yq.append(y[i])

    for n in range(143,301):
        yfi.append(n)
    for i in range(301, 457):
        ysi.append(i)
    for i in range(300,456):
        yti.append(i)
    for i in range(143,300):
        yli.append(i)
    yfi = np.array(yfi)
    yli = (yli[::-1])
    yti = ((yti)[::-1])
    yti = np.append(yti,yli)
    ysi = np.append(ysi,yti)
    yfi = np.append(yfi,ysi)
#in the case of 456-300 and 300-143, python outputs zero
#to fix this we get the list from 300-456, 143-300
#we then use [::-1] which tells python to reverse the list
#using np.array, the lists are converted to arrays
#the four arrays are combined to a single array using np.append
    zc = np.array(zc)
    secondzc = (secondzc)[::-1]
    zc = np.append(zc,secondzc)
    lastzc = (np.array(lastzc))#[::-1]
    thirdzc = (np.array(thirdzc))[::-1]
    lastzc = np.append(thirdzc,lastzc)
    zc = np.append(zc,lastzc)

    yc = np.array(yc)
    last_yq = (yc[::-1])
    third_yq = ((third_yq)[::-1])
    third_yq = np.append(third_yq,last_yq)
    second_yq = np.append(second_yq,third_yq)
    yc = np.append(yc,second_yq)

#to plot the surface cells on the density map 
#first create a meshgrid from the y and z coordinates
#numpy meshgrid takes the two coordinate vectors and makes a coordinate matrix
#then use the equation of a circle x**2 + y**2 = r**2
#this ensures surface cells are connected circularly
    YC,ZC = np.meshgrid(yc,zc)
    circumference = YC ** 2 + ZC ** 2 - radius ** 2 

#plt contour is used to plot the surface cells
    ax = plt.contour(YC,ZC,circumference, [0])
    plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
    plt.colorbar(label='Density [#/m**3]')
    plt.xlabel('Y [km]',fontsize=12)
    plt.ylabel('Z [km]',fontsize=12)
    plt.title('Density [#/m**3] with Equation of the Circle Outlined',fontsize=12)
    plt.show()

#we have the y + z coords of each cell
#but they don't take the circular shape of europa into account
#allsegs is a func which returns the points of a contour line
#below array_split splits line 1 ([0] aka the only line)
#into 2 arrays. axis=0 means rows, axis=1 means columns
    coordinate = np.array_split(ax.allsegs[0][0],2,axis = 1)
    z_coordinates = np.array(coordinate[0])
    surface_ycoords= np.array(coordinate[1])
    z_coordinates_transposed = z_coordinates * -1
    y_coordinates_transposed = surface_ycoords *-1
    z_coordinates = np.append(z_coordinates,z_coordinates_transposed)
    surface_ycoords = np.append(surface_ycoords,y_coordinates_transposed)

#using the index calculator all indexes can be found 
#and converted to integers using astype(int)
    surface_yindex = Index_Calculator(surface_ycoords)
    surface_zindex = Index_Calculator(z_coordinates)
    outer = density_ppcc[ x_slice,:,  :].T


#this code creates a scatter plot of the density 
#along the yz axes simultaneously
#some of the coordinates lie in the centre of the circle so first they're removed in a for loop

    plt.imshow(outer,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
    plt.colorbar(label='Density [#/cc]')
    plt.xlabel('Y [km]',fontsize=12)
    plt.ylabel('Z [km]',fontsize=12)
    plt.title('Density [in particles per cubic cm] with Surface Cells as Scattered Points',fontsize=12)
    plt.scatter(surface_ycoords,z_coordinates,0.5, c='midnightblue')
    plt.show()

#now we can plot the density distributions
#the x axis corresponds to the point on the surface
#starting at 0 (plume source) and goiing anticlockwise
#the y axis corresponds to the number of cells with that density

    def MassFlux(p,A,V):
        m = p*A*V
        return m

    velocity = inp.v0[2] * -1
    area = (10**2)

    plt.plot(density_ppcc[300,surface_yindex,surface_zindex], marker='.', c="indigo")
    plt.title("Surface Densities starting at Europa's South Pole and progressing anti-clockwise",fontsize=12)
    plt.ylabel("Density on a Log Scale",fontsize=12)
    plt.xlabel("Point on Europa's Surface",fontsize=12)
    plt.yscale("log")
    plt.grid(True)
    plt.show()
    surface_densities = density_ppcc[x_slice,surface_yindex,surface_zindex]
    cell_flux = MassFlux(surface_densities,area,velocity)

    plt.plot(cell_flux,marker='.')
    plt.title("Mass Flux on the Surface starting at Europa's South Pole and progressing anti-clockwise",fontsize=12)
    plt.ylabel("Mass Flux on a SymLog Scale",fontsize=12)
    plt.xlabel("Point on Europa's Surface",fontsize=12)
    plt.yscale("log")
    plt.grid(True)
    plt.show()

    particle_number = cell_flux * t
    plt.plot(particle_number,marker='.',c="teal")
    plt.title("Particles on the Surface starting at Europa's South Pole and progressing anti-clockwise",fontsize=12)
    plt.ylabel("Particles on a Log Scale",fontsize=12)
    plt.xlabel("Point on Europa's Surface",fontsize=12)
    plt.yscale("log")
    plt.grid(True)
    plt.show()

    sputter_rate = ((3.2e13)*pt)
    particles = particle_number - sputter_rate
    plt.plot(particles,marker='.',c="teal")
    plt.title("Particles left on the Surface starting at Europa's South Pole and progressing anti-clockwise",fontsize=12)
    plt.ylabel("Particles on a Log Scale",fontsize=12)
    plt.xlabel("Point on Europa's Surface",fontsize=12)
    plt.yscale("symlog")
    plt.grid(True)
    plt.show()


DensityChange(100,30000,172800)
