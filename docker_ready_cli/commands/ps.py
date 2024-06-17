import click
from dateutil.parser import parse
from docker_ready import get_project_by_name, get_running_projects
from rich.table import Table

from docker_ready_cli.utils.tools import console


@click.command(name="ps", help="Show project status.")
@click.argument("project_name", required=False)
def ps(project_name: str | None) -> None:
    if project_name:
        _ps_project_by_name(name=project_name)
    else:
        _ps_all_projects()


def _ps_project_by_name(name: str) -> None:
    if project := get_project_by_name(name=name):
        if not project.containers:
            console.print(f"Project {name} is not running.")
            return

        table = Table(title=f"Status of the {name} project.", show_lines=True)
        table.add_column()
        container_ids, images = [], []
        started_ats, statuses = [], []
        hostnames, ports = [], []
        commands = []
        for container in project.containers:
            table.add_column(header=str(container.name))
            container_ids.append(container.id[:12] if container.id else "-")
            images.append(container.attrs["Config"]["Image"])
            started_ats.append(str(parse(container.attrs["State"]["StartedAt"])))
            statuses.append(container.status)
            hostnames.append(container.attrs["Config"]["Hostname"])
            ports.append(_text_ports(ports=container.ports))
            commands.append(str(container.attrs["Config"]["Cmd"]))

        table.add_row("CONTAINER ID", *container_ids)
        table.add_row("IMAGE", *images)
        table.add_row("STARTED AT", *started_ats)
        table.add_row("STATUS", *statuses)
        table.add_row("HOSTNAME", *hostnames)
        table.add_row("PORTS(HOST->CONTAINER)", *ports)
        table.add_row("COMMAND", *commands)
        console.print(table)

    else:
        console.print(f"Project {name} not found.")


def _ps_all_projects() -> None:
    if projects := get_running_projects():
        table = Table(title="All running projects", show_lines=True)
        table.add_column(header="NAME")
        table.add_column(header="CONTAINERS")
        table.add_column(header="IMAGES")
        table.add_column(header="STATUS")
        table.add_column(header="PORTS(HOST->CONTAINER)")

        for project in projects:
            if project.containers:
                containers, images = [], []
                statuses, ports = [], []
                for container in project.containers:
                    container_id = container.id[:12] if container.id else "-"
                    containers.append(f"{container.name}({container_id})")
                    images.append(container.attrs["Config"]["Image"])
                    statuses.append(container.status)
                    ports.append(_text_ports(ports=container.ports))
                table.add_row(
                    project.compose.name,
                    "\n".join(containers),
                    "\n".join(images),
                    "\n".join(statuses),
                    "\n".join(ports),
                )

        console.print(table)
    else:
        console.print("You don't have any running projects.")


def _text_ports(ports: dict[str, list[dict[str, str]]]) -> str:
    if not ports:
        return "-"
    else:
        text_ports = ""
        for container_port, host_addresses in ports.items():
            if host_addresses:
                for host_address in host_addresses:
                    host_ip = host_address["HostIp"]
                    host_port = host_address["HostPort"]
                    text_ports += f"{host_ip}:{host_port}->{container_port}, "
            else:
                text_ports += f"{container_port}, "
        return text_ports[:-2]


__all__ = ["ps"]
