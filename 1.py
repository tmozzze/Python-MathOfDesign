import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def generate_spiral(angle, num_points=200):
    t = np.linspace(0, 8 * np.pi, num_points)
    r = 0.1 * t
    x = r * np.cos(t + angle)
    y = r * np.sin(t + angle)
    return x, y


def update(frame, ax, angle, num_points):
    ax.clear()

    x, y = generate_spiral(angle, num_points)

    ax.plot(x[:frame], y[:frame], color='blue', lw=2)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')


def create_animation(angle, num_points=100):
    fig, ax = plt.subplots(figsize=(6, 6))

    ani = FuncAnimation(fig, update, frames=np.arange(1, num_points + 1), fargs=(ax, angle, num_points),
                        interval=50, repeat=False)

    plt.show()


def main():
    print("Выберите угол наклона для спирали:")
    print("1. Угол 0 (стандартная спираль)")
    print("2. Угол 45 градусов")
    print("3. Угол 90 градусов")

    choice = input("Введите номер угла (1/2/3): ")

    if choice == "1":
        angle = 0
    elif choice == "2":
        angle = np.pi / 4
    elif choice == "3":
        angle = np.pi / 2
    else:
        print("Неверный выбор, используем угол 0 по умолчанию.")
        angle = 0

    create_animation(angle)


if __name__ == "__main__":
    main()
