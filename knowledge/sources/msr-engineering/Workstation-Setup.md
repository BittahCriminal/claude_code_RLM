# Requirements & Recommendations

- Linux environment (the ansible-lint tool will not run on Windows)
- SSH key configured with Azure DevOps (If you work in Chef, you should probably already have this)
  - Start the built-in SSH-Agent service on your Windows machine
  - Configure your SSH to ensure agent forwarding is configured
- VSCode (Highly Recommended)
  - Modules:
    - VSCode Remote
      - SSH
      - SSH-Edit
      - WSL
    - Python
    - vscode-ansible

We use [pre-commit](https://pre-commit.com/) to apply policies and linting to our repository.

The Windows Subsystem for Linux can be QUITE slow for some operations.  For day-to-day work it is just fine but your initial setup of pre-commit will probably take a while.  WSL2 is much faster but is not available until Windows 10 20H1.

-----------

## Linux Environment

I use the WSL for most things currently.  Here are the [installation/setup](https://docs.microsoft.com/en-us/windows/wsl/install-win10) instructions if you choose to go this route.

Once you have a Linux environment, install the dependencies: Python (if not already present), pip and pre-commit:

```
sudo apt install python3 python3-distutils
# Thank you krisz for explaining why we don't take the repository's possibly outdated/stuck python3-pip....
# This is the idiomatic way of installing pip
sudo curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
sudo python3 /tmp/get-pip.py
sudo pip3 install pre-commit
```

If the pip3 installation fails due to a distutils version of PyYaml already existing, try downgrading the pip3 version, per [this StackOverflow question](https://stackoverflow.com/questions/49911550/how-to-upgrade-disutils-package-pyyaml).

Finally, decide if you want pre-commit to be automatically enabled on all eligible cloned repositories (__*highly recommended*__) or if you want to manually enable it per-repository.  If you select the automatic option, this will only effect repositories where pre-commit is configured in the repository.  It will not affect repositories which are not using pre-commit.

To enable pre-commit automatically on newly-cloned repositories:

```
mkdir ~/.git-template
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir ~/.git-template
```

-----------
## Windows (Workstation, editor) environment

You need to have the OpenSSH for Windows feature installed in order to have the best experience.  We can also make sure the agent starts automatically.  Run the following in an administrative PowerShell window:

```
if(Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Client*' | Where-Object State -ne 'Installed') {
  Add-WindowsCapability -Online -Name OpenSSH.Client
}
Set-Service -Name ssh-agent -StartupType Automatic
Start-Service ssh-agent
```

### Configure Editor (VS Code)

Install Visual Studio Code and the recommended extensions.  If you like, this will do that for you:

```
Function Save-InstallerFile {
  [CmdletBinding()]
  param(
    [Parameter(mandatory=$true)]
    [string] $uri
  )
  $oldProgressPreference = $ProgressPreference
  $ProgressPreference = "SilentlyContinue"
  $tempFile = New-TemporaryFile
  Rename-Item -Path $tempFile.FullName -NewName "$($tempFile.BaseName).exe"
  $destination = Get-ChildItem -Path $tempFile.DirectoryName | Where-Object { $_.Name -eq "$($tempFile.BaseName).exe" }
  $installerResponse = Invoke-WebRequest -Uri $uri -UseBasicParsing
  if($PSVersionTable.PSEdition -eq 'Core') {
    Set-Content -Path $destination.FullName -Value $installerResponse.Content -AsByteStream
  } else {
    Set-Content -Path $destination.FullName -Value $installerResponse.Content -Encoding Byte
  }
  $ProgressPreference = $oldProgressPreference
  return $destination
}

# Older versions of PowerShell do not include New-TemporaryFile
if(-not [bool](Get-Command 'New-TemporaryFile' -errorAction SilentlyContinue))
{
    Write-Host "New-TemporaryFile Cmdlet is missing, creating replacement"
    Set-Item function:New-TemporaryFile -Value {
        <#
        .SYNOPSIS
        New-TemporaryFile completes the same task as the PowerShell v5.0+ cmdlet of the same name
        #>
        $tempFile = New-Item -ItemType File -Path (Join-Path ([System.IO.Path]::GetTempPath()) ([System.IO.Path]::GetRandomFileName()))
        Write-Host "Created temporary file ${tempfile} with New-TemporaryFile replacement function"
        return $tempFile
    }
}

# Do we have a Visual Studio Code?
while($true) {
  try {
    if(Get-Command code -ErrorAction SilentlyContinue) {
      # Looks good to me
      break
    }
  } catch {
    # OK, go get it...
    $oldProgressPreference = $ProgressPreference
    $ProgressPreference = "SilentlyContinue"
    $uri = 'https://aka.ms/win32-x64-user-stable'
    Write-Host "VSCode is missing, downloading installer from $uri"
    $installFile = Save-InstallerFile -uri $uri
    $ProgressPreference = $oldProgressPreference
    Start-Process $installFile.FullName
    Read-Host "Press <Enter> once the installation has been completed..."
    # Update PATH for this session...
    $machinePath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
    $userPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::User)
    $env:Path = "${machinePath};${userPath}"
  }
}

$desiredExtensions = @("ms-vscode-remote.remote-ssh",
                       "ms-vscode-remote.remote-ssh-edit",
                       "ms-vscode-remote.remote-ssh-explorer",
                       "ms-vscode-remote.remote-wsl",
                       "ms-vscode.powershell",
                       "ms-vsts.team",
                       "ms-python.python",
                       "vscoss.vscode-ansible")
$vsCodeExtensions = code --list-extensions
foreach ($extension in $desiredExtensions) {
  if($extension -notin $vsCodeExtensions) {
    Write-Host "Installing ${extension} extension for VSCode..."
    code --install-extension $extension 2>$null
  }
}
```

Launch VSCode and edit your SSH configuration (if necessary).  Use the SSH extension to access your configuration file:  Select the green button in the lower left, then select "Remote-SSH: Open Configuration File" from the menu.

![image.png](/.attachments/image-868f5d5e-7851-4762-8d8c-5ba825715448.png)

Here are some sane defaults.  **Make sure that the "Host \*" entry is LAST**:

```
# This name is just an alias and can be anything.  If set, it will appear in VSCode for easy selection
Host MyOtherHostAlias
  # Enter a DNS name or an IP address
  HostName xxx.xxx.xxx.xxx
  # If you need a special port, you can set one
  Port 54422
  # The value in "Host *" becomes the default...if you set something here, it will override
  User jordan
  # Options which are not set here inherit from the "Host *" entry, e.g. ForwardAgent...

Host *
  # Put your username here
  User REDMOND.jordan     
  Protocol 2
  ForwardX11 no
  Compression yes
  # You definitely want this!
  ForwardAgent yes 
```

If you __*do not*__ go the WSL route, make sure that you have added a host entry to your SSH config file: doing so will add it to the quick-launch menu (and you can configure protocol version, compression, and agent forwarding here if you like, among other things.  **Make sure that host-specific entries appear ABOVE a "Host \*" entry in your SSH Config!**

-----------

## First-Time Repository Setup

Once connected, make sure you have a terminal ( Terminal-> New Terminal if you don't have one in the bottom of your window).  Unfortunately the initial checkout and setup isn't as easy through VSCode as it seems it will let you __*open*__ a folder or workspace, but not create one new.

Checkout the repo:

```
sudo mkdir /opt/ansible/repo/myrepo
sudo chown $(whoami) /opt/ansible/repo/myrepo
git clone git@ssh.dev.azure.com:v3/msresearch/MSR%20Engineering/gcr-ansible /opt/ansible/repo/myrepo
```
You may now select "Open Folder" from the file menu and navigate to your repository.  You can edit in VSCode as if you were working locally.

If you did not opt for the automatic pre-commit configuration earlier, you need to install the pre-commit hooks.  To do so, in your terminal run:

```
# Run the below as the user you used to check out your code
# If you use root for the below command but a normal user for checkout,
# you'll get errors.
pre-commit install
```
-----------

## Working in the repository

Create, edit and delete as desired.  You can run the pre-commit checks ad-hoc if you want:

```
# Run the below as the user you used to check out your code
# If you use root for the below command but a normal user for checkout,
# you'll get errors.
#
pre-commit install
# Run against staged files
pre-commit run

# Run against specific file(s)
pre-commit run --file FILE [...]

# Run against all files in the repository (This is how the build pipeline checks your work)
pre-commit run --all-files

```

When you make a commit via VS Code, the pre-commit checks could succeed or they could fail.  In the event of a failure, you will see a popup window such as this one:  note that VS Code only shows the *last* line of the output, so if you get an error saying "PASSED", do not be alarmed.

![image.png](/.attachments/image-360bd436-07f3-4231-b28c-e8667ee523df.png)

Take a look at the rest of the output.  Press "View Git Log" or select the output pane to view the results.

![image.png](/.attachments/image-2e4ee4ec-0f41-4bb8-b9ad-5e403bc3676d.png)

This is the advantage of running the test prior to commit from the terminal pane:  at the very least, you will get colorized output:

![image.png](/.attachments/image-6a15a9b9-8f4b-4525-8fa5-4c552fa2b29c.png)

**What to do if your commit fails**

If your commit fails, you *may* need to resolve the issues before re-attempting the commit.  For instance, if the "Trim Trailing Whitespace" check fails, the tool will automatically remove the whitespace for you.  **However:**  Since this changes the staged file, you must re-stage the file before committing again.

For other failures that cannot be automatically corrected, you must make the adjustments manually and then re-stage the file before re-committing.

In either case, the general workflow is:

1. After the commit fails, check to see if there are un-staged files:  this is a hint that the tool has corrected them for you.
1. Stage the files to prepare for re-committing the change.
1. If the tool reports files that it cannot automatically correct, update those files as necessary and then re-stage them.
1. Commit the changes.

Once your commit is successful on your development workstation, you can be confident that it will pass the automated build checks.  Publish your branch and submit your PR.