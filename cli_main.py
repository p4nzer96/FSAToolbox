import os
import re
import shlex
import nltk
from termcolor import colored

from fsatoolbox.utils.check_determinism import ObsNotSet
from fsatoolbox_cli.cli_commands import cmdict


def levenstein_distance(chaine1, chaine2):
    return nltk.edit_distance(chaine1, chaine2)


def parse(inp):
    inp1 = shlex.split(inp, posix=False)
    if not inp1:
        return {'comm': None, 'args': [], 'opts': []}

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

        try:
            word_list = list(cmdict.keys())
            hamming_values = [levenstein_distance(p_command, x) for x in cmdict.keys()]
            nearest_word = word_list[hamming_values.index(min(hamming_values))]
            if min(hamming_values) <= 3:
                print(colored("Did you mean ", "red") + colored(nearest_word, "red", attrs=["bold"]) + colored("?",
                                                                                                               "red"))

        except Exception:
            print("")

        return False

    if pattern not in cmdict[p_command].input_formats:
        print(colored("ERROR: Input format not supported", "red"))
        return False

    return True


if __name__ == "__main__":

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    forg_color = 'green'
    back_color = 'cyan'
    back1_color = 'on_grey'
    splash = [" ███████╗███████╗ █████╗ ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗",
              " ██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝",
              " █████╗  ███████╗███████║   ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝ ",
              " ██╔══╝  ╚════██║██╔══██║   ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗ ",
              " ██║     ███████║██║  ██║   ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗",
              " ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝"]
    os.system('cls' if os.name == 'nt' else 'clear')  # clear term
    print("")
    for row in splash:
        for char in row:
            if char == '█':
                print(colored(char, forg_color), end='')
            else:
                print(colored(char, back_color, back1_color), end='')
        print("")

    print(colored("Alpha version \n", "green"))
    print(colored("Credits: ", "green") + colored("Andrea Panzino", "green", attrs=["bold"]) + colored(", ", "green")
          + colored("Dennis Loi ", "green", attrs=["bold"]) + colored("- University of Cagliari\n", "green"))
    print("Type " + colored("help", attrs=["bold"]) + " to see the list of commands")
    print("Instead type " + colored("exit", attrs=["bold"]) + " or press " + colored("CTRL+C", attrs=["bold"]) +
          " to quit\n")

    args = []
    opts = []

    cmdict["showdir"].func_call(args, opts)
    print("")

    while True:

        try:

            str_inp = input(">> ")

            pattern, inp = parse(str_inp)

            if checkinput(pattern, inp):

                comm_obj = cmdict[inp['comm']]
                args = [x for x in inp['args'] if x != ""]
                opts = [x for x in inp['opts'] if x != ""]

                if pattern == 'matlab' and comm_obj.category == "functions":
                    args.insert(0, None)

                comm_obj.func_call(args, opts)

        except KeyboardInterrupt:

            print("")
            exit()

        except ObsNotSet as obs_e:  # Need to set the "observable" property

            while True:
                print(colored("\nWARNING: To continue it is required to set the "
                              "observability property for the events of {}".format(obs_e.fsa.name), "yellow"))
                inp = input("Please input the observable events of {}, "
                            "separated by a space (events: {}): ".format(obs_e.fsa.name, str(obs_e.fsa.E)[1:-1]))

                # If the input is blank, abort the procedure
                if inp == "":
                    print(colored("Exit from the procedure", colored("yellow")))
                    break

                else:

                    # Check if the user as inputted non-existent events

                    wrong_events = []
                    for e in inp.split(" "):
                        if e not in obs_e.fsa.E:
                            wrong_events.append(e)

                    if len(wrong_events) > 0:
                        print(colored("Events {} does not belong to {}"
                                      .format(str(wrong_events)[1:-1], obs_e.fsa.name), "red"))
                        continue

                    # Set isObservable property of all the events of the current FSA

                    else:
                        for e in obs_e.fsa.E:
                            if e in inp.split(" "):
                                setattr(e, "isObservable", True)
                            else:
                                setattr(e, "isObservable", False)

                        # Call again the function
                        comm_obj.func_call(args, opts)
                        break



        except Exception:

            continue
