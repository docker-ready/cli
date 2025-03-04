import click

from docker_ready_cli.commands import ps, run, show


@click.group()
def cli() -> None:
    pass


cli.add_command(run)
cli.add_command(show)
cli.add_command(ps)


if __name__ == "__main__":
    cli()
