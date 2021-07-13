#!/usr/bin/env python3

"""
	IRC Send.
	A utility to send IR remote control codes from the Raspberry Pi.
	Copyright (C) 2021 Michael Paul Korthals.

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


## IRC Send.
#  A utility to send IR remote control codes from the Raspberry Pi.
#  Created on 2021-07-05.
#
#  @author Michael Paul Korthals


# Import Python language packages

import argparse
import datetime
import json
import os
import platform
import sys
import time


#*****************************************************************************************************
# ENABLE REMOTE DEBUGGING IN ECLIPSE DEVELOPING ENVIRONMENT:
# Remote debug service is available on the development workstation at port 5678".
# Start this program on the remote system with parameter "--db" or "--debug" as last parameter.
# 
# SOURCE SYNCHRONISATION:
# While developing, use WinSCP on development workstation to permanently keep 
# the development folder on the target Linux test machine up-to-date.
#
#
# IN CASE OF FAILURE:
#    * Close Eclipse.
#    * Delete the folder "<workspace>/.metadata/.plugins/org.eclipse.e4.workbench",
#      where "<workspace>" is the folder of your Eclipse workspace.
#        * This will reinitialize your Eclipse workbench settings.
#		 * WARNING: Do this only, if you have you have eliminated all other problems.
#    * Open Eclipse.
#    * Ensure that the "PyDev plug-in" for Eclipse is installed and up-to-date
#      on the development workstation and the "PyDev" menu item is visible
#      in the "Debug" perspective.
#        * See [Menu] -> Help -> Eclipse Marketplace -> Installed.
#    * Ensure the the "pydevd" is installed on the test machine:
#        * # pip show pydevd
#        * # pip install pydevd==
#        * It is recommended to update it, if a newer version is available.
#            * # pip install pydevd --upgrade
#    * Set the perspective in the upper right corner in Eclipse:
#        * Select the "PyDev" perspective (blue snake icon).
#        * Open the Python file, which will be debugged.
#        * Select the "Debug" perspective (green bug icon).
#    * Start the remote debugging server via [Menu] -> PyDev -> Start Debug Server
#    * Ensure that all the remote debugging data are up to date and valid:
#        * The source folders (local and remote)
#            * See below: "MY_PATHS_FROM_ECLIPSE_TO_PYTHON". ESSENTIAL!!!
#        * The port forwarding rules on the network components between
#          the test machine and the development workstation, if any.
#        * The environment variable "DEBUG_HOSTNAME" in the 
#          login shell of the test user and root user on the test machine. ESSENTIAL!!!        
#    * Start the script which will be debugged on the remote test machine.
#    * Wait ~15 seconds until the script execution will stop at the 
#      first code line after the "pydevd.settrace( ... )" command (see below).
#      SUCCESS!!!
#    * Finally debug the script. 
# 
if len(sys.argv) >= 2 and sys.argv[-1] in ['-db', '--debug']:
	# Append PydDev remote debugger
	# Import the PyDev remote debugger
	import pydevd 
	from pydevd_file_utils import setup_client_server_paths
	import socket 
	# Configure the Eclipse project path 
	# on the Windows Development Workstation within the "eclipse-workspace" folder
	# and on the remote test machine 
	# exactly in this order and all paths must be absolute:
	hostname = socket.gethostname()
	MY_PATHS_FROM_ECLIPSE_TO_PYTHON = [
		(
			f'C:\\Users\\Paul\\eclipse-workspace\\{hostname}-irrcd', # local (development workstation)
			f'/home/pi/eclipse-workspace/{hostname}-irrcd'  # remote (test machine)
		)
	]
	debug_hostname = os.environ['DEBUG_HOSTNAME'] # The localhost IP address on which the debug server is listening 
	if debug_hostname == None: debug_hostname = 'unknown_host'
	debug_port = 5678 # The TCP/IP port on which the debug server is listening
	# Enable remote debugging 
	setup_client_server_paths(MY_PATHS_FROM_ECLIPSE_TO_PYTHON)	
	try: 
		pydevd.settrace(debug_hostname, port=debug_port, stdoutToServer=True, stderrToServer=True)
	except:
		print(f'ERROR: Cannot connect to debugger at "tcp://{debug_hostname}:{debug_port}".')
		sys.exit(1)

#*****************************************************************************************************


# Import community packages

try:
	import pigpio
except:
	sys.stdout.write('ERROR: The PyPi package "pigpio" is missing. Execute "pip install pigpio" to install it.\n\n')
	sys.exit(65)
	
try:
	import subprocess 
except:
	print('ERROR: Cannot find library "subprocess".\nExecute "pip install subprocess" to setup it.')
	sys.exit(65)


## A class to send IR remote control codes from Raspberry Pi.
#  	
class IRCSenderProgram:
	
	## The command line arguments object. Default: None.
	args = None
	
	## The Raspberry Pi GPIO control object. Default: None.
	pi = None
	
	## CONSTRUCTOR.
	#
	def __init__(self):
		# Create argument parser
		parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description="""\
