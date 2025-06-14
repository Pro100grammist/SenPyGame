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
        'rusty_shuriken': load_image('weapons/shuriken/rusty_shuriken.png').convert_alpha(),
        'steel_shuriken': load_image('weapons/shuriken/steel_shuriken.png').convert_alpha(),
        'ice_shuriken': load_image('weapons/shuriken/ice_shuriken.png').convert_alpha(),
        'emerald_shuriken': load_image('weapons/shuriken/emerald_shuriken.png').convert_alpha(),
        'poisoned_shuriken': load_image('weapons/shuriken/poisoned_shuriken.png').convert_alpha(),
        'phantom_shuriken': load_image('weapons/shuriken/phantom_shuriken.png').convert_alpha(),
        'shuriken_piranha': load_image('weapons/shuriken/shuriken_piranha.png').convert_alpha(),
        'stinger_shuriken': load_image('weapons/shuriken/stinger_shuriken.png').convert_alpha(),
        'supersonic_shuriken': load_image('weapons/shuriken/supersonic_shuriken.png').convert_alpha(),
        'double_bladed_shuriken': load_image('weapons/shuriken/double_bladed_shuriken.png').convert_alpha(),

        # animated projectiles
        'fireball': load_images('particles/fireball'),
        'ground_flame': load_images('particles/ground_flame'),
        'fire': load_images('entities/enemy/supreme_daemon/daemon_breath/fire'),
        'fire_flip': load_images('entities/enemy/supreme_daemon/daemon_breath/fire_flip'),
        'blue_fire': load_images('entities/enemy/supreme_daemon/daemon_breath/blue_fire'),
        'blue_fire_flip': load_images('entities/enemy/supreme_daemon/daemon_breath/blue_fire_flip'),
        'worm_fireball': load_images('entities/enemy/fire_worm/fire_ball/move'),
        'skullsmoke': load_images('particles/skullmoke'),
        'toxic_explosion': load_images('particles/toxic_explosion'),
        'earth_strike': load_images('particles/earth_strike'),
        'rock_wave': load_images('particles/rock_wave'),

        # spells
        'holly_spell': load_images('particles/spell/holly_spell'),
        'speed_spell': load_images('particles/spell/speed_spell'),
        'bloodlust_spell': load_images('particles/spell/bloodlust_spell'),
        'invulnerability_spell': load_images('particles/spell/invulnerability_spell'),
        'blood': load_images('particles/spell/blood'),
        'fire_totem': load_images('particles/fire_totem'),
        'hell_storm': load_images('particles/hell_storm'),
        'water_geyser': load_images('particles/spell/water_geyser'),
        'magic_shield': load_images('particles/magic_shield'),
        'magic_shield_effect': load_images('particles/magic_shield_effect'),
        'tornado': load_images('particles/spell/tornado'),
        'water_tornado': load_images('particles/spell/water_tornado'),
        'ice_arrow': load_images('particles/ice_arrow'),
        'thunderbolt': load_images('particles/thunderbolt'),
        'runic_obelisk': load_images('particles/runic_obelisk'),
        'dashing': load_images('particles/dashing'),
        'freezing': load_images('particles/freezing'),

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
        'orc_archer/idle': Animation(load_images_entities('entities/enemy/orc_archer/idle', scale_factor=1.25), img_dur=6),
        'orc_archer/run': Animation(load_images_entities('entities/enemy/orc_archer/run', scale_factor=1.25), img_dur=4),

        'big_zombie/idle': Animation(load_images_entities('entities/enemy/big_zombie/idle', scale_factor=1), img_dur=6),
        'big_zombie/run': Animation(load_images_entities('entities/enemy/big_zombie/run', scale_factor=1), img_dur=4),

        'fire_worm/idle': Animation(load_images_entities('entities/enemy/fire_worm/idle', scale_factor=1), img_dur=6),
        'fire_worm/run': Animation(load_images_entities('entities/enemy/fire_worm/run', scale_factor=1), img_dur=6),
        'fire_worm/attack': Animation(load_images_entities('entities/enemy/fire_worm/attack', scale_factor=1), loop=False, img_dur=3),
        'fire_worm/dead': Animation(load_images_entities('entities/enemy/fire_worm/dead', scale_factor=1), loop=False, img_dur=8),

        'big_daemon/idle': Animation(load_images_entities('entities/enemy/big_daemon/idle', scale_factor=1), img_dur=6),
        'big_daemon/run': Animation(load_images_entities('entities/enemy/big_daemon/run', scale_factor=1), img_dur=4),

        'supreme_daemon/idle': Animation(load_images_entities('entities/enemy/supreme_daemon/idle', scale_factor=1), img_dur=6),
        'supreme_daemon/run': Animation(load_images_entities('entities/enemy/supreme_daemon/run', scale_factor=1), img_dur=8),
        'supreme_daemon/attack': Animation(load_images_entities('entities/enemy/supreme_daemon/attack', scale_factor=1), loop=False, img_dur=6),

        'golem/idle': Animation(load_images_entities('entities/enemy/golem/idle', scale_factor=1), img_dur=7),
        'golem/run': Animation(load_images_entities('entities/enemy/golem/run', scale_factor=1), img_dur=6),
        'golem/attack': Animation(load_images_entities('entities/enemy/golem/attack', scale_factor=1), loop=False, img_dur=6),
        'golem/hurt': Animation(load_images_entities('entities/enemy/golem/hurt', scale_factor=1), loop=False, img_dur=12),
        'golem/dead': Animation(load_images_entities('entities/enemy/golem/dead', scale_factor=1), loop=False, img_dur=8),

        'hells_watchdog/idle': Animation(load_images_entities('entities/enemy/hells_watchdog/idle', scale_factor=1), img_dur=8),
        'hells_watchdog/run': Animation(load_images_entities('entities/enemy/hells_watchdog/run', scale_factor=1), img_dur=8),
        'hells_watchdog/attack': Animation(load_images_entities('entities/enemy/hells_watchdog/attack', scale_factor=1), loop=False, img_dur=12),
        'hells_watchdog/hurt': Animation(load_images_entities('entities/enemy/hells_watchdog/hurt', scale_factor=1), loop=False, img_dur=12),
        'hells_watchdog/dead': Animation(load_images_entities('entities/enemy/hells_watchdog/dead', scale_factor=1), loop=False, img_dur=10),
        # player
        'player/idle': Animation(load_images_entities('entities/player/idle'), img_dur=6),
        'player/run': Animation(load_images_entities('entities/player/run'), img_dur=4),
        'player/attack': Animation(load_images_entities('entities/player/attack', trim_right=0), img_dur=3),
        'player/dash_attack': Animation(load_images_entities('entities/player/dash_attack'), img_dur=6),
        'player/jump': Animation(load_images_entities('entities/player/jump'), img_dur=3),
        'player/fall': Animation(load_images_entities('entities/player/fall'), img_dur=3),
        'player/slide': Animation(load_images_entities('entities/player/slide'), img_dur=5),
        'player/wall_slide': Animation(load_images_entities('entities/player/wall_slide', trim_left=0, trim_right=0), img_dur=3),
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
        'loot/magic_crystal': Animation(load_images('tiles/loot/magic_crystal')),
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

        # portals
        'portals/inter_level': Animation(load_images('tiles/portals/inter_level'), img_dur=6, loop=False),

        # traders
        'merchant': Animation(load_images_entities('entities/merchant', scale_factor=0.80), img_dur=8),

        # npc
        'old_man': Animation(load_images_entities('npc/old_man', scale_factor=1), img_dur=8),
        'blacksmith': Animation(load_images_entities('npc/blacksmith', scale_factor=1), img_dur=8),

        # particle
        'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
        'particle/cross_particle': Animation(load_images('particles/cross_particle'), img_dur=6, loop=False),

        # effects
        'kaboom': load_images('particles/kaboom'),
        'puff_and_stars': load_images('particles/puff_and_stars'),
        'necromancy': load_images('particles/spell/necromancy'),
    }


