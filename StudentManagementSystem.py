from tkinter import  *
from tkinter import ttk
from  tkinter.font import Font
from CseProject.checkValues import *
from CseProject.sendmail import *
from CseProject.sendmailwithAttachment import sendNotice
from CseProject.netConncectionCheck import netConCheck
from tkinter import  filedialog
import mysql.connector as mysql
import tkinter.messagebox as msgbox

import  time

root = Tk()
root.geometry("1366x720")
root.resizable("false","false")
root.title("Student Management System")
root.iconbitmap(r'E:\StudentManagementSystemMTE18\student.ico')



style = ttk.Style()


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#bgcolor = "#08B929"
bgcolor = "#389ED7"

#bgcolor = "#17a3f3"
fileTuple = []

ruetImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\headline.png")
bgImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\background2.png")
frontbgImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\frontBg.png")
regiFormImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\registrationform.png")
deleteImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\delete.png")
searchQueryImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\searchquery.png")
resetImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\reset.png")
queryEntryImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\queryentry.png")
aboutUsImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\aboutus.png")
registerBtnImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\register.png")
searchBtnImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\search.png")
dbBtnImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\database.png")
attendanceBtnImage  = PhotoImage(file=r"E:\StudentManagementSystemMTE18\attendance.png")
announcementBtnImage  = PhotoImage(file=r"E:\StudentManagementSystemMTE18\announcement.png")
announceactivitybgImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\announcementbg.png")
sendbtnImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\sendbtn.png")
attachmentImage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\attachment.png")
#Label(frame1, bg='black', image=ruetImage).pack()
#Label(root, bg='#10364c', image=frontbgImage).pack()
Label(root,image=frontbgImage).pack()


# ============================================== mysql connection ==============================================#==============================================
# mysql connection
def connection():
    try:
        con = mysql.connect(host="localhost", user="root", password="", database="test")
        cursr = con.cursor()
        return con, cursr
    except:
        msgbox.showerror("Failed", "Connection Failed\n Please Run mysql server at port 3306\nYou can use xampp software to run mysql server ")


# ============================================== creating database table ==============================================#==============================================
def create_table():
    con, crsr = connection()
    try:
        crsr.execute("""
                CREATE TABLE students(
                Roll INT(7) PRIMARY KEY,
                Name VARCHAR(255),
                Attendance FLOAT,
                Present int,
                TotalClass int,
                Department VARCHAR(255),
                Phone VARCHAR(255),
                Email VARCHAR(255),
                Series int(2),
                Blood VARCHAR(2),
                PresentAddress VARCHAR(100),
                ParmanentAddress VARCHAR(100)

                )

            """)
        con.commit()
        con.close()
    except:
        return 


create_table()  # calling for create table


#=====================================
def registerFunc():
    registerActivity = Toplevel()
    registerActivity.geometry("1081x600")
    registerActivity.resizable("false","false")
    registerActivity.title("Registration Form")
    registerActivity.iconbitmap(r'E:\StudentManagementSystemMTE18\student.ico')



    regFrame1 = Frame(registerActivity)
    regFrame1.pack()
    Label(regFrame1, bg='black', image=regiFormImage).pack()



    nameEntry = Entry(regFrame1,font=('arial',14))
    nameEntry.place(x=550,y=72)
    nameEntry.config(bd=0,bg="#F4F9F5",width=18,fg="red")

    rollEntry = Entry(regFrame1, font=('arial', 14))
    rollEntry.place(x=550, y=120)
    rollEntry.config(bd=0, bg="#F4F9F5", width=18, fg="red")

    emailEntry = Entry(regFrame1, font=('arial', 14))
    emailEntry.place(x=550, y=165)
    emailEntry.config(bd=0, bg="#F4F9F5", width=18, fg="red")

    phoneEntry = Entry(regFrame1, font=('arial', 14))
    phoneEntry.place(x=550, y=210)
    phoneEntry.config(bd=0, bg="#F4F9F5", width=18, fg="red")

    presentAdEntry = Text(regFrame1, font=('arial', 14),width=17,height=2)
    presentAdEntry.place(x=550, y=264)
    presentAdEntry.config(bd=0, bg="white", fg="red")

    parmanentAdEntry = Text(regFrame1, font=('arial', 14),width=17,height=3)
    parmanentAdEntry.place(x=550, y=350)
    parmanentAdEntry.config(bd=0, bg="white" ,fg="red")

    bloodClicked = StringVar()
    bloodClicked.set('Blood')

    bloodGroup = OptionMenu(regFrame1, bloodClicked, "A+", "B+", "AB+", "O+", "A-", "B-", "AB-", "O-")
    bloodGroup.place(x=545,y=435)
    bloodGroup.config(bg="red", fg="white",width=15,font=("arial",14))
    bloodGroup['menu'].config(bg="red",fg="white")

    # ============================================== Checking Department ==============================================#==============================================

    def departmentChecking(deptcode):
        return {
            '00': 'CE',
            '01': 'EEE',
            '02': 'ME',
            '03': 'CSE',
            '04': 'ETE',
            '05': 'IPE',
            '06': 'GCE',
            '07': 'URP',
            '08': 'MTE',
            '09': 'Arch',
            '10': 'ECE',
            '11': 'CFPE',
            '12': 'BECM',
            '13': 'MSE',

        }.get(deptcode, "sorry not found")

