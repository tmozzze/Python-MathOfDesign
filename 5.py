import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon

amplitude = np.random.uniform(0.1, 1.0)
frequency = np.random.uniform(0.1, 1.5)
phase = np.random.uniform(0, 2 * np.pi)

x = np.linspace(0, 10, 1000)
y = amplitude * np.sin(frequency * x + phase)

fig, ax = plt.subplots()
line, = ax.plot(x, y, lw=2, color='cyan', alpha=0.4)
tangent_patch = Polygon([[0, 0], [0, 0], [0, 0], [0, 0]], closed=True, color='brown', alpha=0.7)
perpendicular_line, = ax.plot([], [], color='black', lw=2)
triangle_patch = Polygon([[0, 0], [0, 0], [0, 0]], closed=True, color='red', alpha=0.5)

ax.add_patch(tangent_patch)
ax.add_patch(triangle_patch)

water_poly = PolyCollection([], color='lightblue', alpha=0.9)
ax.add_collection(water_poly)

ax.set_xlim(0, 10)
ax.set_ylim(-3, 3)

ax.set_xticks([])
ax.set_yticks([])


ax.set_title("Кораблик плавает круто по волнам ЭЩКЕРЕ")

def update(frame):
    shift = frame * 0.1
    y_shifted = amplitude * np.sin(frequency * (x + shift) + phase)
    line.set_data(x, y_shifted)
    ax.set_aspect('equal')

    #Ploshad pod graficom(water)
    water_coords = np.column_stack((x, y_shifted))
    water_coords = np.vstack(([x[0], -3], water_coords, [x[-1], -3]))
    water_poly.set_verts([water_coords])

    #Tocka kasaniya
    tangent_x = 5
    tangent_y = amplitude * np.sin(frequency * (tangent_x + shift) + phase) - 0.2

    #Napravlenie kasat
    dx = 1
    dy = amplitude * frequency * np.cos(frequency * (tangent_x + shift) + phase) # Производная как направление
    norm = np.sqrt(dx ** 2 + dy ** 2)
    dx /= norm
    dy /= norm

    # Param Korablik
    base_length = 0.7
    offset_length = 2

    top_left = [tangent_x - dx * base_length / 2, tangent_y - dy * base_length / 2]
    top_right = [tangent_x + dx * base_length / 2, tangent_y + dy * base_length / 2]

    bottom_left = [tangent_x - dx * offset_length / 2 - dy * 0.5, tangent_y - dy * offset_length / 2 + dx * 0.5]
    bottom_right = [tangent_x + dx * offset_length / 2 - dy * 0.5, tangent_y + dy * offset_length / 2 + dx * 0.5]

    trapezoid_coords = [bottom_left, bottom_right, top_right, top_left]
    tangent_patch.set_xy(trapezoid_coords)

    # Param perpendicular
    mid_x = (bottom_left[0] + bottom_right[0]) / 2
    mid_y = (bottom_left[1] + bottom_right[1]) / 2

    dx_line = bottom_right[0] - bottom_left[0]
    dy_line = bottom_right[1] - bottom_left[1]

    perp_dx = -dy_line
    perp_dy = dx_line

    norm = np.sqrt(perp_dx ** 2 + perp_dy ** 2)
    perp_dx /= norm
    perp_dy /= norm

    perp_length = 1.1
    perp_end_x = mid_x + perp_dx * perp_length
    perp_end_y = mid_y + perp_dy * perp_length

    perpendicular_line.set_data([mid_x, perp_end_x], [mid_y, perp_end_y])

    # Treugolnik
    triangle_base_length = 0.5
    triangle_height = 1.0

    triangle_left_x = mid_x - perp_dy * triangle_base_length / 2
    triangle_left_y = mid_y + perp_dx * triangle_base_length / 2

    triangle_right_x = mid_x + perp_dy * triangle_base_length / 2
    triangle_right_y = mid_y - perp_dx * triangle_base_length / 2

    triangle_top_x = mid_x + perp_dx * triangle_height
    triangle_top_y = mid_y + perp_dy * triangle_height

    triangle_coords = [[triangle_left_x, triangle_left_y],
                       [triangle_right_x, triangle_right_y],
                       [triangle_top_x, triangle_top_y]]
    triangle_patch.set_xy(triangle_coords)

    return line, tangent_patch, water_poly, perpendicular_line, triangle_patch

# Anime
ani = FuncAnimation(
    fig,
    update,
    interval=50,
    blit=False,
    repeat=True,
    frames=None
)

plt.show()
