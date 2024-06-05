import click
from docker_ready import get_project_by_name, run_project

from docker_ready_cli.utils.tools import console


@click.command(name="run", help="Run project.")
@click.argument("project_name")
def run(project_name: str) -> None:
    if project := get_project_by_name(name=project_name):
        run_project(project=project)
    else:
        console.print(f"Project {project_name} not found.")


__all__ = ["run"]
