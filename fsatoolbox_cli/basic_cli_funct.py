import ntpath
import os

from termcolor import colored
import colorama

from fsatoolbox import fsa, state, event
from fsatoolbox_cli.utils.config_mng import create_config, change_cwdir, read_cwdir
import configparser

colorama.init()


# Internal --------------------------------------------------------------------------

def fix_config_path(recreate=False):
    if recreate is True:

        create_config()

    else:

        err_str = "Invalid working path in configuration file: " \
                  "Press ENTER to reset the value or enter a valid path"

        inp = input(colored(err_str, "red"))

        if os.path.isdir(inp):

            change_cwdir(inp)

        else:

            change_cwdir(os.getcwd())

        print(colored("Current working directory:", attrs=["bold"]) + read_cwdir())


# Directory management -----------------------------------------------------------------------

def remove_cli_f(fsa_name, fsa_dict):
    if fsa_name not in fsa_dict.keys():
        print(colored("FSA not found", "red"))
        return

    del fsa_dict[fsa_name]


def chdir_cli_f(new_path):
    if os.path.isabs(os.path.normpath(new_path)):
        if os.path.isdir(os.path.normpath(new_path)):
            try:
                change_cwdir(os.path.normpath(new_path))
            except FileNotFoundError:
                create_config()

        else:
            print(colored("Invalid path", "red"))
            return

        # Path is not absolute

    else:

        try:
            path = read_cwdir()

        except configparser.NoSectionError:
            fix_config_path()
            path = read_cwdir()
        except FileNotFoundError:
            fix_config_path(recreate=True)
            path = read_cwdir()

        tail = os.path.normpath(new_path)
        head = read_cwdir()

        # Parsing the path
        parsed_path = os.path.split(tail)

        # ".." Escape character
        if ".." in parsed_path:
            if parsed_path == ("", ".."):
                new_path = os.path.split(head)[0]
            elif parsed_path[0] == ".." and parsed_path[1] != "":
                head = os.path.split(path)[0]
                tail = parsed_path[1]
                new_path = os.path.join(head, tail)
            else:
                print(colored("Invalid path", "red"))
                return head

        # "." Escape character
        elif "." in parsed_path:
            if parsed_path == ("", "."):
                new_path = head
            elif parsed_path[0] == "." and parsed_path[1] != "":
                tail = parsed_path[1]
                new_path = os.path.join(path, tail)
            else:
                print(colored("Invalid path", "red"))
                return head

        # No escape character
        else:
            new_path = os.path.join(head, tail)

        # Checking if new_path exists
        if os.path.isdir(new_path):
            change_cwdir(new_path)
        else:
            print(colored("Invalid path", "red"))
            change_cwdir(head)


def ldir_cli_f():
    try:
        path = read_cwdir()

    except configparser.NoSectionError:
        fix_config_path()
        path = read_cwdir()
    except FileNotFoundError:
        fix_config_path(recreate=True)
        path = read_cwdir()

    print(colored("\nElements in: ", "yellow", attrs=["bold"]) + path + "\\\n")
    file_list = os.listdir(path + "\\")  # files only
    for el in file_list:
        if os.path.isdir(el):
            print(colored(el, "green"))
        else:
            print(el)
    print("\n" + colored("Legend: ", attrs=["bold"]) + colored("green", "green") + " represents directories\n")


def showdir_cli_f():
    try:
        path = read_cwdir()

    except configparser.NoSectionError:
        fix_config_path()
        path = read_cwdir()
    except FileNotFoundError:
        fix_config_path(recreate=True)
        path = read_cwdir()

    print("Current working directory: " + path)


def clear_cli_f(fsa_dict):
    fsa_dict.clear()


# FSA build and show -----------------------------------------------------------------------

def showfsa_cli_f(fsa_name, fsa_dict):
    if fsa_name not in fsa_dict:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    print(fsa_dict[fsa_name])


def list_cli_f(fsa_dict):
    print("FSA currently loaded: " + str(list(fsa_dict.keys())))


# Load and save -----------------------------------------------------------------------

def load_cli_f(arg1=None, arg2=None, fsa_dict=None):
    # Double argument mode -> arg1: fsa_name; arg2: filepath
    # Single argument mode -> arg1: filepath

    try:
        path = read_cwdir()

    except configparser.NoSectionError:
        fix_config_path()
        path = read_cwdir()
    except FileNotFoundError:
        fix_config_path(recreate=True)
        path = read_cwdir()

    if not arg2:  # single argument mode
        name = ntpath.split(arg1)[1]
        name = name.split('.')[0]
        filepath = arg1
    else:  # two arguments mode
        name = arg1
        filepath = arg2

    if name in fsa_dict:
        inp = input(colored("Warning, fsa already exists, do you want to overwrite it? [y/N]: ", "yellow"))
        if inp.lower() == 'n' or inp == '':
            return

    if not os.path.isabs(filepath):
        filepath = os.path.join(path, filepath)

    if os.path.isfile(filepath):
        G = fsa.from_file(filepath)

    else:
        if filepath[-5:] == ".json" or filepath[-4:] == ".txt":
            print(colored("Error: file does not exists", "red"))
        else:
            print(colored("Error: file does not exists (did you forget the extension?)", "red"))
        return

    fsa_dict[name] = G


