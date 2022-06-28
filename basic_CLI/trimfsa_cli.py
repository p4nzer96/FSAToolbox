from basic_CLI.cli_command import command

trimfsa_cli = command(
    category="functions",
    input_formats=["standard", "matlab", "matlab_eq"],
    n_req_args=2,
    f_name="trimfsa",
    description="This functions computes a trim of a FSA",
    help_usage="trimfsa output input",
    help_example="trimfsa G0 G1",
    help_optional=("-v", "verbose output, this will print the steps of the algorithm")
)
