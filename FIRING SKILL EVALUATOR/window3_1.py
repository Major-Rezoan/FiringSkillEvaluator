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

def progress_page(window, relative_to_assets, Army_No_This_Session, indl_groups, unit):

    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()

    Army_No_This_Session = Army_No_This_Session
    indl_groups = indl_groups

    gl_name = []
    gl_rank = []

    gl_svc_length = []
    gl_previous_perf = []
    gl_avg_gp = []
    gl_present_perf = []
    gl_unit = unit

    def store_data(Army_No_This_Session, index, indl_groups):

        conn = sqlite3.connect('firingevaluator.db')
        cur = conn.cursor()
        army_no = Army_No_This_Session[index]
        group = indl_groups[index]

        today = date.today()
        month = today.month

        name = cur.execute("SELECT name FROM personalInfo WHERE army_no=?", (army_no,))
        nm1 = cur.fetchone()
        name = nm1[0]
        gl_name.append(name)

        rank = cur.execute("SELECT rank FROM personalInfo WHERE army_no=?", (army_no,))
        rk1 = cur.fetchone()
        rank = rk1[0]
        gl_rank.append(rank)

        jng_date = cur.execute("SELECT joining_date FROM personalInfo WHERE army_no=?", (army_no,))
        d1 = cur.fetchone()
        jng_date = d1[0]

        last_eval_date = cur.execute("SELECT eval_date FROM evaluationInfo WHERE army_no=? ORDER BY eval_date DESC LIMIT 2 ", (army_no,))
        le1 = cur.fetchall()
        if (len(le1) != 0):
            if (le1[0][0] == str(today) and len(le1) > 1):
                last_eval_date = le1[1][0]
            else:
                last_eval_date = le1[0][0]
        else:
            last_eval_date = today

        no_of_firings = cur.execute("SELECT COUNT(firing_date) FROM firingInfo WHERE army_no=? AND firing_date=?", (army_no, today) )
        nof1 = cur.fetchone()
        no_of_firings = nof1[0]

        interval = cur.execute("SELECT CAST ((JULIANDAY('now') - JULIANDAY(?)) AS INTEGER)", (last_eval_date,))
        int1 = cur.fetchone()
        interval = int(int1[0])

        season = month/2

        prev_perf = cur.execute("SELECT performance FROM performanceInfo WHERE army_no=? ORDER BY perf_date DESC LIMIT 1 ", (army_no,))
        prp1 = cur.fetchone()
        if (prp1 != None):
            prev_perf = prp1[0]
        else:
            prev_perf = 0
        gl_previous_perf.append(prev_perf)

        svc_length = cur.execute("SELECT CAST ((JULIANDAY(?) - JULIANDAY(?)) AS INTEGER)", (today, jng_date))
        sl1 = cur.fetchone()
        svc_length = sl1[0]/365
        gl_svc_length.append(svc_length)

        avg_gp = cur.execute("SELECT AVG(grouping) FROM firingInfo WHERE army_no = ? AND firing_date = ?", (army_no, today))
        avg1 = cur.fetchone()
        avg_gp =(avg1[0])
        gl_avg_gp.append(avg_gp)

        eval_check = cur.execute("SELECT avg_gp FROM evaluationInfo WHERE army_no = ? AND eval_date = ?", (army_no, today))
        pf1 = cur.fetchall()
        if (len(pf1) > 0):
            cur.execute("UPDATE evaluationInfo SET no_of_firings = ?, interval = ?,	season = ?,	svc_length = ?, avg_gp = ? WHERE army_no = ? AND eval_date = ?", (no_of_firings,interval,season,svc_length,avg_gp, army_no, today))
        else:
            cur.execute("INSERT INTO evaluationInfo VALUES (?,?,?,?,?,?,?)", (army_no,today,no_of_firings,interval,season,svc_length,avg_gp))

        path = 'finalCode.exe'
        param = [group,no_of_firings,interval,season,svc_length,avg_gp]
        param = str(param)
        p = subprocess.Popen([path],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        out, err = p.communicate(param)

        performance = out
        gl_present_perf.append(performance)
        perf_check = cur.execute("SELECT performance FROM performanceInfo WHERE army_no = ? AND perf_date = ?", (army_no, today))
        pf1 = cur.fetchall()
        if (len(pf1) > 0):
            cur.execute("UPDATE performanceInfo SET performance = ? WHERE army_no = ? AND perf_date = ?", (performance, army_no, today))
        else:
            cur.execute("INSERT INTO performanceInfo VALUES (?,?,?)", (army_no, today, performance))

        x_perfs = []
        y_dates = []
        graph = cur.execute("SELECT * FROM performanceInfo WHERE army_no = ? ORDER BY perf_date ASC", (army_no, ))
        gr1 = cur.fetchall()
        for i in gr1:
            y_dates.append(i[1])
            x_perfs.append(i[2])

        colors = np.arange(len(x_perfs))

        plt.grid()
        plt.plot(y_dates, x_perfs)
        plt.scatter(y_dates, x_perfs, c=colors)
        plt.yticks(rotation=45) 
        plt.xticks(rotation=65) 
        plt.xlabel('X -----> Dates')
        plt.ylabel('Y -----> Performances')
        plt.title('Performance Graph for ' + rank + ' ' + name)
        mat_file_name = 'data_final/graph' + str(index+1) + '.png'
        plt.savefig(mat_file_name,dpi=300,bbox_inches='tight')
        # plt.show()
        plt.clf()
        
        conn.commit()
        conn.close()

    def nextPage():

        canvas.destroy()
        button_1.destroy()
        frame1.destroy()
        
        from window4 import result_page  
        result_page(window, relative_to_assets, Army_No_This_Session, gl_name, gl_rank, gl_svc_length, gl_previous_perf, gl_avg_gp, gl_present_perf, gl_unit)

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

    frame1=Frame(window, bd=2, bg="#95AC28", relief=RAISED)
    frame1.pack(pady=(int(scr_height/3),15))

    style = ttk.Style()
    style.theme_use('alt')
    style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')

    chandan_progress = ttk.Progressbar(frame1, style="green.Horizontal.TProgressbar", orient=HORIZONTAL, length=400, mode='determinate')
    chandan_progress.pack(padx=15, pady=15)

    lbl_No0=Label(frame1,font=("aria",15,'normal'),text="", bg="#95AC28", fg="#042E04")
    lbl_No0.pack(padx=10, pady=10)

    button_image_1 = PhotoImage(
    file=relative_to_assets("button_7.png"))
    button_1 = Button(
    image=button_image_1,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=nextPage,
    relief="flat"
    )
    button_1.pack(padx=15, pady=15)

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

    bar_value = 0
    lbl_No0.config(text="Calculation Progress..." + str(bar_value) + "%")
    
    for ind in range(0, len(Army_No_This_Session)):
        window.update()
        store_data(Army_No_This_Session, ind, indl_groups)
        chandan_progress.step(12.5)
        bar_value += 12.5
        lbl_No0.config(text="Calculation Progress..." + str(bar_value) + "%")
        window.update()

    bar_value = 100
    lbl_No0.config(text="Calculation Progress..." + str(bar_value) + "%")
    chandan_progress.step(99.99)
    window.update()

        

    window.resizable(False, False)
    window.mainloop()
    return window
