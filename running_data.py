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
import matplotlib.dates as mdates


def AddRun():
	"""Asks user if they want to add a new run, if yes then it runs WriteRunToFile()"""
	add_run = raw_input("Do you want to add a new run? (y/n)\n")
	if (add_run == "y" or add_run == "Y"):
		#print "yes detected"
		WriteRunToFile()

def ViewStats():
	"""Asks user if they want to view their stats, if yes then it runs ReadData()"""
	view_stats = raw_input("\nDo you want to view your stats? (y/n)\n")
	if (view_stats == "y" or view_stats == "Y"):
		ReadData()


def WriteRunToFile():
	""""Runs when user wants to add a run to file. Finds the file and then asks the
		user to input data and writes to file. If it is their first run, then it will
		create the file before asking the user for their run data and writing it to
		file."""
	if (os.path.isfile("past_runs.txt")): # finds file and opens it
		f = open("past_runs.txt", "a") 
	else: # creates file if it doesn't exist
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
	"""Runs when user wants to see their stats. This reads the user's run info and 
		stores it in a list. If run when no data exists, it will ask user to add data
		before running again."""
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
		ReadData()
	return

def CalculateTotal():
	"""This calculates the statistics for all runs."""
	totDist = 0
	totRuns = 0
	totTime = 0

	for i in range(len(distanceArray)):
		totDist += distanceArray[i]
		totRuns += 1
		totTime += Hour2Seconds(timeArray[i])
	avgDist = totDist/totRuns
	avgPace = totTime/totDist
	return totDist, totRuns, avgDist, Seconds2Hours(totTime), Seconds2Hours(avgPace)

def Hour2Seconds(fullTime):
	"""Converts time format (hh, mm, ss) into seconds."""
	secs = fullTime.second
	mins = fullTime.minute
	hours = fullTime.hour
	totalSeconds = secs + (mins*60) + (hours*3600)
	return totalSeconds

def Seconds2Hours(secs):
	"""Converts seconds into time formt (hh, mm, ss)."""
	if (secs > 3600):
		hour = int(secs/3600)
		minutes = secs%hour
		seconds = minutes%60
	else:
		hour = 0
		minutes = int(secs/60)
		seconds = int(secs%minutes)
	timeform = time(hour, minutes, seconds, 0)
	return timeform

def ThisMonth():
	"""Calculates statistics for current month"""
	monthDate = []
	monthDistance = []
	monthTime = []

	monthTotDist = 0
	monthTotSecs = 0
	monthTotRuns = 0 

	for i in range(len(dateArray)):
		if (date.today().month == dateArray[i].month):
			monthDate.append(dateArray[i])
			monthDistance.append(distanceArray[i])
			monthTime.append(timeArray[i])
			monthTotDist += distanceArray[i]
			monthTotSecs += Hour2Seconds(timeArray[i])
			monthTotRuns += 1
	
	monthAvgDist = monthTotDist/monthTotRuns
	monthAvgPace = monthTotSecs/monthTotDist
	return monthDate, monthDistance, monthTotDist, monthTotRuns, monthAvgDist, Seconds2Hours(monthTotSecs), Seconds2Hours(monthAvgPace)

def RunDistGraphs(dateList, distList, graph_title, graph_xaxis, graph_yaxis):
	"""Creates graph showing the distance ran for each run."""
	dates = [mdates.date2num(day) for day in dateList]
	plt.plot(dates, distList, 'bo')
	plt.title(graph_title)
	plt.xlabel(graph_xaxis)
	plt.ylabel(graph_yaxis)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
	plt.gcf().autofmt_xdate()
	plt.show()

			
if __name__ == '__main__':

	print "----------------------------------"
	print "Welcome to your running statistics"
	print "----------------------------------\n"

	# Defining lists that contain all run data
	dateArray = []
	distanceArray = []
	timeArray = []

	AddRun()
	ViewStats()

	print "\n----------------------------------"
	print "----------------------------------"
	print "----------- STATISTICS -----------"
	print "----------------------------------"
	print "----------------------------------\n"

	# Calculate total statistics
	totalDistance, totalNumberOfRuns, totalAverageDistance, totalRunTime, totalAveragePace = CalculateTotal()
	print "\n----- Total -----"
	print "-----------------"
	print "You have run a total distance of %.2fkms" %totalDistance
	print "You have run a total of %d times" %totalNumberOfRuns
	print "You run an average of %.2fkms" %totalAverageDistance
	print "You have run for a total of %s hrs" %totalRunTime.isoformat()
	print "You run with an average pace of %s hrs/km" %totalAveragePace.isoformat()
	RunDistGraphs(dateArray, distanceArray, "All time runs", "Date", "Distance (km)")

	# Calculate current month's statistics
	monthDateList, monthDistanceList, monthTotDist, monthTotRuns, monthAvgDist, monthTotTime, monthAvgPace = ThisMonth()
	print "\n----- This month -----"
	print "----------------------"
	print "You have run a total distance of %.2fkms" %monthTotDist
	print "You have run a total of %d times" %monthTotRuns
	print "You run an average of %.2fkms" %monthAvgDist
	print "You have run for a total of %s hrs" %monthTotTime.isoformat()
	print "You have run with an average pace of %s hrs/km" %monthAvgPace.isoformat()
	RunDistGraphs(monthDateList, monthDistanceList, "Runs this month", "Date", "Distance (km)")