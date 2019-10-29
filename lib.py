import os
import socket

def PrintSuccess(Msg):
	if os.name == 'nt':
		print '[+] ' + Msg
	else:
		print '\033[1;32m[+]\033[1;m ' + Msg

def PrintStatus(Msg):
	if os.name == 'nt':
		print '[*] ' + Msg
	else:
		print '\033[1;34m[*]\033[1;m ' + Msg

def PrintFailure(Msg):
	if os.name == 'nt':
		print '[-] ' + Msg
	else:
		print '\033[1;31m[-]\033[1;m ' + Msg

def PrintError(Msg):
	if os.name == 'nt':
		print '[!] ' + Msg
	else:
		print '\033[1;31m[!]\033[1;m ' + Msg

def IsValidIP(Address):
	AddrChunks = Address.split('.')
	if len(AddrChunks) != 4:
		return False
	for AddrChunk in AddrChunks:
		if not AddrChunk.isdigit():
			return False
		Range = int(AddrChunk)
		if Range < 0 or Range > 255:
			return False
	return True

def IsIPAddress(String):
	try:
	    socket.inet_aton(String)
	    return True
	except socket.error:
	    return False

def ReadFile(File):
	print File
