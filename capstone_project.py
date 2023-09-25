import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors

#the following code is used to load the densityStorage.npy file
#the path file will need to be changed if run on another device. 
f = np.load(r"C:\Users\Isabelle\Documents\europa_tommy_100\input\densityStorage.npy", allow_pickle=True)
#splitting the file into x-y-z coordinates and density data
x, y, z = f[1]
density = f[0]

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
print(inp.conversionFactor_density_ppcc)
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
#density_ppm = (density_ppcc/1e6)
plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
plt.colorbar(label='Density [#/m**3]')
#plt.clim([335,4.2*10**8])
plt.xlabel('Y [km]')
plt.ylabel('Z [km]')
plt.title('Density [#/m**3]')
plt.show()

#now trying to determine surface cells
#europa's radius can be extracted from europa_input_neutral as below
radius = (inp.rEuropa)/1000 #converts to [km]
#there will be a surface at z[radius],[-radius],y[radius],[-radius]

#the following function calculates what the index is at a desired coordinate 
#the indexes are integers but the radius is a float
#the round function rounds any float numbers to the nearest integer value
def Index_Calculator(coord):
    initial_coord = -2995.
    factor = 10
    index = ((coord-initial_coord)/factor)
    return (round(index))

print(f"The index of the positive radius is {Index_Calculator(radius)}")
print(f"The index of the negative radius is {Index_Calculator(-radius)}")
print(z[456],y[456])
print(z[143],y[143])
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

YC,ZC = np.meshgrid(yc,zc)
out = YC ** 2 + ZC ** 2 - radius ** 2 
plt.imshow(density_ppcc[ x_slice,:,  :].T,extent=[x.min(),x.max(),z.min(),z.max()],origin = 'lower', cmap= 'plasma', norm=colors.LogNorm())
plt.colorbar(label='Density [#/m**3]')
#plt.contourf(YC,ZC,YC**2+ZC**2)
plt.contour(YC,ZC,out, [0])
#plt.xlabel('Y [km]')
#plt.ylabel('Z [km]')
#plt.title('Density [#/m**3]')
plt.show()
