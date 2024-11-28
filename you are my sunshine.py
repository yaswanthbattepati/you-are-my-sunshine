import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize the mixer for audio
pygame.mixer.init()

# Load the background music
background_music_path = r"C:\Users\yaswanth\Downloads\WhatsApp Audio 2024-11-28 at 10.22.53 AM.mpeg"
try:
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
except pygame.error as e:
    print(f"Error loading background music: {e}")

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Coins")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_image_path = r"C:\Users\yaswanth\Downloads\WhatsApp Image 2024-11-28 at 4.45.34 PM (1).jpeg"
player_image = pygame.image.load(player_image_path)
player_image = pygame.transform.scale(player_image, (player_size, player_size))
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_size, player_size)
player_speed = 10

# Coin settings
coin_size = 30
coin = pygame.Rect(
    random.randint(0, WIDTH - coin_size), random.randint(0, HEIGHT - coin_size), coin_size, coin_size
)

# Moving obstacle settings
obstacle_size = 60
obstacle_image_path = r"C:\Users\yaswanth\Downloads\WhatsApp Image 2024-11-28 at 4.45.34 PM.jpeg"
obstacle_image = pygame.image.load(obstacle_image_path)
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_size, obstacle_size))
obstacles = []
obstacle_speeds = []
max_obstacles = 5  # Set the fixed number of obstacles

# Initialize obstacles
for _ in range(max_obstacles):
    obstacles.append(
        pygame.Rect(
            random.randint(0, WIDTH - obstacle_size),
            random.randint(0, HEIGHT - obstacle_size),
            obstacle_size,
            obstacle_size,
        )
    )
    obstacle_speeds.append((random.choice([-3, 3]), random.choice([-3, 3])))

# Load background image
background_image_path = r"C:\Users\yaswanth\Downloads\WhatsApp Image 2024-11-28 at 4.46.58 PM.jpeg"
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Score
score = 0
font = pygame.font.Font(None, 36)
end_font = pygame.font.Font(None, 48)

# Clock for frame rate control
clock = pygame.time.Clock()


def show_instructions():
    """Display the instructions screen."""
    while True:
        screen.fill(WHITE)

        # Display instructions
        title_text = end_font.render("Welcome to Collect the Coins!", True, (0, 0, 255))
        instructions_text = font.render("Avoid obstacles and collect the yellow coin.", True, BLACK)
        controls_text = font.render("Use arrow keys to move.", True, BLACK)
        start_text = font.render("Press ENTER or SPACE to start the game.", True, RED)

        # Center the text
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        # Wait for user input to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:  # Start game
                    return


def display_game_over(final_score):
    """Display the 'Game Over' screen with final score."""
    screen.fill(WHITE)
    game_over_text = end_font.render("Better Luck Next Time!", True, RED)
    score_text = font.render(f"Your Score: {final_score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds
    pygame.quit()
    sys.exit()


# Show instructions before starting the game
show_instructions()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move player with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += player_speed
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Check for collision with the coin
    if player.colliderect(coin):
        score += 1
        # Reposition the coin
        coin.x = random.randint(0, WIDTH - coin_size)
        coin.y = random.randint(0, HEIGHT - coin_size)

    # Move obstacles
    for i, obstacle in enumerate(obstacles):
        obstacle.x += obstacle_speeds[i][0]
        obstacle.y += obstacle_speeds[i][1]

        # Reverse direction if an obstacle hits the screen edges
        if obstacle.left <= 0 or obstacle.right >= WIDTH:
            obstacle_speeds[i] = (-obstacle_speeds[i][0], obstacle_speeds[i][1])
        if obstacle.top <= 0 or obstacle.bottom >= HEIGHT:
            obstacle_speeds[i] = (obstacle_speeds[i][0], -obstacle_speeds[i][1])

        # Check for collision with the player
        if player.colliderect(obstacle):
            display_game_over(score)  # Call game over function

    # Draw everything
    screen.blit(background_image, (0, 0))  # Draw background image
    screen.blit(player_image, player.topleft)  # Draw player as image
    pygame.draw.ellipse(screen, YELLOW, coin)  # Coin

    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle.topleft)

    # Display the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)
