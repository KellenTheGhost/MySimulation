# python3
import datetime
import queue
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas

###############################################################################
# Definitions

bConsoleOutput = True   # Output to console vs output to file
iNumPeople = 15000   # Number of people to come to the park on a given day
iBins = 200     # Number of bins for generating pdf of arrival data
                # More bins = more precise numbers, takes WAY longer

##overrides everything for multiple simulations
bSuperMain = True   # Run multiple days, each with iSuperIncrement more people than the last
iSuperTimes = 30   # How many days to run

## Used for finding the 'magic number' of people per day
iSuperMax = 16000   # Max number of people to enter the park on any day
iSuperMin = 14000
iSuperIncrement = 10    # How much each day should increment people by

###############################################################################
# Output to File
def loadFile():
    f = open("project.console.txt",'w')
    f.write("Simulation ran on:  " + str(datetime.datetime.now())+'\n')
    return f

def makeLog():
    f = open('project.log.txt','w')
    return f

def makeLogSuper():
    f = open('project.log.super.txt','w')
    return f

def loadArriveData():
    ad = open('p.arriveData.txt','r')
    if(gateCloses - parkOpens > 840):
        print('The Park is open too long.  Change the time to be less than 14 hours.')
        return None
    adl = [(float(i)*60 - (parkOpens-480)) for i in ad.read().splitlines()]
    ad.close()
 
    n,bin,patch=plt.hist(adl,iBins,density=1)#Observed
    plt.close()
    return n,bin,patch

###############################################################################
# park data
#all attractions at Magic Kingdom, Disney World, USA
loc = []
#time between cars
carTime = []
#number of people in each car
rideSize = []
#closest ride to current ride
closestRide = []
#time to ride ride
rideTime = []

#time park opens
parkOpens = 540 #9am
#time gate closes
gateCloses = 1080 #6pm
#time park closes 
parkCloses = 1085 #6:05pm give 5 minutes for people to finish current event

#current number of people in each line
lineSize = []
#total number of people who rode each ride
timesRidden = []
waitTimes = []

#fill above lists with data from 'p.RideData.txt'
def loadParkData():
    global loc
    global carTime
    global rideSize
    global closestRide
    global rideTime
    f = open('p.rideData.txt','r')
    df = pandas.read_csv(f,delimiter='\t')
    loc = df['Location'].tolist()
    carTime = df['CarTime'].tolist()
    rideSize = df['RideSize'].tolist()
    closestRide = df['ClosestRide'].tolist()
    rideTime = df['RideTime'].tolist()
    resetParkData()
        
def resetParkData():
    global lineSize
    global timesRidden
    global waitTimes
    lineSize.clear()
    timesRidden.clear()
    waitTimes.clear()
    for x in range(len(loc)):
        lineSize.append(0)
        timesRidden.append(0)
        waitTimes.append(0)
            
def printTimes():
    string = ''
    string += str(timesRidden[0]) + ' people entered the park.\n'
    string += str(timesRidden[1]) + ' people exited the park.\n'
    for x in range(2,len(loc)):
        string += '\'' + loc[x] + '\' was ridden ' + str(timesRidden[x]) + ' times.\n'
    return string

def printAverages():
    string = ''
    for x in range (2,len(loc)):
        string += '\'{}\' had an average waiting time of {:.2f}\n'.format(loc[x],waitTimes[x]/timesRidden[x])
    return string

def logTimes():
    string = ''
    for x in range(len(loc)):
        string += str(timesRidden[x]) + '\t'
    return string

def logAverages():
    string = ''
    for x in range (2,len(loc)):
        string += str('{:.2f}\t'.format(waitTimes[x]/timesRidden[x]))
    return string

###############################################################################
# Name Generator
# Entrirely Cosmetic
nameList = []
def loadNameList():
    global nameList
    f = open('p.name_list.txt','r')
    nameList = nameList + f.read().splitlines()
    f.close()
    
def genName():
    ind = rng.randint(0,len(nameList)-1)
    return nameList[ind]

###############################################################################
# Weight Generator
def genWeight():
    ##get weight data for area near park
    ##normal m=161.8 s=1.88
    return math.ceil(rng.normal(161.8,1.88))

###############################################################################
# Create RNG
seed = 0
rng = 0
def genRNG():
    global seed
    global rng
    seed = np.random.randint(0,2147483647)
    rng = np.random.RandomState()
    rng.seed(seed)

###############################################################################
# person class
personContainer = []  
class person(object):
    def __init__(self, id, name, weight):
        self.id = id
        self.name = name
        self.weight = weight
        self.location = -1
        self.energy = 100
        self.time = 0
        self.numRides = 0
        
    def nextRide(self,location,time):
        self.location = location
        self.time = time
        
    def detEnergy(self):
        if(self.location > 1):
            self.energy -= math.ceil( ((self.weight / 100 - 1)**2 + 1) \
                * (self.time / (10 if self.time < 100 else 100)) )
        
    def print(self):
        if(self.location == -1):
            return '#' + str(self.id) + ':\t' + str(self.name) + ' [' \
                + str(self.weight) + ',' + str(self.energy) \
                + '] arrived'
        else:
            return '#' + str(self.id) + ':\t' + str(self.name) + ' [' \
                + str(self.weight) + ',' + str(self.energy) \
                + '] is at ' + str(loc[self.location])
    
    def log(self):
        if(self.location == -1):
            return str(self.id) + '\t' + str(self.energy) + '\t' \
                + str(lineSize[self.location]) + '\t' \
                + 'arrived'
        else:
            return str(self.id) + '\t' + str(self.energy) + '\t' \
                + str(lineSize[self.location]) + '\t' \
                + str(loc[self.location])
    
