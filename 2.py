import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
import random


num_rays = random.randint(5, 12)
outer_radius = random.uniform(1, 3)
inner_radius = outer_radius / random.uniform(2, 3)
colors = [np.random.rand(3, ) for _ in range(num_rays)]

fig, ax = plt.subplots()
ax.set_xlim(-outer_radius * 1.5, outer_radius * 1.5)
ax.set_ylim(-outer_radius * 1.5, outer_radius * 1.5)
ax.set_aspect('equal')
ax.axis('off')

patches = []


def calculate_star_vertices(num_rays, outer_radius, inner_radius):
    angles = np.linspace(0, 2 * np.pi, num_rays * 2, endpoint=False)
    radii = np.empty(len(angles))
    radii[::2] = outer_radius
    radii[1::2] = inner_radius
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    vertices = np.column_stack((x, y))
    return vertices


def update(frame):
    for patch in patches:
        patch.remove()
    patches.clear()

    vertices = calculate_star_vertices(num_rays, outer_radius, inner_radius)
    for i in range(frame + 1):
        polygon = Polygon([vertices[i % len(vertices)],
                           vertices[(i + 1) % len(vertices)],
                           (0, 0)],
                          closed=True,
                          color=colors[i % num_rays],
                          alpha=0.8)
        ax.add_patch(polygon)
        patches.append(polygon)


ani = FuncAnimation(fig, update, frames=num_rays * 2, interval=200, repeat=False)

plt.show()