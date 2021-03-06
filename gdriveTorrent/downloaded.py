#!/usr/bin/python

'''
This script will be run automatically on-bt-download-complete of aria2c i.e. when the torrent is successfully downloaded.
It gets a list of files into your downloads directory and uploads them one by one to your google drive.
'''

import os
import sys
from subprocess import Popen
import subprocess
import commands
from gdriveTorrent import settings

f = open('done.txt','a')
f.write('\nFILES: ')

def uploadFiles():
    #Get list of files in download folder
    path = settings.BASE_DIR + '/downloads/'
    files = os.listdir(path)
    for fileName in files:
        f.write(fileName)

        #Run gdrive command and upload the file:"./downloads/fileName" to gdrive
        script = 'gdrive upload  "%s%s" --recursive'%(path,fileName)
        process = Popen(script, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #Delete the uploaded file from ./downloads folder, after the subprocess is completed
        poll = process.poll()
        while poll == None:
            poll = process.poll()
            continue
        result = process.communicate()[0]
        if 'Failed' not in result:
            #File successfully uploaded, delete it now
            script = 'rm -rf "%s%s"'%(path,fileName)
            os.system(script)
        else:
            #gdrive script failed, try again
            #NOTE: This may cause the script to run for a long time if API quota is exhausted, but it won't delete those files from server that have not successfully been uploaded.
            continue


#If another instance of this script is already running, exit
def running():
    script_name = 'downloaded.py'
    try:
        l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'| awk '{print $2}'" % script_name)
    except:
        return False
    if l[1] != '\n' and l[1]:
        print 'Already running'
        return True
    else:
        print 'Not Running'
        return False

if not running():
    uploadFiles()
