import matplotlib.animation as animation

import plantsKin as pk
from math import pi
import numpy as np
import matplotlib.pyplot as plt
import imp
import time
import baseToolbox as bt



print(1)
roots = pk.Roots(20,.5,theta0 =0)

roots.addCollectiveInteraction(name ='Apical')

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

#roots.addCollectiveInteraction(name ='Apical')
#roots.addInteractions(name = 'ApicalTropism' ,intensity=-10,direction = -pi/3)
fig = plt.figure(figsize=(10.80, 10.80), dpi=100)
fig.tight_layout()

#ig.patch.set_visible(False)

ax = fig.add_subplot(111)
ax.axis('off')
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
lines = []
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False) 
for root in roots.roots:
    lines.append(ax.plot(root.x[:,0],root.x[:,2], antialiased=True))
ax.set_xlim(0,10.1)
ax.set_ylim(-0.1,1.1)
    
def init():
    for line in lines:
        line.set_data([],[])
    return lines
def animate():
    
    for k in range(0,len(lines)):
        lines[k].set_data(root.x[k][:,0],root.x[k][:,2])

    t0=time.time()
    roots.update()
    t1=time.time()
    ax.set_xlim(0,10.1)
    ax.set_ylim(-0.1,1.1)
    #print(-1/(t0-t1))
    t0=t1
    return lines

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=20, interval=20, blit=True)
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])