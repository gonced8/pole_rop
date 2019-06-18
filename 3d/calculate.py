import numpy as np

f = open("temp.txt", 'w')

dt = 0.001

n = 3
r = .1
a = 2*r*np.sin(np.pi/n)
g = 9.81

t0 = 0.
l0 = 10.
v0 = 10.
theta0 = np.pi/2.5
theta_d0= 0.
phi0 = 0.
phi_d0 = v0/(l0*np.sin(theta0))

angles = [i*2.0*np.pi/n for i in range(n)]
vertices = [[r*np.sin(angle), r*np.cos(angle)] for angle in angles]

for vertex in vertices:
    for coordinate in vertex:
        f.write("%s\t" % coordinate)
    f.write('\n')
f.write('\n')

t = t0
l = l0
theta = theta0
theta_d = theta_d0
theta_dd = 0
phi = phi0
phi_d = phi_d0
phi_dd = 0
h=0

max_phi = angles[1]
d_angle = (n-2)*np.pi/n*0.5

i = 0
while l>0 and np.sin(theta)>0:

    if i>=n:
        i %= n

    angle = angles[i] + d_angle
    vertex = vertices[i]


    while phi<max_phi and np.sin(theta)>0:

        phi += phi_d * dt
        theta += theta_d*dt + 0.5*theta_dd*dt*dt

        phi_d = (np.sin(theta0)/np.sin(theta))**2 * phi_d0
        theta_d += theta_dd * dt

        theta_dd = (phi_d**2 * np.cos(theta) - g/l) * np.sin(theta)

        x = l*np.sin(theta)*np.sin(angle+phi)
        y = l*np.sin(theta)*np.cos(angle+phi)
        z = -l*np.cos(theta)
        #print(l, angle, phi, theta, x, y, z)
        #print(theta_dd, theta_d, theta*180/np.pi)

        pos  = [vertex[0]+x, vertex[1]+y, h+z]
        #print(pos)

        f.write("%s\t" % t)

        #print(((theta_d*l)**2+(phi_d*l*np.sin(theta))**2)*0.5 + g*(h+z), np.sqrt((theta_d*l)**2+(phi_d*l)**2)) #energy and velocity

        for coordinate in vertex:
            f.write("%s\t" % coordinate)

        f.write("%s\t" % h)

        for coordinate in pos:
            f.write("%s\t" % coordinate)

        f.write('\n')

        t += dt

    t -= (phi-max_phi)/phi_d

    phi = 0
    l2 = l - a/np.sin(theta)
    theta_d = theta_d * l/l2
    phi_d = phi_d * l/l2
    phi_d0 = phi_d
    theta0 = theta
    l = l2
    h -= a/np.tan(theta)

    i += 1

f.close()
