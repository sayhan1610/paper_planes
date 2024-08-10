import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLANE_WIDTH = 50
PLANE_HEIGHT = 30
PLANE_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (255, 0, 0)
UPWIND_COLOR = (255, 255, 0)
DOWNWIND_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (0, 0, 0)
GRAVITY = 0.5
LIFT = 0.3
MAX_VELOCITY = 5
OBSTACLE_SPEED = 5
MIN_OBSTACLE_SIZE = 20
MAX_OBSTACLE_SIZE = 100
OBSTACLE_FREQUENCY = 40
WIND_FREQUENCY = 80
WIND_EFFECT = 1

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

        # Check if the plane hits the top or bottom of the screen
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            return True  # Indicate that the plane has crashed

        return False

    def draw(self):
        pygame.draw.rect(screen, PLANE_COLOR, self.rect)

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - MIN_OBSTACLE_SIZE),
            random.randint(MIN_OBSTACLE_SIZE, MAX_OBSTACLE_SIZE),
            random.randint(MIN_OBSTACLE_SIZE, MAX_OBSTACLE_SIZE),
        )

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0

class Wind:
    def __init__(self, wind_type):
        self.wind_type = wind_type
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - MIN_OBSTACLE_SIZE),
            random.randint(MIN_OBSTACLE_SIZE, MAX_OBSTACLE_SIZE),
            random.randint(MIN_OBSTACLE_SIZE, MAX_OBSTACLE_SIZE),
        )

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        color = UPWIND_COLOR if self.wind_type == 'up' else DOWNWIND_COLOR
        pygame.draw.rect(screen, color, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0

    def apply_effect(self, plane):
        if self.wind_type == 'up':
            plane.velocity -= WIND_EFFECT
        elif self.wind_type == 'down':
            plane.velocity += WIND_EFFECT

def game_loop():
    clock = pygame.time.Clock()
    plane = Plane()
    obstacles = []
    winds = []
    frame_count = 0
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

        # Update the plane and check if it crashed
        if plane.update(holding_space):
            running = False  # End the game if the plane crashes

        # Add obstacles
        if frame_count % OBSTACLE_FREQUENCY == 0:
            obstacles.append(Obstacle())

        # Add wind (upwind or downwind)
        if frame_count % WIND_FREQUENCY == 0:
            wind_type = 'up' if random.random() < 0.5 else 'down'
            winds.append(Wind(wind_type))

        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw()
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)

        for wind in winds:
            wind.update()
            wind.draw()
            if plane.rect.colliderect(wind.rect):
                wind.apply_effect(plane)
            if wind.is_off_screen():
                winds.remove(wind)

        plane.draw()

        for obstacle in obstacles:
            if plane.rect.colliderect(obstacle.rect):
                running = False

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    pygame.quit()

game_loop()
