###########################################################
###                                                     ###
###  This script was created so that a runner can gain  ###
###  more insights into their runs.                     ###
###                                                     ###
###  Creator: Callum Kift                               ###
###  email: callumkift@gmail.com                        ###
###                                                     ### 
###########################################################

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
	run_time = raw_input("\nHow long did you run for? (HH:MM:SS)\n") 

	f.write("\n" + run_date + " " + run_distance + " " + run_time) 
	f.close
	return

def ViewStats():
	"""Asks user if they want to view their stats, if yes then it runs ReadData()"""
	view_stats = raw_input("\nDo you want to view your stats? (y/n)\n")
	if (view_stats == "y" or view_stats == "Y"):
		ReadData()

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
					dateList.append(date(int(column[2]), int(column[1]), int(column[0])))
					distanceList.append(float(column[3]))
					timeList.append(time(int(column[4]), int(column[5]), int(column[6]),0))
					paceList.append(Seconds2Hours(Hour2Seconds(time(int(column[4]), int(column[5]), int(column[6]),0))/float(column[3])))
		# print "Data read", len(distanceList)
	else:
		print "\n-- It seems that you have no previous runs saved."
		print "--",
		AddRun()
		ReadData()
	return

def Hour2Seconds(fullTime):
	"""Converts time format (hh, mm, ss) into seconds."""
	secs = fullTime.second
	mins = fullTime.minute
	hours = fullTime.hour
	totalSeconds = secs + (mins*60) + (hours*3600)
	return totalSeconds

def Seconds2Hours(secs):
	"""Converts seconds into time formt (hh, mm, ss)."""
	hour = int(secs/3600)
	minutes = int((secs-(hour*3600))/60)
	seconds = int(secs-(hour*3600)-(minutes*60))
	timeform = time(hour, minutes, seconds, 0)
	return timeform

def CalculateTotal():
	"""This calculates the statistics for all runs."""
	totDist = 0
	totRuns = 0
	totTime = 0

	runAvgPace = []

	bestDistValue = 0
	bestDistIndex = 0
	bestAvgPaceValue = 1000000
	bestAvgPaceIndex = 0
	longTimeValue = time(0, 0, 0, 0)
	longTimeIndex = 0

	for i in range(len(distanceList)):
		totDist += distanceList[i]
		totRuns += 1
		totTime += Hour2Seconds(timeList[i])
		#secsAvgPace = Hour2Seconds(timeList[i])/distanceList[i]
		#runAvgPace.append(Seconds2Hours(secsAvgPace))
		if (distanceList[i] > bestDistValue):
			bestDistValue = distanceList[i]
			bestDistIndex = i
		if (bestAvgPaceValue > Hour2Seconds(paceList[i])):
			bestAvgPaceValue = Hour2Seconds(paceList[i])
			bestAvgPaceIndex = i
		if (longTimeValue < timeList[i]):
			longTimeValue = timeList[i]
			longTimeIndex = i
	avgDist = totDist/totRuns
	avgPace = totTime/totDist
	
	return bestDistIndex, bestAvgPaceIndex, longTimeIndex, totDist, totRuns, avgDist, Seconds2Hours(totTime), Seconds2Hours(avgPace)

def ThisMonth():
	"""Calculates statistics for current month"""
	monthDate = []
	monthDistance = []
	monthTime = []
	monthRunAvgPace = []

	monthTotDist = 0
	monthTotSecs = 0
	monthTotRuns = 0 

	for i in range(len(dateList)):
		if (date.today().month == dateList[i].month and date.today().year == dateList[i].year):
			monthDate.append(dateList[i])
			monthDistance.append(distanceList[i])
			monthTime.append(timeList[i])
			monthRunAvgPace.append(paceList[i])
			
			monthTotDist += distanceList[i]
			monthTotSecs += Hour2Seconds(timeList[i])
			monthTotRuns += 1

	monthAvgDist = monthTotDist/monthTotRuns
	monthTotAvgPace = monthTotSecs/monthTotDist
	return monthDate, monthDistance, monthTotDist, monthTotRuns, monthAvgDist, Seconds2Hours(monthTotSecs), Seconds2Hours(monthTotAvgPace), monthRunAvgPace

def DistPaceGraph(x_dateList, y1_paceList, y2_distList, graph_title, graph_xaxis, graph_y1axis, graph_y2axis):
	"""Creates a graph showing the distance of each run and the average pace
		of it."""
	dates = [mdates.date2num(day) for day in x_dateList]
	paces = [Hour2Seconds(time) for time in y1_paceList]

	fig, ax1 = plt.subplots()
	ax1.plot(dates, paces, '#FFD6D6')
	ax1.set_title(graph_title)
	ax1.set_xlabel(graph_xaxis)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
	ax1.set_ylabel(graph_y1axis, color='r')
	ax1.set_ylim([(min(paces)-30), (max(paces)+30)])
	ax1.fill_between(dates, paces, color='#FCE6E6')
	for tl in ax1.get_yticklabels():
		tl.set_color('r')

	ax2 = ax1.twinx()
	ax2.plot(dates, y2_distList, 'bo')
	ax2.set_ylabel(graph_y2axis, color='b')
	ax2.set_ylim([(min(y2_distList)-0.5), (max(y2_distList)+0.5)])
	for tl in ax2.get_yticklabels():
		tl.set_color('b')
	plt.show()

