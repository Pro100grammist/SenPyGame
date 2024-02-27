import os
from pathlib import Path

import pygame

BASE_IMG_PATH = 'data/images/'


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        num_frames = self.img_duration * len(self.images)
        self.frame = (self.frame + 1) % num_frames if self.loop else min(self.frame + 1, num_frames - 1)
        self.done = self.frame >= num_frames - 1 if not self.loop else False

    def current_sprite(self):
        return self.images[int(self.frame / self.img_duration)]


def load_image(path):
    sprite = pygame.image.load(BASE_IMG_PATH + path)
    sprite.set_colorkey((0, 0, 0))
    return sprite


def load_images(path):
    return [load_image(path + '/' + name).convert_alpha() for name in sorted(os.listdir(BASE_IMG_PATH + path))]


def load_images_entities(path, trim_left=0, trim_right=0, scale_factor=0.85):
    sprites = []

    for sprite_path in sorted(Path(BASE_IMG_PATH + path).glob("*")):
        sprite = pygame.image.load(str(sprite_path)).convert_alpha()
        sprite.set_colorkey((0, 0, 0))
        sprite = sprite.subsurface(trim_left, 0, sprite.get_width() - trim_left - trim_right, sprite.get_height())
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale_factor), int(sprite.get_height() * scale_factor)))
        sprites.append(sprite)

    return sprites
