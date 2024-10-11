import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

# Colors
BLACK = (0, 0, 0)
CYAN_GREEN = (0, 255, 200)

# Eye properties
eye_size = min(width, height) // 4
eye_distance = eye_size * 1.5

# Eye positions
left_eye_pos = (width // 2 - eye_distance // 2, height // 2)
right_eye_pos = (width // 2 + eye_distance // 2, height // 2)

clock = pygame.time.Clock()

def draw_squircle(surface, color, center, size, radius):
    rect = pygame.Rect(center[0] - size // 2, center[1] - size // 2, size, size)
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_eye(surface, center, time):
    # Draw the outer shape of the eye (squircle)
    outer_size = eye_size
    outer_radius = eye_size // 4
    draw_squircle(surface, CYAN_GREEN, center, outer_size, outer_radius)
    
    # Calculate the inner shape's dimensions
    inner_size = int(eye_size * 0.8)
    inner_radius = inner_size // 4
    
    # Animate the inner shape
    offset = math.sin(time * 2) * (eye_size * 0.05)
    inner_center = (center[0], center[1] + int(offset))
    
    # Draw the inner shape (squircle)
    draw_squircle(surface, BLACK, inner_center, inner_size, inner_radius)

running = True
start_time = pygame.time.get_ticks()

# Create a surface for anti-aliasing
aa_surface = pygame.Surface((width, height), pygame.SRCALPHA)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False

    aa_surface.fill((0, 0, 0, 0))  # Clear with transparent black

    current_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds

    # Draw eyes on the anti-aliasing surface
    draw_eye(aa_surface, left_eye_pos, current_time)
    draw_eye(aa_surface, right_eye_pos, current_time)

    # Scale down and up for anti-aliasing effect
    small_surface = pygame.transform.smoothscale(aa_surface, (width // 2, height // 2))
    smooth_surface = pygame.transform.smoothscale(small_surface, (width, height))

    # Draw the final result on the screen
    screen.fill(BLACK)
    screen.blit(smooth_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)  # 60 FPS for smooth animation

pygame.quit()
sys.exit()
