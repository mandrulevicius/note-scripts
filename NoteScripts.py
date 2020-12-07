from datetime import datetime
from pyautogui import typewrite
# Presentable Portfolio Project
# barebones prototype

# first thing to do next session (after backup):
# setup git
# mouseless coding
# DONE - load and display multiple notes
# DONE - selection of notes
# editing of notes
# editing history/deltas/edit tracing?
# add tags functionality
# ...
# UI?
# when to move on to 0.002?

# note loading separate from note display - changing loading to sql shouldnt impact display - maybe not in prototype - leave modularity for release

# '' printing for debug info, "" for user

# commands = {"m":"main", "x":"exit", "n":"notes"}
commands = ["m", "x", "n"]
run_mode = ""


def main():
    on_main_begin()
    setup_data = load_setup_from_file()
    # if pass_check():
    if True:
        setup_data = main_loop(setup_data)
    save_setup_to_file(setup_data)
    on_main_end()


def on_main_begin():
    print('__on_main_begin__')
    print("Welcome")


def on_main_end():
    print('__on_main_end__')


def main_loop(setup_data):
    print('__main_loop__')
    run_main_loop = True
    while run_main_loop:
        current_input = ask_for_input("Please enter a command")
        if current_input in commands:
            # print('Command recognized as {}'.format(commands[current_input].value))
            print('Command recognized')
            if current_input == "x":
                run_main_loop = False
            else:
                setup_data = execute_command(current_input, setup_data)
        else:
            print('Command unrecognised')
    return setup_data


def backup_database():
    pass


def set_mode():
    # print(run_mode)  # will print global or local?
    run_mode = "default"  # user admin debug
    print(run_mode)  # will print local?


def pass_check():
    return ask_for_input("Please provide a password") == "pfef"   # PassFromEncryptedFile


def load_setup_from_file():
    print('__load_setup_from_file__')
    with open('Data/Setup.txt') as file:
        return file.read()


def save_setup_to_file(setup_data):
    print('__save_setup_to_file__')

    with open('Data/Setup.txt', "w") as file:
        file.write(setup_data)

    # We can check that the file has been automatically closed.
    # file.closed


def load_note_from_file(setup_data):
    print('__load_notes_from_file__')
    with open('Data/Note{}.txt'.format(setup_data)) as f:
        return f.read()

    # We can check that the file has been automatically closed.
    # f.closed


def save_to_file(current_data_string, setup_data):
    print('__save_to_file__')
    # find last file name
    # move last file to archive
    # create new file
    # save current_data_string
    # close file

    current_note_no = int(setup_data)
    current_note_no += 1

    # fiel = open('Data/Note.txt', "x")
    # fiel = open('Data/Note{}.txt'.format(current_note_no, "x"))

    with open('Data/Note{}.txt'.format(current_note_no), "w") as file:
        file.write(current_data_string)

    setup_data = str(current_note_no)

    # We can check that the file has been automatically closed.
    file.closed
    return setup_data


def save_to_database():
    print('__save_to_database__')


def ask_for_input(input_text):
    print('__ask_for_input__')
    # sanitize inputs
    return input("{} \n../> ".format(input_text))


def execute_command(command, setup_data):
    print('__execute_command__')
    print("Executing command - {}".format(command))
    if command == "x":
        execute_x()
    if command == "m":
        execute_m()
    if command == "n":
        setup_data = execute_n(setup_data)
    return setup_data


def execute_x():
    # obsolete, code shouldnt reach this for now
    print('__execute_x__')
    print("Closing")
    quit()


def execute_m():
    print('__execute_m__')
    print("Testing persistence")
    # menu, mode?
    pass


