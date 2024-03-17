import pygame

from support import load_image, load_images, load_images_entities
from support import BASE_IMG_PATH, Animation


def load_assets():
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
                   'switch', 'select', 'use_potion', 'suriken_rebound',
                   'flipping_scroll1', 'flipping_scroll2', 'flipping_scroll3',
                   'green_smoke', 'corruption',
                   'holly_spell', 'speed_spell', 'bloodlust_spell', 'invulnerability_spell',
                   'holly_scroll', 'bloodlust_scroll', 'speed_scroll', 'invulnerability_scroll',
                   'heal', 'healed', 'cough', 'tired', 'revive',
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

DEFAULT_EQUIPMENT = {
    "Squire's armor": {
        "name": "Squire's armor",
        "e_type": "body_armor",
        "e_class": 0,
        "rarity": "Common",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/body_armor.png',
        "price": 40,
        "properties": {
            'defence': 1,
        }
    },
    "Squire's helmet": {
        "name": "Squire's helmet",
        "e_type": "head_protection",
        "e_class": 0,
        "rarity": "Common",
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/helmet.png',
        "price": 30,
        "properties": {
            'defence': 1,
        }
    },
    "Tanned swordsman belt": {
        "name": "Tanned swordsman belt",
        "e_type": "belt",
        "e_class": 0,
        "rarity": "Common",
        "condition": 500,
        "pic": BASE_IMG_PATH + 'ui/equipment/belt.png',
        "price": 20,
        "properties": {
            'defence': 1,
        }
    },
    "Hunting Gloves": {
        "name": "Hunting Gloves",
        "e_type": "gloves",
        "e_class": 0,
        "rarity": "Common",
        "condition": 500,
        "pic": BASE_IMG_PATH + 'ui/equipment/gloves.png',
        "price": 20,
        "properties": {
            'defence': 1,
        }
    },
    "Knight's leggings": {
        "name": "Knight's leggings",
        "e_type": "pants",
        "e_class": 0,
        "rarity": "Common",
        "condition": 500,
        "pic": BASE_IMG_PATH + 'ui/equipment/pants.png',
        "price": 20,
        "properties": {
            'defence': 1,
        }
    },
    "Boots of nobles": {
        "name": "Boots of nobles",
        "e_type": "boots",
        "e_class": 0,
        "rarity": "Rare",
        "condition": 600,
        "pic": BASE_IMG_PATH + 'ui/equipment/boots.png',
        "price": 20,
        "properties": {
            'defence': 1,
            'stamina': 5,
        }
    },
    "Stone Defender Amulet": {
        "name": "Stone Defender Amulet",
        "e_type": "amulet",
        "e_class": 0,
        "rarity": "Unique",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/amulet.png',
        "price": 100,
        "properties": {
            'health': 1,
            'mana': 1,
        }
    },
    "The Ring of Darkness": {
        "name": "The Ring of Darkness",
        "e_type": "ring",
        "e_class": 0,
        "rarity": "Mythical",
        "condition": 1000000,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring.png',
        "price": 1000,
        "properties": {
            'defence': 3,
            'damage': 3,
            'health': 5,
            'stamina': 5,
            'mana': 5,
            'experience': 5
        }
    },
    "Executioner's Sword": {
        "name": "Executioner's Sword",
        "e_type": "melee",
        "e_class": 0,
        "rarity": "Epic",
        "condition": 5000,
        "pic": BASE_IMG_PATH + 'ui/equipment/executioner_sword.png',
        "price": 300,
        "properties": {
            'damage': 5
        }
    },
    "A Forgotten Master's Bow": {
        "name": "A Forgotten Master's Bow",
        "e_type": "long_rage_weapon",
        "e_class": 0,
        "rarity": "Legendary",
        "condition": 10000,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_masters_bow.png',
        "price": 700,
        "properties": {
            'distance_damage': 10,
            'experience': 1
        }
    }
}

