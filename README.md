# <img src="https://github.com/tyzen9/tyzen9/blob/main/images/logos/t9_logo.png" height="25"> Tyzen9 - docker-myanonamouse-ip-helper
If you are a [myanonamouse.net](https://www.myanonamouse.net/) user, then you are likely familiar with their [dynamic seedbox IP](https://www.myanonamouse.net/api/endpoint.php/3/json/dynamicSeedbox.php) concept. 
This configuration is crucial if your activity runs behind a VPN connection whose IP address can change automatically.

> [!NOTE]
> This [docker image](https://hub.docker.com/repository/docker/tyzen9/myanonamouse-ip-helper/general) is used in my in my experimental Docker stack [docker-servarr-seedbox](https://github.com/tyzen9/docker-servarr-seedbox), and keeps the qBittorrent instance reachable even as the PIA IP address changes.


I created this image for use with my [docker-servarr-seedbox](https://github.com/tyzen9/docker-servarr-seedbox) stack that uses a [Private Internet Access](https://www.privateinternetaccess.com/) (PIA) VPN service but it can be used with any VPN.

This image is simple, all it does is make a once an hour call to [myanonamouse.net](https://www.myanonamouse.net/) with the cookie assigned to my dynamic seedbox IP (they call a MAM-ID) from the network that the VPN is running on.

## Supported Architectures
Simply pulling `tyzen9/myanonamouse-ip-helper:latest` should retrieve the correct image for your arch. The architectures supported by this image are:

| Architecture | Available | Tag |
| :---   | :--- | :--- |
| x86-64 | ✅ | latest |
| arm64	 | ✅ | latest |

Specific version tags are available on [Docker Hub](https://hub.docker.com/repository/docker/tyzen9/myanonamouse-ip-helper/tags).

## Deployment
This is best deployed using docker compose, and typically in the same stack as the VPN client - see my [docker-servarr-seedbox](https://github.com/tyzen9/docker-servarr-seedbox) stack. Here is an example:

```yaml
services:
  mam-ip-helper:
    image: tyzen9/myanonamouse-ip-helper:latest
    container_name: myanonamouse-ip-helper
    environment:
      - MAM_ID=<yourmamkeygoeshere-yourmamkeygoeshere-yourmamkeygoeshere-yourmamkeygoeshere>
    network_mode: "service:vpn"
    depends_on:
      - vpn
```
> [!IMPORTANT]
> The `network-mode: "service:vpn"` setting will ensure this stack is running on the network created by a service in your stack called VPN.  You need this to make sure the IP address the call comes from is the VPN IP

## Configuration Options
| Variable | Type | Example | Definition |
| :---   | :--- | :--- | :--- |
| *MAM_ID | string | "\<mam-id\>" | The 200+ character session cookie string for your active seedbox IP session. [See here](https://www.myanonamouse.net/preferences/index.php?view=security)|
| UPDATE_INTERVAL | int | 3600 | The number of seconds between updates, defaults to 3600 (1 hour) |
| LOG_LEVEL | string | "INFO" | The logging level to be used ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'). Defaults to "INFO" |
\*required parameter

# Development
This project is designed to be developed with VS code and the [Dev Containers](https://marketplace.visualstudio.com/items/?itemName=ms-vscode-remote.remote-containers) extension. 

> [!IMPORTANT]
> In development, a `.env` file is expected. You can copy `sample.env` to make a `.env` file for testing.

To start the project at the resulting dev container command line, issue the following command:

```
python3 /usr/src/tyzen9/main.py 
```

## Development Environment Requirements
- Docker Engine 
- Docker Desktop (optional)
- Make - used to build and publish images

## VS Code
The following extensions are recommended to be installed in VS Code:

- [Dev Containers](https://marketplace.visualstudio.com/items/?itemName=ms-vscode-remote.remote-containers)
- [Docker](https://marketplace.visualstudio.com/items/?itemName=ms-azuretools.vscode-docker)
- [Python](https://marketplace.visualstudio.com/items/?itemName=ms-python.python)

### Open the project in a Docker Dev Container for development using VS Code
1. Install the Recommended extensions (above):
2. Ensure Docker Desktop (or another Docker service) is running on your system.
3. In VS Code, Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P), and Select Dev Containers: `Reopen in Container`
    - VS Code will build the container based on the `.devcontainer/devcontainer.json` configuration 
      The first build might take some time, but subsequent openings will be faster.
7. Develop Inside the Container. 
    - Once connected, you can use all of VS Code's features (e.g., IntelliSense, debugging) as if working locally.

## Build & Publish
Update the `Makefile` to contain the appropriate Docker Hub username, application name and version number

```
DOCKER_USERNAME ?= username
APPLICATION_NAME ?= application-name
VERSION ?= 1.0.0
```

To build images of this container, use this command in the root directory of the project:

```
make build
```

To publish th built images to to Docker Hub use this command in the root directory of the project:

To build use this command:
```
make push
```

# References
[Setting up a dockerized Python environment the elegant way](https://towardsdatascience.com/setting-a-dockerized-python-environment-the-elegant-way-f716ef85571d/)

