import pygame

from support import BASE_IMG_PATH


class GameLoot:
    def __init__(self, game, pos, size, i_type):
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
    def __init__(self, name='', e_type='', e_class=0, rarity='', defence=0, damage=0, condition=0, pic=None, price=0):
        self.name = name
        self.e_type = e_type
        self.e_class = e_class
        self.rarity = rarity
        self.defence = defence
        self.damage = damage
        self.condition = condition
        self.pic = pic
        self.price = price


def load_default_equipment():

    equipment = []

    # default body armor
    body_armor_default = Equipment(
        name="Iron Chest Armor",
        e_type="body_armor",
        e_class=0,
        rarity="common",
        defence=1,
        damage=0,
        condition=1000,
        pic=BASE_IMG_PATH + 'ui/equipment/body_armor.png',
        price=25
    )
    equipment.append(body_armor_default)

    return equipment


