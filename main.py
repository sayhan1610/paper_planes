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
PLANE_WIDTH = 70
PLANE_HEIGHT = 70
OBSTACLE_SIZE = 60  # Example size, adjust as needed
BONUS_ITEM_SIZE = 30
POWERUP_SIZE = 40  # Size for power-ups
WIND_SIZE = 50  # Size for wind images
GRAVITY = 0.5
LIFT = 0.3
MAX_VELOCITY = 5
OBSTACLE_SPEED = 5
OBSTACLE_FREQUENCY = 40
WIND_FREQUENCY = 80
WIND_EFFECT = 1
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 30
COMBO_MULTIPLIER_DURATION = 300  # frames

# Load and scale images
sky_background = pygame.image.load("images/sky.png")
sky_background = pygame.transform.scale(sky_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

plane_img = pygame.image.load("images/plane.gif")
plane_img_up = pygame.transform.rotate(plane_img, 15)
plane_img_down = pygame.transform.rotate(plane_img, -15)
plane_img = pygame.transform.scale(plane_img, (PLANE_WIDTH, PLANE_HEIGHT))
plane_img_up = pygame.transform.scale(plane_img_up, (PLANE_WIDTH, PLANE_HEIGHT))
plane_img_down = pygame.transform.scale(plane_img_down, (PLANE_WIDTH, PLANE_HEIGHT))

# Load and scale wind images
upwind_img = pygame.image.load("images/upwind.png")
downwind_img = pygame.image.load("images/downwind.png")
upwind_img = pygame.transform.scale(upwind_img, (WIND_SIZE, WIND_SIZE))
downwind_img = pygame.transform.scale(downwind_img, (WIND_SIZE, WIND_SIZE))

# Load and scale power-up images
speed_up_img = pygame.image.load("images/speed_up.png")
speed_down_img = pygame.image.load("images/speed_down.png")
shield_img = pygame.image.load("images/shield.png")  # Load shield image
speed_up_img = pygame.transform.scale(speed_up_img, (POWERUP_SIZE, POWERUP_SIZE))
speed_down_img = pygame.transform.scale(speed_down_img, (POWERUP_SIZE, POWERUP_SIZE))
shield_img = pygame.transform.scale(shield_img, (POWERUP_SIZE, POWERUP_SIZE))  # Scale shield image

# Load and scale bonus item images
coin_img = pygame.image.load("images/coin.png")
star_img = pygame.image.load("images/star.png")
coin_img = pygame.transform.scale(coin_img, (BONUS_ITEM_SIZE, BONUS_ITEM_SIZE))
star_img = pygame.transform.scale(star_img, (BONUS_ITEM_SIZE, BONUS_ITEM_SIZE))

# Scale obstacle images
obstacle_images = [
    pygame.transform.scale(pygame.image.load(f"images/object{i}.png").convert_alpha(), (OBSTACLE_SIZE, OBSTACLE_SIZE)) for i in range(10)
]

# Load sounds
bg_music = pygame.mixer.Sound("sounds/bg_music.mp3")
crash_sound = pygame.mixer.Sound("sounds/crash.mp3")
item_sound = pygame.mixer.Sound("sounds/item.mp3")
wind_sound = pygame.mixer.Sound("sounds/wind.mp3")

# Play background music on loop
bg_music.play(loops=-1)

# Define classes for game objects
class Plane:
    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT // 2, PLANE_WIDTH, PLANE_HEIGHT)
        self.velocity = 0
        self.shield = 0
        self.speed_boost = 0
        self.slow_motion = 0
        self.combo_multiplier = 1
        self.last_powerup_time = 0
        self.trail_positions = []  # List to store trail positions
        self.trail_length = 30  # Number of positions to keep for the trail

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

        # Update trail positions
        self.trail_positions.append(self.rect.midbottom)  # Track bottom center of the plane
        if len(self.trail_positions) > self.trail_length:
            self.trail_positions.pop(0)

        return False

    def draw(self):
        if self.velocity < -0.5:  # Plane is moving upward
            screen.blit(plane_img_up, self.rect.topleft)
        elif self.velocity > 0.5:  # Plane is moving downward
            screen.blit(plane_img_down, self.rect.topleft)
        else:  # Plane is level
            screen.blit(plane_img, self.rect.topleft)
        
        if self.shield > 0:
            # Draw the shield image
            screen.blit(shield_img, (self.rect.x - 10, self.rect.y - 10))
        
        # Draw the dashed trail
        for i in range(len(self.trail_positions) - 1):
            start_pos = self.trail_positions[i]
            end_pos = self.trail_positions[i + 1]
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            distance = math.sqrt(dx**2 + dy**2)
            num_dashes = int(distance / 10)  # Length of each dash
            for j in range(num_dashes):
                dash_start = (start_pos[0] + j * dx / num_dashes, start_pos[1] + j * dy / num_dashes)
                dash_end = (start_pos[0] + (j + 0.5) * dx / num_dashes, start_pos[1] + (j + 0.5) * dy / num_dashes)
                pygame.draw.line(screen, (255, 255, 255), dash_start, dash_end, 2)  # Draw dashed line



class Obstacle:
    def __init__(self, obstacle_type='static'):
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE),
            OBSTACLE_SIZE,
            OBSTACLE_SIZE,
        )
        self.type = obstacle_type
        self.angle = 0
        self.direction = random.choice(['up', 'down'])
        self.speed = random.randint(2, 4)
        self.image = random.choice(obstacle_images)

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
            screen.blit(self.image, self.rect.topleft)

    def is_off_screen(self):
        return self.rect.right < 0

