import math

import pygame

from support import BASE_IMG_PATH
from items import Equipment, Book
from data import POTIONS, SCROLLS, MERCHANT_ITEM_POS, UI_PATH


class UI:
    """
    Class UI represents user interface on display in game.
    That include: heart - shows the player's health level,
                  mana globe - shows the level of player's mana,
                  life hearts - shows how many player's life left,
                  green bar - shows the player's stamina level,
                  inventory blue panel - display player's potions,
                  scrolls - display active magic scroll,
                  player panel - shows experience points and level, gems, coins, projectile and active buffs.
    """
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

        health = int((self.game.player.current_health / self.game.player.max_health) * 100)
        self.heart_image = next((img for rng, img in heart_images.items() if health in rng), self.heart_empty)
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
        shuriken_count_x = panel_x + 162
        shuriken_count_y = panel_y + 16
        self.game.display.blit(self.shuriken_icon, (shuriken_count_x, shuriken_count_y))
        shuriken_remaining = self.font.render(f" {shuriken_count}", True, (176, 196, 222))
        self.game.display.blit(shuriken_remaining, (shuriken_count_x + 16, shuriken_count_y + 1))

        # stamina
        st_x = 54
        st_y = 24
        intensity = min(int(255 * (self.game.player.stamina / self.game.player.max_stamina)), 255)
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
    """
    A class representing the character's skill.
    """
    def __init__(self, name, image_path, coordinates, description, required_experience, level, accessibility):
        self.name = name
        self.image_path = image_path
        self.coordinates = coordinates
        self.description = description
        self.required_experience = required_experience
        self.accessibility = accessibility
        self.level = level
        self.opened = False


