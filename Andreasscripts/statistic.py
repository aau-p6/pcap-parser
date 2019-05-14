import os
import math
import re
Test_type = ["AODV", "DSR", "OLSR", "DSDV"];

def statistic():
    Interval_Storage="Histogramdata/Intervaller"
    for test_navn in Test_type: # We are going through the 4 directories defined in Test_type
        for node_count in os.walk("%s" % (test_navn)).next()[1]: # We go through the individual type test i.e 5 nodes, 10 nodes and so on
            #Clearing variables used during extraction of individual tests data.
            Delays = []
            Overhead = []
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
            Worst_Overhead = 10
            Worst_delay = 0
            Worst_Droprate = 0
            
            # We will now extract the actual number for the metrics
            #These are extracted by saving which lines contain the relevant info.
            tempDelays = os.popen("grep nanoseconds %s/%s/Collected_data.txt" % ( test_navn, node_count)).read()
            for s in tempDelays.split(): 
                #With the lines stored in tempDelays they are then afterwards cut up so that only the digits are preserved
                #This only works because each line only has one number present
                if s.isdigit():
                    Delays.append(s)
                    
            tempOverhead = os.popen("grep Overhead %s/%s/Collected_data.txt" % ( test_navn, node_count)).read()
            for s in tempOverhead.split():
                print(s)
                if s.isdigit():
                    Overhead.append(s)
                    
            tempPacketsSent = os.popen("grep 'packets sent' %s/%s/Collected_data.txt" % ( test_navn, node_count)).read()
            for s in tempPacketsSent.split():
                
                if s.isdigit():
                    PacketsSent.append(s)
                    
            tempPacketsReceived = os.popen("grep 'packets received' %s/%s/Collected_data.txt" % ( test_navn, node_count)).read()
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
            if len(Overhead) !=0:
                for entry in Overhead:
                    c = float(entry)/100
                    value = (1/c)*100
                    Overhead_fixed.append(value)
                for entry in Overhead_fixed:
                    if Worst_Overhead > float(entry):
                        #print(Worst_Overhead)
                        Worst_Overhead = float(entry)
                    OverheadAverage = OverheadAverage + float(entry)
                OverheadAverage = OverheadAverage/len(Overhead)
                for entry in Overhead_fixed:
                    Overhead_Variation= ((float(entry)) - OverheadAverage) * ((float(entry))-OverheadAverage) + Overhead_Variation
                Overhead_Variation = Overhead_Variation / len(Overhead)
                Overhead_Standard_deviation = math.sqrt(Overhead_Variation)
                Overhead_Confidence_leftside = round(OverheadAverage - (1.96 * Overhead_Standard_deviation/math.sqrt(len(Overhead))),5)
                Overhead_Confidence_rightside =round(OverheadAverage + (1.96 * Overhead_Standard_deviation/math.sqrt(len(Overhead))), 5)
                #print (" Overhead For test %s Confidence interval is %s < theta > %s" %(node_count,Overhead_Confidence_leftside, Overhead_Confidence_rightside))
            
            
            #Droprate
            #We first create a Droprate list by finding the droprate for each test
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
                #print ("Droprate For test %s Confidence interval is %f < theta > %f" %(node_count, Droprate_Confidence_leftside, Droprate_Confidence_rightside))
            
            f = open("%s/Confidenceinterval_Left_Delay" %Interval_Storage, 'a')
            f.write("%s,"%Delay_Confidence_leftside)
            f.close()
            
            f = open("%s/Confidenceinterval_Right_Delay" %Interval_Storage, 'a')
            f.write("%s," %Delay_Confidence_rightside)
            f.close()
            
            f = open("%s/Confidenceinterval_Left_Droprate" %Interval_Storage, 'a')
            f.write("%s,"%Droprate_Confidence_leftside)
            f.close()
            
            f = open("%s/Confidenceinterval_Right_Droprate" %Interval_Storage, 'a')
            f.write("%s,"%Droprate_Confidence_rightside)
            f.close()
            
            f = open("%s/Confidenceinterval_Left_Overhead" %Interval_Storage, 'a')
            f.write("%f," %Overhead_Confidence_leftside)
            f.close()
            
            f = open("%s/Confidenceinterval_Right_Overhead" %Interval_Storage, 'a')
            f.write("%f," %Overhead_Confidence_rightside)
            f.close()
                
                
            #Write to file - Is currently placed in the upper folder as in Results/{Protocol}/{Test_type} where the tests run for that configuration are placed.
            #Test_type could here be a specific amount of nodes.
            f = open("%s/Statistic data.txt" %( test_navn), 'a')
            f.write("\n############################ Data for test %s ###########################\n" %node_count)
            f.write("Average Delay in milliseconds %s\nStandard deviation %s\nWorstcase %s\n" % (DelayAverage, Delay_Variation, Worst_delay))
            f.write("Confidence interval was %f < theta >%f\n \n" % (Delay_Confidence_leftside, Delay_Confidence_rightside))
            f.write("Average Overhead in Percent %s\nStandard deviation %s\nWorstcase %s\n" % (OverheadAverage, Overhead_Variation, Worst_Overhead))
            f.write("Confidence interval was %f < theta >%f\n \n" % (Overhead_Confidence_leftside, Overhead_Confidence_rightside))
            f.write("Average droprate in percent %s\nStandard deviation %s\nWorstcase %s\n" % (DroprateAverage, Droprate_Variation, Worst_Droprate))
            f.write("Confidence interval was %f < theta >%f\n \n" % (Droprate_Confidence_leftside, Droprate_Confidence_rightside))
            f.close()

            

            



statistic()
