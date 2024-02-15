# Containercraft
**Containercraft** simplifies the process of setting up consistent, isolated, and reproducible Python development environments using Docker containers. By automating the environment setup, Containercraft eliminates the common "it works on my machine" problem, ensuring that every team member, from interns to seasoned developers, works in an identical setup. This streamlined approach not only saves time but also enhances productivity, allowing developers to focus on coding rather than configuration.  

![Screenshot from 2024-02-16 00-02-55](https://github.com/s1dharth-s/containercraft/assets/16634798/98bf435b-13ae-48dc-8d8f-3f1b454e19f0)  
  
Key Features:

- Automated Docker Environment Creation: Quickly sets up Docker containers tailored for Python development.
- Pre-Configured with Best Practices: Includes setups for [**Ruff**](https://github.com/astral-sh/ruff) (linting), [**Ruff-format**](https://github.com/astral-sh/ruff) (formatting), [**mypy**](https://github.com/python/mypy) (static type checking), [**pytest**](https://github.com/pytest-dev/pytest) (testing), [**pre-commit**](https://github.com/pre-commit/pre-commit) hooks, [**GitHub Actions**](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions), and [**tox**](https://github.com/tox-dev/tox) for CI testing.
- Consistent Development Environments: Guarantees identical environments across all machines, eliminating compatibility issues.
- Simplicity and Customizability: Easy for newcomers to use with minimal Docker knowledge, yet customizable for specific project needs.
- Efficient Onboarding: Ideal for teams with rotating roles like student jobs and interns, facilitating immediate productivity with minimal setup time.

Containercraft offers a hassle-free solution for managing Python development environments with advanced features like Docker-in-Docker capability, embodying a perfect blend of consistency, efficiency, and best practices. It's designed to make the setup process as seamless as possible, ensuring that developers can start their projects with the right tools and configurations from day one.

The containers are to be used in tandem with VS Code's [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).

## Set Up
1. Clone the [containercraft](https://github.com/s1dharth-s/containercraft) repository to your machine.**Note:** If you are cloning the current repository, make sure to use `git clone --recurse-submodules`.
2. Run `./setup.sh` inside the repo to setup the dependencies. If you are curious, the script is just setting up [pipx](https://github.com/pypa/pipx), [Poetry](https://github.com/python-poetry/poetry) and Docker. After the script finishes executing, **make sure to open up a new terminal to continue**. If docker does not work without `sudo`, try running the following:
    ```bash
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    ```
3. (**In new terminal**) Navigate to the `containercraft` directory and run:
    ```bash
    poetry install
    poetry shell
    ```
4. That's it! :tada: Now you can use `containercraft`.

## Usage
Run `containercraft --help` to see the available commands.

### `containercraft create`: To create a new dev container.
As a quick demo of `containercraft`, let us setup a sample workspace.  
  
![image](https://github.com/s1dharth-s/containercraft/assets/16634798/b1a6e469-28d4-4812-8ba0-27a0ee4b7346)  
  
1. In the same directory, run:
    ```bash
    # Create a
    containercraft create -w ./sample_workspace -p 3.11
    ```
    You can choose to name your container to your liking and also enter the ports to be forwarded (none required for our sample). Docker capability is also optional for this sample.
2. Open the created workspace folder in VS Code and when prompted, click the button to install the [Dev Container extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). If you have the extension already installed, you will be prompted to open the workspace as a dev container.

    ![image](https://github.com/s1dharth-s/containercraft/assets/16634798/7a5f552d-705b-4bd0-b882-7c93bdc92293)  
  
4. To manually launch as a dev container, or if you missed the prompt, press `F1` and then select **Dev Containers: Reopen in Container command**  
  
   ![image](https://github.com/s1dharth-s/containercraft/assets/16634798/550c5405-c2af-4dcd-92d1-a7a3d3c1e9cb)  
  
6. There open up `sample.py` to get a glimpse of ruff linter and mypy in action. If you decide to push the repository to GitHub, you can see the CI pipeline working as well!  

  ![image](https://github.com/s1dharth-s/containercraft/assets/16634798/0c76d113-9bf4-4266-9e50-78b65792e75c)  

  
### `containercraft start`: To start a Dev Container outside of the VS Code environment.
**This command will only work if you have build your container at least once with VS Code!**

Sometimes you just want access to your development environment outside of VS Code. That's where you can use `containercraft start` to start and attach to a container **that was previously built with VS Code**.

For example, run:
```bash
# Starts and attatches to the container that was built as part of the last example
containercraft start -w ./sample_workspace
```