class Wind:
    def __init__(self, wind_type):
        self.wind_type = wind_type
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - OBSTACLE_SIZE),
            OBSTACLE_SIZE,
            OBSTACLE_SIZE,
        )

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        image = upwind_img if self.wind_type == 'up' else downwind_img
        screen.blit(image, self.rect.topleft)

    def is_off_screen(self):
        return self.rect.right < 0

    def apply_effect(self, plane):
        if self.wind_type == 'up':
            plane.velocity -= WIND_EFFECT
        elif self.wind_type == 'down':
            plane.velocity += WIND_EFFECT
        wind_sound.play()  # Play wind sound when wind affects the plane

class PowerUp:
    def __init__(self, powerup_type):
        self.powerup_type = powerup_type
        self.rect = pygame.Rect(
            SCREEN_WIDTH,
            random.randint(0, SCREEN_HEIGHT - POWERUP_SIZE),
            POWERUP_SIZE,
            POWERUP_SIZE,
        )
        self.duration = 300

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self):
        if self.powerup_type == 'shield':
            screen.blit(shield_img, self.rect.topleft)  # Draw shield image for shield power-up
        elif self.powerup_type == 'speed':
            screen.blit(speed_up_img, self.rect.topleft)
        elif self.powerup_type == 'slow':
            screen.blit(speed_down_img, self.rect.topleft)

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
        image = star_img if self.item_type == 'star' else coin_img
        screen.blit(image, self.rect.topleft)

    def is_off_screen(self):
        return self.rect.right < 0

    def apply_effect(self, plane, score):
        if self.item_type == 'star':
            score += 100
        elif self.item_type == 'coin':
            score += 50
        item_sound.play()  # Play item sound when picking up an item
        return score
    
def draw_rounded_rect(surface, rect, color, corner_radius):
    """
    Draw a rectangle with rounded edges.
    :param surface: Surface to draw on.
    :param rect: pygame.Rect object.
    :param color: Color of the rectangle.
    :param corner_radius: Radius of the rounded corners.
    """
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def show_instructions_page():
    font = pygame.font.Font(None, FONT_SIZE)
    instructions = [
        "Instructions:",
        "1. Use SPACEBAR to make the plane fly upwards.",
        "2. Avoid obstacles that move horizontally, vertically, or rotate.",
        "3. Collect coins (+50 points) and stars (+100 points) to increase your score.",
        "4. Catch Power-Ups:",
        "    - Shield: Protects you from one obstacle hit.",
        "    - Speed Boost: Increases your vertical speed temporarily.",
        "    - Slow Motion: Slows down your vertical speed temporarily.",
        "5. Be mindful of the wind:",
        "    - Upwind: Pushes the plane upwards.",
        "    - Downwind: Pushes the plane downwards.",
        "6. The score multiplier increases with power-ups.",
        "Press ENTER to go back."
    ]

    while True:
        screen.blit(sky_background, (0, 0))
        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, FONT_COLOR)
            text_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
            # Define the rounded rectangle background
            bg_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, text_rect.height + 10)
            draw_rounded_rect(screen, bg_rect, (0, 0, 0), 10)  # Draw black rounded rectangle with corner radius 10
            screen.blit(instruction_text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True


def show_home_page():
    font = pygame.font.Font(None, FONT_SIZE)
    while True:
        screen.blit(sky_background, (0, 0))
        
        # Title text with rounded background
        title_text = font.render("Paper Airplane Game", True, FONT_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        title_bg_rect = pygame.Rect(title_rect.left - 10, title_rect.top - 5, title_rect.width + 20, title_rect.height + 10)
        draw_rounded_rect(screen, title_bg_rect, (0, 0, 0), 10)
        screen.blit(title_text, title_rect)

        # Start text with rounded background
        start_text = font.render("Press ENTER to Start", True, FONT_COLOR)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        start_bg_rect = pygame.Rect(start_rect.left - 10, start_rect.top - 5, start_rect.width + 20, start_rect.height + 10)
        draw_rounded_rect(screen, start_bg_rect, (0, 0, 0), 10)
        screen.blit(start_text, start_rect)

        # Instructions text with rounded background
        instructions_text = font.render("Press I for Instructions", True, FONT_COLOR)
        instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        instructions_bg_rect = pygame.Rect(instructions_rect.left - 10, instructions_rect.top - 5, instructions_rect.width + 20, instructions_rect.height + 10)
        draw_rounded_rect(screen, instructions_bg_rect, (0, 0, 0), 10)
        screen.blit(instructions_text, instructions_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_i:
                    if not show_instructions_page():
                        pygame.quit()
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
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

def game_loop():
    while True:
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
            screen.blit(sky_background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # Exit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        holding_space = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        holding_space = False

            if plane.update(holding_space):
                crash_sound.play()  # Play crash sound when plane hits an obstacle
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
                        crash_sound.play()  # Play crash sound when plane hits an obstacle
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

        if not show_score_report(score):
            break  # Exit the main loop if quitting the game

# Show home page before starting the game loop
show_home_page()
game_loop()
