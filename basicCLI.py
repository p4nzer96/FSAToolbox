import os
import shlex

import colorama
from termcolor import colored

from basic_CLI.trimfsa import trimfsa
from basic_CLI.analysis import reachability, coreachability, blocking, trim, dead, reverse
from basic_CLI.conccomp import cc_CLI
from basic_CLI.diagnoser import diagnoser
from basic_CLI.editfsa import addstate, rmstate, addevent, rmevent, addtrans, rmtrans, editstate
from basic_CLI.exth import exth
from basic_CLI.faultmon import faultmon
from basic_CLI.fsabuilder import build_CLI
from basic_CLI.load_CLI import load_CLI
from basic_CLI.observer import observer
from basic_CLI.savefsa import save_CLI
from basic_CLI.super import supervisor


# commands

def help(args, fsalst):
    print("This is only a test version: available commands:\n")

    print(colored("-------------------------- Basic Commands  --------------------------", "green"))
    print("Commands used to create / delete a FSA\n")

    print("-> " + colored("chdir", "yellow") + ":     \tChanges the current working directory")
    print("-> " + colored("showdir", "yellow") + ":  \tShows the current working directory")
    print("-> " + colored("ldir", "yellow") + ":     \tShows the current files into working directory")
    print("-> " + colored("load", "yellow") + ":     \tLoads a FSA from a file")
    print("-> " + colored("save", "yellow") + ":     \tSaves a FSA to a file")
    print("-> " + colored("build", "yellow") + ":     \tCalls a wizard to build the FSA")
    print("-> " + colored("show", "yellow") + ":     \tShow a FSA")
    print("-> " + colored("list", "yellow") + ":     \tLists all FSA")
    print("-> " + colored("remove", "yellow") + ":     \tRemoves a FSA")

    print(colored("\n-------------------------- Edit FSA --------------------------", "green"))
    print("Commands used to edit a FSA\n")

    print("-> " + colored("addstate", "yellow") + ":\tAdds a state to a FSA")
    print("-> " + colored("rmstate", "yellow") + ": \tRemoves a state from a FSA")
    print("-> " + colored("editstate", "yellow") + ": \tEdits state proprieties")
    print("-> " + colored("addevent", "yellow") + ":\tAdds an event to a FSA")
    print("-> " + colored("rmevent", "yellow") + ": \tRemoves an event from a FSA")
    print("-> " + colored("elist", "yellow") + ":   \tLists all events of a FSA")
    print("-> " + colored("editevent", "yellow") + ":\tEdits event properties")
    print("-> " + colored("addtrans", "yellow") + ":\tAdds a transition to a FSA")
    print("-> " + colored("rmtrans", "yellow") + ": \tRemoves a transition to a FSA")

    print(colored("\n-------------------------- FSA Functions --------------------------", "green"))
    print("Commands used to call functions on FSA\n")

    print("-> " + colored("cc", "yellow") + ":       \tComputes the concurrent composition between two FSA")
    print("-> " + colored("trimfsa", "yellow") + ":  \tComputes the a trim of a FSA")
    print("-> " + colored("fm", "yellow") + ":       \tComputes the Fault Monitor of a FSA")
    print("-> " + colored("diag", "yellow") + ":     \tComputes the diagnoser of a FSA")
    print("-> " + colored("obs", "yellow") + ":       \tConverts a NFA into a DFA")
    print("-> " + colored("exth", "yellow") + ":      \tComputes the extended specification automaton")
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
        print(colored("\nchdir: ", "yellow", attrs=["bold"]) + "This functions changes the default path")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tchdir newpath")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tchdir C:\\\\Automi")
        print(colored("\nNotes: ", attrs=["bold"]) + "\n\t * In windows use \\\\ instead of \\ (ex. C:\\\\Automi) or "
                                                     "put the path in brackets (ex. \"C:\\Automi\\\")")
        print("")
        return path

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"chdir -h\" to help", "yellow"))
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


def removefsa(args, fsalst):
    if '-h' in args:
        print(colored("\nremove:", "yellow", attrs=["bold"]) + " Removes a FSA")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tremove fsa_name")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tremove G0")
        print("")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"remove -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print("fsa not found")
        return

    del fsalst[args[0]]


