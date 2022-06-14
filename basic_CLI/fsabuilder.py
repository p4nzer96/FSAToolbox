import fsatoolbox
from fsatoolbox import *
from basic_CLI.checkevents import checkevents


# TODO add exit (abort) option in every input

def fsabuilder(args, eventslst, fsalst, path):
    if len(args) < 1:
        print("Not enough arguments provided, type \"build -h\" to help")
        return

    if '-h' in args:
        print("This functions starts an interactive program to build an fsa")
        print("Usage:\n     build name (ex: build G0)")
        return

    if args[0] in fsalst:
        print("Name already in use")
        return

    G = fsa()

    # states
    inp = input("Insert the states, separated by a space: ").split(' ')

    while "" in inp:  # remove empty strings or double spaces
        inp.remove("")

    if len(inp) != len(set(inp)):
        print("Warning, some duplicate states will be considered only once")  # da riscrivere
        inp = set(inp)
    X = []
    for x in inp:
        X.append(state(x))

    state_prop = {  # name (for the prompt) and attribute name
        'initial': 'isInitial',
        'final': 'isFinal',
        'forbidden': 'isForbidden'
    }

    # TODO: Gestire il problema dello stato inserito non esistente

    for name, attr in state_prop.items():
        inp = input("Insert the " + name + " states, separated by a space [- to skip]: ").split(' ')
        if inp != ['-']:
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
    inp = input("Insert the events, separated by a space: ").split(' ')

    while "" in inp:  # remove empty strings or double spaces
        inp.remove("")

    if len(inp) != len(set(inp)):
        print("Warning, events are duplicate. Will be considered only once")  # da riscrivere
        inp = set(inp)
    E = []
    for e in inp:
        E.append(event(e))

    event_prop = {
        'observable': 'isObservable',
        'controllable': 'isControllable',
        'faulty': 'isFault'
    }

    # TODO: Gestire il problema dell'evento inserito non esistente

    for name, attr in event_prop.items():
        inp = input("Insert the " + name + " events, separated by a space [- to skip]: ").split(' ')
        if inp != ['-']:
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
    while 1:
        inp = input("Insert a transition (in the format x0 a x1) [!q to exit]: ").split(' ')
        if inp[0] == '!q' or inp[0] == '':
            break
        if not len(inp) == 3:
            print("Incorrect transition format")
            continue
        else:
            try:
                G.add_transition(inp[0], inp[1], inp[2])
            except:
                pass

    checkevents(G, eventslst, fsalst)

    fsalst[args[0]] = G