###############################################################################
# Determine Next Ride to go to
def nextRide(location,energy):
    if(location == -1): #if at entrance go to gate
        lineSize[0] += 1
        return 0
    if(energy <= 0):
        return 1 #go to exit to leave
    r = rng.random_sample()
    if(r >= 0.8): ##go to random ride
        ride = rng.randint(2,len(loc))
        lineSize[ride] += 1
        return ride
    elif(r < 0.3):   ## go to shortest line
        shortestRide = 2
        for x in range(2,len(lineSize)):
            if(lineSize[x] < lineSize[shortestRide]):
                shortestRide = x
        lineSize[shortestRide] += 1
        return shortestRide
    else:  ## go to closest ride
        ride = closestRide[location]
        lineSize[ride] += 1
        return ride
        
###############################################################################
# get line time
def lineTime(location):
    return carTime[location] * math.floor(lineSize[location] / rideSize[location])
    
###############################################################################
# custom List getindex
def pIndex(lst,item):
    for a in range(len(lst)):
        if item < lst[a+1]:
            return a
        
###############################################################################
# Driver
def main():
    global personContainer
    
    if (iNumPeople == 0): return 0
    if(len(nameList) < 2): 
        loadNameList()
        loadParkData()
        genRNG()
    else:
        resetParkData()
    
    if(not bSuperMain):  
        l = makeLog()
        if(bConsoleOutput): 
            print("RNG seed used: ", seed)
            print('Generating arrival times; please wait...')
        else: 
            f = loadFile()
            f.write("RNG seed used: %d\n\n"% seed)
    
    #rejection sampling to generate arrival data
    que = queue.PriorityQueue()
    n,bin,patch=loadArriveData()
    num = 0
    while (que.qsize() < iNumPeople):
        x = rng.random_sample()*(gateCloses-parkOpens)+parkOpens
        y = rng.random_sample()
        ind = pIndex(bin,x)
        if(ind == None): # something funky happened, 'x' is not in 'bin'
            continue
        if(y < n[ind]): # do not reject sample
            personContainer.append(person(num,genName(),genWeight()))
            que.put((x, personContainer[-1]))
            num += 1
        
    ##run queue, park closes at 2am
    worldClock = 0
    while( (not que.empty())  and worldClock < parkCloses ):
        next = que.get()
        p = next[1]
        worldClock = next[0]
        
        if(not bSuperMain): 
            if(bConsoleOutput): print(p.print() + ' at %0.2f' % worldClock)
            else: f.write(p.print()+ ' at %0.2f\n' % worldClock)
            l.write('%.2f\t'%worldClock)
            l.write(p.log()+'\t'+logTimes()+str(que.qsize())   +'\n')
            
        if(p.location != -1): 
            lineSize[p.location] -= 1
            timesRidden[p.location] += 1
            if(p.location > 1):
                p.numRides += 1
        p.detEnergy()
        loc = p.location
        nRide = nextRide(p.location,p.energy)
        if(loc == 1):
            continue
        elif(loc == -1):
            time = lineTime(nRide) 
            p.nextRide(nRide,time)
            que.put((worldClock + time, p))
        else:
            time = lineTime(nRide) 
            waitTimes[nRide] += time
            p.nextRide(nRide,time)
            que.put((worldClock + time + rideTime[loc], p))
            
    sum = 0        
    for peep in personContainer:
        sum += peep.numRides
    sum /= len(personContainer) 
       
    if(not bSuperMain):    
        if(bConsoleOutput): 
            print('\n%d people are still in the park at closing.'%que.qsize())
            print(printTimes(),end='')
            print('The average amount of rides ridden is %.2f rides.\n'%sum)
            print(printAverages(),end='')
        else: 
            f.write('\n%d people are still in the park at closing.\n'%que.qsize())
            f.write(printTimes())
            f.write('The average amount of rides ridden is %.2f rides.\n'%sum)
            f.write(printAverages(),end='')
            f.close()
        l.close()
    
    return sum
    
###############################################################################
# super driver for multiple simulations
def superMain():
    global iNumPeople
    global personContainer
    log = makeLogSuper()
    
    
    for x in range(iSuperTimes):
#        iNumPeople = ((x * iSuperIncrement) % (iSuperMax - iSuperMin)) \
#                + iSuperMin  #range: [iSuperMin, iSuperMax]
        
        personContainer.clear()

        s = main()
#        log.write('%d\t%.2f\t' % (iNumPeople,s))
        log.write('%.2f\t' % (s))
        log.write(logAverages())
        log.write('\n')
#        print('%d\t%.2f' % (iNumPeople,s),end='\t')
        print('%d\t%.2f' % (x,s),end='\t')
        print(logAverages())

    log.close()
   
###############################################################################
# run program.    
if(not bSuperMain):    
    main()
else:
    superMain()