# ============================================== Insert Data  ==============================================#==============================================

    def inserFunc():
        if (len(rollEntry.get()) ==7 and len(emailEntry.get())==0):
            emailEntry.insert(0,"{}@student.ruet.ac.bd".format(rollEntry.get()))
        if (namecheck(nameEntry.get()) and rollcheck(rollEntry.get()) and phonecheck(phoneEntry.get()) and checkmail(
                emailEntry.get()) and len(presentAdEntry.get('1.0', END)) > 1 and len(parmanentAdEntry.get('1.0', END)) > 1):
            if (bloodClicked.get().lower() == 'blood'):
                msgbox.showwarning('Blood', 'Please select your Blood Group',parent=registerActivity)
                return
            if(not netConCheck()):
                msgbox.showerror("Falied","Please turn on your internet connection.\n Otherwise student won't notify about registration.",parent=registerActivity)
                return

            con, cursr = connection()
            rollStr = rollEntry.get()
            series = int(rollStr[0]) * 10 + int(rollStr[1])

            temp = rollEntry.get()
            deptRollCode = temp[2] + temp[3]
            departmentgefromRoll = departmentChecking(deptRollCode)

            Attendance = 0
            try:
                cursr.execute(
                    "insert into Students (Roll,Name,Attendance,Present,Totalclass,Phone,Email,Series,Department,Blood,PresentAddress,ParmanentAddress) Values('%s','%s','%f','%d','%d','%s','%s','%d','%s','%s','%s','%s')" % (
                        rollEntry.get(), nameEntry.get(), 0, 0, 0, phoneEntry.get(), emailEntry.get(), series, departmentgefromRoll,
                        bloodClicked.get(), presentAdEntry.get('1.0', END), parmanentAdEntry.get('1.0', END)))

                con.commit()
                con.close()

                send(emailEntry.get(),"Registration Successful","Congrats! Your Registration is Successful.")
                msgbox.showinfo("Success", "Inserted Successfully !\nAn Email is  sent to {}".format(emailEntry.get()),
                                parent=registerActivity)

                rollEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                presentAdEntry.delete('1.0',END)
                parmanentAdEntry.delete('1.0',END)
                bloodClicked.set('Blood')
            except EXCEPTION as e:
                print(e)
                #msgbox.showerror("Duplicate","Something went wrong!\n  {} ".format(rollEntry.get()),parent=registerActivity)



        else:
            msgbox.showinfo("Failed",
                                "Sorry! Insertion failed\n1. Roll must be 7 digits\n2. Phone must be 11 digits\n3. Email should be valid\n4.Present and Parmanent Address should not be Empty ",parent=registerActivity)

    registerBtn = Button(regFrame1, image=registerBtnImage, bd=0, bg="#10C933", activebackground='red',command=inserFunc)
    registerBtn.place(x=520,y=490)



