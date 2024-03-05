import pygame

from support import load_image, load_images, load_images_entities
from support import Animation


def load_assets():
    return {
        # levels background
        'background': load_images('background'),

        # projectiles and weapons
        'bow': load_image('weapons/bow.png'),
        'projectile': load_image('weapons/arrow.png'),
        'arrow': load_image('weapons/arrow.png'),
        'suriken': load_image('weapons/suriken.png'),

        # anamated projectiles
        'fireball': load_images('particles/fireball'),
        'skullsmoke': load_images('particles/skullmoke'),

        # spells
        'holly_spell': load_images('particles/spell/holly_spell'),
        'speed_spell': load_images('particles/spell/speed_spell'),
        'bloodlust_spell': load_images('particles/spell/bloodlust_spell'),
        'invulnerability_spell': load_images('particles/spell/invulnerability_spell'),
        'blood': load_images('particles/spell/blood'),

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
        'orc_archer/idle': Animation(load_images_entities('entities/enemy/orc_archer/idle', trim_left=0, trim_right=0, scale_factor=1.25), img_dur=6),
        'orc_archer/run': Animation(load_images_entities('entities/enemy/orc_archer/run', trim_left=0, trim_right=0, scale_factor=1.25), img_dur=4),

        'big_zombie/idle': Animation(load_images_entities('entities/enemy/big_zombie/idle', trim_left=0, trim_right=0, scale_factor=1), img_dur=6),
        'big_zombie/run': Animation(load_images_entities('entities/enemy/big_zombie/run', trim_left=0, trim_right=0, scale_factor=1), img_dur=4),

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
        'player/wall_slide': Animation(load_images_entities('entities/player/wall_slide', trim_left=0, trim_right=0), img_dur=3),
        'player/death': Animation(load_images_entities('entities/player/death', trim_left=0, trim_right=0), img_dur=6),


        # game
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
        'loot_spawn': load_images('tiles/loot_spawn/'),

        # particle
        'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),

        # effects
        'kaboom': load_images('particles/kaboom'),
    }


def load_sfx():
    sound_names = ['jump', 'jump1', 'jump2', 'jump3', 'dash', 'hit', 'shoot', 'arrow_crash', 'ambience',
                   'attack', 'attack1', 'attack2', 'attack3', 'pain', 'damaged1', 'damaged2', 'damaged3', 'running',
                   'orc_archer', 'big_zombie', 'big_daemon',
                   'fireball', 'fire_hit', 'fire_punch',
                   'coin', 'gem', 'glass_red', 'glass_blue', 'glass_green', 'glass_yellow', 'level_up',
                   'switch', 'select', 'use_potion', 'suriken_rebound', 'green_smoke', 'corruption',
                   'holly_spell', 'speed_spell', 'bloodlust_spell', 'invulnerability_spell',
                   'holly_scroll', 'bloodlust_scroll', 'speed_scroll', 'invulnerability_scroll',
                   'heal', 'healed', 'cough', 'tired',
                   'move_cursor', 'open_skill', 'rejected']

    return {name: pygame.mixer.Sound(f'data/sfx/{name}.wav') for name in sound_names}


color_schema = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'big_daemon': (255, 69, 0),
    'big_zombie': (127, 255, 0),
    'orc_archer': (255, 0, 0),
    'fireball': (255, 140, 0),
    'toxic': (127, 255, 0, 150)
}


experience_points = {
    'big_daemon': 50,
    'big_zombie': 30,
    'orc_archer': 10,
}
