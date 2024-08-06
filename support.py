import os
import pygame

from pathlib import Path


BASE_IMG_PATH = 'data/images/'
Sound = pygame.mixer.Sound


class Animation:
    def __init__(self, images, img_dur=5, loop=True, num_cycles=None):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
        self.num_cycles = num_cycles
        self.current_cycle = 0

        if self.num_cycles is not None:
            self.loop = True

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop, self.num_cycles)

    def update(self):
        num_frames = self.img_duration * len(self.images)
        self.frame += 1

        if self.frame >= num_frames:
            self.current_cycle += 1
            if self.loop and (self.num_cycles is None or self.current_cycle < self.num_cycles):
                self.frame = 0
            else:
                if self.num_cycles is not None and self.current_cycle >= self.num_cycles:
                    self.loop = False
                self.done = not self.loop
                self.frame = num_frames - 1 if not self.loop else 0

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


def antialiasing(a, b, t):
    return a + (b - a) * t


def render_scroll(coord):
    return tuple((int(i) for i in coord))


def volume_adjusting(sfx: dict[str, Sound], volume_settings: dict[str, float]):
    for sound, volume in volume_settings.items():
        sfx[sound].set_volume(volume)
