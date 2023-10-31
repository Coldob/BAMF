import pyabf
import pyabf.filter
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
import pandas as pd

#All the files I will be analysing
Files = listdir(path="Data")
slopeList = []
FileDataFrame = []
ChannelDataFrame = []
ErrorDataFrame = []
#all the data 
def GetMyPoints():
    for files in Files:
        abf = pyabf.ABF("Data/"+files)
        for ChN in range(abf.channelCount):
            pyabf.filter.gaussian(abf, .5, channel=ChN)
            abf.setSweep(sweepNumber=0, channel=ChN)
            listy = abf.sweepY
            listx = abf.sweepX
            ErrorCheck = False
            ErrorPoints = []
            #this number can change on protocol
            y = 900
            peakList = []
            dipList = []
            # first set of 21 points
            while y < 2990:
                MinorPeaks = []
                MinorDips = []
                for x in range(y, (y+100)):
                    if listy[(x-1)] <= listy[x] >= listy[(x+1)]:
                        MinorPeaks.append(x)
                    if listy[(x-1)] >= listy[x] <= listy[(x+1)]:
                        if not (len(MinorPeaks) == 0):
                            #attempt to get rid of positive slopes^
                            MinorDips.append(x)
                if len(MinorPeaks) > 1:
                    peakList.append(MinorPeaks[1])
                else:
                    peakList.append(MinorPeaks[0])
                    ErrorCheck = True
                    ErrorPoints.append(len(peakList))
                if len(MinorDips) > 1:
                    dipList.append(MinorDips[1])
                else:
                    dipList.append(MinorDips[0])
                    ErrorCheck = True
                    ErrorPoints.append(len(dipList))
                y += 100
            # Middle spaced points 6 mid sections total
            y = 7150
            while y < 14778:
                MinorPeaks = []
                MinorDips = []
                for x in range(y, (y+1250)):
                    if listy[(x-1)] <= listy[x] >= listy[(x+1)]:
                        MinorPeaks.append(x)
                    if listy[(x-1)] >= listy[x] <= listy[(x+1)]:
                        if not (len(MinorPeaks) == 0):
                            MinorDips.append(x)
                if len(MinorPeaks) > 1:
                    peakList.append(MinorPeaks[1])
                else:
                    peakList.append(MinorPeaks[0])
                    ErrorCheck = True
                    ErrorPoints.append(len(peakList))
                if len(MinorDips) > 1:
                    dipList.append(MinorDips[1])
                else:
                    dipList.append(MinorDips[0])
                    ErrorCheck = True
                    ErrorPoints.append(len(dipList))
                y += 1250
                #below could just be written as loop
            MinorPeaks = []
            MinorDips = []
            for x in range(25900, 25986):
                if listy[(x-1)] <= listy[x] >= listy[(x+1)]:
                    MinorPeaks.append(x)
                if listy[(x-1)] >= listy[x] <= listy[(x+1)]:
                        if not (len(MinorPeaks) == 0):
                            MinorDips.append(x)
            if len(MinorPeaks) > 1:
                peakList.append(MinorPeaks[1])
            else:
                peakList.append(MinorPeaks[0])
                ErrorCheck = True
                ErrorPoints.append(len(peakList))
            if len(MinorDips) > 1:
                dipList.append(MinorDips[1])
            else:
                dipList.append(MinorDips[0])
                ErrorCheck = True
                ErrorPoints.append(len(dipList))
            MinorPeaks = []
            MinorDips = []
            for x in range(55900, 56020):
                if listy[(x-1)] <= listy[x] >= listy[(x+1)]:
                    MinorPeaks.append(x)
                if listy[(x-1)] >= listy[x] <= listy[(x+1)]:
                    if not (len(MinorPeaks) == 0):
                        MinorDips.append(x)
            if len(MinorPeaks) > 1:
                peakList.append(MinorPeaks[1])
            else:
                peakList.append(MinorPeaks[0])
                ErrorCheck = True
                ErrorPoints.append(len(peakList))
            if len(MinorDips) > 1:
                dipList.append(MinorDips[1])
            else:
                dipList.append(MinorDips[0])
                ErrorCheck = True
                ErrorPoints.append(len(dipList))
            slope = []
            try:
                for x in range(30):
                    print("file: " +files+ "channel: "+str(ChN))
                    print(listy[dipList[x]])
                    print("-")
                    print(listy[peakList[x]])
                    print("/")
                    print(listx[dipList[x]])
                    print("-")
                    print(listx[peakList[x]])
                    slope.append(((listy[dipList[x]] - listy[peakList[x]])/(1000*(listx[dipList[x]] - listx[peakList[x]]))))
                slopeList.append(slope)
                FileDataFrame.append(files)
                ChannelDataFrame.append(ChN)
                ErrorDataFrame.append(ErrorPoints)
                #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #if ErrorCheck == True:
                #    print("Possible error on points listed")
                #    print(ErrorPoints)
                #print("Slopes for File: "+files)
                #print("Channel Number: "+str(ChN))
                #for x in slope:
                #    print(x)
                #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            except Exception as e:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("Error with File: "+files)
                print("Channel Number: "+str(ChN))
                print(e)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
def toExcel():
	DataFrame = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],FileDataFrame,ChannelDataFrame,ErrorDataFrame,]
	for x in range(30):
		for eachFile in slopeList:
			DataFrame[x].append(eachFile[x])
	#print(DataFrame)
	pd.DataFrame(DataFrame).to_excel('Slopes.xlsx', sheet_name="Slopes", index=False)
def GraphIt():
	FileN = input("File Number: ")
	ChannelN = input("Channel Number: ")
	abf = pyabf.ABF("Data/"+str(FileN)+".abf") 
	abf.setSweep(sweepNumber=0, channel=int(ChannelN))
	plt.plot(abf.sweepX, abf.sweepY, alpha=.3, label="original")
#
	pyabf.filter.gaussian(abf, .5, channel=int(ChannelN))  # apply custom sigma
	abf.setSweep(sweepNumber=0, channel=int(ChannelN))  # reload sweep with new filter
#
	plt.plot(abf.sweepX, abf.sweepY, alpha=.8, label='label')



	plt.show()
check = True
while check:
	command = input(":")
	eval(command + "()")
	if command == 'quit':
		check = False
#print(slopeList)
#print(len(slopeList))
