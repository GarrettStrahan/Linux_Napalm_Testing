#Programmed with Python 3.6, with Ubuntu 18.04.2 LTS. I have the Windows 10 version this does the same thing at my github up at my github.

from napalm import get_network_driver
import os
import shutil
import re
from datetime import datetime
import mynapalmfunctions



ipaddr = input("What is the IP-Address?")
username = input("What is the username?")
password = input("What is the password?")

junos_driver = get_network_driver('junos')
junos_device = {'username': username, 'password': password, 'hostname': ipaddr}


with junos_driver(**junos_device) as junos:
  shrun = junos.get_config()


with junos_driver(**junos_device) as junos:
  interfaces = junos.get_interfaces()

log = ['show log']
with junos_driver(**junos_device) as junos:
    logs = junos.cli(log)

commands = ['show version', 'show chassis hardware'] #These commands have the serial # + model #, just need to parse the data

with junos_driver(**junos_device) as junos:
    commands = junos.cli(commands)

mynapalmfunctions.writetohdd(interfaces, shrun, logs, commands) #This is creating files with SSH data
serialnum = mynapalmfunctions.parsingdata() #This is getting serial #
serialnum = re.sub(r'[^\w]', ' ', serialnum)
serialnum = serialnum.strip()

foldercreation = r'/tmp/Testing'
today = datetime.now
startfolder = r"/tmp/Testing/{}".format(today().strftime('%m-%d-%Y-')) + serialnum

if os.path.exists(foldercreation) == False: #this is checking to see if the sub folder exists
    os.mkdir(foldercreation)
    print ("Did the first function start?")
    os.system('mkdir {}'.format(foldercreation))

if os.path.exists(foldercreation) == True:
    if os.path.exists(startfolder) == False:
        os.mkdir(startfolder)
        os.system('mkdir {}'.format(startfolder))

# os.mkdir(FILLTHISOUTLATER) #You want folder to be Hostname.MODEL#.SERIAL  #WILL DO THIS LATER WITH ANOTHER LATER VERSION, SERIAL CHECK! NEED HOSTNAME + MODEL#s

startfolder = startfolder + "/"

newfilename = startfolder  + "Logs.txt"
shutil.move("Logs.txt", newfilename)
newfilename = startfolder + "Running-Config.txt"
shutil.move("Running-Config.txt", newfilename)
newfilename = startfolder + "Interfaces.txt"
shutil.move("Interfaces.txt", newfilename)
newfilename = startfolder  + "Commands.txt"
shutil.move("Commands.txt", newfilename)

print("Your files have been moved to /tmp/Testing/")
print("The full file path is {}".format(startfolder))
