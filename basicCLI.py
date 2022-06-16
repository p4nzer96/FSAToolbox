import os
import shlex

import colorama
from termcolor import colored

from basic_CLI.analysis import reachability, coreachability, blocking, trim, dead, reverse
from basic_CLI.checkevents import updateevents
from basic_CLI.conccomp import conccomp
from basic_CLI.diagnoser import diagnoser
from basic_CLI.editfsa import addstate, rmstate, addevent, rmevent, addtrans, rmtrans, editstate
from basic_CLI.exth import exth
from basic_CLI.faultmon import faultmon
from basic_CLI.fsabuilder import fsabuilder
from basic_CLI.loadfsa import loadfsa
from basic_CLI.observer import observer
from basic_CLI.savefsa import savefsa
from basic_CLI.super import supervisor


# commands

def help(args, eventslst, fsalst, path):
    print("This is only a test version: available commands:\n")

    print(colored("-------------------------- Basic Commands  --------------------------", "green"))
    print("Commands used to load / save an FSA from / to file\n")

    print("-> " + colored("chdir", "yellow") + ":     \tChanges the current working directory")
    print("-> " + colored("showdir", "yellow") + ":  \tShows the current working directory")
    print("-> " + colored("ldir", "yellow") + ":     \tShows the current files into working directory")
    print("-> " + colored("load", "yellow") + ":     \tLoads a FSA from a file")
    print("-> " + colored("save", "yellow") + ":     \tSaves a FSA to a file")
    print("-> " + colored("build", "yellow") + ":     \tCalls a wizard to build the FSA")
    print("-> " + colored("show", "yellow") + ":     \tShow a FSA")
    print("-> " + colored("list", "yellow") + ":     \tLists all FSAs")
    print("-> " + colored("remove", "yellow") + ":     \tRemoves a FSA")

    print(colored("\n-------------------------- Edit FSA --------------------------", "green"))
    print("Commands used to edit a FSA\n")

    print("-> " + colored("addstate", "yellow") + ":\tAdds a state to a FSA")
    print("-> " + colored("rmstate", "yellow") + ": \tRemoves a state from a FSA")
    print("-> " + colored("editstate", "yellow") + ": \tEdits state proprieties")
    print("-> " + colored("addevent", "yellow") + ":\tAdds an event to a FSA")
    print("-> " + colored("rmevent", "yellow") + ": \tRemoves an event from a FSA")
    print("-> " + colored("elist", "yellow") + ":   \tLists all events of a FSA")
    print("-> " + colored("editevent", "yellow") + "\tEdits event properties")
    print("-> " + colored("addtrans", "yellow") + ":\tAdds a transition to a FSA")
    print("-> " + colored("rmtrans", "yellow") + ": \tRemoves a transition to a FSA")

    print(colored("\n-------------------------- FSA Functions --------------------------", "green"))
    print("Commands used to call functions on FSAs\n")

    print("-> " + colored("cc", "yellow") + ":       \tComputes the concurrent composition between two FSAs")
    print("-> " + colored("fm", "yellow") + ":       \tComputes the Fault Monitor of a FSA")
    print("-> " + colored("diag", "yellow") + ":     \tComputes the diagnoser of a FSA")
    print("-> " + colored("nfa2dfa", "yellow") + ":    \tConverts a NFA into a DFA")
    print("-> " + colored("supervisor", "yellow") + ":\tComputes the supervisor of a FSA")

    print(colored("\n-------------------------- FSA Analysis --------------------------", "green"))
    print("Functions for analyze a FSA\n")

    print("-> " + colored("reach", "yellow") + ":    \tComputes the reachability of a FSA")
    print("-> " + colored("coreach", "yellow") + ":    \tComputes the co-reachability of a FSA")
    print("-> " + colored("blocking", "yellow") + ":\tComputes if a FSA is blocking")
    print("-> " + colored("trim", "yellow") + ":    \tComputes if a FSA is trim")
    print("-> " + colored("dead", "yellow") + ":    \tComputes the dead states of a FSA")
    print("-> " + colored("reverse", "yellow") + ":   \tComputes if a FSA is reversbible")

    print(colored("\n[CTRL+C or exit to quit the program]\n", "red"))


def changepath(args, path):
    if '-h' in args:
        print(colored("\nchdir: ", "yellow", attrs=["bold"]) + "This functions changes the default path\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\tchdir newpath")
        print(colored("Example:", attrs=["bold"]) + "\n\tchdir C:\\\\Automi")
        print(colored("Notes: ", attrs=["bold"]) + "\n\t * In windows use \\\\ instead of \\ (ex. C:\\\\Automi) or "
                                                   "put the path in brackets (ex. \"C:\\Automi\\\")")
        return path

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"chdir -h\" to help", "red"))
        return path

    # Path is absolute

    if os.path.isabs(os.path.normpath(args[0])):
        if os.path.isdir(os.path.normpath(args[0])):
            return os.path.normpath(args[0])
        else:
            print(colored("Invalid path", "red"))
            return path

        # Path is not absolute

    else:
        tail = os.path.normpath(args[0])
        head = path
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
            return new_path
        else:
            print(colored("Invalid path", "red"))
            return head


