import pygame

from collections import defaultdict
from typing import Any

from support import BASE_IMG_PATH
from data import DEFAULT_EQUIPMENT, player_equipments


class GameLoot:
    """
    The class represents the gaming items like a potions, scrolls, coins, gems.
    """
    def __init__(self, game, pos, size, i_type):
        """
        Initializes the GameLoot object.
        :param game: game class instance
        :param pos: spawn position on map
        :param size: the size of the object's rectangle for intercepting collisions with it
        :param i_type: type of GameLoot object item
        """
        self.game = game
        self.i_type = i_type
        self.animation = self.game.assets['loot/' + self.i_type].copy()
        self.pos = list(pos)
        self.size = size
        self.flip = False
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

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
                self.game.loot.remove(loot_item)

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - offset[0], self.pos[1] - 2 - offset[1]))


class Gem(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'gem')


class Coin(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'coin')


# Potions
class HealthPoison(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'glass_red')


class MagicPoison(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'glass_blue')


class StaminaPoison(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'glass_green')


class PowerPoison(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'glass_yellow')


# scrolls
class HollyScroll(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'holly_scroll')


class BloodlustScroll(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'bloodlust_scroll')


class SpeedScroll(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'speed_scroll')


class InvulnerabilityScroll(GameLoot):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'invulnerability_scroll')


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
