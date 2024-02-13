import json
import os
import shutil
from pathlib import Path
from typing import Annotated, Optional

import typer

current_script_path = Path(__file__).resolve()  # Path to the current script
project_root = current_script_path.parent
templates_path = project_root / "templates"
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
        Optional[str],
        typer.Option("--requirements", "-r", help="Path to the requirements file"),
    ] = None,
):
    """
    Create a Dockerfile and setup the configuration for thes Dev Container.
    """

    print(
        f"Creating Dockerfile for Python {pyversion} and requirements file {requirements_file}"
    )

    if not os.path.exists(workspace_location):
        typer.echo(
            f"Workspace location {workspace_location} not found. Creating workspace with empty git repository..."
        )
        os.makedirs(workspace_location)
        os.system(f"cd {workspace_location} && git init")
    else:
        typer.echo(f"Workspace location {workspace_location} found. Proceeding...")
        # Check if workspace is a git repo or not
        if not os.path.isdir(f"{workspace_location}/.git"):
            typer.echo("Directory is not a git repository. Initializing git...")
            os.system(f"cd {workspace_location} && git init")
        else:
            typer.echo(
                "Directory is already a git repository. Skipping git initialization."
            )

    # create .devcontainer folder and devcontainer.json
    devcontainer_folder = f"{workspace_location}/.devcontainer"
    if not os.path.exists(devcontainer_folder):
        os.makedirs(devcontainer_folder)
    else:
        if os.path.exists(f"{devcontainer_folder}/devcontainer.json"):
            typer.echo(
                f"devcontainer already exists in {devcontainer_folder}. Please remove exisiting .devcontainer file before proceeding. Exiting..."
            )
            return

    with open(templates_path / "devcontainer_template.json", "r") as f:
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
        .replace("{{WORKSPACE}}", os.path.basename(workspace_location))
    )

    with open(f"{devcontainer_folder}/devcontainer.json", "w") as f:
        f.write(new_content)

    # Copy the requirements file to the workspace
    if not requirements_file:
        requirements_file = "requirements.txt"
        with open(f"{workspace_location}/{requirements_file}", "w") as f:
            f.write("")
    else:
        requirements_file = os.path.abspath(requirements_file)
        shutil.copy2(requirements_file, workspace_location)

    # Copy pre-commit config file to the workspace
    shutil.copy2(
        templates_path / ".pre-commit-config-template.yaml",
        workspace_location + "/.pre-commit-config.yaml",
    )
    
    # Copy .gitingore file to the workspace
    shutil.copy2(templates_path / ".gitignore", workspace_location + "/.gitignore")
    
    # Copy start.sh file to the workspace
    shutil.copy2(templates_path / "startup.sh" ,f"{devcontainer_folder}/startup.sh")

    with open(templates_path / "docker_template", "r") as f:
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
