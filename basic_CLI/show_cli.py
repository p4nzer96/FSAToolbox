from basic_CLI.cli_command import command

show_cli = command(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="show",
    description="Prints the structure of the FSA",
    help_usage="show fsa_name",
    help_example="show G0"
)
