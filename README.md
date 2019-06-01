# MySimulation
Simulation of a day in Magic Kingdom using Python

DEFINITIONS   
	iNumPeople -- Number of people to enter the park today.   
	bEnableConsole -- If true, output goes to console. If false, output goes to file.   
	bSuperMain -- If true, run the simulation multiple times with increasing number of people.    
	iSuperTimes -- How many times to run the simulation when bSuperMain is true.    
	iSuperMax -- The upper bound of people when bSuperMain is true.   
	iSuperMin -- The lower bound of people when bSuperMain is true.   
	iSuperIncrement -- How much to increment the number of people by when bSuperMain is true.   

FILES   
INCLUDED FILES -- All of these are needed to run the program. Store in same directory.
	Project_v002.alpha.py -- The python script
	p.arriveData.txt -- list of average arrival times needed to generate random arrival times for simulated day.
	p.name_list.txt -- List of random names for cosmetic purposes.
	p.rideData.txt -- List of data about Magic Kingdom
PROGRAM-GENERATED FILES
	project.log.txt -- Log data for simulated day
		Column Key:
			Time[minutes], personID, personEnergy, lineSizeAtLocation, LocationPersonIsAt, (for each ride: total times ridden), queSizeForDay
	project.log.super.txt -- Log data for multiple simulated days
		Column Key:
			AvgRidesRidden, (for each ride: avg wait time)

WHAT THIS PROGRAM DOES    
This program uses pRNG to create an Event Driven Simulation of Magic Kindom, Disney World.
First, Rejection Sampling is used with p.arriveData to determine when everyone will enter the park on the given day.
Then, All of the people are created.  People will weigh varying amounts based on a qaussian curve and this effects their energy levels throughout the day.
Now the Events begin. People start to enter the park.
People will decide what ride to go to based partially on RNG, and partially on formula. There is a chance, they might go to the closest ride, they might go to the ride with the shortest line, or they might just pick a random ride.
Once all of the people have entered and exited the park, the simulation ends.

HOW TO USE
	1)  edit Definitions as desired
	2)  run Project_v002.alpha.py
	3)  wait until finished.  This will take a while
	4)  interpret log files

Warning: takes a LONG time to run!!!
