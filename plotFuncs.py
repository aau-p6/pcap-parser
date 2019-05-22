#!/usr/bin/env python

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def readAndPlotConf(plotNum,filePathX,filePathLeft,filePathRight,outputName):
    xData = []
    leftData = []
    rightData = []
    myFile = open(filePathX,"r")
    for line in myFile:
        fields = line.split(",")
    for var in range(len(fields)):
        xData.append(fields[var]) 
    myFile.close()
    xData = list(map(float, xData))
    xData = list(map(int, xData))

    myFile = open(filePathLeft,"r")
    for line in myFile:
        fields = line.split(",")
    for var in range(len(fields)):
        leftData.append(fields[var]) 
    myFile.close()
    leftData = list(map(float, leftData))
    leftData = list(map(int, leftData))

    myFile = open(filePathRight,"r")
    for line in myFile:
        fields = line.split(",")
    for var in range(len(fields)):
        rightData.append(fields[var]) 
    myFile.close()
    #for x in leftDelay2:
        #leftDelay2[x].rstrip('\n')
    rightData = list(map(float, rightData))
    rightData = list(map(int, rightData))

    print(leftData)
    plotConfidence(plotNum,xData,leftData,rightData,1,outputName,"someting x-axis","something y-axis")

def readAndPlotHist(plotNumber,dataPath,wantedBins,outputHistName):
    histData = []
    myFile = open(dataPath,"r")
    for line in myFile:
        fields = line.split(",")
    for var in range(len(fields)):
        histData.append(fields[var]) 
    myFile.close()
    #for x in leftDelay2:
        #leftDelay2[x].rstrip('\n')
    histData = list(map(float, histData))
    histData = list(map(int, histData))

    plotHistogram(plotNumber,histData,wantedBins,outputHistName,"end-to-end delay","amount")

def plotHistogram(figNumHis,dataSet,binAmount,fileNameHist,xAxis,yAxis):
#End to end delay plots
    plt.figure(figNumHis)
    histogram_delay = plt.hist(dataSet,bins=binAmount)

    histogram_delay = plt.xlabel(xAxis)

    histogram_delay = plt.ylabel(yAxis)

    plt.savefig('/home/jonas/Documents/p6/{}.png'.format(fileNameHist)) #Write the path where you want to save the figure here
    print("Following Histogram saved: {}.png \n".format(fileNameHist))
    plt.show()

def plotConfidence(figNumConf,x_interval,left_side,right_side,middle,fileNameConf,x_Axis,y_Axis): 
    sortedLeft = [x for _,x in sorted(zip(x_interval,left_side))]
    sortedRight = [x for _,x in sorted(zip(x_interval,right_side))]
    plt.figure(figNumConf)
    plt.xlabel(x_Axis)
    plt.ylabel(y_Axis)
    plt.plot(sorted(x_interval),sortedLeft,label = "Left confidence",linestyle='dashed')
    #plt.plot(sorted(x_interval),middle,label = "Average",linestyle='solid')
    plt.plot(sorted(x_interval),sortedRight,label = "Right confidence",linestyle='dashed')
    plt.legend()
    plt.savefig('/home/jonas/Documents/p6/{}.png'.format(fileNameConf)) #Write the path where you want to save the figure here

    print("Following Confidenceplot saved: {}.png \n".format(fileNameConf))
    plt.show()   


readAndPlotConf(1,"/home/jonas/Desktop/SignalStrenghtfixedfiles/fixedfiles/X.txt","/home/jonas/Desktop/SignalStrenghtfixedfiles/fixedfiles/Confidenceinterval_Left_Delay.txt","/home/jonas/Desktop/SignalStrenghtfixedfiles/fixedfiles/Confidenceinterval_Right_Delay.txt","collectedConfidence")

readAndPlotHist(2,"/home/jonas/Desktop/Results/Histogramdata/OLSR20HistogramDelay.txt",40,'newHistogram')