import re
import csv


def parser(logfile):
    """This is a function that parses the log file and saves the relevant information to a CSV file"""
    with open('output.csv', 'w') as csvfile:
        #Create Headers in the CSV file
        header = ['IP', 'Data Size', 'Date Time', 'Status', "Words"]
        writer = csv.writer(csvfile)
        writer.writerow(header)
        
        #Use Regex to get the information needed line by line
        with open(logfile + '.log', 'r') as log_file:
            for line in log_file:
                ipregex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                datasizenumregex = r'(?<=\d ).\d{1,5}(?= ")'
                statusregex = r'(?<=" ).\d{1,3}(?= )'
                datetimeregex = r'\d{2}/\w\w\w/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}'
                wordsregex = r'(?<="GET |POST |HEAD )(.*)(?= HTTP)'

                ip = re.findall(ipregex, line)
                status = re.findall(statusregex, line)
                datasize = re.findall(datasizenumregex, line)
                datetime = re.findall(datetimeregex, line)
                words = re.findall(wordsregex, line)
                #Check if the Data size is empty
                if len(datasize) == 0:
                    #Leave column blank if Data size is empty
                    datasize.append('')
                #Join the outputs of Regex into one list and write it as a row into the CSV file
                joinedlist = ip + datasize + datetime + status + words
                writer.writerow(joinedlist)

parser('access copy')