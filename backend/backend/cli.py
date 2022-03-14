#!/bin/python
import click
from constants import ADMIN_CONTAINER_NAME
from data_management.cli import cli as cli_data
from utils.shell import is_running_container
from utils.shell import run_command_in_container
from utils.shell import run_command_in_shell


@click.group(name="cli", context_settings={"show_default": True})
def cli():
    pass


@cli.command(
    context_settings={"ignore_unknown_options": True},
    help="Run commands in docker container.",
)
@click.option("-t", "--target-container", default=ADMIN_CONTAINER_NAME)
@click.argument("container_args", nargs=-1, type=click.UNPROCESSED)
def docker(target_container: str, container_args: tuple[str]):
    if is_running_container("docker", target_container):
        run_command_in_container(
            "docker",
            target_container,
            f"cd backend && python cli.py {' '.join(container_args)}"
        )
        return

    click.echo(f"Could not find running container '{target_container}'")


@cli.command(
    context_settings={"ignore_unknown_options": True},
    help="Run shell commands.",
)
@click.argument("shell_cmd_segments", nargs=-1, type=click.UNPROCESSED)
def shell(shell_cmd_segments: tuple[str]):
    run_command_in_shell(" ".join(shell_cmd_segments))


cli.add_command(cli_data, "data")


if __name__ == "__main__":
    cli()
