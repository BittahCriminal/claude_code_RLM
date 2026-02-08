# Installing Ansible

## Install dependencies:
```bash
# Run this as root
apt-get update
apt-get install sudo curl -y
```
## Install Ansible on a node

refer to this page([Manual Ansible installation on GCR hosts](/Team-Pages/SES/Service-Management/Services/Ansible/Manual-Ansible-installation-on-GCR-hosts))


# To put GCR User Auth on an Ubuntu host (no DNS)
## Install Ansible method
* Install Ansible (above)
* Run:
   ```bash
   sudo ansible-run --playbook gcrauth.yml
   ```
* `sudo apt-get purge gcr-ansible-pkg`

# Central method (corpnet only)
This will do a one time configuration on the remote host, not installing any ansible bits.

* ssh to a gcr host, I recommend `gcr-batch01`
* Replace `myremotehost` with the hostname or ip address. Yes you'll need a comma `,` after it.
* You can get the GCRCMVAULTRO_PASS from [Azure Key Vault](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://gcrcmvault.vault.azure.net/secrets/gcrcmvaultro/a5c8b18c1d7845a78019f9da9e117d39).
* The `-u` is the username for the host, you'll be prompted for the password (which is done with `-k`). You'll also need passwordless sudo, or otherwise will need to add `-K` which will ask for the sudo pass.
```bash
. /opt/ansible/venv/bin/activate
cd /opt/ansible/repo/gcr-ansible
export GCRCMVAULTRO_PASS="fill_in_password_here"
ansible-playbook -u msrsupp -k -b -i myremotehost, gcrauth.yml
```
# To put GCR User Auth on an Ubuntu host with DNS (corpnet only)
This will continuously run Ansible on the host, which is needed because the msrhpcni cred will need to be refreshed whenever the password is changed.
* Install Ansible (above)
* Run:
   ```bash
   sudo ansible-run --playbook gcrauthdns.yml
   ```