def LastRunComparison():
	"""This compares the last run with other runs you have done of a similar distance. These distances will be
		of the ranges: (0-3), (3-5), (5-7.5), (7.5-10), (10-15), (15-20), (20-30), (30-50), (50+)."""
	lastRunDate = dateList[-1]
	lastRunDistance = distanceList[-1]
	lastRunTime = timeList[-1]
	lastRunAvgPaceSecs = (Hour2Seconds(lastRunTime)/lastRunDistance)

	distRangeString = ""

	sameDistListDate = [lastRunDate]
	sameDistListPace = [lastRunAvgPaceSecs]

	for i in range(len(dateList)-1):
		if (distanceList[i] < 3.0 and lastRunDistance < 3.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "less than 3km"
		if (distanceList[i] >= 3.0 and distanceList[i] < 5.0 and lastRunDistance >= 3.0 and lastRunDistance < 5.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "3 - 5 km"
		if (distanceList[i] >= 5.0 and distanceList[i] < 7.5 and lastRunDistance >= 5.0 and lastRunDistance < 7.5):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "5 - 7.5 km"
		if (distanceList[i] >= 7.5 and distanceList[i] < 10.0 and lastRunDistance >= 7.5 and lastRunDistance < 10.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "7.5 - 10 km"
		if (distanceList[i] >= 10.0 and distanceList[i] < 15.0 and lastRunDistance >= 10.0 and lastRunDistance < 15.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "10 - 15 km"
		if (distanceList[i] >= 15.0 and distanceList[i] < 20.0 and lastRunDistance >= 15.0 and lastRunDistance < 20.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "15 - 20 km"
		if (distanceList[i] >= 20.0 and distanceList[i] < 30.0 and lastRunDistance >= 20.0 and lastRunDistance < 30.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "20 - 30 km"
		if (distanceList[i] >= 30.0 and distanceList[i] < 50.0 and lastRunDistance >= 30.0 and lastRunDistance < 50.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "30 - 50 km"
		if (distanceList[i] >= 50.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "more than 50km"

	sameDistListPace, sameDistListDate = (list(t) for t in zip(*sorted(zip(sameDistListPace, sameDistListDate))))
	pacePosit = 0
	for i in range(len(sameDistListDate)):
		if lastRunDate == sameDistListDate[i]:
			pacePosit = i+1
		
	return lastRunAvgPaceSecs, lastRunDate, sameDistListPace, sameDistListDate, pacePosit, distRangeString


if __name__ == '__main__':

	print "----------------------------------"
	print "Welcome to your running statistics"
	print "----------------------------------\n"

	# Defining lists that contain all run data
	dateList = [] # datetime.date(yyyy, mm, dd)
	distanceList = [] # float
	timeList = [] # datetime.time(hh, mm, ss)
	paceList = [] # secs

	AddRun()
	ViewStats()

	print "\n----------------------------------"
	print "----------------------------------"
	print "----------- STATISTICS -----------"
	print "----------------------------------"
	print "----------------------------------\n"

	# Calculate total statistics
	# --------------------------
	totalBestDist, totalBestPace, totalLongRun, totalDistance, totalNumberOfRuns, totalAverageDistance, totalRunTime, totalAveragePace = CalculateTotal()
	print "\n----- Total -----"
	print "-----------------"
	print "You have run a total distance of %.2fkms" %totalDistance
	print "You have run a total of %d times" %totalNumberOfRuns
	print "You run an average of %.2fkms" %totalAverageDistance
	print "You have run for a total of %s hrs" %totalRunTime.isoformat()
	print "You run with an average pace of %s mins/km" %totalAveragePace.strftime('%M.%S')

	print "\nYour furthest run was %.2fkm on %s with an average pace of %s mins/km" %(distanceList[totalBestDist], dateList[totalBestDist].strftime('%d/%m/%Y'), paceList[totalBestDist].strftime('%M.%S'))
	print "Your longest run was %shrs on %s where you ran %.2f at an average pace of %s mins/km." %(timeList[totalLongRun].isoformat(), dateList[totalLongRun].strftime('%d/%m/%Y'), distanceList[totalLongRun], paceList[totalBestDist].strftime('%M.%S'))
	print "Your best pace was %s mins/km on %s for a distance of %.2fkm" %(paceList[totalBestPace].strftime('%M.%S'), dateList[totalBestPace].strftime('%d/%m/%Y'), distanceList[totalBestPace])
	DistPaceGraph(dateList, paceList, distanceList, "All runs", "Date", "Pace (secs/km)", "Distance (km)")


	# Calculate current month's statistics
	# ------------------------------------
	monthDateList, monthDistanceList, monthTotDist, monthTotRuns, monthAvgDist, monthTotTime, monthTotAvgPace, monthIndAvgPace = ThisMonth()
	print "\n----- This month -----"
	print "----------------------"
	print "You have run a total distance of %.2fkms" %monthTotDist
	print "You have run a total of %d times" %monthTotRuns
	print "You run an average of %.2fkms" %monthAvgDist
	print "You have run for a total of %s hrs" %monthTotTime.isoformat()
	print "You have run with an average pace of %s mins/km" %monthTotAvgPace.strftime('%M.%S')
	DistPaceGraph(monthDateList, monthIndAvgPace, monthDistanceList, "Runs this month", "Date", "Pace (secs/km)", "Distance (km)")


	# Compare last run to similar run distance
	# ----------------------------------------
	lrPace, lrDate, sdPace, sdDate, lrPosit, distRange = LastRunComparison()
	print "\n----- Last run compaision -----"
	print "-------------------------------"
	print "Your last run on %s is ranked #%d for your best pace for the distance %s." %(lrDate.strftime('%d/%m/%Y'), lrPosit, distRange)
	for i in range(len(sdPace)):
		print "%d) %s mins/km on %s" %((i+1), Seconds2Hours(sdPace[i]).strftime('%M.%S'), sdDate[i].strftime('%d/%m/%Y'))