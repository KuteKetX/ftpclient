import os
import sys
import ftplib
from time import sleep

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

def main(host):
	sleep(1)
	FTPServer = ftplib.FTP(host)
	print ""
	print FTPServer.getwelcome()
	print FTPServer.login()
	print ""
	while True:
		FTPInput = str(raw_input('\033[91m[\033[93m' + host + '\033[91m][\033[93m' + FTPServer.pwd() + '\033[91m]::\033[93m$ \033[0m'))
		if FTPInput == "":
			pass
		elif "ls" in FTPInput:
			try:
				Command, Directory = FTPInput.split()
				FTPServer.dir(Directory)
			except ValueError:
				FTPServer.dir()
		elif "cd" in FTPInput:
			Command, Directory = FTPInput.split()
			try:
				FTPServer.cwd(str(Directory))
			except ftplib.error_perm:
				PrintError("That isn't a directory retard.")
		elif "file" in FTPInput:
			Command, File = FTPInput.split(" ")
			print FTPServer.size(File)
		elif FTPInput == "exit":
			FTPServer.quit()
			PrintStatus("Exiting...")
			exit()
		elif FTPInput == "getwelcome":
			print FTPServer.getwelcome()
		elif FTPInput == "clear":
			os.system("clear")
		elif "setdebuglevel" in FTPInput:
			Command, Level = FTPInput.split()
			try:
				FTPServer.set_debuglevel(int(Level))
			except ValueError:
				PrintFailure("Argument must be an integer!")
		elif "retr" in FTPInput:
			Command, Filename = FTPInput.split(" ")
			FTPServer.retrbinary('RETR ' + Filename, open(Filename, 'wb').write)
		else:
			PrintError("\"" + FTPInput + "\": Command Not Found!")

if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except IndexError:
		PrintFailure("Missing argument!")
		PrintStatus("Usage: checkftpserver HOST")