# ===================================== search or show Activity======================================
def searchFunc():
    searchActivity = Toplevel()
    searchActivity.geometry("1230x406")
    searchActivity.resizable("false","false")
    searchActivity.title("Show Data")


    Label(searchActivity,bg=bgcolor).place(relwidth=1, relheight=1)
    queryLbl = Label(searchActivity,image=queryEntryImage,bg=bgcolor)
    queryLbl.pack()
    searchEntry = Entry(searchActivity,bd=0,font=("Arial",14),width=12,justify=CENTER)
    searchEntry.place(x=550,y=15)

    # ============================================== Hide Widget ==============================================#==============================================
    def hideFunc():
        lableNodata.forget()
        table.forget()
        xscrollbar.forget()
        yscrollbar.forget()

    # ============================================== Show All ==============================================#==============================================
    def showFunc():


        hideFunc()
        # clear previous table data
        for i in table.get_children():
            table.delete(i)
        con, cursr = connection()

        try:
            deparmentget = deptClicked.get()
            #print(deparmentget)

            if(len(searchEntry.get()) ==0):
                queryData = "department="
                searchEntry.insert(0,deparmentget)
                querytext = "'"+searchEntry.get()+"'"
            elif (len(searchEntry.get()) == 11):
                queryData = "phone="
                querytext = "'"+searchEntry.get()+"'"
            elif ("+" in searchEntry.get() or "-" in searchEntry.get()):
                queryData = "blood="
                querytext = "'"+searchEntry.get()+"'"
            elif (">" in searchEntry.get() or "<" in searchEntry.get()):
                queryData = "attendance "
                querytext = searchEntry.get()
            elif(len(searchEntry.get()) == 2):
                queryData = "series='{}' AND department='{}'".format(searchEntry.get(),deptClicked.get())
                querytext = ""
            elif(len(searchEntry.get()) == 7):
                queryData = "roll="
                querytext = "'"+searchEntry.get()+"'"
            elif("@" in searchEntry.get()):
                queryData = "email="
                querytext = "'"+searchEntry.get()+"'"
            else:
                queryData = "name="
                querytext = "'"+searchEntry.get()+"'"


            cursr.execute("SELECT * FROM STUDENTS WHERE {}{} ORDER BY ROLL".format(queryData,querytext))
            #  "SELECT * FROM Students  ")
            records = cursr.fetchall()

            if (len(records) == 0):
                #lableNodata.grid(row=0, column=1)
                lableNodata.pack()
                return

            # lableNodata.config(text="")

            for record in records:
                table.insert('', 'end', values=record)

            con.commit()
            con.close()
            #table.grid(row=0, column=1)
            # table.pack(side=LEFT,)
            table.pack(side=LEFT)


            yscrollbar.pack(side=LEFT, fill="y")
            xscrollbar.pack(fill="x")

        except:
            # table.insert('','end',values=". . No Data Found . ")
            lableNodata.pack()
    #============reset function==============================================================================================
    def reset_yesfunc():
        try:
            con, cursr = connection()
            cursr.execute(
                "UPDATE students SET present=0,Totalclass=0,Attendance=0 where series=" + searchEntry.get() + " AND Department='" + deptClicked.get() + "'")
            con.commit()
            con.close()
            msgbox.showinfo("Success", "Attendance has been resetted",parent=searchActivity)
        except:
            msgbox.showerror("Error", "Something Wrong",parent=searchActivity)

    def delete_yesfunc():
        con, cursr = connection()
        carry = searchEntry.get()
        if (len(carry) == 2):
            cursr.execute("DELETE  FROM students WHERE Series=" + carry+" AND department = '"+deptClicked.get()+"'")
            msgbox.showinfo('Delete', "successfully deleted All Entries From {} {} Series ".format(deptClicked.get(),carry),parent=searchActivity)
        elif (len(carry) == 7):
            cursr.execute("DELETE FROM students WHERE Roll=" + carry)
            msgbox.showinfo('Delete', "successfully deleted Roll " + carry,parent=searchActivity)
        else:
            msgbox.showinfo('Delete', "Please Enter Roll Or Series in The Query Box",parent=searchActivity)

        con.commit()
        con.close()

    def deleteFunc():
        if (len(searchEntry.get()) < 2 or (len(searchEntry.get()) > 2 and len(searchEntry.get()) < 7)):
            return
        if(len(searchEntry.get()) ==2):
            thisString = "{} {} series".format(deptClicked.get(),searchEntry.get())
        elif(len(searchEntry.get()) == 7):
            thisString = "roll {}".format(searchEntry.get())

        Msg = msgbox.askquestion("Delete","Are you sure you want to delete {}?".format(thisString),icon="warning",parent=searchActivity)
        if(Msg == 'yes'):
            delete_yesfunc()
        else:
            return

    def resetAttendanceFunc():
        if (len(searchEntry.get()) != 2):
            return

        Msg = msgbox.askquestion("Reset Attendance","Are You sure you want to Reset Attendance of {} {} series".format(deptClicked.get(),searchEntry.get()),parent=searchActivity,icon="warning")
        if(Msg == 'yes'):
            reset_yesfunc()
        else:
            return

    searchBtn = Button(searchActivity,text="search",command=showFunc,image=searchQueryImage,bd=0,activebackground="red",bg=bgcolor)
    deleteBtn = Button(searchActivity,command=deleteFunc,image=deleteImage,bd=0,activebackground="blue",bg=bgcolor)
    resetBtn = Button(searchActivity,text="Reset\nAttendance",image=resetImage,bd=0,activebackground="red",bg=bgcolor,command=resetAttendanceFunc)


    # drop down deparment list
    deptClicked = StringVar()
    deptClicked.set('MTE')
    deparment = OptionMenu(searchActivity, deptClicked, "Arch", "BECM", "CE", "CFPE", "Chemical", "CSE", "ECE", "EEE", "ETE",
                           "GCE",
                           "IPE", "ME", "MSE", "MTE", "URP")
    deparment.place(x=700,y=10)
    resetBtn.pack()
    deleteBtn.place(x=430,y=60)
    searchBtn.place(x=685,y=64)
    deparment.config(bg="yellow", fg="black")



    thisLabelFrame = LabelFrame(searchActivity)
    thisLabelFrame.config(pady=5,bg=bgcolor)
    thisLabelFrame.pack()

    style = ttk.Style()
    table = ttk.Treeview(thisLabelFrame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), height=10,
                         selectmode="extended", show="headings")

    table.pack(side=LEFT)
    lableNodata = Label(thisLabelFrame, text="No Data Found")
    lableNodata.config(bg="white")

    style.theme_use("clam")
    style.configure("Treeview", background='#2caee6', fieldbackground='#2caee6')

    table.heading(1, text="Roll")
    table.heading(2, text="Name")
    table.heading(3, text="Attendance")
    table.heading(4, text="Present")
    table.heading(5, text="Total Class")
    table.heading(6, text="Department")
    table.heading(7, text="Phone")
    table.heading(8, text="Email")
    table.heading(9, text="Series")
    table.heading(10, text="Blood Group")
    table.heading(11, text="Present/Addr.")
    table.heading(12, text="Parmanent/Addr.")

    table.column(1, anchor='center', width=100, minwidth=100)
    table.column(2, anchor='center', width=100, minwidth=160)
    table.column(3, anchor='center', width=100, minwidth=101)
    table.column(4, anchor='center', width=100, minwidth=101)
    table.column(5, anchor='center', width=100, minwidth=101)
    table.column(6, anchor='center', width=100, minwidth=160)
    table.column(7, anchor='center', width=100, minwidth=160)
    table.column(8, anchor='center', width=100, minwidth=160)
    table.column(9, anchor='center', width=100, minwidth=160)
    table.column(10, anchor='center', width=100, minwidth=160)
    table.column(11, anchor='center', width=100, minwidth=160)
    table.column(12, anchor='center', width=100, minwidth=160)

    # table scrollbar adding
    yscrollbar = Scrollbar(thisLabelFrame, orient='vertical', command=table.yview)
    xscrollbar = Scrollbar(searchActivity, orient='horizontal', command=table.xview)

    table.configure(yscrollcommand=yscrollbar.set)
    table.configure(xscrollcommand=xscrollbar.set)



