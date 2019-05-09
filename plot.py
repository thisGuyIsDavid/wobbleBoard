# libraries
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation
import math
import random

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')xq
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

x = []
y = []
z = []

def init():
    ax.view_init(30, 185)

def update():
    pass

def animate(i):
    x.append(math.sin(i))
    z.append(math.cos(i))
    y.append(random.randint(0, i+1))
    ax.clear()
    ax.grid(False)

    ax.xaxis.pane.set_edgecolor('grey')
    ax.yaxis.pane.set_edgecolor('grey')
    ax.zaxis.pane.set_edgecolor('grey')

    print(x)
    ax.axis(alpha=1.0)
    ax.spines['right'].set_color('red')
    ax.spines['left'].set_color('red')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.plot(x, y, z, label='parametric curve')


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=10, blit=False)

anim.save('index.html')




#


