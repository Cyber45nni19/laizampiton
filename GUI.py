import Tkinter, ttk, tkFileDialog
from ParserChecker import *
from Hash import *
from Graph import *

# Variable for the access log
logpath = ""

# Variable for the location to export log file
savepath = ""

# Variable to know if a log has been selected
selected = False
selected2 = False



# Function to browse logs when clicked
def selectlog():
    global selected
    window.filename = tkFileDialog.askopenfilename(initialdir="C:/", title="Select Access Log")
    window.label = ttk.Label(Pathnamelabel, text="")
    if window.filename != "":
        Pathnamelabel.configure(text=window.filename)
        selected = True
    else:
        Pathnamelabel.configure(text="No logs selected!")
        selected = False


# Function to allow user to choose where to save the exports, default is C:\\
def save():
    global selected2
    window.path = tkFileDialog.askdirectory()
    window.label2 = ttk.Label(Savenamelabel, text="")
    if window.path != "":
        Savenamelabel.configure(text=window.path)
        selected2 = True
    else:
        Savenamelabel.configure(text="No export location selected!")
        selected2 = False


# If analyzed button is clicked, the path of the log file is put into a variable so it can be analyzed
isclicked = False


def clicked():
    global isclicked
    global logpath
    global savepath

    path = Pathnamelabel.cget("text")
    save = Savenamelabel.cget("text")

    # assign checkbox values to dic
    dict['sql'] = sql.get()
    dict['lfi'] = lfi.get()
    dict['rfi'] = rfi.get()
    dict['xss'] = xss.get()

    atleastone = sum(dict.itervalues())

    print "How many selected? " + str(atleastone)
    print "which options? " + str(dict)

    format = path.endswith('.log')
    print "Correct format?" + str(path.endswith('.log'))
    # if valid and got selected
    if selected == True and selected2 == True and format == True and atleastone >= 1:
        logpath = path
        isclicked = True
    else:
        isclicked = False
        statuslabel.configure(text="There is an invalid setting!")

    # assign the save location to the variable
    savepath = save

    print "Analyzed is clicked, proceed to analyze? : " + str(isclicked)
    print "Got log file selected already? : " + str(selected)
    print "Got save location selected already? : " + str(selected2)

    print "Final logpath : " + str(logpath)
    print "Final Export Directory : " + str(savepath)



    if isclicked == True:
        print "Scanning"
        export = attackchecker(parser(logpath), savepath, dict)
        mylist = showflaggedIP(parser(logpath), export)

        print "Hashing"
        filetohash = savepath + '/Suspicious_Actions.csv'
        filetohash2 = savepath + '/FlaggedIPActions.csv'
        txt1 = hashing(filetohash)
        txt2 = hashing(filetohash2)

        text_file1 = open(savepath + "/MD5 of Suspicious_Actions.txt", "w")
        text_file1.write(txt1)
        text_file1.close()

        text_file2 = open(savepath + "/MD5 of FlaggedIPActions.txt", "w")
        text_file2.write(txt2)
        text_file2.close()

        statuslabel.configure(text="Completed!")

        print "Plotting Graph"
        plotgraph(mylist)

# GUI Window.
window = Tkinter.Tk()
window.title("Access Log Analyzer")

window.geometry("500x100+300+300")
window.minsize(300, 300)

# Frame of GUI
top_frame = Tkinter.Frame(window).pack()
bottom_frame = Tkinter.Frame(window).pack(side="bottom")
button_frame = Tkinter.Frame(window)
button_frame.pack(side="bottom", fill="x", expand=False)


# Button to find logs
logbutton = Tkinter.Button(top_frame, text="Browse access log", command=selectlog)
logbutton.pack()

# Label to indicate what log has been selected
Pathnamelabel = Tkinter.Label(top_frame, text="No Access log selected yet", pady=10)
Pathnamelabel.pack()


# Button to choose save path
savebutton = Tkinter.Button(top_frame, text="Choose directory of export", command=save)
savebutton.pack()

# Label to indicate what save location has been selected
Savenamelabel = Tkinter.Label(top_frame, text="No export location", pady=10)
Savenamelabel.pack()

# Variable to know what has been selected in checkbox
sql = Tkinter.IntVar()
sql.set(0)

lfi = Tkinter.IntVar()
lfi.set(0)

rfi = Tkinter.IntVar()
rfi.set(0)

xss = Tkinter.IntVar()
xss.set(0)

# Dictionary for function
dict = {'sql': 0, 'lfi': 0, 'rfi': 0, 'xss': 0}

# Checkbox
checkboxlabel = Tkinter.Label(top_frame, text="Scan for:")
checkboxlabel.pack()

sqlc = Tkinter.Checkbutton(window, text="SQL", variable=sql)
sqlc.pack()

lfic = Tkinter.Checkbutton(window, text="LFI", variable=lfi)
lfic.pack()

rfic = Tkinter.Checkbutton(window, text="RFI", variable=rfi)
rfic.pack()

xssc = Tkinter.Checkbutton(window, text="XSS", variable=xss)
xssc.pack()



# Analyze button
Analyze = Tkinter.Button(button_frame, text="Analyze", command=clicked)
button_frame.grid_columnconfigure(0, weight=1)
Analyze.grid(row=1, column=2)

# Status to inform user if analyzing or not
statuslabel = Tkinter.Label(top_frame, text="Configure settings")
statuslabel.pack(side="bottom")


window.mainloop()


