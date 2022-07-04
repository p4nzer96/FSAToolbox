from abc import ABC
from termcolor import colored
from fsatoolbox_cli.command import command


class command_analysis(command):

    def __init__(self, input_formats, n_req_args, callback, fsa_dict, category="analysis", **kwargs):
        super().__init__(category, input_formats, n_req_args, callback, fsa_dict, **kwargs)

    def func_call(self, args: list, opts: list):

        if "-h" in opts:
            self.helper()
            return

        # Checking the arguments

        # Too few arguments
        if len(args) < min(self.n_req_args):
            print(colored("Not enough arguments provided, type \"{} -h\" to help", self.WARN_COLOR).format(self.f_name))

        # Correct number of arguments
        elif len(args) > max(self.n_req_args):
            print(colored("Too much arguments provided, type \"{} -h\" to help", self.WARN_COLOR).format(self.f_name))
            return

        else:

            p_args = self._retrieve_fsa(args)
            self.callback(*p_args)

    def _retrieve_fsa(self, args):

        return [self.fsa_dict[x] for x in args if x and x in self.fsa_dict]
