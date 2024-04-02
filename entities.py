import math
import random

import pygame

from data import experience_points
from particle import Particle, Spark, create_particles
from projectile import (Suriken, AnimatedFireball, SkullSmoke, HollySpell, SpeedSpell,
                        BloodlustSpell, InvulnerabilitySpell, HitEffect, DamageNumber)


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

        self.last_movement = [0, 0]

        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.size[0] + 10, self.size[1])
        self.show_hitboxes = False

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update_hitbox(self):
        self.hitbox = pygame.Rect(self.pos[0] - 16, self.pos[1] - 12, self.size[0] + 32, self.size[1] + 12)

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.tiles_around_the_player(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.tiles_around_the_player(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] != 0:
            self.flip = False if movement[0] > 0 else True

        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

        self.update_hitbox()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - 10 - offset[1] + self.anim_offset[1]))


class Enemy(PhysicsEntity):
    def __init__(self, game, image,  pos, size, e_type, health):
        super().__init__(game, image, pos, size)

        self.walking = 0
        self.e_type = e_type
        self.health = health

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.checking_physical_tiles((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if self.collisions['right'] or self.collisions['left']:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if abs(dis[1]) < 16:
                    if self.flip and dis[0] < 0:
                        self.game.sfx['shoot'].play()
                        self.shoot([-7, 0], -1.5)
                    elif not self.flip and dis[0] > 0:
                        self.game.sfx['shoot'].play()
                        self.shoot([7, 0], 1.5)
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        if 50 <= abs(self.game.player.dashing) >= 40:
            if self.hitbox.colliderect(self.game.player.hitbox):
                self.game.shaking_screen_effect = max(16, self.game.shaking_screen_effect)
                self.game.sfx['hit'].play()
                self.game.sfx[self.e_type].play()
                shade = self.e_type
                stamina = self.game.player.stamina

                if stamina >= 25:
                    self.game.player.stamina -= 25
                else:
                    self.game.player.stamina = 0

                damage = 20 * self.game.player.double_power

                self.health -= damage

                self.game.damage_rates.append(DamageNumber(self.hitbox.center, damage, (255, 255, 255)))

                self.game.sfx[self.e_type].play()

                create_particles(self.game, self.rect().center, shade)

                if self.health <= 0:
                    self.game.effects.append(HitEffect(self.game, self.hitbox.midtop, 0))
                    self.game.player.increase_experience(experience_points[self.e_type])
                    return True
                else:
                    return False

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

    def shoot(self, offset, direction):
        pass


class OrcArcher(Enemy):

    def __init__(self, game, pos, size=(8, 15)):
        super().__init__(game, 'orc_archer', pos, size, e_type='orc_archer', health=100)

    def shoot(self, offset, direction):
        projectile_pos = [self.rect().centerx + offset[0], self.rect().centery + offset[1]]
        self.game.projectiles.append([projectile_pos, direction, 0, 'arrow'])

        for i in range(4):
            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi,
                                          2 + random.random(), 'white'))

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['bow'], True, False), (
                self.rect().centerx - self.game.assets['bow'].get_width() - offset[0],
                self.rect().centery - 16 - offset[1]))

        else:
            surf.blit(self.game.assets['bow'],
                      (self.rect().centerx + 4 - offset[0], self.rect().centery - 16 - offset[1]))

        if self.show_hitboxes:
            pygame.draw.rect(surf, (255, 0, 0), (self.hitbox.x - offset[0], self.hitbox.y - offset[1],
                                                 self.hitbox.width, self.hitbox.height), 1)


class BigZombie(Enemy):
    def __init__(self, game, pos, size=(8, 15)):
        super().__init__(game, 'big_zombie', pos, size, e_type='big_zombie', health=200)

    def shoot(self, offset, direction):
        direction = 1 if not self.flip else -1
        self.game.animated_projectiles.append(SkullSmoke(self.game, self.rect().center, direction))

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - 14 - offset[0] + self.anim_offset[0],
                   self.pos[1] - 20 - offset[1] + self.anim_offset[1]))

        if self.show_hitboxes:
            pygame.draw.rect(surf, (255, 0, 0), (self.hitbox.x - offset[0], self.hitbox.y - offset[1],
                                                 self.hitbox.width, self.hitbox.height), 1)


