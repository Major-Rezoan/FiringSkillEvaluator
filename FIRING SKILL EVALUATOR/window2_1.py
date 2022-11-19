import sqlite3
from pathlib import Path

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def input_indl_page_compile(window, relative_to_assets, Army_No_This_Session, unit):
    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()
    unit = unit
    Army_No_This_Session = Army_No_This_Session

    def nextPage():
        canvas.destroy()
        button_1.destroy()
        from window3 import input_image_page
        input_image_page(window, relative_to_assets, Army_No_This_Session, unit)

    def previousPage():
        canvas.destroy()
        button_1.destroy()
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

    button_image_1 = PhotoImage(
    file=relative_to_assets("button_3.png"))
    button_1 = Button(
    image=button_image_1,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=nextPage,
    relief="flat"
    )
    button_1.pack(padx=50, pady=350)

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