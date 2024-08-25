import random
import math
import pygame

from particle import Particle, Spark, create_particles, create_sparks
from support import Animation
from data import EXP_POINTS, PROJECTILE_DAMAGE, SHURIKEN_CONFIGS


class Projectile:
    def __init__(self, game, pos, direction, **kwargs):
        self.game = game
        self.pos = list(pos)
        self.direction = direction
        self.speed = kwargs.get('speed', 4)
        self.image = self.game.assets.get(kwargs.get('image', ''))

    def update(self):
        self.pos[0] += self.speed * self.direction

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
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()
        self.damage = 0
        self.show_hit_boxes = False

    def rect(self):
        return pygame.Rect(
            self.pos[0] - self.rect_width // 2,
            self.pos[1] - self.rect_height // 2,
            self.rect_width,
            self.rect_height
        )

    def update(self):
        self.animation.update()
        if self.reverse and self.animation.current_cycle >= self.num_cycles // 2:
            self.direction *= -1
            self.reverse = False
        self.pos[0] += self.velocity * self.direction

    def render(self, surf, offset=(0, 0)):
        rotated_frame = pygame.transform.rotate(self.animation.current_sprite(), self.rotation)
        self.image = rotated_frame
        super().render(surf, offset)
        if self.show_hit_boxes:
            super().render(surf, offset)
            rect = self.rect()
            rect.topleft = (rect.left - offset[0], rect.top - offset[1])
            pygame.draw.rect(surf, (255, 0, 0), rect, 2)


