import pygame
import random
import math

pygame.init()

# Set up the screen before loading images
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paper Airplane Game")

# Constants
PLANE_WIDTH = 50
PLANE_HEIGHT = 30
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

# Load images after screen initialization
sky_background = pygame.image.load("images/sky.png")
sky_background = pygame.transform.scale(sky_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

plane_img = pygame.image.load("images/plane.gif")
plane_img_up = pygame.transform.rotate(plane_img, 15)
plane_img_down = pygame.transform.rotate(plane_img, -15)
plane_img = pygame.transform.scale(plane_img, (PLANE_WIDTH, PLANE_HEIGHT))
plane_img_up = pygame.transform.scale(plane_img_up, (PLANE_WIDTH, PLANE_HEIGHT))
plane_img_down = pygame.transform.scale(plane_img_down, (PLANE_WIDTH, PLANE_HEIGHT))

upwind_img = pygame.image.load("images/upwind.png")
downwind_img = pygame.image.load("images/downwind.png")
speed_up_img = pygame.image.load("images/speed_up.png")
speed_down_img = pygame.image.load("images/speed_down.png")
coin_img = pygame.image.load("images/coin.png")
star_img = pygame.image.load("images/star.png")

# Obstacle images
obstacle_images = [
    pygame.image.load(f"images/object{i}.png").convert_alpha() for i in range(10)
]

# Continue with the rest of your game code...


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
        self.image = plane_img

    def update(self, holding_space):
        if self.shield > 0:
            self.shield -= 1
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.slow_motion > 0:
            self.slow_motion -= 1

        if holding_space:
            self.velocity -= LIFT
            self.image = plane_img_up
        else:
            self.velocity += GRAVITY
            self.image = plane_img_down

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
        screen.blit(self.image, self.rect)
        if self.shield > 0:
            pygame.draw.ellipse(screen, (0, 255, 0), self.rect.inflate(20, 20), 2)


class Obstacle:
    def __init__(self, obstacle_type='static'):
        self.image = random.choice(obstacle_images)
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))
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
            rotated_surface = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_surface.get_rect(center=self.rect.center)
            screen.blit(rotated_surface, rotated_rect.topleft)
        else:
            screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0


class Wind:
    def __init__(self, wind_type):
        self.wind_type = wind_type
        self.image = upwind_img if wind_type == 'up' else downwind_img
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))
        )

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)

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
        if powerup_type == 'speed':
            self.image = speed_up_img
        elif powerup_type == 'slow':
            self.image = speed_down_img
        else:
            self.image = pygame.Surface((PLANE_WIDTH, PLANE_HEIGHT))  # Default shape
            self.image.fill((0, 255, 0))  # Shield color

        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))
        )
        self.duration = 300

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)

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
        self.image = star_img if item_type == 'star' else coin_img
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT))
        )

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)

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
        screen.blit(sky_background, (0, 0))
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
        screen.blit(sky_background, (0, 0))
        score_text = font.render(f"Final Score: {score}", True, FONT_COLOR)
        retry_text = font.render("Press ENTER to Retry", True, FONT_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 - 30))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True


def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, FONT_SIZE)

    plane = Plane()
    obstacles = []
    winds = []
    powerups = []
    bonus_items = []

    score = 0
    frame_count = 0

    holding_space = False
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    holding_space = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    holding_space = False

        game_over = plane.update(holding_space)
        frame_count += 1

        if frame_count % OBSTACLE_FREQUENCY == 0:
            obstacle_type = random.choice(['static', 'moving', 'rotating'])
            obstacles.append(Obstacle(obstacle_type))

        if frame_count % WIND_FREQUENCY == 0:
            wind_type = random.choice(['up', 'down'])
            winds.append(Wind(wind_type))

        if frame_count % 200 == 0:
            powerup_type = random.choice(['shield', 'speed', 'slow'])
            powerups.append(PowerUp(powerup_type))

        if frame_count % 150 == 0:
            item_type = random.choice(['coin', 'star'])
            bonus_items.append(BonusItem(item_type))

        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.is_off_screen():
                obstacles.remove(obstacle)
            if plane.rect.colliderect(obstacle.rect):
                if plane.shield > 0:
                    obstacles.remove(obstacle)
                else:
                    game_over = True

        for wind in winds[:]:
            wind.update()
            if wind.is_off_screen():
                winds.remove(wind)
            if plane.rect.colliderect(wind.rect):
                wind.apply_effect(plane)

        for powerup in powerups[:]:
            powerup.update()
            if powerup.is_off_screen():
                powerups.remove(powerup)
            if plane.rect.colliderect(powerup.rect):
                powerup.apply_effect(plane)
                powerups.remove(powerup)

        for bonus_item in bonus_items[:]:
            bonus_item.update()
            if bonus_item.is_off_screen():
                bonus_items.remove(bonus_item)
            if plane.rect.colliderect(bonus_item.rect):
                score = bonus_item.apply_effect(plane, score)
                bonus_items.remove(bonus_item)

        screen.blit(sky_background, (0, 0))

        plane.draw()

        for obstacle in obstacles:
            obstacle.draw()

        for wind in winds:
            wind.draw()

        for powerup in powerups:
            powerup.draw()

        for bonus_item in bonus_items:
            bonus_item.draw()

        score_text = font.render(f"Score: {score}", True, FONT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    if show_score_report(score):
        main()


show_home_page()
main()
