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
		f.write("DATE (YYYY/MM/DD) | " + "DISTANE (KM) | " + "TIME (HH:MM:SS) \n")
		f.write("--------------------------------------------------\n")
		f.write("\n")

	run_date = raw_input("\nWhat was the date of the run? (YYYY/MM/DD)\n")
	run_distance = raw_input("\nHow far did you run? (x.yz km)\n")
	run_time = raw_input("\nHow long did you run for? (HH:MM:SS)\n") 

	f.write(run_date + " " + run_distance + " " + run_time + "\n") 
	f.close
	return

def ReadData():
	if (os.path.isfile("past_runs.txt")):
		f = open("past_runs.txt", "r")
		column_title = f.readline()
		underline = f.readline()
		blank_line = f.readline
		for line in f:
				line = line.strip() 
				columns = line.split(" ") 
		print "Data read"
	else:
		print "\n-- It seems that you have no previous runs saved."
		print "--",
		AddRun()
	return

			
if __name__ == '__main__':

	print "----------------------------------"
	print "Welcome to your running statistics"
	print "----------------------------------\n"

	AddRun()
	ViewStats()



