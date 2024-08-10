import pygame
import random
import math

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
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 30
BONUS_ITEM_SIZE = 20
COMBO_MULTIPLIER_DURATION = 300  # frames

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paper Airplane Game")

class Plane:
    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2, PLANE_WIDTH, PLANE_HEIGHT)
        self.velocity = 0
        self.shield = 0
        self.speed_boost = 0
        self.slow_motion = 0
        self.combo_multiplier = 1
        self.last_powerup_time = 0

    def update(self, holding_space):
        if self.shield > 0:
            self.shield -= 1
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.slow_motion > 0:
            self.slow_motion -= 1

        if holding_space:
            self.velocity -= LIFT
        else:
            self.velocity += GRAVITY

        if self.speed_boost > 0:
            self.velocity = max(min(self.velocity, MAX_VELOCITY * 1.5), -MAX_VELOCITY * 1.5)
        elif self.slow_motion > 0:
            self.velocity = max(min(self.velocity, MAX_VELOCITY * 0.5), -MAX_VELOCITY * 0.5)
        else:
            self.velocity = max(min(self.velocity, MAX_VELOCITY), -MAX_VELOCITY)

        self.rect.y += int(self.velocity)

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            return True

        return False

    def draw(self):
        pygame.draw.rect(screen, PLANE_COLOR, self.rect)
        if self.shield > 0:
            pygame.draw.ellipse(screen, (0, 255, 0), self.rect.inflate(20, 20), 2)

class Obstacle:
    def __init__(self, obstacle_type='static'):
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - MIN_OBSTACLE_SIZE),
            random.randint(MIN_OBSTACLE_SIZE, MAX_OBSTACLE_SIZE),
            random.randint(MIN_OBSTACLE_SIZE, MAX_OBSTACLE_SIZE),
        )
        self.type = obstacle_type
        self.angle = 0
        self.direction = random.choice(['up', 'down'])
        self.speed = random.randint(2, 4)

    def update(self):
        if self.type == 'static':
            self.rect.x -= OBSTACLE_SPEED
        elif self.type == 'moving':
            self.rect.x -= OBSTACLE_SPEED
            if self.direction == 'up':
                self.rect.y -= self.speed
                if self.rect.top <= 0:
                    self.direction = 'down'
            elif self.direction == 'down':
                self.rect.y += self.speed
                if self.rect.bottom >= SCREEN_HEIGHT:
                    self.direction = 'up'
        elif self.type == 'rotating':
            self.rect.x -= OBSTACLE_SPEED
            self.angle += self.speed
            self.angle %= 360

    def draw(self):
        if self.type == 'rotating':
            rotated_surface = pygame.transform.rotate(pygame.Surface(self.rect.size), self.angle)
            rotated_surface.fill(OBSTACLE_COLOR)
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)
            screen.blit(rotated_surface, rotated_rect.topleft)
        else:
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

class PowerUp:
    def __init__(self, powerup_type):
        self.powerup_type = powerup_type
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - MIN_OBSTACLE_SIZE),
            PLANE_WIDTH,
            PLANE_HEIGHT,
        )
        self.duration = 300

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        if self.powerup_type == 'shield':
            color = (0, 255, 0)
        elif self.powerup_type == 'speed':
            color = (0, 255, 255)
        elif self.powerup_type == 'slow':
            color = (255, 0, 255)
        pygame.draw.rect(screen, color, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0

    def apply_effect(self, plane):
        if self.powerup_type == 'shield':
            plane.shield = self.duration
        elif self.powerup_type == 'speed':
            plane.speed_boost = self.duration
        elif self.powerup_type == 'slow':
            plane.slow_motion = self.duration

class BonusItem:
    def __init__(self, item_type):
        self.item_type = item_type
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - BONUS_ITEM_SIZE),
            BONUS_ITEM_SIZE,
            BONUS_ITEM_SIZE,
        )

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        if self.item_type == 'star':
            color = (255, 255, 0)
        elif self.item_type == 'coin':
            color = (255, 215, 0)
        pygame.draw.rect(screen, color, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0

    def apply_effect(self, plane, score):
        if self.item_type == 'star':
            score += 100
        elif self.item_type == 'coin':
            score += 50
        return score

def show_home_page():
    font = pygame.font.Font(None, FONT_SIZE)
    while True:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Paper Airplane Game", True, FONT_COLOR)
        start_text = font.render("Press ENTER to Start", True, FONT_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 30))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def show_score_report(score):
    font = pygame.font.Font(None, FONT_SIZE)
    while True:
        screen.fill(BACKGROUND_COLOR)
        score_text = font.render(f"Final Score: {score}", True, FONT_COLOR)
        restart_text = font.render("Press ENTER to Restart", True, FONT_COLOR)
        quit_text = font.render("Press ESC to Quit", True, FONT_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 - 30))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

def game_loop():
    clock = pygame.time.Clock()
    plane = Plane()
    obstacles = []
    winds = []
    powerups = []
    bonus_items = []
    frame_count = 0
    score = 0
    last_powerup_time = 0
    running = True
    holding_space = False

    font = pygame.font.Font(None, FONT_SIZE)

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

        if plane.update(holding_space):
            running = False

        if frame_count % OBSTACLE_FREQUENCY == 0:
            obstacle_type = random.choice(['static', 'moving', 'rotating'])
            obstacles.append(Obstacle(obstacle_type))

        if frame_count % WIND_FREQUENCY == 0:
            wind_type = 'up' if random.random() < 0.5 else 'down'
            winds.append(Wind(wind_type))

        if frame_count % (WIND_FREQUENCY * 2) == 0:
            powerup_type = random.choice(['shield', 'speed', 'slow'])
            powerups.append(PowerUp(powerup_type))

        if frame_count % 200 == 0:  # Adjust frequency of bonus items
            item_type = random.choice(['star', 'coin'])
            bonus_items.append(BonusItem(item_type))

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

        for powerup in powerups:
            powerup.update()
            powerup.draw()
            if plane.rect.colliderect(powerup.rect):
                powerup.apply_effect(plane)
                last_powerup_time = frame_count
                plane.combo_multiplier = 1.5  # Increase multiplier for power-ups
                powerups.remove(powerup)
            if powerup.is_off_screen():
                powerups.remove(powerup)

        for bonus_item in bonus_items:
            bonus_item.update()
            bonus_item.draw()
            if plane.rect.colliderect(bonus_item.rect):
                score = bonus_item.apply_effect(plane, score)
                bonus_items.remove(bonus_item)
            if bonus_item.is_off_screen():
                bonus_items.remove(bonus_item)

        plane.draw()

        for obstacle in obstacles:
            if plane.rect.colliderect(obstacle.rect):
                if plane.shield <= 0:
                    running = False

        # Update and draw score
        score += plane.rect.x // 10  # Increase score based on distance traveled
        if frame_count - last_powerup_time > COMBO_MULTIPLIER_DURATION:
            plane.combo_multiplier = 1  # Reset multiplier if duration has passed

        score_text = font.render(f"Score: {score * plane.combo_multiplier} m", True, FONT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    show_score_report(score)

# Show home page before starting the game loop
show_home_page()
game_loop()
