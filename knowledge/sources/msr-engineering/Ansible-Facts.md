# Ansible Facts

## Introduction

Ansible's variables are also known as facts. It's similar to Chef's "attributes" with same quirks.

Variables get set as they are found. Unlike Chef

## Defining facts in a role

In a role, you can define facts in your `rolename/defaults/main.yml` where rolename is the name of your role.

Facts set here can be overwritten according to the Variable precedence below.

## Fact/Variable rules
These aren't RTE rules, but rules with the system itself.
* No variable or dict names with chars other than [A-Za-z_]. If you use things like dashes(-) or dots(.), you won't get errors, but you will have problems referencing the variable.
* Nested keys can have dashes and dots in them.


## Defining facts in a playbook

## Defining and referencing a fact with register
You can also use the `shell` module with `register` to set facts, though there are some caveats with the approach:

```yaml
- name: detect and apply redmond domain
  shell: if $(dig +short redmond.corp.microsoft.com|head -n1|grep -q '^[0-9]');then echo "true"; else echo "false";fi
  register: is_corpnet_reg
```

If you wish to reference the above value, you'll need to use the stdout and treat it like a bool like so.

```yaml
- name: test action
  debug:
    msg: this is true
  when: is_corpnet_reg.stdout|bool
```

For this reason, I like to name my registers ending with `_reg` so I know how I should reference them.

The documentation implies that registers are short lived, but like other facts, they live until the ansible run completion.



### Changing nested values
Also note, that nested variables in dicts must be changed carefully.

If you have your main.yml that looks like:
```yaml
groups:
  gcrmembers: 
    gid: 8000
    objectid: acca2b01-5230-4aef-a28d-709a63473383
  msrdl:
    gid: 8028
    objectid: c717ee5a-79fc-4518-8ece-ec4c5c0b4ada 
```
And you change it like so:
```yaml
- name: "Set fact groups['gcrmembers']['gid'] to 8001"
  set_fact:
    groups:
      gcrmembers:
        gid: 8001
```
The above will be your new dict for `groups` all other data will be erased. Changing the above requires:
```yaml
    - name: Change groups.gcrmembers.gid to 8001
      set_fact:
        groups: "{{ groups|combine({'gcrmembers': {'gid': '8001'}}, recursive=True) }}"
```

For this reason, it's recommended that if you have a dict, use it for information that won't change. Fact gathering modules follow this rule.

## Referencing dict values

You can reference dict values one of two ways:

*array notation*
```yaml
groups['gcrmembers']['gid']
```

*dot notation*
```yaml
groups.gcrmembers.gid
```


Since you can have nested items with other characters (like dots), array notation is the most robust if you're to choose one.

## Precedence
Ansible variable/fact precedence is the following:
* Configuration Settings (what's set in ansible.cfg)
* Command-line options (when Ansible is invoked)
* Playbook keywords
* Variables

### Variable precedence:

command line values (eg “-u user”)
role defaults [1]
inventory file or script group vars [2]
inventory group_vars/all [3]
playbook group_vars/all [3]
inventory group_vars/* [3]
playbook group_vars/* [3]
inventory file or script host vars [2]
inventory host_vars/* [3]
playbook host_vars/* [3]
host facts / cached set_facts [4]
play vars
play vars_prompt
play vars_files
role vars (defined in role/vars/main.yml)
block vars (only for tasks in block)
task vars (only for the task)
include_vars
set_facts / registered vars
role (and include_role) params
include params
extra vars (always win precedence)

## Referencing variables

Variables often get referenced using jinja2 template style

```yaml
{{ groups['gcrmembers']['gid'] }}
```

You can also transform variables using [jinja2 filters](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html). The documentation gives many examples.


## References
[Using Variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)
[Controlling how Ansible Behaves: precedence rules.](https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html)
[Changing a deeply-nested dict variable in an Ansible playbook](https://www.jeffgeerling.com/blog/2017/changing-deeply-nested-dict-variable-ansible-playbook)
[Playbook Filters](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html)