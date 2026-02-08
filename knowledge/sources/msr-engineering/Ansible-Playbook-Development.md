# Introduction
This describes the development flow for testing your Ansible code on a workstation.

# Create a Branch
In ADO, create a branch from the master branch of the Ansible repository you wish to work on. For GCR this is [gcr-ansible](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible)

Link this branch to work in ADO. You'll eventually do a pull request on this branch when you're satisfied.


# Install dependencies:
```bash
# Run this as root
apt-get update
apt-get install sudo curl -y
```
## Install Ansible on a node
For Linux, install the Ansible package. You can install it on linux with the following method:
```bash
curl -s "https://gcransible.blob.core.windows.net/artifacts/linux/scripts/install_ansible.sh${SAS_TOKEN}"|bash
```

The SAS token for accessing the above can be found [here](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/asset/Microsoft_Azure_KeyVault/Secret/https://gcrcmvault.vault.azure.net/secrets/gcr-ansible-sas/23fa88a653204e78898f23378c6a62c2)

## Download the repo and check out branch
You'll want to do the clone as your user, or you'll have issues running VSCode against that dir.
```bash
sudo mkdir /opt/ansible/repo/myrepo
sudo chown $(whoami) /opt/ansible/repo/myrepo
git clone git@ssh.dev.azure.com:v3/msresearch/MSR%20Engineering/gcr-ansible /opt/ansible/repo/myrepo
```

From here, you can use Visual Studio Code to edit the files on the host remotely (see [this guide](https://code.visualstudio.com/docs/remote/ssh)). You can also use VSCode to switch to the appropriate branch.

# Creating a clean Linux Environment for Iterations
You can obviously use a VM and run your ansible code there, though you'll find that your environment will become less clean after continuous runs and testing. The best thing to do is then to use a clean environement that's easy to spin up.

You can use docker for this, but it doesn't very well support systemd out of the box. A decent alternative is LXD.

## LXD/LXC

You'll want to put your ansible installer into a script:

`/root/install_ansible.sh`
```
#!/usr/bin/env bash
apt-get update -y
apt-get install curl sudo systemd systemd-sysv -y
SAS_TOKEN="<redacted>"
curl -s "https://gcransible.blob.core.windows.net/artifacts/linux/scripts/install_ansible.sh${SAS_TOKEN}"|bash
```

### Setup
For a new host, you'll want to initialize lxd
```bash
lxd init --auto
```


### Launch
The below will launch a new lxd container, be sure to change your container name, and ensure the repo path is correct. This will allow your remote vscode session to edit code, while still allowing the lxd container to access it.

```bash
CONTAINERNAME="gcrpgsqltest"
MYREPO="/opt/ansible/repo/gcr-ansible"
lxc launch ubuntu:18.04 $CONTAINERNAME
# Mount your ansible source to the container
lxc config device add $CONTAINERNAME gcr-ansible disk source=$MYREPO path=$MYREPO
lxc file push /root/install_ansible.sh $CONTAINERNAME/root/install_ansible.sh
```

## Install Ansible/Run/Iterate
You can get into your container like so:
```bash
 lxc exec gcrpgsqltest -- /bin/bash
```
From here you can run the installer set up previously
```bash
/root/install_ansible.sh
```

# Removing
Once you are done, you can remove your container, and start this section again with a new container.
```bash
lxc delete --force $CONTAINERNAME
```

# Iterations - Editing code and running ansible

You can run ansible with the custom entry point you set, like so:
```bash
ansible-run -playbook /opt/ansible/repo/myrepo/test.yml
```
You can also run the main entrypoint without the Azure Storage sync
```bash
ansible-run -nosync


This allows you to customize which recipe to use if you want recipe level testing. Like so:

*/opt/ansible/repo/myrepo/test.yml*
```yaml
- hosts: all
  strategy: debug
  tasks:
  - include_role:
      name: base-linux
      tasks_from: test
```
This will execute the `test.yml` cookbook in your `base-linux` role. With this test playbook, you can put debug messages in place:

*/opt/ansible/repo/myrepo/roles/base-linux/tasks/test.yml*
```yaml
---
- name: debug
  debug:
    msg: this is test
- name: /etc/apt/sources.list
  vars:
    aptmirror: "azure.archive.ubuntu.com"
    aptmirrordir: "/ubuntu/"
  template:
    src: templates/sources.list.j2
    dest: /etc/apt/sources.list
    owner: root
    group: root
    mode: '0644'
  notify: apt-get update
  when: not ansible_hostname | regex_search("^GCR-DGX")
```

Once you've made edits, and are satisfied the code works on the cases you've tested, make your commits, and create a PR.

# References
[Ansible Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
[Ansible Debugger](https://docs.ansible.com/ansible/latest/user_guide/playbooks_debugger.html)
[Debug Ansible Playbooks like a Pro](https://blog.codecentric.de/en/2017/06/debug-ansible-playbooks-like-pro/)
