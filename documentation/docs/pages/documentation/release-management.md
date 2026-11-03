Description of both development->production->release framework details and release strategies.


## Virtual Machines

ACCESS-NRI has currently the option to deploy VMs on:
- NCI NIRIN Cloud
- Nectar ARDC Cloud
- AWS (Untested and comes with additional costs)

The NIRIN and NECTAR Dashboards are very similar.
Deployment of VMs is constrained by the amount of resources allocated to the project you are working on. Please try to estimate
your requirements as accurately as possible.

## Create a VM instance

Instances are created using the *Instance* sub-menu. You can choose a `flavour` for your instance. If you are unsure, a simple Ubuntu LTS image is a good place to start but there are other options.

You need to allocate resources to the VMs. The wizard will help you through the process but keep in mind that time and resource usage is charged to the project so please be reasonable.

Password access is disabled so you need to make sure that you have associated an SSH key pair to the VM. This is done directly from the dashboards. You can generate key pairs on your machine and upload the keys to the system using the dashboard. You then associate keys to the VM.

Network and security groups can also be defined. Make sure you enable the appropriate ports (SSH, HTTP etc)

For remote access, you need to associate a floating IP to your VM using the dashboard.

## Deploying a Web server on Nirin / Nectar

This is based on an Ubuntu 22.04LTS image. We assume that you have an instance running and that you can now ssh into it.

Connecting to an Ubuntu instance is typically done like this:

`ssh ubuntu@xxx.xxx.xxx.xxx`

The `xxx.xxx.xxx.xxx` is the floating IP address associated with your VM.


