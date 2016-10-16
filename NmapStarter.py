import os
import nmap

host = raw_input("Provide the ip range to scan: ")
filedir = raw_input("Enter the folder name: ")
filename = raw_input("Enter the file name: ")

try:
    original_umask = os.umask(0)
    os.mkdir(filedir, 0777)
    os.umask(original_umask)
except OSError:
    pass
while os.path.exists("%s/%s" % (filedir, filename)):
    selection = raw_input("The file already exists. Do you want to override it? y-n")
    if selection == 'y':
        os.remove("%s/%s" % (filedir, filename))
        break
    else:
        filename = raw_input("Enter the file name: ")

Nscanner = nmap.PortScanner()
Nscanner.scan(hosts=host, arguments="-open -n -T4 -oN %s/nmapformat.txt" % filedir)
# create the list for the live IPs
# the value x is echange for the value in the list in the library in all_hosts
# pentes.all_hosts() is a function to list all the hosts scanned
hostsList = [(x, Nscanner[x]['status']['state']) for x in Nscanner.all_hosts()]

print ('-------------------- Live Hosts -----------------------------')
# print Nscanner.get_nmap_last_output() can be used for xml type output
for host, status in hostsList: # loop through all the hosts
    if 'up' in status: #check to see if the host is up
        print('{0}:{1}'.format(host, status))
        fileHandler = open(filedir + "/" + filename, 'a') #create a file with live ips
        fileHandler.write('{0}'.format(host) + '\n')

print ('Your file %s is saved in %s' % (filename, filedir))
