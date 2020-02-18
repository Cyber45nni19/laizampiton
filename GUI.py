import Tkinter, ttk, tkFileDialog

# Variable for the access log
logpath = ""

# Variable for the location to export log file (Default location is as follows)
savepath = "C:/"

# Variable to know if a log has been selected
selected = False

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


# Function to browse logs when clicked
def open():
    global selected
    window.filename = tkFileDialog.askopenfilename(initialdir="C:/", title="Select Access Log",
                                                   filetypes=(('text files', 'txt'),))
    window.label = ttk.Label(Pathnamelabel, text="")
    if window.filename != "":
        Pathnamelabel.configure(text=window.filename)
        selected = True
    else:
        Pathnamelabel.configure(text="No logs selected!")
        selected = False


# Button to find logs
logbutton = Tkinter.Button(top_frame, text="Browse access log", command=open)
logbutton.pack()

# Label to indicate what log has been selected
Pathnamelabel = Tkinter.Label(top_frame, text="No Access log selected yet", pady=10)
Pathnamelabel.pack()


# Function to allow user to choose where to save the exports, default is C:\\
def save():
    window.path = tkFileDialog.askdirectory()
    window.label2 = ttk.Label(Savenamelabel, text="")
    if window.path != "":
        Savenamelabel.configure(text=window.path)
    else:
        Savenamelabel.configure(text=savepath)


# Button to choose save path
savebutton = Tkinter.Button(top_frame, text="Choose directory of export", command=save)
savebutton.pack()

# Label to indicate what save location has been selected
Savenamelabel = Tkinter.Label(top_frame, text=savepath, pady=10)
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

# If analyzed button is clicked, the path of the log file is put into a variable so it can be analyzed
isclicked = False


def clicked():
    global isclicked
    global logpath
    global savepath

    path = Pathnamelabel.cget("text")
    save = Savenamelabel.cget("text")

    # if valid and got selected
    if selected == True and path.endswith('.txt'):
        logpath = path
        isclicked = True
    else:
        isclicked = False

    # assign the save location to the variable
    savepath = save

    # assign checkbox values to dic
    dict['sql'] = sql.get()
    dict['lfi'] = lfi.get()
    dict['rfi'] = rfi.get()
    dict['xss'] = xss.get()

    print "which options? " + str(dict)

    print "Analyzed is clicked, proceed to analyze? : " + str(isclicked)
    print "Got log file selected already? : " + str(selected)

    print "Final logpath : " + logpath
    print "Final Export Directory : " + savepath


# Analyze button
Analyze = Tkinter.Button(button_frame, text="Analyze", command=clicked)
button_frame.grid_columnconfigure(0, weight=1)
Analyze.grid(row=1, column=2)

# Status to inform user if analyzing or not
statuslabel = Tkinter.Label(top_frame, text="Software not analyzing")
statuslabel.pack(side="bottom")

# If isclicked True > run the main to analyze the log file

#Dictionary dict to pass on to function

window.mainloop()
