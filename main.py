from tkinter import *
import tkinter.messagebox
from tkinter import messagebox
import sqlite3
import uuid
from PIL import ImageTk, Image
# import partial
conn = sqlite3.connect('storg.db')
curr = conn.cursor()

class Application:
    def home():
        global root
        root = Tk()
        app = Application(root)
        root.geometry('1920x1080')
        root.title("Bus Booking Portal")
        root.resizable(False,False)
        root.mainloop()

    def homehelper():
        root.destroy()
        Application.home()
    def booking():
        flag = False
        arr = (numseats.get(),choice.get(),numseats.get())
        try:
            curr.execute('UPDATE Buses SET seats = seats-(?) WHERE rowid=(?) AND seats>(?)',arr)
            conn.commit()
            flag = True
            messagebox.showinfo("Alert","Successfully Booked")
        except:
            messagebox.showinfo("Alert","Number of Seats is bigger than number of seats Available")
        if(flag):
            randstring = str(uuid.uuid1())
            cust = (randstring,custname.get(),numseats.get())
            try:
                curr.execute('CREATE TABLE Passengers (refid text,name text,seats int)')
                curr.execute('INSERT INTO Passengers VALUES (?,?,?)',cust)
                conn.commit()
            except:
                curr.execute('INSERT INTO Passengers VALUES (?,?,?)',cust)
                conn.commit()
            finally:
                messagebox.showinfo("Alert","Your Reference id is "+ randstring)
    def showstats():
        arr=(uid.get(),)
        curr.execute('SELECT * FROM Passengers WHERE refid=?',arr)
        l = curr.fetchall()
        if(len(l)>0):
            messagebox.showinfo("Alert","Your Seat is Booked")
        else:
            messagebox.showinfo("Alert","Invalid ID")
    def showbuses():
        global root
        root=Tk()
        root.geometry('1920x1080')
        root.title("Available Buses")
        Label(root,text="Available Buses Are:",font='helvetica 30',bg='#00ff00').place(x=650,y=0)
        Label(root,text="RegID Number",font='helvetica 15 bold').place(x=0,y=160)
        Label(root,text="Operator Name",font='helvetica 15 bold').place(x=245,y=160)
        Label(root,text="Source",font='helvetica 15 bold').place(x=490,y=160)
        Label(root,text="Destination",font='helvetica 15 bold').place(x=735,y=160)
        Label(root,text="Seats",font='helvetica 15 bold').place(x=980,y=160)
        Label(root,text="Fare",font='helvetica 15 bold').place(x=1230,y=160)
        arr = ((src.get(),dest.get()))
        # messagebox.showinfo("Alert Check",str(src.get()+dest.get()))
        Label(root,text="Select the Bus you want to book",font='helvetica 30',bg='#00ff00').place(x=650,y=50)
        curr.execute('SELECT rowid,opname,src,dest,seats,fare FROM Buses WHERE src=(?) AND dest=(?) AND seats>0',arr)
        ans = (curr.fetchall())
        global choice,numseats,name,custname
        i = 0
        for record in ans:
            for j in range(len(record)):
                e = Entry(root,width=30,fg='red')
                e.grid(row=i,column=j,pady=200)
                e.insert(END,record[j])
            i+=1
        Label(root,text="Enter The ID Number of the Bus you want to Book",font='helvetica 25').place(x=0,y=800)
        # Button(root,command=root.destroy,text="Exit",font='helvetica 30').place(x=1800,y=950)
        choice = IntVar()
        custname = StringVar()
        numseats = IntVar()
        Entry(root,textvariable=choice,font='helvetica 20').place(x=750,y=805)
        Entry(root,textvariable=numseats,font='helvetica 20').place(x=750,y=850)
        Label(root,text="Number of Seats to Book",font='helvetica 25').place(x=0,y=850)
        Button(root,text="Submit",font='helvetica 20',command=Application.booking).place(x=650,y=930)
        Label(root,text="Enter your Name",font='helvetica 25').place(x=1100,y=800)
        Entry(root,textvariable=custname,font='helvetica 20').place(x=1390,y=800)
        Button(root,text="Home",font='helvetica 25 bold',command=Application.homehelper).place(x=1700,y=900)


    def Search():
        if(Application.check()):
            messagebox.showinfo("Error", "Source and Destination Cant' be Same")
        else:
            try:
                arr = ((src.get(),dest.get()))
                curr.execute('SELECT * FROM Buses WHERE src=(?) AND dest=(?)',arr)
                ans  = str(curr.fetchall())
                messagebox.showinfo("Alert","Buses Found Taking you to booking Page")
            except:
                messagebox.showinfo("Error","No Bus Found")
            finally:
                root.destroy()
                Application.showbuses()
    def fun():
        Label(root,text=a.get()).pack(side=BOTTOM)
    def passhelper():
        root.destroy()
        Application.passengr()
    def passengr():
        global root,src,dest,uid
        root = Tk()
        root.geometry('1920x1080')
        root.title("Passengers Section")
        Label(root, text="Welcome to Passenger Section of Bus Booking Portal", font=('helvetica 40 bold'), fg='#000000', bg='#00ff00').place(x=300,y=0)
        imgfile = ImageTk.PhotoImage(Image.open("./busstop.png"))
        Label(root,text="bus",image=imgfile).place(x=1290,y=250)
        Label(root,text="Enter Source",font = 'helvetica 30').place(x=100,y=250)
        src = StringVar()
        dest = StringVar()
        uid  = StringVar()
        Label(root, text="Enter Destination", font='helvetica 30').place(x=100, y=350)
        Entry(root,textvariable=src,width=30).place(x=100,y=310)
        Entry(root, textvariable=dest, width=30).place(x=100, y=410)
        Label(root,text="Click The Button Below to Search For Available Buses",font='helvetica 30').place(x=100,y=500)
        Button(root,text="Submit",font='helvetica 35',command=Application.checkifavailable).place(x=450,y=600)
        Label(root,text="Enter your Reference Number Below to check your Booking Status",font='helvetica 30').place(x=100,y=700)
        Entry(root,textvariable=uid,font='helvetica 18').place(x=100,y=750)
        Button(root,text="Check Status",font='helvetica 25 bold',command=Application.showstats).place(x=450,y=800)
        Button(root,text="Home",font='helvetica 25 bold',command=Application.homehelper).place(x=1700,y=900)
        root.mainloop()
    def checkifavailable():
        arr = ((src.get(),dest.get()))
        curr.execute('SELECT * FROM Buses WHERE src=(?) AND dest=(?)',arr)
        ans  = (curr.fetchall())
        if(len(ans)>0):
            Application.Search()
        else:
            messagebox.showinfo("Alert","No Buses Available on this route")
    def ophelper():
        root.destroy()
        Application.operator()
    def check():
        if(src.get()==dest.get()):
            return True
        else:
            return False

    def onClick():
        messagebox.showinfo("Alert","Successfully Added Bus")
        arr = [(busnum.get(),opname.get(),src.get(),dest.get(),seats.get(),fare.get())]
        if(Application.check()):
            messagebox.showinfo("Error", "Source and Destination Cant' be Same")
        else:
            try:
                curr.execute('''CREATE TABLE Buses (busnum text,opname text,src text,dest text,seats real,fare real)''')
                curr.executemany('INSERT INTO Buses VALUES (?,?,?,?,?,?)',arr)
                conn.commit()
            except:
                curr.executemany('INSERT INTO Buses VALUES (?,?,?,?,?,?)',arr)
                conn.commit()

    def operator():
        global root
        root = Tk()
        root.geometry('1920x1080')
        root.title("Operator Portal")

        Label(root, text="Welcome to Operator Section of Bus Booking Portal", font=(
            'helvetica 40 bold'), fg='#000000', bg='#00ff00').place(x=300, y=0)
        Label(root,text="Bus Number",font='helvetica 30').place(x=100,y=180)
        Label(root,text="Bus Name",font='helvetica 30').place(x=100,y=280)
        Label(root,text="Source",font='helvetica 30').place(x=100,y=380)
        Label(root,text="Destination",font='helvetica 30').place(x=100,y=480)
        Label(root,text="Seats Available",font='helvetica 30').place(x=100,y=580)
        Label(root,text="Fare",font='helvetica 30').place(x=100,y=680)
        global opname,src,dest,seats,fare,busnum
        opname = StringVar()
        busnum = StringVar()
        src = StringVar()
        dest = StringVar()
        seats = IntVar()
        fare = IntVar()
        Entry(root,textvariable=busnum,width=40).place(x=400,y=186)
        Entry(root,textvariable=opname,width=40).place(x=400,y=286)
        Entry(root,textvariable=src,width=40).place(x=400,y=386)
        Entry(root,textvariable=dest,width=40).place(x=400,y=486)
        Entry(root,textvariable=seats,width=40).place(x=400,y=586)
        Entry(root,textvariable=fare,width=40).place(x=400,y=686)
        Button(root,command=Application.onClick,font='helvetica 30',text="Submit").place(x=400,y=780)
        Button(root,text="Home",font='helvetica 25 bold',command=Application.homehelper).place(x=1700,y=900)


    def __init__(self,windows):
        self.windows = windows
        # Top frame
        self.top = Frame(windows, width = 1000,height=50).pack(side = TOP)
        self.title = Label(self.top,text = "Welcome to Bus Booking Portal",font = ('helvetica 40 bold'),fg='#000000',bg='#00ff00')
        self.title.place(x=600,y=0)


        #left frame
        self.left = Frame(windows, width=960, height=850, bg='#76ab44').pack(side=LEFT)
        self.passenger = Label(self.left, text="If you are a Passenger\n and want to search for Buses\n click the button below", font='helvetica 30 bold')
        self.passenger.place(x=140, y=170)
        self.path = './passenger.png'
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.passsubmit = Button(
            self.left, text="Passenger", command=Application.passhelper, font='helvetica 30')
        self.imagefile = Label(self.left, text="img", image=self.img)
        self.imagefile.place(x=210, y=330)
        self.passsubmit.place(x=350, y=900)


        #right frame
        self.right = Frame(windows, width=960, height=850, bg='#32b8b1').pack(side=RIGHT)
        self.operator = Label(
            self.right, text="If you are a Operator\n and want to register your Buses\n click the button below", font='helvetica 30 bold')
        self.operator.place(x=1130,y=170)
        self.spath = './Operator.png'
        self.img2 = ImageTk.PhotoImage(Image.open(self.spath))
        self.opsubmit = Button(
            self.right, text="Operator", font='helvetica 30',command=Application.ophelper)
        self.opsubmit.place(x=1350,y=900)
        self.opimage = Label(self.right,text = "img",image=self.img2)
        self.opimage.place(x=1210,y=330)

        #bottom frame
        self.bottom = Frame(windows,width=1000,height=950).pack(side=BOTTOM)
        self.exit = Button(self.bottom,text="Exit",bg = "red",font = 'helvetica 20 bold',command=root.destroy)
        self.exit.place(x=1830,y=50)



root = Tk()
app = Application(root)
root.geometry("1920x1080")
root.title("Bus Booking Portal")
root.resizable(False,False)
# Button(root,text="Exit",command=root.destroy).pack()
root.mainloop()
