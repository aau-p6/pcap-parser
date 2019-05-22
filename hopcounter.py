#!/usr/bin/env python

import os
import pcapy
from struct import*
import threading
from threading import Thread, Lock
import math
MaxThreads = 20
mutex=Lock()

def HopsBehandler(Protocol):
    for test_typer_count in os.walk("%s" % (Protocol)).next()[1]:
        Hops = []
        HopsVariance = 0
        Hopsum = 0
        print ("Now checking %s/%s"%(Protocol,test_typer_count))
        if os.path.isfile("%s/%s/hops.txt"%(Protocol,test_typer_count)):
            readfile = open("%s/%s/hops.txt"%(Protocol,test_typer_count),'r')
            for line in readfile:
                line = line.rstrip()
                Hops.append(line)
            
            for entry in Hops:
                Hopsum = Hopsum + float(entry)
            AverageHops = Hopsum/len(Hops)
            for entry in Hops:
                HopsVariance = (((float(entry)) - AverageHops) * ((float(entry)) - AverageHops)) + HopsVariance
                #print HopsVariance
            HopsVariance = HopsVariance/len(Hops)
            HopsStandardDeviation = math.sqrt(HopsVariance)
            Hops_Confidence_left = round(AverageHops - (1.96 * HopsStandardDeviation/math.sqrt(len(Hops))),3 )
            Hops_Confidence_right =round(AverageHops + (1.96 * HopsStandardDeviation/math.sqrt(len(Hops))),3 )
            print Hops_Confidence_left
            print Hops_Confidence_right
            mutex.acquire()
            try:
                f=open("Histogramdata/Intervaller/Averagehops.txt",'a')
                f.write("%s,"%AverageHops)
                f.close()
            finally:
                mutex.release()
                
            mutex.acquire()
            try:
                f=open("Histogramdata/Intervaller/Confidenceinterval_Hops_left.txt",'a')
                f.write("%s,"%Hops_Confidence_left)
                f.close()
            finally:
                mutex.release()
                
            mutex.acquire()
            try:
                f=open("Histogramdata/Intervaller/Confidenceinterval_Hops_right.txt",'a')
                f.write("%s,"%Hops_Confidence_right)
                f.close()
            finally:
                mutex.release()
        
def hopcount(Protocol,statistic_test_count):
#Receive a testype directory to go through
                #Go through each test and calculate average hops for these
                
                    #print statistic_test_count
                    path = Protocol + "/" + statistic_test_count
                    reader = pcapy.open_offline("%s/wifi-simple-adhoc-0-0.pcap" % path)
                    Lenght = os.popen('tshark -r %s/wifi-simple-adhoc-0-0.pcap | wc -l' %path).read()
                    PcapLenght = int(Lenght)
                    i = 0
                    Samlethops = 0
                    Averagehopsprsim = 0
                    Averagehops = 0
                    for x in range(0, PcapLenght):
                        (header, payload) = reader.next();
                        #payload size is between 100 and 110 for the UDP packets from what i have seen
                        if len(payload)>100 and len(payload)<110 :
                            #Strange string is the format that the payload should be read into
                            #56:76 is where the IPv4 packet starts and ends where a total of 9 fields are created
                            ipheader=unpack('!BBHHHBBHII',payload[56:76])
                            #167837956 does not exist in packets we want
                            if ipheader[8] !="167837956":
                            #167837953 seems to be some sort of identification for node 1 or gateway
                                if ipheader[9] ==167837953:
                                    i = i+1
                            #Field 5 is the Ttl that is wanted. Where a Ttl of 64 is default and if this is read in the file it means 1 hop was taken
                                    Samlethops = Samlethops + (65-ipheader[5])
                    #should only execute this code if there was any udp packets to be read, where i is the number of udp packets read
                    if i > 0:
                        Averagehops = Samlethops*1.0/i
                        #print round(Averagehops,2)
                        mutex.acquire()
                        try:
                            f = open("%s/hops.txt"%Protocol,'a')
                            f.write("%f\n"%Averagehops)
                            f.close()
                        finally:
                            mutex.release()
                    #print Samlethops
                    #print Averagehops
                    #print "%d\n"%i

def main():
    #for Protocol in Protocols:
                Protocol = "OLSR"
                for test_typer_count in os.walk("%s" % (Protocol)).next()[1]:
                    os.popen("rm -r %s/%s/hops.txt"%(Protocol,test_typer_count))
                    print "Ny test type %s"%test_typer_count
                    test = Protocol + "/" + test_typer_count
                    for statistic_test_count in os.walk("%s" % ( test)).next()[1]:
                        while True:
                            #We call the if to ensure no more than the max allowed threads are running at once
                            if threading.activeCount() < MaxThreads:
                                x = Thread(target = hopcount, args = (test ,statistic_test_count,))
                                x.start()
                            #Break out of the while loop to return to the above for loop.
                                break
                    
                HopsBehandler(Protocol)





main()

