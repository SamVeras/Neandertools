from sys import exit
from variables import DICT
from colorama import Fore as fr, Style as st


def read_file(arg: str) -> list:
    try:
        with open(arg, "r") as file:
            lines_as_list = file.read().splitlines()
            lines_with_sublists = [x.split() for x in lines_as_list]
            return [x for y in lines_with_sublists for x in y]
    except:
        print("File not found.")
        exit(1)


def translate_list(listed: list) -> list:
    nu_listed = []
    for i in listed:
        for x, y in DICT.items():
            i = str(i).replace(x, y)
        nu_listed.append(i)

    listed = [int(i) for i in nu_listed]

    return listed


def check_diff(l1: list, l2: list) -> str:
    diff_string = ""
    for c, (x, y) in enumerate(zip(l1, l2)):
        if x != y:
            diff_string += f"Address {c}: {x} -> {y}.\n"
    return diff_string


def log_color(logged: str) -> str:
    color_dict = {
        "LDA:": f"{fr.GREEN}LDA:",
        "STA:": f"{fr.BLUE}STA:",
        "ADD:": f"{fr.YELLOW}ADD:",
        "OR:": f"{fr.MAGENTA}OR:",
        "AND:": f"{fr.MAGENTA}AND:",
        "NOT:": f"{fr.RED}NOT:",
        "JMP:": f"{fr.CYAN}JMP:",
        "JN:": f"{fr.CYAN}JN:",
        "JZ:": f"{fr.CYAN}JZ:",
        "HLT:": f"{st.DIM}HLT:",
        ".     ": f"{st.RESET_ALL}",
    }
    for x, y in color_dict.items():
        logged = logged.replace(x, y)
    return logged
