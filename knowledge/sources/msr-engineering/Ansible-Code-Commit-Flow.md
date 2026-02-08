# Introduction

There are certain requirements in getting code committed to the Ansible codebase. This tutorial offers a step-by-step guide. Before you do this, this guide assumes you have a configured Visual Studio Code equivalent to the configuration in [the Ansible Playbook Development guide](/Team-Pages/SES/Service-Management/Services/Ansible/Ansible-Playbook-Development).

## OPTIONAL: Create an object in ADO to link your branch to

This can be a User Story, Task or Bug in the Boards section of ADO. Keep in mind that whatever you create to link your branch to, will get moved to the "resolved" state automatically once your pull request succeeds.

Note the number of the User Story, Bug or Task. You'll be linking it to your branch below.

## Create a Branch, and link your object

Under [Repos->Branches](https://dev.azure.com/msresearch/MSR%20Engineering/_git/gcr-ansible/branches) you'll want to create a new branch clicking the meatball menu next to master.
![image.png](/.attachments/image-8492c204-b610-464b-8eeb-be4993ae39c9.png)


Under the New Branch window, name your branch. It's best to use your alias as a folder, with the branch name what makes sense to you. I like to use the number that my linked object is as the name.
![image.png](/.attachments/image-c0d202f4-26cc-4d42-88ed-d861e2cd0366.png)


## Open your branch under Visual Studio Code

Once your branch is under Visual Studio Code, you can open it by clicking the branch link at the bottom
![image.png](/.attachments/image-60e8c2dc-3bfc-4d67-91c7-bd04868a41b6.png)

A dropdown from the middle of the screen will appear with all current local and remote branches, select the one you just created above. If it doesn't show up, run `git fetch --prune` from the CLI on your branch path, and try again.

![image.png](/.attachments/image-1ebdd1b3-a170-4f0b-b9a8-cc1ef1cd1400.png)

This will make Visual Studio code create a local branch for you to edit, you'll see you're on this local branch as indicated by the branch display on the bottom left:
![image.png](/.attachments/image-b8cfae7f-86e6-404d-99f6-1c51dc865953.png)

## Make your Edits and Make a Pull Request

Make the edits you want, commit them to your local branch, and sync them with your remote branch. If you don't know how this works, please see [this tutorial](https://code.visualstudio.com/docs/introvideos/versioncontrol).

Once you're done, it's time to make a pull request under Azure Devops. If you go to Repos, and the Pull Requests menu, you can make one there. If you recently updated a branch, you'll see an indicator to make a PR for that branch. Otherwise you can use the "New Pull Request" Button.

![image.png](/.attachments/image-7009cd9e-9d4d-4d2f-973b-b0c8dee8f8f5.png)

From here, add a title, description, and reviewers. Click the create button once you're done. Once someone approves and completes your pull request your remote branch will be deleted, and you code will be merged to master.

## Remove your local branch

The remote branch will be deleted, but your local branch will remain. You can  delete the local branch on the command line. In this case, with my branch `krisz/102637`

```bash
# Switch to the master branch if not already
git checkout master
# Delete the local branch
git branch -D krisz/102637
Deleted branch krisz/102637 (was c2694768).
# Optional - prune remote branches that vscode hasn't
git fetch --prune
```

## Automating housekeeping
### Powershell
Edit your powershell profile

```powershell
code $PROFILE
```

And add the following to it

```powershell
function git-clean {
  git checkout master
  git pull
  git fetch --prune
  foreach ($i in $(git branch -vv|grep gone|awk '{ print $1 }')){ 
    git branch -D $i
  }
}
```

Now from your ansible repo dir, you can simply run

```powershell
git-clean
```

and perform the normal housekeeping activities in one command after doing your pull request.

### Bash (Linux)
You can do something similar in bash. Create a file that exists in your `$PATH` with the following code, and make it executable:

```bash
#!/usr/bin/env bash
git checkout master
git pull
git fetch --prune
for i in $(git branch -vv|grep gone|awk '{ print $1 }');do
  git branch -D $i
done
```




