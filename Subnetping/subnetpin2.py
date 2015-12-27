import os
import socket

ip_arp = {}
bcast_addr = socket.INADDR_BROADCAST

print ("Pinging broadcast address...")
ping_res = os.popen('ping -c 5 ' + str(bcast_addr) +'|grep \'bytes from\'|awk \'{print $4}\'|cut -d: -f1|sort -u')
for line in ping_res:
    ip_arp[line.strip()] = ''
    arp = os.popen('arp ' + line.strip())
    for x in arp:
        ip_arp[line.strip()] = x.split()
    
print ("IP Address - Host Name - MAC Address")
for key in ip_arp.keys():
    print (key + "\t" + ip_arp[key][0] + "\t" + ip_arp[key][3])
    
print (str(len(ip_arp)) + " hosts replied to ping")