def load_sfx():
    sound_names = ['jump', 'jump1', 'jump2', 'jump3', 'dash', 'hit', 'shoot', 'arrow_crash', 'ambience',
                   'attack', 'attack1', 'attack2', 'attack3', 'pain', 'damaged1', 'damaged2', 'damaged3', 'running',
                   'orc_archer', 'big_zombie', 'big_daemon', 'supreme_daemon', 'golem', 'golem_attack', 'golem_fall',
                   'fire_worm', 'fire_worm1', 'fire_worm2', 'fire_worm3', 'freezing', 'rock_wave', 'hells_watchdog',
                   'fireball', 'fire_hit', 'fire_punch', 'burning', 'ice_arrow', 'ice_hit', 'tornado', 'runic_obelisk',
                   'coin', 'gem', 'glass_red', 'glass_blue', 'glass_green', 'glass_yellow', 'level_up',
                   'switch', 'select', 'use_potion', 'suriken_rebound', 'locked', 'portal_rock_break',
                   'flipping_scroll1', 'flipping_scroll2', 'flipping_scroll3',
                   'green_smoke', 'zombie_fart', 'corruption', 'water', 'geyser', 'hell_storm', 'thunder',
                   'holly_spell', 'speed_spell', 'bloodlust_spell', 'invulnerability_spell',
                   'holly_scroll', 'bloodlust_scroll', 'speed_scroll', 'invulnerability_scroll',
                   'heal1', 'heal2', 'heal3', 'healed', 'cough', 'tired', 'revive',
                   'cursor_up', 'cursor_down', 'cursor_select', 'move_cursor', 'open_skill', 'rejected', 'chest_open',
                   'steel_key', 'red_key', 'bronze_key', 'purple_key', 'gold_key',
                   'not_enough_money', 'buy_goods', 'item_equip', 'get_item', 'lock_closed', 'default_item_equip',
                   'new_journal_entry', 'quest_completed',
                   ]

    return {name: pygame.mixer.Sound(f'data/sfx/{name}.wav') for name in sound_names}


