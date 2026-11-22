
import pygame
import random
import math

# ==========================
# 1. 初始化
# ==========================

pygame.init()

WIDTH = 1000
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Particle Christmas Tree")

clock = pygame.time.Clock()

CENTER_X = WIDTH // 2
CENTER_Y = 370

BLACK = (3, 5, 18)
GOLD = (255, 210, 70)
WHITE = (255, 255, 255)

# ==========================
# 2. 生成3D圣诞树粒子
# ==========================

particles = []

for i in range(2200):

    y = random.uniform(-230, 220)

    # 树体由上到下逐渐变宽
    progress = (y + 230) / 450

    max_radius = progress * 180

    radius = max_radius * math.sqrt(random.random())

    angle = random.uniform(0, math.pi * 2)

    x = radius * math.cos(angle)
    z = radius * math.sin(angle)

    particles.append({
        "x": x,
        "y": y,
        "z": z,
        "size": random.uniform(1, 3),
        "phase": random.uniform(0, math.pi * 2)
    })


# ==========================
# 3. 生成彩灯
# ==========================

lights = []

for i in range(90):

    y = random.uniform(-210, 210)

    progress = (y + 230) / 450

    radius = progress * 175

    angle = random.uniform(0, math.pi * 2)

    x = radius * math.cos(angle)
    z = radius * math.sin(angle)

    lights.append({
        "x": x,
        "y": y,
        "z": z,
        "color": random.choice([
            (255, 40, 60),
            (255, 210, 40),
            (50, 150, 255),
            (255, 255, 255)
        ]),
        "phase": random.uniform(0, 6.28)
    })


# ==========================
# 4. 生成雪花
# ==========================

snowflakes = []

for i in range(160):

    snowflakes.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.uniform(0.5, 2.5),
        "size": random.randint(1, 3)
    })


# ==========================
# 5. 3D坐标投影
# ==========================

def project(x, y, z, angle):

    # 绕Y轴旋转
    rotated_x = x * math.cos(angle) - z * math.sin(angle)
    rotated_z = x * math.sin(angle) + z * math.cos(angle)

    # 透视投影
    distance = 650

    scale = distance / (distance + rotated_z)

    screen_x = CENTER_X + rotated_x * scale
    screen_y = CENTER_Y + y * scale

    return int(screen_x), int(screen_y), scale, rotated_z


# ==========================
# 6. 绘制五角星
# ==========================

def draw_star(surface, x, y, size, color):

    points = []

    for i in range(10):

        angle = -math.pi / 2 + i * math.pi / 5

        if i % 2 == 0:
            radius = size
        else:
            radius = size * 0.42

        px = x + math.cos(angle) * radius
        py = y + math.sin(angle) * radius

        points.append((px, py))

    pygame.draw.polygon(surface, color, points)


# ==========================
# 7. 主循环
# ==========================

running = True

time = 0

while running:

    time += 0.018

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # ======================
    # 绘制背景星星
    # ======================

    for i in range(45):

        x = (i * 137) % WIDTH
        y = (i * 83) % HEIGHT

        brightness = int(
            100 + 100 * abs(math.sin(time + i))
        )

        pygame.draw.circle(
            screen,
            (brightness, brightness, brightness),
            (x, y),
            1
        )

    # ======================
    # 绘制3D树体粒子
    # ======================

    angle = time

    visible_particles = []

    for p in particles:

        x, y, scale, depth = project(
            p["x"],
            p["y"],
            p["z"],
            angle
        )

        visible_particles.append(
            (depth, x, y, scale, p)
        )

    # 远处的粒子先绘制
    visible_particles.sort(reverse=True, key=lambda item: item[0])

    for depth, x, y, scale, p in visible_particles:

        brightness = 0.65 + 0.35 * math.sin(
            time * 3 + p["phase"]
        )

        green = int(160 * brightness)

        color = (
            10,
            green,
            int(65 * brightness)
        )

        size = max(1, int(p["size"] * scale))

        pygame.draw.circle(
            screen,
            color,
            (x, y),
            size
        )

    # ======================
    # 绘制动态彩灯
    # ======================

    for light in lights:

        x, y, scale, depth = project(
            light["x"],
            light["y"],
            light["z"],
            angle
        )

        glow = abs(
            math.sin(time * 3 + light["phase"])
        )

        radius = max(2, int((2 + glow * 4) * scale))

        color = light["color"]

        # 光晕
        pygame.draw.circle(
            screen,
            tuple(int(c * 0.3) for c in color),
            (x, y),
            radius * 3
        )

        pygame.draw.circle(
            screen,
            color,
            (x, y),
            radius
        )

    # ======================
    # 树顶发光星星
    # ======================

    star_size = 23 + int(
        5 * math.sin(time * 4)
    )

    # 星星光晕
    pygame.draw.circle(
        screen,
        (100, 75, 15),
        (CENTER_X, 115),
        star_size * 2
    )

    draw_star(
        screen,
        CENTER_X,
        115,
        star_size,
        GOLD
    )

    draw_star(
        screen,
        CENTER_X,
        115,
        star_size // 2,
        WHITE
    )

    # ======================
    # 树干
    # ======================

    pygame.draw.rect(
        screen,
        (110, 55, 25),
        (CENTER_X - 20, 580, 40, 75)
    )

    # ======================
    # 雪花飘落
    # ======================

    for snow in snowflakes:

        pygame.draw.circle(
            screen,
            WHITE,
            (int(snow["x"]), int(snow["y"])),
            snow["size"]
        )

        snow["y"] += snow["speed"]

        snow["x"] += math.sin(
            time + snow["y"] * 0.02
        ) * 0.7

        if snow["y"] > HEIGHT:

            snow["y"] = 0
            snow["x"] = random.randint(0, WIDTH)

    # ======================
    # 标题
    # ======================

    font = pygame.font.SysFont(
        "Arial",
        38,
        bold=True
    )

    title = font.render(
        "MERRY CHRISTMAS",
        True,
        GOLD
    )

    screen.blit(
        title,
        (
            CENTER_X - title.get_width() // 2,
            30
        )
    )

    # 底部文字
    small_font = pygame.font.SysFont("Arial", 18)

    text = small_font.render(
        "A Magical 3D Particle Christmas Tree",
        True,
        (180, 180, 200)
    )

    screen.blit(
        text,
        (
            CENTER_X - text.get_width() // 2,
            690
        )
    )

    pygame.display.flip()

    clock.tick(60)


pygame.quit()

