from queue import Empty
import pyabf
import pyabf.filter
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
import pandas as pd

#All the files I will be analysing
Files = listdir(path="Data")
FinalSlopes = []
fileOrder = []
ChannelOrder = []
#peaksAnddips = [[],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
#peaks will be one dips will be 2 associated position number will be position -1 in list
def GetMyPoints():
    for files in Files:
        fileOrder.append(files)
        abf = pyabf.ABF("Data/"+files)
        for chN in range(abf.channelCount):
            ChannelOrder.append(chN)
            peaksAnddips = [[],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
            pyabf.filter.gaussian(abf, .1, channel=chN)
            abf.setSweep(sweepNumber=0, channel=chN)
            listy = abf.sweepY
            listx = abf.sweepX
            fSlope = float(input("please input first slope : ) : "))
            x = 0
            pos=910
            resultSlopes =[]
            for y in peaksAnddips:
                if not x == 0:
                    if x < 21:
                        for c in range(pos, pos+100):
                            #peak
                            if listy[(c-1)] <= listy[c] >= listy[(c+1)]:
                                y[0].append(c)
                            #dip
                            if listy[(c-1)] >= listy[c] <= listy[(c+1)]:
                                y[1].append(c)
                        print(x)
                        pos += 100
                    if x == 20:
                        pos = 7160
                    if x >20 and x < 28:
                        for c in range(pos, pos+200):
                            if listy[(c-1)] <= listy[c] >= listy[(c+1)]:
                                y[0].append(c)
                            #dip
                            if listy[(c-1)] >= listy[c] <= listy[(c+1)]:
                                y[1].append(c)
                        print(x)
                        pos += 1250
                    if x == 28:
                        for c in range(25910, 26095):
                            if listy[(c-1)] <= listy[c] >= listy[(c+1)]:
                                y[0].append(c)
                            #dip
                            if listy[(c-1)] >= listy[c] <= listy[(c+1)]:
                                y[1].append(c)
                        print(x)
                    if x == 29:
                        for c in range(55910, 56100):
                            if listy[(c-1)] <= listy[c] >= listy[(c+1)]:
                                y[0].append(c)
                            #dip
                            if listy[(c-1)] >= listy[c] <= listy[(c+1)]:
                                y[1].append(c)
                        print(x)
                    x += 1  
                else:
                    y.append(fSlope)
                    x += 1


            #top section done


            for d in range(30):
                if not d == 0:
                    if d < 21:
                        print(d)
                        Tslopes =[]
                        bc = 100000
                        for o in peaksAnddips[d][0]:
                            for m in peaksAnddips[d][1]:
                                if o < m:
                                    Tslopes.append(((listy[m] - listy[o])/(1000*(listx[m] - listx[o]))))
                        for X in Tslopes:
                            if X < LS:
                                PC = (abs((X/LS)) - 1)
                                if PC < bc :
                                    bc = PC
                                    BestSlope = X
                                    #print(BestSlope)
                            else:
                                PC = (1-abs((X/LS)))
                                if PC < bc:
                                    bc = PC
                                    BestSlope = X
                                    #print(BestSlope)

                        LS = BestSlope
                        resultSlopes.append(BestSlope)
                    else:
                        print(d)
                        Tslopes =[]
                        bc = 100000
                        for o in peaksAnddips[d][0]:
                            for m in peaksAnddips[d][1]:
                                if o < m and listy[o] > listy[m]:
                                    #if d == 22:
                                    #    print(m)
                                    #    print(o)
                                    #    print(((listy[m] - listy[o])/(1000*(listx[m] - listx[o]))))
                                    #    print("dip")
                                    #    print(listx[m])
                                    #    print("peak")
                                    #    print(listx[o])
                                    Tslopes.append(((listy[m] - listy[o])/(1000*(listx[m] - listx[o]))))
                        for X in Tslopes:
                            if X < OG:
                                PC = (abs((X/OG)) - 1)
                                if PC < bc :
                                    bc = PC
                                    BestSlope = X
                                    #print(BestSlope)
                            else:
                                PC = (1-abs((X/OG)))
                                if PC < bc:
                                    bc = PC
                                    BestSlope = X
                                    #print(BestSlope)
                        LS = BestSlope
                        resultSlopes.append(BestSlope)

                else:
                    resultSlopes.append(peaksAnddips[0][0])
                    OG = resultSlopes[0]
                    LS = OG

            print(peaksAnddips)
            FinalSlopes.append(resultSlopes)
def toExcel():
    DataFrame = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],fileOrder,ChannelOrder]
    for x in range(30):
        for eachfile in FinalSlopes:
            DataFrame[x].append(eachfile[x])
    pd.DataFrame(DataFrame).to_excel('Slopes.xlsx', sheet_name="Slopes", index=False)
            

GetMyPoints()
toExcel()
