import pygame
import random

# Initialize Pygame
pygame.init()

# Set up game constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 50, 80
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
INITIAL_SPEED = 3  # Slower initial speed
BACKGROUND_COLOR = (50, 50, 50)
CAR_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 255, 0)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Define the Car class
class Car:
    def __init__(self):
        self.x = WIDTH // 2 - CAR_WIDTH // 2
        self.y = HEIGHT - CAR_HEIGHT - 10
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.speed = INITIAL_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, CAR_COLOR, (self.x, self.y, self.width, self.height))

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

# Define the Obstacle class
class Obstacle:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        self.y = -OBSTACLE_HEIGHT
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed

# Restart button
def restart_button():
    font = pygame.font.SysFont("Arial", 30)
    text = font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

# Set up the game loop
def game_loop():
    car = Car()
    obstacles = []
    clock = pygame.time.Clock()
    score = 0
    game_over = False
    obstacle_spawn_rate = 60  # How frequently obstacles spawn (in frames)
    obstacle_speed = INITIAL_SPEED  # Initial speed of obstacles

    while not game_over:
        clock.tick(FPS)
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Get key presses for moving the car
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.move(-car.speed)
        if keys[pygame.K_RIGHT]:
            car.move(car.speed)

        # Spawn new obstacles with increasing frequency
        if random.randint(1, obstacle_spawn_rate) == 1:
            obstacles.append(Obstacle(obstacle_speed))

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(screen)

            # Check for collision with the car
            if (car.x < obstacle.x + obstacle.width and
                car.x + car.width > obstacle.x and
                car.y < obstacle.y + obstacle.height and
                car.y + car.height > obstacle.y):
                game_over = True

            # Remove obstacles that have gone off the screen
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        # Increase difficulty over time but more slowly
        if score % 20 == 0 and score > 0:  # Every 20 points, increase difficulty
            obstacle_speed += 0.2  # Increase speed of obstacles more slowly
            obstacle_spawn_rate = max(45, obstacle_spawn_rate - 2)  # Spawn obstacles more frequently, but more gradually

        # Draw the car
        car.draw(screen)

        # Display the score
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.update()

    # Game Over message
    font = pygame.font.SysFont("Arial", 50)
    game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    restart_button()

    pygame.display.update()

    # Wait for the player to press 'R' to restart or 'Q' to quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game if 'R' is pressed
                    game_loop()
                    waiting_for_input = False
                elif event.key == pygame.K_q:  # Quit the game if 'Q' is pressed
                    pygame.quit()
                    return

# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()
