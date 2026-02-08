# Chronos Reservation Sync

## Introduction
This page describes the reservation service that works between Chronos and the reserved nodes.

## SLO/SLI/KVI

The following are definitions of SLO/SLI and KVI. No actual metrics are available for this service currently.

| <span style= "font-weight: normal; color: inherit;">SLO</span> | <span style="font-weight: normal;">Provide data to the consumption service that is the same as what Chronos provides 99% of the time.</span>|
| --- | --- |
| SLI | ADO tickets count where a user isn't able to log in due to the reservation not being available. |
| KVI | • Number of sandboxes using this service<br> • Number of times the service has been queried. |

### SLO Explanation
We have an SLO of 99% because there are edge cases where sometimes the data isn't synchronized. However the effort to fix this outweighs the benefit provided.

### KVI method: 
- Link to the number of GCR GPU sandboxes in play
- Have our fetching tool provide metrics data showing when the fetch happened, or gather query data from the Azure table if available.

## How it works
gcr_reservation sync binary scans the service tags on the Azure VM or the Azure Arc system.


## Client Side
### gcr_reservation command
5-7 minutes after the hour, and 15-20 minutes after the hour, each sandbox host runs a cron job at `/etc/cron.d/gcr_reservation` that executes the `/usr/local/bin/gcr_reservation` compiled Go program ([repo](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr_reservation)).



#### This script does the following:
- Checks the IMDS service for tags indicating the current reservation data.
  - For Azure VMs only: If no tag is found, it will check the Chronos database.
- If reservation data is found, it will:
  - Add the user(s) to the `adm` group in `/etc/group`.
  - Create a file for the reserved user(s) to sudo in /etc/sudoers.d/. This file will be the user's alias.
  - Create a crontab `/etc/cron.d/reservation_end` which executes the `/usr/local/bin/remove_user_data.sh` script on the reservation end date and time, as found in the tags for the Azure asset (or for VMs it will look up reservation data the Chronos db as a backup).
  - This script will parse the data in `/root/gcr_reservation.json`, gather the reservation users, and delete their home directories and reboot the host.
- Enforces users in the `adm` group in `/etc/group` and `/etc/sudoers.d`. If there are users found that don't belong, they're removed.

The crontab will write the output of the script to `/root/gcr_reservation.json` which has the reservation information.

## Troubleshooting
- Ensure the user exists by running `id alias@microsoft.com`, and ensure they exist in the `adm` group in `/etc/group`.
- Make sure `/etc/passwd` does not have any entry for the old account if you find `DOMAIN.alias` entries remove the line.
- Check `/etc/sudoers.d/alias` to ensure the user's `alias@microsoft.com` is listed correctly.

### Running Manually:
- You can run the script manually on VMs with: `/usr/local/bin/gcr_reservations`
- On Arc/On-prem systems, this command should be `/usr/local/bin/gcr_reservations -tagsonly`

If you're finding that the above commands are not producing the expected output do the following;
- Check the tags on the host. You can do this in the following ways:
  - Use the Azure Portal to find the host, and then use the overview page to view the tags.
  - From an Azure VM, you can run the following command:
    ```bash
    curl -H "Metadata:true" "http://169.254.169.254/metadata/instance/compute/tagsList?api-version=2021-01-01" |jq
    ```
  - From an on-prem or Arc VM you can run the following command:
    ```bash
    curl -H Metadata:true "http://127.0.0.1:40342/metadata/instance/compute?api-version=2020-06-01" | jq .tagsList
    ```
- Check the host's reservations on the [Chronos API](https://chronos-api-prod.azurewebsites.net/docs#/Admins/get_reservations_admin_reservations_get). For Azure VMs, the API will be checked as a backup. For on-prem/Arc VMs, tags must be present.

### Remediations
- You can kick off the tagging process again by modifying the reservation in any way, including editing the reservation reason.
- You can manually add users to a reservation if there is no tagging data in the following ways:
  1. If there is no reservation data, a user can be added with `add_sandbox_user.sh alias`. However, as soon as reservation data is found, the user will be removed if they're not part of the reservation. If no reservation data ever is added to the host, the user may be on the host past their reservation.
  2. Manually add the tags with the reservation data to the host. Tags should be overwritten once the host reservation is modified, or a new one occurs. You'll need to be sure you add the following tags:
      - name - `Chronos:ReservationStartDate`
      - value - Date in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format
        - You can generate this in Linux with: date -u -d `"2024-09-24 00:00:00" +"%Y-%m-%dT%H:%M:%SZ"`
      - name - `Chronos:ReservationEndDate`
      - value - Same as the above.
      - name - `Chronos:Usernames`
      - value - Comma separated list of usernames, such as: `krisz, msmith`. UPNs can also be used like `krisz@microsoft.com, msmith@microsoft.com`
      - name - `Chronos:ReservationID`
      - value - Ideally is the reservation ID, but can be any number. This is not used in a meaningful way.

