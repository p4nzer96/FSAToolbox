from abc import ABC, abstractmethod
from termcolor import colored
import colorama

colorama.init()


class command(ABC):

    def __init__(self, category, input_formats, n_req_args, **kwargs):
        self.category = category
        self.input_formats = input_formats
        self.n_req_args = n_req_args

        # Optional arguments to format the help

        self.f_name = kwargs.get('f_name')
        self.description = kwargs.get('description')
        self.help_usage = kwargs.get('help_usage')
        self.help_example = kwargs.get('help_example')
        self.help_optional = kwargs.get('help_optional')
        self.help_notes = kwargs.get('help_notes')

    @abstractmethod
    def func_call(self):
        pass

    def helper(self):

        print("")
        print(colored(self.f_name, "yellow", attrs=["bold"]) + ":\t{}\n".format(self.description))
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
