#AUTHOR: Pratham Singh Gahlaut
#VERSION: 1.1.2
#DATE: 04/03/2021
#CONTACT: pgahlaut994@gmail.com, pratham_m200710ca@nitc.ac.in
#DESC: Automated script to scrape through the Eduserver Courses and submit the attendance. Much needed for people like me! 

import requests
from bs4 import BeautifulSoup
import time
import os
import sys


def display_ascii_art():
	print("""\

	               ._ o o
	               \_`-)|_
	            ,""       \ 
	          ,"  ## |   ಠ ಠ. 
	        ," ##   ,-\__    `.
	      ,"       /     `--._;)
	    ,"     ## /
	  ,"   ##    /
                    """)
	print('*'*40)
	print("AUTOMATED ATTENDANCE MARKER V1.1.2")
	print('*'*40)

########### DOMAIN ###############
URL = 'https://eduserver.nitc.ac.in' 

######### API Endpoints ################
login_api = '/login/index.php'
course_view_api = '/course/view.php' ## takes 'id' as a parameter, ex: /course/view.php?id=1076 for Logic Design Course, 1075 for IP etc.
attendance_view_api = '/mod/attendance/view.php' ## takes 'id' as a parameter
attendance_index_api = '/mod/attendance/index.php' ## takes course 'id' as a parameter
attend_submit_api = '/mod/attendance/attendance.php' ## takes 'sessid' and 'sesskey' as parameter

######### STATIC ATENDANCE ID's ############# 
ip_attendance_id = '29087'
ld_attandance_id = {"monday":"30433","tuesday":"32124","wednesday":"29645","thursday":"29803"} 
pc_attendance_id = '28248'

######### STATIC COURSE ID's ############
ip_course_id = '1075'
ld_course_id = '1076'
pc_course_id = '1322'
dm_course_id = '1030'
stat_course_id = '1031'

######## READING LOGIN DETAILS FROM FILE ###############
credentials = open("credentials.txt","r")
text=credentials.read()
username = text[0:10]
password = text[10:]
credentials.close()

####### READING TODAY'S SCHEDULE ###########
f = open("schedule.txt","r")
lines = f.readlines()
schedule={}
schedule_marked={}
for line in lines:
	line = line.strip()
	line = line.split()
	schedule[line[0]] = line[1]
	schedule_marked[line[1]] = False

###### CREATING A MOODLE SESSION ######
session = requests.Session()
response = session.get(URL)

####### SCRAPING THE 'logintoken' ##########
login_soup = BeautifulSoup(response.content,'html.parser')

#This token had to be scraped from the hidden 'logintoken' element on login page
logintoken = str(login_soup.find('input'))[46:-3]

data = {"logintoken":logintoken,"username":username,"password":password}

##### TRYING TO LOGIN #####
login_response = session.post(URL+login_api,data=data)

# Successfully Logged in at this point, hopefully! if the creds were right. Otherwise no one can help you now XD.

######### GRABBING THE NAME ###########
# This could also tell if the login was successful or not #
sourp = BeautifulSoup(login_response.content,'html.parser')
t = sourp.find('span',attrs={'class':'usertext mr-1'})
display_name=''
try:
	display_name=t.text
except:
	print("\nAn error has occured while logging in! May be just check your credentials?")
	sys.exit()

t = time.localtime()
current_hour = time.strftime("%H",t)
current_time =  time.strftime("%H:%M",t)

########## DOWN HERE GOES THE CODE RESPONSIBLE FOR MARKING MY PRECIOUS ATTENDANCE #########