player_equipments = {
    'Common': [
        "Legionnaire's Helmet", "Warrior's Helmet", "Abandoned Knight's Tophelm", "Hunter's Whispering Hood",
        "Fallen Legionnaires Armor", "Great Fire Armor", "Invincible Archer's Cape", "Spellcaster's Robe",
        "Warlord's Bracelets", "Warrior's Gauntlets", "Magical Cuffs",
    ],
    'Rare': [
        "Paladin's Helmet", "Blood Warrior's Helmet", "Forgotten King's Mage Helmet", "Archer's Star Crown",
        "Divine Warrior’s Armor", "Forgotten Legionnaire's Armor", "Stone Guardians Armor", "Witch Lord's Cloak",
        "Leviathan's Defender Gloves", "Invisible Archer's Gloves", "Witch Archer's Gloves",
    ],
    'Unique': [
        "Stone Columns Helmet", "Leviathan King's Helmet", "Moonwatcher's glengarry", "Mighty Magician's Hood",
        "Holy Knight's Armor", "Shadow Chainmail", "Leviathan Archer's Cape", "Witcher's Cuirass",
        "Desert Fires Gauntlets", "Moon Archer's Gloves",
    ],
    'Epic': [
        "Dragon Guardian Helmet", "Witches' Mantilla of Anturium", "Archangel's Hope Tiara",
        "Leviathan Conqueror Chainmail", "Moon Defender's Armor", "Scriptologist's Robe",
        "Dragon Warrior's Bracelets", "Mystery Archer's Gloves"
    ],
    'Legendary': [
        "Supreme Liberator's Helmet", "Mighty Mage's Capyrot",
        "Dragon Guard Armor", "Magic and Mysticism Robe",
        "Fire Lord's Gloves"
    ],
    'Mythical': [
        "Great Fire Conqueror's Helmet",
        "Armor of the Immortals",
        "Dragon Mage Lord's Gloves"
    ]
}