def execute_n(last_note_no):
    print('__execute_n__')
    print("Opening notes")
    last_note_no = int(last_note_no)
    print("Last note number: {}".format(last_note_no))
    # landing screen (favourite/frequent/newest notes, new note, search notes, filter/group notes)
    full_data_string = ""
    i = 0
    if int(last_note_no) > 5:
        while i < 5:
            full_data_string += load_note_from_file(int(last_note_no) - i) + "<N>"
            i += 1
    else:
        while (int(last_note_no) - i) >= 0:
            full_data_string += load_note_from_file(int(last_note_no) - i) + "<N>"
            i += 1

    print("BEGIN full_data_string BEGIN")
    print(full_data_string)
    print("END full_data_string END")
    note_list = full_data_string.split("<N>")
    display_last_notes(note_list)

    print("BEGIN note_list BEGIN")
    print(note_list)
    print("END note_list END")
    last_note = note_list[0]
    last_note_lines = last_note.splitlines()
    print("Last note: \n{}".format(last_note_lines[1:]))

    current_note_no, current_data_string = select_note(last_note_no)

    # redundant code for now, might be used later to split data
    # data_lines = current_data_string.splitlines()
    # header_data = data_lines[0].split("|")

    # text_data_lines = data_lines[1:]
    # print("Latest note: \n{}".format(text_data_lines))

    while True:
        note_command = input("Enter note command \n../> ")
        if note_command == "x":
            print("Exiting notes")
            return str(last_note_no)
        elif note_command == "new":
            last_note_no = int(create_new_note(str(last_note_no)))
            current_note_no, current_data_string = select_note(last_note_no)
        elif note_command == "edit":
            edit_note(current_data_string)
        elif note_command == ",":
            if current_note_no > 0:
                current_note_no, current_data_string = select_note(current_note_no - 1)
            else:
                print("First note selected, there are no previous notes")
        elif note_command == ".":
            if current_note_no < last_note_no:
                current_note_no, current_data_string = select_note(current_note_no + 1)
            else:
                print("Last note selected, there are no more notes")
        else:
            try:
                go_to_note_no = int(note_command)
                if (go_to_note_no >= 0) and (go_to_note_no <= last_note_no):
                    current_note_no, current_data_string = select_note(go_to_note_no)
                else:
                    print("Note number {} does not exist".format(go_to_note_no))
            except ValueError:
                print("Command unrecognized")


def select_note(note_no):
    print('__select_note__')
    current_data_string = load_note_from_file(note_no)
    current_note_lines = current_data_string.splitlines()
    current_note_header = current_note_lines[0].split("|")
    current_note_number = int(current_note_header[0])
    print("Current note ({}): \n{}".format(current_note_number, current_note_lines[1:]))
    return current_note_number, current_data_string


def create_new_note(last_note_no):
    print('__create_new_note__')
    note_tags = ""  # (category and type in one?)
    note_type = ""  # type of note (quote, picture, thought, reminder, event, etc.
    note_category = ""  # note category (selfdev, stoicism, gamedev, gaming)

    text_data = (input("{} \n../> ".format("New note")) + "\n")
    if text_data == "x\n":
        print("Cancelling new note")
        return last_note_no

    previous_reference_ID = last_note_no
    new_header = (str(int(last_note_no) + 1) + "|" + previous_reference_ID + "|" + str(datetime.now()) + "|" +
                  note_tags + "|" + note_type + "|" + note_category + "\n")

    current_data_string = new_header + text_data
    # edit existing note/create new note
    new_note_no = save_to_file(current_data_string, last_note_no)
    save_setup_to_file(new_note_no)
    # file structure, create dependencies?
    return new_note_no


def edit_note(current_data_string):
    # currently only works for single line notes
    print('__edit_note__')
    note_lines = current_data_string.splitlines()
    note_header = note_lines[0]
    # note_full_text = ""
    # for note_text_line in note_lines[1:]:
    #     note_full_text += (note_text_line)
    note_header_info_list = note_header.split("|")
    print("Editing note {}: \n".format(note_header_info_list[0]))
    typewrite(note_lines[1])  # buggy, use win console?
    note_lines[1] = input()
    # also doesnt change the original creation timestamp
    save_edit_to_file(note_lines)


"""
import win32console

_stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)

def input_def(prompt, default=''):
    keys = []
    for c in unicode(default):
        evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
        evt.Char = c
        evt.RepeatCount = 1
        evt.KeyDown = True
        keys.append(evt)

    _stdin.WriteConsoleInput(keys)
    return raw_input(prompt)

if __name__ == '__main__':
    name = input_def('Folder name: ')
    print
    print name
"""


def save_edit_to_file(note_lines):
    print('__save_edit_to_file__')
    note_header_info_list = note_lines[0].split("|")

    # fiel = open('Data/Note.txt', "x")
    # fiel = open('Data/Note{}.txt'.format(current_note_no, "x"))

    with open('Data/Note{}.txt'.format(note_header_info_list[0]), "w") as file:
        # only works with one line of text
        file.write(note_lines[0] + "\n" + note_lines[1])

    # We can check that the file has been automatically closed.
    file.closed


def display_home_page(full_data):
    print('__display_home_page__')


def display_last_notes(note_list):
    print('__display_last_notes__')
    for note in note_list:
        if note != "":
            split_note = note.splitlines()
            note_header = split_note[0]
            note_lines = split_note[1:]
            split_note_header = note_header.split("|")
            print("Note ID: {}".format(split_note_header[0]))
            print("Note text: \n{}".format(note_lines))


main()