class WormFireball(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['worm_fireball']
        super().__init__(game, pos, direction, sprites, loop=True, image_duration=3, velocity=5)
        self.damage = PROJECTILE_DAMAGE.get('WormFireball', 49)


class AnimatedFireball(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['fireball']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=3, velocity=4)
        self.damage = PROJECTILE_DAMAGE.get('AnimatedFireball', 33)


class GroundFlame(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['ground_flame']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=8, velocity=2)
        self.damage = PROJECTILE_DAMAGE.get('GroundFlame', 1)


class DaemonBreath(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['blue_fire']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=8)


class DaemonBreathFlip(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['blue_fire_flip']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=8)


class DaemonFireBreath(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['fire']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=8)

    def update(self):
        self.animation.update()
        if self.animation.done:
            x_offset = 0
            for blaze in range(10):
                spawn_point = self.rect().midbottom
                spawn_point = (spawn_point[0] - 32 - x_offset, spawn_point[1] - 16)
                self.game.animated_projectiles.append(GroundFlame(self.game, spawn_point, direction=1))
                x_offset -= 16


class DaemonFireBreathFlip(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['fire_flip']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=8)

    def update(self):
        self.animation.update()
        if self.animation.done:
            x_offset = 0
            for blaze in range(10):
                spawn_point = self.rect().midbottom
                spawn_point = (spawn_point[0] + 32 - x_offset, spawn_point[1] - 16)
                self.game.animated_projectiles.append(GroundFlame(self.game, spawn_point, direction=-1))
                x_offset += 16


class SkullSmoke(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['skullsmoke']
        super().__init__(game, pos, direction, sprites, False, image_duration=8, transparency=200)

    def rect(self):
        return pygame.Rect(self.pos[0] - 30, self.pos[1] - 40, 64, 74)


class ToxicExplosion(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['toxic_explosion']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=4)


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


class HitEffect2(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['puff_and_stars']
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

    def update(self):
        self.animation.update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                enemy.take_damage(1)
                create_sparks(self.game, enemy.rect().center, shade='orange')

        for effect in self.game.magic_effects.copy():
            if self.rect().colliderect(effect.rect()) and isinstance(effect, Tornado):
                self.hit_on_target = True
                effect.hit_on_target = True
                spawn_point = self.rect().center
                spawn_point = (spawn_point[0], spawn_point[1] - 20)
                self.game.magic_effects.append(HellStorm(self.game, spawn_point, direction=0))
                self.game.shaking_screen_effect = max(64, self.game.shaking_screen_effect)
                self.game.sfx['hell_storm'].play()


class WaterGeyser(AnimatedProjectile):
    def __init__(self, game, pos):
        sprites = game.assets['water_geyser']
        direction = 0
        super().__init__(game, pos, direction, sprites, False, image_duration=4)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()


class MagicShield(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['magic_shield']
        super().__init__(game, pos, direction, sprites, loop=True, num_cycles=10, image_duration=1, velocity=1)
        self.safety_margin = 200
        self.shield_is_active = False

    def update(self):
        super().update()
        if self.safety_margin > 0:
            for projectile in self.game.animated_projectiles.copy():
                if self.rect().colliderect(projectile.rect()):
                    self.safety_margin -= projectile.damage
                    if not any(isinstance(effect, MagicShieldEffect) for effect in self.game.magic_effects):
                        spawn_point = self.rect().center
                        direction = 1 if projectile.direction == 1 else -1
                        self.game.magic_effects.append(
                            MagicShieldEffect(self.game, spawn_point, direction=direction))

                    if not isinstance(projectile, (DaemonBreath, DaemonBreathFlip,
                                                   DaemonFireBreath, DaemonFireBreathFlip)):
                        self.game.animated_projectiles.remove(projectile)

        else:
            self.hit_on_target = True
            self.game.player.shield = None


class MagicShieldEffect(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['magic_shield_effect']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=3)


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
                enemy.take_damage(self.damage)
                self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(self.damage), (255, 255, 255)))
                create_sparks(self.game, enemy.rect().center, shade='ice')
                self.hit_on_target = True

                # base chance of an additional lightning strike of 10% + 1% for each level of player wisdom (max 25%)
                if random.random() <= 0.1 + min(0.15, self.game.player.wisdom // 100):
                    spawn_point = enemy.rect().center
                    spawn_point = (spawn_point[0], spawn_point[1] - 140)
                    self.game.magic_effects.append(Thunderbolt(self.game, spawn_point, direction=0))
                    self.game.shaking_screen_effect = max(32, self.game.shaking_screen_effect)
                    self.game.sfx['thunder'].play()

        for effect in self.game.magic_effects.copy():
            if self.rect().colliderect(effect.rect()) and isinstance(effect, Tornado):
                self.hit_on_target = True
                effect.hit_on_target = True
                spawn_point = effect.rect().center
                spawn_point = (spawn_point[0], spawn_point[1] - 16)
                self.game.magic_effects.append(WaterTornado(self.game, spawn_point, self.direction))
                self.game.sfx['geyser'].play()


class Thunderbolt(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['thunderbolt']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=8)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()
        self.total_damage = 0
        self.damage = random.randint(2, 8) * min(1.5, 1 + self.game.player.wisdom // 50)

    def update(self):
        super().update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                self.total_damage += self.damage
                enemy.take_damage(self.damage)
                if self.animation.done:
                    self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(self.total_damage)))


class Tornado(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['tornado']
        super().__init__(game, pos, direction, sprites, loop=True, num_cycles=10, image_duration=6, velocity=1, reverse=True)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()

    def update(self):
        super().update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                damage = random.randint(0, 1)
                enemy.take_damage(damage)
                # self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(damage), (255, 255, 255)))
                create_sparks(self.game, enemy.rect().center, shade='white', num_sparks=(1, 5))


class WaterTornado(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['water_tornado']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=8, velocity=1)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()

    def update(self):
        super().update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                damage = random.randint(1, 3)
                enemy.take_damage(damage)
                # self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(damage), (255, 255, 255)))
                create_sparks(self.game, enemy.rect().center, shade='white', num_sparks=(1, 5))


class HellStorm(AnimatedProjectile):
    def __init__(self, game, pos, direction):
        sprites = game.assets['hell_storm']
        super().__init__(game, pos, direction, sprites, loop=False, image_duration=6)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()
        self.total_damage = 0
        self.damage = random.randint(4, 8)

    def update(self):
        super().update()
        for enemy in self.game.enemies.copy():
            if self.rect().colliderect(enemy.hitbox):
                self.total_damage += self.damage
                enemy.take_damage(self.damage)
                if self.animation.done:
                    self.game.sfx['hell_storm'].play()
                    self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(self.total_damage)))


class RunicObelisk(AnimatedProjectile):
    def __init__(self, game, pos, direction=0):
        sprites = game.assets['runic_obelisk']
        super().__init__(game, pos, direction, sprites, loop=True, num_cycles=10, image_duration=6)
        self.rect_width = sprites[0].get_width()
        self.rect_height = sprites[0].get_height()
        self.next_sound_time = pygame.time.get_ticks() + random.uniform(1000, 3000)
        action_range_increase = 100
        self.action_range = pygame.Rect(
            self.pos[0] - self.rect_width // 2 - action_range_increase // 2,
            self.pos[1] - self.rect_height // 2 - action_range_increase // 2,
            self.rect_width + action_range_increase,
            self.rect_height + action_range_increase
        )

    def update(self):
        super().update()
        current_time = pygame.time.get_ticks()
        if self.action_range.colliderect(self.game.player.rect()):
            if random.random() < 5 / 60:  # 5 units per second at 60 FPS
                if self.game.player.current_health < self.game.player.max_health:
                    self.game.player.current_health += 1
                if self.game.player.stamina < self.game.player.max_stamina:
                    self.game.player.stamina += 1
                # animation of treatment
                angle = random.random() * math.pi * 2  # a random angle in radians from 0 to 2π (360 degrees)
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(
                    Particle(
                        game=self.game,
                        p_type='cross_particle',
                        pos=self.game.player.rect().midtop,
                        velocity=pvelocity,
                        frame=random.randint(0, 7)
                    )
                )
                if current_time >= self.next_sound_time:
                    voice = str(random.randint(1, 3))
                    self.game.sfx['heal' + voice].play()
                    self.next_sound_time = current_time + random.uniform(1000, 3000)


class Arrow(Projectile):
    def __init__(self, game, pos, direction):
        super().__init__(game, pos, direction, **{'image': 'arrow'})
        self.damage = 20


class Fireball(Projectile):
    def __init__(self, game, pos, direction):
        super().__init__(game, pos, direction, **{'image': 'fireball'})
        self.damage = 33


class Shuriken(Projectile):
    def __init__(self, game, pos, direction, shooter, config):
        super().__init__(game, pos, direction, **{'image': config['image'], 'speed': config['speed']})
        self.shooter = shooter
        self.damage = config['damage']
        self.max_distance = config.get('max_distance', 360)
        self.distance = 0
        self.rotation = 0
        self.recoil = False
        self.rect = pygame.Rect(self.pos[0] - self.image.get_width() / 2,
                                self.pos[1] - self.image.get_height() / 2,
                                self.image.get_width(), self.image.get_height())

    def update(self):
        if self.distance >= self.max_distance:
            return True

        super().update()
        self.rotation += -20 if self.direction > 0 else 20
        self.rect = pygame.Rect(self.pos[0] - self.image.get_width() / 2,
                                self.pos[1] - self.image.get_height() / 2,
                                self.image.get_width(), self.image.get_height())

        for enemy in self.game.enemies.copy():
            if self.rect.colliderect(enemy.hitbox):
                self.game.sfx['hit'].play()
                sound = str(random.randint(1, 3))
                self.game.sfx.get(enemy.e_type + sound, self.game.sfx[enemy.e_type]).play()
                enemy.take_damage(self.damage)
                self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(self.damage), (255, 255, 255)))
                create_particles(self.game, enemy.rect().center, enemy.e_type)

                return True

        self.distance += abs(self.speed * self.direction)
        return False

    def render(self, surf, offset=(0, 0)):
        rotated_suriken = pygame.transform.rotate(self.image, self.rotation)
        surf.blit(rotated_suriken, (self.pos[0] - offset[0] - rotated_suriken.get_width() / 2,
                                    self.pos[1] - 8 - offset[1] - rotated_suriken.get_height() / 2))


class DamageNumber(pygame.sprite.Sprite):

    def __init__(self, position, number, color=(255, 255, 255)):
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
