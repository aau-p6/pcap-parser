import pcapy
import os
import re
from threading import Thread, Lock
import threading
#Define the amount of threads to allow be run at the same time. Running more threads should decrease time to extract information.
MaxThreads = 20
#Define the name of test types as found in the /ns-3-dev/Results 
mutex = Lock()

def Flow_Monitor(test_typer, test_typer_count, statistic_test_count):
                
                
                # We check if the previously defined dir_navn exists and if so we will look for the xml file in there
                if (os.path.isdir(test_typer + "/" + test_typer_count)):
                    xml_navn = test_typer + ".xml"
                # We open the flow_monitor xml file for extraction
                    Flow_Ids = []
                    f = open('%s/%s/%s/%s' % (test_typer, test_typer_count, statistic_test_count, xml_navn), 'r')
                    #We read the entire file
                    f1 = f.readlines()
                    f.close()
                    #we define a substring which we will use to look for the entries in the file that are of relevance to us
                    substring = "timeFirstTxPacket"
                    #Clear variables used for extraction
                    del Flow_Ids[:]
                    for lines in f1:
                        #All of the relevant lines are saved into the list flow.ids
                            if substring in lines:
                                Flow_Ids.append(lines)
                            DataSent = 0
                            DataReceived = 0
                            PacketsSent = 0
                            PacketsReceived = 0
                            PacketsDropped = 0
                            Unlisted_Dropped = 0
                            EndtoEndDelay = 0
                            Average_EndtoEndDelay = -1
                            OverheadData = 0
                            Packet_drop_rate = 0
    # We will go through each individual Flow_ID and find their respective data and sum it up

                            for lines in Flow_Ids:
    #We will split up each line between each "" as these are around all the data we are interested in
                                Data_line = lines
                                Data = re.split('"|"',Data_line)
    #These substrings that are saved through spliting are saved 
    #Disse er gennemgaaet manuelt og navnet svarer til talvaerdien set i xml filen uden +/- og ns
                                PacketsSent = int(Data[21]) + PacketsSent
                                PacketsReceived = int(Data[23]) + PacketsReceived
                                PacketsDropped =  int(Data[25]) + PacketsDropped
                                DataSent = PacketsSent * 1000
                                DataReceived = 1000 * PacketsReceived
                                EndtoEndDelay = int(Data[11][1:-4]) + EndtoEndDelay
                                
                    if PacketsReceived != 0:
                        Average_EndtoEndDelay = (EndtoEndDelay /PacketsReceived)
    # We calculate data based on the sum of the previous extracted data 
                    sti = test_typer + "/"+ test_typer_count + "/" + statistic_test_count
                    print(sti)
                    SamletData = int(AltDataSendt(sti))
                    if DataReceived != 0:
                        OverheadData = (((SamletData*1.0) -DataReceived*1.0)/(DataReceived*1.0))*100.0
                    print(OverheadData)
                    Packet_drop_rate = round((1.0-(PacketsReceived*1.0)/(PacketsSent*1.0)) * 100.0)
                    print (Packet_drop_rate)
                    if len(Flow_Ids) != 0:
                    #We save a collecte_data.txt in each of the directories of the different tests run
                        Data_storage =  test_typer +"/" + test_typer_count
                        Histogram_storage = "Histogramdata/" +  test_typer_count[0:]

                        #Write Droprates for histograms
                        mutex.acquire()
                        try:
                            f= open('%sHistogramDroprate.txt' %(Histogram_storage) , 'a')
                            f.write("%f," % Average_EndtoEndDelay)
                            f.close()
                        finally:
                            mutex.release()
                            
                            #Write Delays for histogram
                        mutex.acquire()
                        try:
                            f= open('%sHistogramDelay.txt' %(Histogram_storage) , 'a')
                            f.write("%d," % Packet_drop_rate)
                            f.close()
                        finally:
                            #Write Overhead for histogram
                            mutex.release()
                            
                        mutex.acquire()
                        try:
                            f= open('%sHistogramOverhead.txt' %(Histogram_storage) , 'a')
                            f.write("%d," % OverheadData)
                            f.close()
                        finally:
                            mutex.release()
                            
                            
                        mutex.acquire()
                        try:
                            f= open('%s/Collected_data.txt' %(Data_storage) , 'a')
                            f.write('Vi er nu i fil %s/%s\n' %(test_typer_count, statistic_test_count))
                            f.write ('Total amount of packets sent %d\n Toal amount of packets received %d\nThe Average end to end delay was %d nanoseconds\n' %( PacketsSent, PacketsReceived, Average_EndtoEndDelay))
                            f.write('Overhead for this test was %d procent \nPacket drop rate for this test was %d\n' % (OverheadData, Packet_drop_rate))
                            f.write ("\nNew test data will come in \n\n")
                            f.close()
                        finally:
                            mutex.release()

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
    return(Samlet)
    





def main():
    #Used to save Histogram data
    if os.path.isdir('Histogramdata') !=True:
        os.makedirs('Histogramdata')
    
      # We will go through the different tests we have as defined in the Test_type array
    for test_typer in os.walk('.').next()[1]:
        #Directory wise this is /ns-3-dev/Results/OLSR for example
        for test_typer_count in os.walk("%s" % (test_typer)).next()[1]:
            # Directory wise this is /ns-3-dev/Results/OLSR/OLSR5 where the last directory is the different tests as specified in automatic.py
            #Further down we now are in the directory of extra tests for the same test in order to make statistical analysis on it
            if os.path.isdir('%s/%s' % (test_typer, test_typer_count )) == True:
                for statistic_test_count in os.walk("%s/%s" % ( test_typer, test_typer_count)).next()[1]: 
                # Directory wise this is /ns-3-dev/Results/OLSR/OLSR5/test5 where the last directory will maximum be the run_number specified in automatic.py
                #We define the specific directory to look into for the thread.
                    dir_navn = test_typer + "/" + test_typer_count
                    while True:
                #We call the if to ensure no more than the max allowed threads are running at once
                        if threading.activeCount() < MaxThreads:
                            x = Thread(target = Flow_Monitor, args = (test_typer, test_typer_count, statistic_test_count))
                            x.start()
                            #Break out of the while loop to return to the above for loop.
                            break

main()
#Flow_Monitor('OLSR', 'OLSR15', 'test50')


