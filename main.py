import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLANE_WIDTH = 50
PLANE_HEIGHT = 30
PLANE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
GRAVITY = 0.5
LIFT = 0.3
MAX_VELOCITY = 5
OBSTACLE_SPEED = 5
OBSTACLE_WIDTH = 80
OBSTACLE_HEIGHT = 200
OBSTACLE_GAP = 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paper Airplane Game")

class Plane:
    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2, PLANE_WIDTH, PLANE_HEIGHT)
        self.velocity = 0

    def update(self, holding_space):
        if holding_space:
            self.velocity -= LIFT
        else:
            self.velocity += GRAVITY
        self.velocity = max(min(self.velocity, MAX_VELOCITY), -MAX_VELOCITY)
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def draw(self):
        pygame.draw.rect(screen, PLANE_COLOR, self.rect)

class Obstacle:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.top_height = random.randint(50, SCREEN_HEIGHT - OBSTACLE_GAP - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - OBSTACLE_GAP

    def update(self):
        self.x -= OBSTACLE_SPEED

    def draw(self):
        top_rect = pygame.Rect(self.x, 0, OBSTACLE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, OBSTACLE_WIDTH, self.bottom_height)
        pygame.draw.rect(screen, OBSTACLE_COLOR, top_rect)
        pygame.draw.rect(screen, OBSTACLE_COLOR, bottom_rect)

    def is_off_screen(self):
        return self.x < -OBSTACLE_WIDTH

def game_loop():
    clock = pygame.time.Clock()
    plane = Plane()
    obstacles = []
    running = True
    holding_space = False

    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    holding_space = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    holding_space = False
        plane.update(holding_space)
        if len(obstacles) == 0 or obstacles[-1].x < SCREEN_WIDTH - 300:
            obstacles.append(Obstacle())
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw()
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
        plane.draw()
        for obstacle in obstacles:
            if plane.rect.colliderect(pygame.Rect(obstacle.x, 0, OBSTACLE_WIDTH, obstacle.top_height)) or \
               plane.rect.colliderect(pygame.Rect(obstacle.x, SCREEN_HEIGHT - obstacle.bottom_height, OBSTACLE_WIDTH, obstacle.bottom_height)):
                running = False
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

game_loop()
