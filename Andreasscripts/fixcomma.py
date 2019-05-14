import os
import re


def main():
    filelist = os.popen("ls |grep .txt").read()
    filelist = filelist.rstrip()
    test = re.split('\n',filelist)
    for files in test:
        newdata = os.popen("cat %s" %files).read()
        newdata = newdata[:-1]
        f = open("fixedfiles/%s" %files, 'a')
        f.write("%s" %newdata)
        f.close()
    
    
    
main()
