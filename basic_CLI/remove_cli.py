from basic_CLI.cli_command import command

remove_cli = command(
    category="basic",
    input_formats=["standard", "matlab"],
    n_req_args=1,
    f_name="remove",
    description="Removes a FSA",
    help_usage="remove fsa_name",
    help_example="remove G0"
)
