#!/usr/bin/env python

import os
import math
from decimal import*
Protocols = ["AODV", "DSR", "OLSR", "DSDV"];
getcontext().prec = 10


def statistic():
    
        Interval_Storage="Histogramdata/Intervaller"
        if os.path.isdir(Interval_Storage) != True:
            os.makedirs(Interval_Storage)
    #for Protocol in Protocols: # We are going through the 4 directories defined in Test_type
        Protocol = "OLSR"
        print os.walk("%s" % (Protocol)).next()
        for node_count in os.walk("%s" % (Protocol)).next()[1]: # We go through the individual type test i.e 5 nodes, 10 nodes and so on
            #Clearing variables used during extraction of individual tests data.
            Delays = []
            samletDataSent = []
            PacketsSent = []
            PacketsReceived = []
            tempDelays = []
            tempOverhead = []
            tempPacketsSent = []
            tempPacketsReceived = []
            Droprate = []
            Overhead_fixed = []
            delay = 0
            DelaySum = 0
            OverheadAverage = 0
            PacketsSentSum = 0
            PacketsReceivedSum = 0
            DroprateAverage = 0
            DelayAverage = 0
            Delay_Variation = 0
            Droprate_Variation = 0
            Overhead_Variation = 0
            Worst_Overhead = 1
            Worst_delay = 0
            Worst_Droprate = 0
            Xnummer = []
            Delay_Confidence_leftside = 0
            Delay_Confidence_rightside = 0
            Overhead_Confidence_leftside = 0
            Overhead_Confidence_rightside = 0
            Droprate_Confidence_leftside = 0
            Droprate_Confidence_rightside = 0
            # We will now extract the actual number for the metrics
            #These are extracted by saving which lines contain the relevant info.
            tempDelays = os.popen("grep nanoseconds %s/%s/Collected_data.txt" % ( Protocol, node_count)).read()
            for s in tempDelays.split(): 
                #With the lines stored in tempDelays they are then afterwards cut up so that only the digits are preserved
                #This only works because each line only has one number present
                if s.isdigit():
                    Delays.append(s)
                    
            tempOverhead = os.popen("grep samletDataSent %s/%s/Collected_data.txt" % ( Protocol, node_count)).read()
            for s in tempOverhead.split(): 
                if s.isdigit():
                    samletDataSent.append(s)
                    
            tempPacketsSent = os.popen("grep 'packets sent' %s/%s/Collected_data.txt" % ( Protocol, node_count)).read()
            for s in tempPacketsSent.split(): 
                if s.isdigit():
                    PacketsSent.append(s)
                    
            tempPacketsReceived = os.popen("grep 'packets received' %s/%s/Collected_data.txt" % ( Protocol, node_count)).read()
            for s in tempPacketsReceived.split(): 
                if s.isdigit():
                    PacketsReceived.append(s)
            #We are done saving the relevant data.        
            #We will now calculate the average and standard deviation for the metrics extracted
            
            #Delays
            if len(Delays) !=0:
                for entry in Delays:
                #If sentence is used to find the worst delay e.g the highest one
                    if Worst_delay < int(entry)/1000000: # Dividing by 1000000 is to have the number in milliseconds rather than nanoseconds
                        Worst_delay = int(entry)/1000000
                #Average is calculated by summing up all the entries divided by the amount of entries.
                    DelayAverage= DelayAverage + (int(entry)/1000000)
                DelayAverage = DelayAverage/len(Delays)
                for entry in Delays:
                #Standard_Deviation is calculated as the sum of each entry minus the average squared.
                    Delay_Variation = (((int(entry)/1000000) - DelayAverage) * ((int(entry)/1000000) - DelayAverage)) + Delay_Variation
            #We furthermore divide this by the lenght of entries
                Delay_Variation = Delay_Variation/len(Delays)
                Delay_Standard_deviation = math.sqrt(Delay_Variation)
                #Confidence interval is presented with 2 digits
                Delay_Confidence_leftside = round(DelayAverage - (1.96 * Delay_Standard_deviation/math.sqrt(len(Delays))),2 )
                Delay_Confidence_rightside = round(DelayAverage + (1.96 * Delay_Standard_deviation/math.sqrt(len(Delays))),2 )
                #print(" Delay For test %s Confidence interval is %s < theta > %s" %(node_count, Delay_Confidence_leftside, Delay_Confidence_rightside))
            #Comments in this section also apply to the others
            
            #Overhead
            getcontext().prec = 10
            if len(samletDataSent) !=0:
                for entry in range(len(samletDataSent)):
                    
                    if PacketsReceived[entry]!='0':
                        #print "First:  ",PacketsReceived[entry], "   " ,samletDataSent[entry]
                        PacketDataSent = int(PacketsReceived[entry])*20
                        AllDataSent = int(samletDataSent[entry])
                        Overhead_fixed.append(Decimal(1.0-((AllDataSent-PacketDataSent)*1.0/AllDataSent*1.0)))
                getcontext().prec = 10
                print("overhead is".format(Overhead_fixed))
                for entry in Overhead_fixed:
                    if Worst_Overhead > Decimal(entry):
                        #print "nu"
                        Worst_Overhead = Decimal(entry)
                        #print entry
                        #print Worst_Overhead
                    OverheadAverage = OverheadAverage + (Decimal(entry))
                OverheadAverage = OverheadAverage/len(Overhead_fixed)
                for entry in Overhead_fixed:
                    Overhead_Variation= ((Decimal(entry)) - OverheadAverage) * ((Decimal(entry))-OverheadAverage) + Overhead_Variation
                Overhead_Variation = Overhead_Variation / len(Overhead_fixed)
                Overhead_Standard_deviation = math.sqrt(Overhead_Variation)
                print Overhead_Standard_deviation

                Overhead_Confidence_leftside = Decimal(Decimal(OverheadAverage) - (Decimal('1.96') * Decimal(Overhead_Standard_deviation)/Decimal(math.sqrt(len(Overhead_fixed)))))
                Overhead_Confidence_rightside =Decimal(Decimal(OverheadAverage) + (Decimal('1.96') * Decimal(Overhead_Standard_deviation)/Decimal(math.sqrt(len(Overhead_fixed)))))
                
            #Droprate
            #We first create a Droprate list by finding the droprate for each test
            getcontext().prec = 10
            if len(PacketsReceived) !=0:
                
                for i in range(len(PacketsReceived)):
                    Droprate.append((1 * 1.0 - (int(PacketsReceived[i]) *1.0/ int(PacketsSent[i] )*1.0))*100) 
                for entry in Droprate:
                    if Worst_Droprate < int(entry):
                        Worst_Droprate = int(entry)
                    DroprateAverage = DroprateAverage + (float(entry))
                DroprateAverage = DroprateAverage/len(Droprate)
                for entry in Droprate:
                    Droprate_Variation = (float(entry) - DroprateAverage) * (float(entry) - DroprateAverage) + Droprate_Variation
                Droprate_Variation = Droprate_Variation/len(Droprate)
                Droprate_Standard_deviation = math.sqrt(Droprate_Variation)
                Droprate_Confidence_leftside = round(DroprateAverage - (1.96 * Droprate_Standard_deviation/math.sqrt(len(Droprate))), 2)
                Droprate_Confidence_rightside = round(DroprateAverage + (1.96 * Droprate_Standard_deviation/math.sqrt(len(Droprate))), 2)
                #print (" Droprate For test %s Confidence interval is %s < theta > %f" %(node_count, Droprate_Confidence_leftside, Droprate_Confidence_rightside))
            getcontext().prec = 10
            f = open("%s/Confidenceinterval_Left_Delay.txt" %Interval_Storage, 'a')
            f.write("%s,"%Delay_Confidence_leftside)
            f.close()
            
            f = open("%s/Average_Delay.txt" %Interval_Storage, 'a')
            f.write("%s,"%DelayAverage)
            f.close()
            
            f = open("%s/Confidenceinterval_Right_Delay.txt" %Interval_Storage, 'a')
            f.write("%s," %Delay_Confidence_rightside)
            f.close()
            
            f = open("%s/Confidenceinterval_Left_Droprate.txt" %Interval_Storage, 'a')
            f.write("%s,"%Droprate_Confidence_leftside)
            f.close()
            
            f = open("%s/Average_Droprate.txt" %Interval_Storage, 'a')
            f.write("%s,"%DroprateAverage)
            f.close()
            
            f = open("%s/Confidenceinterval_Right_Droprate.txt" %Interval_Storage, 'a')
            f.write("%s,"%Droprate_Confidence_rightside)
            f.close()
            if len(Overhead_fixed) != 0:
                f = open("%s/Confidenceinterval_Left_Overhead.txt" %Interval_Storage, 'a')
                f.write("{:.10f},".format(Overhead_Confidence_leftside))
                f.close()
            
                f = open("%s/Average_Overhead.txt" %Interval_Storage, 'a')
                f.write("{:.10f},".format(OverheadAverage))
                f.close()
            
                f = open("%s/Confidenceinterval_Right_Overhead.txt" %Interval_Storage, 'a')
                f.write("{:.10f}," .format(Overhead_Confidence_rightside))
                f.close()
        
            for s in node_count:
                X =''
                if s.isdigit():
                    Xnummer.append(s)
            #print("Xnummer er %s\n" % Xnummer)
            for string in range(len(Xnummer)):
                X = X + Xnummer[string]
                X = X.rstrip()
            #print(X)
                    
                    #print(X)
            f = open("%s/X.txt" %Interval_Storage, 'a')
            f.write("%s,"%X)
            f.close()
            #Write to file - Is currently placed in the upper folder as in Results/{Protocol}/{Test_type} where the tests run for that configuration are placed.
            #Test_type could here be a specific amount of nodes.
            f = open("%s/Statistic data.txt" %(Protocol), 'a')
            f.write("\n############################ Data for test %s ###########################\n" %node_count)
            f.write("Average Delay in milliseconds %s\nStandard deviation %s\nWorstcase %s\n" % (DelayAverage, Delay_Variation, Worst_delay))
            f.write("Confidence interval was %f < theta >%f\n \n" % (Delay_Confidence_leftside, Delay_Confidence_rightside))
            f.write("Average Overhead in Percent {:.10f}\nStandard deviation {:.10f}\nWorstcase {:.10f}\n".format(OverheadAverage, Overhead_Variation, Worst_Overhead))
            if len(Overhead_fixed) !=0:
                f.write("Confidence interval was {:.10f} < theta >{:.10f}\n \n". format(Overhead_Confidence_leftside, Overhead_Confidence_rightside))
            f.write("Average droprate in percent %s\nStandard deviation %s\nWorstcase %s\n" % (DroprateAverage, Droprate_Variation, Worst_Droprate))
            f.write("Confidence interval was %f < theta >%f\n \n" % (Droprate_Confidence_leftside, Droprate_Confidence_rightside))
            f.close()

            

            



statistic()

