# vmware_py_scripts
VMware scripts
A basic CLI VMwareutility build on python 3.7
Performs different power operations on VMs identified by the pattern passed 


##################################################################################
usage: vmPowerOps.py [-h] -o OPERATION [-v VMNAME]

Identify and perform power operations on VM, also has listing functionality

optional arguments:
  -h, --help            show this help message and exit
  -o OPERATION, --operation OPERATION
                        Legal inputs: on, off, reset, shutdown, reboot, list
  -v VMNAME, --vmname VMNAME
                        Substring in VM name
###################################################################################
