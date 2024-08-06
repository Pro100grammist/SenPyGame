import random
import math
import pygame

from support import Animation
from data import EXP_POINTS, COLOR_SCHEMA


class Particle:
    def __init__(self, game, p_type, pos, velocity=None, frame=0):
        if velocity is None:
            velocity = [0, 0]
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame
    
    def update(self):
        kill = False
        if self.animation.done:
            kill = True
        
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        self.animation.update()
        
        return kill
    
    def render(self, surf, offset=(0, 0)):
        img = self.animation.current_sprite()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))


class Spark:
    def __init__(self, pos, angle, speed, shade='red', spark_color=None):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.shade = shade
        self.spark_color = spark_color

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)
        return not self.speed

    def render(self, surf, offset=(0, 0)):
        render_points = [
            (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[0], self.pos[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[0], self.pos[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[1]),
        ]

        if self.spark_color:
            pygame.draw.polygon(surf, self.spark_color, render_points)
        else:
            color = COLOR_SCHEMA.get(self.shade, (255, 255, 255))
            pygame.draw.polygon(surf, color, render_points)


def create_particles(game, position, shade='red', num_particles=(10, 50), speed_range=(0, 5), offset=2, image='particle', frame_range=(0, 7)):
    for i in range(random.randint(*num_particles)):
        angle = random.random() * math.pi * 2
        speed = random.uniform(*speed_range)
        game.sparks.append(Spark(position, angle, offset + random.random(), shade))
        game.particles.append(Particle(game, image, position,
                                       velocity=[math.cos(angle + math.pi) * speed * 0.5,
                                                 math.sin(angle + math.pi) * speed * 0.5],
                                       frame=random.randint(*frame_range)))


def create_sparks(game, position, shade='red', num_sparks=(1, 5), offset=2):
    for i in range(random.randint(*num_sparks)):
        angle = random.random() * math.pi * 2
        spark_color = vary_color(COLOR_SCHEMA[shade])
        game.sparks.append(Spark(position, angle, offset + random.random(), shade, spark_color))


def vary_color(base_color):
    r, g, b = base_color[:3]
    variation = 80  # color variation amount
    r = min(255, max(0, r + random.randint(-variation, variation)))
    g = min(255, max(0, g + random.randint(-variation, variation)))
    return r, g, b