def save_cli_f(*args, fsa_dict):
    try:
        path = read_cwdir()

    except configparser.NoSectionError:
        fix_config_path()
        path = read_cwdir()
    except FileNotFoundError:
        fix_config_path(recreate=True)
        path = read_cwdir()

    if args[0] in fsa_dict:

        if not os.path.isabs(args[1]):
            filename = os.path.join(path, args[1])
        else:
            filename = args[1]

        try:
            fsa_dict[args[0]].to_file(filename)  # current path
        except Exception as e:
            print(colored("Error while saving the file:", "red"))
            print(e)
    else:
        print(colored("Error, fsa doesn't exists", "red"))


# TODO add exit (abort) option in every input

def build_cli_f(args, fsa_dict):
    prompt_col = 'green'
    warn_col = 'yellow'

    if args in fsa_dict:
        inp = input(colored("Error, fsa already exists, ado you want to overwrite it? [y/N]: ", warn_col))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    G = fsa(name=args)

    # states
    while True:
        inp = input(colored("Insert the states, separated by a space [!q to abort]:\n", prompt_col)).split(' ')
        if inp == ['!q']:
            print(colored("Build of fsa aborted", warn_col))
            return

        while "" in inp:  # remove empty strings or double spaces
            inp.remove("")

        if len(inp) != len(set(inp)):
            print(colored("Warning, there are duplicates states", warn_col))
            print(colored("States: ", prompt_col), end='')
            print(set(inp))
            q = input(colored("Do you want to input the states again? [Y/n]:\n", prompt_col))
            if q.lower() != 'n':
                continue
            inp = set(inp)
        break
    X = []
    for x in inp:
        X.append(state(x))
    states = inp

    state_prop = {  # name (for the prompt) and attribute name
        'initial': 'isInitial',
        'final': 'isFinal',
        'forbidden': 'isForbidden'
    }

    for name, attr in state_prop.items():
        while True:
            inp = input(colored("Insert the " + name + " states, separated by a space [- to skip, !q to abort]:\n",
                                prompt_col)).split(' ')

            if inp == ['!q']:
                print(colored("Build of fsa aborted", warn_col))
                return

            if inp == ['-']:
                break

            if inp == ['']:
                break

            for el in inp:
                if el not in states:
                    print(colored("The state: " + el + " is not in the fsa, try again", warn_col))
                    break
            else:
                break
            continue

        for x in X:
            setattr(x, attr, False)
        for x in inp:
            for y in X:
                if x == y.label:
                    setattr(y, attr, True)
                    break

    # add the states to the fsa
    for x in X:
        G.add_state(x)
        # print(x.label+" "+str(x.isInitial)+" "+str(x.isFinal)+" "+str(x.isForbidden))

    # events
    while True:
        inp = input(colored("Insert the events, separated by a space [!q to abort]:\n", prompt_col)).split(' ')

        if inp == ['!q']:
            print(colored("Build of fsa aborted", warn_col))
            return

        while "" in inp:  # remove empty strings or double spaces
            inp.remove("")

        if inp == ['']:
            break

        if len(inp) != len(set(inp)):
            print(colored("Warning, there are duplicates events", warn_col))
            print(colored("Events: ", prompt_col), end='')
            print(set(inp))
            q = input(colored("Do you want to input the events again? [Y/n]:\n", prompt_col))
            if q.lower() != 'n':
                continue
            inp = set(inp)
        break

    E = []
    for e in inp:
        E.append(event(e))
    events = inp

    event_prop = {
        'observable': 'isObservable',
        'controllable': 'isControllable',
        'faulty': 'isFault'
    }

    for name, attr in event_prop.items():
        while True:
            inp = input(colored("Insert the " + name + " events, separated by a space [- to skip, !q to abort]:\n",
                                prompt_col)).split(' ')
            if inp == ['!q']:
                print(colored("Build of fsa aborted", warn_col))
                return

            if inp == ['-']:
                break

            for el in inp:
                if el not in events:
                    print(colored("The event: " + el + " is not in the fsa, try again", warn_col))
                    break
            else:
                break
            continue

        for e in E:
            setattr(e, attr, False)
        for e in inp:
            for y in E:
                if e == y.label:
                    setattr(y, attr, True)
                    break

    # add the events to the fsa
    for e in E:
        G.add_event(e)
        # print(e.label+" "+str(e.isObservable)+" "+str(e.isControllable)+" "+str(e.isFault))

    # transitions
    while True:
        inp = input(
            colored("Insert a transition (in the format x0 a x1) [!q to abort, - to end]:\n", prompt_col)).split(' ')
        if inp[0] == '!q':
            print(colored("Build of fsa aborted", warn_col))
            return
        if inp[0] == '-':
            break
        if not len(inp) == 3:
            print(colored("Incorrect transition format", warn_col))
            continue
        else:
            try:
                G.add_transition(inp[0], inp[1], inp[2])
            except Exception:
                continue

    fsa_dict[args] = G
