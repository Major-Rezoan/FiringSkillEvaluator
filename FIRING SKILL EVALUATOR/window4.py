import cv2
import sqlite3
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import date

today = date.today()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def result_page(window, relative_to_assets, Army_No_This_Session, gl_name, gl_rank, gl_svc_length, gl_previous_perf, gl_avg_gp, gl_present_perf, gl_unit):
    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()

    gl_name = gl_name
    gl_rank = gl_rank

    gl_svc_length = gl_svc_length
    gl_previous_perf = gl_previous_perf
    gl_avg_gp = gl_avg_gp
    gl_present_perf = gl_present_perf
    gl_unit = gl_unit
        
    def nextPage(army_no_from_prev,index):
        from window5 import show_indl_results

        n_window = Toplevel()
        n_window.title("Firing Skill Evaluator Results")
        n_window.attributes('-fullscreen', True)
        n_window.configure(bg = "#2DD32C")

        conn = sqlite3.connect('firingevaluator.db')
        cur = conn.cursor()


        army_no = army_no_from_prev
        name = gl_name[index-1]
        rank = gl_rank[index-1]
        unit = gl_unit

        svc_length = gl_svc_length[index-1]
        svc_length = round(float(svc_length), 2)
        previous_perf = gl_previous_perf[index-1]
        if previous_perf != '':
            previous_perf = int(previous_perf)
            previous_perf = round(float(previous_perf), 2)
        else:
            previous_perf = 0

        avg_gp = '15.85'
        avg_gp = round(float(avg_gp), 2)
        present_perf = gl_present_perf[index-1]
        present_perf = round(float(present_perf), 2)
        perf_diff = present_perf - previous_perf

        result_img_path = "data_final/FiringResult" + str(index) + ".jpg"
        error_img_path = "data_final/Error" + str(index) + ".jpg"
        graph_img_path = "data_final/graph" + str(index) + ".png"
        
        show_indl_results(n_window, relative_to_assets, army_no, name, rank, unit, svc_length, previous_perf, avg_gp, present_perf, perf_diff, result_img_path, error_img_path, graph_img_path)

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

    frame1=Frame(window, bd=2, bg="#95AC28", height=scr_height-(scr_height/8.5)*2.25, width=1100, relief=RAISED)
    frame1.pack(padx=scr_height/5,pady=scr_height/8.5)

    result_1 = Image.open("data_final/FiringResult1.jpg")
    result_1 = result_1.resize((300,150), Image.ANTIALIAS)
    result_1 = ImageTk.PhotoImage(result_1)
    result_show_1 = cv2.imread("data_final/FiringResult1.jpg")
    result_show_1 = cv2.resize(result_show_1, (1200,600))

    img_button_1 = Button(
    image=result_1,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[0],1),
    relief="flat"
)
    img_button_1.place(
    x=425.0,
    y=scr_height/8,
)

    result_2 = Image.open("data_final/FiringResult2.jpg")
    result_2 = result_2.resize((300,150), Image.ANTIALIAS)
    result_2 = ImageTk.PhotoImage(result_2)
    result_show_2 = cv2.imread("data_final/FiringResult2.jpg")
    result_show_2 = cv2.resize(result_show_2, (1000,500))

    img_button_2 = Button(
    image=result_2,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[1],2),
    relief="flat"
)
    img_button_2.place(
    x=995.0,
    y=scr_height/8,
)

    result_3 = Image.open("data_final/FiringResult3.jpg")
    result_3 = result_3.resize((300,150), Image.ANTIALIAS)
    result_3 = ImageTk.PhotoImage(result_3)
    result_show_3 = cv2.imread("data_final/FiringResult3.jpg")
    result_show_3 = cv2.resize(result_show_3, (1000,500))

    img_button_3 = Button(
    image=result_3,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[2],3),
    relief="flat"
)
    img_button_3.place(
    x=425.0,
    y=scr_height/8+165.0,
)

    result_4 = Image.open("data_final/FiringResult4.jpg")
    result_4 = result_4.resize((300,150), Image.ANTIALIAS)
    result_4 = ImageTk.PhotoImage(result_4)
    result_show_4 = cv2.imread("data_final/FiringResult4.jpg")
    result_show_4 = cv2.resize(result_show_4, (1000,500))

    img_button_4 = Button(
    image=result_4,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[3],4),
    relief="flat"
)
    img_button_4.place(
    x=995.0,
    y=scr_height/8+165.0,
)

    result_5 = Image.open("data_final/FiringResult5.jpg")
    result_5 = result_5.resize((300,150), Image.ANTIALIAS)
    result_5 = ImageTk.PhotoImage(result_5)
    result_show_5 = cv2.imread("data_final/FiringResult5.jpg")
    result_show_5 = cv2.resize(result_show_5, (1000,500))

    img_button_5 = Button(
    image=result_5,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[4],5),
    relief="flat"
)
    img_button_5.place(
    x=425.0,
    y=scr_height/8+165.0*2,
)
    result_6 = Image.open("data_final/FiringResult6.jpg")
    result_6 = result_6.resize((300,150), Image.ANTIALIAS)
    result_6 = ImageTk.PhotoImage(result_6)
    result_show_6 = cv2.imread("data_final/FiringResult6.jpg")
    result_show_6 = cv2.resize(result_show_6, (1000,500))

    img_button_6 = Button(
    image=result_6,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[5],6),
    relief="flat"
)
    img_button_6.place(
    x=995.0,
    y=scr_height/8+165.0*2,
)

    result_7 = Image.open("data_final/FiringResult7.jpg")
    result_7 = result_7.resize((300,150), Image.ANTIALIAS)
    result_7 = ImageTk.PhotoImage(result_7)
    result_show_7 = cv2.imread("data_final/FiringResult7.jpg")
    result_show_7 = cv2.resize(result_show_7, (1000,500))

    img_button_7 = Button(
    image=result_7,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[6],7),
    relief="flat"
)
    img_button_7.place(
    x=425.0,
    y=scr_height/8+165.0*3,
)

    result_8 = Image.open("data_final/FiringResult8.jpg")
    result_8 = result_8.resize((300,150), Image.ANTIALIAS)
    result_8 = ImageTk.PhotoImage(result_8)
    result_show_8 = cv2.imread("data_final/FiringResult8.jpg")
    result_show_8 = cv2.resize(result_show_8, (1000,500))

    img_button_8 = Button(
    image=result_8,
    borderwidth=2,
    bg="green",
    highlightthickness=1,
    command=lambda: nextPage(Army_No_This_Session[7],8),
    relief="flat"
)
    img_button_8.place(
    x=995.0,
    y=scr_height/8+165.0*3,
)


    lbl_No1=Label(frame1,font=("aria",25,'bold'),text="Target No-1:", bg="#95AC28", fg="#042E04")
    lbl_No1.grid(row=1,column=0, padx=30, pady=70)
    lbl_No2=Label(frame1,font=("aria",25,'bold'),text="Target No-2:", bg="#95AC28", fg="#042E04")
    lbl_No2.grid(row=1,column=1, padx=340, pady=70)
    lbl_No3=Label(frame1,font=("aria",25,'bold'),text="Target No-3:", bg="#95AC28", fg="#042E04")
    lbl_No3.grid(row=2,column=0, padx=5, pady=50)
    lbl_No4=Label(frame1,font=("aria",25,'bold'),text="Target No-4:", bg="#95AC28", fg="#042E04")
    lbl_No4.grid(row=2,column=1, padx=340, pady=50)
    lbl_No5=Label(frame1,font=("aria",25,'bold'),text="Target No-5:", bg="#95AC28", fg="#042E04")
    lbl_No5.grid(row=3,column=0, padx=5, pady=60)
    lbl_No6=Label(frame1,font=("aria",25,'bold'),text="Target No-6:", bg="#95AC28", fg="#042E04")
    lbl_No6.grid(row=3,column=1, padx=340, pady=60)
    lbl_No7=Label(frame1,font=("aria",25,'bold'),text="Target No-7:", bg="#95AC28", fg="#042E04")
    lbl_No7.grid(row=4,column=0, padx=5, pady=65)
    lbl_No8=Label(frame1,font=("aria",25,'bold'),text="Target No-8:", bg="#95AC28", fg="#042E04")
    lbl_No8.grid(row=4,column=1, padx=340, pady=65)
    
    back_button = PhotoImage(file=relative_to_assets("back.png"))
    button_back = Button(
    image=back_button,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=window.iconify,
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

    window.resizable(False, False)
    window.mainloop()
    return window
