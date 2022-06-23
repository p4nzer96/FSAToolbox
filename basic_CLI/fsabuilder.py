import fsatoolbox
from fsatoolbox import *
from termcolor import colored
import colorama

colorama.init()


# TODO add exit (abort) option in every input

def build_CLI(args, fsalst, **kwargs):
    prompt_col = 'green'
    warn_col = 'yellow'

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"build -h\" to help", warn_col))
        return

    if '-h' in args:
        print(colored("\nbuild: ", "yellow", attrs=["bold"]) + "This functions starts an interactive program to build "
                                                               "a FSA")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tbuild fsa_name (ex: build G0)")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tbuild G0")
        print("")
        return

    if args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", warn_col))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    G = fsa(name=args[0])

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
            colored("Insert a transition (in the format x0 a x1) [!q to abort, - to end]:\n", prompt_col)).split(
            ' ')
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

    fsalst[args[0]] = G
