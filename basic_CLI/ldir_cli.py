from basic_CLI.cli_command import command

ldir_cli = command(
    category='basic',
    input_formats=["standard"],
    n_req_args=0,
    f_name="showdir",
    description="Prints the current working directory"
)
