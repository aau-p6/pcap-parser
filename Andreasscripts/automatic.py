import os
import signal
import subprocess
from threading import Thread
import threading
import time
import sys
import socket
import errno
MaxThreads = 7
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


            
def functest(dirnavn, RunNumber, numNodes):
    #Error at times occur where some of the threads will terminate.
    #threads will create the directory but when the simulation normally would be done nothing can be found in the directory
    if os.path.isdir(dirnavn) != True:
        os.makedirs ('%s' % dirnavn)
    os.popen('./waf --run "scratch/bitchboi --Run_number=%d --File_name=%s --numNodes=%d --XRange=500 --YRange=500 --SignalStrenght=0"' % (RunNumber, dirnavn, numNodes), 'w', 0)
    
def autotest():
    root = "Results/OLSR"
    if os.path.isdir(root) != True:
        os.makedirs('%s' % root)
    for gtc in range(2):
        numNodes= ((gtc*2)+8)*10
        dirnavn = root + "/OLSR" + str(numNodes)
        for i in range(50):
            RunNumber = (i + 1)
            runname = dirnavn + "/test" + str(RunNumber)
            while True:
                time.sleep(2)
                if threading.activeCount() < MaxThreads:
                    x = Thread(target = functest, args= (runname, RunNumber, numNodes,))
                    x.start()
                #functest(runname, RunNumber, gtc)
                    break
    
    

autotest()

