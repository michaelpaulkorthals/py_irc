#!/usr/bin/env python3

"""
	IRC API.
	An API module for Raspberry Pi, e.g. to send IR remote control codes via a TCP / IP service.
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


## IRC API.
#  An API module for Raspberry Pi, e.g. to send IR remote control codes via a TCP / IP service.
#  Created on 2021-07-08.
#
#  @author Michael Paul Korthals

# Import Python language packages

import datetime
import json
import os
import sys
import time

# Import community libraries

try:
	import pigpio 
except:
	sys.stderr.write('ERROR: Cannot find library "pigpio".\nExecute "pip install pigpio" to setup it.\n')
	sys.exit(65)


## A class to send remote control data on Raspberry Pi.
#  It provides the features of an API-based universal remote control.
#
class UniversalRemoteControl:
	
	## List of IR code JSON files in the ./data sub folder. Default: Empty list.
	devices = []
	
	## Raspberry Pi object. Default: None.
	pi = None
	
	## GPIO port number for transmitting IR signals.
	gpio = None

	## Path to the folder, where the IR remote control data is stored. Default: Empty string.   
	data_dir = ''
	
	## Output verbose information. Default: False.
	verbose = False
	
	## CONSTRUCTOR.
	#
	#  @param gpio The Raspberry Pi GPIO port, on which the IR sender is connected.
	#  @param data_dir The path to the folder, where the IR remote control data is stored. Default: The "data" sub directory in the script folder. 
	#  @param verbose Output verbose information. Default: False.
	def __init__(
			self, 
			gpio, 
			data_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data'),
			verbose=False
	):
		# Init properties
		self.gpio = gpio 
		self.data_dir = data_dir
		self.verbose = verbose
		# Connect to Raspberry Pi
		self.pi = pigpio.pi()
		if not self.pi.connected:
			sys.stderr.write('ERROR: Cannot initialize "pigpio".\n')
			sys.exit(1)
		# IR TX connect to the GPIO port
		self.pi.set_mode(self.gpio, pigpio.OUTPUT)
		# Load devices
		self.devices = []
		data_dir = os.path.join(data_dir)
		for (path, dirs, files) in os.walk(data_dir): #@UnusedVariable
			for name in files:
				filepath = os.path.join(path, name) 
				device_name, file_extension = os.path.splitext(name)
				if file_extension.lower() == '.json' and name.startswith('.') == False:
					try:
						with open(filepath, 'r') as file:
							# Load IR remote control JSON data as a dictionary
							keys = json.load(file)
							file.close()
					except:
						Exception(f'The infrared code file "{filepath}" cannot be opened or has errors.')
						break
					# Ensure downwards compatibility to former "irrp.py" recordings
					keys_stringlist = ' '.join(list(keys.keys()))
					key_names = keys_stringlist.split()
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
					# Store data
					data_record = {}
					data_record['device_name'] = device_name
					data_record['filepath'] = filepath
					data_record['keys'] = keys
					self.devices.append(data_record)
			break
	
	## DESTRUCTOR.
	def __del__(self):
		# IR TX disconnect from the GPIO port
		self.pi.set_mode(self.gpio, pigpio.INPUT)
		# Disconnect from Raspberry Pi
		self.pi.stop() 
	
	## Send the IR signals sequence for specific key to a specific device.
	#  
	#  @param device_name Name of the IR-controlled device (see file name without extension in the "./data" folder.
	#  @param key_name Name of the key on the IR remote control (e.g. "power", "on", "off", etc.). 
	#  @param carrier_frequency IR carrier frequency in kc/s as float value. Default: 38.0.
	#  @param key_space Delay after a key has been sent or None, if no key_space is required. Default: 0.1 seconds.
	#  @param no_repeat Do not send the repetitions. Default: False.
	#  @return Result code as element of {0 = SUCCESS; 1 = FAILURE}. 
	def send(self, device_name, key_name, carrier_frequency=38.0, key_space=0.1, no_repeat=False):
		# Find the device
		device_found = None
		for device in self.devices:
			if device['device_name'] == device_name:
				device_found = device
		if not device_found:
			sys.stderr.write(f'ERROR: Device "{device_name}" not found.\n')
			return 1
		# Find the infrared code list for the key
		try:
			keys = device_found['keys']
		except:
			sys.stderr.write(f'ERROR: Command "{key_name}" not found.\n')
			return 1
		if self.verbose:
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
			if not no_repeat:
				for i in range(key['repeat_count']):
					sequences.append(key['repetition_first'])
		elif key_type == 2:
			# Double layer protocol
			status_file_path = os.path.join(self.data_dir, f'.status_{device_name}_{key_name}.json') 
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
				if not no_repeat:
					for i in range(key['repeat_count']):
						sequences.append(key['repetition_first'])
				timeout = now + datetime.timedelta(seconds=key['timeout_space'])
				timeout_str = timeout.strftime('%Y-%m-%d %H:%M:%S')
				key_status = {'timeout': timeout_str}
			else:
				sequences.append(key['next'])
				if not no_repeat:
					for i in range(key['repeat_count']):
						sequences.append(key['repetition_next'])
				key_status = None
		else:
			sys.stderr.write(f'ERROR: Unknown protocol type "{key_type}".\n')
			return 1
		if self.verbose: sys.stdout.write('Sending ...\n')
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
						wf = self.carrier(self.gpio, carrier_frequency, ci)
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
		if self.verbose: sys.stdout.write('... sent.\n')
		# After the IR signal has been sent 
		if key_type == 2:
			# Double layer protocol
			if key_status == None:
				# Delete the status file
				if os.path.isfile(status_file_path):
					try:
						os.remove(status_file_path)
					except:
						sys.stderr.write(f'ERROR: Cannot remove the status file "{status_file_path}".\n')
						return 13
			else:
				# Save the status file
				try:
					f = open(status_file_path, "w")
					try:
						json.dump(key_status, f, indent='\t')
					except:
						sys.stderr.write(f'ERROR: Cannot JSON encode and save the status to file "{status_file_path}".\n')
						f.close()
						return 1
					f.close()
				except:
					sys.stderr.write(f'ERROR: Cannot open file "{status_file_path}" to write.\n')
					return 13
		# Done
		sys.stdout.write(f'The IR signal for key {key_name} has been successfully sent.\n')
		# Space between the IR signals to following IR signals
		if key_space != None:
			time.sleep(key_space)
		# Everything is fine
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
	
