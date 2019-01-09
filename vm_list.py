####################################################################
#
#	Identifies VM based on patterns passed as arg
#	python vm_list.py <vmname-hint> 
#
####################################################################
from pyvim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import sys
import re
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode=ssl.CERT_NONE

vms = {}
msg = "Is this the VM to reboot (y/n)?"
connect = SmartConnect(host="server", user="user", pwd='password', sslContext=context)
content = connect.content
container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

for managed_object_ref in container.view:
	vms.update({managed_object_ref: managed_object_ref.name})
try:
	for vm in vms:
		if re.match('.*'+sys.argv[1]+'.*' , vm.name ):
			print(vm.name+"\t\t"+vm.runtime.powerState)
			if vm.runtime.powerState == "poweredOn": 
				if input(msg) == 'y':
					vm.Reset()							# You may replace the opreation from the comented
					print("Successfully rebooted..\nSystem is booting please be patient")
#			vm.PowerOn()
#			vm.Suspend()
#			vm.PowerOff()

except:
	print('No argument passed')
		
		
Disconnect(connect)
