import random
import math
import pygame

from particle import Particle, Spark, create_particles, create_sparks
from support import Animation
from data import EXP_POINTS


class Projectile:
    def __init__(self, game, pos, direction, **kwargs):
        self.game = game
        self.pos = list(pos)
        self.direction = direction
        self.speed = kwargs.get('speed', 4)
        self.image = self.game.assets.get(kwargs.get('image', ''))

    def update(self):
        self.pos[0] += self.speed * self.direction
        rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        for enemy in self.game.enemies.copy():
            if rect.colliderect(enemy.rect()):
                self.game.enemies.remove(enemy)

        if self.game.map.checking_physical_tiles(self.pos):
            return True
        return False

    def render(self, surf, offset=(0, 0)):
        projectile_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        flipped_projectile = pygame.transform.flip(self.image, self.direction < 0, False)
        surf.blit(flipped_projectile, (projectile_pos[0] - flipped_projectile.get_width() / 2,
                                       projectile_pos[1] - flipped_projectile.get_height() / 2))


class AnimatedProjectile(Projectile):
    def __init__(self, game, pos, direction, sprites, loop, num_cycles=None, image_duration=5, transparency=255,
                 velocity=0, reverse=False, **kwargs):
        super().__init__(game, pos, direction, **kwargs)
        self.rotation = 0
        self.loop = loop
        self.num_cycles = num_cycles
        self.transparency = transparency
        self.velocity = velocity
        self.hit_on_target = False
        self.reverse = reverse
        self.animation = Animation(sprites, img_dur=image_duration, loop=self.loop, num_cycles=self.num_cycles)

    def update(self):
        self.animation.update()
        if self.reverse and self.animation.current_cycle >= self.num_cycles // 2:
            self.direction *= -1
            self.reverse = False
        self.pos[0] += self.velocity * self.direction

    def render(self, surf, offset=(0, 0)):
        projectile_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        rotated_frame = pygame.transform.rotate(self.animation.current_sprite(), self.rotation)
        flipped_frame = pygame.transform.flip(rotated_frame, self.direction < 0, False)
        flipped_frame.set_alpha(self.transparency)
        surf.blit(flipped_frame, (projectile_pos[0] - flipped_frame.get_width() / 2,
                                  projectile_pos[1] - flipped_frame.get_height() / 2))


class WormFireball(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['worm_fireball']
        super().__init__(game, pos, direction, sprites, True, image_duration=3, velocity=5)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 20, 20)


class AnimatedFireball(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['fireball']
        super().__init__(game, pos, direction, sprites, False, image_duration=3, velocity=4)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 20, 20)


