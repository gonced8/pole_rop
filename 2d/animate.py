import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import patches

interactive=True
gif=False

speed=10
step=100
DIM=2

f = open("temp.txt", 'r')

vertices=np.empty((0, DIM))
l=f.readline()
while l!='\n' and l!="":
    #l = list(map(float, l.split()))
    l = np.fromstring(l, dtype='float', sep='\t')
    vertices=np.append(vertices, [l], axis=0)
    l=f.readline()
#print(vertices)

data=np.empty((0, 1+2*DIM))
l=f.readline()
while l!="":
    #l = list(map(float, l.split()))
    l = np.fromstring(l, dtype='float', sep='\t')
    data = np.append(data, [l], axis=0)
    if step>1:
        for i in range(step-1):
            f.readline()
    l=f.readline()
#print(data.shape)

f.close()

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

size=int(sum(data[0][-DIM:]))
ax = plt.axes(xlim=(-size, size), ylim=(-size, size))

polygon = plt.Polygon(vertices, fc='b')
trail, = ax.plot([], [], lw=1, c='g')

if interactive:
    mass = plt.Circle((0, 0), 0.2, fc='r')
    rope = patches.FancyArrowPatch(posA=(0, 0), posB=(0, 0), ls='solid', lw='1')

    def init():
        mass.center = data[0][-DIM:]
        ax.add_patch(mass)
        rope.set_positions(data[0][-2*DIM:-DIM], data[0][-DIM:])
        ax.add_patch(rope)
        ax.add_patch(polygon)
        trail.set_data(data[0][-2], data[0][-1])
        return mass, rope, polygon, trail,

    def animate(i):
        mass.center = data[i][-DIM:]
        rope.set_positions(data[i][-2*DIM:-DIM], data[i][-DIM:])
        trail.set_data(data[:i+1,-2], data[:i+1,-1])
        return mass, rope, polygon, trail,

    frames=int(data.shape[0])
    interval=data[1][0]*1000/speed
    if int(interval)==0:
        print("Interval set to 1ms")
        interval=1

    anim = animation.FuncAnimation(fig, animate,
                                   init_func=init,
                                   frames=frames,
                                   interval=interval,
                                   blit=True)


else:
    trail.set_data(data[:,-2], data[:,-1])
    ax.add_patch(polygon)

if gif:
    anim.save('./gif.gif', writer='imagemagick', fps=30)

ax.set_aspect('equal')
plt.tight_layout()
plt.show()

