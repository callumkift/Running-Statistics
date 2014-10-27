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
from datetime import date, time, timedelta
from array import array
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

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
	totTime = 0
	for i in range(len(distanceArray)):
		totDist += distanceArray[i]
		totRuns += 1
		totTime += Hour2Seconds(timeArray[i])
		
	avgDist = totDist/totRuns
	return totDist, totRuns, avgDist, Seconds2Hours(totTime)

def Hour2Seconds(fullTime):
	secs = fullTime.second
	mins = fullTime.minute
	hours = fullTime.hour
	totalSeconds = secs + (mins*60) + (hours*3600)
	return totalSeconds

def Seconds2Hours(secs):
	hour = int(secs/3600)
	minutes = secs%hour
	seconds = minutes%60
	timeform = time(hour, minutes, seconds, 0)
	return timeform

def ThisMonth():
	#today = datetime.date.today()
	monthDate = []
	monthDistance = []
	monthTime = []

	# monthTotDist = 0
	# monthTotTime = time(0, 0, 0, 0)

	#print "poo", monthTotTime

	for i in range(len(dateArray)):
		if (date.today().month == dateArray[i].month):
			monthDate.append(dateArray[i])
			monthDistance.append(distanceArray[i])
			monthTime.append(timeArray[i])

			# monthTotDist += distanceArray[i]
			# monthTotTime += timedelta(timeArray[i].hour, timeArray[i].minute, timeArray[i].second, 0)

	dates = [date2num(day) for day in monthDate]
	#dates = [datetime.strptime(str(int(day)),'%Y%m%d') for day in monthDate]
	plt.plot(dates, monthDistance, 'bo')
	plt.title(r'This months runs')
	plt.xlabel(r'Date')
	plt.ylabel(r'Distance')
	plt.show()

	#print monthTotTime, monthTotDist
	return



			
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

	totalDistance, numberOfRuns, averageDistance, totalRunTime = CalculateTotal()

	print "You have run a total distance of %.2fkms" %totalDistance
	print "You have run a total of %d times" %numberOfRuns
	print "You have run for a total time of", totalRunTime
	print "You run an average of %.2fkms" %averageDistance

	ThisMonth()
