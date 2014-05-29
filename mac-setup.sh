#!/usr/local/bin/python2.7
print "Add new Test bed entries to mac file"
hostname = raw_input("Enter hostname: ")
mac_addr = raw_input("Enter MAC Address: ")
ip_addr = raw_input("Enter IP ADDRESS: ")
pxe_dir = raw_input("Enter PXE DIRECTORY: ")
location = raw_input("Enter Location of Testbed: ")
fh = open('mac','a')
fh.write('%s\t%s\t%s\t%s\t%s' % (mac_addr,hostname,pxe_dir,location,ip_addr))
fh.close()
