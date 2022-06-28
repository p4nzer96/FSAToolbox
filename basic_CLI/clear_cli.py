from basic_CLI.cli_command import command

clear_cli = command(
    category="basic",
    input_formats=["standard"],
    n_req_args=0,
    f_name="clear",
    description="Remove all the FSA",
    help_usage="clear"
)
