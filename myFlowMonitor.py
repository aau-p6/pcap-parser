import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import pcapy
import math

def treatData(sendID,sendTime,rID,rTime):
    delayList = []
    for i in range(len(sendID)):
	    for j in range(len(rID)):
		    if sendID[int(i)] == rID[int(j)]:
			    delayList.append(rTime[int(j)] - sendTime[int(i)])
    endToEndDelay = np.mean(delayList)
    print("packets send: {}\npackets received: {}".format(len(sendID),len(rID)))
    dropRate = round(((1-len(rID)/len(sendID))*100))
    print("Droperate: {}".format(dropRate))
    print("Average end-to-end delay is: {}".format(endToEndDelay))
    samletDat = AltDataSendt("/home/jonas/Desktop/Results/Experimental/")
    print(samletDat)

    

def getData ():
    sendingID = []
    sendingTime = []
    receivedID = []
    receivedTime = []

    myFile = open("/home/jonas/Documents/p6/flowmonitor replacement/SendingLogdata.txt","r")
    for line in myFile:
        fields = line.split(", ")
        if fields[1].isdigit():
            sendingID.append(fields[1]) 
        sumvar = fields[3]
        sumvar = sumvar[1:-3]
        sendingTime.append(sumvar)
    myFile.close()

    sendingID = list(map(int, sendingID))
    sendingTime = list(map(float, sendingTime))
    sendingTime = list(map(int, sendingTime))

    myFile = open("/home/jonas/Documents/p6/flowmonitor replacement/ReceivedLogdata.txt","r")
    for line in myFile:
        fields = line.split(", ")
        if fields[1].isdigit():
            receivedID.append(fields[1]) 
        sumvar = fields[3]
        sumvar = sumvar[1:-3]
        receivedTime.append(sumvar)
    myFile.close()

    receivedID = list(map(int, receivedID))
    receivedTime = list(map(float, receivedTime))
    receivedTime = list(map(int, receivedTime))

    print("Sending ID: {} \n".format(sendingID))
    print("Sending time: {} \n".format(sendingTime))

    print("Receiving ID: {} \n".format(receivedID))
    print("Receiving time: {} \n".format(receivedTime))
    
    treatData(sendingID,sendingTime,receivedID,receivedTime)

def AltDataSendt(path):
    File_list = []
    PcapFiles =[]
    Overheadsum = 0
    Samlet = 0
 #Vi finder alle Pcap filer i den folderen vi er i
    substring = '.pcap'
    for Allfiles in os.popen('ls %s' %path):
        if substring in Allfiles:
            PcapFiles.append(Allfiles) 
 #Vi kan nu finde alt data sendt som er i pcap filen.
    for pcap in PcapFiles:
 #We read one pcap file at a time.
        fil = path + "/" + pcap.rstrip()
        reader = pcapy.open_offline("%s" % fil)
 #Vi finder hvor mange frames der er i den givne pcap filen
        Lenght = os.popen('tshark -r %s | wc -l' % fil).read()
        PcapLenght = int(Lenght)
  #Vi koerer igennem alle frames/pakker og finder deres laengder i bytes
        for x in range(0, PcapLenght):
            (header, payload) = reader.next();
      # Summer alle frames laengder
      
            Overheadsum = Overheadsum + header.getlen();
    Samlet = Samlet + Overheadsum
    print(Samlet)
    return(Overheadsum)


getData()
