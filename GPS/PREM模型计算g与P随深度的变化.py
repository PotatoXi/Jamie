import numpy as np
import matplotlib.pyplot as plt

G = 6.672e-11  # Universal gravitational constant in m^3/s^2
Radius = [0, 1221.5, 3480, 5701, 5771, 5971, 6151, 6346.6, 6356, 6368 ]  # Earth's radii in km
depth_earth = np.linspace(0, 6371, 6371)  # Depths from 0 to 6371

# depth (km) ,reference Earth Model (PREM)
def calculate_density(depth):
    radius = 6371 - depth
    x = radius / 6371  # Normalize depth 
    if radius < Radius[1]:
        density = 13.0885 - 8.8381* x**2  # Inner Core
    elif radius < Radius[2]:
        density = 12.5815 - 1.2638 * x - 3.6426 * x**2 - 5.5281 * x**3  # Outer Core
    elif radius < Radius[3]:
        density = 7.9565 - 6.4761 * x + 5.5283 * x**2 - 3.0807 * x**3  # Lower Mantle
    elif radius < Radius[4]:
        density = 5.3197 - 1.4836 * x  # Transition Zone 1
    elif radius < Radius[5]:
        density = 11.2494 - 8.0298 * x   # Transition Zone 2
    elif radius < Radius[6]:
        density = 7.1089 - 3.8045 * x  # Transition Zone 23
    elif radius < Radius[7]:
        density = 2.6910 + 0.6924*x   # LVZ LID
    elif radius < Radius[8]:
        density = 2.9   # Crust2
    elif radius < Radius[9]:
        density = 2.6# Crust1
    else:
        density = 1.02  # Ocean
        
    return density

prem_density = [calculate_density(depth) for depth in depth_earth]  #地表到地心

premmodel = depth_earth[::-1] #6371----0
premmodel_density = prem_density[::-1] #地心-地表 

N = premmodel.shape[0]
g = [0]
m = 0
for ii in range(0,N-1):
    dm = (4 / 3) * np.pi * premmodel_density[ii+1]*1000.0* (depth_earth[ii+1]**3 - depth_earth[ii]**3) * 1.0e9
    m += dm
    g.append(G * m / (depth_earth[ii+1] * 1000)**2)
    
#g随地心的变化，从0-6371
plt.figure()
plt.plot(g[1:], premmodel[1:])
plt.gca().invert_yaxis()
plt.ylabel('Depth (km)')
plt.xlabel('g (m/s2)')
plt.title('g vs Depth')

P = [0]
Ptmp = 0
#dP=density.g.dz
for ii in range(0, N-1):
    dP = (premmodel_density[ii+1]*1000 * g[ii+1] * (depth_earth[ii+1]- depth_earth[ii]) * 1000)/ 1e9
    Ptmp += dP
    P.append(Ptmp)

plt.figure()
plt.plot(P[1:], depth_earth[1:])
plt.gca().invert_yaxis()

#Plot the roi 
depths_ROI = [410, 660, 2885, 5701]
pressure_ROI = [P[depth-1] for depth in depths_ROI]
plt.plot(pressure_ROI, depths_ROI, '*')
for depth, pressure in zip(depths_ROI, pressure_ROI):
    plt.text(pressure, depth, f'Depth: {depth} km, P: {pressure:.2f} GPa', va='bottom', ha='center')



plt.title('Pressures vs. Depth in the Earth')
plt.xlabel('Pressures (GPa)')
plt.ylabel('Depth (km)')
plt.grid(True)
plt.show()
