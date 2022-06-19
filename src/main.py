from typing import List, Dict
from pathlib import WindowsPath
from helpers import *
from rw_functions import load_file, patch_mod_files, load_mod_files, save_backup, dump_json

def main():

    raw_data: Dict

    print_welcome()

    file_path: WindowsPath = get_target_file()

    vanilla_options: Dict | None = load_file(file_path, True)
    if vanilla_options is None:
        return

    loaded_mod_options: List[(str, Dict)] | None = load_mod_files(str(file_path))
    if loaded_mod_options == None:
        return
    elif len(loaded_mod_options) == 0:
        print("> No mod files to patch. Exiting.")
        return

    result: bool | None = patch_mod_files(vanilla_options, loaded_mod_options)
    if result is None:
        return
    elif result == False:
        print("> " + str(file_path) + " doesn't need patching. Goodbye.")
        return

    if get_yes_no_answer("Save backup of " + str(file_path) + "?", False):
        save_backup(file_path)

    success: bool = dump_json(vanilla_options, file_path)
    if success:
        print("> All done. Goodbye.")

main()

