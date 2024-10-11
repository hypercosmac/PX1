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
eye_size = min(width, height) // 2  # Increased eye size for higher resolution
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

# Create a high-resolution surface for rendering
render_scale = 1  # Increase this for even higher resolution
render_width, render_height = width * render_scale, height * render_scale
render_surface = pygame.Surface((render_width, render_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False

    render_surface.fill(BLACK)

    current_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds

    # Scale up eye positions and size for the render surface
    scaled_left_eye_pos = (left_eye_pos[0] * render_scale, left_eye_pos[1] * render_scale)
    scaled_right_eye_pos = (right_eye_pos[0] * render_scale, right_eye_pos[1] * render_scale)
    scaled_eye_size = eye_size * render_scale

    # Draw eyes on the high-resolution render surface
    draw_eye(render_surface, scaled_left_eye_pos, current_time)
    draw_eye(render_surface, scaled_right_eye_pos, current_time)

    # Scale down the render surface to the screen size with anti-aliasing
    scaled_surface = pygame.transform.smoothscale(render_surface, (width, height))

    # Draw the final result on the screen
    screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)  # 60 FPS for smooth animation

pygame.quit()
sys.exit()
