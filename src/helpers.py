from pathlib import Path, WindowsPath

def print_(value: str):
    print(value, end="")

def print_welcome():
    print('--------------------------------')
    print('+                              +')
    print('+   CP77 Options JSON Merger   +')
    print('+                              +')
    print('--------------------------------')

def get_target_file() -> WindowsPath:
    target: WindowsPath
    path: str
    valid: bool = False

    while not valid:
        path = input("> What target file do you wish to merge into? (leave empty for default 'options.json'): ")

        if len(path) == 0:
            path = "options.json"
        elif not path.endswith(".json"):
            print("> File must be a .json file.")
            continue

        print_("> Looking for " + path + "...")
        target = Path(path)
        if target.exists():
            print(" Found.")
            valid = True
        else:
            print(" Not found.")


    return target

def get_yes_no_answer(question: str, default: bool) -> bool:
    answer: bool = default
    x: str
    valid: bool = False

    while not valid:
        default_hint: str = 'y'
        if not default:
            default_hint = 'n'

        x = input("> " + question + " [n/y] (default " + default_hint + "): ")

        if len(x) == 0:
            x = default_hint

        x = x.lower()

        if x == "y" or x == "yes":
            answer = True
            valid = True
        elif x == "n"  or x == "no":
            answer = False
            valid = True

    return answer
