import time 
import requests 

# Function to calculate the RTT 
def RTT(url): 
	for j in range(0,9):
	    total = 0
	    for i in range(0,19):
		    # time period when the signal is sent 
		    t1 = time.time() 

		    r = requests.get(url) 

		    # time  period when acknowledgement of signal 
		    # is received 
		    t2 = time.time() 

		    # total time taken during this process 
		    tim = t2-t1
		    total = total+tim
	    wow = str(tim/20) 

	    print("Time in seconds :" + wow) 

# Pilot program 
# url address to hit
url = "http://200.122.2.2/"
RTT(url) 
