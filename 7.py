import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from pygame import mixer
from threading import Thread

BOX_SIZE = 10
NUM_BALLS = np.random.randint(2, 5)
BALL_SIZE = 0.5
BALL_COLORS = np.random.rand(NUM_BALLS, 3)


#ZVUK INIT
mixer.init()
mixer.music.load('materials/sound_for_7.mp3')
def music():mixer.music.play()


positions = np.random.uniform(
    BALL_SIZE, BOX_SIZE - BALL_SIZE, (NUM_BALLS, 2)
)
velocities = np.random.uniform(-0.2, 0.2, (NUM_BALLS, 2))

fig, ax = plt.subplots()
ax.set_xlim(0, BOX_SIZE)
ax.set_ylim(0, BOX_SIZE)
ax.set_aspect('equal')
ax.set_title("ОХ-Х, Ё-МОЁ")

ax.set_xticks([])
ax.set_yticks([])


circles = [plt.Circle(positions[i], BALL_SIZE, color=BALL_COLORS[i]) for i in range(NUM_BALLS)]
for circle in circles:
    ax.add_patch(circle)


def resolve_collision(i, j):
    delta_pos = positions[i] - positions[j]
    dist = np.linalg.norm(delta_pos)
    overlap = 2 * BALL_SIZE - dist

    if overlap > 0:
        #ZVUK
        Thread(target = music, daemon=True).start()

        collision_dir = delta_pos / dist if dist != 0 else np.array([1, 0])

        positions[i] += collision_dir * overlap / 2
        positions[j] -= collision_dir * overlap / 2

        v1_proj = np.dot(velocities[i], collision_dir)
        v2_proj = np.dot(velocities[j], collision_dir)

        velocities[i] -= v1_proj * collision_dir
        velocities[j] -= v2_proj * collision_dir
        velocities[i] += v2_proj * collision_dir
        velocities[j] += v1_proj * collision_dir


def update(frame):
    global positions, velocities, BALL_SIZE, circles

    # Обновление позиций
    positions += velocities

    for i in range(len(positions)):
        if positions[i, 0] - BALL_SIZE < 0:
            # ZVUK
            Thread(target = music, daemon=True).start()

            velocities[i, 0] *= -1
            positions[i, 0] = BALL_SIZE
        elif positions[i, 0] + BALL_SIZE > BOX_SIZE:
            # ZVUK
            Thread(target = music, daemon=True).start()

            velocities[i, 0] *= -1
            positions[i, 0] = BOX_SIZE - BALL_SIZE

        if positions[i, 1] - BALL_SIZE < 0:
            # ZVUK
            Thread(target = music, daemon=True).start()

            velocities[i, 1] *= -1
            positions[i, 1] = BALL_SIZE
        elif positions[i, 1] + BALL_SIZE > BOX_SIZE:
            # ZVUK
            Thread(target = music, daemon=True).start()

            velocities[i, 1] *= -1
            positions[i, 1] = BOX_SIZE - BALL_SIZE

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < 2 * BALL_SIZE:
                resolve_collision(i, j)

    for i, circle in enumerate(circles):
        circle.set_center(positions[i])
        circle.set_radius(BALL_SIZE)
    return circles

#SLIDER AND BUTTONS
def update_size(val):
    global BALL_SIZE
    BALL_SIZE = size_slider.val

ax_size_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
size_slider = Slider(ax_size_slider, 'Size', 0.1, 1.0, valinit=BALL_SIZE)
size_slider.on_changed(update_size)

ax_add_button = plt.axes([0.85, 0.3, 0.1, 0.075])
ax_remove_button = plt.axes([0.85, 0.2, 0.1, 0.075])
add_button = Button(ax_add_button, 'Add')
remove_button = Button(ax_remove_button, 'Remove')

def add_ball(event):
    global positions, velocities, BALL_COLORS, circles

    new_position = np.random.uniform(BALL_SIZE, BOX_SIZE - BALL_SIZE, (1, 2))
    new_velocity = np.random.uniform(-0.2, 0.2, (1, 2))
    new_color = np.random.rand(1, 3)

    positions = np.vstack((positions, new_position))
    velocities = np.vstack((velocities, new_velocity))
    BALL_COLORS = np.vstack((BALL_COLORS, new_color))

    new_circle = plt.Circle(new_position[0], BALL_SIZE, color=new_color[0])
    circles.append(new_circle)
    ax.add_patch(new_circle)

def remove_ball(event):
    global positions, velocities, BALL_COLORS, circles

    if len(positions) > 0:
        positions = positions[:-1]
        velocities = velocities[:-1]
        BALL_COLORS = BALL_COLORS[:-1]
        circle = circles.pop()
        circle.remove()

add_button.on_clicked(add_ball)
remove_button.on_clicked(remove_ball)


ani = FuncAnimation(
    fig,
    update,
    frames=200,
    interval=50,
    blit=False
)

plt.show()
