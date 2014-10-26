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

def getfile():
	### Get's file to add runs to.
	if (os.path.isfile("past_runs.txt")):
		print "file exists"
		f = file("past_runs.txt", "a") # opens and appends to file
	else:
		# Creates file
		print "This seems to be your first run - congratulations."
		f = file("past_runs.txt", "w")
	return

print "----------------------------------"
print "Welcome to your running statistics"
print "----------------------------------\n"

add_run = raw_input("Do you want to add a new run? (y/n) \npress 'n' if you want to just see your statistics\n\n")

if (add_run == "y" or add_run == "Y"):
	print "yes detected"
	getfile()
	# Check to see if there is a file
	# If not create it
	# Input data
	# Read file
else:
	print "not a yes"
	# Just want our statistics
	# Read file


