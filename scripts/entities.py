import pygame
import math
import random

class Circle:
    def __init__(self, radius, color, pos):
        self.pos = list(pos)
        self.radius = radius
        self.color = color
    
    def update(self, movement=(0,0)):
        pass
    
    def render(self, surf):
        pygame.draw.circle(surf, self.color, self.pos, self.radius)
        
    def get_radius(self):
        return self.radius    
    
    def get_center(self):
        return self.pos
    
    def get_x(self):
        return self.pos[0]
    
    def get_y(self):
        return self.pos[1]
    
    def get_radius(self):
        return self.radius

class Circles:
    def __init__(self, amount, game, radius):
        self.amount = amount
        self.game = game
        self.radius = radius
        self.circles = []
        self.generate_circles()
        
    def generate_circles(self):
        self.circles.clear()
        for _ in range(self.amount):
            random_radius = random.randint(1, self.radius)
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            a_x = random_radius
            b_x = self.game.display.get_width() - random_radius
            pos_x = random.randint(a_x, b_x)
            
            a_y = random_radius
            b_y = self.game.display.get_height() - random_radius
            pos_y = random.randint(a_y, b_y)
            
            pos = [pos_x, pos_y]
            self.circles.append(Circle(random_radius, random_color, pos))
    
    def update_circles(self):
        for circle in self.circles:
            circle.update()
    
    def render_circles(self, surf):
        for circle in self.circles:
            circle.render(surf)
            
    def get_circles(self):
        return self.circles
    
class LightSource:
    def __init__(self, radius, color, pos, ray_amount, ray_color, game):
        self.radius = radius
        self.color = color
        self.pos = list(pos)
        self.ray_amount = ray_amount
        self.color = color
        self.velocity = [0, 0]
        self.game = game
        
        self.rays = Rays(ray_amount, ray_color, self.pos, self.game)
        
    def cast_rays(self, surf):
        self.rays.render_rays(surf, self.game.circles.get_circles())
        
    def update(self, movement):
        self.pos[0] = movement[0]
        self.pos[1] = movement[1]
    
    def render(self, surf):
        pygame.draw.circle(surf, self.color, self.pos, self.radius)
        self.cast_rays(surf)
    
    def get_ray_amount(self):
        return self.ray_amount

class Ray:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        
    def get_dx(self):
        return self.dx 

    def get_dy(self):
        return self.dy
    
    def get_dist(self, delta, dimension_length, origin_p):
        if delta != 0:
            if delta > 0:
                return (dimension_length - origin_p) / delta
            else:
                return -origin_p / delta
        else:
            return float('inf')

    def get_max_distance(self, width, height, origin):
        dist_x = self.get_dist(self.dx, width, origin[0])
        dist_y = self.get_dist(self.dy, height, origin[1])
        return min(dist_x, dist_y)
    
    def get_last_point_x(self, t, origin_p):
        return origin_p + t * self.dx
        
    def get_last_point_y(self, t, origin_p):
        return origin_p + t * self.dy
        
        
class Rays:
    def __init__(self, amount, color, origin, game):
        self.amount = amount
        self.color = color
        self.origin = origin
        self.game = game

        self.display_width = self.game.display.get_width()
        self.display_height = self.game.display.get_height()
        
        self.angle_inc = self.get_angle_increments()
        self.rays = self.generate_rays()
        
    def get_angle_increments(self):
        if self.amount > 0:
            return math.pi * 2 / self.amount
        else:
            return None
        
    def generate_rays(self):
        rays = []   
        for i in range(self.amount):
            angle = i * self.angle_inc
            dx, dy = math.cos(angle), math.sin(angle)
            rays.append(Ray(dx, dy))
        return rays

    def ray_circle_collision(self, dx, dy, c_center, radius):
        x_0, y_0 = self.origin
        h, k = c_center
        
        A = pow(dx, 2) + pow(dy, 2)
        B = 2 * (dx * (x_0 - h) + dy * (y_0 - k))
        C = pow(x_0 - h, 2) + pow(y_0 - k, 2) - pow(radius, 2)
        
        discriminant = pow(B, 2) - 4 * A * C
        
        if discriminant < 0:
            return None
        
        sqrt_disc = math.sqrt(discriminant)
        
        # Quadratic Solutions
        t1 = (-B - sqrt_disc) / 2 * A
        t2 = (-B + sqrt_disc) / 2 * A
        
        # Collided in two points or a tangent intersection
        if (t1 > 0 and t2 > 0):
            return min(t1, t2)
        elif t1 > 0:
            return t1
        elif t2 > 0:
            return t2
        else:
            return None
    
    def find_closest_collision(self, origin, ray, circles):
        closest_t = float('inf')
        dx, dy = ray.get_dx(), ray.get_dy()
        collision_point = None
        for circle in circles:
            center = circle.get_center()
            radius = circle.get_radius()
            t_collision = self.ray_circle_collision(dx, dy, center, radius)
            if t_collision is not None and t_collision < closest_t:
                closest_t = t_collision
                x_p = origin[0] + t_collision * dx
                y_p = origin[1] + t_collision * dy
                collision_point = (x_p, y_p)
        return collision_point
    
    def render_rays(self, surf, circles):
        for ray in self.rays:
            collision_p = self.find_closest_collision(self.origin, ray, circles)
            if collision_p is not None:
                end_x, end_y = collision_p
            else:
                max_dist = ray.get_max_distance(self.display_width, self.display_height, self.origin)
                end_x = ray.get_last_point_x(max_dist, self.origin[0])
                end_y = ray.get_last_point_y(max_dist, self.origin[1])
            end_pos = (end_x, end_y)
            pygame.draw.line(surf, self.color, self.origin, end_pos, 1)
    
    
            

                
    
    
    
    
            
        
        
    
    