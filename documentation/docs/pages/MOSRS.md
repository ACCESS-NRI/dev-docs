## Met Office Science Repository Service (MOSRS)

## MOSRS Authentication on Gadi
To authenticate to MOSRS on Gadi, follow the steps outlined in [Rose, Cylc and MOSRS setup](https://docs.access-hive.org.au/models/run-a-model/run-access-cm2/#rosecylcmosrs-setup).

### mosrs-auth with a simple password input dialog
To reduce the password insertion for `mosrs-auth` to a simple command-line input dialog, you need to set `pinentry-tty` as the default program for GPG password entry. 
To do so, run:
```
cat >> ~/.gnupg/gpg-agent.conf <<< 'pinentry-program /g/data/vk83/apps/spack/0.22/release/linux-rocky8-x86_64_v4/gcc-14.1.0/pinentry-1.3.0-ofj7ps4pibezqnax644jvym6bmnvirjj/bin/pinentry-tty'
gpgconf --reload gpg-agent
```
