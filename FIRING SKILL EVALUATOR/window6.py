import sqlite3
from pathlib import Path

import pandas as pd
import numpy as np
import scipy as sp
from sklearn.linear_model import LinearRegression
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def perf_predict_page(window, relative_to_assets,  name, rank, svc_length, avg_gp, X, Y):

    global result
    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()

    def predict_performance(v1,v2, v3, v4, v5, X, Y):

        X = np.array(X)
        Y = np.array(Y)
   
        reg = LinearRegression().fit(X, Y)
        result = reg.predict(np.array([[float(v1), float(v2), float(v3)/2, float(v4), float(v5)]]))

        result = round(result[0][0],2)
        entry_No6=Label(frame1,font=("aria",20,'bold'),text=str(result), bg="#95AC28", bd=4, width=9, height=1,fg="#042E04")
        entry_No6.grid(row=3,column=3, padx=5, pady=5)

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

    frame1=Frame(window, bd=2, bg="#95AC28", height=scr_height/1.75, width=200, relief=RAISED)
    frame1.pack(padx=10,pady=(250,15))

    lbl_hd=Label(frame1,font=("aria",20,'bold'),text="Name: " + rank + ' ' + name, bg="#95AC28", width=50,fg="#042E04")
    lbl_hd.grid(row=0,column=0, columnspan=5, padx=5, pady=5)

    lbl_No0=Label(frame1,font=("aria",20,'bold'),text="No of Firing", bg="#95AC28", width=10,fg="#042E04")
    lbl_No0.grid(row=1,column=0, padx=5, pady=5)
    lbl_No1=Label(frame1,font=("aria",20,'bold'),text="Interval", bg="#95AC28", width=10,fg="#042E04")
    lbl_No1.grid(row=1,column=1, padx=5, pady=5)
    lbl_No2=Label(frame1,font=("aria",20,'bold'),text="Month", bg="#95AC28", width=10,fg="#042E04")
    lbl_No2.grid(row=1,column=2, padx=5, pady=5)
    lbl_No3=Label(frame1,font=("aria",20,'bold'),text="Svc Length", bg="#95AC28", width=10,fg="#042E04")
    lbl_No3.grid(row=1,column=3, padx=5, pady=5)
    lbl_No4=Label(frame1,font=("aria",20,'bold'),text="Avg Gp", bg="#95AC28", width=10,fg="#042E04")
    lbl_No4.grid(row=1,column=4, padx=5, pady=5)

    result = StringVar()

    lbl_No5=Label(frame1,font=("aria",20,'bold'),text="Predicted Performance Rate:", bg="#95AC28", width=30,fg="#042E04", anchor=E)
    lbl_No5.grid(row=3,column=0, columnspan=3, padx=5, pady=5)
    entry_No6=Label(frame1,font=("aria",20,'bold'),text="", bg="#95AC28", bd=4, width=10,fg="#042E04")
    entry_No6.grid(row=3,column=3, padx=5, pady=5)
    lbl_No6=Label(frame1,font=("aria",20,'bold'),text="%", bg="#95AC28", width=10,fg="#042E04", anchor=W)
    lbl_No6.grid(row=3,column=4, padx=5, pady=5)

    No1=StringVar()
    No2=StringVar()
    No3=StringVar()
    No4=StringVar(window, value=svc_length)
    No5=StringVar(window, value=avg_gp)

    entry_No1=Entry(frame1,font=("aria",20,'bold'),textvariable=No1, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_No1.grid(row=2,column=0, padx=5, pady=5)
    entry_No2=Entry(frame1,font=("aria",20,'bold'),textvariable=No2, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_No2.grid(row=2,column=1, padx=5, pady=5)
    entry_No3=Entry(frame1,font=("aria",20,'bold'),textvariable=No3, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_No3.grid(row=2,column=2, padx=5, pady=5)
    entry_No4=Entry(frame1,font=("aria",20,'bold'),textvariable=No4, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_No4.grid(row=2,column=3, padx=5, pady=5)
    entry_No5=Entry(frame1,font=("aria",20,'bold'),textvariable=No5, bg="#98FF98", bd=4, width=10,fg="#042E04")
    entry_No5.grid(row=2,column=4, padx=5, pady=5)

    pred_img = Image.open(relative_to_assets("button_9.png"))   
    button_image_1 = ImageTk.PhotoImage(pred_img, master=window)
    button_1 = Button(window,
    image=button_image_1,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=lambda:predict_performance(No1.get(), No2.get(), No3.get(), No4.get(), No5.get(), X, Y),
    relief="flat"
    )
    button_1.pack()

    close_img = Image.open(relative_to_assets("exit.png"))   
    exit_button = ImageTk.PhotoImage(close_img, master=window)
    button_exit = Button(window,
    image=exit_button,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=window.destroy,
    relief="flat"
    )
    button_exit.place(x=scr_width-75,y=scr_height-75,width=75,height=75)


    window.resizable(False, False)
    window.mainloop()
    return window