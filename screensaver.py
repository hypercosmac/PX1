import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Eye properties
eye_radius = min(width, height) // 8
pupil_radius = eye_radius // 2
eye_distance = eye_radius * 3

# Eye positions
left_eye_pos = (width // 2 - eye_distance // 2, height // 2)
right_eye_pos = (width // 2 + eye_distance // 2, height // 2)

# Pupil movement
max_pupil_offset = eye_radius - pupil_radius

clock = pygame.time.Clock()

def draw_eye(surface, center, pupil_offset):
    pygame.draw.circle(surface, WHITE, center, eye_radius)
    pupil_pos = (center[0] + pupil_offset[0], center[1] + pupil_offset[1])
    pygame.draw.circle(surface, BLUE, pupil_pos, pupil_radius)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False

    screen.fill(BLACK)

    # Calculate pupil offsets
    pupil_offset_x = random.randint(-max_pupil_offset, max_pupil_offset)
    pupil_offset_y = random.randint(-max_pupil_offset, max_pupil_offset)
    pupil_offset = (pupil_offset_x, pupil_offset_y)

    # Draw eyes
    draw_eye(screen, left_eye_pos, pupil_offset)
    draw_eye(screen, right_eye_pos, pupil_offset)

    pygame.display.flip()
    clock.tick(5)  # Update every 200ms for a slow, cute movement

pygame.quit()
sys.exit()
