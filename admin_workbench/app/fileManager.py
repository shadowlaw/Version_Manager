def read_file(absolutePath):
    try:
        with open(absolutePath, "r") as stream:
            data = stream.read()
            
        return data
    except Exception as e:
        print e
        return ""
        
def write_to(absolutePath, data):
    try:
        with open(absolutePath, "w") as stream:
            stream.write(data)
    except Exception as e:
        print e
        return ""