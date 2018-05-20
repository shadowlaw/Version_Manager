import os

def read(fileName):
    
    try:
        with open(fileName, "r") as stream:
            return stream.read()
    except Exception as e:
        print e
        return ''
        
def write(fileName, data, overWrite=False):
    
    mode ='a'
    
    if overWrite == True:
        mode = 'w'
        
    with open(fileName, mode) as stream:
        stream.write(data)


def exists(file_path):
    if os.path.exists:
        return True

    return False