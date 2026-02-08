# Purpose
This page is meant to discuss the transition to Ansible from Chef. Ansible has many similarities and differences to Chef, but it's a quite flexible tool, and some decisions will need to be made. I plan on making them transparent here. Feel free and discuss here or in the teams channel 👨‍🍳👩‍🍳Config Management 📡🛸.

# Proposals
## Push v Pull
[krisz] Ansible's default method is push, though we currently have a pull method with Chef. I propose we keep this method due to the fact that we have one Internet host that all NAT and Internet First hosts can connect to. Using a push method means that we'd have to have multiple Ansible servers to deal with. From their [`ansible-pull` documentation](https://docs.ansible.com/ansible/latest/cli/ansible-pull.html):

*(ansible-pull) is used to up a remote copy of ansible on each managed node, each set to run via cron and update playbook source via a source repository. This inverts the default push architecture of ansible into a pull architecture, which has **near-limitless scaling potential**.* (emphasis mine)

I've created a method to do pulls from an Azure Storage account. Since `ansible-pull` requires a git repository. Downsides of us using a git repository:
* You'd need to manage an SP and the associated credential to pass to `ansible-pull` to use the git repo.
* We'd likely run into ADO limits on git pulls at our scale.

### Shell script for running ansible
I've been using a shell script, which will run ansible automatically.
```bash
#!/bin/bash
SAS_TOKEN="<SAS TOKEN GOES HERE>"
if [ ! -x /usr/local/bin/azcopy ];then
   curl -L https://aka.ms/downloadazcopy-v10-linux -s -o - | tar -C /usr/local/bin --strip-components 1 --wildcards --no-anchored -zxf - '*azcopy'
fi
if [ ! -d /opt/ansible/repository ];then
  mkdir -p /opt/ansible/repository
fi
if [ ! -d /opt/ansible/.azcopy/plans ];then
  mkdir -p /opt/ansible/.azcopy/plans
fi

export AZCOPY_LOG_LOCATION="/opt/ansible/.azcopy"
export AZCOPY_JOB_PLAN_LOCATION="/opt/ansible/.azcopy/plans"
echo "## Azcopy Ansible Sync ##"
/usr/local/bin/azcopy sync "https://gcransible.blob.core.windows.net/repository/$SAS_TOKEN" /opt/ansible/repository --recursive=true --log-level NONE
cd /opt/ansible/repository
ansible-playbook -c local /opt/ansible/repository/main.yml -i $(hostname), --limit $(hostname)
```

However, since we end up with a cred in the script, I've also mocked up a go app which will obfuscate the SAS token in a binary. This go binary is different in that it doesn't install azcopy for you. Doing so drastically increases the complexity of the program. Installing AzCopy should be done at the ansible install time by whatever method happens there. The oneliner is the shell script is still useful for that install process.

```go
package main

import (
        "fmt"
        "io"
        "os"
        "os/exec"
        "syscall"
)

func main() {

        sasToken := "<SAS TOKEN GOES HERE>"

        // Get azcopy if it doesn't exist
        if _, err := os.Stat("/usr/local/bin/azcopy"); os.IsNotExist(err) {
                fmt.Println("no azcopy :(")
                panic(err)
        }

        if _, err := os.Stat("/opt/ansible/repository"); os.IsNotExist(err) {
                os.MkdirAll("/opt/ansible/repository", 0777)
        }

        if _, err := os.Stat("/opt/ansible/.azcopy/plans"); os.IsNotExist(err) {
                os.MkdirAll("/opt/ansible/.azcopy/plans", 0777)
        }

        hostname, err := os.Hostname()
        if err != nil {
                panic(err)
        }

        binary, lookErr := exec.LookPath("ansible-playbook")
        if lookErr != nil {
                panic(lookErr)
        }

        env := os.Environ()
        err = os.Setenv("AZCOPY_LOG_LOCATION", "/opt/ansible/.azcopy")
        if err != nil {
                panic(err)
        }
        err = os.Setenv("AZCOPY_JOB_PLAN_LOCATION", "/opt/ansible/.azcopy/plan")
        if err != nil {
                panic(err)
        }
        args := []string{"azcopy", "sync", "https://gcransible.blob.core.windows.net/repository/" + sasToken, "/opt/ansible/repository/", "-i", "--recursive=true", "--log-level", "NONE"}

        execErr := syscall.Exec(binary, args, env)
        if execErr != nil {
                panic(execErr)
        }

        args := []string{"ansible-playbook", "-c", "local", "/opt/ansible/repository/main.yml", "-i", hostname + ",", "--limit", hostname}

        execErr := syscall.Exec(binary, args, env)
        if execErr != nil {
                panic(execErr)
        }
}
```

## Recipe routing
Reference: [targeting hosts and groups](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html)

Traditional ansible likes to have an inventory file, that is populated with hosts. These hosts can be in groups, etc. The downside is that this file is limited when it comes to wildcards. The reason is because this list is used like a traditional pssh or fabric host list to ssh to. You can't just say "ssh to all possibilities" because that isn't practical.

If you're running locally, it makes sense to ditch the inventory file and use your own host to specify itself. This is why we invoke ansible as:
```bash
ansible-playbook -c local /opt/ansible/repository/main.yml -i $(hostname), --limit $(hostname)
```
The -i specifies your own custom inventory list (and yes the "," is needed), and limit will make it so playbooks to creep to other host definitions. Now that we're using the play to route, we can use wildcards there.

### Two ways to route

From here you can specify hosts and host patterns in your `main.yml`, or you can use conditionals. The pattern method is below:

*main.yml*
```yaml
---
- hosts: all
  tasks:
    - include_role:
        name: base-linux
        tasks_from: install-roles
- hosts: gcrazgdl*
  tasks:
    - include_role:
        name: common
- hosts: kz-ansible*
  tasks:
    - include_role:
        name: base-linux
```

However, this has issues because if your parsing runs into a `hosts:` line with patterns not in your inventory, you'll get warnings:
```bash
[WARNING]: Could not match supplied host pattern, ignoring:
```
These warnings will increase with unrecognized patterns. [Ansible has been resistant to provide a fix for this issue](https://github.com/ansible/ansible/issues/40030). As a side note, you also can't use `{{ ansible_hostname }}` in your `hosts:` line.

A method to get around this is to use conditionals instead:

*main.yml*
```yml
---
- hosts: all
  tasks:
    - include_role:
        name: base-linux
        tasks_from: install-roles
    - include_role:
        name: common
      when: ansible_hostname | regex_search("^gcrazgdl*")
    - include_role:
        name: base-linux
      when: ansible_hostname | regex_search("^kz-ansible*")
```

## Use of Ansible Tower OSS (known as [AWX](https://github.com/ansible/awx))
AWX stands for Ansible Works, which was the original name of the company Red Hat acquired. It was open sourced due to a promise that Red Hat Made to the community.

Ansible tower is built on Anisble's default configuration (push). It also provides statistics on Ansible runs that it initiates. Finally, it's got a nifty RBAC system that separates roles on it.

Since we're adopting a push methodology, Tower isn't much use to us. For statistics, we would likely be best served gathering them ourselves somehow. This also eliminates the need to configure and maintain another server (so we end up not agentless, but we are serverless).

## Repository
### Current repo is gcr-ansible, to differentiate other ansible repos.


## Keyvault Secrets 
(discussion by krisz)
Ansible comes with a lookup plugin that allows Azure Keyvault lookups using MSI or service principal. There are pros and cons with this:
### MSI:
* There is no persistant password on disk, and the credential is easily revokable on a per VM basis.
* The password is in a well known location, even though the keyvault requires looking at the code.

### Service Principal
* There is a persistent password (or if you want to be tricky, a derivation of the password) on the disk. Revocation is for all systems using the SP
* The password can be obscured, but still discoverable, keyvault still requires looking at the code. 

Based on the ease of revocation, I'm recommending MSI for all Azure VMs, and SP for on-prem assets.