#====================================================== Attendance Activity ================================================
def attendanceFunc():
    # All declarations and initiations
    varse = 1
    var = []
    tempvarContainer = []
    number = []
    activeRoll = []
    rowcount = 0

    attendanceActivity = Toplevel()
    attendanceActivity.geometry("1080x720")
    attendanceActivity.title("Attendance")
    attendanceActivity.iconbitmap(r'E:\StudentManagementSystemMTE18\attendance.ico')
    attendanceActivitybgimage = PhotoImage(file=r"E:\StudentManagementSystemMTE18\background2.png")
    canvimage = PhotoImage(r"E:\StudentManagementSystemMTE18\student.png")
    # attendanceActivitybgimage = PhotoImage(file=r"classroomart.png")
    Label(attendanceActivity, bg='#389ED7', image=attendanceActivitybgimage).place(relwidth=1, relheight=1)

    # clear textfield text when cursor on this box
    def clear_entry(event, entry):
        entry.delete(0, END)

    frameout = LabelFrame(attendanceActivity)
    frameout.config(bg="#389ED7")

    mycanvas = Canvas(frameout)
    mycanvas.config(bg="#389ED7")
    myframe = Frame(mycanvas)

    text = Text(attendanceActivity, width=5)

    scrollbar = Scrollbar(frameout, orient='vertical', command=mycanvas.yview)

    series = Entry(attendanceActivity)
    series.insert(END, "Series?")
    series.config(bd=5, bg="cyan")
    series.bind("<Button-1>", lambda event: clear_entry(event, series))

    # drop down deparment list
    deptClicked = StringVar()
    deptClicked.set('MTE')
    deparment = OptionMenu(attendanceActivity, deptClicked, "Arch", "BECM", "CE", "CFPE", "Chemical", "CSE", "ECE",
                           "EEE", "ETE",
                           "GCE", "ME", "MSE", "MTE", "URP")
    deparment.grid(row=6, column=4, padx=15)
    deparment.config(bg="lime", fg="black",activebackground="pink")
    deparment['menu'].config(bg="cyan",activebackground="red")

    # ======================================== Establish Connection ========================================#========================================


    '''
    #row counting
    intseries = int(series.get())
    cursr.execute("select * from students where series="+intseries)
    tempvar = cursr.fetchall()
    rowcount = len(tempvar)
    print(rowcount)'''

    # ====================================================== Insert Attendance ===================================

    # function execute after take_button  had clicked
    def insertAttendance():

        serie = series.get()
        if (len(serie) != 2):
            return
            # row counting
        # stablish connection with sql
        conn, cursr = connection()
        dept = deptClicked.get()

        # print(series.get())

        # stablish connection with sql
        # conn = mysql.connect(host="localhost", user="attendanceActivity", password="", database="test")
        # cursr = conn.cursor()

        cursr.execute(
            "UPDATE students SET TotalClass=Totalclass+1 WHERE series=" + serie + " And Department='" + dept + "'")

        rowcount = tempvarContainer[0]
        for i in range(rowcount):
            number[i] += var[i].get()
            text.insert(END, str(number[i]) + '\n')

        for i in range(rowcount):
            cursr.execute(" UPDATE students SET Present = Present +" + str(number[i]) + " WHERE Roll='" +
                          activeRoll[i] + "' and Series=" + serie + " And Department='" + dept + "'")

        for i in range(rowcount):
            cursr.execute(
                " UPDATE students SET Attendance = Present * 100/TotalClass WHERE Roll='" +
                activeRoll[i] + "' and Series=" + serie + " And Department='" + dept + "'")

        conn.commit()
        conn.close()
        msgbox.showinfo("Success", "Attendance has been taken")
        #*-------------- sending mail to low attendance students---------------
        con,crsr = connection()
        crsr.execute("SELECT Totalclass from students where Department = '{}' AND Series={}".format(dept,serie))
        totalclass = crsr.fetchall()
        totalclass = totalclass[0]

        if(totalclass[0] >5):
            crsr.execute("SELECT name,roll,email FROM students WHERE Attendance < 60 AND Department = '{}' AND Series={}".format(dept,serie))
            lowAttndEmailAddrs = crsr.fetchall()
            first=0
            last=len(lowAttndEmailAddrs)
            #print(lowAttndEmailAddrs)
            for records in lowAttndEmailAddrs:

                name = records[0]
                roll = records[1]
                email = records[2]
                subject = "Low Attendance"
                body = "Dear {},\n Roll - {}. Your attendance is below 60% . Please try to attend the class regularly. Otherwise you won't take part in the final Exam.\n\nThank you".format(name,roll)
                #print(name,roll,email)

                try:
                    send(email,subject,body)
                except:
                    pass





        attendanceActivity.destroy()

    def takebtnclick():


        MsgBox = msgbox.askquestion('Exit Application', 'Are you sure you want to take the Attendance',
                                    icon='warning',parent=attendanceActivity)
        if MsgBox == 'yes':
            insertAttendance()
        else:
            return

    take_btn = Button(myframe, text="Take", command=takebtnclick)
    take_btn.config(bg="red", fg="white", bd=5, pady=5)

    attendanceLabel = Label(attendanceActivity,bg="#389ED7",text="To take Attendance\nEnter Series And Select Department  ",width=45,anchor=CENTER,bd=10,cursor="dot",height=2)
    attendanceLabel.config(font="Arial 20", bg="white",justify=CENTER)

    # ================================================== Fetch Students =====================================================================
    def fetchStudents():

        varse = 1
        serie = series.get()
        if (len(serie) != 2):
            return
        if (not netConCheck()):
            Msg = msgbox.askquestion("No internet",
                                     "Please turn on your internet connection\n so that the low attendance students will be notified.\nAre you agree to turn on internet? ",
                                     parent=attendanceActivity)
            if (Msg == 'yes'):
                attendanceActivity.destroy()
                return
            else:
                print("Those who have less than 60% Attendence were not notified\n as your internet connection is off ")
        conn, cursr = connection()

        dept = deptClicked.get()

        # row counting
        cursr.execute(
            "select Roll from students where series=" + serie + " And Department='" + dept + "'" + " ORDER BY Roll")
        tempvar = cursr.fetchall()

        if (len(tempvar) < 1):
            attendanceLabel.config(text="No data found for {} {} Series".format(dept,serie))
            return
        try:
            scrollbar.pack(side=RIGHT, fill=Y)
            mycanvas.pack(side=LEFT)
            fetch_btn.config(state=DISABLED)  # after clicking button will be disabled
            tempvarContainer.append(len(tempvar))
        except:
            pass

        # attendanceLabel.config(text="Taking Attendance for Department of " + dept + " " + serie + " series")
        # attendanceLabel.config(font="Arial 20")



        global rowcount
        rowcount = len(tempvar)
        if rowcount < 2:
            auxVerb = "is"
            student = "student"
        else:
            auxVerb = "are"
            student = "students"
        try:
            attendanceLabel.config(
                text="Taking Attendance for Department of " + dept + " " + serie + " series" + "\nThere {} {} {} included".format(
                    auxVerb, rowcount, student))
        except:
            pass

        try:
            # Relateing Scrollbar with mycanvas and myframe
            mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
            mycanvas.create_window((0, 0), window=myframe, anchor="center")
            mycanvas.configure(yscrollcommand=scrollbar.set, height=500)
        except:
            pass

        # initialinzing number list elements
        for i in range(rowcount):
            number.append(0)

        # setting integer value of checked and unchecked boxes
        #print("rowcont= ", rowcount)
        for i in range(rowcount):
            temtemvaroftem = tempvar[i]
            strTemptemp = str(temtemvaroftem[0])
            activeRoll.append(strTemptemp)

            # temtemvaroftem = tempvar[i]
            var.append(IntVar())
            checkbox = Checkbutton(myframe, text=strTemptemp[-2] + strTemptemp[-1], variable=var[i])
            number.append(var)
            checkbox.pack(fill=Y)

    fetch_btn = Button(attendanceActivity, text="Fetch", command=fetchStudents)
    fetch_btn.config(bd=5, bg="cyan", fg="black")

    # all packings , gridings or placings
    take_btn.pack(side=BOTTOM, ipadx=5)

    frameout.place(x=400, y=100)
    frameout.config(bg="black")

    # attendanceActivity.place(x=5,y=5)
    # series.place(x=450,y=520)
    series.place(x=100, y=200)
    deparment.place(x=205, y=197)
    fetch_btn.place(x=100, y=245)
    attendanceLabel.place(x=200, y=10)
