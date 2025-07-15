import pygame
from scripts.entities import LightSource, Circles

DISPLAY_SIZE = (640, 480)
DISPLAY_MODE = (1280, 960)
SCREEN_CENTER = (320, 240)
COLORS = ["red", "yellow", "blue", "pink", "green", "salmon", "white", "black", "violet", "orange"]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_MODE)
        self.display = pygame.Surface(DISPLAY_SIZE)
        
        self.clock = pygame.time.Clock()
        
        self.pos = [SCREEN_CENTER[0] * 2, SCREEN_CENTER[1] * 2]
        self.follow = [0,0]

        self.current_color_index = 0
        self.circles = Circles(10, self, 60)
        self.lightsource = LightSource(5, "salmon", SCREEN_CENTER, 300, "salmon", self)
    
    def run(self):
        while True:
            self.display.fill((60, 60, 60))
            self.follow[0] += (self.pos[0] - self.follow[0]) / 10
            self.follow[1] += (self.pos[1] - self.follow[1]) / 10
            
            self.circles.update_circles()
            self.circles.render_circles(self.display)
            self.lightsource.update(self.follow)
            self.lightsource.render(self.display)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEMOTION:
                    self.pos = event.pos
                    self.pos = [self.pos[0] / 2, self.pos[1] / 2]
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if event.button == 1:
                        self.circles.generate_circles()
                    if event.button == 4:
                        amount = self.lightsource.get_ray_amount() + 5
                        self.lightsource = LightSource(5, "salmon", SCREEN_CENTER, amount, "salmon", self)
                        self.lightsource.rays.generate_rays()
                    if event.button == 5:
                        amount = self.lightsource.get_ray_amount() - 5
                        if amount <= 0: 
                            amount = 0
                        self.lightsource = LightSource(5, "salmon", SCREEN_CENTER, amount, "salmon", self)
                        self.lightsource.rays.generate_rays()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        amount = self.lightsource.get_ray_amount()
                        self.current_color_index
                        self.current_color_index = (self.current_color_index + 1) % len(COLORS)
                        index = self.current_color_index
                        self.lightsource = LightSource(5, COLORS[index], SCREEN_CENTER, amount, COLORS[index], self)
    
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            
Game().run()
                    
                
            
        