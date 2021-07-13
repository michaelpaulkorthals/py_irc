#!/usr/bin/env python3

"""
	IRC Learn.
	A utility to reliably record IR remote control codes on the Raspberry Pi.
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


## IRC Learn.
#  A utility to reliably record IR remote control codes on the Raspberry Pi.
#  Created on 2021-06-30.
#
#  @author Michael Paul Korthals


# Import language libraries

import argparse
import json
import os
import platform
import signal
import sys

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
	import subprocess 
except:
	print('ERROR: Cannot find library "subprocess".\nExecute "pip install subprocess" to setup it.')


## An application class to to suitable record IR remote control codes.
#
class IRCLearningProgram:
	
	## The command line arguments object.
	args = None
	
	## The current subprocess. Default: None.
	p = None
	
	## CONSTRUCTOR.
	#
	def __init__(self):
		# Create argument parser
		parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description="""\
IRC Learn
========= 
Copyright (C) 2021 Michael Paul Korthals.
This program comes with ABSOLUTELY NO WARRANTY; for details 
see <https://www.gnu.org/licenses/>.
This is free software, and you are welcome to redistribute it
under certain conditions; see the GNU General Public License 
for details.

Infrared Remote Control Learning Program
----------------------------------------
This program scans the key presses
of the original IRC hardware and save these
to a JSON data file.

It works on Debian based Linux only with
Python 3.6+ and LIRC-compatible hardware and 
LIRC software installed and correctly configured.

It is also backwards compatible to 
the "irrp.py" JSON files. The key names and codes
of these files will be used in this program.

This program uses the "raw" scan method only, 
but it is enabled to recognize the double layer 
protocol too.

"Double Layer Protocol" means, that the second
key press on the same key has another code than 
the first key press.

This program also recognizes and records the
automatic repetitions of the code sequence, 
when the key is pressed a little bit longer.

Sometimes scanning a key press failed due to
mechanical instability of the original remote
control or other technical root causes. 

In this case you will be required to repeat 
the recording for that key press.

If this will not help, please execute the 
following program to check if you have an 
IR jammer in your room (e.g. open fire, 
light bulbs or other IR sending devices):

$ mode2 -d /dev/lirc1

