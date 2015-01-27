import pickle
import sys
import re

###
#This file, reads the data of all the employees , that booked the cab from the pickle object that was created by the crawler.py
#It takes the name of the employee that we want to search for as an argument and displays the answer appropriately
###

name_list = []
place_list = []
cabNumber_list = []
resultCab_list = []
def __main__():
	global name_list
	global place_list
	global cabNumber_list
	global resultIndex_list


	argv = sys.argv
	name = argv[1]
	#reading the pickle data
	name_list = pickle.load(open("name_list"))
	place_list = pickle.load(open("place_list"))
	cabNumber_list = pickle.load(open("cabNumber_list"))

	#doing a search on the data
	for x in range(len(name_list)):
		if re.search(name , name_list[x] , re.IGNORECASE):
			if 	cabNumber_list[x] not in resultCab_list:
				resultCab_list.append(cabNumber_list[x])

	#displaying results
	for cabresult in resultCab_list:
		for cabNum in range(len(cabNumber_list)):
			if cabresult == cabNumber_list[cabNum]:
				print name_list[cabNum] , "\t" , cabNumber_list[cabNum]
		print "*************************************************************************`"

__main__()