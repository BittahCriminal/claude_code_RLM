#Introduction
When we're going to make a change to the system or if we know there's downtime or an issue, we should communicate this to users of our Azure DevOps organization, [msresearch](https://dev.azure.com/msresearch). The best way to do this that we've found thus far is to use the built-in banner functionality. This document relies on you having the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) installed on your machine, with the [_devops_ extension](https://docs.microsoft.com/en-us/cli/azure/azure-cli-extensions-overview?view=azure-cli-latest).

If you would like more examples for usage of these commands, each one allows a `-h` parameter to show help, or you can go to the [Docs page](https://docs.microsoft.com/en-us/cli/azure/ext/azure-devops/devops?view=azure-cli-latest).

#Usage
##Adding a banner
When adding a banner, it's necessary to set at least the `--organization` (`--org`) and the `--message` parameters, as seen below. It's important to note that the `--org` parameter is technically optional for this command, it's effectively required for our purposes as you otherwise won't know which ADO organization you're adding a banner to.
```
az devops admin banner add --org https://dev.azure.com/msresearch --message "Your message here."
````
The following parameters are also likely to be helpful:
- `--expiration` - Causes the banner to be automatically disabled at a certain date and time. Example: `"2019-06-10 17:21:00 UTC"` or `"2019-06-10"`
- `--type` or `-t` - Changes the formatting of the banner that is displayed. Options are `error`, `info`, and `warning`, with `info` as the default. See below for examples.
<IMG  src="https://dev.azure.com/msresearch/ba03da23-a813-4111-89f4-e785b3fba956/_apis/wit/attachments/fd3ce9b5-03aa-4517-a636-b0ca7635c90a?fileName=image.png"/>

##Listing and Removing a banners
If you don't set an expiration when adding a banner (see above), you will need to later remove that banner when it's no longer relevant. This can be done by first listing all active/expired banners with `az devops admin banner list --org https://dev.azure.com/msresearch`. This will return a list of banners in JSON format, as in the example below:
```json
{
  "2d674bbc-e20e-45d2-44c5-70c44e873a32": {
    "expirationDate": "10/02/2019 19:00:00",
    "level": "Info",
    "message": "This is some banner text that will expire on October 2nd."
  },
  "3bf48b9d-5b53-4ac1-943a-67fcdf46992c": {
    "level": "Info",
    "message": "This is some banner text that will show until it is removed manually."
  }
}
```
The first banner (2d674bbc) will stop being displayed after the time specified in `expirationDate`, but will remain in the list until removed manually. The second banner (3bf48b9d) will continue to display to users until remove manually. To remove a banner run `az devops admin banner remove --org https://dev.azure.com/msresearch --id 00000000-0000-0000-0000-000000000000`, replacing the empty guid with the Id of the banner that you'd like to remove.

#History
We previously attempted (mid-2019) to set up a mailing list so that we'd be able to notify users by email, but it ended up with only one person outside of our team on it.