import requests
import os


class FileDistrib:
    __ip_list__ = []
    __fileName__ = ""

    def __init__(self, ip_list=[], fileName=""):
        self.__ip_list__ = ip_list
        self.__fileName__ = fileName

    def isListEmpty(self):
        return self.__ip_list__ == ['']

    def setIpList(self, ip_list):
        self.__ip_list__ = ip_list

    def addIP(self, ip_address):
        self.__ip_list__.append(ip_address)

    def setFilename(self, fileName):
        
        if fileName != "" or fileName is not None:
            self.__filName__ = fileName
    
    def send(self, ipAddress, relativeUrl=""):
        
        protocol=""
            
        if("http" not in ipAddress.split(":")[0]):
            protocol = "http://"
        
        try:
        	stream = open(self.__fileName__, "rb")
        	file = {"file": stream}
        	
        	requests.post(protocol+ipAddress+"/"+relativeUrl, files=file, headers={"enctype": "multipart/form-data"}, timeout=(3, None))

        	stream.close()
        	
        	return True
        except Exception as e:
            pass
    
    
    def send_all(self, relativeUrl=""):
        
        for ipAddress in self.__ip_list__:
            self.send(ipAddress, relativeUrl)
            
        return True
    
    def file_exist(self):
            
        if not os.path.exists(self.__fileName__):
            return False
            
        return True
    