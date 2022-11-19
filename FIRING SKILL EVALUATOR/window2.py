import sqlite3
from pathlib import Path

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

Army_No_This_Session = []
Ranks_This_Session = []
Names_This_Session = []
JoiningDates_This_Session = []

def append_all(unit,no1,no2,no3,no4,no5,no6,no7,no8,rk1,rk2,rk3,rk4,rk5,rk6,rk7,rk8,nm1,nm2,nm3,nm4,nm5,nm6,nm7,nm8,dt1,dt2,dt3,dt4,dt5,dt6,dt7,dt8):
    Army_No_This_Session.append(no1)
    Army_No_This_Session.append(no2)
    Army_No_This_Session.append(no3)
    Army_No_This_Session.append(no4)
    Army_No_This_Session.append(no5)
    Army_No_This_Session.append(no6)
    Army_No_This_Session.append(no7)
    Army_No_This_Session.append(no8)

    Ranks_This_Session.append(rk1)
    Ranks_This_Session.append(rk2)
    Ranks_This_Session.append(rk3)
    Ranks_This_Session.append(rk4)
    Ranks_This_Session.append(rk5)
    Ranks_This_Session.append(rk6)
    Ranks_This_Session.append(rk7)
    Ranks_This_Session.append(rk8)

    Names_This_Session.append(nm1)
    Names_This_Session.append(nm2)
    Names_This_Session.append(nm3)
    Names_This_Session.append(nm4)
    Names_This_Session.append(nm5)
    Names_This_Session.append(nm6)
    Names_This_Session.append(nm7)
    Names_This_Session.append(nm8)

    JoiningDates_This_Session.append(dt1)
    JoiningDates_This_Session.append(dt2)
    JoiningDates_This_Session.append(dt3)
    JoiningDates_This_Session.append(dt4)
    JoiningDates_This_Session.append(dt5)
    JoiningDates_This_Session.append(dt6)
    JoiningDates_This_Session.append(dt7)
    JoiningDates_This_Session.append(dt8)

    for elem in list(Army_No_This_Session):
        if elem == '':
            Army_No_This_Session.remove(elem)
            Ranks_This_Session.remove(elem)
            Names_This_Session.remove(elem)

    insertIntoDatabase(len(Army_No_This_Session),unit)

class MyDateEntry(DateEntry):
    def __init__(self, master=None, align='left', **kw):
        DateEntry.__init__(self, master, **kw)
        self.align = align

    def drop_down(self):
        """Display or withdraw the drop-down calendar depending on its current state."""
        if self._calendar.winfo_ismapped():
            self._top_cal.withdraw()
        else:
            self._validate_date()
            date = self.parse_date(self.get())
            if self.align == 'left':  # usual DateEntry
                x = self.winfo_rootx()
            else:  # right aligned drop-down
                x = self.winfo_rootx() + self.winfo_width() - self._top_cal.winfo_reqwidth()
            y = self.winfo_rooty() + self.winfo_height()
            if self.winfo_toplevel().attributes('-topmost'):
                self._top_cal.attributes('-topmost', True)
            else:
                self._top_cal.attributes('-topmost', False)
            self._top_cal.geometry('+%i+%i' % (x, y))
            self._top_cal.deiconify()
            self._calendar.focus_set()
            self._calendar.selection_set(date)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def insertIntoDatabase(length,unit):
    conn = sqlite3.connect('firingevaluator.db')
    cur = conn.cursor()
    for i in range(0,length):
        cur.execute("INSERT OR IGNORE INTO personalInfo VALUES(?,?,?,?,?)",(Army_No_This_Session[i], Names_This_Session[i], Ranks_This_Session[i], unit, JoiningDates_This_Session[i]))
    cur.execute("SELECT * FROM personalInfo")
    conn.commit()
    conn.close()

