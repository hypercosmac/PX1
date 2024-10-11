import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up the display (adjust for your Raspberry Pi screen)
screen = pygame.display.set_mode((880, 528))
width, height = screen.get_size()
pygame.display.set_caption('Home Launcher')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN_GREEN = (0, 255, 200)
BLUE = (0, 122, 255)
PURPLE = (128, 0, 128)

# Font
font = pygame.font.Font(None, 36)

# App icons
class AppIcon:
    def __init__(self, x, y, width, height, color, text, script):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.script = script

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=20)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

# Create app icons
apps = [
    AppIcon(50, 50, 150, 150, CYAN_GREEN, "Eyes", "screensaver.py"),
    AppIcon(250, 50, 150, 150, (100, 100, 255), "Orchard Nav", "x-terminal-emulator -e 'python3 hailo/basic_pipelines/detection.py --labels-json hailo/resources/zaptrack-labels.json --hef zaptrack-2024-10-08.hef -i rpi'"),
    AppIcon(450, 50, 150, 150, BLUE, "Pose", "x-terminal-emulator -e 'rpicam-hello -t 0s --post-process-file /usr/share/rpi-camera-assets/imx500_posenet.json --viewfinder-width 1920 --viewfinder-height 1080 --framerate 30'"),
    AppIcon(650, 50, 150, 150, PURPLE, "People", "x-terminal-emulator -e 'rpicam-hello -t 0s --post-process-file /usr/share/rpi-camera-assets/imx500_mobilenet_ssd.json --viewfinder-width 1920 --viewfinder-height 1080 --framerate 30'")
    
]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for app in apps:
                if app.rect.collidepoint(pos):
                    try:
                        subprocess.Popen(["python3", app.script])
                    except FileNotFoundError:
                        print(f"Error: {app.script} not found.")

    # Draw background
    screen.fill(BLACK)

    # Draw app icons
    for app in apps:
        app.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
