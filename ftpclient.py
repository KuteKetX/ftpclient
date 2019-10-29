import os
import lib
import sys
import socket
import ftplib
import readline
from time import sleep

HistoryFile = os.path.join(os.path.expanduser("~"), ".ftphistory")

def main(Host):
	sleep(1)
	FTPServer = ftplib.FTP(Host)
	print "\n" + FTPServer.getwelcome() + "\n"
	sleep(1)
	LoginStatus = FTPServer.login()
	if "230" in str(LoginStatus):
		lib.PrintSuccess("230 Login Successful.\n")
	if lib.IsIPAddress(Host) == True:
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
				lib.PrintError("That isn't a directory retard.\n")
		elif "file" in FTPInput:
			Command, File = FTPInput.split(" ")
			print FTPServer.size(File)
		elif FTPInput == "exit":
			FTPServer.quit()
			lib.PrintStatus("Exiting...\n")
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
				lib.PrintFailure("Argument must be an integer!\n")
		elif "retr" in FTPInput:
			Command, Filename = FTPInput.split(" ")
			if FTPServer.retrbinary('RETR ' + Filename, open(Filename, 'wb').write) == "226 Transfer complete.":
				PrintSuccess("226 Transfer complete.")
		elif "cat" in FTPInput:
			Command, Filename = FTPInput.split(" ")
			try:
				FTPServer.retrbinary('RETR ' + Filename, lib.ReadFile)
			except ftplib.error_perm:
				lib.PrintFailure("550 Failed to open file.\n")
		else:
			lib.PrintError("\"" + FTPInput + "\": Command Not Found!\n")

if __name__ == '__main__':
	try:
		try:
		    readline.read_history_file(HistoryFile)
		    readline.set_history_length(1000)
		except IOError:
		    pass
		main(sys.argv[1])
	except IndexError:
		lib.PrintFailure("Missing argument!")
		lib.PrintStatus("Usage: checkftpserver HOST")
