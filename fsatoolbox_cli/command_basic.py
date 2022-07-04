import inspect

from termcolor import colored

from fsatoolbox_cli.command import command


class command_basic(command):

    def __init__(self, input_formats, n_req_args, callback, category='basic', fsa_dict=None, **kwargs):
        super().__init__(category, input_formats, n_req_args, callback, fsa_dict, **kwargs)

    def func_call(self, args: list, opts: list):

        if "-h" in opts:
            self.helper()
            return

        if len(args) < min(self.n_req_args):
            print(colored("Not enough arguments provided, type \"{} -h\" to help", self.WARN_COLOR).format(self.f_name))

        elif len(args) in self.n_req_args:

            if "fsa_dict" in inspect.signature(self.callback).parameters:
                self.callback(*args, fsa_dict=self.fsa_dict)
            else:
                self.callback(*args)

        else:
            print(colored("Too much arguments provided, type \"{} -h\" to help", self.WARN_COLOR).format(self.f_name))
