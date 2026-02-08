# Introduction
This is to provide some guidance creating an Azure Function to replace a crontab. There are many other applications for Azure Functions, but for SES, this seems to be the most common.

# Function Type - Linux Container - Timer Based (like cron)
Elements to consider:

## User Defined Identity 
You'll want to create a User Defined Identity if you're creating more than one function, you'll want to use this instead of using System Defined Identities.

## Azure Container Repo (ACR)
If you're creating an RG with a number of functions, you'll want an ACR for them. ensure you permiss the above User Defined Identity to the `AcrPull` role.

### Azure Container Repo Webhook
Once you've created your Azure Function and have uploaded your container image, you'll want to create a webhook so that the function automatically downloads a new container when it's available. You'll need The Azure Function Webhook URL. Found under the Function, in the "Container Settings" blade.
* Go to the Azure Container Repo, and click on the "Webhooks" blade.
* Click + Add
* Fill out the Webhook name, ensure the location matches the function and ACR if possible. 
* Enter the "Service URI" as the Webhook URL you retrieved before.
* Actions should be "push"
* Status should be "on"
* Scope should be your repository/container name such as "gcr/groupsyncpgsql"


## Azure Key Vault (AKV)
If you have secrets in your container or code, it's best to reveal them as environment variables. Put the secrets in the AKV, and configure the access policy to permiss the User Defined Identity to be able to Get and List.

To access secrets from an Azure Key Vault into an environment variable for your container:
- Go to the Function in the Portal, and click the `Configuration` blade
- Click on the Advanced Edit button to be able to edit the JSON for the application settings.
- A secret in the JSON can be put in like so:
  ```json
  {
    "name": "clientsecret",
    "value": "@Microsoft.KeyVault(SecretUri=https://gcrcmvault.vault.azure.net/secrets/gcrusrgrpsync/0e58f365cbd84e9691f662e7908c9d42)",
    "slotSetting": false
  },
  ```

## Setting "Always On"
If you don't set your function to "Always On" you'll want to if it's a cron based function as mentioned in [their documentation](https://docs.microsoft.com/en-us/azure/app-service/configure-common#configure-general-settings). If you don't set this, you'll see a warning on the overview page.
- Go to the Function in the Portal, and click the `Configuration` blade
- Click on the `General Settings` tab
- Set the "Always On" radio button to "On"

# Enabling sshd
For troubleshooting and developing the script running on your app, it's highly recommended you enable ssh on your container. [The instructions on Azure's Documentation should help](https://docs.microsoft.com/en-us/azure/app-service/configure-custom-container?pivots=container-linux#enable-ssh). The high level overview to getting it working is as follows:
- Install openssh-server into your container
- Change the root password to `Docker!`
- Install the sample [/etc/ssh/sshd_config](https://github.com/Azure-App-Service/node/blob/master/10.14/sshd_config) into your container. You can change the `SSH_PORT` text in the sample to `2222`.
- Ensure you have an `ENTRYPOINT` line in your `Dockerfile` that has a container init script. The script should use the CMD used in your source container, as well as sshd. For example:
```bash
#!/usr/bin/env bash
/usr/sbin/sshd &
/azure-functions-host/Microsoft.Azure.WebJobs.Script.WebHost
```

# Logging
If you want pretty logs that get output to the Monitor section, I highly suggest using the logger functionality.

Setup can be done like so to enable stdout and file based logging:
```python
logging.basicConfig(filename='/var/log/groupsyncpgsql.log')
stderrLogger=logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
```
Then down in your functions, etc, you can emit logs:
```python
logging.info("fixing user {} was {}".format(key,modmember))
```
This will allow pretty logs in the monitor section, instead of having to go to the log stream, or inside the container to find your logs:
![image.png](/.attachments/image-cb48b64f-9972-4d2f-80c6-b223067fb681.png)

As opposed to:
![image.png](/.attachments/image-70b78c57-e01b-48e9-9a5f-94f3d2a15ca3.png)

# Adding Outbound Addresses
You can discover the outbound addresses of your Azure Function using [this documentation](https://docs.microsoft.com/en-us/azure/azure-functions/ip-addresses?tabs=portal#find-outbound-ip-addresses), and add them to the NSG or firewall necessary.

# Troubleshooting
Keep in mind the time for all your logs will be default in UTC. Taking note of the current UTC time will help you better know what's going on.

If you're looking at your logs and you see a message about enabling container logging and looking at https://aka.ms/linux-diagnostics, it's really just referring to this command. Recommended if you need debugging:

```bash
az webapp log config --name <app-name> --resource-group <resource group> --docker-container-logging filesystem
```

## Container Loading
The first place to look when troubleshooting your Azure Function container is by clicking into the Function, and then clicking on the `Container Settings` blade. You'll see logs at the bottom that will tell you how your container load went. Newest logs are at the bottom, so you'll need to scroll to the bottom to see recent output.

## Functions - Invocations and Logs
The second place to look in the `Functions` blade. You should see the name of your function listed. Click into that, and you'll be taken to a new screen. 

### Monitor
The 'Monitor' blade here will take you into the `Invocations` tab which will show you the last runs, and whether they were successful or not. There's also the `Logs` tab, which will show you logs from the container.

The the `Log Stream` blade inside the function will show you the same data as the the Logs tab mentioned above.

### Code + Test
The Code + Test blade will show you the actual code being executed. If there's nothing here, then there's a problem with the container.

## Common Messages
### `Unhandled exception in request pipeline: System.Net.Http.HttpRequestException: Connection refused`
A common issue when this error shows up is that your `function.json` is incorrect. It could be you specified the cron incorrectly, or it's otherwise formatted wrong. Take a look at the [Azure Functions function.json documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python#example).

# Container specifications

# References
[Functions Reference](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference)
[Function Bindings Timer](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python#example)
[Azure Functions host.json Reference](https://docs.microsoft.com/en-us/azure/azure-functions/functions-host-json)
[Azure Functions Python Sample Repo](https://github.com/Azure/azure-functions-docker-python-sample)
[Azure Functions Python Worker Repo](https://github.com/Azure/azure-functions-python-worker)