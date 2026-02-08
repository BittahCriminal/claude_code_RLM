One thing that is not covered by Azure update management is upgrading the Linux kernel. MLS patch compliance has become so advance that it detects the old image kernel. If you get flagged in S360 for kernel upgrade similar as below 

![image.png](/.attachments/image-801165d7-92ba-470e-8ee6-73d1f91a34d9.png)

Then you can manually run the below script on the affected node to upgrade the Linux kernel


This script is to **dynamically detect the currently installed kernel series**, then **upgrade to the latest available version in that series** from the package repository based on the ubuntu version.

Note that this script will reboot the node so it must be run during the maintenance windows


```
# Maintainer Omid last modified 5/5/2025

#!/bin/bash

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

# Get current kernel series (e.g. 5.15)
kernel_series=$(uname -r | cut -d '-' -f1 | cut -d '.' -f1,2)
echo "Detected kernel series: $kernel_series"

# Find latest matching kernel version
latest_kernel=$(apt-cache search "linux-image-${kernel_series}." \
  | awk '{print $1}' \
  | grep -E "^linux-image-${kernel_series}\.[0-9]+-[0-9]+-generic$" \
  | sed -E "s/linux-image-([^-]+-[^-]+)-generic/\1/" \
  | sort -V \
  | tail -n 1)

if [[ -z "$latest_kernel" ]]; then
  echo "No matching kernel found for series $kernel_series"
  exit 1
fi

echo "Installing latest kernel: $latest_kernel"

# Install kernel packages silently
sudo apt-get update -qq
sudo apt-get install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
  "linux-headers-${latest_kernel}" \
  "linux-headers-${latest_kernel}-generic" \
  linux-headers-generic \
  "linux-image-${latest_kernel}-generic" \
  linux-image-generic \
  "linux-modules-${latest_kernel}-generic" \
  "linux-modules-extra-${latest_kernel}-generic"

# Mark as auto
sudo apt-mark auto \
  "linux-headers-${latest_kernel}" \
  "linux-headers-${latest_kernel}-generic" \
  linux-headers-generic \
  "linux-image-${latest_kernel}-generic" \
  linux-image-generic \
  "linux-modules-${latest_kernel}-generic" \
  "linux-modules-extra-${latest_kernel}-generic"

# Upgrade rest of system quietly
sudo apt-get upgrade -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"

# Optional: clean old kernels
# sudo apt-get autoremove -y --purge

echo "Kernel $latest_kernel installed. Rebooting in 5 seconds..."
sleep 5
sudo reboot
```
