def read_file(filename, mode):
    try:
        with open(filename, mode) as stream:
            data = stream.read()
            
        return data
    except Exception as e:
        print e
        return ""