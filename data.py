import json
import pygame

from support import load_image, load_images, load_images_entities
from support import BASE_IMG_PATH, Animation


def load_assets():
    """
    :return: dictionary with Surface objects that represent static image or Animation objects (group of sprites)
    """
    return {
        # levels background
        'background': load_images('background'),

        # projectiles and weapons
        'bow': load_image('weapons/bow.png'),
        'projectile': load_image('weapons/arrow.png'),
        'arrow': load_image('weapons/arrow.png'),
        'suriken': load_image('weapons/suriken.png'),

        # animated projectiles
        'fireball': load_images('particles/fireball'),
        'skullsmoke': load_images('particles/skullmoke'),

        # spells
        'holly_spell': load_images('particles/spell/holly_spell'),
        'speed_spell': load_images('particles/spell/speed_spell'),
        'bloodlust_spell': load_images('particles/spell/bloodlust_spell'),
        'invulnerability_spell': load_images('particles/spell/invulnerability_spell'),
        'blood': load_images('particles/spell/blood'),
        'fire_totem': load_images('particles/fire_totem'),

        # tiles
        'background_objects': load_images('tiles/background_objects'),
        'clouds': load_images('clouds'),
        'decor': load_images('tiles/decor'),
        'grass': load_images('tiles/grass'),
        'large_decor': load_images('tiles/large_decor'),
        'stone': load_images('tiles/stone'),
        'terrain': load_images('tiles/terrain'),

        # animated tiles
        'animated_tiles': [
            load_images('animated_tiles/wall_fountain_basin_blue'),
            load_images('animated_tiles/wall_fountain_basin_red'),
            load_images('animated_tiles/wall_fountain_mid_blue'),
            load_images('animated_tiles/wall_fountain_mid_red'),
        ],

        # enemies
        'orc_archer/idle': Animation(
            load_images_entities('entities/enemy/orc_archer/idle', trim_left=0, trim_right=0, scale_factor=1.25),
            img_dur=6),
        'orc_archer/run': Animation(
            load_images_entities('entities/enemy/orc_archer/run', trim_left=0, trim_right=0, scale_factor=1.25),
            img_dur=4),

        'big_zombie/idle': Animation(
            load_images_entities('entities/enemy/big_zombie/idle', trim_left=0, trim_right=0, scale_factor=1),
            img_dur=6),
        'big_zombie/run': Animation(
            load_images_entities('entities/enemy/big_zombie/run', trim_left=0, trim_right=0, scale_factor=1),
            img_dur=4),

        'big_daemon/idle': Animation(load_images_entities('entities/enemy/big_daemon/idle', scale_factor=1), img_dur=6),
        'big_daemon/run': Animation(load_images_entities('entities/enemy/big_daemon/run', scale_factor=1), img_dur=4),

        # player
        'player/idle': Animation(load_images_entities('entities/player/idle'), img_dur=6),
        'player/run': Animation(load_images_entities('entities/player/run'), img_dur=4),
        'player/attack': Animation(load_images_entities('entities/player/attack', trim_right=0), img_dur=3),
        'player/dash_attack': Animation(load_images_entities('entities/player/dash_attack'), img_dur=6),
        'player/jump': Animation(load_images_entities('entities/player/jump'), img_dur=3),
        'player/fall': Animation(load_images_entities('entities/player/fall'), img_dur=3),
        'player/slide': Animation(load_images_entities('entities/player/slide'), img_dur=5),
        'player/wall_slide': Animation(load_images_entities('entities/player/wall_slide', trim_left=0, trim_right=0),
                                       img_dur=3),
        'player/death': Animation(load_images_entities('entities/player/death', trim_left=0, trim_right=0), img_dur=6),

        # game loot
        'loot/gem': Animation(load_images('tiles/loot/gem'), img_dur=6),
        'loot/coin': Animation(load_images('tiles/loot/coin'), img_dur=6),
        'loot/glass_red': Animation(load_images('tiles/loot/glass_red'), img_dur=6),
        'loot/glass_blue': Animation(load_images('tiles/loot/glass_blue'), img_dur=6),
        'loot/glass_green': Animation(load_images('tiles/loot/glass_green'), img_dur=6),
        'loot/glass_yellow': Animation(load_images('tiles/loot/glass_yellow'), img_dur=6),
        'loot/holly_scroll': Animation(load_images('tiles/loot/holly_scroll')),
        'loot/bloodlust_scroll': Animation(load_images('tiles/loot/bloodlust_scroll')),
        'loot/speed_scroll': Animation(load_images('tiles/loot/speed_scroll')),
        'loot/invulnerability_scroll': Animation(load_images('tiles/loot/invulnerability_scroll')),
        'loot/dungeon_shadows': load_image('ui/books/books_icons/dungeon_shadows.png'),
        'loot/forgotten_souls': load_image('ui/books/books_icons/forgotten_souls.png'),
        'loot/bridge_to_eternity': load_image('ui/books/books_icons/bridge_to_eternity.png'),
        'loot/whispers_of_afterlife': load_image('ui/books/books_icons/whispers_of_afterlife.png'),
        'loot/necronomicon': load_image('ui/books/books_icons/necronomicon.png'),
        'loot_spawn': load_images('tiles/loot_spawn'),

        # keys
        'loot/steel_key': Animation(load_images('tiles/loot/keys/steel_key'), img_dur=6),
        'loot/red_key': Animation(load_images('tiles/loot/keys/red_key'), img_dur=6),
        'loot/bronze_key': Animation(load_images('tiles/loot/keys/bronze_key'), img_dur=6),
        'loot/purple_key': Animation(load_images('tiles/loot/keys/purple_key'), img_dur=6),
        'loot/gold_key': Animation(load_images('tiles/loot/keys/gold_key'), img_dur=6),

        # chests
        'chest/common': Animation(load_images('tiles/chest/common'), img_dur=6, loop=False),
        'chest/rare': Animation(load_images('tiles/chest/rare'), img_dur=6, loop=False),
        'chest/unique': Animation(load_images('tiles/chest/unique'), img_dur=6, loop=False),
        'chest/epic': Animation(load_images('tiles/chest/epic'), img_dur=6, loop=False),
        'chest/legendary': Animation(load_images('tiles/chest/legendary'), img_dur=6, loop=False),
        'chest/mythical': Animation(load_images('tiles/chest/mythical'), img_dur=6, loop=False),
        'chest_spawn': load_images('tiles/chest/chest_spawn/'),

        # traders
        'merchant': Animation(load_images_entities('entities/merchant', scale_factor=0.80), img_dur=8),

        # particle
        'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),

        # effects
        'kaboom': load_images('particles/kaboom'),
        'necromancy': load_images('particles/spell/necromancy'),
    }


