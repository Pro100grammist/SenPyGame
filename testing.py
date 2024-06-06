import os
import json
import random

from data import EQUIPMENT
from backup import EQUIPMENT as EQ
from support import BASE_IMG_PATH

# 1 script for filling EQUIPMENT dictionary
# player_equipments = {}
#
#
# for item_name, item_info in EQUIPMENT.items():
#     rarity = item_info["rarity"]
#     if rarity in player_equipments:
#         player_equipments[rarity].append(item_name)
#     else:
#         player_equipments[rarity] = [item_name]
#
# for rarity, items in player_equipments.items():
#     print(rarity + ":")
#     print(items)
#     print()

# 2 script for saving EQUIPMENT dictionary in json format
# with open('equipment.json', 'w') as json_file:
#     json.dump(EQUIPMENT, json_file, indent=4)
#
# items_score = len(EQ)
# print(items_score)

# 3 script rename files in directory
#
# directory = BASE_IMG_PATH + 'entities/merchant'
# files = os.listdir(directory)
# files.sort()
#
# for file_name in files:
#     base_name, extension = os.path.splitext(file_name)
#     underscore_index = base_name.find('_')
#     new_base_name = base_name[underscore_index + 1:]
#     new_base_name = new_base_name.replace('_', '0')
#     new_file_name = f"{new_base_name}{extension}"
#     os.rename(os.path.join(directory, file_name), os.path.join(directory, new_file_name))
