import sqlite3
from pathlib import Path
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_db():
    conn = sqlite3.connect('firingevaluator.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS personalInfo (army_no VARCHAR2(30) primary key,name VARCHAR2(100),rank VARCHAR2(30),unit VARCHAR2(30),joining_date DATE);")
    cur.execute("CREATE TABLE IF NOT EXISTS firingInfo (army_no VARCHAR(30),firing_date DATE,grouping DOUBLE,error VARCHAR(30));")
    cur.execute("CREATE TABLE IF NOT EXISTS performanceInfo (army_no VARCHAR(30),perf_date DATE,performance DOUBLE);")
    cur.execute("CREATE TABLE IF NOT EXISTS evaluationInfo(army_no VARCHAR(30),eval_date DATE,no_of_firings INTEGER,interval INTEGER,season DOUBLE,svc_length DOUBLE,avg_gp DOUBLE);")

    conn.commit()
    conn.close()

create_db()

def index_items(window, relative_to_assets):

    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()

    def nextPage(value):
        unit = value
        canvas.destroy()
        button_1.destroy()
        drop.destroy()
        from window2 import input_indl_page
        input_indl_page(window, relative_to_assets, unit)

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
    
    img = Image.open(relative_to_assets("image_1.png"))
    img = img.resize((scr_width,int(scr_height)), Image.ANTIALIAS)
    image_image_1 = ImageTk.PhotoImage(img,  master=window)
    image_1 = canvas.create_image(
    0,
    0,
    image=image_image_1,
    anchor="nw"
    )

    window.option_add("*TCombobox*Listbox*Background", "#1d2128")
    window.option_add("*TCombobox*Listbox*Foreground", "#C4F96C")
    window.option_add("*TCombobox*Listbox*Font", "Courier")

    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure('TCombobox',background="#B3E253",fieldbackground="#1d2128",
                    foreground="#C4F96C",darkcolor="#95AF50",selectbackground="grey",lightcolor="#95AC35")
    
    units = ['MIST', 'INFANTRY', 'CAVALRY', 'ARTILLARY', 'ENGINEERS', 'SIGNALS'] 
    variable = StringVar(window)
    drop = ttk.Combobox(window, value = units, textvariable=variable, font=("Courier",30))
    drop.pack(pady=(scr_height/1.925,10))

    button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
    button_1 = Button(
    image=button_image_1,
    borderwidth=0.25,
    bg="#95AC18",
    highlightthickness=2,
    command=lambda: nextPage(variable.get()),
    relief="flat"
    )

    button_1.pack(pady=75)

    min_button = PhotoImage(file=relative_to_assets("minimize.png"))
    button_minimize = Button(
    image=min_button,
    borderwidth=0.25,
    bg="#95AC18",
    highlightthickness=2,
    command=window.iconify,
    relief="flat"
    )
    button_minimize.place(x=scr_width-75*2,y=scr_height-75,width=75,height=75)

    exit_button = PhotoImage(file=relative_to_assets("exit.png"))
    button_exit = Button(
    image=exit_button,
    borderwidth=0.25,
    bg="#95AC00",
    highlightthickness=2,
    command=window.destroy,
    relief="flat"
    )
    button_exit.place(x=scr_width-75,y=scr_height-75,width=75,height=75)
    
    window.resizable(False, False)
    window.mainloop()
    return window