class BigDaemon(Enemy):
    def __init__(self, game, pos, size=(8, 15)):
        super().__init__(game, 'big_daemon', pos, size, e_type='big_daemon', health=300)

    def shoot(self, offset, direction):
        direction = 1 if not self.flip else -1
        self.game.animated_projectiles.append(AnimatedFireball(self.game, self.rect().center, direction))

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - 14 - offset[0] + self.anim_offset[0],
                   self.pos[1] - 20 - offset[1] + self.anim_offset[1]))

        if self.show_hitboxes:
            pygame.draw.rect(surf, (255, 0, 0), (self.hitbox.x - offset[0], self.hitbox.y - offset[1],
                                                 self.hitbox.width, self.hitbox.height), 1)


class Player(PhysicsEntity):
    def __init__(self, game, pos=(50, 50), size=(9, 17)):
        super().__init__(game, 'player', pos, size)

        self.level = 1
        self.experience = 0
        self.next_level_experience = 100
        self.exp_multiplier = 0

        self.name = 'Valkyrie'
        self.class_name = 'Warlock'

        self.air_time = 0
        self.jumps = 2
        self.wall_slide = False
        self.dashing = 0
        self.attack_pressed = False
        self.attack_timer = 0

        self.suriken_count = 20

        self.death_hit = False

        self.initial_size = size
        self.current_size = size

        self.life = 2
        self.experience_points = 60

        self.vitality = 0
        self.wisdom = 0
        self.agile = 0  # dex
        self.strength = 0
        self.defence = 0
        self.double_power = 1

        self.max_health = 100
        self.current_health = self.max_health

        self.max_mana = 100
        self.mana = self.max_mana

        self.max_stamina = 100
        self.min_stamina = 20
        self.stamina = self.max_stamina

        self.money = 0
        self.heal_potions = 3
        self.magic_potions = 3
        self.stamina_potions = 3
        self.power_potions = 3
        self.power_potion_timer = 600
        self.corruption = False
        self.corruption_timer = 601
        self.super_speed = 1
        self.super_speed_timer = 720
        self.critical_hit_chance = False
        self.critical_hit_timer = 1200
        self.invulnerability = False
        self.invulnerability_timer = 1000

        self.selected_item = 0
        self.selected_scroll = 0

        self.scrolls = {
            'holly_spell': 1,
            'speed_spell': 1,
            'bloodlust_spell': 1,
            'invulnerability_spell': 1,
        }

        self.skills_menu_is_active = False
        self.character_menu_is_active = False
        self.inventory_menu_is_active = False

        self.skills = {
            # health and vitality
            "Healing Mastery": False,
            "Vitality Infusion": False,
            "Poison Resistance": False,
            "Absorption": False,

            # endurance and ranged combat
            "Endurance Mastery": False,
            "Hawk's Eye": False,
            "Swift Reflexes": False,
            "Rapid Recovery": False,

            # strength and close combat
            "Ruthless Strike": False,
            "Weapon Mastery": False,
            "Steel Skin": False,
            "Berserker Rage": False,

            # magic and witchcraft
            "Sorcery Mastery": False,
            "Enchanter's Blessing": False,
            "Inscription Mastery": False,
            "Resurrection": False,
        }

        self.keys = {
            "steel_key": 2, "red_key": 2, "bronze_key": 2, "purple_key": 2, "gold_key": 2
        }

        self.inventory = []

        self.equipment = {}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.current_size[0], self.current_size[1])

    def adjust_position(self, pixels):
        self.pos[1] -= pixels

    def increase_experience(self, points):
        self.experience += points + ((points * self.exp_multiplier) // 100)
        if self.experience >= self.next_level_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience_points += 1
        self.next_level_experience = int(self.next_level_experience * 1.5)
        self.experience = 0
        self.vitality = self.skills["Vitality Infusion"] * self.level
        self.agile = self.skills["Endurance Mastery"] * self.level
        self.strength = self.skills["Weapon Mastery"] * self.level
        self.wisdom = self.skills["Sorcery Mastery"] * self.level
        self.max_health += self.vitality * 2
        self.max_mana += self.wisdom * 2
        self.max_stamina += self.agile * 2
        self.game.sfx['level_up'].play()

    def jump(self):
        voice = str(random.randint(1, 3))
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                self.game.sfx['jump' + voice].play()
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                self.game.sfx['jump' + voice].play()
                return True

        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.game.sfx['jump' + voice].play()
            self.air_time = 5
            return True

    def dash(self):
        if not self.dashing and self.stamina >= self.min_stamina:
            self.stamina -= 20 - (self.agile // 4)
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -65
            else:
                self.dashing = 65

    def attack(self):
        if not self.game.dead and not self.wall_slide:
            if self.stamina < self.min_stamina:
                self.game.sfx['tired'].play()
            else:
                self.attack_pressed = True
                self.game.sfx['attack'].play()
                voice = str(random.randint(1, 3))
                self.game.sfx['attack' + voice].play()
                self.stamina -= 10
                self.attack_timer = len(self.animation.images) * self.animation.img_duration
                self.current_size = (self.current_size[0] + 10, self.current_size[1])

                for enemy in self.game.enemies.copy():
                    if self.hitbox.colliderect(enemy.hitbox) and self.attack_pressed:
                        self.game.sfx['hit'].play()

                        # standard damage
                        damage = int(10 + (random.random() ** 2) * 10) + self.strength

                        # chance of critical hit
                        if random.random() < 0.1 + (0.1 * self.critical_hit_chance):
                            damage *= 3

                        if self.skills['Ruthless Strike']:
                            if random.random() < 0.1:
                                damage *= 2

                        if self.skills["Berserker Rage"]:
                            if self.current_health <= 25:
                                damage *= 0.3

                        # enemy damage
                        enemy.health -= int(damage * self.double_power)

                        self.game.sfx[enemy.e_type].play()
                        shade = enemy.e_type

                        if self.skills["Absorption"]:
                            restored_vitality = damage // 10
                            if self.current_health + restored_vitality <= self.max_health:
                                self.current_health += restored_vitality
                            else:
                                self.current_health = self.max_health

                        if enemy.e_type == 'big_zombie':
                            self.current_health -= 5
                            self.game.sfx['pain'].play()

                        self.game.shaking_screen_effect = max(16, self.game.shaking_screen_effect)

                        create_particles(self.game, enemy.rect().center, shade)

                        self.game.damage_rates.append(DamageNumber(enemy.hitbox.center, int(damage), (255, 255, 255)))

                        if enemy.health <= 0:
                            self.increase_experience(experience_points[enemy.e_type])
                            self.game.enemies.remove(enemy)

    def ranged_attack(self):
        if not self.game.dead and not self.wall_slide and self.suriken_count > 0 and self.stamina >= self.min_stamina:
            self.stamina -= 20 - (self.agile // 4)
            direction = 1 if not self.flip else -1
            self.game.munition.append(Suriken(self.game, self.rect().center, direction, shooter=self))
            self.suriken_count -= 1

    def cast_spell(self):
        if not self.game.dead and not self.wall_slide and self.mana >= 25:
            available_spells = sorted([key for key, value in self.scrolls.items() if value > 0])
            if available_spells:
                spell = available_spells[self.selected_scroll]
                direction = 0
                start_point = self.rect().center
                if self.flip:
                    start_point = (start_point[0] - 4, start_point[1] - 16)
                else:
                    start_point = (start_point[0] + 2, start_point[1] - 16)
                if spell == 'holly_spell' and self.mana >= 50:
                    self.mana -= 50 - self.wisdom // 2
                    self.game.spells.append(HollySpell(self.game, start_point, direction))
                if spell == 'speed_spell':
                    self.mana -= 25 - self.wisdom // 4
                    self.game.spells.append(SpeedSpell(self.game, start_point, direction))
                if spell == 'bloodlust_spell':
                    self.mana -= 25 - self.wisdom // 4
                    self.game.spells.append(BloodlustSpell(self.game, start_point, direction))
                if spell == 'invulnerability_spell':
                    self.mana -= 40 - self.wisdom // 2
                    self.game.spells.append(InvulnerabilitySpell(self.game, start_point, direction))
                if self.skills["Inscription Mastery"]:
                    if random.random() > 0.1 + (self.wisdom / 50):
                        self.scrolls[spell] -= 1
                else:
                    self.scrolls[spell] -= 1

    def use_item(self):
        if self.selected_item == 1 and self.heal_potions:
            self.current_health += 50 + (self.skills["Healing Mastery"] * 50)
            self.heal_potions -= 1
            self.game.sfx['use_potion'].play()
            self.game.sfx['healed'].play()
            if self.current_health > self.max_health:
                self.current_health = self.max_health
        elif self.selected_item == 2 and self.magic_potions:
            self.mana += 50
            self.magic_potions -= 1
            self.game.sfx['use_potion'].play()
            if self.mana > self.max_mana:
                self.mana = self.max_mana
        elif self.selected_item == 3 and self.stamina_potions:
            self.stamina += 50
            self.game.sfx['use_potion'].play()
            if self.stamina > self.max_stamina:
                self.stamina = self.max_stamina
            self.stamina_potions -= 1
        elif self.selected_item == 4 and self.power_potions and self.double_power == 1:
            self.double_power += 1
            self.game.sfx['use_potion'].play()
            self.power_potions -= 1

    def check_chest_collision(self):
        for chest in self.game.chests:
            if chest.rect.colliderect(self.rect()):
                if not chest.is_opened:
                    return chest

    @staticmethod
    def wave_value():
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def refreshing_player_status(self, item, in_dec=1):
        self.strength += item.increase_damage * in_dec
        self.defence += item.increase_defence * in_dec
        self.max_health += item.increase_health * in_dec
        self.max_stamina += item.increase_stamina * in_dec
        self.max_mana += item.increase_mana * in_dec
        self.exp_multiplier += item.increase_experience * in_dec

    def update(self, tilemap, movement=(0, 0)):
        speed = (movement[0] * self.super_speed, movement[1])
        super().update(tilemap, movement=speed)

        self.air_time += 1

        if self.air_time > 200:
            if not self.game.dead:
                self.game.shaking_screen_effect = max(16, self.game.shaking_screen_effect)
            self.game.dead += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2

        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

        if not self.wall_slide:
            if self.air_time > 4:
                if self.velocity[1] > 0:
                    self.set_action('fall')
                else:
                    self.set_action('jump')
            elif self.dashing:
                self.set_action('dash_attack')
            elif self.attack_pressed:
                self.set_action('attack')
            elif movement[0] != 0:
                self.set_action('run')
            elif self.death_hit:
                self.set_action('death')
            else:
                self.set_action('idle')

        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(
                    Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 10
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(
                Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        if self.attack_timer > 0:
            self.attack_timer = max(0, self.attack_timer - 1)
            if self.attack_timer == 0:
                self.attack_pressed = False
                self.current_size = self.initial_size

        if self.selected_item > 5:
            self.selected_item = 1

        if self.selected_scroll > sum(1 for value in self.scrolls.values() if value > 0) - 1:
            self.selected_scroll = 0

        if self.super_speed == 2:
            self.super_speed_timer -= 1
            if self.super_speed_timer <= 0:
                self.super_speed = 1
                self.super_speed_timer = 720

        if self.double_power == 2:
            self.power_potion_timer -= 1
            if self.power_potion_timer <= 0:
                self.double_power = 1
                self.power_potion_timer = 600

        if self.corruption:
            self.corruption_timer -= 1
            if self.corruption_timer % 15 == 0:
                self.current_health -= 1
            if self.corruption_timer <= 0:
                self.corruption = False
                self.corruption_timer = 601

        if self.invulnerability:
            self.invulnerability_timer -= 1
            if self.invulnerability_timer <= 0:
                self.invulnerability = False
                self.invulnerability_timer = 1000

        if self.critical_hit_chance:
            self.critical_hit_timer -= 1
            if self.critical_hit_timer <= 0:
                self.critical_hit_chance = False
                self.critical_hit_timer = 1200

        if self.stamina < self.max_stamina:
            if not self.wall_slide and not self.dashing and not self.corruption:
                self.stamina += 0.1 + (self.skills["Rapid Recovery"] * 0.1)

    def render(self, surf, offset=(0, 0)):
        current_image = self.animation.current_sprite()
        alpha = 96 if self.invulnerability else 255  # transparency value depending on self.invulnerability
        current_image.set_alpha(alpha)

        if not self.flip:
            surf.blit(pygame.transform.flip(current_image, self.flip, False),
                      (self.pos[0] - 14 - offset[0] + self.anim_offset[0],
                       self.pos[1] - 16 - offset[1] + self.anim_offset[1]))
        else:
            surf.blit(pygame.transform.flip(current_image, self.flip, False),
                      (self.pos[0] - 28 - offset[0] + self.anim_offset[0],
                       self.pos[1] - 16 - offset[1] + self.anim_offset[1]))

        if self.show_hitboxes:
            pygame.draw.rect(surf, (0, 255, 0), (self.hitbox.x - offset[0], self.hitbox.y - offset[1],
                                                 self.hitbox.width, self.hitbox.height), 1)

        # pygame.draw.rect(surf, (0, 255, 0), (self.rect().x - offset[0], self.rect().y - offset[1],
        #                                      self.rect().width, self.rect().height), 1)
