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
def GetMyPoints():
    for files in Files:
        fileOrder.append(files)
        abf = pyabf.ABF("Data/"+files)
        for chN in range(abf.channelCount):
            ChannelOrder.append(chN)
            peaksAnddips = [[],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
            abf.setSweep(sweepNumber=0, channel=chN)
            plt.plot(abf.sweepX, abf.sweepY)
            listy = abf.sweepY
            listx = abf.sweepX
            fSlope = float(input("please input first slope : ) : "))
            FPX  = float(input("please First time : ) :"))
            FDX  = float(input("please second time : ) :"))
            print(str(files)+" Running")
            LPX = FPX-90
            LDX = FDX-90
            x = 0
            pos=1010
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
                        pos += 1250
                    if x == 28:
                        for c in range(25910, 26095):
                            if listy[(c-1)] <= listy[c] >= listy[(c+1)]:
                                y[0].append(c)
                            #dip
                            if listy[(c-1)] >= listy[c] <= listy[(c+1)]:
                                y[1].append(c)
                    if x == 29:
                        for c in range(55910, 56100):
                            if listy[(c-1)] <= listy[c] >= listy[(c+1)]:
                                y[0].append(c)
                            #dip
                            if listy[(c-1)] >= listy[c] <= listy[(c+1)]:
                                y[1].append(c)
                    x += 1
                else:
                    y.append(fSlope)
                    x += 1


            #top section done

            addi = 0
            for d in range(30):
                if not d == 0:
                    if d < 21:
                        Tslopes =[]
                        Lslopes = []
                        bc = 100000
                        for o in peaksAnddips[d][0]:
                            for m in peaksAnddips[d][1]:
                                if o < m:
                                    Tslopes.append(((listy[m] - listy[o])/(1000*(listx[m] - listx[o]))))
                                    cpeak = ((o/10)-((10*d)+90))
                                    #dip
                                    cdip = ((m/10)-((10*d)+90))
                                    Lslopes.append([cdip,cpeak])
                        for sp in range(len(Lslopes)):
                            cs = Tslopes[sp]
                            cdip = Lslopes[sp][0]
                            cpeak =Lslopes[sp][1]
                            if cdip < LDX:
                                dval = (1 - abs((cdip/LDX)))
                            else:
                                dval = (abs((cdip/LDX)) - 1)
                            if cpeak < LPX:
                                pval = (1 - abs((cpeak/LPX)))
                            else:
                                pval = (abs((cpeak/LPX)) - 1)
                            disval = (dval + pval)
                            PC = disval
                            if PC < bc and cs < 0:
                                bc = PC
                                bcdip = cdip
                                bcpeak = cpeak
                                BestSlope = cs

                        plt.axvline(x = listx[int((((bcdip+(d*10)+90)*10)))], color = 'b')
                        plt.axvline(x = listx[int((((bcpeak+(d*10)+90)*10)))], color = 'b')
                        resultSlopes.append(BestSlope)
                    else:

                        Tslopes =[]
                        Lslopes = []
                        bc = 100000
                        for o in peaksAnddips[d][0]:
                            for m in peaksAnddips[d][1]:
                                if o < m and listy[o] > listy[m]:

                                    Tslopes.append(((listy[m] - listy[o])/(1000*(listx[m] - listx[o]))))
                                    if d < 28:
                                        cdip = ((m/10) - ((125*(d-21))+(716)))
                                        cpeak = ((o/10) - ((125*(d-21))+(716)))
                                        Lslopes.append([cdip,cpeak])
                                    else:
                                        if d == 28:
                                            cdip = ((m/10) - (2590))
                                            cpeak = ((o/10) - (2590))
                                            Lslopes.append([cdip,cpeak])
                                        else:
                                            cdip = ((m/10) - (5590))
                                            cpeak = ((o/10) - (5590))
                                            Lslopes.append([cdip,cpeak])
                        for sp in range(len(Tslopes)):

                            cs = Tslopes[sp]
                            cdip = Lslopes[sp][0]
                            cpeak =Lslopes[sp][1]
                            if cdip < LDX:
                                dval = (1 - abs((cdip/LDX)))
                            else:
                                dval = (abs((cdip/LDX)) - 1)
                            if cpeak < LPX:
                                pval = (1 - abs((cpeak/LPX)))
                            else:
                                pval = (abs((cpeak/LPX)) - 1)
                            disval = (dval + pval)
                            PC = disval
                            if PC < bc and cs < 0:
                                bc = PC
                                bcdip = cdip
                                bcpeak = cpeak
                                BestSlope = cs
                        LS = BestSlope
                        resultSlopes.append(BestSlope)
                        if d < 28:
                            plt.axvline(x = listx[int(((bcdip+((125*(d-21))+(716)))*10))], color = 'b')
                            plt.axvline(x = listx[int((((bcpeak+((125*(d-21))+(716)))*10)))], color = 'b')
                        else:
                            if d == 28:
                                plt.axvline(x = listx[int(((bcdip+(2591))*10))], color = 'b')
                                plt.axvline(x = listx[int(((bcpeak+(2591))*10))], color = 'b')
                            else:
                                plt.axvline(x = listx[int(((bcdip+(5591))*10))], color = 'b')
                                plt.axvline(x = listx[int(((bcpeak+(5591))*10))], color = 'b')
                    addi += 100
                else:
                    resultSlopes.append(peaksAnddips[0][0])
                    OG = resultSlopes[0]
                    LS = OG

            print(files+" finished")
            plt.show()
            FinalSlopes.append(resultSlopes)
def toExcel():
    DataFrame = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],fileOrder,ChannelOrder]
    for x in range(30):
        for eachfile in FinalSlopes:
            DataFrame[x].append(eachfile[x])
    pd.DataFrame(DataFrame).to_excel('Slopes.xlsx', sheet_name="Slopes", index=False)


GetMyPoints()
toExcel()

