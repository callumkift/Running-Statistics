#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  This script was created so that a runner can gain
#  more insights into their runs.
#
#  Creator: Callum Kift
#  email: callumkift@gmail.com
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

import os.path
import re
from datetime import date, time, datetime, timedelta
from array import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def AddRun():
	"""Asks user if they want to add a new run, if yes then it runs WriteRunToFile()"""
	add_run = raw_input("Do you want to add a new run? (y/n)\n")
	if (add_run == "y" or add_run == "Y"):
		#print "yes detected"
		WriteRunToFile()
		return True
	else:
		return False

def ValidateDate(date_text):
	try:
		datetime.strptime(date_text, '%d/%m/%Y')
		return True
	except ValueError:
		print "\n*** Incorrect date fromat ***\n"

def ValidateDistance(distance_text):
	try:
		float(distance_text)
		return True
	except ValueError:
		print "\n*** Incorrect distance fromat ***\n"

def ValidateTime(time_text):
	try:
		datetime.strptime(time_text, '%H:%M:%S')
		return True
	except ValueError:
		print "\n*** Incorrect time format ***\n"

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

	if (ValidateDate(run_date) and ValidateDistance(run_distance) and ValidateTime(run_time)):
		f.write("\n" + run_date + " " + run_distance + " " + run_time)
		f.close
		return
	else:
		retry = raw_input("\nInput again? (y/n)\n")
		if (retry == 'y' or retry == 'Y'):
			f.close
			WriteRunToFile()
		else:
			f.close
			return

def ViewStats():
	"""Asks user if they want to view their stats, if yes then it runs ReadData()"""
	view_stats = raw_input("\nDo you want to view your stats? (y/n)\n")
	if (view_stats == "y" or view_stats == "Y"):
		return True
	else:
		return False

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
		return True
	else:
		print "\n-- It seems that you have no previous runs saved."
		print "--",
		if AddRun():
			ReadData()
		else:
			return False

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

def ThisYear():
	"""Calculates sttistics for current year"""
	yearDate = []
	yearDistance = []
	yearTime = []
	yearRunAvgPace = []

	yearTotDist = 0
	yearTotSecs = 0
	yearTotRuns = 0

	for i in range(len(dateList)):
		if (date.today().year == dateList[i].year):
			yearDate.append(dateList[i])
			yearDistance.append(distanceList[i])
			yearTime.append(timeList[i])
			yearRunAvgPace.append(paceList[i])

			yearTotDist += distanceList[i]
			yearTotSecs += Hour2Seconds(timeList[i])
			yearTotRuns += 1

	yearAvgDist = yearTotDist/yearTotRuns
	yearTotAvgPace = yearTotSecs/yearTotDist
	return yearDate, yearDistance, yearTotDist, yearTotRuns, yearAvgDist, Seconds2Hours(yearTotSecs), Seconds2Hours(yearTotAvgPace), yearRunAvgPace



def LastMonth():
	"""Calculates statistics for the previous month"""

	monthTotDist = 0
	monthTotSecs = 0
	monthTotRuns = 0

	lastMonthNum = date.today().month

	for i in range(len(dateList)):
		if (lastMonthNum == 1):
			if (dateList[i].year + 1 == date.today().year and dateList[i].month == 12):
			# This is incase we are in January - i.e. the previous month is from a different year

				monthTotDist += distanceList[i]
				monthTotSecs += Hour2Seconds(timeList[i])
				monthTotRuns += 1
		else:
			if (date.today().month -1 == dateList[i].month and date.today().year == dateList[i].year):

				monthTotDist += distanceList[i]
				monthTotSecs += Hour2Seconds(timeList[i])
				monthTotRuns += 1
	if monthTotRuns != 0:
		monthAvgDist = monthTotDist/monthTotRuns
		monthTotAvgPace = monthTotSecs/monthTotDist
	else:
		monthAvgDist = 0
		monthTotAvgPace = 0
	return monthTotDist, monthTotRuns, monthAvgDist, Seconds2Hours(monthTotSecs), Seconds2Hours(monthTotAvgPace)

