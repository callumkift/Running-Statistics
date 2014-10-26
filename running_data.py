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
	### Get's file to add runs to.
	if (os.path.isfile("past_runs.txt")):
		print "file exists"
		#f = open("past_runs.txt", "a") # opens and appends to file
		RunInfo("previous")
	else:
		# Creates file
		print "This seems to be your first run - congratulations."
		#f = open("past_runs.txt", "w")
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

	f.write(run_date + " " + run_distance + " " + run_time + "\n") 
	f.close
	return

print "----------------------------------"
print "Welcome to your running statistics"
print "----------------------------------\n"

add_run = raw_input("Do you want to add a new run? (y/n) \npress 'n' if you want to just see your statistics\n\n")

if (add_run == "y" or add_run == "Y"):
	print "yes detected"
	GetFile()
	# Check to see if there is a file
	# If not create it
	# Input data
	# Read file
else:
	print "not a yes"
	# Just want our statistics
	# Read file


