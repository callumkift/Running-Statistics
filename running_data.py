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
	run_date = raw_input("What was the date of the run? (YYYY/MM/DD)\n")
	run_distance = raw_input("How far did you run? (x.yz km)\n")
	run_time = raw_input("How long did you run for? (HH:MM:SS)\n") 

	if (a == "previous"):
		f = open("past_runs.txt", "a") # opens and appends to file
	elif (a == "new"):
		f = open("past_runs.txt", "w")
		f.write("DATE (YYYY/MM/DD) | " + "DISTANE (KM) | " + "TIME (HH:MM:SS) \n")
		f.write("--------------------------------------------------\n")
		f.write("\n")

	f.write(run_date + " " + run_distance + " " + run_time + "\n") 
	f.close
	return

def ReadData():
	f = open("past_runs.txt", "r")
	column_title = f.readline()
	underline = f.readline()
	blank_line = f.readline
	for line in f:
			line = line.strip() 
			columns = line.split(" ") 

	print "Data read"
	return
			


print "----------------------------------"
print "Welcome to your running statistics"
print "----------------------------------\n"

add_run = raw_input("Do you want to add a new run? (y/n) \npress 'n' if you want to just see your statistics\n\n")

if (add_run == "y" or add_run == "Y"):
	#print "yes detected"
	GetFile()
	ReadData()
	# Read file
else:
	#print "not a yes"
	ReadData()
	# Read file


