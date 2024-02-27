import os
import sys
import math
import random

import pygame

from data import load_assets, load_sfx, color_schema
from entities import Player, OrcArcher, BigZombie, BigDaemon
from tilemap import Tilemap
from weather import Clouds, Raindrop
from particle import Particle, Spark, create_particles
from player_controller import PlayerController
from ui import UI
from support import volume_adjusting
from settings import *

from projectile import (SkullSmoke, AnimatedFireball, HollySpell, SpeedSpell,
                                BloodlustSpell, InvulnerabilitySpell, BloodEffect)
from items import (Coin, Gem, HealthPoison, MagicPoison, StaminaPoison,
                           PowerPoison, HollyScroll, SpeedScroll, BloodlustScroll,
                           InvulnerabilityScroll)


pygame.init()
pygame.display.set_caption('Some Simple Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))


class Game:
    def __init__(self):

        self.screen = screen
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGTH), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGTH))
        self.clock = pygame.time.Clock()
        self.sfx = load_sfx()
        self.volume_settings = volume_settings

        self.assets = load_assets()
        self.clouds = Clouds(self.assets['clouds'])
        self.raindrops = pygame.sprite.Group()

        self.movement = [False, False]
        self.player = Player(self)
        self.player_controller = PlayerController(self.player, self.sfx, self.movement)

        self.tilemap = Tilemap(self, tile_size=16)
        self.ui = UI(self)

        self.shaking_screen_effect = 0

        self.projectiles = []
        self.animated_projectiles = []
        self.particles = []
        self.sparks = []
        self.munition = []
        self.spells = []
        self.effects = []
        self.damage_rates = []
        self.loot = []
        self.leaf_spawners = []
        self.enemies = []

        self.scroll = [0, 0]
        self.dead = None
        self.transition = None
        self.death_timer = None
        self.artifacts_remaining = None

        self.level = 0
        self.game_over = False
        self.load_level(self.level)

    def clear_lists(self):
        """cleaning the list of objects on the map before loading a new level"""
        lists_to_clear = [
            self.enemies, self.loot,
            self.projectiles, self.animated_projectiles,
            self.particles, self.sparks, self.munition,
            self.spells, self.effects, self.damage_rates
        ]
        for lst in lists_to_clear:
            lst.clear()

    def load_level(self, map_id):
        """downloading the level map and all objects"""
        self.clear_lists()
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        pygame.mixer.music.load(f'data/music/level{str(self.level)}.wav')
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

        # calibrate the volume of sound effects
        volume_adjusting(self.sfx, self.volume_settings)

        # enemy spawn list
        enemy_constructors = {
            1: lambda pos: OrcArcher(self, pos),
            2: lambda pos: BigZombie(self, pos),
            3: lambda pos: BigDaemon(self, pos)
        }

        for spawner in self.tilemap.extract([('spawners', i) for i in range(4)]):
            variant = spawner['variant']
            if variant == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            elif variant in enemy_constructors:
                self.enemies.append(enemy_constructors[variant](spawner['pos']))

        # game loot
        loot_id = {
            0: Gem,
            1: Coin,
            2: HealthPoison,
            3: MagicPoison,
            4: StaminaPoison,
            5: PowerPoison,
            6: SpeedScroll,
            7: BloodlustScroll,
            8: HollyScroll,
            9: InvulnerabilityScroll,
        }

        for item in self.tilemap.extract([('loot_spawn', i) for i in range(10)]):
            loot_class = loot_id.get(item['variant'])
            if loot_class:
                self.loot.append(loot_class(self, item['pos'], (8, 15)))

        self.artifacts_remaining = len([item for item in self.loot if isinstance(item, Gem)])

        # rain effect
        self.raindrops.empty()
        if self.level in rain_on_levels:
            wind_strength = random.randint(1, 4)
            for _ in range(300):
                x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGTH)
                self.raindrops.add(Raindrop(x, y, wind_strength))  # type: ignore

        self.scroll = [0, 0]
        self.dead = False
        self.transition = -30
        self.death_timer = 60

    def handle_projectile_collision(self, projectile):
        self.sfx['arrow_crash'].play()
        for i in range(4):
            self.sparks.append(
                Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0),
                      2 + random.random(), 'white'))

    def handle_player_collision(self, projectile):
        if not self.player.invulnerability:
            self.player.current_health -= 15
            if self.player.current_health > 0:
                self.sfx['pain'].play()
                self.shaking_screen_effect = max(16, self.shaking_screen_effect)
                create_particles(self, self.player.rect(), num_particles=(10, 15))
                center_x = self.ui.heart_image.get_width() / 2
                center_y = self.ui.heart_image.get_height() / 2
                self.effects.append(BloodEffect(self, (center_x, center_y)))

    def run(self):
        """start the main game cycle"""

        # download music and background sound effects
        pygame.mixer.music.load(f'data/music/level{str(self.level)}.wav')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        pygame.mixer.Sound(f'data/ambiance/{str(self.level)}.wav').play(-1)

        def transition_to_next_level():
            self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
            self.player.current_health = self.player.max_health
            self.player.stamina = self.player.max_stamina
            self.player.mana = self.player.max_mana
            self.player.stamina = 100
            self.load_level(self.level)

        def level_restart():
            self.player.current_health = self.player.max_health
            self.player.stamina = self.player.max_stamina
            self.player.life -= 1
            self.player.death_hit = False
            self.load_level(self.level)

        while not self.game_over:

            """It processes all events that occur at a level in the game."""

            self.display.fill((0, 0, 0, 0))
            self.display_2.blit(pygame.transform.scale(self.assets['background'][self.level], self.display_2.get_size()), (0, 0))
            self.shaking_screen_effect = max(0, self.shaking_screen_effect - 1)

            # checking the level completion
            if not self.artifacts_remaining:
                self.transition += 1
                if self.transition > 30:
                    transition_to_next_level()
            if self.transition < 0:
                self.transition += 1

            # restarting level if player has been killed or fall
            if self.dead:
                self.dead += 1
                if self.dead >= 20:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 60:
                    level_restart()

            # screen offset rendering
            offset_y = -75
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += ((self.player.rect().centery + offset_y) - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # updating and rendering clouds
            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)

            # render map
            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.update_animated_tiles()

            # updating state and rendering enemies
            for enemy in self.enemies.copy():
                if not enemy.update(self.tilemap, (0, 0)):
                    enemy.render(self.display, offset=render_scroll)
                else:
                    self.sfx[enemy.e_type].play()
                    self.enemies.remove(enemy)

            # player status update and rendering
            if self.player.current_health <= 0:
                self.player.death_hit = True

            if self.player.life <= 0:
                self.game_over = True
                break

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
                if self.player.death_hit:
                    self.death_timer -= 1
                    if self.death_timer <= 0:
                        self.dead = True

            # processing of conventional projectiles
            for projectile in self.projectiles.copy():
                projectile_pos = (projectile[0][0] - render_scroll[0], projectile[0][1] - render_scroll[1])
                img = self.assets[projectile[-1]]
                flipped_projectile = pygame.transform.flip(img, math.copysign(1, projectile[1]) < 0, False)
                self.display.blit(flipped_projectile, (projectile_pos[0] - flipped_projectile.get_width() / 2,
                                                       projectile_pos[1] - flipped_projectile.get_height() / 2))
                projectile[0][0] += 2 * projectile[1]
                projectile[2] += 1

                # projectile collision with an obstacle
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    self.handle_projectile_collision(projectile)
                elif projectile[2] > 180:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50 and self.player.rect().collidepoint(projectile[0]):
                    self.projectiles.remove(projectile)
                    self.handle_player_collision(projectile)

            # processing animated projectiles
            for projectile in self.animated_projectiles.copy():
                if self.player.rect().colliderect(projectile.rect()):
                    if isinstance(projectile, AnimatedFireball):
                        self.sfx['fire_punch'].play()
                        if not self.player.invulnerability:
                            voice = str(random.randint(1, 3))
                            self.sfx['damaged' + voice].play()
                            self.player.current_health -= 30
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            self.sparks.append(
                                Spark(self.player.rect().center, angle, 2 + random.random(), 'fireball'))
                    elif isinstance(projectile, SkullSmoke):
                        if not self.player.invulnerability:
                            self.sfx['cough'].play(2)
                            self.sfx['corruption'].play()
                            self.player.corruption = True
                            for i in range(50):
                                angle = random.random() * math.pi * 4
                                self.sparks.append(
                                    Spark(self.player.rect().center, angle, 2 + random.random(), 'toxic'))

                    self.animated_projectiles.remove(projectile)

                projectile.update()
                projectile.render(self.display, offset=render_scroll)
                if projectile.update() or projectile.animation.done:
                    self.animated_projectiles.remove(projectile)

            # spark handling
            for spark in self.sparks.copy():
                spark.update()
                spark.render(self.display, offset=render_scroll)
                if spark.update():
                    self.sparks.remove(spark)

            # long-range player's weapon handling
            for slug in self.munition.copy():
                if self.tilemap.solid_check(slug.pos):
                    self.sfx['suriken_rebound'].play()
                    for i in range(4):
                        self.sparks.append(
                            Spark(slug.pos, random.random() - 0.5 + (math.pi if slug.direction > 0 else 0),
                                  2 + random.random(), 'white'))
                    slug.direction *= -1
                    slug.recoil = True

                if self.player.rect().colliderect(slug.rect) and slug.recoil:
                    self.munition.remove(slug)
                    self.player.current_health -= 5
                    self.sfx['pain'].play()
                    for i in range(10):
                        angle = random.random() * math.pi * 2
                        self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))

                kill = slug.update()
                slug.render(self.display, offset=render_scroll)
                if kill:
                    self.munition.remove(slug)

            # magic spells handling
            for spell in self.spells.copy():
                if isinstance(spell, HollySpell):
                    self.player.current_health = 100
                    self.player.stamina = 100
                    self.player.corruption = False
                    self.player.double_power = 2
                    self.sfx['holly_spell'].play()
                if isinstance(spell, SpeedSpell):
                    self.player.super_speed = 2
                    self.sfx['speed_spell'].play()
                if isinstance(spell, BloodlustSpell):
                    self.player.critical_hit_chance = True
                    self.sfx['bloodlust_spell'].play()
                if isinstance(spell, InvulnerabilitySpell):
                    self.player.invulnerability = True
                    self.sfx['invulnerability_spell'].play()

                kill = spell.update()
                spell.render(self.display, offset=render_scroll)
                if kill or spell.animation.done:
                    self.spells.remove(spell)

            # rendering user interface
            self.ui.render()

            # updating and rendering items on map
            for item in self.loot:
                item.update()
                item.render(self.display, offset=render_scroll)

            # updating and rendering VFX
            for effect in self.effects:
                effect.update()
                effect.render(self.display, offset=render_scroll)
                if effect.animation.done:
                    self.effects.remove(effect)

            # updating and rendering damage info
            for damage in self.damage_rates.copy():
                damage.update()
                damage.render(self.display, offset=render_scroll)
                if damage.timer <= 0:
                    self.damage_rates.remove(damage)

            # updating and rendering particles
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if kill:
                    self.particles.remove(particle)

            # updating raindrops
            for raindrop in self.raindrops:
                raindrop.update()
            self.raindrops.draw(self.display)

            #  handling of controller events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player_controller.handle_events(event)

            if self.transition:
                color = color_schema['white']
                trans_mapping = pygame.Surface(self.display.get_size())
                pygame.draw.circle(trans_mapping, color, (DISPLAY_WIDTH // 2, DISPLAY_HEIGTH // 2), (30 - abs(self.transition)) * 8)
                trans_mapping.set_colorkey(color)
                self.display.blit(trans_mapping, (0, 0))

            display_mask = pygame.mask.from_surface(self.display)
            display_outline = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            sse_offset = (random.random() * self.shaking_screen_effect - self.shaking_screen_effect / 2,
                          random.random() * self.shaking_screen_effect - self.shaking_screen_effect / 2)
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_outline, offset)

            self.display_2.blit(self.display, (0, 0))
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), sse_offset)
            pygame.display.update()
            self.clock.tick(60)


