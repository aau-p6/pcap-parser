import pcapy
import os
import re
#Definer fil listen som vil indeholde alle Pcap filer
File_list = []
Flow_Ids = []
def Flow_monitor():
    #Vi laeser foesrt indholdet af XML filen
    f= open('Aodvtest.xml', 'r')
    f1 = f.readlines()
    f.close()
    substring = "timeFirstTxPacket"
    for lines in f1:
        if substring in lines:
            Flow_Ids.append(lines)
    DataSent = 0
    DataReceived = 0
    PacketsSent = 0
    PacketsReceived = 0
    PacketsDropped = 0
    Unlisted_Dropped = 0
    EndtoEndDelay = 0
    # We will go through each individual Flow_ID and find their respective data and sum it up
    for lines in Flow_Ids:
    #Vi splitter nu linjen op saa vi kun faar strings mellem 2 " "
        Data_line = lines
        Data = re.split('"|"',Data_line)
    #Vi gemmer saa de nye substrings som er relevante
    #Disse er gennemgaaet manuelt og navnet svarer til talvaerdien set i xml filen uden +/- og ns
        #FirstPacketSent =  int(Data[3][1:-4])
        #FirstPacketReceived = int(Data[5][1:-4]) - FirstPacketSent
        #LastPacketSent = int(Data[7][1:-4]) - FirstPacketSent
        #LastPacketReceived = int(Data[9][1:-4]) - FirstPacketSent
        #Delaysum = int(Data[11][1:-4])
        #Jittersum = int(Data[13][1:-4])
        PacketsSent = int(Data[21]) + PacketsSent
        PacketsReceived = int(Data[23]) + PacketsReceived
        PacketsDropped =  int(Data[25]) + PacketsDropped
        DataSent = 1000 * PacketsSent + DataSent
        DataReceived = 1000 * PacketsReceived + DataReceived
        tempPacketsReceived = int(Data[23])
        if tempPacketsReceived != 0:
            EndtoEndDelay = EndtoEndDelay + (int(Data[11][1:-4]) /tempPacketsReceived)
            
    # We calculate data based on the sum of the previous extracted data 
    OverheadData = int(SamletDataSendt()) - DataSent
    Average_EndtoEndDelay = EndtoEndDelay / len(Flow_Ids)
    Unlisted_Dropped = (PacketsSent - (PacketsReceived + PacketsDropped))
    f= open('Collected_data.txt', 'a')
    #f.write('First packet received at %d ns from start \n' % (FirstPacketReceived))
    f.write ('Total amount of packets sent %d\n Toal amount of packets received %d\nThe Average end to end delay was %d nanoseconds\n' %( PacketsSent, PacketsReceived, Average_EndtoEndDelay))
    f.write ('Packets lost in transmission %d\nA total of %d bytes were sent\nA total of %d bytes were received\n' %(PacketsDropped, DataSent, DataReceived))
    f.write ('Overhead Data sent is %d\nA total of %d were dropped but not listed\n' % (OverheadData, Unlisted_Dropped))
    f.close
def SamletDataSendt():
    
 #Vi finder alle Pcap filer i den folderen vi er i
 os.popen('ls | grep pcap > idunno.txt').read()
 Pcap_count = os.popen('wc -l idunno.txt').read()
 
 # Vi finder det reelle antal af filer af pcap typen
 File_list_lenght =''.join(c for c in "%s"%Pcap_count if c.isdigit())
 readfile= open('idunno.txt', 'r')
 if readfile:
     for lines in readfile:
         File_list.append(lines)
 readfile.close()
 Lenght = len(File_list)
 
 Samlet = 0

 #Vi kan nu finde alt data sendt som set i pcap filerne
 for i in range(0, len(File_list)):
  Overheadsum = 0
 # Vi laeser fra vores oenskede pcap fil en af gangen
  fil = File_list[i].rstrip()
  reader= pcapy.open_offline("%s"%fil)
 #Vi finder hvor mange frames der er i den givne pcap filen
  Lenght = os.popen('tshark -r %s | wc -l' % fil).read()
  PcapLenght = int(Lenght)

  #Vi koerer igennem alle frames/pakker og finder deres laengder i bytes
  for x in range(0, PcapLenght):
      (header, payload) = reader.next();
      # Summer alle frames laengder
      
      Overheadsum = Overheadsum + header.getlen();
  Samlet = Samlet + Overheadsum
 f = open('Collected_data.txt', 'a')
 f.write("Total byte count in the system is %d\n" %Samlet)
 f.close()
 return Samlet
Flow_monitor()
