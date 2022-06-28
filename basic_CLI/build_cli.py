from basic_CLI.cli_command import command

build_cli = command(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=1,
    description="This functions starts an interactive program to build a FSA",
    help_usage="build fsa_name",
    help_example="build G0")
