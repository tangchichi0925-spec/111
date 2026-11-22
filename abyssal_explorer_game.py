import math
import random
import sys

import pygame


WIDTH, HEIGHT = 900, 600
FPS = 60

OCEAN_TOP = (18, 116, 166)
OCEAN_BOTTOM = (5, 25, 70)
WHITE = (235, 250, 255)
GOLD = (255, 218, 80)
SEAWEED_COLORS = [(32, 155, 112), (42, 185, 122), (24, 125, 105)]


def make_bubbles():
    bubbles = []
    for _ in range(35):
        bubbles.append({
            "x": random.randint(20, WIDTH - 20),
            "y": random.randint(0, HEIGHT),
            "speed": random.uniform(20, 65),
            "size": random.randint(2, 6),
        })
    return bubbles


def make_treasures():
    treasures = []
    for _ in range(8):
        treasures.append({
            "x": random.randint(60, WIDTH - 60),
            "y": random.randint(130, HEIGHT - 70),
            "taken": False,
        })
    return treasures


def make_seaweed():
    seaweed = []
    for _ in range(55):
        seaweed.append({
            "x": random.randint(0, WIDTH),
            "height": random.randint(25, 100),
            "width": random.randint(8, 18),
            "phase": random.uniform(0, 6.28),
            "color": random.choice(SEAWEED_COLORS),
        })
    return seaweed


def make_corals():
    corals = []
    for _ in range(18):
        corals.append({
            "x": random.randint(20, WIDTH - 20),
            "y": random.randint(HEIGHT - 70, HEIGHT - 30),
            "color": random.choice([(225, 95, 110), (220, 115, 185), (245, 150, 75)]),
            "size": random.randint(8, 18),
        })
    return corals


def make_fish():
    fish = []
    for _ in range(12):
        fish.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(110, HEIGHT - 130),
            "speed": random.randint(25, 65),
            "size": random.randint(5, 10),
        })
    return fish


def make_rocks():
    rocks = []
    for _ in range(30):
        rocks.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(HEIGHT - 62, HEIGHT - 28),
            "width": random.randint(10, 30),
            "height": random.randint(6, 18),
            "color": random.choice([(45, 65, 76), (55, 76, 82), (66, 82, 86)]),
        })
    return rocks