def DistPaceGraph(x_dateList, y1_paceList, y2_distList, graph_title, graph_xaxis, graph_y1axis, graph_y2axis, graph_type):
	"""Creates a graph showing the distance of each run and the average pace
		of it."""
	dates = [mdates.date2num(day) for day in x_dateList]
	paces = [Hour2Seconds(time) for time in y1_paceList]

	fig, ax1 = plt.subplots()
	ax1.plot(dates, paces, '#FAC8CA')
	ax1.set_title(graph_title)
	ax1.set_xlabel(graph_xaxis)
	ax1.set_ylim([(min(paces)-60), (max(paces)+60)])
	ax1.set_ylabel(graph_y1axis, color='r')
	ax1.fill_between(dates, paces, color='#FCE6E6')
	for tl in ax1.get_yticklabels():
		tl.set_color('r')

	ax2 = ax1.twinx()
	ax2.vlines(dates, 0, y2_distList, 'b')
	ax2.set_ylabel(graph_y2axis, color='b')
	ax2.set_ylim([0, (max(y2_distList)+0.5)])
	for tl in ax2.get_yticklabels():
		tl.set_color('b')

	if graph_type == "month":
		ax2.xaxis.set_major_formatter(mdates.DayLocator())
		ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
		dates.append(mdates.date2num(mdates.num2date(min(dates))-timedelta(hours=6)))
		dates.append(mdates.date2num(mdates.num2date(max(dates))+timedelta(hours=6)))
		ax2.set_xlim([(mdates.num2date(min(dates))), (mdates.num2date(max(dates)))])
	elif graph_type == "all" or graph_type == "year":
		ax2.xaxis.set_major_formatter(mdates.MonthLocator())
		ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
		dates.append(mdates.date2num(mdates.num2date(min(dates))-timedelta(days=3)))
		dates.append(mdates.date2num(mdates.num2date(max(dates))+timedelta(days=3)))
		ax2.set_xlim([(mdates.num2date(min(dates))), (mdates.num2date(max(dates)))])
	plt.show()

def PaceDateGraph(x_list, y_list, graph_title, graph_xaxis, graph_yaxis):
	"""Creates a graph showing the average pace of each run at the same
		distance range"""
	dates = [mdates.date2num(day) for day in x_list]
	#paces = [Hour2Seconds(time) for time in y1_paceList]

	fig, ax = plt.subplots()
	ax.plot(dates, y_list, '#FAC8CA')
	ax.set_title(graph_title)
	ax.set_xlabel(graph_xaxis)
	ax.set_ylim([(min(y_list)-60), (max(y_list)+60)])
	ax.set_ylabel(graph_yaxis)
	ax.fill_between(dates, y_list, color='#FCE6E6')
	ax.xaxis.set_major_formatter(mdates.MonthLocator())
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

	dates.append(mdates.date2num(mdates.num2date(min(dates))-timedelta(days=3)))
	dates.append(mdates.date2num(mdates.num2date(max(dates))+timedelta(days=3)))
	ax.set_xlim([(mdates.num2date(min(dates))), (mdates.num2date(max(dates)))])

	# if graph_type == "month":
	# 	ax2.xaxis.set_major_formatter(mdates.DayLocator())
	# 	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
	# elif graph_type == "all":
	# 	dates.append(mdates.date2num(mdates.num2date(min(dates))-timedelta(days=3)))
	# 	dates.append(mdates.date2num(mdates.num2date(max(dates))+timedelta(days=3)))
	# 	ax2.set_xlim([(mdates.num2date(min(dates))), (mdates.num2date(max(dates)))])
	plt.show()

