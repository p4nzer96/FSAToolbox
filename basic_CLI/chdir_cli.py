from basic_CLI.cli_command import command

chdir_cli = \
    command(
        category='basic',
        input_formats=["standard"],
        n_req_args=1,
        f_name="chdir",
        description="This functions changes the default path",
        help_usage="chdir newpath",
        help_example="chdir C:\\\\Automi",
        help_notes=["In windows use \\\\ instead of \\ (ex. C:\\\\Automi) or put "
                    "the path in brackets (ex. \"C:\\Automi\\\")"]
    )