def load_voices():
    voice_names = [
        'old_man_greetings', 'old_man_response_001', 'old_man_response_002', 'old_man_response_003', 'old_man_response_004',
        'old_man_response_012', 'old_man_response_014', 'old_man_response_022', 'old_man_response_112', 'old_man_response_212'
    ]
    return {name: pygame.mixer.Sound(f'data/voices/{name}.wav') for name in voice_names}


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

SPELL_COOLDOWN = {
    'fire_totem': 0,
    'water_geyser': 0,
    'ice_arrow': 0,
    'tornado': 0,
    'runic_obelisk': 0,
    'magic_shield': 0,
}

COOLDOWN_DURATIONS = {
    'fire_totem': 10000,
    'water_geyser': 2000,
    'ice_arrow': 3000,
    'tornado': 20000,
    'runic_obelisk': 15000,
    'magic_shield': 12000,
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

    'dialogue_box': pygame.image.load(BASE_IMG_PATH + 'ui/dialog/dialogue_box.png'),
    'dialogue_box_npc': pygame.image.load(BASE_IMG_PATH + 'ui/dialog/dialogue_box_npc.png'),
    'dialogue_box_player': pygame.image.load(BASE_IMG_PATH + 'ui/dialog/dialogue_box_player.png'),
    'cursor': pygame.image.load(BASE_IMG_PATH + 'ui/dialog/cursor.png'),

    # npc
    'old_man': pygame.image.load(BASE_IMG_PATH + 'ui/avatars/old_man.png'),
    'blacksmith': pygame.image.load(BASE_IMG_PATH + 'ui/avatars/blacksmith.png'),

    # characters
    'valkiria': pygame.image.load(BASE_IMG_PATH + 'ui/avatars/valkiria.png'),

}