class SkullSmoke(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['skullsmoke']
        super().__init__(game, pos, direction, sprites, False, image_duration=8, transparency=200)

    def rect(self):
        return pygame.Rect(self.pos[0] - 30, self.pos[1] - 40, 64, 74)


class HollySpell(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['holly_spell']
        super().__init__(game, pos, direction, sprites, False, image_duration=8)


class SpeedSpell(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['speed_spell']
        super().__init__(game, pos, direction, sprites, False, image_duration=1)


class BloodlustSpell(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['bloodlust_spell']
        super().__init__(game, pos, direction, sprites, False, image_duration=3)


class InvulnerabilitySpell(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['invulnerability_spell']
        super().__init__(game, pos, direction, sprites, False, image_duration=3)


class HitEffect(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['kaboom']
        super().__init__(game, pos, direction, sprites, False, image_duration=1)


class Necromancy(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['necromancy']
        super().__init__(game, pos, direction, sprites, False, image_duration=8)


class BloodEffect(AnimatedProjectile):
    def __init__(self, game, pos):
        sprites = game.assets['blood']
        direction = 0
        super().__init__(game, pos, direction, sprites, False, image_duration=4)


class FireTotem(AnimatedProjectile):
    def __init__(self, game, pos):
        sprites = game.assets['fire_totem']
        direction = 0
        super().__init__(game, pos, direction, sprites, False, image_duration=6)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()

    def rect(self):
        return pygame.Rect(self.pos[0] - self.rect_width // 2, self.pos[1] - self.rect_height // 2,
                           self.rect_width, self.rect_height)

    def update(self):
        self.animation.update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                enemy.health -= 1
                create_sparks(self.game, enemy.rect().center, shade='orange')

    # def render(self, surf, offset=(0, 0)):
    #     # temporary technical method for visualization of the totem lesion area
    #     super().render(surf, offset)
    #     rect = self.rect()
    #     rect.topleft = (rect.left - offset[0], rect.top - offset[1])
    #     pygame.draw.rect(surf, (255, 0, 0), rect, 2)


class WaterGeyser(AnimatedProjectile):
    def __init__(self, game, pos):
        sprites = game.assets['water_geyser']
        direction = 0
        super().__init__(game, pos, direction, sprites, False, image_duration=4)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()

    def rect(self):
        return pygame.Rect(self.pos[0] - self.rect_width // 2, self.pos[1] - self.rect_height // 2,
                           self.rect_width, self.rect_height)


class IceArrow(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['ice_arrow']
        super().__init__(game, pos, direction, sprites, False, image_duration=3, velocity=5)
        self.hit_on_target = False
        self.damage = random.randint(40, 60)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 20, 20)

    def update(self):
        super().update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                self.game.sfx['ice_hit'].play()
                sound = str(random.randint(1, 3))
                self.game.sfx.get(enemy.e_type + sound, self.game.sfx[enemy.e_type]).play()
                enemy.health -= self.damage
                self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(self.damage), (255, 255, 255)))
                create_sparks(self.game, enemy.rect().center, shade='ice')
                self.hit_on_target = True


class Tornado(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['tornado']
        super().__init__(game, pos, direction, sprites, loop=True, num_cycles=10, image_duration=6, velocity=1, reverse=True)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()

    def rect(self):
        return pygame.Rect(self.pos[0] - self.rect_width // 2, self.pos[1] - self.rect_height // 2,
                           self.rect_width, self.rect_height)

    def update(self):
        super().update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                damage = random.randint(0, 1)
                enemy.health -= damage
                # self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(damage), (255, 255, 255)))
                create_sparks(self.game, enemy.rect().center, shade='white', num_sparks=(1, 5))


class Arrow(Projectile):
    def __init__(self, game, pos, direction):
        super().__init__(game, pos, direction, **{'image': 'arrow'})


class Fireball(Projectile):
    def __init__(self, game, pos, direction):
        super().__init__(game, pos, direction, **{'image': 'fireball'})


class Shuriken(Projectile):
    def __init__(self, game, pos, direction, shooter, image, damage, speed, max_distance=360):
        super().__init__(game, pos, direction, **{'image': image, 'speed': speed})
        self.rotation = 0
        self.direction = direction
        self.rect = pygame.Rect(self.pos[0] - self.image.get_width() / 2, self.pos[1] - self.image.get_height() / 2,
                                self.image.get_width(), self.image.get_height())
        self.shooter = shooter
        self.recoil = False
        self.distance = 0
        self.max_distance = max_distance
        self.damage = damage

    def update(self):
        if self.distance >= self.max_distance:
            return True

        super().update()
        self.rotation += -20 if self.direction > 0 else 20
        self.rect = pygame.Rect(self.pos[0] - self.image.get_width() / 2, self.pos[1] - self.image.get_height() / 2,
                                self.image.get_width(), self.image.get_height())

        for enemy in self.game.enemies.copy():
            if self.rect.colliderect(enemy.hitbox):
                self.game.sfx['hit'].play()
                sound = str(random.randint(1, 3))
                self.game.sfx.get(enemy.e_type + sound, self.game.sfx[enemy.e_type]).play()

                enemy.health -= self.damage
                self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(self.damage), (255, 255, 255)))
                create_particles(self.game, enemy.rect().center, enemy.e_type)

                return True

        self.distance += abs(self.speed * self.direction)

        return False

    def render(self, surf, offset=(0, 0)):
        rotated_suriken = pygame.transform.rotate(self.image, self.rotation)
        surf.blit(rotated_suriken, (self.pos[0] - offset[0] - rotated_suriken.get_width() / 2,
                                    self.pos[1] - 8 - offset[1] - rotated_suriken.get_height() / 2))

        # self.rect.topleft = (self.rect.left - offset[0], self.rect.top - offset[1])
        # pygame.draw.rect(surf, (255, 0, 0), self.rect, 2)


class RustyShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='rusty_shuriken', damage=30, speed=4)


class SteelShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='steel_shuriken', damage=40, speed=3, max_distance=400)


class IceShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='ice_shuriken', damage=50, speed=5, max_distance=380)


class EmeraldShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='emerald_shuriken', damage=60, speed=4, max_distance=380)


class PoisonedShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='poisoned_shuriken', damage=75, speed=3, max_distance=380)


class StingerShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='stinger_shuriken', damage=90, speed=6, max_distance=420)


class PiranhaShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='shuriken_piranha', damage=100, speed=3, max_distance=400)


class SupersonicShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='supersonic_shuriken', damage=120, speed=7, max_distance=600)


class PhantomShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='phantom_shuriken', damage=150, speed=2, max_distance=500)


class DoubleBladedShuriken(Shuriken):
    def __init__(self, game, pos, direction, shooter):
        super().__init__(game, pos, direction, shooter, image='double_bladed_shuriken', damage=220, speed=3, max_distance=300)


class DamageNumber(pygame.sprite.Sprite):

    def __init__(self, position, number, color):
        super().__init__()
        self.x_offset = random.randint(-10, 10)
        self.y_offset = random.randint(16, 32)
        self.position = (position[0] + self.x_offset, position[1] - self.y_offset)
        self.size = 14
        self.color = color
        if 20 > number > 14:
            self.size = 16
        elif 25 > number > 20:
            self.size = 18
        elif 33 > number > 25:
            self.size = 20
        elif number > 33:
            self.size = 24
            self.color = (220, 20, 60)

        self.font = pygame.font.Font(None, size=self.size)
        self.image = self.font.render(str(number), True, self.color)
        self.rect = self.image.get_rect(center=self.position)
        self.timer = 60

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

    def render(self, surface, offset=(0, 0)):
        surface.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
