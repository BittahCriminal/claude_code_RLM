# Introduction
Most of the point of this is how to get a custom Mariner image from docker working, but this can work with other distros as well. Note that I've used my username (krisz) throughout this tutorial. Change it to suit your needs.

You can also use Mariner WSL from the Windows Store. See here for how:
https://eng.ms/docs/products/mariner-linux/gettingstarted/wsl

# Getting started
If you have a new devbox, you'll need to run `wsl --update` or you'll see a message:
```
This program is blocked by group policy. For more information, contact your system administrator.
```
For more information, see this link:
[Device Experience - Using WSL on managed Windows devices](https://microsoft.sharepoint.com/sites/DeviceExperience/SitePages/Device%20Experience%20-%20Linux%20-%20Apps.aspx?xsdata=MDV8MDJ8fGY4ZWIxMTk3ODU5ODRkNjk0MTI4MDhkYzk2MDFlYjg5fDcyZjk4OGJmODZmMTQxYWY5MWFiMmQ3Y2QwMTFkYjQ3fDB8MHw2Mzg1NTAxODIxNzA1NDIzNzZ8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxMM1JsWVcxekx6RTVPblZJUlMwMk9GZFNOMVJSV2twSGRua3dkVlZwUTAwMGIxVmZTV1pGWTJoNmRrSXRUMnA2TjE5alFXOHhRSFJvY21WaFpDNTBZV04yTWk5amFHRnVibVZzY3k4eE9UcDFTRVV0TmpoWFVqZFVVVnBLUjNaNU1IVlZhVU5OTkc5VlgwbG1SV05vZW5aQ0xVOXFlamRmWTBGdk1VQjBhSEpsWVdRdWRHRmpkakl2YldWemMyRm5aWE12TVRjeE9UUXlNVFF4TlRNM05nPT18NmY2MzFmMzcyMjcxNGM0YTQxMjgwOGRjOTYwMWViODl8YTdjMTM1NjVmYjI3NDU0OTlkZTc1NWU5N2Q2NjEyZTc%3D&sdata=ejFoWTVndjlyUTV3YVJqRlV1dHpvNnpGd3lmd0dCeEZ0QWlhRHVwaElSYz0%3D&ovuser=72f988bf-86f1-41af-91ab-2d7cd011db47%2Ckrisz%40microsoft.com&OR=Teams-HL&CT=1719522288150&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDA2MTMxODQwNiJ9)

# Tutorial
I think it's easiest to use a Dockerfile here, because distributions like Mariner are very bare bones, and need tools to make the image useful for day-to-day use.
```Dockerfile
FROM mcr.microsoft.com/cbl-mariner/base/core:2.0
WORKDIR /
RUN tdnf update -qy; \
  tdnf install -qy openssh sudo shadow-utils vim procps-ng net-tools less azure-cli kubernetes-client golang zip make uuid git mlocate tar which util-linux tzdata iputils traceroute bind-utils awk bc ca-certificates; \
  adduser -G wheel krisz; \
  mkdir -p /home/krisz/.ssh/multiplex; \
  echo "krisz ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/krisz
COPY wsl.conf /etc/wsl.conf
COPY ssh/config /home/krisz/.ssh/config
RUN chown -R krisz:wheel /home/krisz; \
  updatedb
```

The `wsl.conf`
```conf
[user]
default=krisz

[automount]
root = /
options = "metadata"
```

Now to tie it all together, you'll have a directory with your `Dockerfile`, the below script will build it, and export a tar file.

```bash
docker pull mcr.microsoft.com/cbl-mariner/base/core:2.0
docker build .
if $(docker build . | grep -q Successfully);then
  DOCKERBUILDID=$(docker build . | grep Successfully | awk '{ print $3 }')
  docker tag $DOCKERBUILDID cblmariner
  docker run -t cblmariner ls /
  DOCKERCONTAINERID=$(docker container ls -a |grep -i cblmariner|head -n 1| awk '{print $1}')
  echo "Exporting container"
  docker export $DOCKERCONTAINERID > cblmariner.tar
fi
```

From here you'll have the `cblmariner.tar` you can use to import into wsl. I typically build the cblmariner.tar on a separate Linux host. Transfer the tar to your Windows host and do the following in Powershell:
```powershell
mkdir C:\wslDistroStorage\cblMariner
wsl --import cblMariner C:\wslDistroStorage\cblMariner ./cblmariner.tar
```

If you want to unregister the image it's simple:
```bash
wsl --unregister cblMariner
```

# References
[Import any Linux distribution to use with WSL | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/use-custom-distro)
[Install Docker on Windows (WSL) without Docker Desktop - DEV Community](https://dev.to/bowmanjd/install-docker-on-windows-wsl-without-docker-desktop-34m9)
