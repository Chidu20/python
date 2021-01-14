#!/usr/bin/python
###############################################################################################
##### THIS SCRIPT ACCEPTS CIDR BLOCK AND CREATES A DICTIONARY                             #####
##### WITH THE FOLLOWING METRICS                                                          #####
##### 1. NETWORK MASK                                                                     #####
##### 2. NETWORK ADDRESS                                                                  #####
##### 3. FIRST IP                                                                         #####
##### 4. LAST IP                                                                          #####
##### 5. BROADCAST IP                                                                     #####
##### 6. Number of IP Addresses                                                           #####
###############################################################################################

import sys

###############################################################################################
##### Function to print error usage and example                                           #####
###############################################################################################

def printError():
    error = "Error\t: Enter a valid CIDR block value"
    usage = "Usage\t: " + sys.argv[0] + " IP/Mask"
    example = "Example\t: " + sys.argv[0] + " 192.168.22.5/20"
    print (error+"\n"+usage+"\n"+example)
    exit()

###############################################################################################
##### Function to validate the given IP address                                           #####
###############################################################################################

def checkIP(ip):
    try:
        val = [int(i) for i in ip.split('.')]
    except ValueError:
        printError()
    if len(val) != 4:
        printError()
    for v in val:
        if v > 255:
            printError()
    else:
        return val

###############################################################################################
##### Function to seperate IP and mask values from CIDR                                   #####
###############################################################################################

def getIpMask(val):
    try:
        ip = val.split('/')[0]
        mask = int(val.split('/')[1])
    except ValueError:
        printError()
    if mask > 32 or mask < 0:
        printError()
    return ip,mask

###############################################################################################
##### Function to convert a decimal value to binary                                       #####
###############################################################################################

def binary(n):
    s           = ""
    while n > 0:
        r       = int(n%2)
        n       = int(n/2)
        s       = s + str(r)
    return s[::-1].rjust(8,'0')

###############################################################################################
##### Function to generate a binary IP address with 4 bytes                               #####
###############################################################################################

def ipBinary(ip):
    val      = ""
    oct      = checkIP(ip)
    for o in oct:
        val  = val + '.' + binary(o)
    return val.lstrip('.')

###############################################################################################
##### Function to convert a binary value to decimal                                       #####
###############################################################################################

def decimal(b):
    b       = str(b[::-1])
    s       = 0
    for i in range(0,len(b)):
        s   = s + int(b[i]) * 2**i
    return s

###############################################################################################
##### Function to generate a decimal IP address with 4 fields                             #####
###############################################################################################

def ipDecimal(ip):
    val     = ""
    for o in ip.split('.'):
        val = val +'.' + str(decimal(o))
    return val.lstrip('.')

###############################################################################################
##### Function to create IP address with required octets                                  #####
###############################################################################################

def createIP(ip):
    ipList  = list(ip)
    for i in range(1,len(ipList)):
        if i%8 == 0:
            ipList[i] = '.' + ipList[i]
    return ''.join(ipList)

###############################################################################################
##### Function to find the number of hosts in the given network                           #####
###############################################################################################

def numAdd(m):
    return str(2**(32-m))

###############################################################################################
##### Function to create a dictionary mapping the attributes to corresponding values      #####
###############################################################################################

def createIpDict(statList):
    defKey = ['CIDR','Network Mask','Network Address','First IP','Last IP', 'Broadcast Address','No. of Addresses']
    ipDict = {}
    for key,val in zip(defKey,statList):
        if len(val) == 32:
            ip      = createIP(val)
            decIP   = ipDecimal(ip)
        else:
            decIP   = val
        ipDict[key] = decIP
    return ipDict

###############################################################################################
##### Function to find the revelant metrics of the IP                                     #####
###############################################################################################

def createIpStats(cidrVal):
    ip,m            = getIpMask(cidrVal)
##### Convert the IP into binary Octets
    binIP           = ipBinary(ip)
##### Calculate the number of addresses
    nh              = numAdd(m)
##### Calculate the network mask using the reference mask as all 1's
    defMask         = ''.join(['1' for i in range(0,32)])
    newMask         = defMask[:m:]+defMask[m::].replace('1','0')
##### Calculate the network address by adding 0's to binary IP after the mask value
    rawIP           = binIP.replace('.','')
    netAdd          = rawIP[:m:].ljust(32,'0')
##### Calculate the broadcast address by replacing 1's to binary IP after the mask value
    broadCastIP     = netAdd[:m:].ljust(32,'1')
##### Calculate the first IP by adding 1 at the end of binary network mask
    firstIP         = netAdd[:len(rawIP)-1:]+'1'
##### Calculate the Last IP by replacing the last bit of broadcast IP to 0
    lastIP          = broadCastIP[:len(broadCastIP)-1:]+'0'
##### Create a list of calculated values
    ipStatList      = [cidrVal,newMask,netAdd,firstIP,lastIP,broadCastIP,nh]
##### Map the values to attributes and create a dictionary
    ipDict          = createIpDict(ipStatList)
    return ipDict

###############################################################################################
##### Print the values in desired format                                                  #####
###############################################################################################

def printVal(cidr):
    ipDict = createIpStats(cidr)
    for key in ipDict.keys():
        print ("%-20s :%s" %(key,ipDict[key]))

###############################################################################################
##### Main function starts here                                                           #####
###############################################################################################

if __name__ == '__main__':
    try:
        printVal(sys.argv[1])
    except IndexError:
        printError()