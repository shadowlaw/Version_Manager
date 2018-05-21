#Client initiation


import socket, sys
import json
import requests
import os
from pathlib import Path
import subprocess
from pathlib2 import Path
import time
from requests.exceptions import ConnectionError

import apps

#THERE IS REPEATED CODE, REFACTOR!!!

class bcolors: #SOME COLOUR TO TERMINAL
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
'''

'''
def newClient():
    HOST= raw_input("Please enter HOST address, without any routes: ")
    AuthKey= raw_input("Please enter Authentication Key: ")
    print(bcolors.OKGREEN +"Contacting server"+bcolors.ENDC )
    '''process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    machine_name= output'''
    serverSuccessfulOnce=False
    while True:
        appz= apps.getApps()
        data = {
                "key": AuthKey
               }
        data.update(appz)
        if apps.internet_up():
            #CONNECTIONERROR
            try:
                response = requests.post(HOST,json=data, headers={"Content-Type": "application/json"})
                #, headers={"Content-Type":"application/json
                if response.json() != {}:
                    print("The server sent a response:")
                    print(response.json())
                    #THE RESPONSE IS THE API KEY AND IS STORED IN PLAIN TEXT
                    
                    AuthF= open("authkey.txt", "w")
                    AuthKey+=";"
                    AuthF.write(AuthKey)
                    AuthF.write(HOST)
                    AuthF.close()
                    command= apps.makeUpdates(response.json())
                    #save task in case of powerloss or reboot
                    TFile= open("task.txt", "w")
                    TFile.write(command)
                    TFile.close()
                    #run changes
                    fin,fout=os.popen4(command)
                    print(fout.read())
                    os.remove("task.txt")
                    print("Task file has been removed and tasks completed")
                    time.sleep(10) #wait for a five minutes before doing the loop again
                    
                else:
                    print(bcolors.FAIL+"Sorry, the authentication failed, please try again.")
                    ANSWER= raw_input("If you'd like to retry with a new host address(Y/N)"+bcolors.ENDC)
                    if ANSWER.lower()=="y":
                        HOST= raw_input("Please enter HOST address, without any routes: ")
                        AuthKey= raw_input("Please enter Authentication Key: ")
                    else:
                        print('retrying')
            except ConnectionError as e:
                print(e)
                print(bcolors.FAIL+"It seems there was a error connecting to the server"+bcolors.ENDC)
                if serverSuccessfulOnce==False:
                    print("Would you like to change the server address.")
                print("Waiting 5 minutes before trying again")
                time.sleep(10)
        else:
            print("Possibly the internet is down, let's wait a bit(5 minutes).")
            time.sleep(10)
        
        #requests.post(http://whatevermusthappenismadness.com/)
        #http://whatevermusthappenismadness.com/
#Run this is the client is already has an authkey        
def oldClient():
    theString=""
    #pull up authkey and host address from 
    with open('authkey.txt') as AF:
        for line in AF:
            theString+=line
    
    
    AuthKey, HOST = theString.split(";")
    task = Path('task.txt')
    command=""
    while True:
        #If there is a task that was uncompleted then do the task
        if task.is_file():
            with open('task.txt') as f:
                command = f.readlines()
        
            fin, fout = os.popen4(command)
            os.remove('task.txt')
        else:
            #update the server as usual 
            appz= apps.getApps()
            data = {
                    "key": AuthKey
                   }
            data.update(appz)
            serverSuccessfulOnce=False
            try:
                response = requests.post(HOST,json=data, headers={"Content-Type": "application/json"})
                #, headers={"Content-Type":"application/json
                serverSuccessfulOnce=True
                if response.json() != {}:
                    print("The server sent a response:")
                    print(response.json())
                    #THE RESPONSE IS THE API KEY AND IS STORED IN PLAIN TEXT
                    command= apps.makeUpdates(response.json())
                    #save task in case of powerloss or reboot
                    TFile= open("task.txt", "w")
                    TFile.write(command)
                    TFile.close()
                    #run changes
                    fin,fout=os.popen4(command)
                    print(fout.read())
                    os.remove("task.txt")
                    print("Task file has been removed and tasks completed")
                    time.sleep(10) #wait for a five minutes before doing the loop again
                    
                else:
                    print(bcolors.FAIL+"Sorry, the authentication failed, please try again."+bcolors.ENDC)
                    print('retrying')
            except ConnectionError as e:
                print(e)
                print(bcolors.FAIL+"It seems there was a error connecting to the server"+bcolors.ENDC)
                if serverSuccessfulOnce==False:
                    print("Would you like to change the server address.")
                print("Waiting 5 minutes before trying again")
                time.sleep(10)
            
    
def main():
    # if authkey file doesn't exists, say you're new to server.
    apps.printMenu()
    my_file= Path("authkey.txt")
    if my_file.is_file():
        # take the authentication key stored and use it for any response
        oldClient()
    else:
        newClient()
        
#start client connection
#send "hi, I'm new message to server"

if __name__ == "__main__":
    main()