def currpath(args, fsalst, path):
    if '-h' in args:
        print(colored("\nshowdir: ", "yellow", attrs=["bold"]) + "Prints the current working directory\n")
    else:
        print(path)


def showfsa(args, fsalst):
    if '-h' in args:
        print(colored("\nshow: ", "yellow", attrs=["bold"]) + "Prints the structure of the FSA")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tshow fsa_name")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tshow G0")
        print("")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided", "red"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    print(fsalst[args[0]])


def lst(args, fsalst):
    if '-h' in args:
        print(colored("\nldir: ", "yellow", attrs=["bold"]) + "Show files/dirs inside current working folder")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tldir")
        print("")
        return

    print(colored("\nElements in: ", "yellow", attrs=["bold"]) + path + "\\\n")
    l = os.listdir(path + "\\")  # files only
    for el in l:
        print(el)
    print("")


def listfsa(args, fsalst):  # TODO add some stats?

    if '-h' in args:
        print(colored("\nlist: ", "yellow", attrs=["bold"]) + "Prints the FSA currently loaded")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tlist")
        print("")

    for key, value in fsalst.items():
        print(key)

# def editevent(args, fsalst):
#     if '-h' in args:
#         print(colored("\neditevent: ", "yellow",
#                       attrs=["bold"]) + "This function is used to edit an event that is loaded in the event list")
#         print(colored("\nUsage:", attrs=["bold"]) + "\n\teditevent event-name -options")
#         print(colored("\nOptions:", attrs=["bold"]) +
#               "\n\t-o set the event as observable" +
#               "\n\t-c set the event as controllable" +
#               "\n\t-f set the event as a fault event")
#         print(colored("\nExample:", attrs=["bold"]) + "\n\teditevent a -o")
#         print("")
#         return
#     if len(args) < 1:
#         print(colored("Not enough arguments provided, type \"editevent -h\" to help", "yellow"))
#         return

#     if not (any(e.label == args[0] for e in eventslst)):
#         print(colored("Error, event not found in the event list", "red"))
#         return

#     e = [i for i in eventslst if i.label == args[0]][0]
#     e.isObservable = ('-o' in args)
#     e.isControllable = ('-c' in args)
#     e.isFault = ('-f' in args)

#     print("- " + e.label + ":  Observable: " + str(e.isObservable) + ", Controllable: " + str(
#         e.isControllable) + ", Fault: " + str(e.isFault))



colorama.init()  # fix for colored text with old cmd

# list of loaded FSA
fsalst = dict()
eventslst = []

commandsPath = {
    'chdir': changepath,
    'showdir': currpath,
    'load': load_CLI,
    'save': save_CLI,
}

commands = {
    'remove': removefsa,
    'build': build_CLI,
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
    # 'editevent': editevent,
    'editstate': editstate,
    'cc': cc_CLI,
    'trimfsa': trimfsa,
    'fm': faultmon,
    'diag': diagnoser,
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

        if cmd[0] == 'exit':
            break

        #check if the input is the function format -> todo fun?
        if  "(" in cmd[0] and ")" in cmd[0]: #TODO regex
            if '=' in cmd[0]:
                dest=cmd[0].split('=')[0]
                comm=cmd[0].split('=')[1].split('(')[0]
                args=cmd[0].split('(')[1].split(')')[0].split(',')
                opts=cmd[1:]
            else:
                dest=None
                comm=cmd[0].split('(')[0]
                args=cmd[0].split('(')[1].split(')')[0].split(',')
                opts=cmd[1:]
        else:
            comm = cmd[0]
            if len(cmd)>1:
                dest=cmd[1]
                args = [x for x in cmd[1:] if '-' not in x]
                opts = [x for x in cmd[1:] if '-' in x]
            else:
                dest=None
                args=None
                opts=None
            
        if comm in commandsPath:
            commandsPath[comm](dest=dest, args=args, opts=opts, fsalst=fsalst, path=path)
        
        elif comm in commands:
            commands[comm](dest=dest, args=args, opts=opts, fsalst=fsalst)
        
        else:
            print(colored("Unrecognized command", "red"))
    except KeyboardInterrupt:
        exit()
