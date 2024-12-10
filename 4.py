import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from pygame import mixer

def draw_snowflake_branch(x, y, angle, length, depth, color, ax):
    if depth == 0:
        return

    x_end = x + length * np.cos(angle)
    y_end = y + length * np.sin(angle)

    ax.plot([x, x_end], [y, y_end], color=color, lw=2)

    draw_snowflake_branch(x_end, y_end, angle - np.pi / 3, length / 3, depth - 1, color, ax)
    draw_snowflake_branch(x_end, y_end, angle, length / 3, depth - 1, color, ax)
    draw_snowflake_branch(x_end, y_end, angle + np.pi / 3, length / 3, depth - 1, color, ax)

def draw_snowflake(num_branches, length, depth, color, ax):
    x, y = 0, 0

    for i in range(num_branches):
        angle = 2 * np.pi * i / num_branches
        draw_snowflake_branch(x, y, angle, length, depth, color, ax)

def random_params():
    num_branches = random.randint(6, 12)
    length = random.uniform(1, 5)
    depth = random.randint(2, 5)
    color = random.choice(['blue', 'red', 'green', 'purple', 'cyan'])
    angle = random.uniform(0, 2 * np.pi)
    return num_branches, length, depth, color, angle

def update(frame, ax, num_branches, length, max_depth, color, angle):
    ax.clear()


    depth = min(frame, max_depth)

    draw_snowflake(num_branches, length, depth, color, ax)

    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.axis('off')

def main():
    num_branches, length, max_depth, color, angle = random_params()


    fig, ax = plt.subplots(figsize=(6, 6))

    anime = FuncAnimation(fig, update, frames=np.arange(1, max_depth + 1), fargs=(ax, num_branches, length, max_depth, color, angle),
                        interval=500, repeat=False)

    # ZVUK INIT
    mixer.init()
    mixer.music.load('materials/sound_for_4.mp3')
    mixer.music.play()

    plt.show()

if __name__ == "__main__":
    main()