For testing purposes use the "irc_send.py"
program on Raspberry Pi to send the IR 
commands to your IR controlled devices.

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
1) Learn the complete set of keys for the iiyama monitor prolite tf3238msc.
$ mkdir data
$ ./irc_learn.py --output data/iiyama_monitor_prolite_tf3238msc.json --key_names "off input info on 1 2 3 4 5 6 7 8 9 0 exit menu up left ok right down"

			"""
		)
		# Define the arguments
		parser.add_argument(
			'-as', 
			'--allow_singleshot', 
			help='Allow a single shot key recording.', 
			action='store_true'
		)
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
			help='Start this program in "debug" mode. This parameter must be the last argument in the command line. This feature is only working when connected to the developer workstation in the same LAN segment. ', 
			action='store_true'
		)
		parser.add_argument(
			'-dr', 
			'--dry_run', 
			help='Do a dry run without saving the data to the output file.', 
			action='store_true'
		)
		parser.add_argument(
			'-kn', 
			'--key_names', 
			help='Define the infrared remote control key names. Default: "". If not defined, the program will ask you for the key name and you have to laboriously enter it before each recording.', 
			type=str, 
			default=''
		)
		parser.add_argument(
			'-md',
			'--max_deviation', 
			help='Define the maximum item value difference deviation (useful range between 0.10 and 0.20 as float). Default: 0.15.', 
			type=float, 
			default=0.15
		)
		parser.add_argument(
			'-o', 
			'--output', 
			help='Define the file path to output the JSON file of the infrared remote control. I recommend to use the following name conventions for the files: "<Manufacturer>_<Device_Type>_<Device_Name>.json".', 
			type=str, 
			required=True
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
			'-t', 
			'--timeout', 
			help='Define the timeout after what the IR Signal has been received (in seconds as int). Default: 1.', 
			type=int, 
			default=1
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
			if id_like != 'debian':
				sys.stdout.write(f'ERROR: This program is not tested on Linux distributions like "{id_like}".\nIt is designed for "debian" distributions (e.g raspbian, ubuntu, etc.) only.\n')
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

	## Analyze the output texts, determine the IR signal first key press and 
	#  repeated key press as array of unsigned integers {H-signal, L-signal, ..., H-signal] 
	#  of pulse and space widths in microseconds.
	#  In addition detect the repeat space between the signal repetitions. 
	#
	#  @param output Console output text of the key IR signal recording.
	#  @return A tuple of result as boolean, first as array, repetition as array and repeat_space as integer (microseconds).
	def analyzeOutput(self, output):
		# Divide the console output texts line by line
		# and remove the first 3 rows 
		lines1 = output.split('\n')[3:]
		if self.args.verbose: sys.stdout.write(f'IR recording lines:\n{lines1}\n')
		# Extract the sequence 
		try:
			result, sequence, repetition, repeat_space = self.extractSequence(lines1)
			if not result: raise Exception("Cannot extract sequence.")
		except:
			return False, None, None, 0
		if self.args.verbose: sys.stdout.write(f'Received sequence:\n{sequence}\n')
		if self.args.verbose: sys.stdout.write(f'Repeted sequence:\n{repetition}\n')
		if self.args.verbose: sys.stdout.write(f'Average space between repetitions: {repeat_space} microseonds\n')
		# Return the results
		return True, sequence, repetition, repeat_space
	
	## Checks if the list "s" is sublist of the list "l".
	#
	#  @param l The list where to find.
	#  @param s The sublist to find.
	#  @return A tuple of the result as boolean and the index where "s" has been found in "l".  
	def isSublist(self, l, s):
		result = False
		index = 0
		if s == []:
			result = True
		elif s == l:
			result = True
		elif len(s) > len(l):
			result = False
		else:
			for i in range(len(l)):
				if l[i] == s[0]:
					n = 1
					while (
						n < len(s) 
						and 
						l[i + n] == s[n]
					):
						n += 1
					if n == len(s):
						result = True
						index = i
						break
		return result, index
	
	## Check using fuzzy logic if the list "s" is a similar sublist of the list "l".
	#
	#  @param l The list where to find.
	#  @param s The sublist to find.
	#  @return A tuple of the result as boolean and the index where "s" has been found in "l".  
	def isSimilarSublist(self, l, s):
		result = False
		index = 0
		if s == []:
			result = True
		elif s == l:
			result = True
		elif len(s) > len(l):
			result = False
		else:
			for i in range(len(l)):
				if self.checkDifferenceDeviation(l[i], s[0]):
					n = 1
					while (
						n < len(s) 
						and 
						self.checkDifferenceDeviation(l[i + n], s[n])
					): 
						n += 1
					if n == len(s):
						result = True
						index = i
						break
		return result, index

	## Compare two lists using fuzzy logic.
	#
	#  @param l1 The first list.
	#  @param l2 The second list.
	#  @return The boolean result as element of {True =  list are similar equal, False = list are not equal}.  
	def isSimilarListPair(self, l1, l2):
		result = True
		if len(l1) != len(l2):
			result = False
		else:
			for i in range(len(l1)):
				if not self.checkDifferenceDeviation(l1[i], l2[i]):
					result = False
					break
		return result

	## Analyze the lines and extract the IR sequence data.
	#
	#  @param lines The lines of the console output text.
	#  @return A tuple of result as boolean, first as array, repetition as array and repeat_space as integer (microseconds).
	def extractSequence(self, lines):
		if self.args.verbose: sys.stdout.write(f'Extracting sequence ...\n')
		# Extract the sequences
		sequences = []
		i = 0
		l = len(lines)
		repeat_space_count  = 0
		repeat_space_sum = 0
		# Searching for relevant data
		flag = False
		while i < l:
			inner_sequence = []
			while i < l:
				line = lines[i].strip()
				if line == '': continue
				words = line.split(' ')
				if words[0] in ['pulse', 'space']:
					length = int(words[1])
					if length > 32768:
						sys.stdout.write(f'ERROR: The text line {json.dumps(line)} shows that LIRC/mode2 is not working as expected. Check LIRC configuration. Reboot your system to repair.')
						# Error due to LIRC malfuction
						return False, None, None, 0 
					inner_sequence.append(length)
					i += 1
					# Now we are in the relevant data
					flag = True
				elif words[0] == 'timeout':
					sequences.append(inner_sequence)
					i += 1
					repeat_space_count += 1
					timeout = int(words[1])
					if timeout > 65532:
						sys.stdout.write(f'ERROR: The text line {json.dumps(line)} shows that LIRC/mode2 is not working as expected. Check LIRC configuration. Reboot your system to repair.')
						# Error due to LIRC malfuction
						return False, None, None, 0 
					repeat_space_sum += timeout
					# Now we are in the relevant data
					flag = True
					break
				else:
					if flag:
						sys.stdout.write(f'ERROR: The text line {json.dumps(line)} from "mode2" does not contain the expected key words.\n')
						# Error or protocol deviation
						return False, None, None, 0 
					else:
						# Ignore the first lines, which does not contain relevant data
						i += 1

		# Calculate the average of the spaces between repetitions
		repeat_space = int(round(repeat_space_sum / repeat_space_count))
		# Remove all sequences with length less than 3
		for i in range(len(sequences) - 1, -1, -1): # reverse order
			sequence = sequences[i]
			if len(sequence) < 3:
				del sequences[i]
		# Detect a sequence on a single shot infrared remote control key
		if len(sequences) < 2:
			if len(sequences) == 1 and self.args.allow_singleshot: 
				if self.args.verbose: sys.stdout.write(f'Received single shot sequence: {sequences}\n')
				sequence = self.normalize(sequences[0])
				return True, sequence, None, 0
			else:
				if self.args.verbose: sys.stdout.write(f'ERROR: Too few sequences has been been recorded. This is insufficient for a precise analysis.\n')
				sys.stdout.write(f'ERROR: Too few sequences has been been recorded.\nPress the key down longer (e.g. 1 second).\n')
				return False, None, None, 0
		else:
			if self.args.verbose: sys.stdout.write(f'Received sequences: {sequences}\n')
			# Extract the longest sequence,
			# the short repeat sequence,
			# the longest repetition, 
			# the count how often the longest sequence occurs
			# and the short repeat sequence.
			longest_sequence = []
			longest_count = 0
			longest_repetition = []
			short_repeat_sequence = []
			short_repeat_count = 0
			for sequence in sequences:
				if len(sequence) > len(longest_sequence):
					longest_sequence = sequence
					longest_count = 1
				if longest_count >= 1 and len(sequence) == len(longest_sequence):
					if len(longest_repetition) == 0:
						longest_repetition = sequence
					longest_count += 1
				if len(longest_sequence) > 0 and len(sequence) == 3:
					short_repeat_sequence = sequence
					short_repeat_count += 1
			# Normalize the longest selected sequences in one pass
			longest_sequence, longest_repetition = self.normalizeTwoSequences(longest_sequence, longest_repetition)
			# Detect the protocol and output related data
			if longest_count == 1 and short_repeat_count > 0:
				# Single or double layer with short repetition  
				return True, longest_sequence, short_repeat_sequence, repeat_space
			elif longest_count > 1 and short_repeat_count == 0:
				# Single or double layer with same repetition
				return True, longest_sequence, longest_repetition, repeat_space
			elif longest_count > 1 and short_repeat_count > 0:
				# Single or double layer with same repetition
				return True, longest_sequence, longest_repetition, repeat_space
			else:
				if self.args.verbose: sys.stdout.write(f'ERROR: Unexpected data: longest_count = {longest_count} and short_repeat_count = {short_repeat_count}.\n')
				sys.stdout.write(f'ERROR: Too few sequences.\nPress the key down longer (e.g. 1 second).\n')
				return False, None, None, 0
			
	## Normalize two sequences in one pass.
	#
	#  @param sequence1	The first sequence.	
	#  @param sequence2 The second sequence.
	#  @return Return the two normalized sequences as a tuple.
	def normalizeTwoSequences(self, sequence1, sequence2):
		p1 = 0
		l1 = len(sequence1)
		p2 = p1 + l1
		l2 = len(sequence2)
		joined_sequence = sequence1 + sequence2
		joined_sequence = self.normalize(joined_sequence)
		sequence1 = joined_sequence[p1:p1 + l1]
		sequence2 = joined_sequence[p2:p2 + l2]
		return sequence1, sequence2
		
	## Normalize four sequences in one pass.
	#
	#  @param sequence1	The first sequence.	
	#  @param sequence2 The second sequence.
	#  @param sequence3	The third sequence.	
	#  @param sequence4 The forth sequence.
	#  @return Return the four normalized sequences as a tuple.
	def normalizeFourSequences(self, sequence1, sequence2, sequence3, sequence4):
		p1 = 0
		l1 = len(sequence1)
		p2 = p1 + l1
		l2 = len(sequence2)
		p3 = p2 + l2
		l3 = len(sequence3)
		p4 = p3 + l3
		l4 = len(sequence4)
		joined_sequence = sequence1 + sequence2 + sequence3 + sequence4
		joined_sequence = self.normalize(joined_sequence)
		sequence1 = joined_sequence[p1:p1 + l1]
		sequence2 = joined_sequence[p2:p2 + l2]
		sequence3 = joined_sequence[p3:p3 + l3]
		sequence4 = joined_sequence[p4:p4 + l4]
		return sequence1, sequence2, sequence3, sequence4
			
	## Check using fuzzy logic if the item {pulse; space} selected by item_index has a similar width in all the sequences.
	#  
	#  @param sequences The sequences in analysis.
	#  @param item_index The item index number inside all these sequences.
	#  @result A tuple of result (boolean) and the normalized sequence item value.
	def checkSequenceItem(self, sequences, item_index):			
		normalized_item_value = 0
		for i in range(len(sequences)):
			# Sum the item values
			inner_sequence = sequences[i] 
			normalized_item_value += inner_sequence[item_index]
			if i > 0:
				# Check the similarity
				val1 = sequences[i - 1][item_index]
				val2 = sequences[i][item_index]
				result = self.checkDifferenceDeviation(val1, val2)
				if not result: 
					sys.stdout.write(f'ERROR: Difference deviation for item index {item_index} between {val1} and {val2} is greater than {self.args.max_deviation} (max. deviation).\n')
					return False, [] 
		# Calculate the normalized item value 
		normalized_item_value /= len(sequences)
		normalized_item_value = round(normalized_item_value)
		return True, normalized_item_value
	
	## Use fuzzy logic to check whether the difference deviation is similar or not.
	#  <br>
	#  NOTE: The similarity results from the fact that IR remote controls do not have  
	#  crystal oscillators and their clock frequency is therefore influenced by 
	#  thermal noise, electomagnetic noise, humidity noise, and voltage noise from the energy source.
	#  <br> 
	#  In addition, small firmware bugs that remain undetected in the manufacturer's 
	#  tests can affect the pulse and gap lengths.
	#  <br>
	#  Thus, the pulse and gap widths of the IR signal deviate randomly from the values ​​defined by the manufacturer each time.
	#  
	#  @param val1 The first value.
	#  @param val2 The second value.
	#  @return The result as boolean as element of {True = the pulses or gaps are ~equal; False = the pulses or gaps are ~not equal}. 
	def checkDifferenceDeviation(self, val1, val2):
		return (self.calculateDifferenceDeviation(val1, val2) <= self.args.max_deviation)
		
	## Calculate the deviation of the difference between two values based on the average of both values as a positive float number between 0.0 and 1.0.
	#
	#  @param val1 The first value.
	#  @param val2 The second value.
	#  @return The positive deviation as float.
	def calculateDifferenceDeviation(self, val1, val2):
		# Avoid the "division by zero error" in all possibles cases
		if val1 == 0 and val2 == 0:
			return float(0.0)
		# Ensure a positive deviation float number value based on the average of both values
		if val2 > val1:
			return (float(val2) - float(val1)) / ((float(val1) + float(val2)) / 2.0)
		else:
			return (float(val1) - float(val2)) / ((float(val1) + float(val2)) / 2.0)
		
	## Use fuzzy logic to normalize an IR signal sequence.
	#  See the comments in the code for more details.
	#
	#  @param sequence The list of pulse/gap length values of an IR signal sequence.  	
	#  @return The the normalized sequence.
	def normalize(self, sequence):
		# Forked from souri-t on GitHub by mpk 
		# Original source: https://github.com/souri-t/RemoteControl-RPI/blob/master/remote/bin/irrp
		#
		# by mpk: Code review and adoption to the interfaces of this program and my quality level. 
		# by souri-t a by mpk: Reviewed explanation:
		"""
		Typically a code will be made up of two or three distinct
		marks (carrier) and spaces (no carrier) of different lengths.
	
		Because of transmission and reception errors those pulses
		which should all be x microseconds long will have a variance 
		around x. See the root causes of this behavior in the Doxygen
		comment lines before the method "checkDifferenceDeviation" 
		of this class.
	
		This function identifies the distinct pulses and takes the
		average of the lengths making up each distinct pulse.
		Marks and spaces are processed separately.
	
		This makes the eventual generation of IR signal sequences 
		by the sender much more accurate.
	
		Input
	
		M    S    M	  S	  M	  S	  M	  S	   M   S    M
		9000 4500 600 540 620 560 590 1660 620 1690 615
	
		Distinct marks
	
		9000                average 9000
		600 620 590 620 615 average  609
	
		Distinct spaces
	
		4500                average 4500
		540 560             average  550
		1660 1690           average 1675
	
		Output
	
		M    S    M	  S   M	  S	  M	  S	   M   S    M
		9000 4500 609 550 609 550 609 1675 609 1675 609
		"""
		# mpk: Calculate the min. and max. tolerance values by argument of this program 
		toler_min = float(1.0) - self.args.max_deviation 
		toler_max = float(1.0) + self.args.max_deviation
		# Verbosely output the sequence before changes
		if self.args.verbose:
			print(f"Sequence before normalizing:\n{sequence}\n\n")
		# Change the sequence
		entries = len(sequence)
		p = [0] * entries # Set all entries not processed
		for i in range(entries):
			if not p[i]: # Not processed?
				v = sequence[i]
				tot = v
				similar = 1.0
				# Find all pulses with similar lengths to the start pulse
				for j in range(i + 2, entries, 2):
					if not p[j]: # Unprocessed
						if (sequence[j] * toler_min) < v < (sequence[j] * toler_max): # Similar
							tot = tot + sequence[j]
							similar += 1.0
				# Calculate the average pulse length
				newv = round(tot / similar, 2)
				sequence[i] = int(round(newv)) # mpk: Integer values needed in this program
				# Set all similar pulses to the average value
				for j in range(i + 2, entries, 2):
					if not p[j]: # Unprocessed.
						if (sequence[j] * toler_min) < v < (sequence[j] * toler_max): # Similar
							sequence[j] = int(round(newv)) # mpk: Integer values needed in this program
							p[j] = 1
		# Verbosely output the sequence after changes
		if self.args.verbose:
			print(f"Sequence after normalizing:\n{sequence}\n\n")
		# Return the changed sequence
		return sequence

	## Do what to do, when the hanger hangs after receiving the IR signal.
	#
	# @param signum Unused.
	# @param frame Unused.
	def _hanger_sigalrm_handler(self, signum, frame): #@UnusedVariable
		# Kill the LIRC mode2 process
		self.p.kill()
		# Raise a runtime error to leave the receiver endless loop
		raise RuntimeError('Timeout')
	
	## Receive an IR signal using the tool LIRC mode2.
	#
	#  @return The console text output from LIRC mode2.
	def receiveIRSignal(self):
		output = ''
		# Record the data from Infrared Remote Control using "LIRC mode2"
		command = f'mode2 -d {self.args.device}'
		self.p = subprocess.Popen(command, shell=True, bufsize=0, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf8')
		# ALARM: Define callback handler to detect, when IR signal has finished
		signal.signal(signal.SIGALRM, self._hanger_sigalrm_handler) #@UndefinedVariable
		# ALARM: Wait for no output after the IR signal has been received. Not before.
		count = 10
		receiving = False
		# The receiver endless loop
		while True:
			try: 
				# ALARM: Start observing the "hanger"
				if receiving: signal.alarm(self.args.timeout) #@UndefinedVariable
				# Read a single line from console output
				# ALARM: Execute the "hanger"
				line = self.p.stdout.readline()
				# ALARM: Stop observing the "hanger"
				signal.alarm(0) #@UndefinedVariable
				# Add the line to the output
				output += line 
				# ALARM: Divert the possibilities
				count -= 1
				if (not receiving) and count <= 0:
					receiving = True
			except KeyboardInterrupt:
				sys.stdout.write(f'\nThe program has been canceled by the user.\n\n')
				sys.exit(125) # 125 = operation canceled
			except RuntimeError:
				# IR data received
				break
		return output.strip()
	
	## Record and verify the IR signal from the remote control.
	#
	#  @param key_name The name of the key on the infrared remote control.
	#  @result The IR signal data for that key as a dictionary. 
	def recordKey(self, key_name):
		sys.stdout.write('\n')
		while True:
			key_dict = {}
			# PASS 1:
			sys.stdout.write(f'Press the "{key_name}" key for the first time ...\n')
			output = self.receiveIRSignal()
			if self.args.verbose: sys.stdout.write(f'FIRST RECORD:\n{output}\n\n')
			# Perform the analysis
			result, sequence1, repetition1, repeat_space1 = self.analyzeOutput(output)
			if not result:
				if self.args.verbose: sys.stdout.write('ERROR: The output analysis failed at first recording.\n')
				sys.stdout.write(f'ERROR: The recording for key "{key_name}" failed at first recording. Try again.\n\n')
				# Try again. Repeat the recording for this key.
				continue
			if repetition1 == None and repeat_space1 == 0:
				# Single Layer single shot protocol
				key_dict = { 
					'type': 0,
					'first': sequence1, 
					'next': None, 
					'repetition_first': sequence1,
					'repetition_next': None, 
					'repeat_count': self.args.repeat_count, 
					'repeat_space': self.args.repeat_space, 
					'timeout_space': self.args.timeout_space 
				}
				sys.stdout.write(f'The recording for key "{key_name}" succeeded.\n\n')
				return key_dict
			# PASS 2:
			sys.stdout.write(f'Press the key "{key_name}" a second time ...\n')
			output = self.receiveIRSignal()
			if self.args.verbose: sys.stdout.write(f'SECOND RECORD:\n{output}\n\n')
			# Perform the analysis
			result, sequence2, repetition2, repeat_space2 = self.analyzeOutput(output) #@UnusedVariable
			if not result:
				if self.args.verbose: sys.stdout.write('ERROR: The output analysis failed at second recording.\n')
				sys.stdout.write(f'ERROR: The recording for key "{key_name}" failed at second recording. Try again.\n\n')
				# Try again. Repeat the recording for this key.
				continue
			# Normalize the two sequences
			sequence1, sequence2 = self.normalizeTwoSequences(sequence1, sequence2)
			if self.isSimilarListPair(sequence1, sequence2):
				# Single layer protocol detected
				key_dict = { 
					'type': 1,
					'first': sequence1, 
					'next': None, 
					'repetition_first': repetition1,
					'repetition_next': None,
					'repeat_count': self.args.repeat_count, 
					'repeat_space': repeat_space1, 
					'timeout_space': self.args.timeout_space 
				}		
			else:
				# Double layer protocol detected
				sys.stdout.write(f'\nDouble layer protocol detected for the key "{key_name}".\nYou need to do 2 further key presses.\n\n')
				# PASS 3:
				sys.stdout.write(f'Press the key "{key_name}" a third time ...\n')
				output = self.receiveIRSignal()
				if self.args.verbose: sys.stdout.write(f'THIRD RECORD:\n{output}\n\n')
				# Perform the analysis
				result, sequence3, repetition3, repeat_space3 = self.analyzeOutput(output) #@UnusedVariable
				if not result:
					if self.args.verbose: sys.stdout.write('ERROR: The output analysis failed at third recording.\n')
					sys.stdout.write(f'ERROR: The recording for key "{key_name}" failed at the third recording. Try again.\n\n')
					# Try again. Repeat the recording for this key.
					continue
				# PASS 4:
				sys.stdout.write(f'Press the key "{key_name}" a forth time ...\n')
				output = self.receiveIRSignal()
				if self.args.verbose: sys.stdout.write(f'FOURTH RECORD:\n{output}\n\n')
				# Perform the analysis
				result, sequence4, repetition4, repeat_space4 = self.analyzeOutput(output) #@UnusedVariable
				if not result:
					if self.args.verbose: sys.stdout.write('ERROR: The output analysis failed at fourth recording.\n')
					sys.stdout.write(f'ERROR: The recording for key "{key_name}" failed at fourth recording. Try again.\n\n')
					# Try again. Repeat the recording for this key.
					continue
				# Check if the sequence of the first key press 
				# is similar to 
				# the sequence of the sequence if the third key press.
				# And check if the sequence of the second key press 
				# is similar to 
				# the sequence of the sequence if the forth key press.
				sequence1, sequence2, sequence3, sequence4 = self.normalizeFourSequences(sequence1, sequence2, sequence3, sequence4)
				if self.isSimilarListPair(sequence1, sequence3) and self.isSimilarListPair(sequence2, sequence4):
					repetition1, repetition2 = self.normalizeTwoSequences(repetition1, repetition2)
					key_dict = {
						'type': 2, 
						'first': sequence1, 
						'next': sequence2, 
						'repetition_first': repetition1,
						'repetition_next': repetition2, 
						'repeat_count': self.args.repeat_count, 
						'repeat_space': repeat_space1, 
						'timeout_space': self.args.timeout_space 
					}
				else:
					# If it is not, we have an unknown protocol or technical disturbance here.
					if self.args.verbose: sys.stdout.write('ERROR: Contrary to expectations, the quantities of the recording sequences {1; 3} and {2; 4} do not contain any similar elements.\n')
					sys.stdout.write(f'ERROR: Technical malfunction occurred for key "{key_name}" or an unknown protocol could have been detected. Try again.\n\n')
					# Try again. Repeat the recording for this key.
					continue
			sys.stdout.write(f'The recording for key "{key_name}" succeeded.\n\n')
			# Finish the recording for this key
			return key_dict
			
	## Run the object.
	#
	def run(self):
		# Output the program information
		sys.stdout.write('INFRARED REMOTE CONTROL LEARNING PROGRAM\n')
		sys.stdout.write('Version 1.0\n')
		sys.stdout.write('by mpk\n\n')
		sys.stdout.write('Press Ctrl-C to cancel this program.\n\n')
		# Display the name of the infrared remote control
		irc_name = os.path.basename(self.args.output)[0:(len(self.args.output.split('.')[-1]) + 1)*(-1)]
		sys.stdout.write(f'Name of controlled device: {irc_name}\n\n')
		# Display output-related information
		sys.stdout.write(f'Output file: {self.args.output}\n')
		# Receive the IR signal data
		if os.path.isfile(self.args.output):
			# Load existing output file as text 
			# Backwards compatible to files generated by the simple "irrp.py"
			with open(self.args.output, 'r') as text_file:
				text = text_file.read()	
			keys = json.loads(text)
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
			if self.args.verbose:
				text = json.dumps(keys, indent="\t", sort_keys=True) 
				sys.stdout.write(f'Current content: \n{text}\n\n')
			text1 = ' '.join(key_names)
			sys.stdout.write(f'Currently existing keys: \n{text1}\n\n')
		else: 
			keys = {}
			sys.stdout.write(f'The data for the infrared remote control "{irc_name}" will be created from scratch.\n')
		if self.args.key_names != '':
			# Use key names from command line argument "--key_names"
			key_names = [word.lower() for word in self.args.key_names.split()]
			key_names.sort()
			text2 = ' '.join(key_names)
			sys.stdout.write(f'Keys to create/update: \n{text2}\n\n')
			for key_name in key_names:
				data = self.recordKey(key_name)
				keys[key_name] = data
		else:
			# Enter the key names manually
			while True:
				try:
					sys.stdout.write('\nEnter the key name: ')
					key_name = input().strip().replace(' ', '_')
				except KeyboardInterrupt:
					sys.stdout.write(f'\nThe program has been canceled by the user.\n\n')
					return 125 # 125 = operation canceled
				if key_name == '': break
				data = self.recordKey(key_name)
				keys[key_name] = data
		# Save the keys data of the infrared remote control to the output file
		text = json.dumps(keys, indent="\t", sort_keys=True)
		if self.args.dry_run:
			sys.stdout.write(f'\nThe new output content could be:\n{text}\n\n')
			sys.stdout.write(f'The dry run of the program has succeeded.\n\n')
		else:
			with open(self.args.output, "w") as text_file:
				text_file.write(f'{text}\n')
			if self.args.verbose:
				# Output the content of that file as text to console
				sys.stdout.write(f'\nCurrent output content:\n{text}\n\n')
				sys.stdout.write(f'The program has been successfully completed.\n\n')
			else:
				sys.stdout.write(f'The program has been successfully completed.\n\n')
				sys.stdout.write(f'Execute to inspect the data:\n$ nano -v "{self.args.output}"\n\n')
		return 0

# MAIN PROGRAM
# Create the class object
irclp = IRCLearningProgram() 
# Run the main program
sys.exit(irclp.run())
		