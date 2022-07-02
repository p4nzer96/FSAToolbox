import os
import re
import shlex
import colorama

from termcolor import colored
from fsatoolbox_cli.cli_commands import cmdict

colorama.init()


def parse(inp):
    inp1 = shlex.split(inp, posix=False)
    if not inp1: return {'comm': None, 'args': [], 'opts': []}

    # remove spaces
    inp_noSpaces = inp.replace(" ", "")

    # pattern a=b(c,d)
    if re.compile('.*=.*\(.*\)').match(inp_noSpaces):

        # the command is between '=' and '('
        comm = inp_noSpaces.split('=')[1].split('(')[0]

        # the first argument is before '='
        args = [inp_noSpaces.split('=')[0]]
        # the other arguments are between the first and last parenthesis, splitted by a comma
        args = args + inp_noSpaces.split("(")[1].split(")")[0].split(',')

        # The options are after the parenthesis, marked by a '-' before
        try:
            opts = re.findall('-[a-zA-Z]+', inp_noSpaces.split(')')[-1])
        except AttributeError:
            opts = []

        pattern = 'matlab_eq'

        return pattern, {'comm': comm, 'args': args, 'opts': opts}

    # pattern a(b,c)
    if re.compile('.*\(.*\)').match(inp_noSpaces):

        # the command is before '('
        comm = inp_noSpaces.split('(')[0]

        # the arguments are between the first and last parenthesis, splitted by a comma
        args = inp_noSpaces.split("(")[1].split(")")[0].split(',')

        # The options are after the parenthesis, marked by a '-' before
        try:
            opts = re.findall('-[a-zA-Z]+', inp_noSpaces.split(')')[-1])
        except AttributeError:
            opts = []
            opts.append('-printOnly')

        pattern = 'matlab'

        return pattern, {'comm': comm, 'args': args, 'opts': opts}

    # pattern a b c d
    inp = list(filter(None, inp.split(' ')))  # split by spaces

    comm = inp[0] if len(inp) > 0 else None
    args = [x for x in inp[1:] if '-' not in x]
    opts = [x for x in inp[1:] if '-' in x]

    pattern = 'standard'

    return pattern, {'comm': comm, 'args': args, 'opts': opts}


def checkinput(pattern, inp):
    p_command = inp['comm']

    if p_command not in cmdict.keys():
        print(colored("ERROR: Unrecognized command", "red"))
        return False

    if pattern not in cmdict[p_command].input_formats:
        print(colored("ERROR: Input format not supported", "red"))
        return False

    return True


command_list = [
    "chdir C:\\Users\\andre\\Desktop\\Automi\\Examples",
    "showdir",
    "list",
    "load G0.json",
    "load G1.json",
    "remove(G0)",
    "list",
    "remove(G1)",
    "G0 = load(G0.json)",
    "load(G1, G1.json)",
    "clear",
    "G1 = load(G1.json)",
    "G0 = load(G0.json)",
    "load(F1.txt)",
    "list",
    "cc(G0, G1)",
    "G2 = cc(G0, G1)",
    "load(Gs.json)",
    "load(Hs.json)",
    "supervisor(Gs, Hs)",
    "S = supervisor(Gs, Hs)"
]
for command in command_list:

    print("\n" + colored(command, "green", attrs=["bold"]))

    pattern, inp = parse(command)

    if checkinput(pattern, inp):

        comm_obj = cmdict[inp['comm']]
        args = [x for x in inp['args'] if x != ""]
        opts = [x for x in inp['opts'] if x != ""]

        if pattern == 'matlab' and comm_obj.category == "functions":
            args = [None] + args

        print(args)

        comm_obj.func_call(args, opts)