def draw_ocean(screen, elapsed):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = tuple(
            int(OCEAN_TOP[i] * (1 - ratio) + OCEAN_BOTTOM[i] * ratio)
            for i in range(3)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    pygame.draw.polygon(
        screen,
        (42, 92, 75),
        [(0, HEIGHT), (0, HEIGHT - 55), (120, HEIGHT - 80),
         (240, HEIGHT - 45), (390, HEIGHT - 90), (560, HEIGHT - 50),
         (720, HEIGHT - 85), (WIDTH, HEIGHT - 55), (WIDTH, HEIGHT)],
    )

    light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for index in range(5):
        x = (index * 220 + elapsed * (8 + index * 2)) % (WIDTH + 220) - 110
        width = 65 + index * 12
        pygame.draw.polygon(
            light,
            (180, 245, 255, 22),
            [(x, 0), (x + width, 0), (x + width + 130, HEIGHT - 130),
             (x + 20, HEIGHT - 130)],
        )
    screen.blit(light, (0, 0))


def draw_rocks(screen, rocks):
    for rock in rocks:
        x, y = rock["x"], rock["y"]
        pygame.draw.ellipse(
            screen,
            rock["color"],
            (x - rock["width"] // 2, y - rock["height"] // 2,
             rock["width"], rock["height"]),
        )


def draw_seaweed(screen, seaweed, elapsed):
    for plant in seaweed:
        base_x = plant["x"]
        base_y = HEIGHT - 52
        sway = math.sin(elapsed * 2 + plant["phase"]) * plant["width"]
        points = []
        for segment in range(5):
            progress = segment / 4
            x = base_x + sway * progress
            y = base_y - plant["height"] * progress
            points.append((int(x), int(y)))
        pygame.draw.lines(screen, plant["color"], False, points, 4)


def draw_corals(screen, corals):
    for coral in corals:
        x, y, size = coral["x"], coral["y"], coral["size"]
        color = coral["color"]
        pygame.draw.line(screen, color, (x, y), (x, y - size * 2), 5)
        pygame.draw.circle(screen, color, (x - size // 2, y - size * 2), size // 2)
        pygame.draw.circle(screen, color, (x + size // 2, y - size * 2 - 5), size // 2)


def draw_fish(screen, fish, dt):
    for little_fish in fish:
        little_fish["x"] += little_fish["speed"] * dt
        if little_fish["x"] > WIDTH + 30:
            little_fish["x"] = -30
            little_fish["y"] = random.randint(110, HEIGHT - 130)
        x, y, size = int(little_fish["x"]), int(little_fish["y"]), little_fish["size"]
        pygame.draw.polygon(screen, (150, 210, 220),
                            [(x + size, y), (x - size, y - size // 2),
                             (x - size, y + size // 2)])
        pygame.draw.circle(screen, (235, 250, 240), (x + size // 2, y - 1), 2)


def draw_particles(screen, particles, dt):
    remaining = []
    for particle in particles:
        particle["life"] -= dt
        particle["x"] += particle["vx"] * dt
        particle["y"] += particle["vy"] * dt
        particle["radius"] += 12 * dt
        if particle["life"] > 0:
            pygame.draw.circle(
                screen,
                GOLD,
                (int(particle["x"]), int(particle["y"])),
                max(1, int(particle["radius"])),
            )
            remaining.append(particle)
    return remaining


def draw_hud(screen, font, oxygen, treasures_found, message, message_timer):
    panel = pygame.Surface((390, 88), pygame.SRCALPHA)
    pygame.draw.rect(panel, (4, 24, 55, 185), (0, 0, 390, 88), border_radius=14)
    screen.blit(panel, (15, 15))

    label = font.render(f"宝藏: {treasures_found}", True, WHITE)
    screen.blit(label, (30, 27))

    pygame.draw.rect(screen, (30, 55, 75), (145, 29, 225, 18), border_radius=8)
    oxygen_width = int(225 * max(0, min(100, oxygen)) / 100)
    oxygen_color = (85, 220, 180) if oxygen > 30 else (245, 110, 85)
    pygame.draw.rect(screen, oxygen_color, (145, 29, oxygen_width, 18), border_radius=8)
    oxygen_text = font.render(f"氧气 {max(0, int(oxygen))}%", True, WHITE)
    screen.blit(oxygen_text, (145, 52))

    if message_timer > 0:
        notice = font.render(message, True, GOLD)
        screen.blit(notice, (WIDTH - notice.get_width() - 25, 28))


def draw_bubbles(screen, bubbles, dt):
    for bubble in bubbles:
        bubble["y"] -= bubble["speed"] * dt
        if bubble["y"] < -10:
            bubble["y"] = HEIGHT + 10
            bubble["x"] = random.randint(20, WIDTH - 20)
        pygame.draw.circle(screen, (185, 235, 245),
                           (int(bubble["x"]), int(bubble["y"])), bubble["size"], 1)


def draw_treasure(screen, treasure):
    if treasure["taken"]:
        return
    x, y = treasure["x"], treasure["y"]
    pygame.draw.rect(screen, (125, 70, 35), (x - 14, y - 8, 28, 18), border_radius=4)
    pygame.draw.line(screen, GOLD, (x - 14, y), (x + 14, y), 3)
    pygame.draw.circle(screen, GOLD, (x, y), 4)


def draw_diver(screen, player):
    x, y = int(player.x), int(player.y)
    pygame.draw.circle(screen, (245, 188, 125), (x, y - 16), 11)
    pygame.draw.ellipse(screen, (245, 115, 70), (x - 14, y - 6, 28, 38))
    pygame.draw.line(screen, (245, 245, 245), (x + 8, y - 2), (x + 23, y - 10), 4)
    pygame.draw.circle(screen, (30, 40, 55), (x + 4, y - 18), 3)
    pygame.draw.circle(screen, (190, 240, 245), (x - 15, y - 28), 4, 1)
    pygame.draw.circle(screen, (190, 240, 245), (x - 22, y - 39), 2, 1)


def draw_shipwreck(screen):
    hull = [(690, HEIGHT - 70), (825, HEIGHT - 70), (790, HEIGHT - 38),
            (720, HEIGHT - 38)]
    pygame.draw.polygon(screen, (82, 54, 48), hull)
    pygame.draw.line(screen, (125, 82, 54), (750, HEIGHT - 68), (750, HEIGHT - 185), 5)
    pygame.draw.polygon(screen, (105, 74, 55),
                        [(754, HEIGHT - 178), (810, HEIGHT - 135), (754, HEIGHT - 135)])
    pygame.draw.line(screen, (48, 42, 50), (690, HEIGHT - 45), (825, HEIGHT - 45), 3)


def draw_manta(screen, manta):
    x, y = int(manta.x), int(manta.y)
    pygame.draw.polygon(screen, (105, 75, 155),
                        [(x - 42, y), (x - 8, y - 10), (x, y - 22),
                         (x + 8, y - 10), (x + 42, y), (x + 8, y + 8),
                         (x, y + 18), (x - 8, y + 8)])


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("深海探险 - 动画版")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Microsoft YaHei", 22)
    big_font = pygame.font.SysFont("Microsoft YaHei", 42)

    player = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    manta = pygame.Vector2(170, 180)
    manta_speed = 90
    oxygen = 100.0
    treasures_found = 0
    bubbles = make_bubbles()
    treasures = make_treasures()
    seaweed = make_seaweed()
    corals = make_corals()
    fish = make_fish()
    rocks = make_rocks()
    particles = []
    message = ""
    message_timer = 0
    move_target = None
    finished = False
    running = True

    while running:
        dt = clock.tick(FPS) / 1000
        elapsed = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                move_target = pygame.Vector2(event.pos)

        if not finished:
            keys = pygame.key.get_pressed()
            direction = pygame.Vector2(
                (keys[pygame.K_d] or keys[pygame.K_RIGHT])
                - (keys[pygame.K_a] or keys[pygame.K_LEFT]),
                (keys[pygame.K_s] or keys[pygame.K_DOWN])
                - (keys[pygame.K_w] or keys[pygame.K_UP]),
            )
            if direction.length_squared() == 0 and move_target is not None:
                direction = move_target - player
                if direction.length_squared() < 400:
                    move_target = None
                    direction = pygame.Vector2()
            if direction.length_squared() > 0:
                direction = direction.normalize()
                player += direction * 220 * dt
                oxygen -= 4 * dt

            player.x = max(25, min(WIDTH - 25, player.x))
            player.y = max(90, min(HEIGHT - 55, player.y))

            manta.x += manta_speed * dt
            if manta.x > WIDTH + 60 or manta.x < -60:
                manta_speed *= -1
                manta.y = random.randint(120, 260)

            for treasure in treasures:
                treasure_pos = pygame.Vector2(treasure["x"], treasure["y"])
                if not treasure["taken"] and player.distance_to(treasure_pos) < 28:
                    treasure["taken"] = True
                    treasures_found += 10
                    message = "发现宝藏！+10"
                    message_timer = 1.4
                    for _ in range(12):
                        particles.append({
                            "x": treasure["x"],
                            "y": treasure["y"],
                            "vx": random.uniform(-45, 45),
                            "vy": random.uniform(-70, -20),
                            "life": random.uniform(0.45, 0.9),
                            "radius": random.randint(2, 4),
                        })

            message_timer = max(0, message_timer - dt)

            if oxygen <= 0 or treasures_found >= 80:
                finished = True

        draw_ocean(screen, elapsed)
        draw_rocks(screen, rocks)
        draw_fish(screen, fish, dt)
        draw_seaweed(screen, seaweed, elapsed)
        draw_corals(screen, corals)
        draw_bubbles(screen, bubbles, dt)
        draw_shipwreck(screen)
        for treasure in treasures:
            draw_treasure(screen, treasure)
        draw_manta(screen, manta)
        particles = draw_particles(screen, particles, dt)
        draw_diver(screen, player)
        draw_hud(screen, font, oxygen, treasures_found, message, message_timer)

        controls = font.render("点击移动 · WASD/方向键移动 · ESC退出", True, (200, 235, 245))
        screen.blit(controls, (20, HEIGHT - 34))

        if finished:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((2, 10, 35, 120))
            screen.blit(overlay, (0, 0))
            if treasures_found >= 80:
                message = "海底传奇！你找齐了宝藏！"
            else:
                message = f"氧气耗尽！你找到 {treasures_found} 分宝藏。"
            result = big_font.render(message, True, GOLD)
            hint = font.render("按 ESC 退出游戏", True, WHITE)
            screen.blit(result, result.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
            screen.blit(hint, hint.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60)))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
