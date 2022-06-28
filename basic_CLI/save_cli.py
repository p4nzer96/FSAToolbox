from basic_CLI.cli_command import command

save_cli = command(
    category='basic',
    input_formats=["standard", "matlab"],
    n_req_args=2,
    f_name="save",
    description="Saves a FSA into a file",
    help_usage="save fsa_to_save path_to_file",
    help_example="save G0 G0.fsa"
)