UI_SET = [
    'life_full', 'life_empty', 'heart_full', 'heart_tq', 'heart_half', 'heart_quarter', 'heart_empty',
    'globe_full', 'globe_tq', 'globe_half', 'globe_quarter', 'globe_empty', 'corner_set', 'vignette',
    'diamond_icon', 'panel', 'shuriken_icon', 'player_icon', 'big_inventory_bar', 'coin_icon', 'potion_bar_frame',
    'heal_potion_icon', 'mana_potion_icon', 'stamina_potion_icon', 'power_potion_icon', 'antidote_icon',
    'defense_potion_icon',
    'corrupted_icon', 'double_power_icon', 'super_speed_icon', 'bloodlust_icon', 'invulnerability_icon',
    'enhanced_protection_icon',
    'scroll_slot', 'hud_bg', 'xp_bar', 'spell_bar',
    'fire_totem_icon', 'watergeyser_icon', 'ice_arrow_icon', 'tornado_icon', 'runic_obelisk_icon', 'magic_shield_icon',
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
    'toxic': (127, 255, 0, 150),
    'ice': (173, 216, 230)
}

HEALTH_BARS = {
    0: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/0.png'),
    1: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/1.png'),
    2: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/2.png'),
    3: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/3.png'),
    4: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/4.png'),
    5: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/5.png'),
    6: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/6.png'),
    7: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/7.png'),
    8: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/8.png'),
    9: pygame.image.load(BASE_IMG_PATH + 'ui/mob_health_bar/9.png'),
}

PROJECTILE_DAMAGE = {
    'AnimatedFireball': 33,
    'WormFireball': 49,
    'SkullSmoke': 0,  # doesn't cause damage directly
    'ToxicExplosion': 1,
    'DaemonBreath': 1,
    'DaemonBreathFlip': 1,
    'DaemonFireBreath': 1,
    'DaemonFireBreathFlip': 1,
    'GroundFlame': 1,
    'EarthStrike': 1,
}

SHURIKEN_LEVELS = {
    0: 'rusty',
    1: 'steel',
    2: 'ice',
    3: 'emerald',
    4: 'poisoned',
    5: 'stinger',
    6: 'piranha',
    7: 'supersonic',
    8: 'phantom',
    9: 'double_bladed',
}

SHURIKEN_CONFIGS = {
    'rusty': {'image': 'rusty_shuriken', 'damage': 30, 'speed': 4},
    'steel': {'image': 'steel_shuriken', 'damage': 40, 'speed': 3, 'max_distance': 400},
    'ice': {'image': 'ice_shuriken', 'damage': 50, 'speed': 5, 'max_distance': 380},
    'emerald': {'image': 'emerald_shuriken', 'damage': 60, 'speed': 4, 'max_distance': 380},
    'poisoned': {'image': 'poisoned_shuriken', 'damage': 75, 'speed': 3, 'max_distance': 380},
    'stinger': {'image': 'stinger_shuriken', 'damage': 90, 'speed': 6, 'max_distance': 420},
    'piranha': {'image': 'shuriken_piranha', 'damage': 100, 'speed': 3, 'max_distance': 400},
    'supersonic': {'image': 'supersonic_shuriken', 'damage': 120, 'speed': 7, 'max_distance': 600},
    'phantom': {'image': 'phantom_shuriken', 'damage': 150, 'speed': 2, 'max_distance': 500},
    'double_bladed': {'image': 'double_bladed_shuriken', 'damage': 220, 'speed': 3, 'max_distance': 300},
}

EXP_POINTS = {
    'orc_archer': 10,
    'big_zombie': 30,
    'big_daemon': 50,
    'fire_worm': 100,
    'golem': 150,
    'supreme_daemon': 400,
}


def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


EQUIPMENTS_CATEGORIES = load_data('data/objects/equipment_categories.json')

EQUIPMENT = load_data('data/objects/equipment.json')

BOOKS = load_data('data/objects/books.json')

SKILLS = load_data('data/objects/skills.json')

NPC_DATA = load_data('data/objects/npc_data.json')