def load_sfx():
    sound_names = ['jump', 'jump1', 'jump2', 'jump3', 'dash', 'hit', 'shoot', 'arrow_crash', 'ambience',
                   'attack', 'attack1', 'attack2', 'attack3', 'pain', 'damaged1', 'damaged2', 'damaged3', 'running',
                   'orc_archer', 'big_zombie', 'big_daemon',
                   'fireball', 'fire_hit', 'fire_punch',
                   'coin', 'gem', 'glass_red', 'glass_blue', 'glass_green', 'glass_yellow', 'level_up',
                   'switch', 'select', 'use_potion', 'suriken_rebound', 'locked',
                   'flipping_scroll1', 'flipping_scroll2', 'flipping_scroll3',
                   'green_smoke', 'corruption',
                   'holly_spell', 'speed_spell', 'bloodlust_spell', 'invulnerability_spell',
                   'holly_scroll', 'bloodlust_scroll', 'speed_scroll', 'invulnerability_scroll',
                   'heal', 'healed', 'cough', 'tired', 'revive',
                   'move_cursor', 'open_skill', 'rejected', 'chest_open',
                   'steel_key', 'red_key', 'bronze_key', 'purple_key', 'gold_key',
                   'not_enough_money', 'buy_goods', 'item_equip', 'get_item', 'lock_closed']

    return {name: pygame.mixer.Sound(f'data/sfx/{name}.wav') for name in sound_names}


POTIONS = {
    'glass_red': 'heal_potions',
    'glass_green': 'stamina_potions',
    'glass_blue': 'magic_potions',
    'glass_yellow': 'power_potions'
}

SCROLLS = {
    'Holly Scroll': 'holly_spell',
    'Speed Scroll': 'speed_spell',
    'Bloodlust Scroll': 'bloodlust_spell',
    'Invulnerability Scroll': 'invulnerability_spell'
}

