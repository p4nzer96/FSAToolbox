from fsatoolbox import nfa2dfa, hhat, compute_supervisor, cc, trim
from fsatoolbox_cli.analysis import reachability_cli, coreachability_cli, blocking_cli, trim_cli, dead_cli, reverse_cli
from fsatoolbox_cli.basic_cli_funct import *
from fsatoolbox_cli.command_analysis import command_analysis
from fsatoolbox_cli.command_basic import command_basic
from fsatoolbox_cli.command_fsa_func import command_fsa_func
from fsatoolbox_cli.functions import fm_cli, diag_cli


def help(cmd=None):

    if(cmd==None):
        command_types = ['basic', 'functions', "analysis"]
        for ct in command_types:
            lines = "--------------------------------------"
            print(colored("\n" + lines + " " + ct.capitalize() + " " + lines + "\n", "green"))
            for key, value in cmdict.items():
                if value.category == ct:
                    print(f'-> {colored(key, "yellow"):<24}', end='')
                    print("" + cmdict[key].description)
        print("")
    else:
        if cmd not in cmdict:
            print(colored(cmd+" not found","red"))
            print(colored("Type \"help\" to show the list of available commands","yellow"))
            return
        cmdict[cmd].helper()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


fsa_dict = dict()

help_cli = command_basic(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=[0, 1],
    f_name="help",
    callback=help,
    description="Prints the list of available commands"
)

exit_cli = command_basic(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="exit",
    callback=exit_cli,
    description="Quits the program"
)

cls_cli = command_basic(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="cls",
    callback=cls,
    description="Clears the CLI"
)

chdir_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="chdir",
    callback=chdir_cli_f,
    description="This function changes the default path",
    help_usage="chdir newpath",
    help_example="chdir C:\\\\Automi",
    help_notes=["In windows use \\\\ instead of \\ (ex. C:\\\\Automi) or put "
                "the path in brackets (ex. \"C:\\Automi\\\")"]
)

showdir_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=0,
    callback=showdir_cli_f,
    f_name="showdir",
    description="Shows the current working directory"
)

ldir_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=0,
    callback=ldir_cli_f,
    f_name="ldir",
    description="Shows the contents of the current working directory"
)

build_cli = command_basic(
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=1,
    callback=build_cli_f,
    fsa_dict=fsa_dict,
    f_name="build",
    description="Calls a wizard for build a FSA",
    help_usage="build G0"
)

load_cli = command_basic(
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=[1, 2],
    callback=load_cli_f,
    fsa_dict=fsa_dict,
    f_name="load",
    description="Loads a FSA from a file",
    help_usage="load G0 G0.fsa"
)

save_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=2,
    f_name="save",
    callback=save_cli_f,
    fsa_dict=fsa_dict,
    description="Saves a FSA into a file",
    help_usage="save G0 G0.fsa"
)

show_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="show",
    callback=showfsa_cli_f,
    fsa_dict=fsa_dict,
    description="Shows the structure of the FSA",
    help_usage="show G0"
)

list_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="list",
    callback=list_cli_f,
    fsa_dict=fsa_dict,
    description="Shows the FSA currently loaded in memory",
    help_usage="list"
)

remove_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="remove",
    callback=remove_cli_f,
    fsa_dict=fsa_dict,
    description="Removes a FSA from memory",
    help_usage="remove G0"
)

clear_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="clear",
    callback=clear_cli_f,
    fsa_dict=fsa_dict,
    description="Removes all the FSA from memory",
    help_usage="clear"
)

cc_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=3,
    f_name="cc",
    callback=cc,
    fsa_dict=fsa_dict,
    description="Computes G = G1||G2: concurrent composition of Fsa G1 and G2",
    help_usage="cc G G1 G2",
    help_optional={"-v": "verbose output, this will print the steps of the algorithm"}
)

trimfsa_cli = command_fsa_func(
    category="functions",
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="trimfsa",
    callback=trim,
    fsa_dict=fsa_dict,
    description="Trims a FSA",
    help_usage="trimfsa G0 G1",
    help_optional={"-v": "verbose output, this will print the steps of the algorithm"}
)

fm_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="fm",
    callback=fm_cli,
    fsa_dict=fsa_dict,
    description="Computes the fault monitor F of the given FSA G",
    help_usage="fm F G",
)

diag_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="diag",
    callback=diag_cli,
    fsa_dict=fsa_dict,
    description="Computes the diagnoser of the given FSA",
    help_usage="diag G1 G0",
    help_optional={"-v": "verbose output, this will print the Fault Monitor and the Fault Recognizer"}
)

obs_cli = command_fsa_func(
    category="functions",
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="obs",
    callback=nfa2dfa,
    fsa_dict=fsa_dict,
    description="Computes the equivalent DFA of the given NFA",
    help_usage="obs G0 N0"
)

supervisor_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=3,
    f_name="supervisor",
    callback=compute_supervisor,
    fsa_dict=fsa_dict,
    description="Computes the supervisor of an automaton G, given the specification automaton H",
    help_usage="supervisor S G0 H0",
    help_optional={"-v": "verbose output, this will print the steps of the algorithm"}

)

reach_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="reach",
    callback=reachability_cli,
    fsa_dict=fsa_dict,
    description="Computes the reachability of a FSA",
    help_usage="reach G0"
)

coreach_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="coreach",
    callback=coreachability_cli,
    fsa_dict=fsa_dict,
    description="Computes the co-reachability of a FSA",
    help_usage="coreach G0"
)

blocking_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="blocking",
    callback=blocking_cli,
    fsa_dict=fsa_dict,
    description="Computes if the FSA is blocking",
    help_usage="blocking G0"
)

trim_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="trim",
    callback=trim_cli,
    fsa_dict=fsa_dict,
    description="Computes if the FSA is trim",
    help_usage="trim G0"
)

dead_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="dead",
    callback=dead_cli,
    fsa_dict=fsa_dict,
    description="Computes if the FSA has dead states",
    help_usage="dead G0"
)

reverse_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="reverse",
    callback=reverse_cli,
    fsa_dict=fsa_dict,
    description="Computes if the FSA is reversible",
    help_usage="reverse G0"
)

cmdict = {
    'exit': exit_cli,
    'cd': chdir_cli,
    'showdir': showdir_cli,
    'ldir': ldir_cli,
    'load': load_cli,
    'save': save_cli,
    'build': build_cli,
    'show': show_cli,
    'list': list_cli,
    'remove': remove_cli,
    'clear': clear_cli,
    'cc': cc_cli,
    'trimfsa': trimfsa_cli,
    'fm': fm_cli,
    'diag': diag_cli,
    'obs': obs_cli,
    'supervisor': supervisor_cli,
    'reach': reach_cli,
    'coreach': coreach_cli,
    'blocking': blocking_cli,
    'trim': trim_cli,
    'dead': dead_cli,
    'reverse': reverse_cli,
    'help': help_cli,
    'cls': cls_cli
}
