import os
import sys
import socket
import ftplib
import readline
from time import sleep

HistoryFile = os.path.join(os.path.expanduser("~"), ".ftphistory")

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

def AddHistory(Command):
	readline.add_history(str(Command))

def main(Host):
	sleep(1)
	FTPServer = ftplib.FTP(Host)
	print "\n" + FTPServer.getwelcome() + "\n"
	sleep(1)
	LoginStatus = FTPServer.login()
	if "230 Login Successful." in str(LoginStatus):
		PrintSuccess("230 Login Successful.\n")
	if IsIPAddress(Host) == True:
		HostPrompt = socket.getfqdn(Host)
	else:
		HostPrompt = Host
	while True:
		FTPInput = str(raw_input('\033[91m[\033[93m' + HostPrompt + '\033[91m][\033[93m' + FTPServer.pwd() + '\033[91m]::\033[93m$ \033[0m'))
		if FTPInput == "":
			pass
		elif "ls" in FTPInput:
			try:
				Command, Directory = FTPInput.split()
				FTPServer.dir(Directory)
				print ""
			except ValueError:
				FTPServer.dir()
				print ""
		elif "cd" in FTPInput:
			Command, Directory = FTPInput.split()
			try:
				FTPServer.cwd(str(Directory))
			except ftplib.error_perm:
				PrintError("That isn't a directory retard.\n")
		elif "file" in FTPInput:
			Command, File = FTPInput.split(" ")
			print FTPServer.size(File)
		elif FTPInput == "exit":
			FTPServer.quit()
			PrintStatus("Exiting...\n")
			exit()
		elif FTPInput == "getwelcome":
			print "\n" + FTPServer.getwelcome() + "\n"
		elif FTPInput == "clear":
			os.system("clear")
		elif "setdebuglevel" in FTPInput:
			Command, Level = FTPInput.split()
			try:
				FTPServer.set_debuglevel(int(Level))
			except ValueError:
				PrintFailure("Argument must be an integer!\n")
		elif "retr" in FTPInput:
			Command, Filename = FTPInput.split(" ")
			if FTPServer.retrbinary('RETR ' + Filename, open(Filename, 'wb').write) == "226 Transfer complete.":
				PrintSuccess("226 Transfer complete.")
		elif "cat" in FTPInput:
			Command, Filename = FTPInput.split(" ")
			try:
				FTPServer.retrbinary('RETR ' + Filename, ReadFile)
			except ftplib.error_perm:
				PrintFailure("550 Failed to open file.\n")
		else:
			PrintError("\"" + FTPInput + "\": Command Not Found!\n")

if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except IndexError:
		PrintFailure("Missing argument!")
		PrintStatus("Usage: checkftpserver HOST")