def LastRunComparison():
	"""This compares the last run with other runs you have done of a similar distance. These distances will be
		of the ranges: (0-4), (4-6), (6-8), (8-10), (10-15), (15-20), (20-30), (30-50), (50+)."""
	lastRunDate = dateList[-1]
	lastRunDistance = distanceList[-1]
	lastRunTime = timeList[-1]
	lastRunAvgPaceSecs = (Hour2Seconds(lastRunTime)/lastRunDistance)

	distRangeString = ""

	sameDistListDate = []
	sameDistListPace = []

	for i in range(len(dateList)):
		if (distanceList[i] < 4.0 and lastRunDistance < 4.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "less than 4km"
		if (distanceList[i] >= 4.0 and distanceList[i] < 6.0 and lastRunDistance >= 4.0 and lastRunDistance < 6.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "4-6 km"
		if (distanceList[i] >= 6.0 and distanceList[i] < 8.0 and lastRunDistance >= 6.0 and lastRunDistance < 8.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "6-8 km"
		if (distanceList[i] >= 8.0 and distanceList[i] < 10.0 and lastRunDistance >= 8.0 and lastRunDistance < 10.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "8-10 km"
		if (distanceList[i] >= 10.0 and distanceList[i] < 15.0 and lastRunDistance >= 10.0 and lastRunDistance < 15.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "10-15 km"
		if (distanceList[i] >= 15.0 and distanceList[i] < 20.0 and lastRunDistance >= 15.0 and lastRunDistance < 20.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "15-20 km"
		if (distanceList[i] >= 20.0 and distanceList[i] < 30.0 and lastRunDistance >= 20.0 and lastRunDistance < 30.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "20-30 km"
		if (distanceList[i] >= 30.0 and distanceList[i] < 50.0 and lastRunDistance >= 30.0 and lastRunDistance < 50.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "30-50 km"
		if (distanceList[i] >= 50.0):
			pace = Hour2Seconds(timeList[i])/distanceList[i]
			sameDistListDate.append(dateList[i])
			sameDistListPace.append(pace)
			distRangeString = "more than 50km"

	sameDistListPaceSorted, sameDistListDateSorted = (list(t) for t in zip(*sorted(zip(sameDistListPace, sameDistListDate))))
	pacePosit = 0
	for i in range(len(sameDistListDateSorted)):
		if lastRunDate == sameDistListDateSorted[i]:
			pacePosit = i+1

	return lastRunAvgPaceSecs, lastRunDate, sameDistListPace, sameDistListDate, sameDistListPaceSorted, sameDistListDateSorted, pacePosit, distRangeString

def LastRunBestPace(dbPace, lrDist):
	"""Calculates time of your last run if it was ran at the best pace for that
		distance."""
	return Seconds2Hours(dbPace*lrDist)

def LastRunAvgPace(sdPace, lrDist):
	dsTotTime = 0
	for i in range(len(sdPace)):
		dsTotTime += sdPace[i]

	lrAP = (dsTotTime/len(sdPace))*lrDist
	return Seconds2Hours(lrAP)

def PrintTotalStats(totalBestDist, totalBestPace, totalLongRun, totalDistance, totalNumberOfRuns, totalAverageDistance, totalRunTime, totalAveragePace):
	print "\n----- Total -----"
	print "-----------------"
	print "You have run a total distance of %.2fkms." %totalDistance
	print "You have run a total of %d times." %totalNumberOfRuns
	print "You run an average of %.2fkms." %totalAverageDistance
	print "You have run for a total of %s hrs." %totalRunTime.isoformat()
	print "You run with an average pace of %s mins/km.\n" %totalAveragePace.strftime('%M.%S')

	print "*** Your furthest run was %.2fkms on %s with an average pace of %s mins/km.\n" %(distanceList[totalBestDist], dateList[totalBestDist].strftime('%d/%m/%Y'), paceList[totalBestDist].strftime('%M.%S'))
	print "*** Your longest run was %shrs on %s where you ran %.2fkms at an average pace of %s mins/km.\n" %(timeList[totalLongRun].isoformat(), dateList[totalLongRun].strftime('%d/%m/%Y'), distanceList[totalLongRun], paceList[totalLongRun].strftime('%M.%S'))
	print "*** Your best pace was %s mins/km on %s for a distance of %.2fkms." %(paceList[totalBestPace].strftime('%M.%S'), dateList[totalBestPace].strftime('%d/%m/%Y'), distanceList[totalBestPace])
	DistPaceGraph(dateList, paceList, distanceList, "All runs", "Date", "Pace (secs/km)", "Distance (km)", "all")

def PrintCurrentMonthStats(monthDateList, monthDistanceList, monthTotDist, monthTotRuns, monthAvgDist, monthTotTime, monthTotAvgPace, monthIndAvgPace ):
	print "\n----- This month -----"
	print "----------------------"
	if monthTotRuns == 0:
		print "You have not run yet this month."
	elif monthTotRuns == 1:
		print "You have run only once this month on %s for %.2fkms at a pace of %s mins/km." %(dateList[-1].strftime('%d/%m/%Y'), distanceList[-1], paceList[-1].strftime('%M.%S'))
	else:
		print "You have run a total distance of %.2fkms." %monthTotDist
		print "You have run a total of %d times." %monthTotRuns
		print "You run an average of %.2fkms." %monthAvgDist
		print "You have run for a total of %s hrs." %monthTotTime.isoformat()
		print "You have run with an average pace of %s mins/km.\n" %monthTotAvgPace.strftime('%M.%S')
		for i in range(len(monthDateList)):
			print "%2d)  %s  %5.2fkms  %s mins/km" %((i+1), monthDateList[i].strftime('%d/%m/%Y'), monthDistanceList[i], monthIndAvgPace[i].strftime('%M.%S'))
		DistPaceGraph(monthDateList, monthIndAvgPace, monthDistanceList, "Runs this month", "Date", "Pace (secs/km)", "Distance (km)", "month")

def PrintCurrentYearStats(yearDateList, yearDistanceList, yearTotDist, yearTotRuns, yearAvgDist, yearTotTime, yearTotAvgPace, yearIndAvgPace ):
	print "\n----- This year -----"
	print "----------------------"
	if yearTotRuns == 0:
		print "You have not run yet this year."
	elif yearTotRuns == 1:
		print "You have run only once this year on %s for %.2fkms at a pace of %s mins/km." %(dateList[-1].strftime('%d/%m/%Y'), distanceList[-1], paceList[-1].strftime('%M.%S'))
	else:
		print "You have run a total distance of %.2fkms." %yearTotDist
		print "You have run a total of %d times." %yearTotRuns
		print "You run an average of %.2fkms." %yearAvgDist
		print "You have run for a total of %s hrs." %yearTotTime.isoformat()
		print "You have run with an average pace of %s mins/km.\n" %yearTotAvgPace.strftime('%M.%S')

		DistPaceGraph(yearDateList, yearIndAvgPace, yearDistanceList, "Runs this year", "Date", "Pace (secs/km)", "Distance (km)", "year")

def PrintLastMonthThisMonthStats(lastMonthTotDist, lastMonthTotRuns, lastMonthAvgDist, lastMonthTotTime, lastMonthTotAvgPace, monthTotDist, monthTotRuns, monthAvgDist, monthTotTime, monthTotAvgPace):
	print "\n----- Last Month vs This Month -----"
	print "------------------------------------"
	if monthTotRuns == 0 and lastMonthTotRuns == 0:
		print "You have not run this month or last month. Get off your arse!"
	elif monthTotRuns == 0 and lastMonthTotRuns != 0:
		print "You have not run this month, last month you ran %d times." %lastMonthTotRuns
	elif lastMonthTotRuns == 0 and monthTotRuns != 0:
		print "You did not run last month, but you have already run %d time(s) this month." %monthTotRuns
	else:
		print "\n                   |  Last  Month  |  This  Month  "
		print "---------------------------------------------------"
		print "Number of runs     |  %2d           | %2d"		%(lastMonthTotRuns, monthTotRuns)
		print "Total distance     | %3.2f kms     | %3.2f kms"	%(lastMonthTotDist, monthTotDist)
		print "Average distance   | %2.2f kms      | %2.2f kms"	%(lastMonthAvgDist, monthAvgDist)
		print "Total time         | %s hrs  | %s hrs"			%(lastMonthTotTime.isoformat(), monthTotTime.isoformat())
		print "Averge pace        | %s mins/km | %s mins/km"	%(lastMonthTotAvgPace.strftime('%M.%S'), monthTotAvgPace.strftime('%M.%S'))

def PrintLastRunComparison(lrPace, lrDate, sdPace, sdDate, sdPaceSorted, sdDateSorted, lrPosit, distRange):
	print "\n----- Last run comparison -----"
	print "-------------------------------"
	if len(sdPaceSorted) != 1:
		lr_bp = LastRunBestPace(sdPaceSorted[0], distanceList[-1])
		lr_ap = LastRunAvgPace(sdPaceSorted,distanceList[-1])
		if lrPosit == 1:
			print "*** CONGRATULATIONS! Your last run on %s was your best pace for the distance %s.\n" %(lrDate.strftime('%d/%m/%Y'), distRange)
		else:
			print "*** Your last run on %s is ranked #%d for your best pace for the distance %s.\n" %(lrDate.strftime('%d/%m/%Y'), lrPosit, distRange)
			print "*** If you had run at your best pace for this distance, your last run would have taken %s minutes less.\n" %(Seconds2Hours(Hour2Seconds(timeList[-1]) - Hour2Seconds(lr_bp)).strftime('%M.%S'))
		if (Hour2Seconds(lr_ap) < Hour2Seconds(timeList[-1])):
			print "*** If you had run at your average pace for this distance, yout last run would have taken %s minutes less." %(Seconds2Hours(abs(Hour2Seconds(timeList[-1]) - Hour2Seconds(lr_ap))).strftime('%M.%S'))
		else:
			print "*** Your run took %s minutes less than if you had run at your average pace for this distance." %(Seconds2Hours(abs(Hour2Seconds(timeList[-1]) - Hour2Seconds(lr_ap))).strftime('%M.%S'))
		PaceDateGraph(sdDate, sdPace, "Runs for the distance " + distRange, "Date", "Pace (secs/km)")
	else:
		print "*** CONGRATULATIONS! This is your first run for the distance %s.\n"%distRange

if __name__ == '__main__':

	print "----------------------------------"
	print "Welcome to your running statistics"
	print "----------------------------------\n"

	# Defining lists that contain all run data
	dateList = [] # datetime.date(yyyy, mm, dd)
	distanceList = [] # float
	timeList = [] # datetime.time(hh, mm, ss)
	paceList = [] # time(hh, mm, ss)/km

	AddRun()

	if ViewStats():
		if ReadData():
			print "\n----------------------------------"
			print "----------------------------------"
			print "----------- STATISTICS -----------"
			print "----------------------------------"
			print "----------------------------------\n"

			# Compare last run to similar run distance
			# ----------------------------------------
			lrPace, lrDate, sdPace, sdDate, sdPaceSorted, sdDateSorted, lrPosit, distRange = LastRunComparison()
			PrintLastRunComparison(lrPace, lrDate, sdPace, sdDate,sdPaceSorted, sdDateSorted, lrPosit, distRange)

			# Calculate current month's statistics
			# ------------------------------------
			monthDateList, monthDistanceList, monthTotDist, monthTotRuns, monthAvgDist, monthTotTime, monthTotAvgPace, monthIndAvgPace = ThisMonth()
			PrintCurrentMonthStats(monthDateList, monthDistanceList, monthTotDist, monthTotRuns, monthAvgDist, monthTotTime, monthTotAvgPace, monthIndAvgPace)

			# This month vs last month
			# ----------------------------
			lmonthTotDist, lmonthTotRuns, lmonthAvgDist, lmonthTotTime, lmonthTotAvgPace = LastMonth()
			PrintLastMonthThisMonthStats(lmonthTotDist, lmonthTotRuns, lmonthAvgDist, lmonthTotTime, lmonthTotAvgPace, monthTotDist, monthTotRuns, monthAvgDist, monthTotTime, monthTotAvgPace)

			# Calculate current year's statistics
			# -----------------------------------

			yearDateList, yearDistanceList, yearTotDist, yearTotRuns, yearAvgDist, yearTotTime, yearTotAvgPace, yearIndAvgPace = ThisYear()
			PrintCurrentYearStats(yearDateList, yearDistanceList, yearTotDist, yearTotRuns, yearAvgDist, yearTotTime, yearTotAvgPace, yearIndAvgPace)


			# Calculate total statistics
			# --------------------------
			totalBestDist, totalBestPace, totalLongRun, totalDistance, totalNumberOfRuns, totalAverageDistance, totalRunTime, totalAveragePace = CalculateTotal()
			PrintTotalStats(totalBestDist, totalBestPace, totalLongRun, totalDistance, totalNumberOfRuns, totalAverageDistance, totalRunTime, totalAveragePace)

		else:
			print "\nYou need to add runs to view stats."
			print "Goodbye."
	else:
		print "\nGoodbye."
