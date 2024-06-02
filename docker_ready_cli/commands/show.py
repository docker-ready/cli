import click
from docker_ready import get_all_projects, get_project_by_name
from rich.table import Table

from docker_ready_cli.utils.tools import console


@click.command(name="show", help="Show project information.")
@click.option("--name", help="Project name.", default=None)
def show(name: str | None) -> None:
    if name:
        _show_project_by_name(name=name)
    else:
        _show_all_projects()


def _show_all_projects() -> None:
    table = Table(title="All available projects", show_lines=True)
    table.add_column(header="Name")
    table.add_column(header="Description")

    for project in get_all_projects():
        info = project.info
        table.add_row(project.compose.name, info.description)

    console.print(table)


def _show_project_by_name(name: str) -> None:
    if project := get_project_by_name(name=name):
        table = Table(title=f"Information about {name} project", show_header=False, show_lines=True)
        table.add_column()
        table.add_column()
        table.add_row("[bold]Name", project.compose.name)
        table.add_row("[bold]Full name", project.info.full_name)
        table.add_row("[bold]Description", project.info.description)
        table.add_row("[bold]Site", str(project.info.site_url))
        table.add_row("[bold]Repository", str(project.info.repo_url))
        table.add_row("[bold]Container registry", str(project.info.container_registry_url))

        console.print(table)
    else:
        console.print(f"Project {name} not found.")


__all__ = ["show"]
