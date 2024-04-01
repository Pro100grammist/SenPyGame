import json
from data import EQUIPMENT


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
with open('equipment.json', 'w') as json_file:
    json.dump(EQUIPMENT, json_file, indent=4)
