import json
import os
import shutil
from pathlib import Path
from typing import Annotated, Optional
import subprocess

import typer
from rich import print

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
        print(
            f"Workspace location {workspace_location} not found. Creating workspace with empty git repository..."
        )
        os.makedirs(workspace_location)
        os.system(f"cd {workspace_location} && git init")
    else:
        print(f"Workspace location {workspace_location} found. Proceeding...")
        # Check if workspace is a git repo or not
        if not os.path.isdir(f"{workspace_location}/.git"):
            print("Directory is not a git repository. Initializing git...")
            os.system(f"cd {workspace_location} && git init")
        else:
            print("Directory is already a git repository. Skipping git initialization.")

    # create .devcontainer folder and devcontainer.json
    devcontainer_folder = f"{workspace_location}/.devcontainer"
    if not os.path.exists(devcontainer_folder):
        os.makedirs(devcontainer_folder)
    else:
        if os.path.exists(f"{devcontainer_folder}/devcontainer.json"):
            print(
                f"devcontainer already exists in {devcontainer_folder}. Please remove exisiting .devcontainer file before proceeding. Exiting..."
            )
            return

    with open(templates_path / "devcontainer.json.template", "r") as f:
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

    with open(f"{devcontainer_folder}/devcontainer.json", "r") as f:
        config = json.load(f)

    docker_capability = typer.prompt("Enable Docker capability?", default="false")

    if docker_capability == "true":
        docker_type = typer.prompt(
            "Enter the type of Docker capability: \n 1. Docker-in-Docker \n2.Docker-outside-of-docker \n",
            default="1",
        )
        match int(docker_type):
            case 1:
                config["features"] = {
                    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
                }
            case 2:
                config["features"] = {
                    "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {}
                }
            case _:
                print("Invalid option. choosing default option...")
                config["features"] = {
                    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
                }

    with open(f"{devcontainer_folder}/devcontainer.json", "w") as f:
        f.write(json.dumps(config))

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
        templates_path / ".pre-commit-config.yaml.template",
        workspace_location + "/.pre-commit-config.yaml",
    )

    # Copy .gitingore file to the workspace
    shutil.copy2(templates_path / ".gitignore", workspace_location + "/.gitignore")

    # Copy start.sh file to the workspace
    shutil.copy2(templates_path / "startup.sh", f"{devcontainer_folder}/startup.sh")

    # Copy github action file to the workspace
    os.makedirs(
        os.path.dirname(f"{workspace_location}/.github/workflows/"), exist_ok=True
    )
    shutil.copy2(
        templates_path / "github_action_template.yml",
        f"{workspace_location}/.github/workflows/test.yml",
    )
    # Copy tox.ini file to the workspace
    shutil.copy2(templates_path / "tox.ini.template", f"{workspace_location}/tox.ini")

    with open(templates_path / "docker_template", "r") as f:
        # Read the entire content
        content = f.read()

    # Replace the specified text
    new_content = content.replace("{{PY_VER}}", pyversion)

    # Open the output file in write mode
    with open(f"{devcontainer_folder}/Dockerfile", "w") as f:
        # Write the modified content
        f.write(new_content)

    print(f"Devcontainer created in {devcontainer_folder}.")
    print(
        f"""\nFollowing files has been created and placed in the workspace:
               1. Pre-commit Configuration File: {workspace_location}/.pre-commit-config.yaml
               2. Tox Configuration File: {workspace_location}/tox.ini
               3. Github Action File: {workspace_location}/.github/workflows/test.yml
               4. Gitignore File: {workspace_location}/.gitignore
               5. requirements.txt: {workspace_location}/{requirements_file}
               6. devcontainer.json: {devcontainer_folder}/devcontainer.json
               7. Dockerfile: {devcontainer_folder}/Dockerfile
               """
    )
    print(
        "[bold red]Note:[/bold red] The template files will serve as a starting point and it might not work for all use cases. Please modify them as per your requirements."
    )
    print(
        "\n[bold green]To run your devcontainer, start VS Code, run the Dev Containers: Open Folder in Container command from the Command Palette (F1) or quick actions Status bar item, and select the worspace folder[/bold green]"
    )


@app.command()
def start(
    workspace: Annotated[str, typer.Option("-w", help="Location of the workspace")],
):
    """
    Allows to start and attatch to the container outside the VS Code environment.
    """

    if not os.path.exists(workspace):
        typer.echo(f"Workspace {workspace} not found. Exiting...")
        raise typer.Exit(code=1)

    devcontainer_path = Path(workspace) / ".devcontainer"
    if not devcontainer_path.exists():
        typer.echo(
            "The specified workspace does not contain a .devcontainer directory. Use containercraft create to create a devcontainer. Exiting..."
        )
        raise typer.Exit(code=1)

    config_file = devcontainer_path / "devcontainer.json"
    container_conf = json.load(open(config_file, "r"))

    name = container_conf["runArgs"][1]

    command = ["docker", "start", str(name)]
    subprocess.Popen(command).wait()

    typer.echo(f"Attatching to container {name} in workspace {workspace}...")
    command2 = f"docker exec -it {name} /bin/bash"
    subprocess.Popen(command2, shell=True).wait()

    command3 = ["docker", "stop", str(name)]
    subprocess.Popen(command3).wait()
    typer.echo(f"Container {name} stopped.")
