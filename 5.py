import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon

# Генерация случайных параметров синусоиды
amplitude = np.random.uniform(0.1, 1.0)
frequency = np.random.uniform(0.1, 1.5)
phase = np.random.uniform(0, 2 * np.pi)  # Случайная фаза

# Параметры синусоиды
x = np.linspace(0, 10, 1000)
y = amplitude * np.sin(frequency * x + phase)

# Создание фигуры и осей
fig, ax = plt.subplots()
line, = ax.plot(x, y, lw=2, color='cyan', alpha=0.4)  # График синусоиды
tangent_patch = Polygon([[0, 0], [0, 0], [0, 0], [0, 0]], closed=True, color='brown', alpha=1)
perpendicular_line, = ax.plot([], [], color='black', lw=2)  # Линия перпендикуляра
triangle_patch = Polygon([[0, 0], [0, 0], [0, 0]], closed=True, color='red', alpha=0.5)  # Треугольник

ax.add_patch(tangent_patch)
ax.add_patch(triangle_patch)

# Площадь под графиком (как PolyCollection)
water_poly = PolyCollection([], color='lightblue', alpha=0.9)
ax.add_collection(water_poly)

# Настройка пределов графика
ax.set_xlim(0, 10)
ax.set_ylim(-3, 3)

ax.set_xticks([])
ax.set_yticks([])

ax.set_title("Кораблик плавает круто по волнам")

# Функция для обновления анимации
def update(frame):
    # Смещение графика
    shift = frame * 0.1
    y_shifted = amplitude * np.sin(frequency * (x + shift) + phase)
    line.set_data(x, y_shifted)

    # Обновление площади под графиком
    water_coords = np.column_stack((x, y_shifted))
    water_coords = np.vstack(([x[0], -3], water_coords, [x[-1], -3]))  # Добавляем нижние углы
    water_poly.set_verts([water_coords])

    # Точка касания
    tangent_x = 5  # x-координата точки касательной
    tangent_y = amplitude * np.sin(frequency * (tangent_x + shift) + phase) - 0.2  # y-координата точки касательной

    # Направление касательной
    dx = 1
    dy = amplitude * frequency * np.cos(frequency * (tangent_x + shift) + phase) # Производная как направление
    norm = np.sqrt(dx ** 2 + dy ** 2)  # Нормализация
    dx /= norm
    dy /= norm

    # Параметры трапеции
    base_length = 0.7  # Длина верхней стороны трапеции
    offset_length = 1.5  # Длина нижней стороны трапеции (расширение)

    # Вычисление координат вершин трапеции
    top_left = [tangent_x - dx * base_length / 2, tangent_y - dy * base_length / 2]
    top_right = [tangent_x + dx * base_length / 2, tangent_y + dy * base_length / 2]

    # Нижняя сторона трапеции: фиксируем длину и смещаем её по диагонали
    bottom_left = [tangent_x - dx * offset_length / 2 - dy * 0.5, tangent_y - dy * offset_length / 2 + dx * 0.5]
    bottom_right = [tangent_x + dx * offset_length / 2 - dy * 0.5, tangent_y + dy * offset_length / 2 + dx * 0.5]

    # Обновление трапеции
    trapezoid_coords = [bottom_left, bottom_right, top_right, top_left]
    tangent_patch.set_xy(trapezoid_coords)

    # Вычисление координат перпендикуляра
    mid_x = (bottom_left[0] + bottom_right[0]) / 2
    mid_y = (bottom_left[1] + bottom_right[1]) / 2

    # Направление перпендикуляра
    dx_line = bottom_right[0] - bottom_left[0]
    dy_line = bottom_right[1] - bottom_left[1]

    # Перпендикуляр должен быть ортогонален этой линии
    perp_dx = -dy_line
    perp_dy = dx_line

    # Нормализация перпендикуляра
    norm = np.sqrt(perp_dx ** 2 + perp_dy ** 2)
    perp_dx /= norm
    perp_dy /= norm

    perp_length = 1.0  # Длина перпендикуляра
    perp_end_x = mid_x + perp_dx * perp_length
    perp_end_y = mid_y + perp_dy * perp_length

    # Обновление перпендикуляра
    perpendicular_line.set_data([mid_x, perp_end_x], [mid_y, perp_end_y])

    # Вершины треугольника, который прикреплен к перпендикуляру
    triangle_base_length = 0.5  # Длина основания треугольника
    triangle_height = 1.0  # Высота треугольника

    # Вершины треугольника: две точки основания по бокам перпендикуляра и вершина вверх
    triangle_left_x = mid_x - perp_dy * triangle_base_length / 2
    triangle_left_y = mid_y + perp_dx * triangle_base_length / 2

    triangle_right_x = mid_x + perp_dy * triangle_base_length / 2
    triangle_right_y = mid_y - perp_dx * triangle_base_length / 2

    # Вершина треугольника: смещаем вверх вдоль перпендикуляра
    triangle_top_x = mid_x + perp_dx * triangle_height
    triangle_top_y = mid_y + perp_dy * triangle_height

    # Обновление треугольника
    triangle_coords = [[triangle_left_x, triangle_left_y],
                       [triangle_right_x, triangle_right_y],
                       [triangle_top_x, triangle_top_y]]
    triangle_patch.set_xy(triangle_coords)

    return line, tangent_patch, water_poly, perpendicular_line, triangle_patch

# Анимация
ani = FuncAnimation(
    fig,
    update,
    interval=50,  # Интервал между кадрами в миллисекундах
    blit=False,
    repeat=True,  # Анимация будет зациклена
    frames=None,  # Бесконечное количество кадров
)

plt.show()
