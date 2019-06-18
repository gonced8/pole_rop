import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib import animation
from matplotlib import patches

interactive=True
gif=False

speed=1
step=100
DIM=3

f = open("temp.txt", 'r')

vertices=np.empty((0, 2))
l=f.readline()
while l!='\n' and l!="":
    #l = list(map(float, l.split()))
    l = np.fromstring(l, dtype='float', sep='\t')
    vertices=np.append(vertices, [l], axis=0)
    l=f.readline()
#print(vertices)

data=np.empty((0, 1+DIM+DIM))
l=f.readline()
while l!="":
    #l = list(map(float, l.split()))
    l = np.fromstring(l, dtype='float', sep='\t')
    data = np.append(data, [l], axis=0)
    if step>1:
        for i in range(step-1):
            f.readline()
    l=f.readline()
#print(data)

f.close()

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

size=int(np.sqrt(np.sum(np.square(np.add(data[0][-2*DIM:-DIM],data[0][-DIM:])))))
ax = p3.Axes3D(fig)
ax.set_xlim3d([-size, size])
ax.set_xlabel('X')
ax.set_ylim3d([-size, size])
ax.set_ylabel('Y')
ax.set_zlim3d([-size, size])
ax.set_zlabel('Z')
ax.set_title('Rope around Pole 3D')

#trail

def draw_polygon(vertices, h):
    v = np.array([np.append(vertex, [z]) for vertex in vertices for z in [size, -size]])
    faces = np.empty((0, 4, DIM))
    for i in range (len(vertices)-1):
        faces = np.append(faces, [[v[2*i], v[2*i+1], v[2*i+3], v[2*i+2]]], axis=0)
    faces = np.append(faces, [[v[-2], v[-1], v[1], v[0]]] , axis=0)

    ax.add_collection3d(Poly3DCollection(faces, facecolors='gray', linewidths=1, edgecolors='green'))

    return

draw_polygon(vertices, size)
role, = ax.plot([0, 0], [0, 0], [0, 0], color='black')
trail, = ax.plot([0, 0], [0, 0], [0, 0], color='black', lw='0.7')

if interactive:

    mass, = ax.plot([0], [0], [0], linestyle="", marker="o")
    rope, = ax.plot([0, 0], [0, 0], [0, 0], color='black')

    def init():
        #mass.center = data[0][-DIM:]
        #ax.add_patch(mass)
        #rope.set_positions(data[0][-2*DIM:-DIM], data[0][-DIM:])
        #ax.add_patch(rope)
        #ax.add_patch(polygon)
        #trail.set_data(data[0][-2], data[0][-1])
        return mass,# rope, polygon, trail,

    def animate(i):

        mass.set_data([data[i][-DIM]], [data[i][-DIM+1]])
        mass.set_3d_properties([data[i][-DIM+2]])
        
        rope.set_data([data[i][-2*DIM], data[i][-DIM]], [data[i][-2*DIM+1], data[i][-DIM+1]])
        rope.set_3d_properties([data[i][-2*DIM+2], data[i][-DIM+2]])

        role.set_data(data[:i+1,-2*DIM], data[:i+1,-2*DIM+1])
        role.set_3d_properties(data[:i+1,-2*DIM+2])

        trail.set_data(data[:i+1,-DIM], data[:i+1,-DIM+1])
        trail.set_3d_properties(data[:i+1,-DIM+2])

        return

    frames=int(data.shape[0])
    interval=data[1][0]*1000/speed

    if int(interval)==0:
        print("Interval set to 1ms")
        interval=1

    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=interval, blit=False)
    #anim = animation.FuncAnimation(fig, animate,init_func=init, frames=frames, interval=interval, blit=False)

else:
    role.set_data(data[:i+1,-2*DIM], data[:i+1,-2*DIM+1])
    role.set_3d_properties(data[:i+1,-2*DIM+2])

    trail.set_data(data[:,-DIM], data[:,-DIM+1])
    trail.set_3d_properties(data[:,-DIM+2])

if gif:
    anim.save('./gif.gif', writer='imagemagick', fps=30)

ax.set_aspect('equal')
#plt.tight_layout()
plt.show()

