import os
import json


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
script_directory = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_directory, 'project_structure.json')

structure = get_directory_structure(script_directory)
save_structure_to_json(structure, output_file)

print(f'Structure of the project saved to {output_file}')
