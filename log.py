import datetime

file_name = "Binary_search.log"
fh = open(file_name,"w")
fh.close()

def open_file(file_name,message) :
        fh = open(file_name,"a")
        TEXT = '%s : INFO : %s \n' % (datetime.datetime.now(),message)
        fh.write(TEXT)
        fh.close()

def info(message) :
        open_file(file_name,message)
