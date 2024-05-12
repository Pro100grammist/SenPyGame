import random
import pygame
import math

from settings import SCREEN_HEIGTH, SCREEN_WIDTH


class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
    
    def update(self):
        self.pos[0] += self.speed
        
    def render(self, surf, offset=(0, 0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))


class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []
        
        for i in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))
        
        self.clouds.sort(key=lambda x: x.depth)
    
    def update(self):
        for cloud in self.clouds:
            cloud.update()
    
    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)


class Raindrop(pygame.sprite.Sprite):
    def __init__(self, x, y, wind_strength):
        super().__init__()
        self.image = pygame.Surface((2, 10), pygame.SRCALPHA)
        color = (random.randint(100, 150), random.randint(100, 150), random.randint(200, 255), random.randint(50, 100))
        pygame.draw.rect(self.image, color, (0, 0, 2, 10))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.uniform(5, 10)
        self.wind_strength = wind_strength

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.wind_strength
        if self.rect.y > SCREEN_HEIGTH:
            self.rect.y = random.randint(-50, -10)
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.speed = random.uniform(5, 10)


class Snow(pygame.sprite.Sprite):
    def __init__(self, x, y, wind_strength):
        super().__init__()
        pass