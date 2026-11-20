"""A small interactive ray-casting experiment built with Pygame."""

import pygame

from scripts.entities import Circles, LightSource

DISPLAY_SIZE = (640, 480)
WINDOW_SIZE = (1280, 960)
SCREEN_CENTER = (DISPLAY_SIZE[0] // 2, DISPLAY_SIZE[1] // 2)
COLORS = ["red", "yellow", "blue", "pink", "green", "salmon", "white", "black", "violet", "orange"]


class Game:
    """Own the window and coordinate input, simulation, and drawing."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Ray Test")
        self.display = pygame.Surface(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        self.mouse_position = [*SCREEN_CENTER]
        self.light_position = [*SCREEN_CENTER]
        self.current_color_index = COLORS.index("salmon")
        self.circles = Circles(10, self, 60)
        self.lightsource = LightSource(5, "salmon", SCREEN_CENTER, 300, "salmon", self)

    def _set_ray_amount(self, amount):
        """Replace the light source while preserving its current color."""
        amount = max(0, amount)
        color = COLORS[self.current_color_index]
        self.lightsource = LightSource(5, color, SCREEN_CENTER, amount, color, self)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEMOTION:
            scale_x = DISPLAY_SIZE[0] / self.screen.get_width()
            scale_y = DISPLAY_SIZE[1] / self.screen.get_height()
            self.mouse_position = [event.pos[0] * scale_x, event.pos[1] * scale_y]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.circles.generate_circles()
            elif event.button == 4:
                self._set_ray_amount(self.lightsource.get_ray_amount() + 5)
            elif event.button == 5:
                self._set_ray_amount(self.lightsource.get_ray_amount() - 5)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.current_color_index = (self.current_color_index + 1) % len(COLORS)
            self._set_ray_amount(self.lightsource.get_ray_amount())
        return True

    def run(self):
        """Run the application until its window is closed."""
        running = True
        while running:
            for event in pygame.event.get():
                running = self._handle_event(event) and running

            self.display.fill((60, 60, 60))
            for axis in range(2):
                self.light_position[axis] += (self.mouse_position[axis] - self.light_position[axis]) / 10

            self.circles.update_circles()
            self.circles.render_circles(self.display)
            self.lightsource.update(self.light_position)
            self.lightsource.render(self.display)

            scaled = pygame.transform.scale(self.display, self.screen.get_size())
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    Game().run()
