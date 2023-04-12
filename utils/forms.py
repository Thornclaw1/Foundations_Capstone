import gnureadline as readline

from utils.ansi import *

def form(*form_fields):
    field_count = len(form_fields)
    max_width = len(max(form_fields, key=len))
    for field in form_fields:
        print(f"{field:>{max_width}} : ")
    form_values = []
    util.move("up", field_count)
    for _ in range(field_count):
        util.move("right", max_width + 3)
        form_values.append(input())
    return tuple(form_values)

def edit_form(form_fields, existing_values):
    field_count = len(form_fields)
    max_width = len(max(form_fields, key=len))
    for idx, field in enumerate(form_fields):
        print(f"{field:>{max_width}} : {existing_values[idx]}")
    form_values = []
    util.move("up", field_count)
    for idx, field in enumerate(form_fields):
        # util.move("right", max_width + 3)
        form_values.append(rlinput(f"{field:>{max_width}} : ", existing_values[idx]))
    return tuple(form_values)

def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()