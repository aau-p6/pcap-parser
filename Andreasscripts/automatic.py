import os
import signal
import subprocess
from threading import Thread
import threading
import time
MaxThreads = 5


def func(dirnavn, RunNumber):
    #Error at times occur where some of the threads will terminate.
    #threads will create the directory but when the simulation normally would be done nothing can be found in the directory
        if os.path.isdir(dirnavn) != True:
            os.popen ('mkdirs %s' % dirnavn)
        os.popen('./waf --run "scratch/bitchboi --Run_number=%d --File_name=%s"' % (RunNumber, dirnavn))


def auto():
        dirnavn = "Results/OLSR/OLSR"
        for i in range(100):
            RunNumber = i + 1
            runname = dirnavn + str(RunNumber)
            while True:
                if threading.activeCount() < MaxThreads:
                    x = Thread(target = func, args= (runname, RunNumber,))
                    time.sleep(1)
                    x.start()
                    break
        # Will catch the process so it won't exit
        while True:
            print("Here we go again")
            print(threading.activeCount())
            time.sleep(3)
            # Will only allow the process to move onwards if there is no active thread besides the process itself.
            if threading.activeCount() == 1:
                for i in range(50):        
                    print("WAT ZE FUCK")
                # Will check the amount of tests that have to be rerun and if more than 0 the process for rerunning these will be called.
                if len(Errorfinder()) > 0:
                    Errorfixer(dirnavn)
            # When no more files need to be rerun which means all directories has a .xml file the program will exit
            if len(Errorfinder()) == 0:
                break
            
def functest(dirnavn, RunNumber, gtc):
    #Error at times occur where some of the threads will terminate.
    #threads will create the directory but when the simulation normally would be done nothing can be found in the directory
    if os.path.isdir(dirnavn) != True:
        os.makedirs ('%s' % dirnavn)
    os.popen('./waf --run "scratch/bitchboi --Run_number=%d --File_name=%s --MaxChildren=%d"' % (RunNumber, dirnavn, gtc))
            
def autotest():
    
    for gtc in range(4):
        dirnavn = "Results/OLSR" + str(gtc) +"/OLSR"
        for i in range(100):
            RunNumber = i + 1
            runname = dirnavn + str(RunNumber)
            while True:
                time.sleep(2)
                if threading.activeCount() < MaxThreads:
                    x = Thread(target = functest, args= (runname, RunNumber, gtc,))
                    x.start()
                    break
        # Will catch the process so it won't exit
        while True:
            print("Here we go again")
            print(threading.activeCount())
            time.sleep(3)
            # Will only allow the process to move onwards if there is no active thread besides the process itself.
            if threading.activeCount() == 1:
                for i in range(50):        
                    print("WAT ZE FUCK")
                # Will check the amount of tests that have to be rerun and if more than 0 the process for rerunning these will be called.
                if len(Errorfinder()) > 0:
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
                
                
                
def Errorfinder():
    Error_list = []
    Redos = []
    Redo = ""
    dir_navn = "Results/OLSR"
    for dirs in os.walk("%s" % dir_navn).next()[1]:
        if os.path.isfile("%s/%s/OLSR.xml" % (dir_navn, dirs)) != True:
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
#Errorfixer("Results/OLSR/OLSR")
#nodes()
#Datarate()
#Packets()
#Errorfinder()


        
    
