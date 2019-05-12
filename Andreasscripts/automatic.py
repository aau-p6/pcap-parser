import os
import signal
import subprocess
from threading import Thread
import threading
import time
import sys
import socket
import errno
MaxThreads = 5
Protocol_types = ['AODV', 'OLSR', 'DSR', 'DSDV']
Datarates = []

#With regards to different starting parameters a small list will be gone through and what they refer to.
#changes in the script may be required in order to change the parameter of interest.

#Run_number refers to which run which means its required to make some sort of statistic on a set of parameters.
#File_name is where the files should be saved as the "root" of the structure. Placing the Overheadthreading.py in the root folder
#Will allow it to be run
#MaxChildren refers to the amount of nodes that are allowed to transmit at the same time. Setting it to 1 or 0 will only let
#The main traffic generator work anything beyond will increase the amount of transmitters through allowing GenerateTrafficChild to be run
#packetSize will alter the size of the packet, if changing this alterations are required in the Overhead.py script 
#Will look into this later on.
#numPacket changes the amount of packets sent during a run 
#min_random_interval refers to the highest number the random interval will generate, could be of interest for higher packetintervals
#max_random_interval refers to the lowest number the random interval will generate
#min_packetinterval is practically added to the max packetinterval, can be a float if of interest
#max_packetinterval is almost the max however min packetinterval is added to it later on. This number MUST be an integer due to modulus


            
def functest(dirnavn, RunNumber, gtc):
    #Error at times occur where some of the threads will terminate.
    #threads will create the directory but when the simulation normally would be done nothing can be found in the directory
    if os.path.isdir(dirnavn) != True:
        os.makedirs ('%s' % dirnavn)
        os.popen('./waf --run "scratch/bitchboi --Run_number=%d --File_name=%s --MaxChildren=%d"' % (RunNumber, dirnavn, gtc), 'w', 0)

def autotest():
    root = "Results/OLSR"
    if os.path.isdir(root) != True:
        os.makedirs('%s' % dirnavn)
    for gtc in range(4):
        children = gtc + 1
        dirnavn = root + "/OLSR" + str(children)
        for i in range(100):
            RunNumber = i + 1
            runname = dirnavn + "/test" + str(RunNumber)
            while True:
                time.sleep(2)
                if threading.activeCount() < MaxThreads:
                    x = Thread(target = functest, args= (runname, RunNumber, children,))
                    x.start()
                #functest(runname, RunNumber, gtc)
                    break
        # Will catch the process so it won't exit
        
def til_errorfixing():
    while True:
        print("Here we go again")
        print(threading.activeCount())
        time.sleep(3)
        # Will only allow the process to move onwards if there is no active thread besides the process itself.
        if threading.activeCount() == 1:
            for i in range(50):        
                print("WAT ZE FUCK")
            # Will check the amount of tests that have to be rerun and if more than 0 the process for rerunning these will be called.
            if len(Errorfinder(dirnavn)) > 0:
                Errorfixer(dirnavn)
        # When no more files need to be rerun which means all directories has a .xml file the program will exit
        if len(Errorfinder()) == 0:
            break
            
        
        
        
def nodes():
    #Virker
    for i in range(10): # How many diffrent node amount we try times 5
        numNodes = (i + 1)*5 
        for j in range(20): # How many individual tests are run for each node amount
                RunNumber = j + 1
                dirnavn = "Results/OLSR/OLSR" + str(numNodes)+ "/" +"Test" +str(RunNumber)
                print(os.path.isdir(dirnavn))
                if os.path.isdir(dirnavn) != True:
                    os.makedirs (dirnavn)
                os.popen('./waf --run "scratch/bitchboi --numNodes=%d --Run_number=%d --File_name=%s"' %(numNodes, RunNumber, dirnavn))    
            #subprocess.Popen('./waf --run "scratch/bitchboi --Run_number=%d --numNodes=%d "' %(RunNumber, numNodes), shell=True)
            
def Datarate():
    #virker ikke endnu
    for i in range(10): # How many diffrent node amount we try times 5
        rate = str((i + 1) * 0.1) # The number here is how much we increase the datarate by for each iteration 
        for j in range(20): # How many individual tests are run for each node amount
            
            ##########################################Note til mig selv: Check errormessag for this config as it contains valid information ################################1##
                RunNumber = j + 1
                DataRate = ("DsssRate%sMbps" % rate)
                dirnavn = "Results/OLSR/OLSR" + str(rate)+ "/" +"Test" +str(RunNumber)
                print(os.path.isdir(dirnavn))
                if os.path.isdir(dirnavn) != True:
                    os.makedirs (dirnavn)
                os.popen('./waf --run "scratch/bitchboi --phyMode=%s --Run_number=%d --File_name=%s"' %(Datarate, RunNumber, dirnavn))    
            
def Packets():
    #virker?
    for i in range(10): # How many diffrent packet sizes we try times 5
        PacketSize = (i + 1) * 100 # This number represents how much the packet size is increased with each iteration
        for j in range(20): # How many individual tests are run for each node amount
                RunNumber = j + 1
                dirnavn = "Results/OLSR/OLSR" + str(PacketSize)+ "/" +"Test" +str(RunNumber)
                print(os.path.isdir(dirnavn))
                if os.path.isdir(dirnavn) != True:
                    os.makedirs (dirnavn)
                os.popen('./waf --run "scratch/bitchboi --packetSize=%d --Run_number=%d --File_name=%s"' %(PacketSize, RunNumber, dirnavn))
                
                
                
def Errorfinder(dirnavn):
    Error_list = []
    Redos = []
    Redo = ""
    dir_navn = "Results/OLSR"
    for dirs in os.walk("%s" % dirnavn).next()[1]:
        if os.path.isfile("%s/%s/OLSR.xml" % (dirnavn, dirs)) != True:
            Error_list.append("%s" % (dirs))
    
    for lines in Error_list:
        for nr in lines:
            if nr.isdigit() == True:
                Redo = Redo + nr
        Redos.append(Redo)
        Redo = ""
    print ("FEJL ER HER")
    print (Redos)
    print ("FEJL ER HER")
    return Redos
                
    
def Errorfixer(dirnavn):
    while True:
        print("We done for now.")
        Redos = Errorfinder()
        print(len(Redos))
        if len(Redos) == 0:
            break
        
        if len(Redos) > 0:
            print("Weeeeelll fuck")
            for errors in Redos:
                fejl = int(errors)
                runagain = dirnavn + errors
                os.popen('./waf --run "scratch/bitchboi --Run_number=%d --File_name=%s"' %(fejl, runagain))
                print("Here we r with test number %d" % fejl)
                print("Here we r with test %s" % runagain)
        Errorfixer(dirnavn)
    
    
    
#auto()
autotest()
#nodes()
#functest('Results/OLSR', 5, 2)
#Datarate()
#Packets()
#Errorfinder()


        
    
