import pygame
from variables import screen_width, screen_height, cols, paddle_col, paddle_outline
class paddle:
    def __init__(self, height=20, width=None, speed=10, radius=10, border=3):
        """Initialize the paddle with a border radius and border size."""
        self.height = height
        self.width = screen_width // cols if width is None else width
        self.speed = speed
        self.radius = radius
        self.border = border
        self.reset()


    def draw(self, screen):
        """Draw the paddle with rounded edges and a border."""
        # Outer border
        self.draw_rounded_rect(screen, self.rect, paddle_outline, self.radius, self.border)
        # Inner color
        inner_rect = pygame.Rect(
            self.rect.x + self.border,
            self.rect.y + self.border,
            self.rect.width - 2 * self.border,
            self.rect.height - 2 * self.border
        )
        self.draw_rounded_rect(screen, inner_rect, paddle_col, self.radius, 0)  # no border for inner color

    def draw_rounded_rect(self, screen, rect, color, radius, border):
        """Helper function to draw a rounded rectangle with the shape of the uploaded paddle."""
        # Draw the main rectangle (without the semi-circles)
        main_rect = pygame.Rect(rect.x + radius, rect.y, rect.width - 2 * radius, rect.height)
        pygame.draw.rect(screen, color, main_rect)

        # Draw the left and right semi-circles
        left_semi_circle = pygame.Rect(rect.x, rect.y, 2 * radius, rect.height)
        right_semi_circle = pygame.Rect(rect.x + rect.width - 2 * radius, rect.y, 2 * radius, rect.height)
        pygame.draw.ellipse(screen, color, left_semi_circle)  # Left semi-circle
        pygame.draw.ellipse(screen, color, right_semi_circle)  # Right semi-circle

        if border > 0:  # Only draw the inner part if there is a border
            # Draw the inner rectangle (without the semi-circles)
            inner_rect = pygame.Rect(rect.x + radius, rect.y + border, rect.width - 2 * radius, rect.height - 2 * border)
            pygame.draw.rect(screen, color, inner_rect)

            # Draw the inner left and right semi-circles
            inner_left_semi_circle = pygame.Rect(rect.x + border, rect.y + border, 2 * (radius - border), rect.height - 2 * border)
            inner_right_semi_circle = pygame.Rect(rect.x + rect.width - 2 * (radius - border) - border, rect.y + border, 2 * (radius - border), rect.height - 2 * border)
            pygame.draw.ellipse(screen, color, inner_left_semi_circle)  # Inner left semi-circle
            pygame.draw.ellipse(screen, color, inner_right_semi_circle)  # Inner right semi-circle
    def move(self):
        """Move the paddle based on user input."""
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def reset(self):
        """Reset the paddle to its initial position."""
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - (self.height * 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

