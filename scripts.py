import os
import json
import re
import datetime


def get_directory_structure(rootdir):
    """
    Створює структуру директорії у вигляді вкладеного словника.
    """
    structure = {}

    for dirpath, dirnames, filenames in os.walk(rootdir):
        # Отримання відносного шляху від кореневої директорії
        rel_path = os.path.relpath(dirpath, rootdir)
        # Розбиваємо шлях на частини
        path_parts = rel_path.split(os.sep)
        # Посилання на поточний рівень структури
        current_level = structure
        for part in path_parts:
            if part != '.':
                current_level = current_level.setdefault(part, {})

        # Додавання файлів на поточному рівні
        for filename in filenames:
            current_level[filename] = None
        # Додавання піддиректорій на поточному рівні
        for dirname in dirnames:
            current_level[dirname] = {}

    return structure


def save_structure_to_json(structure, output_file):
    """
    Зберігає структуру директорії у файл формату JSON.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)


# Отримання абсолютного шляху до директорії, в якій знаходиться скрипт
# script_directory = os.path.dirname(os.path.abspath(__file__))
# output_file = os.path.join(script_directory, 'project_structure.json')
#
# structure = get_directory_structure(script_directory)
# save_structure_to_json(structure, output_file)
#
# print(f'Structure of the project saved to {output_file}')


def rename_files(directory):
    print(f"Target directory: {directory}")
    for filename in os.listdir(directory):
        print(f"Processing file: {filename}")
        match = re.search(r'\d', filename)
        if match:
            new_filename = '0' + filename[match.start():]
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            os.rename(old_file, new_file)
            print(f"Renamed: {filename} -> {new_filename}")
        else:
            print(f"No digit found in: {filename}")


# directory_path = './data/images/entities/enemy/fire_worm/attack'
# rename_files(directory_path)


def auto_backup(file_list):
    """ Скрипт для авто копіювання вмісту всіх файлів з робочим кодом проєкту """
    date_str = datetime.datetime.now().strftime("%d_%m_%Y")  # Поточна дата у форматі **_**_****.
    backup_filename = f"auto_backup_{date_str}.py"  # назва для файлу
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
files_to_backup = [
    'game.py', 'map.py', 'entities.py', 'player_controller.py', 'items.py', 'level.py', 'particle.py',
    'projectile.py', 'support.py', 'ui.py', 'weather.py', 'data.py', 'settings.py', 'scripts.py'
]
auto_backup(files_to_backup)
