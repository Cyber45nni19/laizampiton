import re
import csv
import pandas as pd


def parser(logfile): #Ensure that access log is in the same directory before runningc
    """This is a function that parses the log file and saves the relevant information to a CSV file"""
    with open('output.csv', 'w') as csvfile:
        #Create Headers in the CSV file
        header = ['IP', 'Data Size', 'Date Time', 'Status', 'URL']
        writer = csv.writer(csvfile)
        writer.writerow(header)
        
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

                #Join the outputs of Regex into one list and write it as a row into the CSV file
                joinedlist = ip + datasize + datetime + status + url
                writer.writerow(joinedlist)

def sqlinjectionchecker(filename):
    '''This function searches the csvfile for any columns that contain the specified string and output them'''
    df = pd.read_csv(filename+'.csv')

    #Add keywords filter her
    stringtofind = ['union\%20select', '/etc/passwd']

    #Find specified string in the Words column and show them
    export = df[df["URL"].str.lower().str.contains('|'.join(stringtofind), na=False)]

    #Filter attacks by Status Codes 2XX  and 3XX
    successfulcode = export[(export.Status >= 200) & (export.Status <= 299)]
    redirectedcode = export[(export.Status >= 300) & (export.Status <= 399)]
    print 'SQL Injection: %d Attacks Successful and %d Attempted Attacks redirected' %(successfulcode.shape[0],redirectedcode.shape[0])

    #Export to CSV
    export.to_csv(r'export_dataframe.csv', index=None, header=True)

