#Client
import subprocess
import json
import os
import urllib2
import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

'''
Should refactor to make it an object that can be used for all basic app, version request and is there an available update, etc
'''
appsAndVersions= {"apps":{}}
'''
JSON Array CONSTRUCT:

HOW I'M ASSUMING THE RESPONSE STRUCTURE WILL TYPICALLY BE
{
    "key": key,
    
    "command": whateverTheCommandIs,
    
    "data":[listofdata]
} 

HOW THE JSON RESPONSE STRUCTURE IS NOW FOR GETTING THE LIST OF APPS

{
    "apps":
        [{
            "name": a,
            "version": b
         },
         {
            "name": a,
            "version": b
         }
        ]
}
'''

#cmd = subprocess.Popen('dpkg-query --show',shell = True, stdout=subprocess.PIPE)

'''
For each line of output:
    split the string, remove all spaces and add it to the dictionary
When dictionary is complete, convert to JSON and at pump to server.

'''
def printMenu():
    cprint(figlet_format('NETDATE', font='smisome1'),
       'yellow', 'on_red', attrs=['bold'])

def getApps():
    #Runs the command to show all apps and their version
    fin,fout=os.popen4("dpkg-query --show")

    #converts the results to a string 
    stdOUT= fout.read()

    #converts the string to a list each line of output (the app and it's version)
    stdlist = stdOUT.splitlines()

    #For each line, split the string and put the result in the appsAndVersions dictionary. (DICTIONARYS CAN BE EASILY CONVERTED TO JSON)
    for line in stdlist:
        a, b= line.split()[0], line.split()[1] #AUTOMATICALLY REMOVES ALL SPACES
        c= {a:b}
        appsAndVersions["apps"].update(c)
    return appsAndVersions

    #convert to JSON array and return



#apt-get install application=version
''' 
This command will install each one whether or not the other was completed.
This will allow for error handling later on for each app and prevent one apps failure to install from stopping progress

It auto-answers yes to any possible options and allows to install packages independently
'''
def makeUpdates(appDict):
    finalString=""
    #takes the dictionary of apps and creates a string with the final shell command
    if appDict['changes'] != {}:
        for x in appDict['changes']:
            if appDict['changes'][x]=='0':
                 if finalString=="":
                    finalString+='sudo apt-get -y install {}'.format(x)
                else:
                    finalString+='; sudo apt-get -y install {}'.format(x)
            else:
                if finalString=="":
                    finalString+='sudo apt-get -y install {}={}'.format(x,appDict['changes'][x])
                else:
                    finalString+='; sudo apt-get -y install {}={}'.format(x, appDict['changes'][x])
    
    if appDict['install'] != {}:
        for x in appDict['install']:
            if appDict['install'][x]=="0":
                if finalString=="":
                    finalString+='sudo apt-get -y install {}'.format(x)
                else:
                    finalString+='; sudo apt-get -y install {}'.format(x)
            else:
                if finalString=="":
                    finalString+='sudo apt-get -y install {}={}'.format(x, appDict['install'][x])
                else:
                    finalString+='; sudo apt-get -y install {}={}'.format(x, appDict['install'][x])
    return finalString
    
#TEST IF THE INTERNET IS CONNECTED BY CHECKING IF GOOGLE IS ACCESSIBLE :/
def internet_up():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False