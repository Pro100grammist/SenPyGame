import math

import pygame

from support import BASE_IMG_PATH


import pygame


class UI:
    def __init__(self, game):

        self.game = game
        self.display_height = self.game.display.get_height()
        self.display_width = self.game.display.get_width()

        self.font_ui = pygame.font.Font('data/fonts/MinimalPixelFont.ttf', 14)
        self.font_lvl = pygame.font.Font('data/fonts/Uncial_WIP.ttf', 13)
        self.font = pygame.font.Font('data/fonts/DungeonFont.ttf', 13)
        self.font2 = pygame.font.Font('data/fonts/DungeonFont.ttf', 16)
        self.font3 = pygame.font.Font('data/fonts/Uncial_WIP.ttf', 72)
        self.font4 = pygame.font.Font('data/fonts/Uncial_WIP.ttf', 48)
        self.text_color = (255, 255, 255)

        ui_set = [
            'life_full', 'life_empty', 'heart_full', 'heart_tq', 'heart_half', 'heart_quarter', 'heart_empty',
            'globe_full', 'globe_tq', 'globe_half', 'globe_quarter', 'globe_empty', 'corner_set', 'vignette',
            'diamond_icon', 'panel', 'shuriken_icon', 'player_icon', 'inventory_bar', 'coin_icon',
            'heal_potion_icon', 'mana_potion_icon', 'stamina_potion_icon', 'power_potion_icon', 'inventory_frame',
            'corrupted_icon', 'double_power_icon', 'super_speed_icon', 'bloodlust_icon', 'invulnerability_icon',
            'scroll_slot', 'hud_bg', 'xp_bar'
        ]

        for image in ui_set:
            setattr(self, image, pygame.image.load(BASE_IMG_PATH + f'ui/{image}.png'))

        self.scroll_slot = pygame.image.load(BASE_IMG_PATH + 'ui/scroll_slot.png')
        self.holly_scroll_icon = pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/holly_scroll.png')
        self.speed_scroll_icon = pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/speed_scroll.png')
        self.bloodlust_scroll_icon = pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/bloodlust_scroll.png')
        self.invulnerability_scroll_icon = pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/invulnerability_scroll.png')

        self.status_bar = []
        self.heart_image = self.heart_full
        self.corruption_timer_max = 600
        self.double_power_timer_max = 600
        self.super_speed_timer_max = 720
        self.critical_hit_timer_max = 1200
        self.invulnerability_timer_max = 1000

        self.spellbook = {
            'holly_spell': self.holly_scroll_icon,
            'speed_spell': self.speed_scroll_icon,
            'bloodlust_spell': self.bloodlust_scroll_icon,
            'invulnerability_spell': self.invulnerability_scroll_icon
        }

    def render(self):
        panel_x = 2
        panel_y = self.display_height - self.panel.get_height() - 2
        self.game.display.blit(self.panel, (panel_x, panel_y))

        # health
        heart_images = {
            range(80, 101): self.heart_full,
            range(60, 80): self.heart_tq,
            range(40, 60): self.heart_half,
            range(20, 40): self.heart_quarter,
            range(0, 20): self.heart_empty
        }

        current_health = self.game.player.current_health
        self.heart_image = next((img for rng, img in heart_images.items() if current_health in rng), self.heart_empty)
        self.game.display.blit(pygame.transform.scale(self.heart_image, (self.heart_image.get_width() * 1.2, self.heart_image.get_height() * 1.2)), (22, 16))

        # mana
        self.game.display.blit(self.corner_set, (self.display_width - 87, self.display_height - 115))
        current_mana = self.game.player.mana
        mana_image = self.globe_empty
        mana_x = self.display_width - 82
        mana_y = self.display_height - 82
        mana_images = {
            range(100, 126): self.globe_full,
            range(75, 100): self.globe_tq,
            range(50, 75): self.globe_half,
            range(25, 50): self.globe_quarter,
            range(0, 25): self.globe_empty
        }

        for mana_range, mana_image in mana_images.items():
            if current_mana in mana_range:
                break
        self.game.display.blit(mana_image, (mana_x, mana_y))
        self.game.display.blit(self.vignette, (self.display_width - 98, self.display_height - 96))

        # hud_bg
        self.game.display.blit(self.hud_bg, (10, 10))

        # experience
        xp_x = 62
        xp_y = self.display_height - 20
        self.game.display.blit(self.xp_bar, (xp_x, xp_y))
        xp_line = int(self.game.player.experience / self.game.player.next_level_experience * self.xp_bar.get_width())
        rect = pygame.Rect(xp_x + 2, xp_y + 1, xp_line, 6)
        pygame.draw.rect(self.game.display, (0, 191, 255), rect)

        text = f"{self.game.player.experience} / {self.game.player.next_level_experience}"
        text_render = self.font_ui.render(text, True, (255, 255, 255))
        text_width, text_height = self.font.size(text)
        text_x = xp_x + (self.xp_bar.get_width() - text_width) / 2
        text_y = xp_y + (self.xp_bar.get_height() - text_height) / 2
        self.game.display.blit(text_render, (text_x, text_y))

        # life
        for i in range(6):
            life_heart_x = 50 + i * 15
            life_heart_y = 28
            if i < self.game.player.life:
                self.game.display.blit(self.life_full, (life_heart_x, life_heart_y))
            else:
                self.game.display.blit(self.life_empty, (life_heart_x, life_heart_y))

        # diamonds
        diamond_x = panel_x + 76
        diamond_y = panel_y + 16
        self.game.display.blit(self.diamond_icon, (diamond_x, diamond_y))
        artifacts_text = self.font.render(f" {self.game.artifacts_remaining}", True, (148, 0, 211))
        self.game.display.blit(artifacts_text, (diamond_x + 16, diamond_y + 1))

        # coins
        coins_x = panel_x + 110
        coins_y = panel_y + 16
        self.game.display.blit(self.coin_icon, (coins_x, coins_y))
        coins_count = self.font.render(f" {self.game.player.money}", True, self.text_color)
        self.game.display.blit(coins_count, (coins_x + 16, coins_y + 1))

        # shuriken
        shuriken_count = self.game.player.suriken_count
        shuriken_count_x = panel_x + 142
        shuriken_count_y = panel_y + 16
        self.game.display.blit(self.shuriken_icon, (shuriken_count_x, shuriken_count_y))
        shuriken_remaining = self.font.render(f" {shuriken_count}", True, (176, 196, 222))
        self.game.display.blit(shuriken_remaining, (shuriken_count_x + 16, shuriken_count_y + 1))

        # stamina
        st_x = 54
        st_y = 24
        intensity = int(255 * (self.game.player.stamina / 100))
        stamina_color = (0, intensity, 0)
        stamina_rect = pygame.Rect(st_x, st_y, self.game.player.stamina * 0.8, 3)
        pygame.draw.rect(self.game.display, stamina_color, stamina_rect)

        for i in range(stamina_rect.width):
            gradient_intensity = int(255 * (i / stamina_rect.width))
            gradient_color = (0, gradient_intensity, 0)
            pygame.draw.line(self.game.display, gradient_color, (st_x + i, st_y),
                             (st_x + i, st_y + stamina_rect.height), 0)

        # hero icon
        hero_icon_x = panel_x + 6
        hero_icon_y = panel_y + 14
        self.game.display.blit(self.player_icon, (hero_icon_x, hero_icon_y))

        # player_level
        player_level = f" Level {self.game.player.level}"
        level_render = self.font_lvl.render(player_level, True, (255, 255, 255))
        self.game.display.blit(level_render, (8, 420))

        # inventory
        inventory_x = panel_x + 260
        inventory_y = panel_y + 10
        self.game.display.blit(self.inventory_bar, (inventory_x, inventory_y))

        # potions
        x, y = inventory_x + 10, inventory_y + 10
        icon_offset = 36

        potions = [
            (self.heal_potion_icon, self.game.player.heal_potions),
            (self.mana_potion_icon, self.game.player.magic_potions),
            (self.stamina_potion_icon, self.game.player.stamina_potions),
            (self.power_potion_icon, self.game.player.power_potions)
        ]

        for potion_icon, potion_count in potions:
            if potion_count > 0:
                self.game.display.blit(potion_icon, (x, y))
                potion_count_text = self.font.render(f" {potion_count}", True, self.text_color)
                self.game.display.blit(potion_count_text, (x + 16, y + 16))
            x += icon_offset

        # frame
        frame_positions = [x - 147 + i * 36 for i in range(5)]
        active_frame = self.game.player.selected_item
        if 1 <= active_frame <= len(frame_positions):
            self.game.display.blit(self.inventory_frame, (frame_positions[active_frame - 1], y - 9))

        # scrolls
        self.game.display.blit(self.scroll_slot, (self.display_width - 80, 2))
        active_scroll = self.game.player.selected_scroll
        scrolls = sorted(list({(key, value) for key, value in self.game.player.scrolls.items() if value > 0}))
        if scrolls:
            x = self.display_width - 74
            y = 10
            scroll = self.spellbook[scrolls[active_scroll][0]]
            count = scrolls[active_scroll][1]
            self.game.display.blit(scroll, (x, y))
            scroll_count = self.font2.render(f" {count}", True, self.text_color)
            self.game.display.blit(scroll_count, (x + 44, y + 46))

        # status
        status_updates = [
            (self.corrupted_icon, 'corruption', self.game.player.corruption),
            (self.double_power_icon, 'double_power', self.game.player.double_power == 2),
            (self.super_speed_icon, 'super_speed', self.game.player.super_speed == 2),
            (self.bloodlust_icon, 'critical_hit', self.game.player.critical_hit_chance),
            (self.invulnerability_icon, 'invulnerability', self.game.player.invulnerability)
        ]

        for icon, status, condition in status_updates:
            if condition and (icon, status) not in self.status_bar:
                self.status_bar.append((icon, status))
            elif not condition and (icon, status) in self.status_bar:
                self.status_bar.remove((icon, status))

        timer_attributes = {
            'double_power': ('power_potion_timer', 'double_power_timer_max'),
            'corruption': ('corruption_timer', 'corruption_timer_max'),
            'super_speed': ('super_speed_timer', 'super_speed_timer_max'),
            'critical_hit': ('critical_hit_timer', 'critical_hit_timer_max'),
            'invulnerability': ('invulnerability_timer', 'invulnerability_timer_max')
        }

        for pos, (icon, status) in enumerate(self.status_bar):
            x = panel_x + 50 + 22 * pos
            y = panel_y - 12
            color = (255, 255, 255)

            if status in timer_attributes:
                timer_attribute, timer_max_attribute = timer_attributes[status]
                left_time = getattr(self.game.player, timer_attribute)
                elapsed_time = getattr(self, timer_max_attribute) - left_time
                transparency = 255 - min(255, int(255 * (elapsed_time / getattr(self, timer_max_attribute))))
                icon.set_alpha(transparency)
                self.game.display.blit(icon, (x, y))
                timer_text = self.font.render(f"{left_time // 60}", True, color)
                timer_text.set_alpha(transparency)
                self.game.display.blit(timer_text, (x + icon.get_width() // 2, y + 12))


class Skill:
    def __init__(self, name, image_path, coordinates, description, required_experience):
        self.name = name
        self.image_path = image_path
        self.coordinates = coordinates
        self.description = description
        self.required_experience = required_experience
        self.opened = False


class SkillsTree:
    def __init__(self, game):
        self.game = game
        self.skill_tree_base = pygame.image.load(BASE_IMG_PATH + 'ui/skills/skills_tree.png')
        self.skills = self.create_skills()

    @staticmethod
    def create_skills():
        """
        This method create 16 character skills that player can open during the game using experience points.

        :return: list of Skill objects that include next skills ("Vitality Boost", "Endurance Mastery",
        "Resilience Training", "Health Regeneration", "Power Strike", "Berserker Rage", "Weapon Mastery",
        "Brute Force", "Agile Reflexes", "Acrobatic Moves", "Stealth Tactics", "Precision Strikes",
        "Arcane Knowledge", "Elemental Affinity", "Sorcery Mastery", "Time Manipulation"
        """
        skills = []

        # Skill 1: Vitality Boost
        vitality_boost = Skill(
            name="Vitality Boost",
            image_path=BASE_IMG_PATH + 'ui/skills/vitality_boost.png',
            coordinates=(50, 50),
            description="Increases health points",
            required_experience=1
        )
        skills.append(vitality_boost)

        # Skill 2: Endurance Mastery
        endurance_mastery = Skill(
            name="Endurance Mastery",
            image_path=BASE_IMG_PATH + 'ui/skills/endurance_mastery.png',
            coordinates=(50, 150),
            description="Improves endurance",
            required_experience=2
        )
        skills.append(endurance_mastery)

        return skills

    def render(self):
        x = 172
        y = 0
        self.game.display.blit(self.skill_tree_base, (x, y))
        for skill in self.skills:
            if skill.opened:
                self.game.display.blit(pygame.image.load(skill.image_path), skill.coordinates)

    def open_skill(self, skill):
        if not skill.opened and self.game.player.experience_points >= skill.required_experience:
            skill.opened = True
            self.game.player.experience_points -= skill.required_experience
