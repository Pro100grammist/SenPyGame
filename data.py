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
                   'switch', 'select', 'use_potion', 'suriken_rebound', 'locked',
                   'flipping_scroll1', 'flipping_scroll2', 'flipping_scroll3',
                   'green_smoke', 'corruption',
                   'holly_spell', 'speed_spell', 'bloodlust_spell', 'invulnerability_spell',
                   'holly_scroll', 'bloodlust_scroll', 'speed_scroll', 'invulnerability_scroll',
                   'heal', 'healed', 'cough', 'tired', 'revive',
                   'move_cursor', 'open_skill', 'rejected', 'chest_open',
                   'steel_key', 'red_key', 'bronze_key', 'purple_key', 'gold_key',]

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
        'Fallen Legionnaires Armor', 'Great Fire Armor', "Invincible Archer's Cape", "Spellcaster's Robe",
        "Warlord's Bracelets", "Warrior's Gauntlets", 'Magical Cuffs',
        'Hunting Boots', "Forgotten Legionnaire's Boots", 'Boots of the Light Mage',
        'Armored Scabbard', 'Embroidered Pants', 'Light Archer Leggings',
        'Light Belt', 'Combat Belt', 'Armored Belt', 'Light Hunting Belt',
        "Battle Winner's Ring", 'Ring of Strength', 'Ring of Vitality', 'Ring of Agility',
        "Moon Magician's Amulet", 'Light Warrior Amulet',
        'Light Katana', 'Short Sword', "Forgotten Hero's Dagger",
        'Hunting Bow', "Legionnaire's bow", 'Knife of the Ruthless Killer', 'Boomerang'
    ],

    'Rare': [
        "Paladin's Helmet", "Blood Warrior's Helmet", "Forgotten King's Mage Helmet", "Archer's Star Crown",
        'Divine Warrior’s Armor', "Forgotten Legionnaire's Armor", 'Stone Guardians Armor', "Witch Lord's Cloak",
        "Leviathan's Defender Gloves", "Invisible Archer's Gloves", "Witch Archer's Gloves",
        'Leviathan Defender Boots', 'Stone Guardian Boots', 'Invincible Archer Boots',
        'Leviathan Defender Breeches', 'Fireproof Pants', "Forgotten Legionnaire's Scabbard",
        'Invincible Warrior Belt', 'Leviathan Defender Belt', "Forgotten Legionnaire's Belt",
        'Ring of Wisdom', 'Ring of Endurance', "Forgotten Legionnaire's Ring", 'Invincible Warrior Ring',
        "Amulet Witch's Eye", "Winning archer's amulet",
        "Assassin's Sting", "Ruthless Warrior's Sword", 'Battle Flamberg', 'Axe of the Victorious',
        "Forgotten Master's Bow", "Legendary Archer's Bow", 'Sacrificial Knives', "Firefighter's Crossbow"
    ],

    'Unique': [
        'Stone Columns Helmet', "Leviathan King's Helmet", "Moonwatcher's glengarry", "Mighty Magician's Hood",
        "Holy Knight's Armor", 'Shadow Chainmail', "Leviathan Archer's Cape", "Witcher's Cuirass",
        'Desert Fires Gauntlets', "Moon Archer's Gloves",
        'Invincible Warrior Boots', 'Boots of the Moon Archer',
        'Stone Guardian Scabbard', 'Invincible Warrior Pants',
        'Moon Chest Belt', 'Stone Guardian Belt', "Legendary Archer's Belt",
        'Ring of Precision', 'Ring of Arcana', 'Leviathan Defender Ring', "Stone Guardian's Ring",
        'Mage warrior amulet', "Leviathan's guardian amulet",
        "Leviathan's cutter", "Beastmaster's great hammer", 'Blade of Lightning',
        "Firebender's Bow", 'Legendary Sniper Crossbow', 'Shadow Masters Shuriken', 'Forged Dragon Crossbow'
    ],

    'Epic': [
        'Dragon Guardian Helmet', "Witches' Mantilla of Anturium", "Archangel's Hope Tiara",
        'Leviathan Conqueror Chainmail', "Moon Defender's Armor", "Scriptologist's Robe",
        "Dragon Warrior's Bracelets", "Mystery Archer's Gloves",
        "Fire Lord's Magical Boots", 'Moon Magic Boots',
        "Moon Archer's Kneeguards", 'Dragon Warrior Breeches',
        "Moon Magician's Belt", "Fire Lord's Belt",
        'Ring of Power', 'Magic Fire Ring', "Light Defender's Ring",
        'Stone Guardian Amulet', "Fire Lord's Amulet",
        'Gladius of the Stone Guardian', 'Legendary Battle Axe', 'Ebonite Rapier',
        'Crystal Bow', "Dragon's Wrath Bow", 'Wind Lord Shuriken'
    ],

    'Legendary': [
        "Supreme Liberator's Helmet", "Mighty Mage's Capyrot",
        'Dragon Guard Armor', 'Magic and Mysticism Robe',
        "Fire Lord's Gloves",
        'Dragon Warrior Boots', 'Arcanical Boots',
        "Arcanic Witcher's Knee Pads",
        'Dragon Warrior Belt', "Arcane Wizard's Belt",
        "Moon Mage's Ring", 'Ring of Immortality', 'Dragon Warrior Ring',
        'Dragon Guardian Amulet',
        'Blade of Dragons', 'Arcanic two-handed sword', 'Crystal Sword',
        'Dragon Slayer', 'Magic Crossbow'
    ],

    'Mythical': [
        "Great Fire Conqueror's Helmet",
        'Armor of the Immortals',
        "Dragon Mage Lord's Gloves",
        "Mythical Wizard's Boots",
        'Kilt of the Immortals',
        'Immortality Belt',
        "Darkness Spellcaster's Ring",
        'Amulet of immortality',
        "Titan's Thunderbolt", 'The Soul Ripper',
        'Wind conqueror', 'Whisper of death'
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
    },

    # boots  ------------ 13 items --------------------
    "Hunting Boots": {
        "name": "Hunting Boots",
        "e_type": "boots",
        "rarity": "Common",
        "e_class": 1,
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/hunting_boots.png',
        "price": 20,
        "properties": {
            'stamina': 10,
        }
    },
    "Forgotten Legionnaire's Boots": {
        "name": "Forgotten Legionnaire's Boots",
        "e_type": "boots",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_legionnaires_boots.png',
        "price": 25,
        "properties": {
            'defence': 1,
        }
    },
    "Boots of the Light Mage": {
        "name": "Boots of the Light Mage",
        "e_type": "boots",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/boots_of_the_light_mage.png',
        "price": 30,
        "properties": {
            'mana': 5,
        }
    },
    "Leviathan Defender Boots": {
        "name": "Leviathan Defender Boots",
        "e_type": "boots",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathan_defender_boots.png',
        "price": 80,
        "properties": {
            'defence': 2,
        }
    },
    "Stone Guardian Boots": {
        "name": "Stone Guardian Boots",
        "e_type": "boots",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/stone_guardian_boots.png',
        "price": 75,
        "properties": {
            'defence': 1,
            'health': 5,
        }
    },
    "Invincible Archer Boots": {
        "name": "Invincible Archer Boots",
        "e_type": "boots",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/invincible_archer_boots.png',
        "price": 50,
        "properties": {
            'defence': 1,
            'stamina': 5,
        }
    },
    "Invincible Warrior Boots": {
        "name": "Invincible Warrior Boots",
        "e_type": "boots",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/invincible_warrior_boots.png',
        "price": 120,
        "properties": {
            'defence': 3,
            'health': 5,
        }
    },
    "Boots of the Moon Archer": {
        "name": "Boots of the Moon Archer",
        "e_type": "boots",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1200,
        "pic": BASE_IMG_PATH + 'ui/equipment/boots_of_the_moon_archer.png',
        "price": 125,
        "properties": {
            'defence': 3,
            'stamina': 5,
        }
    },
    "Fire Lord's Magical Boots": {
        "name": "Fire Lord's Magical Boots",
        "e_type": "boots",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/fire_lords_magical_boots.png',
        "price": 200,
        "properties": {
            'defence': 3,
            'mana': 10,
        }
    },
    "Moon Magic Boots": {
        "name": "Moon Magic Boots",
        "e_type": "boots",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 1800,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_magic_boots.png',
        "price": 190,
        "properties": {
            'defence': 3,
            'health': 5,
            'mana': 5,
        }
    },
    "Dragon Warrior Boots": {
        "name": "Dragon Warrior Boots",
        "e_type": "boots",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2800,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_warrior_boots.png',
        "price": 240,
        "properties": {
            'defence': 5,
            'health': 10,
        }
    },
    "Arcanical Boots": {
        "name": "Arcanical Boots",
        "e_type": "boots",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2600,
        "pic": BASE_IMG_PATH + 'ui/equipment/arcanical_boots.png',
        "price": 250,
        "properties": {
            'defence': 5,
            'mana': 10,
        }
    },
    "Mythical Wizard's Boots": {
        "name": "Mythical Wizard's Boots",
        "e_type": "boots",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 5500,
        "pic": BASE_IMG_PATH + 'ui/equipment/mythical_wizards_boots.png',
        "price": 450,
        "properties": {
            'defence': 6,
            'health': 5,
            'stamina': 5,
            'mana': 5,
            'experience': 1,
        }
    },

    # pants  ------------ 12 items --------------------
    "Armored Scabbard": {
        "name": "Armored Scabbard",
        "e_type": "pants",
        "rarity": "Common",
        "e_class": 1,
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/armored_scabbard.png',
        "price": 15,
        "properties": {
            'defence': 1,
        }
    },
    "Embroidered Pants": {
        "name": "Embroidered Pants",
        "e_type": "pants",
        "rarity": "Common",
        "e_class": 1,
        "condition": 600,
        "pic": BASE_IMG_PATH + 'ui/equipment/embroidered_pants.png',
        "price": 25,
        "properties": {
            'mana': 5,
        }
    },
    "Light Archer Leggings": {
        "name": "Light Archer Leggings",
        "e_type": "pants",
        "rarity": "Common",
        "e_class": 1,
        "condition": 700,
        "pic": BASE_IMG_PATH + 'ui/equipment/light_archer_leggings.png',
        "price": 15,
        "properties": {
            'stamina': 5,
        }
    },
    "Leviathan Defender Breeches": {
        "name": "Leviathan Defender Breeches",
        "e_type": "pants",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathan_defender_breeches.png',
        "price": 50,
        "properties": {
            'defence': 2,
        }
    },
    "Fireproof Pants": {
        "name": "Fireproof Pants",
        "e_type": "pants",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/fireproof_pants.png',
        "price": 45,
        "properties": {
            'defence': 1,
            'health': 5,
        }
    },
    "Forgotten Legionnaire's Scabbard": {
        "name": "Forgotten Legionnaire's Scabbard",
        "e_type": "pants",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1200,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_legionnaires_scabbard.png',
        "price": 50,
        "properties": {
            'defence': 1,
            'mana': 5,
        }
    },
    "Stone Guardian Scabbard": {
        "name": "Stone Guardian Scabbard",
        "e_type": "pants",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1300,
        "pic": BASE_IMG_PATH + 'ui/equipment/stone_guardian_scabbard.png',
        "price": 100,
        "properties": {
            'defence': 3,
            'health': 5,
        }
    },
    "Invincible Warrior Pants": {
        "name": "Invincible Warrior Pants",
        "e_type": "pants",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/invincible_warrior_pants.png',
        "price": 110,
        "properties": {
            'defence': 3,
            'stamina': 5,
        }
    },
    "Moon Archer's Kneeguards": {
        "name": "Moon Archer's Kneeguards",
        "e_type": "pants",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_archers_kneeguards.png',
        "price": 150,
        "properties": {
            'defence': 4,
            'stamina': 10,
        }
    },
    "Dragon Warrior Breeches": {
        "name": "Dragon Warrior Breeches",
        "e_type": "pants",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2200,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_warrior_breeches.png',
        "price": 110,
        "properties": {
            'defence': 4,
            'health': 10,
        }
    },
    "Arcanic Witcher's Knee Pads": {
        "name": "Arcanic Witcher's Knee Pads",
        "e_type": "pants",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2800,
        "pic": BASE_IMG_PATH + 'ui/equipment/arcanic_witchers_knee_pads.png',
        "price": 200,
        "properties": {
            'defence': 5,
            'mana': 10,
        }
    },
    "Kilt of the Immortals": {
        "name": "Kilt of the Immortals",
        "e_type": "pants",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 5500,
        "pic": BASE_IMG_PATH + 'ui/equipment/kilt_of_the_immortals.png',
        "price": 450,
        "properties": {
            'defence': 6,
            'health': 5,
            'stamina': 5,
            'mana': 5,
            'experience': 1,
        }
    },

    # belt  ------------ 15 items --------------------
    "Light Belt": {
        "name": "Light Belt",
        "e_type": "belt",
        "rarity": "Common",
        "e_class": 1,
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/light_belt.png',
        "price": 15,
        "properties": {
            'defence': 1,
        }
    },
    "Combat Belt": {
        "name": "Combat Belt",
        "e_type": "belt",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/combat_belt.png',
        "price": 20,
        "properties": {
            'defence': 1,
            'health': 5,
        }
    },
    "Armored Belt": {
        "name": "Armored Belt",
        "e_type": "belt",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/armored_belt.png',
        "price": 25,
        "properties": {
            'defence': 2,
        }
    },
    "Light Hunting Belt": {
        "name": "Light Hunting Belt",
        "e_type": "belt",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/light_hunting_belt.png',
        "price": 30,
        "properties": {
            'defence': 1,
            'stamina': 5,
        }
    },
    "Invincible Warrior Belt": {
        "name": "Invincible Warrior Belt",
        "e_type": "belt",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/invincible_warrior_belt.png',
        "price": 40,
        "properties": {
            'defence': 2,
            'health': 5,
        }
    },
    "Leviathan Defender Belt": {
        "name": "Leviathan Defender Belt",
        "e_type": "belt",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathan_defender_belt.png',
        "price": 55,
        "properties": {
            'defence': 2,
            'mana': 5,
        }
    },
    "Forgotten Legionnaire's Belt": {
        "name": "Forgotten Legionnaire's Belt",
        "e_type": "belt",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_legionnaires_belt.png',
        "price": 50,
        "properties": {
            'defence': 2,
            'stamina': 5,
        }
    },
    "Moon Chest Belt": {
        "name": "Moon Chest Belt",
        "e_type": "belt",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1300,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_chest_belt.png',
        "price": 80,
        "properties": {
            'defence': 3,
            'stamina': 5,
        }
    },
    "Stone Guardian Belt": {
        "name": "Stone Guardian Belt",
        "e_type": "belt",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/stone_guardian_belt.png',
        "price": 90,
        "properties": {
            'defence': 3,
            'health': 5,
        }
    },
    "Legendary Archer's Belt": {
        "name": "Legendary Archer's Belt",
        "e_type": "belt",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/legendary_archers_belt.png',
        "price": 90,
        "properties": {
            'defence': 3,
            'distance_damage': 5,
        }
    },
    "Moon Magician's Belt": {
        "name": "Moon Magician's Belt",
        "e_type": "belt",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_magicians_belt.png',
        "price": 120,
        "properties": {
            'defence': 4,
            'mana': 10,
        }
    },
    "Fire Lord's Belt": {
        "name": "Fire Lord's Belt",
        "e_type": "belt",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 1800,
        "pic": BASE_IMG_PATH + 'ui/equipment/fire_lords_belt.png',
        "price": 110,
        "properties": {
            'defence': 4,
            'health': 5,
            'mana': 5,
        }
    },
    "Dragon Warrior Belt": {
        "name": "Dragon Warrior Belt",
        "e_type": "belt",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2800,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_warrior_belt.png',
        "price": 200,
        "properties": {
            'defence': 5,
            'health': 10,
        }
    },
    "Arcane Wizard's Belt": {
        "name": "Arcane Wizard's Belt",
        "e_type": "belt",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2600,
        "pic": BASE_IMG_PATH + 'ui/equipment/arcane_wizards_belt.png',
        "price": 190,
        "properties": {
            'defence': 5,
            'mana': 10,
        }
    },
    "Immortality Belt": {
        "name": "Immortality Belt",
        "e_type": "belt",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 5500,
        "pic": BASE_IMG_PATH + 'ui/equipment/immortality_belt.png',
        "price": 450,
        "properties": {
            'defence': 6,
            'health': 5,
            'stamina': 5,
            'mana': 5,
            'experience': 1,
        }
    },

    # ring  ------------ 19 items --------------------
    "Battle Winner's Ring": {
        "name": "Battle Winner's Ring",
        "e_type": "ring",
        "rarity": "Common",
        "e_class": 1,
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/battle_winners_ring.png',
        "price": 15,
        "properties": {
            'defence': 1,
        }
    },
    "Ring of Strength": {
        "name": "Ring of Strength",
        "e_type": "ring",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_strength.png',
        "price": 20,
        "properties": {
            'damage': 2,
        }
    },
    "Ring of Vitality": {
        "name": "Ring of Vitality",
        "e_type": "ring",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_vitality.png',
        "price": 25,
        "properties": {
            'health': 10,
        }
    },
    "Ring of Agility": {
        "name": "Ring of Agility",
        "e_type": "ring",
        "rarity": "Common",
        "e_class": 1,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_agility.png',
        "price": 40,
        "properties": {
            'stamina': 10,
        }
    },
    "Ring of Wisdom": {
        "name": "Ring of Wisdom",
        "e_type": "ring",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_wisdom.png',
        "price": 55,
        "properties": {
            'mana': 10,
        }
    },
    "Ring of Endurance": {
        "name": "Ring of Endurance",
        "e_type": "ring",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1300,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_endurance.png',
        "price": 50,
        "properties": {
            'health': 10,
        }
    },
    "Forgotten Legionnaire's Ring": {
        "name": "Forgotten Legionnaire's Ring",
        "e_type": "ring",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_legionnaires_ring.png',
        "price": 40,
        "properties": {
            'defence': 2,
            'health': 5,
        }
    },
    "Invincible Warrior Ring": {
        "name": "Invincible Warrior Ring",
        "e_type": "ring",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/invincible_warrior_ring.png',
        "price": 45,
        "properties": {
            'defence': 2,
            'damage': 5,
        }
    },
    "Ring of Precision": {
        "name": "Ring of Precision",
        "e_type": "ring",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_precision.png',
        "price": 90,
        "properties": {
            'defence': 3,
            'damage': 5,
        }
    },
    "Ring of Arcana": {
        "name": "Ring of Arcana",
        "e_type": "ring",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1600,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_arcana.png',
        "price": 120,
        "properties": {
            'defence': 5,
            'mana': 10,
        }
    },
    "Leviathan Defender Ring": {
        "name": "Leviathan Defender Ring",
        "e_type": "ring",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1300,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathan_defender_ring.png',
        "price": 80,
        "properties": {
            'defence': 3,
            'mana': 10,
        }
    },
    "Stone Guardian's Ring": {
        "name": "Stone Guardian's Ring",
        "e_type": "ring",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/stone_guardians_ring.png',
        "price": 90,
        "properties": {
            'defence': 3,
            'stamina': 10,
        }
    },
    "Ring of Power": {
        "name": "Ring of Power",
        "e_type": "ring",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2800,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_power.png',
        "price": 150,
        "properties": {
            'defence': 5,
            'damage': 5,
            'distance_damage': 10,
        }
    },
    "Magic Fire Ring": {
        "name": "Magic Fire Ring",
        "e_type": "ring",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 3000,
        "pic": BASE_IMG_PATH + 'ui/equipment/magic_fire_ring.png',
        "price": 130,
        "properties": {
            'damage': 10,
            'health': 10,
        }
    },
    "Light Defender's Ring": {
        "name": "Light Defender's Ring",
        "e_type": "ring",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2800,
        "pic": BASE_IMG_PATH + 'ui/equipment/light_defenders_ring.png',
        "price": 140,
        "properties": {
            'defence': 5,
            'mana': 10,
        }
    },
    "Moon Mage's Ring": {
        "name": "Moon Mage's Ring",
        "e_type": "ring",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2600,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_mages_ring.png',
        "price": 190,
        "properties": {
            'damage': 10,
            'mana': 10,
        }
    },
    "Ring of Immortality": {
        "name": "Ring of Immortality",
        "e_type": "ring",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 4000,
        "pic": BASE_IMG_PATH + 'ui/equipment/ring_of_immortality.png',
        "price": 300,
        "properties": {
            'defence': 5,
            'damage': 5,
            'distance_damage': 10,
            'health': 10,
        }
    },
    "Dragon Warrior Ring": {
        "name": "Dragon Warrior Ring",
        "e_type": "ring",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 4800,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_warrior_ring.png',
        "price": 300,
        "properties": {
            'defence': 5,
            'damage': 5,
            'distance_damage': 10,
            'stamina': 10,
        }
    },
    "Darkness Spellcaster's Ring": {
        "name": "Darkness Spellcaster's Ring",
        "e_type": "ring",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 5500,
        "pic": BASE_IMG_PATH + 'ui/equipment/darkness_spellcasters_ring.png',
        "price": 450,
        "properties": {
            'defence': 6,
            'damage': 5,
            'health': 10,
            'stamina': 10,
            'mana': 10,
            'experience': 2
        }
    },

    # amulet  ------------ 10 items --------------------
    "Moon Magician's Amulet": {
        "name": "Moon Magician's Amulet",
        "e_type": "amulet",
        "rarity": "Common",
        "e_class": 1,
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/moon_magicians_amulet.png',
        "price": 50,
        "properties": {
            'defence': 2,
            'mana': 5
        }
    },
    "Light Warrior Amulet": {
        "name": "Light Warrior Amulet",
        "e_type": "amulet",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/light_warrior_amulet.png',
        "price": 60,
        "properties": {
            'defence': 2,
            'health': 10
        }
    },
    "Amulet Witch's Eye": {
        "name": "Amulet Witch's Eye",
        "e_type": "amulet",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/amulet_witchs_eye.png',
        "price": 80,
        "properties": {
            'defence': 2,
            'mana': 5,
            'health': 10
        }
    },
    "Winning archer's amulet": {
        "name": "Winning archer's amulet",
        "e_type": "amulet",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/winning_archers_amulet.png',
        "price": 65,
        "properties": {
            'defence': 2,
            'stamina': 10
        }
    },
    "Mage warrior amulet": {
        "name": "Mage warrior amulet",
        "e_type": "amulet",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1300,
        "pic": BASE_IMG_PATH + 'ui/equipment/mage_warrior_amulet.png',
        "price": 80,
        "properties": {
            'defence': 3,
            'damage': 5,
            'mana': 5
        }
    },
    "Leviathan's guardian amulet": {
        "name": "Leviathan's guardian amulet",
        "e_type": "amulet",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathans_guardian_amulet.png',
        "price": 110,
        "properties": {
            'defence': 5,
            'health': 10
        }
    },
    "Stone Guardian Amulet": {
        "name": "Stone Guardian Amulet",
        "e_type": "amulet",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/stone_guardian_amulet.png',
        "price": 140,
        "properties": {
            'defence': 4,
            'damage': 5,
            'health': 5
        }
    },
    "Fire Lord's Amulet": {
        "name": "Fire Lord's Amulet",
        "e_type": "amulet",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 1800,
        "pic": BASE_IMG_PATH + 'ui/equipment/fire_lords_amulet.png',
        "price": 150,
        "properties": {
            'defence': 4,
            'mana': 5,
            'health': 5,
            'stamina': 5,
        }
    },
    "Dragon Guardian Amulet": {
        "name": "Dragon Guardian Amulet",
        "e_type": "amulet",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2800,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_guardian_amulet.png',
        "price": 200,
        "properties": {
            'defence': 5,
            'distance_damage': 5,
            'health': 20,
        }
    },
    "Amulet of immortality": {
        "name": "Amulet of immortality",
        "e_type": "amulet",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 5500,
        "pic": BASE_IMG_PATH + 'ui/equipment/amulet_of_immortality.png',
        "price": 750,
        "properties": {
            'defence': 6,
            'distance_damage': 10,
            'health': 10,
            'stamina': 10,
            'mana': 5,
            'experience': 2
        }
    },

    # melee  ------------ 18 items --------------------
    "Light Katana": {
        "name": "Light Katana",
        "e_type": "melee",
        "rarity": "Common",
        "e_class": 1,
        "condition": 750,
        "pic": BASE_IMG_PATH + 'ui/equipment/light_katana.png',
        "price": 35,
        "properties": {
            'damage': 3,
            'stamina': -5,
        }
    },
    "Short Sword": {
        "name": "Short Sword",
        "e_type": "melee",
        "rarity": "Common",
        "e_class": 1,
        "condition": 800,
        "pic": BASE_IMG_PATH + 'ui/equipment/short_sword.png',
        "price": 40,
        "properties": {
            'damage': 4,
            'stamina': -10,
        }
    },
    "Forgotten Hero's Dagger": {
        "name": "Forgotten Hero's Dagger",
        "e_type": "melee",
        "rarity": "Common",
        "e_class": 1,
        "condition": 1400,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_heros_dagger.png',
        "price": 45,
        "properties": {
            'damage': 2,
        }
    },
    "Assassin's Sting": {
        "name": "Assassin's Sting",
        "e_type": "melee",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1000,
        "pic": BASE_IMG_PATH + 'ui/equipment/assassins_sting.png',
        "price": 80,
        "properties": {
            'damage': 5,
        }
    },
    "Ruthless Warrior's Sword": {
        "name": "Ruthless Warrior's Sword",
        "e_type": "melee",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 1100,
        "pic": BASE_IMG_PATH + 'ui/equipment/ruthless_warriors_sword.png',
        "price": 75,
        "properties": {
            'damage': 6,
            'stamina': -5,
        }
    },
    "Battle Flamberg": {
        "name": "Battle Flamberg",
        "e_type": "melee",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 2000,
        "pic": BASE_IMG_PATH + 'ui/equipment/battle_flamberg.png',
        "price": 100,
        "properties": {
            'damage': 6,
            'stamina': -10,
        }
    },
    "Axe of the Victorious": {
        "name": "Axe of the Victorious",
        "e_type": "melee",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 2200,
        "pic": BASE_IMG_PATH + 'ui/equipment/axe_of_the_victorious.png',
        "price": 105,
        "properties": {
            'damage': 7,
            'stamina': -15,
        }
    },
    "Leviathan's cutter": {
        "name": "Leviathan's cutter",
        "e_type": "melee",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 2300,
        "pic": BASE_IMG_PATH + 'ui/equipment/leviathans_cutter.png',
        "price": 180,
        "properties": {
            'damage': 8,
            'stamina': -10,
        }
    },
    "Beastmaster's great hammer": {
        "name": "Beastmaster's great hammer",
        "e_type": "melee",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 2400,
        "pic": BASE_IMG_PATH + 'ui/equipment/beastmasters_great_hammer.png',
        "price": 185,
        "properties": {
            'damage': 9,
            'stamina': -15,
        }
    },
    "Blade of Lightning": {
        "name": "Blade of Lightning",
        "e_type": "melee",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 1500,
        "pic": BASE_IMG_PATH + 'ui/equipment/blade_of_lightning.png',
        "price": 190,
        "properties": {
            'damage': 7,
        }
    },
    "Gladius of the Stone Guardian": {
        "name": "Gladius of the Stone Guardian",
        "e_type": "melee",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2700,
        "pic": BASE_IMG_PATH + 'ui/equipment/gladius_of_the_stone_guardian.png',
        "price": 220,
        "properties": {
            'damage': 11,
            'stamina': -5,
        }
    },
    "Legendary Battle Axe": {
        "name": "Legendary Battle Axe",
        "e_type": "melee",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2400,
        "pic": BASE_IMG_PATH + 'ui/equipment/legendary_battle_axe.png',
        "price": 225,
        "properties": {
            'damage': 12,
            'stamina': -10,
        }
    },
    "Ebonite Rapier": {
        "name": "Ebonite Rapier",
        "e_type": "melee",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 2100,
        "pic": BASE_IMG_PATH + 'ui/equipment/ebonite_rapier.png',
        "price": 210,
        "properties": {
            'damage': 10,
        }
    },
    "Blade of Dragons": {
        "name": "Blade of Dragons",
        "e_type": "melee",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 3200,
        "pic": BASE_IMG_PATH + 'ui/equipment/blade_of_dragons.png',
        "price": 270,
        "properties": {
            'damage': 14,
            'health': 10
        }
    },
    "Arcanic two-handed sword": {
        "name": "Arcanic two-handed sword",
        "e_type": "melee",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 3000,
        "pic": BASE_IMG_PATH + 'ui/equipment/arcanic_two_handed_sword.png',
        "price": 260,
        "properties": {
            'attack': 13,
            'mana': 10,
        }
    },
    "Crystal Sword": {
        "name": "Crystal Sword",
        "e_type": "melee",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 2800,
        "pic": BASE_IMG_PATH + 'ui/equipment/crystal_sword.png',
        "price": 265,
        "properties": {
            'attack': 14,
            'stamina': 15,
        }
    },
    "Titan's Thunderbolt": {
        "name": "Titan's Thunderbolt",
        "e_type": "melee",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 6000,
        "pic": BASE_IMG_PATH + 'ui/equipment/titans_thunderbolt.png',
        "price": 550,
        "properties": {
            'attack': 16,
            'stamina': 10,
            'health': 10,
            'mana': 5,
            'experience': 2
        }
    },
    "The Soul Ripper": {
        "name": "The Soul Ripper",
        "e_type": "melee",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 6500,
        "pic": BASE_IMG_PATH + 'ui/equipment/soul_ripper.png',
        "price": 600,
        "properties": {
            'attack': 15,
            'health': 10,
            'mana': 10,
            'experience': 2
        }
    },

    # long_rage_weapon  ------------ 18 items --------------------
    "Hunting Bow": {
        "name": "Hunting Bow",
        "e_type": "long_rage_weapon",
        "rarity": "Common",
        "e_class": 1,
        "condition": 20,  # shot life
        "pic": BASE_IMG_PATH + 'ui/equipment/hunting_bow.png',
        "price": 25,
        "properties": {
            'distance_damage': 40,
        }
    },
    "Legionnaire's bow": {
        "name": "Legionnaire's bow",
        "e_type": "long_rage_weapon",
        "rarity": "Common",
        "e_class": 1,
        "condition": 30,
        "pic": BASE_IMG_PATH + 'ui/equipment/legionnaires_bow.png',
        "price": 30,
        "properties": {
            'distance_damage': 35,
        }
    },
    "Knife of the Ruthless Killer": {
        "name": "Knife of the Ruthless Killer",
        "e_type": "long_rage_weapon",
        "rarity": "Common",
        "e_class": 1,
        "condition": 20,
        "pic": BASE_IMG_PATH + 'ui/equipment/knife_of_the_ruthless_killer.png',
        "price": 25,
        "properties": {
            'distance_damage': 45,
        }
    },
    "Boomerang": {
        "name": "Boomerang",
        "e_type": "long_rage_weapon",
        "rarity": "Common",
        "e_class": 1,
        "condition": 15,
        "pic": BASE_IMG_PATH + 'ui/equipment/chakramborder.png',
        "price": 35,
        "properties": {
            'distance_damage': 55,
        }
    },
    "Forgotten Master's Bow": {
        "name": "Forgotten Master's Bow",
        "e_type": "long_rage_weapon",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 30,
        "pic": BASE_IMG_PATH + 'ui/equipment/forgotten_masters_bow.png',
        "price": 50,
        "properties": {
            'distance_damage': 90,
        }
    },
    "Legendary Archer's Bow": {
        "name": "Legendary Archer's Bow",
        "e_type": "long_rage_weapon",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 35,
        "pic": BASE_IMG_PATH + 'ui/equipment/legendary_archers_bow.png',
        "price": 45,
        "properties": {
            'distance_damage': 85,
        }
    },
    "Sacrificial Knives": {
        "name": "Sacrificial Knives",
        "e_type": "long_rage_weapon",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 300,
        "pic": BASE_IMG_PATH + 'ui/equipment/sacrificial_knives.png',
        "price": 40,
        "properties": {
            'distance_damage': 75,
        }
    },
    "Firefighter's Crossbow": {
        "name": "Firefighter's Crossbow",
        "e_type": "long_rage_weapon",
        "rarity": "Rare",
        "e_class": 2,
        "condition": 30,
        "pic": BASE_IMG_PATH + 'ui/equipment/firefighters_crossbow.png',
        "price": 55,
        "properties": {
            'distance_damage': 95,
        }
    },
    "Firebender's Bow": {
        "name": "Firebender's Bow",
        "e_type": "long_rage_weapon",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 40,
        "pic": BASE_IMG_PATH + 'ui/equipment/firebenders_bow.png',
        "price": 60,
        "properties": {
            'distance_damage': 105,
        }
    },
    "Legendary Sniper Crossbow": {
        "name": "Legendary Sniper Crossbow",
        "e_type": "long_rage_weapon",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 40,
        "pic": BASE_IMG_PATH + 'ui/equipment/legendary_sniper_crossbow.png',
        "price": 65,
        "properties": {
            'distance_damage': 110,
        }
    },
    "Shadow Masters Shuriken": {
        "name": "Shadow Masters Shuriken",
        "e_type": "long_rage_weapon",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 45,
        "pic": BASE_IMG_PATH + 'ui/equipment/shadow_masters_shuriken.png',
        "price": 70,
        "properties": {
            'distance_damage': 100,
        }
    },
    "Forged Dragon Crossbow": {
        "name": "Forged Dragon Crossbow",
        "e_type": "long_rage_weapon",
        "rarity": "Unique",
        "e_class": 3,
        "condition": 35,
        "pic": BASE_IMG_PATH + 'ui/equipment/forged_dragon_crossbow.png',
        "price": 75,
        "properties": {
            'distance_damage': 120,
        }
    },
    "Crystal Bow": {
        "name": "Crystal Bow",
        "e_type": "long_rage_weapon",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 60,
        "pic": BASE_IMG_PATH + 'ui/equipment/crystal_bow.png',
        "price": 100,
        "properties": {
            'distance_damage': 130,
        }
    },
    "Dragon's Wrath Bow": {
        "name": "Dragon's Wrath Bow",
        "e_type": "long_rage_weapon",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 50,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragons_wrath_bow.png',
        "price": 105,
        "properties": {
            'distance_damage': 140,
        }
    },
    "Wind Lord Shuriken": {
        "name": "Wind Lord Shuriken",
        "e_type": "long_rage_weapon",
        "rarity": "Epic",
        "e_class": 4,
        "condition": 55,
        "pic": BASE_IMG_PATH + 'ui/equipment/wind_lord_shuriken.png',
        "price": 95,
        "properties": {
            'distance_damage': 120,
        }
    },
    "Dragon Slayer": {
        "name": "Dragon Slayer",
        "e_type": "long_rage_weapon",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 70,
        "pic": BASE_IMG_PATH + 'ui/equipment/dragon_slayer.png',
        "price": 150,
        "properties": {
            'distance_damage': 150,
            'health': 15,
        }
    },
    "Magic Crossbow": {
        "name": "Magic Crossbow",
        "e_type": "long_rage_weapon",
        "rarity": "Legendary",
        "e_class": 5,
        "condition": 70,
        "pic": BASE_IMG_PATH + 'ui/equipment/magic_crossbow.png',
        "price": 170,
        "properties": {
            'distance_damage': 140,
            'mana': 10,
        }
    },
    "Wind conqueror": {
        "name": "Wind conqueror",
        "e_type": "long_rage_weapon",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 100,
        "pic": BASE_IMG_PATH + 'ui/equipment/wind_conqueror.png',
        "price": 400,
        "properties": {
            'distance_damage': 170,
            'stamina': 20,
            'experience': 2,
        }
    },
    "Whisper of death": {
        "name": "Whisper of death",
        "e_type": "long_rage_weapon",
        "rarity": "Mythical",
        "e_class": 6,
        "condition": 90,
        "pic": BASE_IMG_PATH + 'ui/equipment/whisper_of_death.png',
        "price": 500,
        "properties": {
            'distance_damage': 200,
            'health': 20,
            'experience': 2,
        }
    }
}
