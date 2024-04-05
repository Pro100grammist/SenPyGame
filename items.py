import random
import pygame


from collections import defaultdict
from typing import Any

from support import BASE_IMG_PATH
from data import EQUIPMENT, player_equipments


class GameLoot:
    """
    The class represents the gaming items like a potions, scrolls, coins, gems.
    """
    def __init__(self, game, pos, size, i_type, name=None):
        """
        Initializes the GameLoot object.
        :param game: game class instance
        :param pos: spawn position on map
        :param size: the size of the object's rectangle for intercepting collisions with it
        :param i_type: type of GameLoot object item
        """
        self.game = game
        self.i_type = i_type
        self.name = name
        self.animation = self.game.assets['loot/' + self.i_type].copy() if self.game else None
        self.pos = list(pos) if pos else None
        self.size = size
        self.flip = False
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) if self.pos else None

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def update(self):
        self.animation.update()

        player_stuff = {
            'coin': 'money',
            'gem': 'artifacts_remaining',
            'glass_red': 'heal_potions',
            'glass_blue': 'magic_potions',
            'glass_green': 'stamina_potions',
            'glass_yellow': 'power_potions',
        }

        scrolls = {
            'holly_scroll': 'holly_spell',
            'bloodlust_scroll': 'bloodlust_spell',
            'speed_scroll': 'speed_spell',
            'invulnerability_scroll': 'invulnerability_spell',
        }

        keys = ['steel_key', 'red_key', 'bronze_key', 'purple_key', 'gold_key']

        for loot_item in self.game.loot.copy():
            if loot_item.rect.colliderect(self.game.player.rect()):
                self.game.sfx[loot_item.i_type].play()
                if loot_item.i_type in player_stuff:
                    if loot_item.i_type == 'gem':
                        self.game.artifacts_remaining -= 1
                    else:
                        player_thing = player_stuff[loot_item.i_type]
                        setattr(self.game.player, player_thing, getattr(self.game.player, player_thing) + 1)
                elif loot_item.i_type in scrolls:
                    scroll_name = scrolls[loot_item.i_type]
                    if scroll_name in self.game.player.scrolls:
                        self.game.player.scrolls[scroll_name] += 1
                    else:
                        self.game.player.scrolls[scroll_name] = 1
                elif loot_item.i_type in keys:
                    self.game.player.keys[loot_item.i_type] += 1

                self.game.loot.remove(loot_item)

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - offset[0], self.pos[1] - 2 - offset[1]))


class Gem(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'gem')
        self.name = 'Gem'


class Coin(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'coin')
        self.name = 'Coin'


# Potions
class HealthPoison(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'glass_red')
        self.name = 'Health Potion'
        self.price = 3
        self.pic = BASE_IMG_PATH + 'ui/merchant/health_potion.png'


class MagicPoison(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'glass_blue')
        self.name = 'Magic Potion'
        self.price = 3
        self.pic = BASE_IMG_PATH + 'ui/merchant/mana_potion.png'


class StaminaPoison(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'glass_green')
        self.name = 'Stamina Poison'
        self.price = 2
        self.pic = BASE_IMG_PATH + 'ui/merchant/stamina_potion.png'


class PowerPoison(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'glass_yellow')
        self.name = 'PowerPoison'
        self.price = 6
        self.pic = BASE_IMG_PATH + 'ui/merchant/power_potion.png'


# scrolls
class HollyScroll(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'holly_scroll')
        self.name = 'Holly Scroll'
        self.price = 10
        self.pic = BASE_IMG_PATH + 'ui/scrolls/holly_scroll.png'


class BloodlustScroll(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'bloodlust_scroll')
        self.name = 'Bloodlust Scroll'
        self.price = 5
        self.pic = BASE_IMG_PATH + 'ui/scrolls/bloodlust_scroll.png'


class SpeedScroll(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'speed_scroll')
        self.name = 'Speed Scroll'
        self.price = 5
        self.pic = BASE_IMG_PATH + 'ui/scrolls/speed_scroll.png'


class InvulnerabilityScroll(GameLoot):
    def __init__(self, game=None, pos=None, size=None):
        super().__init__(game, pos, size, 'invulnerability_scroll')
        self.name = 'Invulnerability Scroll'
        self.price = 10
        self.pic = BASE_IMG_PATH + 'ui/scrolls/invulnerability_scroll.png'


def create_scroll():
    available_scrolls = [BloodlustScroll, SpeedScroll, InvulnerabilityScroll, HollyScroll, SpeedScroll, HollyScroll]
    random.shuffle(available_scrolls)
    scrolls = []
    for scroll in available_scrolls[:6]:
        scrolls.append(scroll())

    return scrolls


def create_poison():
    available_poisons = [HealthPoison, MagicPoison, StaminaPoison, PowerPoison, HealthPoison, StaminaPoison]
    random.shuffle(available_poisons)
    poisons = []
    for poison in available_poisons[:6]:
        poisons.append(poison())

    return poisons


class Equipment:
    """
    The class represents game equipment like weapon, armor, jewelry, and other.
    """
    def __init__(self, name='', e_type='', e_class=0, rarity='', condition=0, pic=None, price=0, properties=None):
        self.name = name
        self.e_type = e_type
        self.e_class = e_class
        self.rarity = rarity
        self.properties = properties
        self.condition = condition
        self.current_condition = self.condition
        self.pic = pic
        self.price = price

        self.increase_defence = self.properties.get('defence', 0)
        self.increase_damage = self.properties.get('damage', 0)
        self.increase_health = self.properties.get('health', 0)
        self.increase_stamina = self.properties.get('stamina', 0)
        self.increase_mana = self.properties.get('mana', 0)
        self.increase_experience = self.properties.get('experience', 0)
        self.distance_damage = self.properties.get('distance_damage', 0)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


