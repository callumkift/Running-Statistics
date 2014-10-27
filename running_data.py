##########
#
# This script was created so that a runner can gain
# more insights into their runs. 
#
# Creator: Callum Kift
# email: callumkift@gmail.com
#
##########
import os.path
import re
from datetime import date, time
from array import array

# Defining variables
dateArray = []
distanceArray = []
timeArray = []


def AddRun():
	add_run = raw_input("Do you want to add a new run? (y/n)\n")
	if (add_run == "y" or add_run == "Y"):
		#print "yes detected"
		GetFile()

def ViewStats():
	view_stats = raw_input("\nDo you want to view your stats? (y/n)\n")
	if (view_stats == "y" or view_stats == "Y"):
		ReadData()

def GetFile():
	### Check's to see if file exists
	if (os.path.isfile("past_runs.txt")):
		#print "file exists"
		RunInfo("previous")
	else:
		#print "This seems to be your first run - congratulations."
		RunInfo("new")
	return

def RunInfo(a):
	### User inputs data and it writes to file
	if (a == "previous"):
		f = open("past_runs.txt", "a") # opens and appends to file
	elif (a == "new"):
		f = open("past_runs.txt", "w")
		f.write("DATE (DD/MM/YYYY) | " + "DISTANE (KM) | " + "TIME (HH:MM:SS) \n")
		f.write("--------------------------------------------------\n")
		f.write("\n")

	run_date = raw_input("\nWhat was the date of the run? (DD/MM/YYYY)\n")
	run_distance = raw_input("\nHow far did you run? (km)\n")
	run_time = raw_input("\nHow long did you run for? (HH:MM_SS)\n") 

	f.write(run_date + " " + run_distance + " " + run_time + "\n") 
	f.close
	return

def ReadData():
	if (os.path.isfile("past_runs.txt")):
		f = open("past_runs.txt", "r")
		column_title = f.readline()
		underline = f.readline()
		blank_line = f.readline()
		for line in f:
				line = line.strip() 
				column = re.split(" |/|:", line)
				if (len(column) == 7):
					dateArray.append(date(int(column[2]), int(column[1]), int(column[0])))
					distanceArray.append(float(column[3]))
					timeArray.append(time(int(column[4]), int(column[5]), int(column[6]),0))
		# print "Data read", len(distanceArray)
	else:
		print "\n-- It seems that you have no previous runs saved."
		print "--",
		AddRun()
		ViewStats()
	return

def CalculateTotal():
	totDist = 0
	totRuns = 0
	for i in range(len(distanceArray)):
		totDist += distanceArray[i]
		totRuns += 1
	avgDist = totDist/totRuns
	return totDist, totRuns, avgDist



			
if __name__ == '__main__':

	print "----------------------------------"
	print "Welcome to your running statistics"
	print "----------------------------------\n"

	# Defining variables
	dateArray = []
	distanceArray = []
	timeArray = []

	AddRun()
	ViewStats()

	print "\n----------------------------------"
	print "----------------------------------"
	print "----------- STATISTICS -----------"
	print "----------------------------------"
	print "----------------------------------\n\n"

	totalDistance, numberOfRuns, averageDistance = CalculateTotal()

	print "Total distance: %.2fkms" %totalDistance
	print "You have ran a total of %d times" %numberOfRuns
	print "Meaning you run an average of %.2fkms" %averageDistance


