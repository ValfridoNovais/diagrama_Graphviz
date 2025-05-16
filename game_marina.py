import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Bolinha - Rampas e Obstáculos")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
YELLOW = (255, 255, 200)
BLACK = (0, 0, 0)
BALL_COLORS = [(255, 0, 0), (0, 200, 0), (0, 0, 255), (255, 255, 0)]

# Bola
ball_radius = 12
ball_color_index = 0
ball_color = BALL_COLORS[ball_color_index]
ball_x = WIDTH // 2
ball_y = 100
ball_vx = 1.5
ball_vy = 0
gravity = 0.4
jump_strength = -8

# Níveis e rampas
LEVELS = []
NUM_LEVELS = 5
RAMP_HEIGHT = 100
RAMP_WIDTH = 400
RAMP_INCLINE = 60  # pixels inclinados
TRIANGLE_SIZE = 20

for i in range(NUM_LEVELS):
    ramps = []
    x_start = 50 if i % 2 == 0 else WIDTH - 50 - RAMP_WIDTH
    direction = 1 if i % 2 == 0 else -1
    for j in range(5):
        x = x_start + direction * (j % 2) * RAMP_WIDTH
        y = 100 + j * RAMP_HEIGHT
        ramps.append((x, y, direction))
    LEVELS.append(ramps)

current_level = 0

# Obstáculos
def generate_obstacles(ramps):
    obstacles = []
    for x, y, direction in ramps:
        if random.random() < 0.7:
            ox = x + RAMP_WIDTH // 2
            oy = y - RAMP_INCLINE // 2
            obstacles.append((ox, oy))
    return obstacles

obstacles = generate_obstacles(LEVELS[current_level])

# Funções
def reset_ball():
    global ball_x, ball_y, ball_vx, ball_vy
    ball_x = WIDTH // 2
    ball_y = 100
    ball_vx = 1.5
    ball_vy = 0

def draw_ramps(ramps):
    for x, y, direction in ramps:
        x_end = x + direction * RAMP_WIDTH
        y_end = y + RAMP_INCLINE
        pygame.draw.line(screen, BLACK, (x, y), (x_end, y_end), 5)

def draw_obstacles(obstacles):
    for x, y in obstacles:
        pygame.draw.polygon(screen, BLACK, [(x, y), (x - TRIANGLE_SIZE//2, y + TRIANGLE_SIZE),
                                            (x + TRIANGLE_SIZE//2, y + TRIANGLE_SIZE)])

def check_collision(obstacles):
    for ox, oy in obstacles:
        dist = math.hypot(ball_x - ox, ball_y - oy)
        if dist < ball_radius + TRIANGLE_SIZE // 2:
            return True
    return False

def check_goal():
    return HEIGHT - 50 < ball_y < HEIGHT and WIDTH // 2 - 50 < ball_x < WIDTH // 2 + 50

def draw_goal():
    pygame.draw.arc(screen, BLACK, (WIDTH//2 - 50, HEIGHT - 30, 100, 50), math.pi, 2*math.pi, 4)

# Loop principal
running = True
while running:
    screen.fill(YELLOW)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_vy = jump_strength
            if event.key == pygame.K_c:
                ball_color_index = (ball_color_index + 1) % len(BALL_COLORS)
                ball_color = BALL_COLORS[ball_color_index]

    # Física da bola
    ball_vy += gravity
    ball_x += ball_vx
    ball_y += ball_vy

    # Rebote nas laterais
    if ball_x < ball_radius or ball_x > WIDTH - ball_radius:
        ball_vx *= -1

    # Colisão
    if check_collision(obstacles):
        reset_ball()
        current_level = 0
        obstacles = generate_obstacles(LEVELS[current_level])

    # Meta
    if check_goal():
        current_level += 1
        if current_level >= NUM_LEVELS:
            current_level = 0
        reset_ball()
        obstacles = generate_obstacles(LEVELS[current_level])

    # Desenhos
    draw_ramps(LEVELS[current_level])
    draw_obstacles(obstacles)
    draw_goal()
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

