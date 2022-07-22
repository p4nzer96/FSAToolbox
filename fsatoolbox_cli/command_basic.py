import inspect

from termcolor import colored

from fsatoolbox_cli.command import command


class command_basic(command):

    def __init__(self, input_formats, n_req_args, callback, category='basic', fsa_dict=None, **kwargs):
        super().__init__(category, input_formats, n_req_args, callback, fsa_dict, **kwargs)

    def func_call(self, args: list, opts: list):

        # Check if I have to print the help
        if "-h" in opts:
            self.helper()
            return

        # (ERROR) Too few arguments
        if len(args) < min(self.n_req_args):
            print(colored("Not enough arguments provided, type \"help {}\" to help", self.WARN_COLOR).format(self.f_name))

        # Correct number of arguments
        elif len(args) in self.n_req_args:

            try:
                if "fsa_dict" in inspect.signature(self.callback).parameters:
                    self.callback(*args, fsa_dict=self.fsa_dict)
                else:
                    self.callback(*args)
            except Exception as e:
                print(colored("There was an error:", "red"))
                print(e)
                return

        # (ERROR) Too many arguments
        else:
            print(colored("Too many arguments provided, type \"help {}\" to help", self.WARN_COLOR).format(self.f_name))
