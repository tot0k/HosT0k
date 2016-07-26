'''
    made by totok (@redtotok)
	project HosT0k - ask me before using my code please.
	made with Twitch-API : https://github.com/justintv/Twitch-API/blob/master/IRC.md
	Thank you to @vambok for his help :)

'''

import socket

HOST = "irc.twitch.tv"
NICK = "bott0k"
PORT = 6667
PASS = "oauth:5if2vwp3jolm2p6isqxdqdvpffxj33"

PATH_STREAMS_LIST = "streamsList.txt"
PATH_HOST = "host.txt"

s = socket.socket()

# Connexion du bot
def connect(s):
	s.connect((HOST, PORT))
	s.send(("PASS " + PASS + "\r\n").encode('utf-8'))
	s.send(("NICK " + NICK + "\r\n").encode('utf-8'))
	return s

# Rejoindre un channel
def joinChannel(s,channel):
	s.send(("JOIN " + channel + "\r\n").encode('utf-8'))
	joinRoom(s,channel)

# Quitter un channel
def leaveChannel(s,channel):
	s.send(("PART " + channel + "\r\n").encode('utf-8'))
	print("*** DISCONNECTED FROM {} ***\n".format(channel))

def joinRoom(s,channel):
	readbuffer = ""
	loading = True

	while loading:
		readbuffer += s.recv(1024).decode('utf-8')
		tempList = readbuffer.split("\n")
		readbuffer = tempList.pop()
		for line in tempList:
			loading = loadingComplete(line,channel)
	print("*** CONNECTED TO {} ***".format(channel))

def loadingComplete(line,channel):
	if("End of /NAMES list" in line):
		return False
	else:
		return True

# Lecture du nom de la chaine à host
def hostName():
	file = open(PATH_HOST,'r')
	host = file.readline()
	file.close()
	return host

# Lecture des chaines sur lesquelles faire le /host
def streamsList():
	file = open(PATH_STREAMS_LIST,'r')
	tab = []
	for line in file:
			tab.append(line[:len(line)-1])
	file.close()
	return tab


connect(s)
host = hostName()

for channel in streamsList():
	channel = "#{}".format(channel)
	joinChannel(s,channel)
	s.send(("PRIVMSG " + channel + " :/host " + host +"\r\n").encode('utf-8)'))	# Envoi de la commande /host
	print("Hosting from {}...".format(channel))
	leaveChannel(s,channel)

