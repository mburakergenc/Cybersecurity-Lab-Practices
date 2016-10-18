import os
import nmap

host = raw_input("Provide the ip range to scan: ")
filedir = raw_input("Enter the folder name: ")
filename = raw_input("Enter the file name: ")

try:
    os.mkdir(filedir, 0777)
except OSError:
    pass
while os.path.exists("%s/%s" % (filedir, filename)):
    selection = raw_input("The file already exists. Do you want to override it?: y-n: ")
    if selection.lower() == 'y': # Could use .casefold() in python 3
        os.remove("%s/%s" % (filedir, filename))
        break
    else:
        filename = raw_input("Enter the file name: ")

Nscanner = nmap.PortScanner()
Nscanner.scan(hosts=host, arguments="-open -Pn -p 1-65535 -T4 -oN %s/scanresults.nmap" % filedir)
print ('------------------ Open Ports ------------------------------')
os.system("cat %s/scanresults.nmap | grep tcp | cut -d'/' -f1 | sort | uniq" % filedir)
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