UI_PATH = {

    'skills_tree': pygame.image.load(BASE_IMG_PATH + 'ui/skills/skills_tree.png'),
    'skills_frame': pygame.image.load(BASE_IMG_PATH + 'ui/skills/skills_frame.png'),

    'scroll_slot': pygame.image.load(BASE_IMG_PATH + 'ui/scroll_slot.png'),
    'holly_scroll_icon': pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/holly_scroll.png'),
    'speed_scroll_icon': pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/speed_scroll.png'),
    'bloodlust_scroll_icon': pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/bloodlust_scroll.png'),
    'invulnerability_scroll_icon': pygame.image.load(BASE_IMG_PATH + 'ui/scrolls/invulnerability_scroll.png'),

    'goods_stand': pygame.image.load(BASE_IMG_PATH + 'ui/merchant/merchant_window.png'),
    'details_desk': pygame.image.load(BASE_IMG_PATH + 'ui/merchant/details_board.png'),
    'frame': pygame.image.load(BASE_IMG_PATH + 'ui/inventory/inventory_window_frame.png'),

    'blood_overlay_hard': pygame.image.load(BASE_IMG_PATH + 'ui/screen_overlay_effect/blood_overlay_hard.png'),
    'blood_overlay_critical': pygame.image.load(BASE_IMG_PATH + 'ui/screen_overlay_effect/blood_overlay_critical.png'),
    'blood_overlay_fatally': pygame.image.load(BASE_IMG_PATH + 'ui/screen_overlay_effect/blood_overlay_fatally.png'),

}

UI_SET = [
    'life_full', 'life_empty', 'heart_full', 'heart_tq', 'heart_half', 'heart_quarter', 'heart_empty',
    'globe_full', 'globe_tq', 'globe_half', 'globe_quarter', 'globe_empty', 'corner_set', 'vignette',
    'diamond_icon', 'panel', 'shuriken_icon', 'player_icon', 'inventory_bar', 'coin_icon',
    'heal_potion_icon', 'mana_potion_icon', 'stamina_potion_icon', 'power_potion_icon', 'inventory_frame',
    'corrupted_icon', 'double_power_icon', 'super_speed_icon', 'bloodlust_icon', 'invulnerability_icon',
    'scroll_slot', 'hud_bg', 'xp_bar'
]

MERCHANT_ITEM_POS = {
    (0, 0): (116, 52), (0, 1): (184, 52), (0, 2): (252, 52), (0, 3): (320, 52), (0, 4): (388, 52), (0, 5): (450, 52),
    (1, 0): (138, 140), (1, 1): (202, 140), (1, 2): (269, 140), (1, 3): (336, 140), (1, 4): (406, 140),
    (1, 5): (473, 140),
    (2, 0): (138, 208), (2, 1): (200, 208), (2, 2): (269, 208), (2, 3): (336, 208), (2, 4): (406, 208),
    (2, 5): (473, 208),
    (3, 0): (138, 268), (3, 1): (200, 268), (3, 2): (269, 268), (3, 3): (336, 268), (3, 4): (406, 268),
    (3, 5): (473, 268),
    (4, 0): (138, 328), (4, 1): (200, 328), (4, 2): (269, 328), (4, 3): (336, 328), (4, 4): (406, 328),
    (4, 5): (473, 328),
    (5, 0): (138, 388), (5, 1): (200, 388), (5, 2): (269, 388), (5, 3): (336, 388), (5, 4): (406, 388),
    (5, 5): (473, 388)
}

COLOR_SCHEMA = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'orange': (255, 152, 0),
    'big_daemon': (255, 69, 0),
    'big_zombie': (127, 255, 0),
    'orc_archer': (255, 0, 0),
    'fireball': (255, 140, 0),
    'toxic': (127, 255, 0, 150)
}

EXP_POINTS = {
    'big_daemon': 50,
    'big_zombie': 30,
    'orc_archer': 10,
}


def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


EQUIPMENTS_CATEGORIES = load_data('data/objects/equipment_categories.json')

EQUIPMENT = load_data('data/objects/equipment.json')

BOOKS = load_data('data/objects/books.json')

SKILLS = load_data('data/objects/skills.json')