last_class_hour = str(list(schedule)[-1]).split(":")[0]
last_class_min = str(list(schedule)[-1]).split(":")[1]
marked = False
console_msg = ''
tracked = 'NONE'
retry_count=0
keepalive_cooldown = 10*60
keepalive_marker = time.time()
tracker_cooldown = 15*60
tracker_marker=0
tracking = False
reason_for_exit = 'No classes scheduled now!'
while int(time.strftime("%H")) <= int(last_class_hour): 
	reason_for_exit = "Either error or success..."
	time.sleep(1)
	if tracking:
		time.sleep(9)
	if keepalive_cooldown < (time.time() - keepalive_marker):
		session.get(URL+'/dashboard')
		keepalive_marker = time.time()
	if tracking and tracker_cooldown < (time.time() - tracker_marker):
		tracked = 'NONE'
		tracking = False
		tracker_marker = 0
	os.system('cls' if os.name == 'nt' else 'clear')
	display_ascii_art()
	print("Your are logged in as "+display_name+"\n")
	print("Script running........")
	print("Current Time: "+time.strftime("%H:%M:%S")+"\n")
	print('-'*40)
	for c in schedule_marked:
		print("Course: "+str(c)+" | Attendance Marked: "+str(schedule_marked[c]))
	print('-'*40)
	print("Last Message: "+console_msg)
	if str(time.strftime("%H:%M")) in schedule or tracking:
		if tracked == 'NONE':
			course = schedule[str(time.strftime("%H:%M"))]
		else:
			course = tracked
		if course=='IP' and not schedule_marked[course]:
			attendance_view = session.get(URL+attendance_view_api+'?id='+ip_attendance_id)
			soup = BeautifulSoup(attendance_view.content,'html.parser')
			subm = soup.findAll('a')
			submit_links=[]
			for link in subm:
				if '/attendance/attendance.php?sessid=' in str(link):
					submit_links.append(link)
					break
			if len(submit_links) == 1:
				soup = BeautifulSoup(str(submit_links[0]),'html.parser')
				href = soup.find('a')
				href = str(href['href'])
				href = href.replace("&amp","&")
				submit_page = session.get(str(href))
				soup = BeautifulSoup(submit_page.content,'html.parser')
				inputs = soup.findAll('input',attrs={'class':'form-check-input'})
				status = inputs[0]['value']
				splitted = href.split('?')
				sess_values = splitted[1].split('&')
				sessid=sess_values[0].split("=")[1]
				sesskey=sess_values[1].split("=")[1]
				_qf__mod_attendance_student_attendance_form=1
				mform_isexpanded_id_session=1 
				submitbutton='Save+changes'
				submit_url = href
				data = {"sessid":sessid,"sesskey":sesskey,"sesskey":sesskey,"_qf__mod_attendance_student_attendance_form":_qf__mod_attendance_student_attendance_form,"mform_isexpanded_id_session":mform_isexpanded_id_session,"status":status,"submitbutton":submitbutton}
				submit_response = session.post(submit_url,data)
				console_msg="Hopefully your attendance has been marked in "+course +" "+ time.strftime("%H:%M:%S")
				marked = True
				schedule_marked[course] = True
				tracked = 'NONE'
				retry_count=0
				tracking = False
			else:
				retry_count=retry_count+1
				console_msg = "There is no attendance link of "+course+" at "+time.strftime("%H:%M:%S")+" ! Retry count: "+retry_count
				tracked = 'IP'
				tracking = True
				tracker_marker = time.time()
		elif course == 'LD' and not schedule_marked[course]:
			day = time.strftime("%A",t)
			attendance_view = session.get(URL+attendance_view_api+'?id='+ld_attandance_id[str(day).lower()])
			soup = BeautifulSoup(attendance_view.content,'html.parser')
			subm = soup.findAll('a')
			submit_links=[]
			for link in subm:
				if '/attendance/attendance.php?sessid=' in str(link):
					submit_links.append(link)
					break
			if len(submit_links) == 1:
				soup = BeautifulSoup(str(submit_links[0]),'html.parser')
				href = soup.find('a')
				href = str(href['href'])
				href = href.replace("&amp","&")
				submit_page = session.get(str(href))
				soup = BeautifulSoup(submit_page.content,'html.parser')
				inputs = soup.findAll('input',attrs={'class':'form-check-input'})
				status = inputs[0]['value']
				splitted = href.split('?')
				sess_values = splitted[1].split('&')
				sessid=sess_values[0].split("=")[1]
				sesskey=sess_values[1].split("=")[1]
				_qf__mod_attendance_student_attendance_form=1
				mform_isexpanded_id_session=1
				submitbutton='Save+changes'
				submit_url = href
				data = {"sessid":sessid,"sesskey":sesskey,"sesskey":sesskey,"_qf__mod_attendance_student_attendance_form":_qf__mod_attendance_student_attendance_form,"mform_isexpanded_id_session":mform_isexpanded_id_session,"status":status,"submitbutton":submitbutton}
				submit_response = session.post(submit_url,data)
				console_msg="Hopefully your attendance has been marked in "+course+" "+ time.strftime("%H:%M:%S")
				marked = True
				schedule_marked[course] = True
				tracked = 'NONE'
				retry_count=0
				tracking = False
			else:
				retry_count=retry_count+1
				console_msg = "There is no attendance link of "+course+" at "+time.strftime("%H:%M:%S")+" ! Retry count: "+retry_count
				tracked = 'LD'
				tracking = True
				tracker_marker = time.time()
		elif course == 'PC' and not schedule_marked[course]:
			attendance_view = session.get(URL+attendance_view_api+'?id='+pc_attendance_id)
			
			soup = BeautifulSoup(attendance_view.content,'html.parser')
			subm = soup.findAll('a')
			submit_links=[]
			for link in subm:
				if '/attendance/attendance.php?sessid=' in str(link):
					submit_links.append(link)
					break
			if len(submit_links) == 1:
				soup = BeautifulSoup(str(submit_links[0]),'html.parser')
				href = soup.find('a')
				href = str(href['href'])
				href = href.replace("&amp","&")
				submit_page = session.get(str(href))
				soup = BeautifulSoup(submit_page.content,'html.parser')
				inputs = soup.findAll('input',attrs={'class':'form-check-input'})
				status = inputs[0]['value']
				splitted = href.split('?')
				sess_values = splitted[1].split('&')
				sessid=sess_values[0].split("=")[1]
				sesskey=sess_values[1].split("=")[1]
				_qf__mod_attendance_student_attendance_form=1
				mform_isexpanded_id_session=1
				submitbutton='Save+changes'
				submit_url = href
				data = {"sessid":sessid,"sesskey":sesskey,"sesskey":sesskey,"_qf__mod_attendance_student_attendance_form":_qf__mod_attendance_student_attendance_form,"mform_isexpanded_id_session":mform_isexpanded_id_session,"status":status,"submitbutton":submitbutton}
				submit_response = session.post(submit_url,data)
				console_msg="Hopefully your attendance has been marked in "+course+" "+ time.strftime("%H:%M:%S")
				marked = True
				schedule_marked[course] = True
				tracked = 'NONE'
				retry_count=0
				tracking = False
			else:
				retry_count=retry_count+1
				console_msg = "There is no attendance link of "+course+" at "+time.strftime("%H:%M:%S")+" ! Retry count: "+retry_count
				tracked = 'PC'
				tracking = True
				tracker_marker = time.time()
		elif course == 'DM' and not schedule_marked[course]:
			course_view = session.get(URL+course_view_api+'?id='+dm_course_id)
			marked = False
			dm_soup = BeautifulSoup(course_view.content,'html.parser')
			all_links = dm_soup.findAll('a',attrs={'class':'aalink'})
			attendance_links=[]
			for link in all_links:
				if '/mod/attendance/view.php?id=' in str(link):
					attendance_links.append(link)
			soup = BeautifulSoup(str(attendance_links[-1]),'html.parser')
			href = soup.find('a')
			resp = session.get(str(href['href']))
			soup = BeautifulSoup(resp.content,'html.parser')
			subm = soup.findAll('a')
			submit_links=[]
			for link in subm:
				if '/attendance/attendance.php?sessid=' in str(link):
					submit_links.append(link)
					break
			if len(submit_links) == 1:
				soup = BeautifulSoup(str(submit_links[0]),'html.parser')
				href = soup.find('a')
				href = str(href['href'])
				href = href.replace("&amp","&")
				submit_page = session.get(str(href))
				soup = BeautifulSoup(submit_page.content,'html.parser')
				inputs = soup.findAll('input',attrs={'class':'form-check-input'})
				status = inputs[0]['value']
				splitted = href.split('?')
				sess_values = splitted[1].split('&')
				sessid=sess_values[0].split("=")[1]
				sesskey=sess_values[1].split("=")[1]
				_qf__mod_attendance_student_attendance_form=1
				mform_isexpanded_id_session=1
				submitbutton='Save+changes'
				submit_url = href
				data = {"sessid":sessid,"sesskey":sesskey,"sesskey":sesskey,"_qf__mod_attendance_student_attendance_form":_qf__mod_attendance_student_attendance_form,"mform_isexpanded_id_session":mform_isexpanded_id_session,"status":status,"submitbutton":submitbutton}
				submit_response = session.post(submit_url,data)
				console_msg="Hopefully your attendance has been marked in "+course+" "+ time.strftime("%H:%M:%S")
				marked = True
				schedule_marked[course] = True
				tracked = 'NONE'
				retry_count=0
				tracking = False
			else:
				retry_count=retry_count+1
				console_msg = "There is no attendance link of "+course+" at "+time.strftime("%H:%M:%S")+" ! Retry count: "+retry_count
				tracked = 'DM'
				tracking = True
				tracker_marker = time.time()
		elif course == 'SM' and not schedule_marked[course]:
			course_view = session.get(URL+course_view_api+'?id='+stat_course_id)
			marked = False
			dm_soup = BeautifulSoup(course_view.content,'html.parser')
			all_links = dm_soup.findAll('a',attrs={'class':'aalink'})
			attendance_links=[]
			for link in all_links:
				if '/mod/attendance/view.php?id=' in str(link):
					attendance_links.append(link)
			soup = BeautifulSoup(str(attendance_links[-1]),'html.parser')
			href = soup.find('a')
			resp = session.get(str(href['href']))
			soup = BeautifulSoup(resp.content,'html.parser')
			subm = soup.findAll('a')
			submit_links=[]
			for link in subm:
				if '/attendance/attendance.php?sessid=' in str(link):
					submit_links.append(link)
					break
			if len(submit_links) == 1:
				soup = BeautifulSoup(str(submit_links[0]),'html.parser')
				href = soup.find('a')
				href = str(href['href'])
				href = href.replace("&amp","&")
				submit_page = session.get(str(href))
				soup = BeautifulSoup(submit_page.content,'html.parser')
				inputs = soup.findAll('input',attrs={'class':'form-check-input'})
				status = inputs[0]['value']
				splitted = href.split('?')
				sess_values = splitted[1].split('&')
				sessid=sess_values[0].split("=")[1]
				sesskey=sess_values[1].split("=")[1]
				_qf__mod_attendance_student_attendance_form=1
				mform_isexpanded_id_session=1
				submitbutton='Save+changes'
				submit_url = href
				data = {"sessid":sessid,"sesskey":sesskey,"sesskey":sesskey,"_qf__mod_attendance_student_attendance_form":_qf__mod_attendance_student_attendance_form,"mform_isexpanded_id_session":mform_isexpanded_id_session,"status":status,"submitbutton":submitbutton}
				submit_response = session.post(submit_url,data)
				console_msg="Hopefully your attendance has been marked in "+course+" "+ time.strftime("%H:%M:%S")
				marked = True
				schedule_marked[course] = True
				tracked = 'NONE'
				retry_count=0
				tracking = False
			else:
				retry_count=retry_count+1
				console_msg = "There is no attendance link of "+course+" at "+time.strftime("%H:%M:%S")+" ! Retry count: "+retry_count
				tracked = 'SM'
				tracking = True
				tracker_marker = time.time()

####### DONE WITH THE ATTENDANCE, NOW EXITING ###########
os.system('cls' if os.name == 'nt' else 'clear')
display_ascii_art()
print("Exiting the program in 2s...")
print("Reason: "+reason_for_exit)
time.sleep(2)

