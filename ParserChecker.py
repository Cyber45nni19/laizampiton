import re
import csv
import pandas as pd
import numpy as np

def parser(logfile): #Ensure that access log is in the same directory before runningc
    """This is a function that parses the log file and saves the relevant information to a CSV file"""
    joinedlist = list()
    #Use Regex to get the information needed line by line
    with open(logfile + '.log', 'r') as log_file:
        for line in log_file:
            ipregex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            datasizenumregex = r'(?<=\d ).\d{1,5}(?= ")'
            statusregex = r'(?<=" ).\d{1,3}(?= )'
            datetimeregex = r'\d{2}/\w\w\w/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}'
            wordsregex = r'(?<= ")(.*)(?= HTTP/)'

            ip = re.findall(ipregex, line)
            status = re.findall(statusregex, line)
            datasize = re.findall(datasizenumregex, line)
            datetime = re.findall(datetimeregex, line)
            url = re.findall(wordsregex, line)

            #Check if the Data size is empty
            if len(datasize) == 0:
                #Leave column blank if Data size is empty
                datasize.append('')

            #Join the outputs of Regex into one list to use in dataframe
            joinedlist.append(ip + datasize + datetime + status + url)

    df = pd.DataFrame(joinedlist, columns=['IP', 'Data Size', 'Date Time', 'Status', 'URL'])
    return df

def attackchecker(df, dict):
    '''This function searches the csvfile for any columns that contain the specified string and output them'''
    #Search for attacks that the user specified
    sqlinjectstring = lfistring = rfistring = xssstring = list()
    #Search if URL contains keywords
    if dict['sql'] == 1:
        sqlinjectstring = ['union%20select', '%27', "' or 1=1--"]

    if dict['lfi'] == 1:
        lfistring = ['\/\.\.','/etc/passwd','/etc/issue','proc/version','etc/profile','etc/passwd','etc/passwd','etc/shadow','root/.bash_history','var/log/dmessage','var/mail/root','var/spool/cron/crontabs/root']

    if dict['rfi'] == 1:
        rfistring = ['$_post', 'include\(', 'page\=']

    if dict['xss'] == 1:
        xssstring = ['<script>','%3cscript%3','&title=','javascript:','onerror\=','onload\=','%3c','<']


    stringtofind = sqlinjectstring+lfistring+rfistring+xssstring
    print stringtofind
    #Find specified string in the Words column and show them
    export = df[df["URL"].str.lower().str.contains('|'.join(stringtofind), na=False)]
    successfulcode = export[export['Status'] == '200']
    redirectedcode = export[export['Status'] == '301']
    #Filter attacks by Status Codes 2XX  and 3XX
    print 'Results: %d Attacks Successful and %d Attempted Attacks redirected' %(successfulcode.shape[0],redirectedcode.shape[0])

    # Export to CSV
    export.to_csv(r'export_dataframe.csv', index=None, header=True)

mydict = {'xss':1, 'sql':0, 'rfi':0, 'lfi':0}
attackchecker(parser('accesssmall'), mydict)