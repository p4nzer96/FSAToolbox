from abc import ABC, abstractmethod
from termcolor import colored
import colorama

colorama.init()


class command(ABC):

    def __init__(self, category, input_formats, n_req_args, callback, fsa_dict, **kwargs):

        self.callback = callback
        self.input_formats = input_formats  # Supported input formats
        self.n_req_args = [n_req_args] if not isinstance(n_req_args, list) else n_req_args  # Req. arguments
        self.category = category  # Command category
        self.fsa_dict = fsa_dict  # Dict containing all the FSA currently loaded

        # Optional arguments to format the help

        self.f_name = kwargs.get('f_name')
        self.description = kwargs.get('description')
        self.help_usage = kwargs.get('help_usage')
        self.help_example = kwargs.get('help_example')
        self.help_optional = kwargs.get('help_optional')
        self.help_notes = kwargs.get('help_notes')

        self.WARN_COLOR = "yellow"
        self.ERR_COLOR = "red"

    @abstractmethod
    def func_call(self, args: list, opts: list):
        pass

    def helper(self):

        print("")
        print(colored(self.f_name, self.WARN_COLOR, attrs=["bold"]) + ":\t{}\n".format(self.description))
        if self.help_usage:
            print(colored("\nUsage:", attrs=["bold"]) + "\n\t{}".format(self.help_usage))
        if self.help_optional:
            print(colored("\nOptional Arguments:", attrs=["bold"]))
            for opt_arg, opt_desc in self.help_optional:
                print("\n\t{} {}".format(opt_arg, opt_desc))
        if self.help_example:
            print(colored("\nExample:", attrs=["bold"]) + "\n\t{}".format(self.help_example))
        if self.help_notes:
            print(colored("\nNotes:", attrs=["bold"]))
            for note in self.help_optional:
                print("\n\t* {}".format(note))
        print("")