def load_default_equipment():
    """
    Creates instances of the Equipment class and passes the equipment defined by default
    at the beginning of the game to the "equipment" dictionary of the Player class instance.
    """
    return {item["e_type"]: Equipment(**item) for item in DEFAULT_EQUIPMENT.values()}


# cache for equipment items
equipment_cache: defaultdict[str, Any] = defaultdict(dict)


def create_equipment(name=None, rareness=None):
    """
    Creates specific or random instances of the Equipment class in the game when it needed.
    """
    if name:
        if name in equipment_cache:
            return equipment_cache[name]
        elif name in EQUIPMENT:
            equipment_instance = Equipment(**EQUIPMENT[name])
            equipment_cache[name] = equipment_instance
            return equipment_instance
        else:
            raise ValueError("An object of the Equipment class with this name does not exist.")
    else:
        rarity = rareness if rareness else random.choices(['Common', 'Rare', 'Unique', 'Epic', 'Legendary', 'Mythical'], weights=[80, 12, 5, 2, 0.9, 0.1], k=1)[0]
        random_item = random.choice(player_equipments[rarity])
        if random_item in equipment_cache:
            return equipment_cache[random_item]
        else:
            equipment_instance = Equipment(**EQUIPMENT[random_item])
            equipment_cache[random_item] = equipment_instance
            return equipment_instance


class Chest:
    def __init__(self, game, pos, size, lock=None, chest_class='common'):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.lock = lock
        self.is_opened = False
        self.animation = self.game.assets['chest/' + chest_class].copy()
        self.chest_close = self.animation.images[0]
        self.chest_opened = self.animation.images[-1]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.message_panel = pygame.image.load(BASE_IMG_PATH + 'tiles/chest/panel/msg_panel.png')
        self.font = pygame.font.Font('data/fonts/simple.ttf', 14)
        self.keys_map = {
            "steel_key": 'Rare', "red_key": 'Unique', "bronze_key": 'Epic', "purple_key": 'Legendary',
            "gold_key": 'Mythical'
        }

    def open(self):
        if not self.is_opened:
            if self.lock is None or self.game.player.keys[self.lock] > 0:
                self.is_opened = True
                self.game.sfx['chest_open'].play()
                if self.lock is not None:
                    self.game.player.keys[self.lock] -= 1
                self.get_item()
            else:
                pass
                # self.game.sfx['closed_lock'].play()

    def get_item(self):
        # Generate and add equipment to player's inventory
        if self.lock:
            equipment = create_equipment(rareness=self.keys_map[self.lock])  # Create equipment based on chest class
        else:
            equipment = create_equipment()  # Create random equipment
        self.game.player.inventory.append(equipment)
        self.game.inventory_menu.refresh_inventory()

    def update(self):
        if self.is_opened and not self.animation.done:
            self.animation.update()

    def render(self, surf, offset=(0, 0)):
        window_offset_x = 40
        window_offset_y = 40
        msg_offset_x = 28
        msg_offset_y = 30
        if not self.is_opened:
            # Render closed chest
            surf.blit(self.chest_close, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

            if self.rect.colliderect(self.game.player.rect()):
                surf.blit(self.message_panel, (self.pos[0] - window_offset_x - offset[0], self.pos[1] - window_offset_y - offset[1]))
                if self.lock is None or self.game.player.keys[self.lock] > 0:
                    message = self.font.render("TO OPEN PRESS X", True, (189, 165, 139))
                    surf.blit(message, (self.pos[0] - msg_offset_x - offset[0], self.pos[1] - msg_offset_y - offset[1]))
                else:
                    message = self.font.render(f"NEED A {self.lock.replace('_', ' ').upper()}", True, (189, 165, 139))
                    surf.blit(message, (self.pos[0] - msg_offset_x - offset[0], self.pos[1] - msg_offset_y - offset[1]))

        else:
            # Render open chest
            if self.animation.done:
                surf.blit(self.chest_opened, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            else:
                surf.blit(self.animation.current_sprite(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

        # pygame.draw.rect(surf, (0, 255, 0), (self.rect.x - offset[0], self.rect.y - offset[1],
        #                                      self.rect.width, self.rect.height), 1)


# chests
class CommonChest(Chest):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)


class RareChest(Chest):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, lock='steel_key', chest_class='rare')


class UniqueChest(Chest):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, lock='red_key', chest_class='unique')


class EpicChest(Chest):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, lock='bronze_key', chest_class='epic')


class LegendaryChest(Chest):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, lock='purple_key', chest_class='legendary')


class MythicalChest(Chest):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, lock='gold_key', chest_class='mythical')


# keys
class SteelKey(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'steel_key')


class RedKey(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'red_key')


class BronzeKey(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'bronze_key')


class PurpleKey(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'purple_key')


class GoldKey(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'gold_key')


class Merchant:
    """
    Class representing traders and merchants in the game.
    """

    def __init__(self, game, pos, size=(32, 32)):
        self.game = game
        self.animation = self.game.assets['merchant'].copy()
        self.pos = list(pos)
        self.size = size
        self.flip = False
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0] + 16, self.size[1] + 16)
        self.stuff = self.generate_stuff()

    @staticmethod
    def generate_stuff():
        stuff = create_scroll() + create_poison()

        while len(stuff) < 36:
            item = create_equipment()
            if item not in stuff:
                stuff.append(item)

        return [stuff[i:i + 6] for i in range(0, len(stuff), 6)]

    def look_stuff(self):
        self.game.merchant_window.stuff = self.stuff
        self.game.player.trading = True

    def update(self):
        self.animation.update()

        for trader in self.game.merchants.copy():
            if trader.rect.colliderect(self.game.player.rect()):
                pass

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1]))
