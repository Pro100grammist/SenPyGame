import os
import json
import re
import datetime


def auto_backup(file_list):
    """ Скрипт для авто копіювання вмісту всіх файлів з робочим кодом проєкту """
    date_str = datetime.datetime.now().strftime("%d_%m_%Y")  # Поточна дата у форматі **_**_****.
    backup_filename = f"auto_backup_{date_str}.json"  # назва для файлу
    backup_filepath = os.path.join('backup', backup_filename)

    with open(backup_filepath, 'w') as backup_file:
        for filename in file_list:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    backup_file.write(f"# {filename}\n")
                    backup_file.write(f.read())
                    backup_file.write("\n# ******** end of file *********\n\n")
        print(f"Backup created at {backup_filepath}")


# Список файлів, які потрібно скопіювати.
data_to_backup = ['books.json', 'equipment.json', 'equipment_category.json', 'npc_data.json', 'skills.json']
auto_backup(data_to_backup)