#==============================================================================================================
def aboutUsFunc():
    aboutTop = Toplevel(root)
    aboutTop.title("About Us")
    aboutTop.iconbitmap(r'E:\StudentManagementSystemMTE18\student.ico')
    canvastop = Canvas(aboutTop,width=300,height=300)
    aboutTop.geometry("1080x700")
    aboutTop.resizable("false","false")
    topLabel = Label(aboutTop, image=aboutUsImage)
    topLabel.place(x=0,y=0,relwidth=1, relheight=1)
    
    canvastop.grid(row=0, column=0, rowspan=5, columnspan=3)


#+============================================= announcement activity ==============================================================

def announceFunc():

    aboutTop = Toplevel(root)
    aboutTop.geometry("1366x720")
    aboutTop.title("Notice or Announcement")
    aboutTop.iconbitmap(r'E:\StudentManagementSystemMTE18\student.ico')

    canvastop = Canvas(aboutTop, width=300, height=300)

    aboutTop.resizable("false", "false")
    topLabel = Label(aboutTop, image=announceactivitybgImage)
    topLabel.place(x=0, y=0, relwidth=1, relheight=1)

    canvastop.grid(row=0, column=0, rowspan=5, columnspan=3)

    deptClicked = StringVar()
    deptClicked.set('MTE')
    deparment = OptionMenu(aboutTop, deptClicked, "Arch", "BECM", "CE", "CFPE", "Chemical", "CSE", "ECE",
                           "EEE", "ETE",
                           "GCE", "ME", "MSE", "MTE", "URP")
    deparment.place(x=725,y=505)
    deparment.config(bg="lime", fg="black",font=("Arial",20),activebackground="red")
    deparment['menu'].config(bg="cyan")

    def fileOpen():
        files = filedialog.askopenfilenames(
            filetypes=(("All Files", "*"), ("ppt", "*.pptx"), ("word", "*.docx"), ("excel", "*.xlsx")),parent=aboutTop)
        fileTuple.append(files)


    attachmentBtn = Button(aboutTop,image=attachmentImage,bd=0,bg="#3F74BA",activebackground="red",command=fileOpen)
    attachmentBtn.place(x=555,y=585)



    subjectentry = Entry(aboutTop,width=32,font=("Arial",20),bd=0)
    subjectentry.place(x=564,y=144)

    bodybox = Text(aboutTop,width=40,height=9,bd=0,font=("Arial",16))
    bodybox.place(x=564, y=250)

    seriesentry = Entry(aboutTop, width=7, font=("Arial", 20),bd=0,justify=CENTER)
    seriesentry.place(x=560, y=512)

    def on_click(event):
        seriesentry.configure(state=NORMAL)
        seriesentry.delete(0, END)

        # make the callback only work once
        seriesentry.unbind('<Button-1>', on_click_id)

    on_click_id = seriesentry.bind('<Button-1>', on_click)

    def sendBtnFunc():


        noticeisSent = True
        rtrnMsg=""
        if(len(seriesentry.get()) != 2):
            msgbox.showinfo("Series Not found","Please Enter Series..",parent=aboutTop)
            return
        Msg = msgbox.askquestion("Send Notice","Are You sure you want to send notice to {} {} Series?".format(deptClicked.get(),seriesentry.get()),icon="warning",parent=aboutTop)
        if(Msg == 'yes'):

            con,cursr = connection()
            cursr.execute("SELECT email FROM students WHERE series='{}' AND department='{}'".format(seriesentry.get(),deptClicked.get()))
            records = cursr.fetchall()
            if(len(records) < 1):
                msgbox.showerror("Not found","No data found for {} {} Series".format(deptClicked.get(),seriesentry.get()),parent=aboutTop)
                return
            print("Sending... This will take some times")
            for email in records:
                email = "%s"%",".join(email)
                if(len(fileTuple) == 0):
                    fileTuple.append("")

                rtrnMsg = sendNotice(email,subjectentry.get(),bodybox.get('1.0',END),fileTuple[0])
                if(len(rtrnMsg) > 1):
                    msgbox.showerror("Info",rtrnMsg,parent=aboutTop)
                    noticeisSent = False
                    break
            if(noticeisSent):
                msgbox.showinfo("Sent","Notice has been sent successfully")
                subjectentry.delete(0,END)
                bodybox.delete('1.0',END)
                seriesentry.delete(0,END)
                aboutTop.destroy()
        else:
            return



    sendbtn = Button(aboutTop, image=sendbtnImage, bd=0, bg="#3F74BA", activebackground="red",command=sendBtnFunc)
    sendbtn.place(x=920, y=560)


#+============================================================================================================

#+============================================================================================================

registerBtn = Button(root,image=registerBtnImage,bd=0,bg=bgcolor,activebackground='red',command=registerFunc)
registerBtn.place(x=screen_width/2-100,y=200)


attendanceBtn = Button(root,image=attendanceBtnImage,bd=0,bg=bgcolor,activebackground='red',command=attendanceFunc)
attendanceBtn.place(x=screen_width/2-100,y=300)



searchBtn = Button(root,image=dbBtnImage,bd=0,bg=bgcolor,activebackground='red',command=searchFunc)
searchBtn.place(x=screen_width/2-100,y=400)

announcementbtn = Button(root,text="Announcement",command=announceFunc,image=announcementBtnImage,bg=bgcolor,bd=0,activebackground='red')
announcementbtn.place(x=screen_width/2-100,y=500)

aboutUsButton = Button(root,text="About\nUs",command=aboutUsFunc,bg="red",fg="white")
aboutUsButton.place(x=10,y=620)


root.mainloop()