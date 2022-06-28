from basic_CLI.cli_command import command

list_cli = command(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=0,
    f_name="list",
    description="Prints the FSA currently loaded",
    help_usage="list"
)
