from basic_CLI.cli_command import command

obs_cli = command(
    category="functions",
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="obs",
    description="This functions computes the equivalent DFA of the given NFA",
    help_usage="obs outputname inputname",
    help_example="obs G0 N0")
