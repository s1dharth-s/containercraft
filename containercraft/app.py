import json
import os
import shutil
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def create(
    workspace_location: Annotated[
        str,
        typer.Option(
            "--workspace",
            "-w",
            help="Location of the workspace. Make sure the workspace exists",
            prompt=True,
        ),
    ],
    pyversion: Annotated[
        str,
        typer.Option(
            "--pyversion", "-p", help="Python version for the container", prompt=True
        ),
    ],
    requirements_file: Annotated[
        str,
        typer.Option(
            "--requirements", "-r", help="Path to the requirements file", prompt=True
        ),
    ],
    include_git_ssh: Annotated[
        bool,
        typer.Option(
            "--include-configs", help="Include ssh and git config in the dev containers"
        ),
    ] = False,
):
    """
    Create a Dockerfile and setup the configuration for thes Dev Container.
    """

    print(
        f"Creating Dockerfile for Python {pyversion} and requirements file {requirements_file}"
    )

    if not os.path.exists(workspace_location):
        typer.echo(
            f"Workspace location {workspace_location} not found. Creating workspace..."
        )
        os.makedirs(workspace_location)
    else:
        typer.echo(f"Workspace location {workspace_location} found. Proceeding...")

    # create .devcontainer folder and devcontainer.json
    devcontainer_folder = f"{workspace_location}/.devcontainer"
    if not os.path.exists(devcontainer_folder):
        os.makedirs(devcontainer_folder)
    else:
        if os.path.exists(f"{devcontainer_folder}/devcontainer.json"):
            typer.echo(
                f"Devcontainer already exists in {devcontainer_folder}. Please use containercraft edit command to edit existing environment. Exiting..."
            )
            return

    with open("templates/devcontainer_template.json", "r") as f:
        # Read the entire content
        content = f.read()

    name = typer.prompt(
        "Enter the name of the dev container", default="Python Dev Container"
    )
    ports = typer.prompt(
        "Enter the ports to expose (comma separated). If none, press enter.", default=""
    )
    if not ports:
        ports = "[]"
    else:
        ports = [int(port) for port in ports.split(",")]

    # Replace the specified text
    new_content = (
        content.replace("{{NAME}}", name)
        .replace("{{PORTS}}", json.dumps(ports))
        .replace("{{PY_VER}}", pyversion)
    )

    with open(f"{devcontainer_folder}/devcontainer.json", "w") as f:
        f.write(new_content)

    # Copy the requirements file to the workspace
    requirements_file = os.path.abspath(requirements_file)
    shutil.copy2(requirements_file, workspace_location)

    with open("templates/docker_template", "r") as f:
        # Read the entire content
        content = f.read()

    # Replace the specified text
    new_content = content.replace("{{PY_VER}}", pyversion)

    # Open the output file in write mode
    with open(f"{devcontainer_folder}/Dockerfile", "w") as f:
        # Write the modified content
        f.write(new_content)

    typer.echo(
        f"Devcontainer created in {devcontainer_folder}. Please use the VS Code Dev Container extension to launch the environment."
    )


@app.command()
def start():
    """
    Start the dev container
    """
    print("Starting the dev container")


if __name__ == "__main__":
    app()
