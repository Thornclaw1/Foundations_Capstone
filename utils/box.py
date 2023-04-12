def box(info, padding=1):
    return box_list(info.split("\n"), padding, line_prefix="")

def box_list(info, padding=1, list_name="", line_prefix="- ", line_suffix=""):
    info = [line_prefix + line + line_suffix for line in info]
    width = len(max(info, key=len))
    width = len(list_name) if len(list_name) > width else width
    padded_width = width + padding * 2
    boxed_info = "┌" + "─"*padded_width + "┐\n"
    if list_name:
        boxed_info += f"│{' '*padding}{list_name:{width}}{' '*padding}│\n"
    for line in info:
        boxed_info += f"│{' '*padding}{line:{width}}{' '*padding}│\n"
    boxed_info += "└" + "─"*padded_width + "┘"
    return boxed_info

def menu(menu_items, padding=1, indexing_format = "[?]", starting_index = 1):
    menu_items = [f"{indexing_format.replace('?',str(idx))} {line}" for idx, line in enumerate(menu_items, starting_index)]
    width = len(max(menu_items, key=len))
    padded_width = width + padding * 2
    boxed_menu = "┌" + "─"*padded_width + "┐\n"
    for line in menu_items:
        boxed_menu += f"│{' '*padding}{line:{width}}{' '*padding}│\n"
    boxed_menu += "└" + "─"*padded_width + "┘"
    return boxed_menu

def full_menu(menu_items, quit=("0", "Quit"), padding=1, indexing_format = "[?]"):
    menu_items[quit[0]] = (quit[1], lambda : True)
    valid_inputs = menu_items.keys()
    menu_strs = [f"{indexing_format.replace('?',str(key))} {val[0]}" for key, val in menu_items.items()]
    width = len(max(menu_strs, key=len))
    padded_width = width + padding * 2

    def print_menu():
        boxed_menu = "┌" + "─"*padded_width + "┐\n"
        for key, val in menu_items.items():
            line = f"{indexing_format.replace('?',key)} {val[0]}"
            boxed_menu += f"│{' '*padding}{line:{width}}{' '*padding}│\n"
        boxed_menu += "└" + "─"*padded_width + "┘"
        print(boxed_menu)

    while True:
        print_menu()
        while True:
            if (user_input := input(">>> ")) in valid_inputs:
                if menu_items[user_input][1]():
                    return
                break
            print("Invalid Input")
        