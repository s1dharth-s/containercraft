# Install Poetry, Docker, and VSCode

printf "Installing Poetry...\n"
sudo apt update && sudo apt install -y pipx git && pipx ensurepath
pipx install poetry && \
poetry install

printf "Installing VSCode...\n"
sudo apt install software-properties-common apt-transport-https wget -y && \
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add - && \
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add - && \
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" && \
sudo apt install code
# Add Docker's official GPG key:

printf "Installing Docker...\n"
sudo apt-get update && \
sudo apt-get install -y ca-certificates curl && \
sudo install -m 0755 -d /etc/apt/keyrings && \
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
sudo apt-get update && \
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
sudo groupadd docker && \
sudo usermod -aG docker $USER && \
newgrp docker && \

sudo systemctl enable docker.service && \
sudo systemctl enable containerd.service

printf "\n Setup Complete!\n"