def input_indl_page(window, relative_to_assets, unit):
    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()
    unit = unit

    def nextPage():
        canvas.destroy()
        button_1.destroy()
        frame1.destroy()
        from window2_1 import input_indl_page_compile
        append_all(unit, No1.get(),No2.get(),No3.get(),No4.get(),No5.get(),No6.get(),No7.get(),No8.get(),Rank1.get(),Rank2.get(),Rank3.get(),Rank4.get(),Rank5.get(),Rank6.get(),Rank7.get(),Rank8.get(),Name1.get(),Name2.get(),Name3.get(),Name4.get(),Name5.get(),Name6.get(),Name7.get(),Name8.get(),Service1.get(),Service2.get(),Service3.get(),Service4.get(),Service5.get(),Service6.get(),Service7.get(),Service8.get())
        input_indl_page_compile(window, relative_to_assets, Army_No_This_Session, unit)

    def previousPage():
        canvas.destroy()
        button_1.destroy()
        frame1.destroy()
        from index import index_items
        index_items(window, relative_to_assets)

    canvas = Canvas(
    window,
    bg = "#95AC28",
    height = scr_height,
    width = scr_width,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    
    img = Image.open(relative_to_assets("image_2.png"))
    img = img.resize((scr_width,int(scr_height/2)), Image.ANTIALIAS)
    image_image_1 = ImageTk.PhotoImage(img)
    image_1 = canvas.create_image(
    0,
    0,
    image=image_image_1,
    anchor="nw"
    )

    frame1=Frame(window, bd=2, bg="#95AC28", height=scr_height/1.75, width=300, relief=RAISED)
    frame1.pack(padx=10,pady=170)

    lbl_No0=Label(frame1,font=("aria",20,'bold'),text="Army Number", bg="#95AC28", width=12,fg="#042E04")
    lbl_No0.grid(row=1,column=1, padx=5, pady=5)
    lbl_No1=Label(frame1,font=("aria",20,'bold'),text="Rank", bg="#95AC28", width=10,fg="#042E04")
    lbl_No1.grid(row=1,column=2, padx=5, pady=5)
    lbl_No1=Label(frame1,font=("aria",20,'bold'),text="Full Name", bg="#95AC28", width=32,fg="#042E04")
    lbl_No1.grid(row=1,column=3, padx=5, pady=5)
    lbl_No2=Label(frame1,font=("aria",20,'bold'),text="Joining Date", bg="#95AC28", width=12,fg="#042E04")
    lbl_No2.grid(row=1,column=4, padx=5, pady=5)

    lbl_No1=Label(frame1,font=("aria",20,'bold'),text="Target No-1", bg="#95AC28", width=10,fg="#042E04")
    lbl_No1.grid(row=2,column=0, padx=5, pady=5)
    lbl_No2=Label(frame1,font=("aria",20,'bold'),text="Target No-2", bg="#95AC28", width=10,fg="#042E04")
    lbl_No2.grid(row=3,column=0, padx=5, pady=5)
    lbl_No3=Label(frame1,font=("aria",20,'bold'),text="Target No-3", bg="#95AC28", width=10,fg="#042E04")
    lbl_No3.grid(row=4,column=0, padx=5, pady=5)
    lbl_No4=Label(frame1,font=("aria",20,'bold'),text="Target No-4", bg="#95AC28", width=10,fg="#042E04")
    lbl_No4.grid(row=5,column=0, padx=5, pady=5)
    lbl_No5=Label(frame1,font=("aria",20,'bold'),text="Target No-5", bg="#95AC28", width=10,fg="#042E04")
    lbl_No5.grid(row=6,column=0, padx=5, pady=5)
    lbl_No6=Label(frame1,font=("aria",20,'bold'),text="Target No-6", bg="#95AC28", width=10,fg="#042E04")
    lbl_No6.grid(row=7,column=0, padx=5, pady=5)
    lbl_No7=Label(frame1,font=("aria",20,'bold'),text="Target No-7", bg="#95AC28", width=10,fg="#042E04")
    lbl_No7.grid(row=8,column=0, padx=5, pady=5)
    lbl_No8=Label(frame1,font=("aria",20,'bold'),text="Target No-8", bg="#95AC28", width=10,fg="#042E04")
    lbl_No8.grid(row=9,column=0, padx=5, pady=(5,15))

    No1=StringVar()
    No2=StringVar()
    No3=StringVar()
    No4=StringVar()
    No5=StringVar()
    No6=StringVar()
    No7=StringVar()
    No8=StringVar()

    entry_No1=Entry(frame1,font=("aria",20,'bold'),textvariable=No1, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No1.grid(row=2,column=1, padx=5, pady=5)
    entry_No2=Entry(frame1,font=("aria",20,'bold'),textvariable=No2, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No2.grid(row=3,column=1, padx=5, pady=5)
    entry_No3=Entry(frame1,font=("aria",20,'bold'),textvariable=No3, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No3.grid(row=4,column=1, padx=5, pady=5)
    entry_No4=Entry(frame1,font=("aria",20,'bold'),textvariable=No4, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No4.grid(row=5,column=1, padx=5, pady=5)
    entry_No5=Entry(frame1,font=("aria",20,'bold'),textvariable=No5, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No5.grid(row=6,column=1, padx=5, pady=5)
    entry_No6=Entry(frame1,font=("aria",20,'bold'),textvariable=No6, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No6.grid(row=7,column=1, padx=5, pady=5)
    entry_No7=Entry(frame1,font=("aria",20,'bold'),textvariable=No7, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No7.grid(row=8,column=1, padx=5, pady=5)
    entry_No8=Entry(frame1,font=("aria",20,'bold'),textvariable=No8, bg="#98FF98", bd=4, width=12,fg="#042E04")
    entry_No8.grid(row=9,column=1, padx=5, pady=(5,15))

    Rank1=StringVar()
    Rank2=StringVar()
    Rank3=StringVar()
    Rank4=StringVar()
    Rank5=StringVar()
    Rank6=StringVar()
    Rank7=StringVar()
    Rank8=StringVar()
    
    entry_Rank1=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank1, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank1.grid(row=2,column=2, padx=5, pady=5)
    entry_Rank2=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank2, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank2.grid(row=3,column=2, padx=5, pady=5)
    entry_Rank3=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank3, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank3.grid(row=4,column=2, padx=5, pady=5)
    entry_Rank4=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank4, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank4.grid(row=5,column=2, padx=5, pady=5)
    entry_Rank5=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank5, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank5.grid(row=6,column=2, padx=5, pady=5)
    entry_Rank6=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank6, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank6.grid(row=7,column=2, padx=5, pady=5)
    entry_Rank7=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank7, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank7.grid(row=8,column=2, padx=5, pady=5)
    entry_Rank8=Entry(frame1,font=("aria",20,'bold'),textvariable=Rank8, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_Rank8.grid(row=9,column=2, padx=5, pady=(5,15))

    Name1=StringVar()
    Name2=StringVar()
    Name3=StringVar()
    Name4=StringVar()
    Name5=StringVar()
    Name6=StringVar()
    Name7=StringVar()
    Name8=StringVar()
    
    entry_Name1=Entry(frame1,font=("aria",20,'bold'),textvariable=Name1, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name1.grid(row=2,column=3, padx=5, pady=5)
    entry_Name2=Entry(frame1,font=("aria",20,'bold'),textvariable=Name2, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name2.grid(row=3,column=3, padx=5, pady=5)
    entry_Name3=Entry(frame1,font=("aria",20,'bold'),textvariable=Name3, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name3.grid(row=4,column=3, padx=5, pady=5)
    entry_Name4=Entry(frame1,font=("aria",20,'bold'),textvariable=Name4, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name4.grid(row=5,column=3, padx=5, pady=5)
    entry_Name5=Entry(frame1,font=("aria",20,'bold'),textvariable=Name5, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name5.grid(row=6,column=3, padx=5, pady=5)
    entry_Name6=Entry(frame1,font=("aria",20,'bold'),textvariable=Name6, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name6.grid(row=7,column=3, padx=5, pady=5)
    entry_Name7=Entry(frame1,font=("aria",20,'bold'),textvariable=Name7, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name7.grid(row=8,column=3, padx=5, pady=5)
    entry_Name8=Entry(frame1,font=("aria",20,'bold'),textvariable=Name8, bg="#98FF98", bd=4, width=32,fg="#042E04")
    entry_Name8.grid(row=9,column=3, padx=5, pady=(5,15))

    Service1=StringVar()
    Service2=StringVar()
    Service3=StringVar()
    Service4=StringVar()
    Service5=StringVar()
    Service6=StringVar()
    Service7=StringVar()
    Service8=StringVar()

    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure('my.DateEntry', background="#98FF98",fieldbackground="#98FF98",
                    foreground="#042E04",darkcolor="#2DD727",selectbackground="grey",lightcolor="#263705")

    entry_Service1=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service1,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service1.grid(row=2,column=4, padx=5, pady=5)
    entry_Service1.configure(justify='center')
    entry_Service2=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service2,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service2.grid(row=3,column=4, padx=5, pady=5) 
    entry_Service2.configure(justify='center')
    entry_Service3=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service3,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service3.grid(row=4,column=4, padx=5, pady=5) 
    entry_Service3.configure(justify='center')
    entry_Service4=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service4,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service4.grid(row=5,column=4, padx=5, pady=5) 
    entry_Service4.configure(justify='center')
    entry_Service5=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service5,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service5.grid(row=6,column=4, padx=5, pady=5) 
    entry_Service5.configure(justify='center')
    entry_Service6=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service6,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service6.grid(row=7,column=4, padx=5, pady=5) 
    entry_Service6.configure(justify='center')
    entry_Service7=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service7,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service7.grid(row=8,column=4, padx=5, pady=5) 
    entry_Service7.configure(justify='center')
    entry_Service8=MyDateEntry(frame1,font=("aria",20,'bold'),textvariable=Service8,style='my.DateEntry', date_pattern='yyyy-mm-dd', bd=4, width=12, align='right')
    entry_Service8.grid(row=9,column=4, padx=5, pady=(5,15))
    entry_Service8.configure(justify='center') 
    
    button_image_1 = PhotoImage(
    file=relative_to_assets("button_2.png"))
    button_1 = Button(
    image=button_image_1,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=nextPage,
    relief="flat"
    )
    button_1.place(
    x=scr_width-500,
    y=scr_height-200.0
    )

    back_button = PhotoImage(file=relative_to_assets("back.png"))
    button_back = Button(
    image=back_button,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=previousPage,
    relief="flat"
    )
    button_back.place(x=scr_width-75*3,y=scr_height-75,width=75,height=75)

    min_button = PhotoImage(file=relative_to_assets("minimize.png"))
    button_minimize = Button(
    image=min_button,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=window.iconify,
    relief="flat"
    )
    button_minimize.place(x=scr_width-75*2,y=scr_height-75,width=75,height=75)

    exit_button = PhotoImage(file=relative_to_assets("exit.png"))
    button_exit = Button(
    image=exit_button,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=window.destroy,
    relief="flat"
    )
    button_exit.place(x=scr_width-75,y=scr_height-75,width=75,height=75)
    
    window.mainloop()