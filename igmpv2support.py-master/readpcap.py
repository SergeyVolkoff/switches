from scapy.all import *
import datetime


def readpcap(file, re, field):
    pcap = rdpcap(file)
    n = 0
    packets = []
    for i in range(len(pcap)):
        n = i + 1
        try:
            if re in str(pcap[i].getfieldval(field)):                
                pckt_show = pcap[i].show(dump=True)
                packets.append((str(n), str(datetime.datetime.fromtimestamp(int(pcap[i].time))), pckt_show))          
        except Exception as err:
            print(err)
            continue    
    return packets