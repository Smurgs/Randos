import os
import socket
import time
import sys

# Get python version number
ver = sys.version_info[0]

# Get own IP address
if ver >= 3:
	ip_addr = input("Enter your IP address: ")
else:
	ip_addr = raw_input("Enter your IP address: ")
	
ip_addr = ip_addr.split('.')
ip_addr = [int(i) for i in ip_addr]

# Turn ip_addr into sum and bits
count = 3
ip_num = 0
for octet in ip_addr:
	ip_num += octet*(256**count)
	count -= 1
ip_bit = bin(ip_num)[2:]


# Get netmask 
if ver >= 3:
	netmask = input("Enter the netmask: ")
else:
	netmask = raw_input("Enter the netmask: ")
# If input is hex
if '0x' in netmask:
	netmask = int(netmask, 16)
	mask_bit = bin(netmask)[2:]
# Else if input is octet notation
else:
	netmask = netmask.split('.')
	netmask = [int(i) for i in netmask]

	# Turn netmask into sum and bits
	count = 3
	mask_num = 0
	for octet in netmask:
		mask_num += octet*(256**count)
		count -= 1
	mask_bit = bin(mask_num)[2:]


#Find min and max ip addr
min_bit = ''
max_bit = ''
count = 0
for char in mask_bit:
	if char == '1':
		max_bit = max_bit + ip_bit[count]
		min_bit = min_bit + ip_bit[count]
	elif count == len(mask_bit)-1:
		max_bit = max_bit + '0'
		min_bit = min_bit + '1'
	else:
		max_bit = max_bit + '1'
		min_bit = min_bit + '0'
	
	count += 1

# Seperate octets
min_sep = [min_bit[i:i+8] for i in range(0, len(min_bit), 8)]
max_sep = [max_bit[i:i+8] for i in range(0, len(max_bit), 8)]

# Convert binary octets to base 10
min_num = []
max_num = []
for octet in min_sep:
	min_num.append(int(octet, 2))

for octet in max_sep:
	max_num.append(int(octet, 2))

# Find difference in min/max to loop through each possible ip
first = range(min_num[0], max_num[0]+1)
second = range(min_num[1], max_num[1]+1)
third = range(min_num[2], max_num[2]+1)
fourth = range(min_num[3], max_num[3]+1)


print ("The smallest IP address on subdomain is: " + \
       str(min_num[0]) + "."+str(min_num[1]) + "." + \
       str(min_num[2]) + "." + str(min_num[3]))

print ("The largest IP address on subdomain is: " + \
       str(max_num[0]) + "."+str(max_num[1]) + "." + \
       str(max_num[2]) + "." + str(max_num[3]))

live_hosts = []
# Ping all ip addresses
for w in first:
	for x in second:
		for y in third:
			print ("Pinging range: "+str(w)+"."+str(x)+"."+str(y)+".x")
			for z in fourth:
				ip = str(w)+"."+str(x)+"."+str(y)+"."+str(z)
				program_output = os.popen('ping -c 1 ' + ip)
				time.sleep(0.01)
				
				

print ("Finished pinging all ip addresses")
print ("Cross checking with arp table")
time.sleep(2)

program_output = os.popen('arp -a')

for line in program_output:
    if 'incomplete' not in line:
        b = line.split()[:4]
        print (b[0]+" "+b[1]+" "+b[2]+" "+b[3])