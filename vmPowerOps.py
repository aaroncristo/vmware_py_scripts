from pyvim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import argparse
import sys
import re
import ssl

def getArgs():
	operations = [ 'on', 'off', 'reset', 'shutdown', 'reboot' , 'list']
	parser = argparse.ArgumentParser(description='Identify and perform power operations on VM, also has listing functionality.')
	parser.add_argument('-o','--operation', required=True, default=list, help="Legal inputs: " + ", ".join(operations))
	parser.add_argument('-v', '--vmname',  help="A substring in VM name" )
	args = parser.parse_args()
	if args.operation not in operations:
		raise Exception("Unknown operation")
	return args
	
def performOperation( vms, arg ):
	op = arg.operation
	pat = arg.vmname
	for vm in vms:
		name = vm.name
		state = vm.runtime.powerState
		if re.match('.*' + pat + '.*' , name ,re.IGNORECASE) if pat is not None else True :
			print('{:<40}{:<30}'.format(name ,state))
			if  op == "list": 			#Skips the rest 
				continue 
			elif pat is None:			# To avoid large scale actions
				raise Exception("Forbidden. Please provide a VM name")
			elif  input("Is " + name + " the VM to be handled (y/n)?") is "y" :
				success = False
				if state == "poweredOn":
					if op == "off":
						vm.PowerOff()		# Force Power Off
						success = True
					elif op == "shutdown":
						vm.ShutdownGuest()	# Gracefull power off
						success = True
					elif op == "reset":
						vm.Reset()			# Force reinitiate power
						success = True
					elif op == "reboot":
						vm.RebootGuest()	# Gracefull reboot
						success = True	
				else:
					if op == "on":
						vm.PowerOn()		# Initiate power
						success = True
					print('here')	
					
				if success:
					print("Operation successful !!")
				elif op is not None:
					print("Oops ..!  The operation is forbidden :(")
					
	return "Done.. Checking..!!"
	
try:
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	context.verify_mode=ssl.CERT_NONE

	vms = {}
	msg = "Is this the VM to reboot (y/n)?"
	##############################################################################
	#	update the values of host user pwd accordingly
	##############################################################################
	connect = SmartConnect(host="host", user="username", pwd='password', sslContext=context)
	content = connect.content
	container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)

	arg = getArgs()
	
	for managed_object_ref in container.view:
		vms.update({managed_object_ref: managed_object_ref.name})
		
	print(performOperation( vms, arg ))
			
except Exception as e:
	print('Error: '+str(e))
finally:		
	Disconnect(connect)
