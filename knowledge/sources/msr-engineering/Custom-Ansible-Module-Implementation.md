# Introduction
How to get a custom module in place and working

# Add the module to your modules dir
I'm using `/opt/ansible/repo/master/modules` for this one.

I'm testing the [azure_vm_metadata_fact.py](https://github.com/ansible/ansible/blob/4fdf75f0c96f3eda70d72aa7e9e72ea07d312e4f/lib/ansible/modules/cloud/azure/azure_vm_metadata_facts.py) module in this case which isn't yet comitted to the main repo.

# Ensure your dir is in the ANSIBLE_LIBRARY var
So something like this will work:
```bash
export ANSIBLE_LIBRARY="$ANSIBLE_LIBRARY:/opt/ansible/repo/master/modules"
```

# Test the module on the command line
I'm using a venv, so I activate it first.
```bash
cd /opt/ansible/repo/master
. /opt/ansible/venv/bin/activate
export ANSIBLE_LIBRARY="$ANSIBLE_LIBRARY:/opt/ansible/repo/master/modules"
 ansible localhost -m azure_vm_metadata_facts
```
This will show you all the facts the module finds with their values.

# Test the module in Ansible
The below will call the fact gathering module. The variables can be called from other playbooks.

*main.yml*
```yml
---
- hosts: kz-ansible*
  tasks:
    - azure_vm_metadata_facts:
    - include_role:
        name: common
        tasks_from: test
```

*roles/common/tasks/test.yml*
```yml
---
- name: debug
  debug:
    msg: "{{ ansible_azure_vm_compute_vmsize }}"

```


# Reference
[Ansible Module Development](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)