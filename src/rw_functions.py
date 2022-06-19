import json
import shutil
from typing import Dict, List, TypeAlias, Generator
from pathlib import WindowsPath, Path
from helpers import print_, get_yes_no_answer

def load_file(path: WindowsPath, require_version: bool) -> Dict | None:
    data: Dict

    print_("> Loading " + str(path) + "...")

    try:
        with open(path, "r") as read_file:
            data = json.load(read_file)

        print(" Success.")

        print_("> Checking structure of " + str(path) + "...")
        if is_structure_valid(data, require_version):
            print(" OK.")
        else:
            print(" Bad structure.")
            return None

    except:
        print(" Failed.")
        return None

    return data

def load_mod_files(ignore_file_name: str) -> List[tuple] | None:
    print_("> Looking for mod .json files...")
    all_json_files: Generator = Path(".").glob("*.json")
    mod_files_paths: List[WindowsPath] = []
    file_path: WindowsPath
    for file_path in all_json_files:
        if not str(file_path) == ignore_file_name:
            mod_files_paths.append(file_path)

    mod_files_count: int = len(mod_files_paths)
    print(" Found " + str(mod_files_count) + ".")

    files_to_patch: List[WindowsPath] = []
    for file_path in mod_files_paths:
        if get_yes_no_answer("Patch " + str(file_path) + "?", True):
            files_to_patch.append(file_path)

    loaded_mod_options: List[(str, Dict)] = []
    mod_file_path: WindowsPath
    for mod_file_path in files_to_patch:
        loaded: Dict | None = load_file(mod_file_path, False)
        if not loaded is None:
            loaded_mod_options.append((str(mod_file_path), loaded))

    return loaded_mod_options

def is_structure_valid(data: Dict, require_version: bool) -> bool:
    if not isinstance(data, Dict) or not 'groups' in data or not 'options':
        return False

    if require_version and not 'version' in data:
        return False

    return True

def list_contains(list: list, key: str, value: str) -> bool:
    for item in list:
        if item[key] == value:
            return True

    return False

def patch_mod_files(vanilla_options: Dict, mods: List[tuple]) -> bool | None:
    vanilla_dirty: bool = False
    for mod in mods:
        print("> Patching " + mod[0] + ":")
        patched: bool | None = patch_file(vanilla_options, mod[1])
        if patched is None:
            return None
        elif patched == True:
            vanilla_dirty = True

    return vanilla_dirty

def patch_file(vanilla: Dict, mod: Dict) -> bool | None:
    was_patched: bool = False
    try:
        for modGroup in mod['groups']:
            print_("\t[groups]" + modGroup['group_name'] + ": ")
            if not list_contains(vanilla['groups'], 'group_name', modGroup['group_name']):
                vanilla['groups'].append(modGroup)
                was_patched = True
                print("Patched.")
            else:
                print("Already in file.")

        for optionsGroup in mod['options']:
            print_("\t[options]" + optionsGroup['group_name'] + ": ")
            if not list_contains(vanilla['options'], 'group_name', optionsGroup['group_name']):
                vanilla['options'].append(optionsGroup)
                was_patched = True
                print("Patched.")
            else:
                print("Already in file.")
    except:
        print("\nPatch file failed.")
        return None

    return was_patched

def save_backup(file: WindowsPath):
    print_("> Saving backup file...")
    shutil.copyfile(file, str(file) + ".bck")
    print("Done.")

def dump_json(data: Dict, file: WindowsPath) -> bool:
    print_("> Overwriting " + str(file) + "...")

    try:
        with open(file, "w") as write_file:
            json.dump(data, write_file, indent = 4)

        print(" Done.")
        return True
    except:
        print(" Error.")
        return False