EQUIPMENT = {
    # helmets __________ 18 items --------------------
    "Legionnaire's Helmet": {
        "name": "Legionnaire's Helmet",
        "e_type": "head_protection",
        "e_class": 1,
        "rarity": "Common",
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/legionnaires_helmet.png',
        "price": 20,
        "properties": {
            'defence': 2,
        }
    },
    "Warrior's Helmet": {
        "name": "Warrior's Helmet",
        "e_type": "head_protection",
        "e_class": 1,
        "rarity": "Common",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/warriors_helmet.png',
        "price": 25,
        "properties": {
            'defence': 1,
            'damage': 1
        }
    },
    "Abandoned Knight's Tophelm": {
        "name": "Abandoned Knight's Tophelm",
        "e_type": "head_protection",
        "e_class": 1,
        "rarity": "Common",
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/abandoned_knights_tophelm.png',
        "price": 30,
        "properties": {
            'defence': 1,
        }
    },
    "Hunter's Whispering Hood": {
        "name": "Hunter's Whispering Hood",
        "e_type": "head_protection",
        "e_class": 1,
        "rarity": "Common",
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/hunters_whispering_hood.png',
        "price": 40,
        "properties": {
            'defence': 1,
            'stamina': 1,
        }
    },
    "Paladin's Helmet": {
        "name": "Paladin's Helmet",
        "e_type": "head_protection",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1200,
        "pic": BASE_IMG_PATH + 'ui/equipment/paladins_helmet.png',
        "price": 80,
        "properties": {
            'defence': 2,
            'health': 5,
        }
    },
    "Blood Warrior's Helmet": {
        "name": "Blood Warrior's Helmet",
        "e_type": "head_protection",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1200,
        "pic": BASE_IMG_PATH + 'ui/equipment/blood_warriors_helmet.png',
        "price": 100,
        "properties": {
            'defence': 2,
            'damage': 1,
        }
    },
    "Forgotten King's Mage Helmet": {
        "name": "Forgotten King's Mage Helmet",
        "e_type": "head_protection",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_kings_mage_helmet.png',
        "price": 95,
        "properties": {
            'defence': 2,
            'mana': 5,
        }
    },
    "Archer's Star Crown": {
        "name": "Archer's Star Crown",
        "e_type": "head_protection",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/archers_star_crown.png',
        "price": 85,
        "properties": {
            'defence': 2,
            'stamina': 5,
        }
    },
    "Stone Columns Helmet": {
        "name": "Stone Columns Helmet",
        "e_type": "head_protection",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/stone_columns_helmet.png',
        "price": 120,
        "properties": {
            'defence': 4,
        }
    },
    "Leviathan King's Helmet": {
        "name": "Leviathan King's Helmet",
        "e_type": "head_protection",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathan_kings_helmet.png',
        "price": 140,
        "properties": {
            'defence': 3,
            'damage': 1,
        }
    },
    "Moonwatcher's glengarry": {
        "name": "Moonwatcher's glengarry",
        "e_type": "head_protection",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 1300,
        "pic": BASE_IMG_PATH + 'ui/equipment/moonwatchers_glengarry.png',
        "price": 135,
        "properties": {
            'defence': 2,
            'stamina': 5,
            'distance_damage': 5
        }
    },
    "Mighty Magician's Hood": {
        "name": "Mighty Magician's Hood",
        "e_type": "head_protection",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 1200,
        "pic": BASE_IMG_PATH + 'ui/equipment/mighty_magicians_hood.png',
        "price": 125,
        "properties": {
            'defence': 1,
            'health': 5,
            'mana': 10,
        }
    },
    "Dragon Guardian Helmet": {
        "name": "Dragon Guardian Helmet",
        "e_type": "head_protection",
        "e_class": 4,
        "rarity": "Epic",
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_guardian_helmet.png',
        "price": 180,
        "properties": {
            'defence': 4,
            'damage': 2,
            'health': 10,
        }
    },
    "Witches' Mantilla of Anturium": {
        "name": "Witches' Mantilla of Anturium",
        "e_type": "head_protection",
        "e_class": 4,
        "rarity": "Epic",
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/witches_mantilla_of_anturium.png',
        "price": 200,
        "properties": {
            'defence': 4,
            'damage': 2,
            'mana': 10,
        }
    },
    "Archangel's Hope Tiara": {
        "name": "Archangel's Hope Tiara",
        "e_type": "head_protection",
        "e_class": 4,
        "rarity": "Epic",
        "condition": 1800,
        "pic": BASE_IMG_PATH + 'ui/equipment/archangels_hope_tiara.png',
        "price": 210,
        "properties": {
            'defence': 4,
            'health': 10,
            'stamina': 10,
        }
    },
    "Supreme Liberator's Helmet": {
        "name": "Supreme Liberator's Helmet",
        "e_type": "head_protection",
        "e_class": 5,
        "rarity": "Legendary",
        "condition": 3000,
        "pic": BASE_IMG_PATH + 'ui/equipment/supreme_liberators_helmet.png',
        "price": 320,
        "properties": {
            'defence': 5,
            'damage': 3,
            'health': 10,
            'stamina': 10,
        }
    },
    "Mighty Mage's Capyrot": {
        "name": "Mighty Mage's Capyrot",
        "e_type": "head_protection",
        "e_class": 5,
        "rarity": "Legendary",
        "condition": 2200,
        "pic": BASE_IMG_PATH + 'ui/equipment/mighty_mages_capyrot.png',
        "price": 350,
        "properties": {
            'defence': 5,
            'health': 10,
            'mana': 10,
            'distance_damage': 5
        }
    },
    "Great Fire Conqueror's Helmet": {
        "name": "Great Fire Conqueror's Helmet",
        "e_type": "head_protection",
        "e_class": 6,
        "rarity": "Mythical",
        "condition": 5000,
        "pic": BASE_IMG_PATH + 'ui/equipment/great_fire_conquerors_helmet.png',
        "price": 500,
        "properties": {
            'defence': 7,
            'damage': 2,
            'health': 5,
            'stamina': 5,
            'mana': 5,
            'experience': 1,
        },
    },
    # body armor ________________ 18 items _______________________
    "Fallen Legionnaires Armor": {
        "name": "Fallen Legionnaires' Armor",
        "e_type": "body_armor",
        "e_class": 1,
        "rarity": "Common",
        "condition": 1200,
        "pic": BASE_IMG_PATH + 'ui/equipment/fallen_legionnaires_armor.png',
        "price": 40,
        "properties": {
            'defence': 2,
        }
    },
    "Great Fire Armor": {
        "name": "Great Fire Armor",
        "e_type": "body_armor",
        "e_class": 1,
        "rarity": "Common",
        "condition": 1300,
        "pic": BASE_IMG_PATH + 'ui/equipment/great_fire_armor.png',
        "price": 45,
        "properties": {
            'defence': 1,
            'damage': 1,
        }
    },
    "Invincible Archer's Cape": {
        "name": "Invincible Archer's Cape",
        "e_type": "body_armor",
        "e_class": 1,
        "rarity": "Common",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/invincible_archers_cape.png',
        "price": 40,
        "properties": {
            'defence': 1,
            'stamina': 5,
        }
    },
    "Spellcaster's Robe": {
        "name": "Spellcaster's Robe",
        "e_type": "body_armor",
        "e_class": 1,
        "rarity": "Common",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/spellcasters_robe.png',
        "price": 50,
        "properties": {
            'defence': 1,
            'mana': 5,
        }
    },
    "Divine Warrior’s Armor": {
        "name": "Divine Warrior’s Armor",
        "e_type": "body_armor",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/divine_warriors_armor.png',
        "price": 100,
        "properties": {
            'defence': 2,
            'health': 5,
        }
    },
    "Forgotten Legionnaire's Armor": {
        "name": "Forgotten Legionnaire's Armor",
        "e_type": "body_armor",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_legionnaires_armor.png',
        "price": 110,
        "properties": {
            'defence': 3,
        }
    },
    "Stone Guardians Armor": {
        "name": "Stone Guardians Armor",
        "e_type": "body_armor",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1600,
        "pic": BASE_IMG_PATH + 'ui/equipment/stone_guardians_armor.png',
        "price": 115,
        "properties": {
            'defence': 3,
        }
    },
    "Witch Lord's Cloak": {
        "name": "Witch Lord's Cloak",
        "e_type": "body_armor",
        "e_class": 2,
        "rarity": "Rare",
        "condition": 1200,
        "pic": BASE_IMG_PATH + 'ui/equipment/witch_lords_cloak.png',
        "price": 110,
        "properties": {
            'defence': 1,
            'stamina': 5,
            'mana': 10,
        }
    },
    "Holy Knight's Armor": {
        "name": "Holy Knight's Armor",
        "e_type": "body_armor",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/holy_knights_armor.png',
        "price": 130,
        "properties": {
            'defence': 3,
            'health': 10,
        }
    },
    "Shadow Chainmail": {
        "name": "Shadow Chainmail",
        "e_type": "body_armor",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/shadow_chainmail.png',
        "price": 140,
        "properties": {
            'defence': 2,
            'distance_damage': 2,
            'stamina': 10,
        }
    },
    "Leviathan Archer's Cape": {
        "name": "Leviathan Archer's Cape",
        "e_type": "body_armor",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 1600,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathan_archers_cape.png',
        "price": 145,
        "properties": {
            'defence': 4,
        }
    },
    "Witcher's Cuirass": {
        "name": "Witcher's Cuirass",
        "e_type": "body_armor",
        "e_class": 3,
        "rarity": "Unique",
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/witchers_cuirass.png',
        "price": 140,
        "properties": {
            'defence': 2,
            'stamina': 10,
            'mana': 5,
        }
    },
    "Leviathan Conqueror Chainmail": {
        "name": "Leviathan Conqueror Chainmail",
        "e_type": "body_armor",
        "e_class": 4,
        "rarity": "Epic",
        "condition": 2500,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathan_conqueror_chainmail.png',
        "price": 200,
        "properties": {
            'defence': 5,
            'stamina': 10,
        }
    },
    "Moon Defender's Armor": {
        "name": "Moon Defender's Armor",
        "e_type": "body_armor",
        "e_class": 4,
        "rarity": "Epic",
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_defenders_armor.png',
        "price": 220,
        "properties": {
            'defence': 3,
            'distance_damage': 5,
            'health': 10,
            'stamina': 10,
        }
    },
    "Scriptologist's Robe": {
        "name": "Scriptologist's Robe",
        "e_type": "body_armor",
        "e_class": 4,
        "rarity": "Epic",
        "condition": 2200,
        "pic": BASE_IMG_PATH + 'ui/equipment/scriptologists_robe.png',
        "price": 225,
        "properties": {
            'defence': 3,
            'health': 10,
            'stamina': 10,
            'mana': 10,

        }
    },
    "Dragon Guard Armor": {
        "name": "Dragon Guard Armor",
        "e_type": "body_armor",
        "e_class": 5,
        "rarity": "Legendary",
        "condition": 4000,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_guard_armor.png',
        "price": 400,
        "properties": {
            'defence': 7,
            'health': 10,
            'stamina': 10,
        }
    },
    "Magic and Mysticism Robe": {
        "name": "Magic and Mysticism Robe",
        "e_type": "body_armor",
        "e_class": 5,
        "rarity": "Legendary",
        "condition": 3000,
        "pic": BASE_IMG_PATH + 'ui/equipment/magic_mysticism_robe.png',
        "price": 420,
        "properties": {
            'defence': 5,
            'health': 10,
            'stamina': 10,
            'mana': 20,
        }
    },
    "Armor of the Immortals": {
        "name": "Armor of the Immortals",
        "e_type": "body_armor",
        "e_class": 6,
        "rarity": "Mythical",
        "condition": 10000,
        "pic": BASE_IMG_PATH + 'ui/equipment/armor_immortals.png',
        "price": 700,
        "properties": {
            'defence': 10,
            'damage': 2,
            'health': 20,
            'stamina': 20,
            'mana': 10,
            'experience': 2
        }
    },
    # gloves  ------------ 12 items --------------------
    "Warlord's Bracelets": {
        "name": "Warlord's Bracelets",
        "e_type": "gloves",
        "rarity": "Common",
        "e_class": 1,
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/warlords_bracelets.png',
        "price": 10,
        "properties": {
            'defence': 1,
        }
    },
    "Warrior's Gauntlets": {
        "name": "Warrior's Gauntlets",
        "e_type": "gloves",
        "rarity": "Common",
        "e_class": 1,
        "condition": 900,
        "pic": BASE_IMG_PATH + 'ui/equipment/warriors_gauntlets.png',
        "price": 20,
        "properties": {
            'defence': 1,
            'health': 5,
        }
    },
    "Magical Cuffs": {
        "name": "Magical Cuffs",
        "e_type": "gloves",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/magical_cuffs.png',
        "price": 25,
        "properties": {
            'defence': 1,
            'mana': 5,
        }
    },
    "Leviathan's Defender Gloves": {
        "name": "Leviathan's Defender Gloves",
        "e_type": "gloves",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathans_defender_gloves.png',
        "price": 50,
        "properties": {
            'defence': 2,
        }
    },
    "Invisible Archer's Gloves": {
        "name": "Invisible Archer's Gloves",
        "e_type": "gloves",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/invisible_archers_gloves.png',
        "price": 75,
        "properties": {
            'defence': 2,
            'stamina': 5,
        }
    },
    "Witch Archer's Gloves": {
        "name": "Witch Archer's Gloves",
        "e_type": "gloves",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/witch_archers_gloves.png',
        "price": 80,
        "properties": {
            'defence': 2,
            'mana': 5,
        }
    },
    "Desert Fires Gauntlets": {
        "name": "Desert Fires Gauntlets",
        "e_type": "gloves",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/desert_fires_gauntlets.png',
        "price": 100,
        "properties": {
            'defence': 2,
            'health': 5,
            'stamina': 5,
        }
    },
    "Moon Archer's Gloves": {
        "name": "Moon Archer's Gloves",
        "e_type": "gloves",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_archers_gloves.png',
        "price": 110,
        "properties": {
            'defence': 2,
            'stamina': 10,
        }
    },
    "Dragon Warrior's Bracelets": {
        "name": "Dragon Warrior's Bracelets",
        "e_type": "gloves",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2300,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_warriors_bracelets.png',
        "price": 150,
        "properties": {
            'defence': 3,
            'health': 10,
            'stamina': 10,
        }
    },
    "Mystery Archer's Gloves": {
        "name": "Mystery Archer's Gloves",
        "e_type": "gloves",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/mystery_archers_gloves.png',
        "price": 175,
        "properties": {
            'defence': 3,
            'stamina': 10,
            'distance_damage': 5
        }
    },
    "Fire Lord's Gloves": {
        "name": "Fire Lord's Gloves",
        "e_type": "gloves",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 3000,
        "pic": BASE_IMG_PATH + 'ui/equipment/fire_lords_gloves.png',
        "price": 250,
        "properties": {
            'defence': 5,
            'distance_damage': 5
        }
    },
    "Dragon Mage Lord's Gloves": {
        "name": "Dragon Mage Lord's Gloves",
        "e_type": "gloves",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 6000,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_mage_lords_gloves.png',
        "price": 500,
        "properties": {
            'defence': 5,
            'health': 5,
            'stamina': 5,
            'mana': 5,
            'experience': 1,
            'distance_damage': 5
        }
    }
}
