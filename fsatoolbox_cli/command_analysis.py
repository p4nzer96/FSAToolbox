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

        # Too many arguments
        elif len(args) > max(self.n_req_args):
            print(colored("Too many arguments provided, type \"{} -h\" to help", self.WARN_COLOR).format(self.f_name))
            return

        # Correct number of arguments
        else:
            # Are there any FSA not present in the fsa_dict?
            missing_fsa = [x for x in args if x not in self.fsa_dict.keys()]

            if len(missing_fsa) > 0:
                print(colored("Error, the following FSA do not exists: " + str(missing_fsa)[1:-1], "red"))
                return

            try:
                # Function call
                p_args = self._retrieve_fsa(args)
                self.callback(*p_args)
            except Exception as e:
                print(colored("There was an error while computing the analysis:", "red"))
                print(e)
                return

    def _retrieve_fsa(self, args):

        return [self.fsa_dict[x] for x in args if x and x in self.fsa_dict]
