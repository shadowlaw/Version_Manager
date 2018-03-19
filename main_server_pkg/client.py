#Client initiation


#BASIC HELLO SERVER, REFACTORING TO FIT OUR NEEDS, UNFINISHED!!!!
import socket, sys
import json
import requests
import os
from pathlib import Path
import subprocess
import getpass

HOST, PORT = "localhost", 9999

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
    HOST= input("Please enter HOST address, without any routes: ")
    AuthKey= input("Please enter Authentication Key: ")
    password = getpass.getpass()   
    print (password)
    print(bcolors.OKGREEN +"Contacting server"+bcolors.ENDC )
    url=HOST +"/node_init_auth" #route for new authentication
    
    bashCommand = "hostname"
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    machine_name= output
    data1= {"key": AuthKey}
    data = {"machine_name": machine_name, "node_auth_code": AuthKey, "new_pass": password}
    
    msg=json.dumps(data1)
    response = requests.post(url,data1)
    print(response.status_code)
    print(response.json())
    if response.json() != {}:
        print("The server sent a response:")
        #THE RESPONSE IS THE API KEY AND IS STORED IN PLAIN TEXT
        
        r= json.loads(response.json())
        AuthF= open("authkey.txt", "w")
        AuthF.write(r["key"])
        print("the authentication key was written to the file")
        
        #YOU THEN REPLY WITH THE MACHINE NAME, API KEY, PASSWORD
        #NEW URL
        try:
            data ={"machine_name": machine_name, "node_auth_code": r["key"], "new_pass": password}
            print("authentication key is in the data being sent")
            response= requests.post(url,json=json.dumps(data))
            print(response)
        except:
            print("The connection failed, sorry.")
            input("Press enter to retry")
            newClient()
    elif response.json()=={}:
            print(bcolors.FAIL+"Sorry, the authentication failed, please try again.")
            input("Please press enter to try again."+bcolors.ENDC)
            newClient()
        
        
        
        
        

def main():
    # if authkey file doesn't exists, say you're new to server.
    my_file= Path("authkey.txt")
    if my_file.is_file():
        # take the authentication key stored and use it for any response
        print(bcolors.OKGREEN + "I'm a known client"+bcolors.ENDC) #colour = OKGREEN 
        #update server about information
        print(bcolors.BOLD+"Updating server about current packages installed"+bcolors.ENDC)
        #get auth key and send list of packages installed to server
    else:
        newClient()
        
#start client connection
#send "hi, I'm new message to server"

if __name__ == "__main__":
    main()