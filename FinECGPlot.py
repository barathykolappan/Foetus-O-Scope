import pygame
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

dataset = pd.read_csv("data3.csv")
pygame.mixer.init()
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
plt.ylim(0,800)
plt.xlim(0,2500)
plt.title("Imposition")
plt.plot(dataset)
plt.show()
hrw = 0.75
fs = 100
mov_avg_mom = dataset['mheart'].rolling(int(hrw*fs)).mean()
mov_avg_baby = dataset['bheart'].rolling(int(hrw*fs)).mean()
mov_avg_final=(mov_avg_mom+mov_avg_baby)/2

mavg_hr = (np.mean(dataset.mheart))
mov_avg_mom = [mavg_hr if math.isnan(x) else x for x in mov_avg_mom]
mov_avg_mom = [x*1.2 for x in mov_avg_mom]

bavg_hr = (np.mean(dataset.bheart))
mov_avg_baby = [bavg_hr if math.isnan(x) else x for x in mov_avg_baby]
mov_avg_baby = [x*1.2 for x in mov_avg_baby]

dataset['mheart_rollingmean'] = mov_avg_mom
dataset['bheart_rollingmean'] = mov_avg_baby

plt.ylim(0,800)
plt.xlim(0, 500)
plt.title("Moving Average")
plt.plot(mov_avg_mom, color ='blue')
plt.plot(mov_avg_baby, color ='orange')
plt.show()

plt.ylim(300,400)
plt.xlim(0,500)
plt.title("Baby Cumulative")

dataset['mov_avg_final_rollingmean'] = mov_avg_final
plt.plot(mov_avg_final, color ='red')
plt.show()

favg_hr = (np.mean(dataset.bheart))
mov_avg_final = [favg_hr if math.isnan(x) else x for x in mov_avg_final]
mov_avg_final = [x*1.2 for x in mov_avg_final]

mov_avg_final

dataset['heart_rollingmean'] = mov_avg_final #Moving Average append to DF
#ROI Markings
window = []
listofpeaks = []
listpos = 0 #Counters to move over cols
for datapoint in dataset.bheart:  
    rollingmean = dataset.heart_rollingmean[listpos]
    if (datapoint < rollingmean) and (len(window) < 1):#RComplex Tracker
        listpos += 1
    elif (datapoint > rollingmean): #>local mean, mark ROI
        window.append(datapoint)
        listpos += 1
    else: #<local mean, determine highest point
        maximum = max(window)
        beatposition = listpos - len(window) + (window.index(max(window)))#Xaxis Point
        listofpeaks.append(beatposition) #Add detected peak to list
        window = [] #clear marked ROI
        listpos += 1

RR_list = []
cnt = 0

while (cnt < (len(listofpeaks)-1)):
    RR_interval = (listofpeaks[cnt+1] - listofpeaks[cnt]) 
#Calculate distance between beats in # of samples
    ms_dist = ((RR_interval / fs) * 1000.0) #Convert sample distances to ms distances
    RR_list.append(ms_dist) #Append to list
    cnt += 1
    
bpm = 60000 / np.mean(RR_list) #60000 ms (1 minute) / average R-R interval of signal

print("Avg Heart Beat is: %.01f" %bpm)

channel1.set_volume(0.4)
channel1.play(pygame.mixer.Sound('FinalWhiteNoise.wav'), loops=1000)
channel2.set_volume(1)
for i in range(int(len(listofpeaks)/3)):
    channel2.play(pygame.mixer.Sound('FinalLubDub.wav'))
    time.sleep(72/160)
channel1.stop() 