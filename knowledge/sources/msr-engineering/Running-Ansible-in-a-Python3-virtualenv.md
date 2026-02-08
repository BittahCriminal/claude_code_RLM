# Introduction

Running Ansible from a VirtualEnv gives us the assurance that we're running in a fairly contistant (and [not EOL](https://www.python.org/doc/sunset-python-2/) environment). 

Instead of setting up the venv, it's also possible to just tar up the venv and deploy it that way.

What would be best is to somehow packagify this and allow it for versioning and upgrades.

# Getting and setting up Python

If you need a newer python environment than what the OS provides, there's always the deadsnakes repo:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
```
## Get pip
```bash
apt-get install python3-dev python3-venv libpython3-dev -y
curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3 /tmp/get-pip.py
rm /tmp/get-pip.py
```
## Create the virtualenv
```bash
python3 -m venv /opt/ansible/venv
```
## Activate it
(to deactivate, just type deactivate)
```bash
. /opt/ansible/venv/bin/activate
```

## Install Ansible
```bash
pip3 install ansible
```
## bash script using venv
```bash
#!/bin/bash
SAS_TOKEN="<SAS TOKEN GOES HERE>"
#echo "SAS_TOKEN: $SAS_TOKEN"
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
#/usr/local/bin/azcopy sync "https://gcransible.blob.core.windows.net/repository/$SAS_TOKEN" /opt/ansible/repository --recursive=true --log-level NONE
cd /opt/ansible/repository
. /opt/ansible/venv/bin/activate
/opt/ansible/venv/bin/ansible-playbook -c local /opt/ansible/repository/main.yml -i $(hostname), --limit $(hostname)
deactivate
```

## A go program using the venv
```go
package main

// go get golang.org/x/sys/unix

import (
        "fmt"
        "golang.org/x/sys/unix"
        "os"
)

func main() {
        var err error
        //      sasToken := "<SAS TOKEN GOES HERE>"

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

        if err != nil {
                panic(err)
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

        err = unix.Exec("/usr/local/bin/azcopy", args, env)
        if err != nil {
                panic(err)
        }

        args := []string{"/bin/bash", "-c", ". /opt/ansible/venv/bin/activate && /opt/ansible/venv/bin/ansible-playbook -c local /opt/ansible/repository/main.yml -i $(hostname), --limit $(hostname)"}
        err = unix.Exec("/bin/bash", args, env)

        if err != nil {
                panic(err)
        }

}
```