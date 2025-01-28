# <img src="https://github.com/tyzen9/tyzen9/blob/main/images/logos/t9_logo.png" height="25"> Tyzen9 - docker-myanonamouse-ip-helper
If you are a [myanonamouse.net](https://www.myanonamouse.net/) user, then you are likely familiar with their [dynamic seedbox IP](https://www.myanonamouse.net/api/endpoint.php/3/json/dynamicSeedbox.php) concept. 
This configuration is crutial if your activity runs behind a VPN connection whose IP address can change automatically.

I created this image for use with my [docker-pia-servarr](https://github.com/tyzen9/docker-pia-servarr) stack that uses a [Private Internet Access](https://www.privateinternetaccess.com/) (PIA) VPN service but uc can be used with any VPN.

This image is simple, all it does is make a once an hour call to [myanonamouse.net](https://www.myanonamouse.net/) with the cookie assigned to my dynamic seedbox IP (they call a MAM-ID) from the network that the VPN is running on.

## Deployment
This is best deployed using docker compose, and typically in the same stack as the VPN client - see my [docker-pia-servarr](https://github.com/tyzen9/docker-pia-servarr) stack. Here is an example:

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
Development guidelines assume you are running on a system connected to Docker Desktop, with `make` installed.

To make this docker image, run this command 
```
make build
```

To run the image, use this command
```
docker run --rm \
    -e MAM_ID='yourmamkeygoeshere-yourmamkeygoeshere-yourmamkeygoeshere-yourmamkeygoeshere' \
    -e LOG_LEVEL='DEBUG' \
    tyzen9/myanonamouse-ip-helper
```