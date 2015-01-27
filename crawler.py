import json
import pickle
import requests
from bs4 import BeautifulSoup as bs
import sys


baseUrl = "http://<the internal ip where the webpage was hosted to show the cab details>/ctmsph1/"
target_url = ""
__VIEWSTATE = ""
__EVENTVALIDATION = ""
current_page_number = 1
name_list = []
place_list = []
cabNumber_list = []
counter = 1

total_pages = -1



def read_url_at_time(t_time):
	global target_url

	f = open("f_1" + t_time  , "w+")
	target_url = baseUrl + "For" + t_time + "Sch.aspx"
	r = requests.get(target_url)
	if r.status_code == requests.codes.ok:
		return r.content
	else:
	    return r.raise_for_status()


def populate_post_parameters(page):
	print "Populating post Params"
	global __VIEWSTATE
	global __EVENTVALIDATION

	__VIEWSTATE = page.find(id="__VIEWSTATE")['value']
	__EVENTVALIDATION = page.find(id="__EVENTVALIDATION")['value']

def construct_post_payload(page_number):
	payload = {"__EVENTTARGET" : "ctl00$MainContent$gvSch1" , "__EVENTARGUMENT" :  "Page$"+str(page_number) , "__VIEWSTATE" : __VIEWSTATE , "__EVENTVALIDATION" : __EVENTVALIDATION}
	return payload

def get_next_page():
	#target_url will be populated the first time the read_url_at_time() function is called
	print "Getting the next page"
	global current_page_number
	current_page_number = current_page_number + 1
	payload = construct_post_payload(current_page_number)
#	payload = construct_post_payload(12)

	r = requests.post(target_url , data=payload)
	return bs(r.content)

def extract_names_places_cabNumbers(page):
	print "Extracting the employee cab details"
	global name_list
	global place_list
	global cabNumber_list

	table = page.find(id = "MainContent_gvSch1")
	trList = table.findAll("tr")
	no_of_rows = len(trList)
	for x in range(1 , no_of_rows-2):	# substracting 2 as the final two rows are not required!
		tdList = trList[x].findAll("td")
	#	print tdList[0].text
		name_list.append(tdList[0].text)
		cabNumber_list.append(tdList[1].text)
		place_list.append(tdList[3].text)

#def get_cabMates_for_employee(emp):
	
def __main__():
	global counter
	##usage : python timepass.py "time" "name_of_employee"
	args = sys.argv
	time = args[1]
#	emp_name = args[2]
#	print time , "..." , emp_name
	raw_page = read_url_at_time(time)
	parsed_page = bs(raw_page)
	try:
		while(1):
			print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
			print "Processing page number : " , counter
			print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
			populate_post_parameters(parsed_page)
			extract_names_places_cabNumbers(parsed_page)
			parsed_page = get_next_page()
			counter = counter + 1
	except Exception as e:
		print e
		print "This exception is thrown when either the last page is processed ,  or the data is not available"
	finally:
		print "now all the information is downloaded, we can start processing"
#		get_cabMates_for_employee(emp_name)
		pickle.dump(name_list , open("name_list" , "w+"))
		pickle.dump(place_list , open("place_list", "w+"))
		pickle.dump(cabNumber_list , open("cabNumber_list", "w+"))
__main__()