class SkillsTree:
    """
    A class representing the character's skills menu (skill tree).
    """
    def __init__(self, game):
        self.game = game
        origin_img = pygame.image.load(BASE_IMG_PATH + 'ui/skills/skills_tree.png')
        self.skill_tree_base = pygame.transform.scale(origin_img, (origin_img.get_width() // 2, origin_img.get_height() // 2))
        self.skills_frame = pygame.image.load(BASE_IMG_PATH + 'ui/skills/skills_frame.png')
        self.font_tree = pygame.font.Font('data/fonts/DungeonFont.ttf', 16)
        self.font_skill = pygame.font.Font('data/fonts/Charmonman-Regular.ttf', 16)
        self.skills = self.create_skills()
        self.selected_row = 0
        self.selected_col = 0

        self.grid = [
            ['s', 's', 's', 'e'],
            ['s', 's', 'e', 's'],
            ['e', 's', 's', 's'],
            ['s', 's', 's', 'e'],
            ['s', 'e', 's', 'e'],
            ['e', 's', 'e', 'e'],
        ]
        self.skill_id = {
            (0, 0): "Healing Mastery",
            (0, 1): "Sorcery Mastery",
            (0, 2): "Steel Skin",
            (1, 0): "Vitality Infusion",
            (1, 1): "Enchanter's Blessing",
            (1, 3): "Endurance Mastery",
            (2, 1): "Inscription Mastery",
            (2, 2): "Weapon Mastery",
            (2, 3): "Hawk's Eye",
            (3, 0): "Poison Resistance",
            (3, 1): "Rapid Recovery",
            (3, 2): "Ruthless Strike",
            (4, 0): "Absorption",
            (4, 2): "Berserker Rage",
            (5, 1): "Resurrection"
        }

    @staticmethod
    def create_skills():
        """
        This method create 16 character skills that player can open during the game using experience points.

        :return: list of Skill objects that include next 4 types of skills
        "Healing Mastery", "Vitality Infusion", "Poison Resistance", "Absorption",
        "Endurance Mastery", "Hawk's Eye", "Swift Reflexes", "Rapid Recovery",
        "Ruthless Strike", "Weapon Mastery", "Steel Skin", "Berserker Rage",
        "Sorcery Mastery", "Enchanter's Blessing", "Inscription Mastery", "Time Manipulation",
        """
        skills = []

        # Skill 1: Healing Mastery
        healing_mastery = Skill(
            name="Healing Mastery",
            image_path=BASE_IMG_PATH + 'ui/skills/healing_mastery.png',
            coordinates=(217, 76),
            description="Doubles the effect of using a healing potion",
            required_experience=1,
            level=1,
            accessibility=None
        )
        skills.append(healing_mastery)

        # Skill 2: Vitality Infusion
        vitality_infusion = Skill(
            name="Vitality Infusion",
            image_path=BASE_IMG_PATH + 'ui/skills/vitality_infusion.png',
            coordinates=(217, 124),
            description="Up max hp points with each lvl and gives a chance to regain hp from the damage if hp<30%.",
            required_experience=2,
            level=2,
            accessibility="Healing Mastery"
        )
        skills.append(vitality_infusion)

        # Skill 3: Poison Resistance
        poison_resistance = Skill(
            name="Poison Resistance",
            image_path=BASE_IMG_PATH + 'ui/skills/poison_resistance.png',
            coordinates=(218, 227),
            description="Grants immunity to poison effects",
            required_experience=4,
            level=4,
            accessibility="Vitality Infusion"
        )
        skills.append(poison_resistance)

        # Skill 4: Absorption
        absorption = Skill(
            name="Absorption",
            image_path=BASE_IMG_PATH + 'ui/skills/absorption.png',
            coordinates=(218, 283),
            description="Absorbs enemy energy and converts it into player's health.",
            required_experience=4,
            level=5,
            accessibility="Rapid Recovery"
        )
        skills.append(absorption)

        # Skill 5: Endurance Mastery
        endurance_mastery = Skill(
            name="Endurance Mastery",
            image_path=BASE_IMG_PATH + 'ui/skills/endurance_mastery.png',
            coordinates=(392, 124),
            description="Increases maximum stamina and reduces stamina consumption.",
            required_experience=2,
            level=2,
            accessibility="Hawk's Eye"
        )
        skills.append(endurance_mastery)

        # Skill 6: Hawk's Eye
        hawks_eye = Skill(
            name="Hawk's Eye",
            image_path=BASE_IMG_PATH + 'ui/skills/hawks_eye.png',
            coordinates=(392, 176),
            description="Enhances critical hit chance with ranged weapons.",
            required_experience=3,
            level=3,
            accessibility="Weapon Mastery"
        )
        skills.append(hawks_eye)

        # Skill 7: Swift Reflexes (This skill not implemented yet, but I think about how to find solution)
        swift_reflexes = Skill(
            name="Swift Reflexes",
            image_path=BASE_IMG_PATH + 'ui/skills/swift_reflexes.png',
            coordinates=(392, 76),
            description="Improves dodge ability, giving you a chance to avoid being hit by an enemy.",
            required_experience=1,
            level=1,
            accessibility=None
        )
        skills.append(swift_reflexes)

        # Skill 8: Rapid Recovery
        rapid_recovery = Skill(
            name="Rapid Recovery",
            image_path=BASE_IMG_PATH + 'ui/skills/rapid_recovery.png',
            coordinates=(277, 227),
            description="Increases the speed of stamina regeneration after combat.",
            required_experience=4,
            level=4,
            accessibility="Ruthless Strike"
        )
        skills.append(rapid_recovery)

        # Skill 9: Ruthless Strike
        ruthless_strike = Skill(
            name="Ruthless Strike",
            image_path=BASE_IMG_PATH + 'ui/skills/ruthless_strike.png',
            coordinates=(333, 227),
            description="Increases the chance to deal a powerful & merciless strike, ignoring enemy's armor.",
            required_experience=4,
            level=4,
            accessibility="Weapon Mastery"
        )
        skills.append(ruthless_strike)

        # Skill 10: Weapon Mastery
        weapon_mastery = Skill(
            name="Weapon Mastery",
            image_path=BASE_IMG_PATH + 'ui/skills/weapon_mastery.png',
            coordinates=(333, 176),
            description="Improves melee weapon skills, increasing damage and attack speed.",
            required_experience=3,
            level=3,
            accessibility=("Steel Skin", "Inscription Mastery")
        )
        skills.append(weapon_mastery)

        # Skill 11: Steel Skin
        steel_skin = Skill(
            name="Steel Skin",
            image_path=BASE_IMG_PATH + 'ui/skills/steel_skin.png',
            coordinates=(333, 76),
            description="Hardens the skin, reducing damage taken.",
            required_experience=1,
            level=1,
            accessibility=None
        )
        skills.append(steel_skin)

        # Skill 12: Berserker Rage
        berserker_rage = Skill(
            name="Berserker Rage",
            image_path=BASE_IMG_PATH + 'ui/skills/berserker_rage.png',
            coordinates=(333, 283),
            description="When 💔 drops below 25%, the hero frenzied rage, increasing the damage inflicted on enemies.",
            required_experience=5,
            level=5,
            accessibility="Ruthless Strike"
        )
        skills.append(berserker_rage)

        # Skill 13: Sorcery Mastery
        sorcery_mastery = Skill(
            name="Sorcery Mastery",
            image_path=BASE_IMG_PATH + 'ui/skills/sorcery_mastery.png',
            coordinates=(277, 76),
            description="Enhances magical abilities and reduces spell casting costs.",
            required_experience=1,
            level=1,
            accessibility=None
        )
        skills.append(sorcery_mastery)

        # Skill 14: Enchanter's Blessing
        enchanters_blessing = Skill(
            name="Enchanter's Blessing",
            image_path=BASE_IMG_PATH + 'ui/skills/enchanters_blessing.png',
            coordinates=(277, 124),
            description="Blessing increases the power and effectiveness of spells.",
            required_experience=2,
            level=2,
            accessibility="Sorcery Mastery"
        )
        skills.append(enchanters_blessing)

        # Skill 15: Inscription Mastery
        inscription_mastery = Skill(
            name="Inscription Mastery",
            image_path=BASE_IMG_PATH + 'ui/skills/inscription_mastery.png',
            coordinates=(277, 176),
            description="Gives you a chance to save a scroll with a spell while using it.",
            required_experience=3,
            level=3,
            accessibility="Enchanter's Blessing"
        )
        skills.append(inscription_mastery)

        # Skill 16: Resurrection
        resurrection = Skill(
            name="Resurrection",
            image_path=BASE_IMG_PATH + 'ui/skills/time_manipulation.png',
            coordinates=(278, 333),
            description="It gives a chance to revive in case of the hero's death.",
            required_experience=6,
            level=6,
            accessibility="Rapid Recovery"
        )
        skills.append(resurrection)

        return skills

    def move_cursor(self, direction):
        if direction == "up":
            self.selected_row -= 1
        elif direction == "down":
            self.selected_row += 1
        elif direction == "left":
            self.selected_col -= 1
        elif direction == "right":
            self.selected_col += 1

        self.selected_row %= len(self.grid)
        self.selected_col %= len(self.grid[0])

        while self.grid[self.selected_row][self.selected_col] == 'e':
            self.move_cursor(direction)

        self.game.sfx['move_cursor'].play()

    def open_skill(self):
        """Open character's skill if this skill available now"""
        skill = self.get_current_skill()

        if not skill.opened and self.game.player.experience_points >= skill.required_experience:
            if skill.name in ("Healing Mastery", "Sorcery Mastery", "Steel Skin"):
                skill.opened = True
                self.game.player.experience_points -= skill.required_experience
                self.game.player.skills[skill.name] = True
                self.game.sfx['open_skill'].play()
            elif skill.name == "Weapon Mastery":
                if self.game.player.skills[skill.accessibility[0]] or self.game.player.skills[skill.accessibility[1]]:
                    skill.opened = True
                    self.game.player.experience_points -= skill.required_experience
                    self.game.player.skills[skill.name] = True
                    self.game.sfx['open_skill'].play()
            else:
                if self.game.player.skills[skill.accessibility]:
                    skill.opened = True
                    self.game.player.experience_points -= skill.required_experience
                    self.game.player.skills[skill.name] = True
                    self.game.sfx['open_skill'].play()
        else:
            self.game.sfx['rejected'].play()

    def get_current_skill(self):
        """Get the current skill that the cursor is pointing to."""
        changed_skill = self.skill_id[(self.selected_row, self.selected_col)]
        return next((s for s in self.skills if s.name == changed_skill), None)

    @staticmethod
    def wrap_text(text, max_line_length):
        """
        Splitting the text into lines with a specified maximum length
        so that the description does not go beyond the skill board.
        """
        words = text.split()
        lines = []
        current_line = ''
        for word in words:
            if len(current_line) + len(word) < max_line_length:
                current_line += ' ' + word
            else:
                lines.append(current_line.strip())
                current_line = word
        if current_line:
            lines.append(current_line.strip())
        return lines

    def render_skill_description(self, current_skill, x, y):
        """Displaying the skill description on the screen"""
        if current_skill is not None:
            description_lines = self.wrap_text(current_skill.description, 44)
            y_offset = 0
            for line in description_lines:
                description_render = self.font_tree.render(line, True, (255, 255, 255))
                self.game.display.blit(description_render, (x + 14, y + 376 + y_offset))
                y_offset += self.font_tree.get_height() - 3

    def render(self):
        """Displaying the skill menu"""
        x = 172
        y = 0

        self.game.display.blit(self.skill_tree_base, (x, y))

        for skill in self.skills:
            if skill.opened:
                self.game.display.blit(pygame.image.load(skill.image_path), skill.coordinates)

        # Positions of skill icons on the skill tree board.
        frame_pos = {(0, 0): (x + 39, y + 68), (0, 1): (x + 98, y + 68), (0, 2): (x + 155, y + 68),
                     (1, 0): (x + 39, y + 117), (1, 1): (x + 98, y + 117), (1, 3): (x + 214, y + 117),
                     (2, 1): (x + 98, y + 168), (2, 2): (x + 155, y + 168), (2, 3): (x + 214, y + 168),
                     (3, 0): (x + 39, y + 220), (3, 1): (x + 98, y + 220), (3, 2): (x + 155, y + 220),
                     (4, 0): (x + 39, y + 276), (4, 2): (x + 155, y + 276), (5, 1): (x + 99, y + 326)}

        # Displaying the cursor
        current_frame_pos = frame_pos[(self.selected_row, self.selected_col)]
        self.game.display.blit(self.skills_frame, current_frame_pos)

        # Get the current skill and display its description
        self.render_skill_description(self.get_current_skill(), x, y)

        # Display the name of the current skill
        skill_name_render = self.font_skill.render(self.get_current_skill().name, True, (255, 255, 255))
        self.game.display.blit(skill_name_render, (x + 14, y + 26))


class CharacterMenu:
    """
    The class represents the character's equipment and
    stats (health, mana, stamina, level of vitality, agility, wisdom, defense and damage).
    """

    def __init__(self, game):
        self.game = game
        self.character_menu = pygame.image.load(BASE_IMG_PATH + 'ui/character/character_menu.png')
        self.info_window = pygame.image.load(BASE_IMG_PATH + 'ui/character/info_window.png')
        self.cursor = pygame.image.load(BASE_IMG_PATH + 'ui/character/cursor.png')
        self.flip_cursor = pygame.image.load(BASE_IMG_PATH + 'ui/character/cursor_flip.png')
        self.font_menu = pygame.font.Font('data/fonts/DungeonFont.ttf', 16)
        self.current_cell = None
        self.selected_row = 0
        self.selected_col = 0

        self.grid = [
            ['c', 'c', 'c'],
            ['c', 'e', 'c'],
            ['c', 'e', 'c'],
            ['c', 'c', 'c'],
        ]
        self.item_id = {
            "body_armor": (0, 0),
            "head_protection": (0, 1),
            "amulet": (0, 2),
            "belt": (1, 0),
            "ring": (1, 2),
            "pants": (2, 0),
            "gloves": (2, 2),
            "melee": (3, 0),
            "boots": (3, 1),
            "long_rage_weapon": (3, 2)
        }

    def move_cursor(self, direction):
        if direction == "up":
            self.selected_row -= 1
        elif direction == "down":
            self.selected_row += 1
        elif direction == "left":
            self.selected_col -= 1
        elif direction == "right":
            self.selected_col += 1

        self.selected_row %= len(self.grid)
        self.selected_col %= len(self.grid[0])

        while self.grid[self.selected_row][self.selected_col] == 'e':
            self.move_cursor(direction)

        self.game.sfx['move_cursor'].play()

    def render(self):
        # board
        x = 200
        y = 150
        self.game.display.blit(self.character_menu, (x, y))

        # Personage attributes rendering
        attributes = {
            "hp": (self.game.player.current_health, self.game.player.max_health, (x + 250, y + 48)),
            "mp": (self.game.player.mana, self.game.player.max_mana, (x + 250, y + 70)),
            "st": (int(self.game.player.stamina), self.game.player.max_stamina, (x + 250, y + 92)),
            "lf": (self.game.player.vitality, None, (x + 272, y + 114)),
            "dmg": (self.game.player.strength, None, (x + 272, y + 136)),
            "def": (self.game.player.defence, None, (x + 272, y + 158)),
            "wis": (self.game.player.wisdom, None, (x + 272, y + 180)),
            "dex": (self.game.player.agile, None, (x + 272, y + 202))
        }

        for attr, (value, max_value, pos) in attributes.items():
            if max_value:
                value_str = f"{value} / {max_value}"
            else:
                value_str = str(value)
            value_render = self.font_menu.render(value_str, True, (255, 255, 255))
            self.game.display.blit(value_render, pos)

        # Name and class of character and level
        text = f"Name [{self.game.player.name}] | Battle class [{self.game.player.class_name}] | Level [{self.game.player.level}]"
        text_render = self.font_menu.render(text, True, (255, 255, 255))
        self.game.display.blit(text_render, (x + 8, y + 4))

        # equipments
        eq_pos = {
            (0, 0): (x + 16, y + 50), (0, 1): (x + 70, y + 34), (0, 2): (x + 126, y + 52),
            (1, 0): (x + 16, y + 88), (1, 2): (x + 124, y + 88),
            (2, 0): (x + 16, y + 124), (2, 2): (x + 124, y + 124),
            (3, 0): (x + 18, y + 166), (3, 1): (x + 70, y + 170), (3, 2): (x + 120, y + 164)
        }

        for key, value in self.game.player.equipment.items():
            self.game.display.blit(pygame.image.load(value.pic), eq_pos[self.item_id.get(key)])

        # Cursor rendering
        cursor_pos = {
            (0, 0): (x + 40, y + 52), (0, 1): (x + 45, y + 34), (0, 2): (x + 100, y + 52),
            (1, 0): (x + 40, y + 92), (1, 2): (x + 100, y + 92),
            (2, 0): (x + 40, y + 124), (2, 2): (x + 100, y + 124),
            (3, 0): (x + 44, y + 170), (3, 1): (x + 45, y + 170), (3, 2): (x + 96, y + 170)
        }

        current_cursor_pos = cursor_pos[(self.selected_row, self.selected_col)]
        if current_cursor_pos[0] < 245:
            self.game.display.blit(self.cursor, current_cursor_pos)
        elif current_cursor_pos[0] > 241:
            self.game.display.blit(self.flip_cursor, current_cursor_pos)

        # Current equipment rendering
        for key, value in self.item_id.items():
            if value == (self.selected_row, self.selected_col):
                self.current_cell = key
                break

        current_equipment = self.game.player.equipment.get(self.current_cell)
        if current_equipment:
            self.game.display.blit(self.info_window, (x - self.info_window.get_width(), y))

            name_render = self.font_menu.render(current_equipment.name, True, (255, 255, 255))
            eq_class = f"Class         {current_equipment.rarity}"
            rarity_render = self.font_menu.render(eq_class, True, (255, 255, 255))

            render_list = [name_render, rarity_render]

            if current_equipment.increase_defence > 0:
                defence = f"Defence         + {current_equipment.increase_defence}"
                defence_render = self.font_menu.render(defence, True, (255, 255, 255))
                render_list.append(defence_render)
            if current_equipment.increase_damage > 0:
                damage = f"Damage         + {current_equipment.increase_damage}"
                damage_render = self.font_menu.render(damage, True, (255, 255, 255))
                render_list.append(damage_render)
            if current_equipment.distance_damage > 0:
                d_damage = f"Damage         + {current_equipment.distance_damage}"
                d_damage_render = self.font_menu.render(d_damage, True, (255, 255, 255))
                render_list.append(d_damage_render)
            if current_equipment.increase_health > 0:
                health = f"Health          + {current_equipment.increase_health}"
                health_render = self.font_menu.render(health, True, (255, 255, 255))
                render_list.append(health_render)
            if current_equipment.increase_stamina > 0:
                stamina = f"Stamina         + {current_equipment.increase_stamina}"
                stamina_render = self.font_menu.render(stamina, True, (255, 255, 255))
                render_list.append(stamina_render)
            if current_equipment.increase_mana > 0:
                mana = f"Mana           + {current_equipment.increase_mana}"
                mana_render = self.font_menu.render(mana, True, (255, 255, 255))
                render_list.append(mana_render)
            if current_equipment.increase_experience > 0:
                experience = f"Experience     + {current_equipment.increase_experience} %"
                experience_render = self.font_menu.render(experience, True, (255, 255, 255))
                render_list.append(experience_render)
            if current_equipment.price > 0:
                price = f"Price        {current_equipment.price} Gold"
                price_render = self.font_menu.render(price, True, (255, 255, 255))
                render_list.append(price_render)

            # condition = self.font_menu.render(current_equipment.condition, True, (255, 255, 255))

            y_offset = 2
            for i in render_list:
                self.game.display.blit(i, (x - self.info_window.get_width() + 10, y + y_offset))
                y_offset += 18


class InventoryMenu:
    """
     The class represents the character's inventory backpack.
    """
    def __init__(self, game):
        """
        Initializes the InventoryMenu class.

        Parameters:
            game (object): The game object.

        Attributes:
            game (object): The game object.
            inventory_menu (pygame.Surface): The image representing the inventory window.
            frame (pygame.Surface): The image representing the inventory window frame.
            font (pygame.font.Font): The font used for rendering text.
            selected_row (int): The currently selected row index.
            selected_col (int): The currently selected column index.
            grid (list): A 2D list representing the inventory grid.
            current_cell (list): The currently selected cell coordinates.
        """
        self.game = game
        self.inventory_menu = pygame.image.load(BASE_IMG_PATH + 'ui/inventory/inventory_window.png')
        self.frame = pygame.image.load(BASE_IMG_PATH + 'ui/inventory/inventory_window_frame.png')
        self.font = pygame.font.Font('data/fonts/MainFont.ttf', 12)
        self.selected_row = 0
        self.selected_col = 0
        self.grid = [[None] * 6 for _ in range(5)]
        self.current_cell = [self.selected_row, self.selected_col]

    def move_cursor(self, direction):
        """
        Moves the cursor in the specified direction.

        Parameters: direction (str): The direction to move the cursor ('up', 'down', 'left', 'right').
        """
        if direction == "up":
            self.selected_row -= 1
        elif direction == "down":
            self.selected_row += 1
        elif direction == "left":
            self.selected_col -= 1
        elif direction == "right":
            self.selected_col += 1

        self.selected_row %= len(self.grid)
        self.selected_col %= len(self.grid[0])
        self.current_cell = [self.selected_row, self.selected_col]

        self.game.sfx['move_cursor'].play()

    def apply(self):
        """
        Applies the selected item.

        Current method is responsible for applying (putting on) equipment by moving the selected item
        on the character
        """
        item = self.grid[self.current_cell[0]][self.current_cell[1]]
        if item:
            if isinstance(item, Equipment):
                if item.e_type not in self.game.player.equipment:
                    self.game.player.equipment[item.e_type] = item
                    self.grid[self.current_cell[0]][self.current_cell[1]] = None
                    self.game.player.inventory.remove(item)

                else:
                    deactivated_equipment = self.game.player.equipment[item.e_type]
                    self.game.player.refreshing_player_status(deactivated_equipment, -1)
                    self.game.player.equipment[item.e_type] = item
                    self.grid[self.current_cell[0]][self.current_cell[1]] = deactivated_equipment
                    replaced_item_index = self.game.player.inventory.index(item)
                    self.game.player.inventory[replaced_item_index] = deactivated_equipment

                self.game.player.refreshing_player_status(item)

            if isinstance(item, Book):
                item.read()
                self.game.player.inventory.remove(item)

            self.refresh_inventory()
            self.game.sfx['item_equip'].play()

    def refresh_inventory(self):
        """
        Updates the inventory grid.

        This method synchronizes the 2D grid (self.grid) with the player's inventory self.game.player.inventory.
        It is called whenever a new item is added to the inventory.
        """
        for i in range(5):
            for j in range(6):
                item_index = i * 6 + j
                if item_index < len(self.game.player.inventory):
                    self.grid[i][j] = self.game.player.inventory[item_index]

    def render(self):
        # board
        x = 32
        y = 32
        self.game.display.blit(self.inventory_menu, (x, y))

        # Displaying items in inventory cells
        item_pos = {(i, j): (x + 195 + j * 45, y + 68 + i * 44) for i in range(5) for j in range(6)}
        for i in range(5):
            for j in range(6):
                item = self.game.player.inventory[i * 6 + j] if i * 6 + j < len(self.game.player.inventory) else None
                if item:
                    item_image = pygame.image.load(item.pic)
                    item_rect = item_image.get_rect()
                    item_rect.topleft = item_pos[(i, j)]
                    self.game.display.blit(item_image, item_rect)

        # Displaying the cursor
        frame_pos = {(i, j): (x + 191 + j * 45, y + 62 + i * 43.5) for i in range(5) for j in range(6)}
        current_frame_pos = frame_pos[(self.selected_row, self.selected_col)]
        self.game.display.blit(self.frame, current_frame_pos)

        # Current equipment rendering
        current_equipment = self.grid[self.selected_row][self.selected_col]
        if current_equipment:
            if isinstance(current_equipment, Equipment):

                name_render = self.font.render(current_equipment.name, True, (255, 255, 255))
                eq_class = f"Class         {current_equipment.rarity}"
                rarity_render = self.font.render(eq_class, True, (255, 255, 255))

                render_list = [name_render, rarity_render]

                if current_equipment.increase_defence > 0:
                    defence = f"Defence         + {current_equipment.increase_defence}"
                    defence_render = self.font.render(defence, True, (255, 255, 255))
                    render_list.append(defence_render)
                if current_equipment.increase_damage > 0:
                    damage = f"Damage         + {current_equipment.increase_damage}"
                    damage_render = self.font.render(damage, True, (255, 255, 255))
                    render_list.append(damage_render)
                if current_equipment.distance_damage > 0:
                    d_damage = f"Damage         + {current_equipment.distance_damage}"
                    d_damage_render = self.font.render(d_damage, True, (255, 255, 255))
                    render_list.append(d_damage_render)
                if current_equipment.increase_health > 0:
                    health = f"Health           + {current_equipment.increase_health}"
                    health_render = self.font.render(health, True, (255, 255, 255))
                    render_list.append(health_render)
                if current_equipment.increase_stamina > 0:
                    stamina = f"Stamina         + {current_equipment.increase_stamina}"
                    stamina_render = self.font.render(stamina, True, (255, 255, 255))
                    render_list.append(stamina_render)
                if current_equipment.increase_mana > 0:
                    mana = f"Mana           + {current_equipment.increase_mana}"
                    mana_render = self.font.render(mana, True, (255, 255, 255))
                    render_list.append(mana_render)
                if current_equipment.increase_experience > 0:
                    experience = f"Experience     + {current_equipment.increase_experience} %"
                    experience_render = self.font.render(experience, True, (255, 255, 255))
                    render_list.append(experience_render)
                if current_equipment.price > 0:
                    price = f"Price            {current_equipment.price}"
                    price_render = self.font.render(price, True, (255, 255, 255))
                    render_list.append(price_render)
                if current_equipment.condition:
                    condition = f"Condition        {current_equipment.condition}"
                    condition_render = self.font.render(condition, True, (255, 255, 255))
                    render_list.append(condition_render)

                y_offset = 2
                for i in render_list:
                    self.game.display.blit(i, (x + 42, y + 84 + y_offset))
                    y_offset += 18

            elif isinstance(current_equipment, Book):
                pass

        # Magic scrolls rendering
        x_offset = 92
        for scroll in self.game.player.scrolls.items():
            scroll_image = self.game.ui.spellbook.get(scroll[0])
            scroll_image = pygame.transform.scale(scroll_image,
                                                  (scroll_image.get_width() * 0.65, scroll_image.get_height() * 0.65))
            scroll_amount = scroll[1]
            self.game.display.blit(scroll_image, (x + x_offset, y + 328))
            x_offset += 44


class MerchantWindow:
    """
    The class represents the merchant's trading window
    """

    def __init__(self, game):
        """

        :param game:
        """
        self.game = game
        self.goods_stand = UI_PATH.get('goods_stand')
        self.details_desk = UI_PATH.get('details_desk')
        self.frame = UI_PATH.get('frame')
        self.font = pygame.font.Font('data/fonts/MainFont.ttf', 16)
        self.font_title = pygame.font.Font('data/fonts/MainFont.ttf', 20)
        self.selected_row = 0
        self.selected_col = 0
        self.stuff = []
        self.view_details = False
        self.current_item = None
        self.item_positions = MERCHANT_ITEM_POS

    def move_cursor(self, direction):
        """
        Moves the cursor in the specified direction.

        Parameters: direction (str): The direction to move the cursor ('up', 'down', 'left', 'right').
        """

        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            if direction == "up":
                self.selected_row -= 1
            elif direction == "down":
                self.selected_row += 1
            elif direction == "left":
                self.selected_col -= 1
            elif direction == "right":
                self.selected_col += 1

            self.selected_row %= len(self.stuff)
            self.selected_col %= len(self.stuff[0])

            if self.stuff[self.selected_row][self.selected_col] is not None:
                break

            attempts += 1

        if attempts == max_attempts:
            pass

        self.current_item = self.stuff[self.selected_row][self.selected_col]

        self.game.sfx['move_cursor'].play()

    def buy(self):
        """
        Applies the selected item.

        Current method is responsible for applying (putting on) equipment by moving the selected item
        on the character
        """
        item = self.stuff[self.selected_row][self.selected_col]
        if item:
            if self.game.player.money >= item.price:
                self.game.player.money -= item.price
                if isinstance(item, Equipment):
                    self.buy_equipment(item)
                elif "Scroll" in type(item).__name__:
                    self.buy_scroll(item)
                elif "Poison" in type(item).__name__:
                    self.buy_poison(item)
                self.stuff[self.selected_row][self.selected_col] = None
                self.game.sfx['buy_goods'].play()
            else:
                self.game.sfx['not_enough_money'].play()

    def buy_equipment(self, item):
        self.game.player.inventory.append(item)
        self.game.inventory_menu.refresh_inventory()

    def buy_scroll(self, item):
        scroll_name = SCROLLS.get(item.name)
        self.game.player.scrolls[scroll_name] += 1

    def buy_poison(self, item):
        potion_type = POTIONS.get(item.i_type)
        setattr(self.game.player, potion_type, getattr(self.game.player, potion_type) + 1)

    def render(self):
        # board
        x = (self.game.display.get_width() - self.goods_stand.get_width()) // 2
        y = 2
        self.game.display.blit(self.goods_stand, (x, y))

        # Displaying items in store cells
        # item_pos = {(i, j): (x + 48 + j * 68, y + 208 + i * 61) for i in range(4) for j in range(6)}
        for i in range(6):
            for j in range(6):
                if i < len(self.stuff) and j < len(self.stuff[i]):
                    item = self.stuff[i][j]
                    if item:
                        item_image = pygame.image.load(item.pic)
                        item_rect = item_image.get_rect()
                        item_rect.topleft = self.item_positions[(i, j)]
                        if [i, j] == [self.selected_row, self.selected_col]:
                            item_image = pygame.transform.scale(item_image,
                                                                (int(item_rect.width * 1.2),
                                                                 int(item_rect.height * 1.2)))

                            details_text = self.font.render('Press "E" to view details', True, 'white')
                            self.game.display.blit(details_text, (x + 32, y + 440))

                        self.game.display.blit(item_image, item_rect)

        if self.view_details:
            self.game.display.blit(self.details_desk, (x + 4, y + 50))
            item = self.stuff[self.selected_row][self.selected_col]
            name_render = self.font_title.render(item.name, True, (255, 255, 255))

            render_list = []

            if item.price > 0:
                price = f"Price        {item.price} Gold"
                price_render = self.font.render(price, True, (255, 255, 255))
                render_list.append(price_render)
            if hasattr(item, 'rarity'):
                eq_class = f"Class         {item.rarity}"
                rarity_render = self.font.render(eq_class, True, (255, 255, 255))
                render_list.append(rarity_render)
            if hasattr(item, 'increase_defence') and item.increase_defence:
                defence = f"Defence         + {item.increase_defence}"
                defence_render = self.font.render(defence, True, (255, 255, 255))
                render_list.append(defence_render)
            if hasattr(item, 'increase_damage') and item.increase_damage > 0:
                damage = f"Damage         + {item.increase_damage}"
                damage_render = self.font.render(damage, True, (255, 255, 255))
                render_list.append(damage_render)
            if hasattr(item, 'distance_damage') and item.distance_damage:
                d_damage = f"Damage         + {item.distance_damage}"
                d_damage_render = self.font.render(d_damage, True, (255, 255, 255))
                render_list.append(d_damage_render)
            if hasattr(item, 'increase_health') and item.increase_health:
                health = f"Health          + {item.increase_health}"
                health_render = self.font.render(health, True, (255, 255, 255))
                render_list.append(health_render)
            if hasattr(item, 'increase_stamina') and item.increase_stamina:
                stamina = f"Stamina         + {item.increase_stamina}"
                stamina_render = self.font.render(stamina, True, (255, 255, 255))
                render_list.append(stamina_render)
            if hasattr(item, 'increase_mana') and item.increase_mana:
                mana = f"Mana           + {item.increase_mana}"
                mana_render = self.font.render(mana, True, (255, 255, 255))
                render_list.append(mana_render)
            if hasattr(item, 'increase_experience') and item.increase_experience:
                experience = f"Experience     + {item.increase_experience} %"
                experience_render = self.font.render(experience, True, (255, 255, 255))
                render_list.append(experience_render)

            self.game.display.blit(name_render, (x + 50, y + 100))

            y_offset = 2
            for i in render_list:
                self.game.display.blit(i, (x + 50, y + 140 + y_offset))
                y_offset += 20

            image = pygame.image.load(self.current_item.pic)
            self.game.display.blit(image, (x + 340, y + 160))

            founds_text = self.font.render(f"Money balance: {self.game.player.money}", True, 'white')
            self.game.display.blit(founds_text, (x + 154, y + 66))

            confirm_text = self.font.render(f"YES/y", True, 'white')
            self.game.display.blit(confirm_text, (x + 72, y + 300))

            cancel_text = self.font.render(f"NO/n", True, 'white')
            self.game.display.blit(cancel_text, (x + 360, y + 300))
