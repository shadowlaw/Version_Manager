import requests

class FileDistrib:
    __ip_list__ = []
    __fileName__ = ""

    def __init__(self, ip_list=[], fileName=""):
        self.__ip_list__ = ip_list
        self.__fileName__ = fileName


    def setIpList(self, ip_list):
        self.__ip_list__ = ip_list

    def addIP(self, ip_address):
        self.__ip_list__.append(ip_address)

    def setFilename(self, fileName):
        
        if fileName != "" or fileName is not None:
            self.__filName__ = fileName
    
    def send(self, relativeUrl=""):
        
        if self.__fileName__ == "" or self.__fileName__ is None:
            return False

        for ipAddress in self.__ip_list__:
            
            protocol=""
            
            if("http" not in ipAddress.split(":")[0]):
                protocol = "http://"
            
            try:
            	stream = open(self.__fileName__, "rb")
            	file = {"file": stream}
            	
            	requests.post(protocol+ipAddress+"/"+relativeUrl, files=file, headers={"enctype": "multipart/form-data"}, timeout=(3, None))

            	stream.close()
            except Exception as e:
                pass

