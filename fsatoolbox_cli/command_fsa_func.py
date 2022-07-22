from termcolor import colored
from fsatoolbox_cli.command import command


class command_fsa_func(command):

    def __init__(self, input_formats, n_req_args, callback, fsa_dict, category="functions", **kwargs):
        super().__init__(category, input_formats, n_req_args, callback, fsa_dict, **kwargs)

    def func_call(self, args: list, opts: list):

        # Check if I have to print the help

        if "-h" in opts:
            self.helper()
            return

        # Checking the arguments

        # (ERROR) Too few arguments
        if len(args) < min(self.n_req_args):
            print(colored("Not enough arguments provided, type \"{} -h\" to help", self.WARN_COLOR).format(self.f_name))
            return

        # (ERROR) Too many arguments
        elif len(args) > max(self.n_req_args):
            print(colored("Too much arguments provided, type \"{} -h\" to help", self.WARN_COLOR).format(self.f_name))
            return

        # Correct number of arguments
        else:

            # Do I just have to show the result?
            if not args[0]:
                show_mode = True
            else:
                show_mode = False

            # Overwrite an exising fsa?
            if show_mode is False and args[0] in self.fsa_dict:
                inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
                if inp.lower() == 'n' or inp == '':
                    return

            # Are there any FSA not present in the fsa_dict?
            missing_fsa = [x for x in args[1:] if x not in self.fsa_dict.keys()]

            if len(missing_fsa) > 0:
                print(colored("Error, the following FSA do not exists: " + str(missing_fsa)[1:-1], "red"))
                return

            try:

                # Function call
                p_args = self._retrieve_fsa(args)
                result = self.callback(*p_args, verbose=('-v' in opts))

                if show_mode is True:
                    print(result)
                else:
                    self.fsa_dict[args[0]] = result

            except Exception as e:
                print(colored("There was an error while computing the function:", "red"))
                print(e)
                return

    def _retrieve_fsa(self, args):

        retrieved = []

        for x in args:
            if x and x in self.fsa_dict:
                if self.fsa_dict[x] not in retrieved:
                    retrieved.append(self.fsa_dict[x])

        return retrieved
