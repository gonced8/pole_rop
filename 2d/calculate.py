import numpy as np

f = open("temp.txt", 'w')

dt = 0.001

n = 1000
r = 1.
a = 2*r*np.sin(np.pi/n)

t0 = 0.
l0 = 10.
theta0 = 0.
v = 1.

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
max_theta = angles[1]
d_angle = (n-2)*np.pi/n*0.5

i = 0
while l>0:

    if i>=n:
        i %= n

    angle = angles[i] + d_angle
    vertex = vertices[i]

    omega=v/l

    while theta<max_theta:

        theta += omega * dt

        x = l*np.sin(angle+theta)
        y = l*np.cos(angle+theta)
        #print(l, angle, theta, x, y)

        pos  = [vertex[0]+x, vertex[1]+y]
        #print(pos_x, pos_y)

        f.write("%s\t" % t)

        for coordinate in vertex:
            f.write("%s\t" % coordinate)

        for coordinate in pos:
            f.write("%s\t" % coordinate)

        f.write('\n')

        t += dt

    t -= (theta-max_theta)/omega
    theta = 0
    l -= a
    i += 1

f.close()
