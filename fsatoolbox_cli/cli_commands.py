import fsatoolbox
from fsatoolbox import trim, fm, diag, nfa2dfa, hhat, compute_supervisor
from fsatoolbox.analysis import get_reachability_info, get_co_reachability_info, get_blockingness_info, get_trim_info, \
    get_deadness_info
from fsatoolbox_cli.basic_cli_funct import *
from fsatoolbox_cli.command_analysis import command_analysis
from fsatoolbox_cli.command_basic import command_basic
from fsatoolbox_cli.command_fsa_func import command_fsa_func


def help():
    command_types = ['basic', 'functions', "analysis"]
    for ct in command_types:
        lines = "--------------------------------------"
        print(colored("\n" + lines + " " + ct.capitalize() + " " + lines + "\n", "green"))
        for key, value in cmdict.items():
            if value.category == ct:
                print(f'-> {colored(key, "yellow"):<24}', end='')
                print("" + cmdict[key].description)
    print("")


fsa_dict = dict()

help_cli = command_basic(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="help",
    callback=help,
    description="Prints the list of available commands"
)

chdir_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="chdir",
    callback=chdir_cli_f,
    description="This functions changes the default path",
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
    description="Prints the current working directory"
)

ldir_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=0,
    callback=ldir_cli_f,
    f_name="showdir",
    description="Prints the current working directory"
)

build_cli = command_basic(
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=1,
    callback=build_cli_f,
    fsa_dict=fsa_dict,
    f_name="build",
    description="Calls a wizard for build a FSA",
    help_usage="build fsa_name",
    help_example="build G0"
)

load_cli = command_basic(
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=[1, 2],
    callback=load_cli_f,
    fsa_dict=fsa_dict,
    f_name="load",
    description="Load a FSA from a file",
    help_usage="load fsa_name path_to_file",
    help_example="load G0 G0.fsa"
)

save_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=2,
    f_name="save",
    callback=save_cli_f,
    fsa_dict=fsa_dict,
    description="Saves a FSA into a file",
    help_usage="save fsa_to_save path_to_file",
    help_example="save G0 G0.fsa"
)

show_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="show",
    callback=showfsa_cli_f,
    fsa_dict=fsa_dict,
    description="Prints the structure of the FSA",
    help_usage="show fsa_name",
    help_example="show G0"
)

list_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="list",
    callback=list_cli_f,
    fsa_dict=fsa_dict,
    description="Prints the FSA currently loaded",
    help_usage="list"
)

remove_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="remove",
    callback=remove_cli_f,
    fsa_dict=fsa_dict,
    description="Removes a FSA",
    help_usage="remove fsa_name",
    help_example="remove G0"
)

clear_cli = command_basic(
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="clear",
    callback=clear_cli_f,
    fsa_dict=fsa_dict,
    description="Remove all the FSA",
    help_usage="clear"
)

cc_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=3,
    f_name="cc",
    callback=fsatoolbox.cc,
    fsa_dict=fsa_dict,
    description="This function computes the concurrent composition between two FSA",
    help_usage="cc output input1 input2",
    help_example="cc G2 G1 G0",
    help_optional=("-v", "verbose output, this will print the steps of the algorithm")
)

trimfsa_cli = command_fsa_func(
    category="functions",
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="trimfsa",
    callback=trim,
    fsa_dict=fsa_dict,
    description="This functions computes a trim of a FSA",
    help_usage="trimfsa output input",
    help_example="trimfsa G0 G1",
    help_optional=("-v", "verbose output, this will print the steps of the algorithm")
)

fm_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="fm",
    callback=fm,
    fsa_dict=fsa_dict,
    description="This functions computes the fault monitor of the given FSA",
    help_usage="fm output input",
    help_example="fm F1 F0",
)

diag_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="diag",
    callback=diag,
    fsa_dict=fsa_dict,
    description="This function computes the diagnoser of the given FSA",
    help_usage="diag output input",
    help_example="diag G1 G0",
    help_optional=("-v", "verbose output, this will print the steps of the algorithm")
)

obs_cli = command_fsa_func(
    category="functions",
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="obs",
    callback=nfa2dfa,
    fsa_dict=fsa_dict,
    description="This functions computes the equivalent DFA of the given NFA",
    help_usage="obs output input",
    help_example="obs G0 N0"
)

exth_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="exth",
    callback=hhat,
    fsa_dict=fsa_dict,
    description="This functions computes the extended specification automaton, given the specification automaton H",
    help_usage="exth output input",
    help_example="exth H2 H1",
)

supervisor_cli = command_fsa_func(
    category='functions',
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=3,
    f_name="supervisor",
    callback=compute_supervisor,
    fsa_dict=fsa_dict,
    description="This function computes the supervisor of an automaton G, given the specification automaton H",
    help_usage="super output input_automaton specif_automaton",
    help_example="super S G0 H0",
    help_optional=("-v", "verbose output, this will print the steps of the algorithm")

)

reach_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="reach",
    callback=get_reachability_info,
    fsa_dict=fsa_dict,
    description="This function computes the reachability of a FSA",
    help_usage="reach fsa_name",
    help_example="reach G0"
)

coreach_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="coreach",
    callback=get_co_reachability_info,
    fsa_dict=fsa_dict,
    description="This function computes the co-reachability of a FSA",
    help_usage="coreach fsa_name",
    help_example="coreach G0"
)

blocking_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="blocking",
    callback=get_blockingness_info,
    fsa_dict=fsa_dict,
    description="This functions computes if the FSA is blocking",
    help_usage="blocking fsa_name",
    help_example="blocking G0"
)

trim_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="trim",
    callback=get_trim_info,
    fsa_dict=fsa_dict,
    description="This functions computes if the FSA is trim",
    help_usage="trim fsa_name",
    help_example="trim G0"
)

dead_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="dead",
    callback=get_deadness_info,
    fsa_dict=fsa_dict,
    description="This functions computes if the FSA has dead states",
    help_usage="dead fsa_name",
    help_example="dead G0"
)

reverse_cli = command_analysis(
    category='analysis',
    input_formats=["standard", "matlab"],
    n_req_args=2,
    f_name="reverse",
    callback=command_analysis,
    fsa_dict=fsa_dict,
    description="This functions computes if the FSA is reversible",
    help_usage="reverse fsa_name",
    help_example="reverse G0"
)

cmdict = {
    'chdir': chdir_cli,
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
    'exth': exth_cli,
    'supervisor': supervisor_cli,
    'reach': reach_cli,
    'coreach': coreach_cli,
    'blocking': blocking_cli,
    'trim': trim_cli,
    'dead': dead_cli,
    'reverse': reverse_cli,
    'help': help_cli
}
