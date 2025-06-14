import math

import pygame

from support import BASE_IMG_PATH
from items import Equipment, Book, QuestItem
from data import POTIONS, SCROLLS, SKILLS, MERCHANT_ITEM_POS, UI_PATH, UI_SET


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

        for image in UI_SET:
            # Loads UI images from files and dynamically creates the corresponding attributes in the class
            setattr(self, image, pygame.image.load(BASE_IMG_PATH + f'ui/{image}.png'))

        self.scroll_slot = UI_PATH.get('scroll_slot')
        self.holly_scroll_icon = UI_PATH.get('holly_scroll_icon')
        self.speed_scroll_icon = UI_PATH.get('speed_scroll_icon')
        self.bloodlust_scroll_icon = UI_PATH.get('bloodlust_scroll_icon')
        self.invulnerability_scroll_icon = UI_PATH.get('invulnerability_scroll_icon')

        self.status_bar = []
        self.heart_image = self.heart_full
        self.corruption_timer_max = 600
        self.double_power_timer_max = 600
        self.super_speed_timer_max = 720
        self.critical_hit_timer_max = 1200
        self.invulnerability_timer_max = 1000
        self.enhanced_protection_timer_max = 1200

        self.spellbook = {
            'holly_spell': self.holly_scroll_icon,
            'speed_spell': self.speed_scroll_icon,
            'bloodlust_spell': self.bloodlust_scroll_icon,
            'invulnerability_spell': self.invulnerability_scroll_icon,
            'fire_totem': self.fire_totem_icon,
            'water_geyser': self.watergeyser_icon,
            'ice_arrow': self.ice_arrow_icon,
            'tornado': self.tornado_icon,
            'runic_obelisk': self.runic_obelisk_icon,
            'magic_shield': self.magic_shield_icon,
        }

        self.blood_overlay_hard = UI_PATH.get('blood_overlay_hard')
        self.blood_overlay_critical = UI_PATH.get('blood_overlay_critical')
        self.blood_overlay_fatally = UI_PATH.get('blood_overlay_fatally')

        # Settings for pulsation
        self.pulse_time = 0

    @staticmethod
    def update_pulse_effect(image):
        """
        Creates a pulsating effect using a sine wave function
        Scales the image x% larger or smaller than the original (in this case, 5%)
        Changes the alpha channel of an image to create a flickering effect
        """
        time = pygame.time.get_ticks() / 1000  # get the time and convert to seconds
        scale = 1 + 0.05 * math.sin(2 * math.pi * time)  # smooth pulsation with an amplitude of 5%
        original_size = image.get_size()
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        scaled_image = pygame.transform.smoothscale(image, new_size)
        alpha = int(128 + 127 * (0.5 * math.sin(2 * math.pi * time) + 0.5))
        scaled_image.set_alpha(alpha)

        return scaled_image, original_size

    def blit_centered(self, image, original_size, position=(-64, -48)):
        """
        Draws the image centered on the display at a specific position.

        :param image: The image to be drawn.
        :param original_size: original_size
        :param position: The position of the image center relative to the display center(
        x=-64, y =-48, because we need 20 % larger image than screen size
        """
        display_rect = self.game.display.get_rect()
        image_rect = image.get_rect(center=display_rect.center)
        image_rect.center = (position[0] + original_size[0] // 2, position[1] + original_size[1] // 2)
        self.game.display.blit(image, image_rect.topleft)

    def render(self):

        # hero panel
        panel_x = - 6
        panel_y = self.display_height - self.panel.get_height() + 20
        self.game.display.blit(self.panel, (panel_x, panel_y))

        # hero icon
        hero_icon_x = panel_x + 15
        hero_icon_y = panel_y + 25
        self.game.display.blit(self.player_icon, (hero_icon_x, hero_icon_y))

        # health & blood screen overlays
        heart_images = {
            range(80, 1001): self.heart_full,
            range(60, 80): self.heart_tq,
            range(40, 60): self.heart_half,
            range(20, 40): self.heart_quarter,
            range(0, 20): self.heart_empty
        }

        health = int((self.game.player.current_health / self.game.player.max_health) * 100)

        if health <= 5:
            pulsating_image, original_size = self.update_pulse_effect(self.blood_overlay_fatally)
            self.blit_centered(pulsating_image, original_size)
        elif health <= 15:
            pulsating_image, original_size = self.update_pulse_effect(self.blood_overlay_critical)
            self.blit_centered(pulsating_image, original_size)
        elif health <= 25:
            pulsating_image, original_size = self.update_pulse_effect(self.blood_overlay_hard)
            self.blit_centered(pulsating_image, original_size)

        self.heart_image = next((img for rng, img in heart_images.items() if health in rng), self.heart_empty)
        self.game.display.blit(pygame.transform.scale(
            self.heart_image, (
                self.heart_image.get_width() * 1.2, self.heart_image.get_height() * 1.2)), (22, 16))

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

        # life
        for i in range(6):
            life_heart_x = 50 + i * 15
            life_heart_y = 28
            if i < self.game.player.life:
                self.game.display.blit(self.life_full, (life_heart_x, life_heart_y))
            else:
                self.game.display.blit(self.life_empty, (life_heart_x, life_heart_y))

        # diamonds
        # diamond_x = panel_x + 76
        # diamond_y = panel_y + 16
        # self.game.display.blit(self.diamond_icon, (diamond_x, diamond_y))
        # artifacts_text = self.font.render(f" {self.game.artifacts_remaining}", True, (148, 0, 211))
        # self.game.display.blit(artifacts_text, (diamond_x + 16, diamond_y + 1))

        # coins
        # coins_x = panel_x + 110
        # coins_y = panel_y + 16
        # self.game.display.blit(self.coin_icon, (coins_x, coins_y))
        # coins_count = self.font.render(f" {self.game.player.money}", True, self.text_color)
        # self.game.display.blit(coins_count, (coins_x + 16, coins_y + 1))

        # shuriken
        # shuriken_count = self.game.player.shuriken_count
        # shuriken_count_x = panel_x + 162
        # shuriken_count_y = panel_y + 16
        # self.game.display.blit(self.shuriken_icon, (shuriken_count_x, shuriken_count_y))
        # shuriken_remaining = self.font.render(f" {shuriken_count}", True, (176, 196, 222))
        # self.game.display.blit(shuriken_remaining, (shuriken_count_x + 16, shuriken_count_y + 1))

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

        # player_level
        l_x, l_y = panel_x + 78, panel_y + 22
        player_level = f"{self.game.player.level}"
        level_render = self.font_lvl.render(player_level, True, (255, 255, 255))
        self.game.display.blit(level_render, (l_x, l_y))

        # potion_bar
        inventory_x = self.display_width // 2 - self.big_inventory_bar.get_width() // 2 + 24
        inventory_y = 8
        self.game.display.blit(self.big_inventory_bar, (inventory_x, inventory_y))

        # potions
        x, y = inventory_x + 6, inventory_y + 8
        icon_offset = 36

        potions = [
            (self.heal_potion_icon, self.game.player.heal_potions),
            (self.mana_potion_icon, self.game.player.magic_potions),
            (self.stamina_potion_icon, self.game.player.stamina_potions),
            (self.power_potion_icon, self.game.player.power_potions),
            (self.antidote_icon, self.game.player.antidotes),
            (self.defense_potion_icon, self.game.player.defense_potions),
        ]

        for potion_icon, potion_count in potions:
            if potion_count > 0:
                self.game.display.blit(potion_icon, (x, y))
                potion_count_text = self.font.render(f" {potion_count}", True, self.text_color)
                self.game.display.blit(potion_count_text, (x + 18, y + 18))
            x += icon_offset

        # frame
        frame_positions = [x - 217 + i * 36 for i in range(7)]
        active_frame = self.game.player.selected_item
        if 1 <= active_frame <= len(frame_positions):
            self.game.display.blit(self.potion_bar_frame, (frame_positions[active_frame - 1], y - 9))

        # spells
        sb_x = self.display_width // 2 - 172
        sb_y = self.display_height - 74
        self.game.display.blit(self.spell_bar, (sb_x, sb_y))

        spells = self.game.player.spells
        spell_cooldowns = self.game.player.spell_cooldowns
        cooldown_durations = self.game.player.cooldown_durations
        current_time = pygame.time.get_ticks()

        if spells:
            x, y = sb_x, sb_y
            icon_offset = 28
            for spell in spells:
                self.game.display.blit(self.spellbook[spell], (x + 64, y + 28))

                remaining_time = (cooldown_durations[spell] - (current_time - spell_cooldowns[spell])) / 1000
                if remaining_time > 0:
                    # spell inactive until recharge
                    overlay = pygame.Surface((24, 24), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 150))
                    self.game.display.blit(overlay, (x + 64, y + 28))
                    text = self.font.render(f"{int(remaining_time)}", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + 76, y + 40))
                    self.game.display.blit(text, text_rect)
                x += icon_offset

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

        # experience
        xp_x = 208
        xp_y = self.display_height - 58
        # self.game.display.blit(self.xp_bar, (xp_x, xp_y))
        xp_line = int(self.game.player.experience / self.game.player.next_level_experience * 100)
        rect = pygame.Rect(xp_x, xp_y, xp_line, 4)
        pygame.draw.rect(self.game.display, (0, 191, 255), rect)

        text = f"XP {self.game.player.experience} / {self.game.player.next_level_experience}"
        text_render = self.font_ui.render(text, True, (255, 255, 255))
        text_width, text_height = self.font.size(text)
        text_x = xp_x - 90 - text_width / 2
        text_y = xp_y + 10 - text_height / 2
        self.game.display.blit(text_render, (text_x, text_y))

        # status
        status_updates = [
            (self.corrupted_icon, 'corruption', self.game.player.corruption),
            (self.double_power_icon, 'double_power', self.game.player.double_power == 2),
            (self.super_speed_icon, 'super_speed', self.game.player.super_speed == 2),
            (self.bloodlust_icon, 'critical_hit', self.game.player.critical_hit_chance),
            (self.invulnerability_icon, 'invulnerability', self.game.player.invulnerability),
            (self.enhanced_protection_icon, 'enhanced_protection', self.game.player.enhanced_protection),
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
            'invulnerability': ('invulnerability_timer', 'invulnerability_timer_max'),
            'enhanced_protection': ('enhanced_protection_timer', 'enhanced_protection_timer_max')
        }

        for pos, (icon, status) in enumerate(self.status_bar):
            x = sb_x + 60 + (22 * pos)
            y = sb_y - 12
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
        origin_img = UI_PATH.get('skills_tree')
        self.skill_tree_base = pygame.transform.scale(origin_img, (origin_img.get_width() // 2, origin_img.get_height() // 2))
        self.skills_frame = UI_PATH.get('skills_frame')
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
        for name, data in SKILLS.items():
            skill = Skill(
                name=name,
                image_path=BASE_IMG_PATH + data["image_path"],
                coordinates=tuple(data["coordinates"]),
                description=data["description"],
                required_experience=data["required_experience"],
                level=data["level"],
                accessibility=data["accessibility"]
            )
            skills.append(skill)
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

            elif isinstance(item, Book):
                item.read()
                self.grid[self.current_cell[0]][self.current_cell[1]] = None
                self.game.player.inventory.remove(item)
                self.game.player.inventory_menu_is_active = False

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
                book_title = self.font.render(current_equipment.book_name, True, (255, 255, 255))
                self.game.display.blit(book_title, (x + 42, y + 92))
                image = pygame.image.load(current_equipment.image)
                self.game.display.blit(image, (x + 52, y + 116))
                hint = self.font.render('To read more, press E', True, (255, 255, 255))
                self.game.display.blit(hint, (x + 48, y + 240))

            elif isinstance(current_equipment, QuestItem):
                name_render = self.font.render(current_equipment.name, True, (255, 255, 255))
                self.game.display.blit(name_render, (x + 42, y + 92))

                lines = current_equipment.description.split('\n')
                for i, line in enumerate(lines):
                    desc_render = self.font.render(line, True, (200, 200, 200))
                    self.game.display.blit(desc_render, (x + 42, y + 110 + i * 16))

        # Magic scrolls rendering
        x_offset = 92
        for scroll in self.game.player.scrolls.items():
            scroll_image = self.game.ui.spellbook.get(scroll[0])
            scroll_image = pygame.transform.scale(scroll_image,
                                                  (scroll_image.get_width() * 0.65, scroll_image.get_height() * 0.65))
            scroll_amount = scroll[1]
            if scroll[1] > 0:
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
