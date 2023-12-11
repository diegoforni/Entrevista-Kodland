import sys
import random
import math
import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (20, 20, 20)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agujeros")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for menu text
font = pygame.font.Font(None, 36)

# Function to display text on the screen
def draw_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to create buttons
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        draw_text(self.text, self.rect.centerx, self.rect.centery)

# Function to create avoider circles
def create_avoider_circle():
    avoider_circle_size_factor = random.uniform(0.3, 1.5)
    avoider_circle_radius = int(player_circle_radius * avoider_circle_size_factor)

    # Generate a random color within the specified range
    avoider_circle_color = (
        random.randint(40, 200),
        random.randint(40, 200),
        random.randint(40, 200)
    )

    avoider_circle_speed = 2

    # Choose a random corner (1, 2, 3, or 4) to place the circle
    corner = random.choice([1, 2, 3, 4])

    if corner == 1:
        # Top-left corner
        avoider_circle_x = random.randint(0, WIDTH // 2)
        avoider_circle_y = random.randint(0, HEIGHT // 2)
    elif corner == 2:
        # Top-right corner
        avoider_circle_x = random.randint(WIDTH // 2, WIDTH - avoider_circle_radius)
        avoider_circle_y = random.randint(0, HEIGHT // 2)
    elif corner == 3:
        # Bottom-left corner
        avoider_circle_x = random.randint(0, WIDTH // 2)
        avoider_circle_y = random.randint(HEIGHT // 2, HEIGHT - avoider_circle_radius)
    else:
        # Bottom-right corner
        avoider_circle_x = random.randint(WIDTH // 2, WIDTH - avoider_circle_radius)
        avoider_circle_y = random.randint(HEIGHT // 2, HEIGHT - avoider_circle_radius)

    return {'radius': avoider_circle_radius, 'color': avoider_circle_color, 'speed': avoider_circle_speed, 'x': avoider_circle_x, 'y': avoider_circle_y, 'direction': math.radians(random.uniform(0, 360))}

# Create buttons for the menu
start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Empezar", "start")
quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Salir", "quit")

# List of buttons
buttons = [start_button, quit_button]

# Main menu loop
in_menu = True
while in_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if any button was clicked
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    if button.action == "start":
                        in_menu = False  # Start the game
                    elif button.action == "quit":
                        pygame.quit()
                        sys.exit()

    # Clear the screen
    screen.fill(WHITE)
    draw_text("Intenta comer los círculos más chicos que tí!",WIDTH/2, 30 )

    # Draw buttons
    for button in buttons:
        button.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Game loop
player_circle_radius = 30
player_circle_color = (20, 20, 20)
circle_x = WIDTH // 2
circle_y = HEIGHT // 2
circle_speed = 5

# Create multiple avoider circles at the start of the game
num_avoider_circles = 3
avoider_circles = [create_avoider_circle() for _ in range(num_avoider_circles)]

eaten_count = 0  # Counter for red circles eaten by the player

# Timer variables
start_time = pygame.time.get_ticks()  # Get the initial time in milliseconds
seconds_passed = 0

# Game over flag
game_over = False

# Create a button for going back to the main menu
menu_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Main Menu", "menu")

# Main game loop
while not in_menu and not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = True  # Go back to the main menu

    keys = pygame.key.get_pressed()

    if not game_over:
        # Update circle position based on arrow keys
        if keys[pygame.K_LEFT] and circle_x > player_circle_radius:
            circle_x -= circle_speed
        if keys[pygame.K_RIGHT] and circle_x < WIDTH - player_circle_radius:
            circle_x += circle_speed
        if keys[pygame.K_UP] and circle_y > player_circle_radius:
            circle_y -= circle_speed
        if keys[pygame.K_DOWN] and circle_y < HEIGHT - player_circle_radius:
            circle_y += circle_speed

        # Update avoider circle positions to follow a random direction each second
        for avoider_circle in avoider_circles:
            avoider_circle['x'] += avoider_circle['speed'] * math.cos(avoider_circle['direction'])
            avoider_circle['y'] += avoider_circle['speed'] * math.sin(avoider_circle['direction'])

            # Ensure avoider circles stay within the screen boundaries
            avoider_circle['x'] = max(avoider_circle['radius'], min(avoider_circle['x'], WIDTH - avoider_circle['radius']))
            avoider_circle['y'] = max(avoider_circle['radius'], min(avoider_circle['y'], HEIGHT - avoider_circle['radius']))

        # Check collision between player and avoider circles
        for avoider_circle in avoider_circles:
            distance = ((circle_x - avoider_circle['x'])**2 + (circle_y - avoider_circle['y'])**2)**0.5
            if distance < player_circle_radius + avoider_circle['radius']:
                # Check if avoider circle is bigger than the player circle
                if avoider_circle['radius'] > player_circle_radius:
                    # Game over
                    game_over = True
                else:
                    # Player circle "eats" the red one and grows by 10%
                    player_circle_radius += player_circle_radius * 0.1
                    eaten_count += 1
                    # Remove the eaten circle
                    avoider_circles.remove(avoider_circle)
                    # Create two new circles
                    avoider_circles.extend([create_avoider_circle() for _ in range(2)])

        # Decrease the size of the avoider circles by 1% each second
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        if elapsed_time >= 1000:  # 1000 milliseconds = 1 second
            for avoider_circle in avoider_circles:
                avoider_circle['radius'] *= 0.99  # Decrease size by 1%
                avoider_circle['direction'] = math.radians(random.uniform(0, 360))  # Choose a new random direction
            start_time = current_time  # Reset the timer

        # Clear the screen
        screen.fill(WHITE)

        # Draw the player's circle
        pygame.draw.circle(screen, player_circle_color, (int(circle_x), int(circle_y)), int(player_circle_radius))

        # Draw the avoider circles
        for avoider_circle in avoider_circles:
            pygame.draw.circle(screen, avoider_circle['color'], (int(avoider_circle['x']), int(avoider_circle['y'])), int(avoider_circle['radius']))

        # Display the counter for red circles eaten in the upper right corner
        draw_text(f"Puntos: {eaten_count}", WIDTH - 100, 20)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Game over loop
# Game over loop
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the quit button was clicked
            if quit_button.rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Display game over text
    draw_text("Juego acabado", WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(f"Puntos: {eaten_count}", WIDTH // 2, HEIGHT // 2)


    quit_button.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)



# Main menu loop
while in_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if any button was clicked
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    if button.action == "start":
                        in_menu = False  # Start the game
                    elif button.action == "quit":
                        pygame.quit()
                        sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Draw buttons
    for button in buttons:
        button.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()