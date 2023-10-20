import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import plotly.express as pe
import os
import math

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
density_ppcc = density * inp.conversionFactor_density_ppcc
density_mks = density * inp.conversionFactor_density_mks

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
plt.xlabel('Y [km]')
plt.ylabel('Z [km]')
plt.title('Density [#/m**3]')
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
    return (index)

print(f"The index of the positive radius is {Index_Calculator(radius)}")
print(f"The index of the negative radius is {Index_Calculator(-radius)}")

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

for n in range(143,301):
    yc.append(y[n])
for i in range(301, 457):
    second_yq.append(y[i])
for i in range(301,456):
    third_yq.append(y[i])
for i in range(144,300):
    last_yq.append(y[i])

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
out = YC ** 2 + ZC ** 2 - radius ** 2 


#plt contour is used to plot the surface cells
ax = plt.contour(YC,ZC,out, [0])
plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
plt.colorbar(label='Density [#/m**3]')
plt.xlabel('Y [km]')
plt.ylabel('Z [km]')
plt.title('Density [#/m**3] with Equation of the Circle Outlined')
plt.show()

#we have the y + z coords of each cell
#but they don't take the circular shape of europa into account
#allsegs is a func which returns the points of a contour line
#below array_split splits line 1 ([0] aka the only line)
#into 2 arrays. axis=0 means rows, axis=1 means columns
coordinate = np.array_split(ax.allsegs[0][0],2,axis = 1)
z_coordinates = np.array(coordinate[0])
y_coordinates= np.array(coordinate[1])
z_coordinates_transposed = z_coordinates * -1
y_coordinates_transposed = y_coordinates *-1
z_coordinates = np.append(z_coordinates,z_coordinates_transposed)
y_coordinates = np.append(y_coordinates,y_coordinates_transposed)

#using the index calculator all indexes can be found 
#and converted to integers using astype(int)

y_index = Index_Calculator(y_coordinates)
z_index = Index_Calculator(z_coordinates)
y_index = y_index.astype(int)
z_index = z_index.astype(int)
outer = density_ppcc[ x_slice,:,  :].T

#to confirm coordinates are correct we print a scatter plot of our density map
#plt.imshow(outer,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
#plt.colorbar(label='Density [#/m**3]')
#plt.scatter(y_coordinates,z_coordinates, s=0.8, c='black')
#plt.xlabel('Y [km]')
#plt.ylabel('Z [km]')
#plt.title('Density [#/m**3] with Surface Cells as Scattered Points')
#plt.show()

#print(y_coordinates)
#the densities of the surface cells can now be stored in an array
#and plotted
surface_densities = density_ppcc[x_slice,y_index,z_index]

plt.plot(surface_densities,y_index)
plt.title("Surface Density vs Surface Index")
plt.xlabel("Surface Density")
plt.ylabel("Surface Index")
plt.show()

#this code creates a scatter plot of the density 
#along the yz axes simultaneously
#some of the coordinates lie in the centre of the circle so first they're removed in a for loop
zero = []
yzero = []
for i in range(len(surface_densities)):
    if surface_densities[i] == 0:
        #print(y_index[i],z_index[i])
        #zero.append(i)
        y_coordinates[i] = y_coordinates[i] + 5
        z_coordinates[i] = z_coordinates[i] + 5
        #surface_densities[i] = surface_densities[i+2]
y_index = Index_Calculator(y_coordinates)
z_index = Index_Calculator(z_coordinates)
y_index = y_index.astype(int)
z_index = z_index.astype(int)
surface_densities = density_ppcc[x_slice,y_index,z_index]
plt.imshow(outer,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
plt.colorbar(label='Density [#/cc]')
#plt.scatter(y_coordinates,z_coordinates, s=0.8, c='black')
plt.xlabel('Y [km]',fontsize=12)
plt.ylabel('Z [km]',fontsize=12)
plt.title('Density [in particles per cubic cm] with Surface Cells as Scattered Points',fontsize=12)
plt.scatter(y_coordinates,z_coordinates,0.5, c='midnightblue')
plt.show()
#surface_densities = np.delete(surface_densities,zero)
#y_coordinates = np.delete(y_coordinates,zero)
#z_coordinates = np.delete(z_coordinates,zero)

#print(len(surface_densities),len(y_coordinates),len(z_coordinates))
#fig, ax1 = plt.subplots()
#ax1.scatter(surface_densities, y_coordinates,2, color='darkblue')
#ax2 = ax1.twinx()
#ax2.scatter(surface_densities, z_coordinates,2, color='darkorange')
#fig.tight_layout()
#plt.title("Densities of each Y Coordinate (blue) and Z Coordinate (orange)")
#plt.xlabel("Density")
#plt.show()


#now we can plot a histogram of the density distributions
#the x axis corresponds to the density value
#the y axis corresponds to the number of cells with that density
plt.plot(surface_densities, marker='.', c="indigo")
plt.title("Surface Densities starting at Europa's South Pole and progressing anti-clockwise",fontsize=12)
plt.ylabel("Density on a Log Scale",fontsize=12)
plt.xlabel("Point on Europa's Surface",fontsize=12)
plt.yscale("log")
plt.grid(True)
plt.show()
mp = 1066/2
plt.scatter(y_index,z_index, 0.1)
plt.show()

eek = []
for j in range(len(surface_densities)):
    if surface_densities[j] >= 1e4:
        eek.append(j)
        print(y_coordinates[j])
        print(surface_densities[j])

plt.imshow(outer,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
plt.colorbar(label='Density [#/m**3]')
#plt.scatter(y_coordinates,z_coordinates, s=0.8, c='black')
plt.xlabel('Y [km]')
plt.ylabel('Z [km]')
plt.title('Density [#/m**3] with Surface Cells as Scattered Points')
plt.scatter(y_coordinates[eek],z_coordinates[eek],0.5)
plt.show()

def MassFlux(p,A,V):
    m = p*A*V
    return m

v = inp.v0[2]
a = inp.gridCellDim1D
plt.plot(MassFlux(surface_densities,a,v),marker='.')
plt.yscale("symlog")
plt.show()