IRC Send.
========= 
Copyright (C) 2021 Michael Paul Korthals.
This program comes with ABSOLUTELY NO WARRANTY; for details 
see <https://www.gnu.org/licenses/>.
This is free software, and you are welcome to redistribute it
under certain conditions; see the GNU General Public License 
for details.

Infrared Remote Control Sender
------------------------------
This program simulates the key presses
of the original IRC hardware, which has been 
learned before by the "irc_learn.py."
program and saved to a JSON file.

It works on Raspberry Pi hardware only with
Raspian Buster+, Python 3.6+ including the 
"pigpio" package installed.

It is also backwards compatible to 
the "irrp.py" JSON files.

You must define the GPIO port in BCM 
notation, where your IR sender is attached.

Before you use this program, your system 
must learn the IR signal sequences of
your remote control devices.

Use the program "irc_learn.py" to record
all the key presses of your remote control
and to save the data to a JSON file.

This program is only recommended for testing 
purposes.

In production please import the "irc_api.py" 
to integrate the IR Sender API into your 
"Universal Remote Control" daemon, which API 
can be accessed via TCP/IP network by your 
"Cinema Control Center" web application on 
your "Media Server".\
			""",
			epilog="""\
EXAMPLE:
--------
1) Send on GPIO port 17 and go to the menu of the iiyama monitor prolite tf3238msc and increase the volume by 3 levels. This device requires the double layer protocol.
$ ./irc_send.py --gpio 17 --input data/iiyama_monitor_prolite_tf3238msc.json --key_names "menu down ok down down down ok right right right menu"
			"""
		)
		# Define the arguments
		parser.add_argument(
			'-bc', 
			'--bypass_checks', 
			help='Bypass technical checks at launch time and do not check dependencies. This will help to launch the program much faster.', 
			action='store_true'
		)
		parser.add_argument(
			'-d', 
			'--device', 
			help='Define the LIRC recording device path. Default: "/dev/lirc1".', 
			type=str, 
			default='/dev/lirc1'
		)
		parser.add_argument(
			'-db', 
			'--debug', 
			help='Start this program in "debug" mode. This parameter must be the last argument in the command line. This feature is only working when connected to the developer workstation on the same LAN segment.', 
			action='store_true'
		)
		parser.add_argument(
			'-dr', 
			'--dry_run', 
			help='Do a dry run without sending the IR signal.', 
			action='store_true'
		)
		parser.add_argument(
			'-cf', 
			'--carrier_frequency', 
			help="Carrier frequency (kc/s). Default: 38.0.", 
			type=float, 
			default=38.0
		)
		parser.add_argument(
			'-g', 
			'--gpio', 
			help="GPIO pin number (BCM notation) for sending an IR signal.", 
			required=True, 
			type=int
		)
		parser.add_argument(
			'-kn', 
			'--key_names', 
			help='Define the infrared remote control key names to send. I case of an empty string, the list of key names will be displayed. Nithing will be sent.',
			required=True, 
			type=str
		)
		parser.add_argument(
			'-ks', 
			'--key_space', 
			help='Define the delay between two key presses (seconds). Default: 1.0.',
			type=float,
			default=1.0
		)
		parser.add_argument(
			'-i', 
			'--input', 
			help='Define the file path to load the JSON file of the infrared remote control.', 
			type=str, 
			required=True
		)
		parser.add_argument(
			'-no', 
			'--no_repeat', 
			help='Do not send any repetitions of the IR signal.', 
			action='store_true'
		)
		parser.add_argument(
			'-rc', 
			'--repeat_count', 
			help='Define how often the sender must repeat the IR signal sequence in the single layer or double layer protocol (count as int). Default: 3.', 
			type=int, 
			default=3
		)
		parser.add_argument(
			'-rs', 
			'--repeat_space', 
			help='Define the space (L-signal) width between 2 repetitions (in microseconds as int). Default: 32000.', 
			type=int, 
			default=32000
		)
		parser.add_argument(
			'-ts', 
			'--timeout_space', 
			help='Define the timeout after the first press on the same key will be forgotten (in seconds as int). Default: 30.', 
			type=int, 
			default=30
		)
		parser.add_argument(
			'-v', 
			'--verbose', 
			help='Allow verbose output to console.', 
			action='store_true'
		)
		# Parse the arguments
		try:
			self.args = parser.parse_args()
		except argparse.ArgumentError:
			sys.stdout.write(f'ERROR: Wrong or missing command line arguments.\nCall "./{os.path.basename(sys.argv[0])} -h | --help" to see how to handle the syntax.\n')
			sys.exit(22) # 22 = Invalid argument
		# Technical checks
		os_name = os.name
		pf_name = platform.system()
		if os_name != 'posix' or pf_name != 'Linux':
			sys.stdout.write(f'ERROR: This program does not run on "{os_name}/{pf_name}". Run it on "posix\Linux" only.')
			sys.exit(1) # 1 = Operation not permitted
		if not self.args.bypass_checks: 
			# RELEASE: Get the Linux version code name
			command = 'cat /etc/*-release 2>/dev/null';
			p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
			std_out = p.communicate()[0].strip()
			rc = p.returncode
			id_like = 'unknown'
			distribution_id = "unknown"
			version_id = 'unknown'
			version_codename = 'unknown'
			if rc != 0:
				sys.stdout.write(f'WARNING: Cannot determine the system OS release information (return code {rc}).\n')
			else:
				items = std_out.replace('"','').split('\n')
				find0 = 'ID_LIKE='
				find1 = 'ID='
				find2 = 'VERSION_ID='
				find3 = 'VERSION_CODENAME='
				for item in items:
					if item.startswith(find0): 
						id_like = item.replace(find0, '').strip().lower()
					elif item.startswith(find1): 
						distribution_id = item.replace(find1, '').strip().lower()
					elif item.startswith(find2):
						version_id = item.replace(find2, '').strip().lower()
					elif item.startswith(find3):
						version_codename = item.replace(find3, '').strip().lower()
			if self.args.verbose: sys.stdout.write(f'Linux distribution is: {id_like}/{distribution_id} {version_id} ({version_codename})\n')
			if id_like != 'debian' or distribution_id != 'raspbian':
				sys.stdout.write(f'ERROR: This program is not running on Linux distributions like "{id_like}/{distribution_id}".\nIt is designed for "debian/raspbian" distribution on Raspberry Pi hardware only.\n')
				sys.exit(1) # 1 = Operation not permitted
			# DEPENDENCY: Check if LIRC is installed (this will take a while)
			command = 'apt -qq list lirc 2>/dev/null'
			p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
			std_out = p.communicate()[0].strip()
			rc = p.returncode
			if rc != 0:
				sys.stdout.write(f'ERROR: Cannot determine that LIRC is installed on this system (return code {rc}).\n')
				sys.exit(1) # 1 = Operation not permitted
			if not std_out.endswith('[installed]'):
				sys.stdout.write(f'ERROR: LIRC is not installed on this system.\nExecute "sudo apt install lirc" to install it.\nYou must follow to the system-specific LIRC setup instructions\nfor "{distribution_id} {version_codename}".\n\n')
				sys.exit(65) # 65 = package not installed
			if self.args.verbose: sys.stdout.write('LIRC is installed on this system.\n\n')
	
	## Run the program.
	#
	#  @return The exit code as integer, which is 0 in case of success. 
	def run(self):
		# INITIALZATION
		# Connect to Raspberry Pi GPIO
		self.pi = pigpio.pi()
		if not self.pi.connected:
			sys.stdout.write(f'ERROR: Cannot connect to Raspberry Pi GPIO.\n')
			return 1
		# Setup the GPIO port for output/sending
		try:
			self.pi.set_mode(self.args.gpio, pigpio.OUTPUT)
		except:
			sys.stdout.write(f'ERROR: Cannot set output mode for GPIO pin {self.args.gpio} (BCM).\n')
			self.pi.stop()
			return 1
		# Send the IR signal sequences depending on the program arguments
		rc = self.send()
		# Disconnect from Raspberry Pi GPIO
		try:
			self.pi.set_mode(self.args.gpio, pigpio.INPUT)
			self.pi.stop()
		except: 
			pass
		return rc
	
	## Send IR signal sequences depending on the program arguments.
	#
	#  @return The exit code as integer, which is 0 in case of success. 
	def send(self):
		# Forked from souri-t on GitHub by michaelpaulkorthals 
		# Original source: https://github.com/souri-t/RemoteControl-RPI/blob/master/remote/bin/irrp
		#
		# by michaelpaulkorthals: Code review and adoption to the interfaces of this program and to my quality level.
		# 
		# Load the IR remote control data from file
		sys.stdout.write(f'Loading file "{self.args.input}".\n')
		try:
			f = open(self.args.input, "r")
			try:
				keys = json.load(f)
			except:
				sys.stdout.write(f'ERROR: Cannot load or JSON decode file "{self.args.input}".\n')
				f.close()
				return 1
			f.close()
		except:
			sys.stdout.write(f'ERROR: Cannot open file "{self.args.input}" to read.\n')
			return 2
		if self.args.verbose:
			sys.stdout.write(f'The data file "{self.args.input}" has been successfully loaded.\n')
		irc_name = os.path.basename(self.args.input)[0:(len(self.args.input.split('.')[-1]) + 1)*(-1)]
		irc_data_dir = os.path.dirname(self.args.input)
		# Ensure downwards compatibility to former "irrp.py" recordings
		keys_stringlist = ' '.join(list(keys.keys()))
		key_names = keys_stringlist.split(' ')
		first_item = keys[key_names[0]]
		# In the simple program the first item is a list, not a dict
		if type(first_item) is list:
			# Automatically migrate to the new data model
			new_keys = {}
			for key_name in key_names:
				new_key = {
					'type': 0,
					'first': keys[key_name],
					'next': None,
					'repetition_first': None,
					'repetition_next': None,
					'repeat_count': 0,
					'repeat_space': 0,
					'timeout_space': None
				}
				new_keys[key_name] = new_key
			keys = new_keys
		sys.stdout.write('Done.\n')
		# Prepare to send the IR signal
		self.pi.wave_add_new()
		# Start to send the keys
		if self.args.verbose:
			sys.stdout.write(f'Sending keys ...\n')
		if len(self.args.key_names) == 0: 
			# Display the list
			sys.stdout.write(f'List of keys:\n{keys_stringlist}\n\n')
		else:
			# Send keys
			key_names = self.args.key_names.split(' ')
			for n in range(0, len(key_names)):
				key_name = key_names[n]
				if key_name in keys:
					if self.args.verbose:
						sys.stdout.write(f'Sending key "{key_name}" ...\n')
					key = keys[key_name]
					# Compose the IR signal
					sequences = [] 
					key_type = key['type']
					if key_type == 0:
						# Single shot protocol 
						sequences.append(key['first'])
					elif key_type == 1:
						# Single layer protocol
						sequences.append(key['first'])
						if not self.args.no_repeat:
							for i in range(key['repeat_count']):
								sequences.append(key['repetition_first'])
					elif key_type == 2:
						# Double layer protocol
						status_file_path = os.path.join(irc_data_dir, f'.status_{irc_name}_{key_name}.json') 
						# Load the key status from file
						key_status = None
						try:
							f = open(status_file_path, "r")
							try:
								key_status = json.load(f)
							except:
								pass
							f.close()
						except:
							pass
						# Depending on the content of the status file 
						# and the current date and time
						# select the correct IR signal sequences. 
						now = datetime.datetime.now()
						if (
							key_status == None 
							or 
							(not ('timeout' in key_status)) 
							or 
							now > datetime.datetime.strptime(key_status['timeout'], '%Y-%m-%d %H:%M:%S')
						):
							sequences.append(key['first'])
							if not self.args.no_repeat:
								for i in range(key['repeat_count']):
									sequences.append(key['repetition_first'])
							timeout = now + datetime.timedelta(seconds=key['timeout_space'])
							timeout_str = timeout.strftime('%Y-%m-%d %H:%M:%S')
							key_status = {'timeout': timeout_str}
						else:
							sequences.append(key['next'])
							if not self.args.no_repeat:
								for i in range(key['repeat_count']):
									sequences.append(key['repetition_next'])
							key_status = None
					else:
						sys.stdout.write(f'ERROR: Unknown protocol type "{key_type}".\n')
						return 1
					# Bypass the sending if the "--dry_run" argument is set
					if not self.args.dry_run:
						if self.args.verbose: sys.stdout.write('Sending ...\n')
						# Send the IR signal sequences
						for m in range(0, len(sequences)):
							sequence = sequences[m]					
							# Create IR signal
							marks_wid = {}
							spaces_wid = {}
							wave = [0]*len(sequence)
							for i in range(0, len(sequence)):
								ci = sequence[i]
								# Check if index is an odd number
								if i & 1: 
									# Space
									if ci not in spaces_wid:
										self.pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
										spaces_wid[ci] = self.pi.wave_create()
									wave[i] = spaces_wid[ci]
								else: 
									# Mark
									if ci not in marks_wid:
										wf = self.carrier(self.args.gpio, self.args.carrier_frequency, ci)
										self.pi.wave_add_generic(wf)
										marks_wid[ci] = self.pi.wave_create()
									wave[i] = marks_wid[ci]
							# Send the signal
							self.pi.wave_chain(wave)
							while self.pi.wave_tx_busy():
								time.sleep(0.002)
							for i in marks_wid:
								self.pi.wave_delete(marks_wid[i])
							marks_wid = {}
							for i in spaces_wid:
								self.pi.wave_delete(spaces_wid[i])
							spaces_wid = {}
							marks_wid = {}
							# Send space between IR signal repetitions
							if m < len(sequences) - 1:
								self.pi.wave_add_generic([pigpio.pulse(0, 0, key['repeat_space'])])
								po = self.pi.wave_create()
								self.pi.wave_chain([po])
								while self.pi.wave_tx_busy():
									time.sleep(0.002)
								self.pi.wave_delete(po)
						if self.args.verbose: sys.stdout.write('... sent.\n')
					# After the IR signal has been sent 
					if key_type == 2:
						# Double layer protocol
						if key_status == None:
							# Delete the status file
							if os.path.isfile(status_file_path):
								try:
									os.remove(status_file_path)
								except:
									sys.stdout.write(f'ERROR: Cannot remove the status file "{status_file_path}".\n')
									return 13
						else:
							# Save the status file
							try:
								f = open(status_file_path, "w")
								try:
									json.dump(key_status, f, indent='\t')
								except:
									sys.stdout.write(f'ERROR: Cannot JSON encode and save the status to file "{status_file_path}".\n')
									f.close()
									return 1
								f.close()
							except:
								sys.stdout.write(f'ERROR: Cannot open file "{status_file_path}" to write.\n')
								return 13
					# Done
					sys.stdout.write(f'The IR signal for key "{key_name}" has been successfully sent.\n')
					# Space between two IR signals
					if n < len(key_names) - 1:
						time.sleep(self.args.key_space)
				else:
					sys.stdout.write(f'ERROR: Id "{key_name}" not found.\n')
					return 1
		sys.stdout.write(f'The program has been successfully completed.\n')
		return 0
	
	## Compose the carrier square wave data for the modulated pulse.
	#
	#  @param gpio The Raspberry Pi GPIO port (BCM notation) where to send the signal.
	#  @param frequency The IR signal carrier frequency in kc/s.
	#  @param micros The duration of the IR signal modulation pulse in microseconds.
	#  @return The "pigpio"-compatible data array to define the IR carrier wave for the modulated pulse.  
	def carrier(self, gpio, frequency, micros):
		# Forked from souri-t on GitHub by michaelpaulkorthals. 
		# Original source: https://github.com/souri-t/RemoteControl-RPI/blob/master/remote/bin/irrp
		#
		# by michaelpaulkorthals: Code review and adoption to my quality level. 
		#
		wf = []
		cycle = 1000.0 / frequency
		cycles = int(round(micros / cycle))
		on = int(round(cycle / 2.0))
		sofar = 0
		for c in range(cycles):
			target = int(round((c + 1) * cycle))
			sofar += on
			off = target - sofar
			sofar += off
			wf.append(pigpio.pulse(1 << gpio, 0, on))
			wf.append(pigpio.pulse(0, 1 << gpio, off))
		return wf
	

# MAIN PROGRAM
# Create the class object
ircsp = IRCSenderProgram() 
# Run the main program
sys.exit(ircsp.run())
	
		