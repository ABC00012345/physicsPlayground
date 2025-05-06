import pygame
import math

# v0_x = v0 * cos(angle)
# v0_y = v0 * sin(angle)
# S_y = v0_y * t  -  1/2 g t^2
# S_x = v0_x * t


import pygame
import math

# Constants for screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Slider class to handle the sliders
class Slider:
    def __init__(self, x, y, width, min_value, max_value, initial_value, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.rect = pygame.Rect(x, y, width, self.height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        # Calculate initial position of handle
        initial_pos = ((initial_value - min_value) / (max_value - min_value)) * width
        self.handle_rect = pygame.Rect(x + initial_pos - 10, y - 5, 20, 30)
        self.selected = False

    def draw(self, screen, font):
        # Draw slider label and current value text
        label_text = font.render(f"{self.label}: {self.value:.2f}", True, (255, 255, 255))
        screen.blit(label_text, (self.x, self.y - 30))
        # Draw slider track and handle
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.handle_rect)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Check if mouse clicked on the handle to start dragging
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.handle_rect.collidepoint(event.pos):
                    self.selected = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = False

        if self.selected or (self.rect.collidepoint(mouse_pos) and mouse_pressed[0]):
            # Move the handle to the mouse x-position
            new_x = mouse_pos[0] - 10  # Center handle on mouse x
            new_x = max(self.rect.x, min(new_x, self.rect.x + self.width - self.handle_rect.width))
            self.handle_rect.x = new_x
            # Update the value based on handle position
            relative_pos = (self.handle_rect.x + 10 - self.rect.x) / self.width
            self.value = self.min_value + relative_pos * (self.max_value - self.min_value)

# Button class for Start button
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, (100, 200, 100), self.rect)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Projectile Simulation with Sliders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    
    running = True
    start_simulation = False

    # Create sliders
    slider_velocity = Slider(50, 50, 300, 0, 200, 100, "Velocity")
    slider_angle = Slider(50, 120, 300, 0, 90, 45, "Angle")
    slider_gravity = Slider(50, 190, 300, 0, 20, 9.81, "Gravity")

    # Create Start button
    start_button = Button(50, 260, 120, 40, "Start")

    # Initial projectile starting position
    projectile_start_x = 20
    projectile_start_y = 500  # near bottom of the screen
    projectile_radius = 15
    simulation_time = 0

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Update sliders if not simulating projectile motion
        if not start_simulation:
            slider_velocity.update(events)
            slider_angle.update(events)
            slider_gravity.update(events)

            # Check for start button press
            if start_button.is_clicked(events):
                start_simulation = True
                simulation_time = 0  # Reset simulation time

        # Fill the screen
        screen.fill("black")

        # Draw sliders and start button only when simulation is not running
        if not start_simulation:
            slider_velocity.draw(screen, font)
            slider_angle.draw(screen, font)
            slider_gravity.draw(screen, font)
            start_button.draw(screen, font)

        # If simulation is running, use the current slider values and animate projectile motion
        if start_simulation:
            # Get simulation parameters from slider values
            velocity = slider_velocity.value
            angle = slider_angle.value
            gravity = slider_gravity.value

            # Convert angle to radians
            angle_rad = math.radians(angle)
            # Calculate initial velocity components
            v0_x = velocity * math.cos(angle_rad)
            v0_y = velocity * math.sin(angle_rad)

            # Calculate projectile positions using physics formulas
            S_x = projectile_start_x + v0_x * simulation_time
            # Invert Y for Pygame (origin top-left)
            S_y = projectile_start_y - (v0_y * simulation_time - 0.5 * gravity * (simulation_time ** 2))

            # Draw the projectile
            pygame.draw.circle(screen, (255, 255, 255), (int(S_x), int(S_y)), projectile_radius)

            # Update simulation time
            simulation_time += 0.2

            # End simulation if projectile goes off-screen
            if S_y > SCREEN_HEIGHT or S_x > SCREEN_WIDTH:
                start_simulation = False
        else:

            L=75

            # Draw the projectile at the starting position
            pygame.draw.circle(screen, (255, 255, 255), (projectile_start_x, projectile_start_y), projectile_radius)

            # Get the angle in radians from the slider
            angle_radians = math.radians(slider_angle.value)

            # Calculate arrow tip coordinates using the fixed length L.
            # The arrow starts at the projectile center
            arrow_tip_x = projectile_start_x + L * math.cos(angle_radians)
            arrow_tip_y = projectile_start_y - L * math.sin(angle_radians)

            # Draw the arrow line
            pygame.draw.line(screen, (255, 0, 0),
                             (projectile_start_x, projectile_start_y),
                             (arrow_tip_x, arrow_tip_y), 3)


        # Render the updates
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()