class Menu:
    def __init__(self):
        self.screen = screen
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGTH), pygame.SRCALPHA)
        self.background = pygame.image.load('data/images/background/main_menu.png')
        self.background_overlay = pygame.image.load('data/images/background/overlay.png').convert_alpha()
        self.overlay_alpha = 70
        self.alpha_direction = 1
        self.overlay_rotation_angle = 0
        self.overlay_rotation_direction = 1
        self.selected_option = 0
        self.options = ["Start Game", "Options", "Credits", "Exit"]
        self.font = pygame.font.Font(None, 48)
        self.menu_select_sound = pygame.mixer.Sound('data/sfx/menu_select.wav')
        self.menu_confirm_sound = pygame.mixer.Sound('data/sfx/menu_confirm.wav')
        self.menu_music = pygame.mixer.Sound('data/music/menu_music.wav')
        self.menu_music.play(-1)
        self.clock = pygame.time.Clock()
        self.sparks = []

    def update_overlay_alpha(self):
        """changes the transparency of the overlay"""
        self.overlay_alpha += self.alpha_direction * 1
        if self.overlay_alpha <= 0 or self.overlay_alpha >= 155:
            self.alpha_direction *= -1

    def update_overlay_rotation(self):
        """changes the angle of rotation of the overlay"""
        self.overlay_rotation_angle += self.overlay_rotation_direction * 0.01
        if self.overlay_rotation_angle <= -1 or self.overlay_rotation_angle >= 1:
            self.overlay_rotation_direction *= -1

    @staticmethod
    def create_spark():
        """Creates particles with random parameters, size, transparency, and direction of movement."""
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGTH)
        speed_x = random.uniform(-1, 1)
        speed_y = random.uniform(-1, 1)
        size = random.randint(1, 2)
        color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255), random.randint(32, 128))
        return {"x": x, "y": y, "speed_x": speed_x, "speed_y": speed_y, "size": size, "color": color}

    def update_sparks(self):
        """Update the position of the particles."""
        for spark in self.sparks:
            spark["x"] += spark["speed_x"]
            spark["y"] += spark["speed_y"]
            # Handling of particle out of the screen
            if spark["x"] < 0 or spark["x"] > SCREEN_WIDTH or spark["y"] < 0 or spark["y"] > SCREEN_HEIGTH:
                self.sparks.remove(spark)

    def draw_sparks(self):
        """Drawing sparks on screen"""
        for spark in self.sparks:
            color = spark["color"]
            size = spark["size"]
            surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (size, size), size)
            self.screen.blit(surface, (int(spark["x"]) - size, int(spark["y"]) - size))

    def show_loading_screen(self):
        """Game loading screen."""
        loading_font = pygame.font.Font(None, 36)
        loading_text = loading_font.render("Loading ...", True, (255, 255, 255))
        loading_text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGTH // 2))
        progress_bar_width = 300
        progress_bar_height = 20
        progress_bar_rect = pygame.Rect((SCREEN_WIDTH // 2 - progress_bar_width // 2, SCREEN_HEIGTH // 2 + 50,
                                         progress_bar_width, progress_bar_height))

        progress = 0
        while progress <= 100:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(loading_text, loading_text_rect)

            pygame.draw.rect(self.screen, (255, 255, 255), progress_bar_rect, 2)
            pygame.draw.rect(self.screen, (255, 255, 255), (progress_bar_rect.left, progress_bar_rect.top, progress * progress_bar_width // 100, progress_bar_height))

            pygame.display.flip()
            progress += 1
            pygame.time.delay(30)

        main()  # start the game

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            rotated_overlay = pygame.transform.rotate(self.background_overlay, self.overlay_rotation_angle)
            rotated_overlay_rect = rotated_overlay.get_rect(topleft=(- 12, -16))
            rotated_overlay.set_alpha(self.overlay_alpha)
            self.screen.blit(rotated_overlay, rotated_overlay_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                        self.menu_select_sound.play()
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                        self.menu_select_sound.play()
                    elif event.key == pygame.K_SPACE:
                        self.menu_confirm_sound.play()
                        if self.selected_option == 0:
                            # Start Game
                            self.menu_music.stop()
                            self.show_loading_screen()
                        elif self.selected_option == 1:
                            # Options
                            return "options"
                        elif self.selected_option == 2:
                            # Credits
                            return "credits"
                        elif self.selected_option == 3:
                            # Exit
                            pygame.quit()
                            sys.exit()

            for i, option in enumerate(self.options):
                color = (255, 255, 255) if i == self.selected_option else (128, 128, 128)
                menu_option = self.font.render(option, True, color)
                menu = menu_option.get_rect(center=(SCREEN_WIDTH // 2, 400 + i * 50))
                self.screen.blit(menu_option, menu)

            if random.random() < 0.1:  # Simulating the appearance of new particles with a certain probability
                self.sparks.append(self.create_spark())
            self.update_sparks()
            self.draw_sparks()

            # Update overlay transparency and rotation
            self.update_overlay_alpha()
            self.update_overlay_rotation()

            pygame.display.flip()
            self.clock.tick(30)


def main():
    game = Game()
    while not game.game_over:
        game.run()

    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    text = game.ui.font3.render("GAME OVER", True, (255, 255, 255))
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGTH // 2))
    screen.blit(text, rect)
    restart_text = game.ui.font4.render("Press E to restart the game, or Q to quit", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGTH // 2 + 50))
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

    pygame.mixer.music.load(f'data/music/game_over.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()

    while game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    pygame.mixer.music.stop()
                    main()
                elif event.key == pygame.K_q:
                    pygame.mixer.music.stop()
                    Menu().run()


if __name__ == "__main__":
    Menu().run()