def removefsa(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nremove:", "yellow", attrs=["bold"]) + " Removes a FSA\n")
        print(colored("Usage:\n\t", attrs=["bold"]) + "remove fsa_name")
        print(colored("Example:\n\t", attrs=["bold"]) + "remove G0")
        return

    if len(args) < 1:
        print("Not enough arguments provided, type \"rm -h\" to help")
        return

    if args[0] not in fsalst:
        print("fsa not found")
        return

    del fsalst[args[0]]


def currpath(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("showdir:", "yellow") + "Prints the current working directory")
    else:
        print(path)


def showfsa(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nshow: ", "yellow", attrs=["bold"]) + "Prints the structure of the FSA\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\tshow fsa_name")
        print(colored("Example:", attrs=["bold"]) + "\n\tshow G0")

    if len(args) < 1:
        print(colored("Not enough arguments provided", "red"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    print(fsalst[args[0]])


def lst(args, eventslst, fsalst, path):
    print("Elements in: " + path + "\\\n")
    l = os.listdir(path + "\\")  # files only
    for el in l:
        print(el)


def listfsa(args, eventslst, fsalst, path):  # TODO add some stats?

    if '-h' in args:
        print(colored("\nload: ", "yellow", attrs=["bold"]) + "Prints the FSAs currently loaded\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\tlist")

    for key, value in fsalst.items():
        print(key)


def listevents(args, eventslst, fsalst, path):
    for e in eventslst:
        print("- " + e.label + ":  Observable: " + str(e.isObservable) + ", Controllable: " + str(
            e.isControllable) + ", Fault: " + str(e.isFault))


def editevent(args, eventslst, fsalst, path):
    if '-h' in args:
        print("This function is used to edit an event that is loaded in the event list")
        print("Usage:\n->editevent event-name -options")
        print("-o set the event as observable")
        print("-c set the event as controllable")
        print("-f set the event as a fault event")
        return
    if len(args) < 1:
        print("Not enough arguments provided, type \"editevent -h\" to help")
        return

    if not (any(e.label == args[0] for e in eventslst)):
        print("Error, event not found in the event list")
        return

    e = [i for i in eventslst if i.label == args[0]][0]
    e.isObservable = ('-o' in args)
    e.isControllable = ('-c' in args)
    e.isFault = ('-f' in args)

    print("- " + e.label + ":  Observable: " + str(e.isObservable) + ", Controllable: " + str(
        e.isControllable) + ", Fault: " + str(e.isFault))

    updateevents(eventslst, fsalst)


colorama.init()  # fix for colored text with old cmd

# list of loaded FSA
fsalst = dict()
eventslst = []

commands = {
    'chdir': changepath,
    'showdir': currpath,
    'load': loadfsa,
    'remove': removefsa,
    'save': savefsa,
    'build': fsabuilder,
    'addstate': addstate,
    'rmstate': rmstate,
    'addevent': addevent,
    'rmevent': rmevent,
    'addtrans': addtrans,
    'rmtrans': rmtrans,
    'show': showfsa,
    'reach': reachability,
    'coreach': coreachability,
    'blocking': blocking,
    'trim': trim,
    'dead': dead,
    'reverse': reverse,
    'ldir': lst,
    'list': listfsa,
    'elist': listevents,
    'editevent': editevent,
    'editstate': editstate,
    'cc': conccomp,
    'fm': faultmon,
    'diag': diagnoser,
    'nfa2dfa': observer,
    'obs': observer,
    'supervisor': supervisor,
    'exth': exth,
    'help': help
}

home = os.path.normpath(os.path.expanduser("~"))
path = home + '/Documents/FsaToolbox'

if not os.path.exists(path):
    os.makedirs(path)

# splashscreen
forg_color = 'green'
back_color = 'cyan'
back1_color = 'on_grey'
splash = [" ███████╗███████╗ █████╗ ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗",
          " ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝",
          " █████╗  ███████╗███████║   ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝ ",
          " ██╔══╝  ╚════██║██╔══██║   ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗ ",
          " ██║     ███████║██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗",
          " ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝"]
print("")
for row in splash:
    for char in row:
        if char == '█':
            print(colored(char, forg_color), end='')
        else:
            print(colored(char, back_color, back1_color), end='')
    print("")

print("Note: this is still in development")
print("Type \"help\" to see the list of commands")
print("\n\nNote: the default path is:")
print(path)
print("")

while 1:
    try:
        cmd = shlex.split(input(">>"), posix=False)
        if not cmd:
            continue
        args = cmd[1:]  # extract arguments

        if cmd[0] == 'chdir':
            path = changepath(args, path)
            continue
        if cmd[0] == 'exit':
            break
        if cmd[0] in commands:
            commands[cmd[0]](args, eventslst, fsalst, path)
        else:
            print(colored("Unrecognized command", "red"))
    except KeyboardInterrupt:
        exit()
