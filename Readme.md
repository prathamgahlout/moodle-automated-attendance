# Automated Attendance Marker

### Description

A python script to automate the task of loging into the eduserver of Nit calicut and marking the attendance manually. Many would agree that it is rather a tough task especially for the morning 8'O clock
classes. 

---

### Requirements

This script would require Python3 to be installed on your machine/mobile device.
In addition to this it requires the python requests module and BeautifulSoup to be there in your machine.

1. Download and install Python from [here](https://www.python.org/downloads/)

After it has been successfully installed, pip install these modules,

`$ pip install requests`

`$ pip install beautifulsoup4`


And you are good to go...

---

### Usage

There is a **credentails.txt** file. Save your login details in that file as space seperated value.
For example,

`m2xxxxxca my_weak_password`

The **schedule.txt** file must contain the schedule of that day. The format is,

*_TIME_ <SPACE> _COURSE_CODE_*

Enter each course time on a new line.
For example on a certain day the file would look like this,

**08:00 IP\
  12:30 PC\
  13:00 LD\
  14:00 DM\
  17:00 STAT**

**Note: Use 24-Hour time format. Otherwise it won't work and don't blame me if you loose your attendance. And please save the schedule in an ascending order of time. This is also must for correct functioning.**

Keep in mind that you have to daily update the schedule.txt file only.

Now just fire it up with,

`$ python RunScript.py`

---

### A message to the users

If you think it is not working perfectly for you, please feel free to contact me or just raise an issue. You can also take the code and customize it for your own use case.
