#!/usr/local/bin/python

network='irc.yelpcorp.com'
port=6697
bufsize = 2**11 # unrealIRCd seems to use 2k buffers

import os
user = os.environ['LOGNAME']

import sys
message = ' '.join(sys.argv[1:])
if not message:
	message = "it's done!"

import socket, ssl
irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
irc = ssl.wrap_socket(irc)
irc.connect( (network, port) )
irc.send( 'PASS regulat0rz\r\n' )
irc.send( 'NICK %s-bot\r\n' % user )
irc.send( 'USER %(user)s-bot %(user)s-bot %(user)s-bot :%(user)s\'s Python bot\r\n' % dict(user=user))

data = True
while data:
	data = irc.recv(bufsize)
	#sys.stdout.write(data)
	if data.startswith( 'PING' ):
		msg = 'PONG ' + data.split() [ 1 ] + '\r\n'
		irc.send( msg )
		irc.send( 'PART #yelp\r\n' )
		irc.send( 'PRIVMSG %s :%s\r\n' % (user, message) )
		break
data = irc.recv(bufsize)
#sys.stdout.write(data)

