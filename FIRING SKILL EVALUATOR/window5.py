import cv2
import sqlite3
from pathlib import Path
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib import units

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path) 

def show_image(path, win_name, length, width):
    show_img = cv2.imread(path)
    show_img = cv2.resize(show_img, (width,length))
    cv2.imshow(win_name,show_img)

def show_indl_results(window, relative_to_assets, army_no, name, rank, unit, svc_length, previous_perf, avg_gp, present_perf, perf_diff, result_img_path, error_img_path, graph_img_path):
    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()

    def predict_perf(army_no, name, rank):
        from window6 import perf_predict_page

        nw_window = Toplevel()
        nw_window.title("Firing Skill Evaluator Results")
        nw_window.attributes('-fullscreen', True)
        nw_window.configure(bg = "#2DD32C")
        
        conn = sqlite3.connect('firingevaluator.db')
        cur = conn.cursor()
        X_Data = cur.execute("SELECT evaluationInfo.no_of_firings, evaluationInfo.interval, evaluationInfo.season, evaluationInfo.svc_length, evaluationInfo.avg_gp FROM evaluationInfo JOIN performanceInfo WHERE evaluationInfo.army_no = performanceInfo.army_no AND evaluationInfo.eval_date = performanceInfo.perf_date")
        x1 = cur.fetchall()
        X_Data = x1
        X = []
        for row in X_Data:
            X.append(list(row))

        Y_Data = cur.execute("SELECT performanceInfo.performance FROM evaluationInfo JOIN performanceInfo WHERE evaluationInfo.army_no = performanceInfo.army_no AND evaluationInfo.eval_date = performanceInfo.perf_date")
        y1 = cur.fetchall()
        Y_Data = y1
        Y = []
        for row in Y_Data:
            Y.append(list(row))

        conn.commit()
        conn.close()

        perf_predict_page(nw_window, relative_to_assets, name, rank, svc_length, avg_gp, X, Y)

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
    image_image_1 = ImageTk.PhotoImage(img, master=window)
    image_1 = canvas.create_image(
    0,
    0,
    image=image_image_1,
    anchor="nw"
    )

    frame1=Frame(window, bd=2, bg="#95AC28", height=scr_height*(9/10), width=scr_width/2, relief=RAISED)
    frame1.pack(side=LEFT, padx=(80,1),pady=(80,60))
    frame1.pack_propagate(0)

    frame2=Frame(window, bd=2, bg="#95AC28", height=scr_height*(9/10), width=scr_width/4, relief=RAISED)
    frame2.pack(side=RIGHT, padx=(1,80),pady=(110,90))
    frame2.pack_propagate(0)

    img1 = Image.open(result_img_path)
    img1 = img1.resize((980,485), Image.ANTIALIAS)
    result_img1 = ImageTk.PhotoImage(img1, master=window)

    img2 = Image.open(error_img_path)
    img2 = img2.resize((360,275), Image.ANTIALIAS)
    result_img2 = ImageTk.PhotoImage(img2, master=window)

    img3 = Image.open(graph_img_path)
    img3 = img3.resize((360,275), Image.ANTIALIAS)
    result_img3 = ImageTk.PhotoImage(img3, master=window)

    label1_1 = Label(frame1, font=("aria",15,'bold'),text="Army No: " + army_no, bg="#95AC28", fg="#042E04",anchor=W, width=30, borderwidth=3, relief=RIDGE)
    label1_1.grid(row=0, column=0, columnspan=3, rowspan=1, padx=2, pady=2)
    label1_2 = Label(frame1, font=("aria",15,'bold'),text="Rank: " + rank, bg="#95AC28", fg="#042E04",anchor=W, width=20, borderwidth=3, relief=RIDGE)
    label1_2.grid(row=0, column=3, columnspan=2, rowspan=1, padx=2, pady=2, sticky=W+N)
    label1_3 = Label(frame1, font=("aria",15,'bold'),text="Unit: " + unit, bg="#95AC28", fg="#042E04",anchor=W, width=30, borderwidth=3, relief=RIDGE)
    label1_3.grid(row=0, column=5, columnspan=3, rowspan=1, padx=2, pady=2, sticky=W+N)
    
    label2_1 = Label(frame1, font=("aria",15,'bold'),text="Name: " + name, bg="#95AC28", fg="#042E04",anchor=W, width=51, borderwidth=3, relief=RIDGE)
    label2_1.grid(row=1, column=0, columnspan=5, rowspan=1, padx=2, pady=2, sticky=W)
    label2_2 = Label(frame1, font=("aria",15,'bold'),text="Svc Length: " + str(svc_length), bg="#95AC28", fg="#042E04",anchor=W, width=30, borderwidth=3, relief=RIDGE)
    label2_2.grid(row=1, column=5, columnspan=3, rowspan=1, padx=2, pady=2, sticky=W)

    label3_1 = Label(frame1, font=("aria",15,'bold'),text="Previous Performance: " + str(previous_perf), bg="#95AC28", fg="#042E04",anchor=W, width=30, borderwidth=3, relief=RIDGE)
    label3_1.grid(row=2, column=0, columnspan=3, rowspan=1, padx=2, pady=2, sticky=W+N)
    label3_2 = Label(frame1, font=("aria",15,'bold'),text="Avg Gp: " + str(avg_gp), bg="#95AC28", fg="#042E04",anchor=W, width=20, borderwidth=3, relief=RIDGE)
    label3_2.grid(row=2, column=3, columnspan=2, rowspan=1, padx=2, pady=2, sticky=W+N)
    label3_3 = Label(frame1, font=("aria",15,'bold'),text="Present Performance: " + str(present_perf), bg="#95AC28", fg="#042E04",anchor=W, width=30, borderwidth=3, relief=RIDGE)
    label3_3.grid(row=2, column=5, columnspan=3, rowspan=1, padx=2, pady=2, sticky=W+N)
    if (previous_perf != 0):
        if (perf_diff > 0):
            label3_3_1 = Label(frame1, font=("aria",13,'bold'),text=u'\u2191', bg="yellow", fg="green")
            label3_3_1.grid(row=2, column=7, padx=1, pady=1)
        else:
            label3_3_2 = Label(frame1, font=("aria",13,'bold'),text=u'\u2193', bg="yellow", fg="red")
            label3_3_2.grid(row=2, column=7, padx=1, pady=1)
    
    label4 = Button(frame1, image = result_img1,  command=lambda:show_image(result_img_path, 'Firing Result', 750, 1500),  height=500, width=80, bg="#95AC28", borderwidth=3, relief=RIDGE)
    label4.grid(row=3, column=0, columnspan=8, rowspan=8, padx=2, pady=2, sticky=E+W+S+N)

    label5 = Label(frame1, font=("aria",15,'bold'),text="OVERALL RESULT", bg="#95AC28", fg="#042E04", height=1, width=82, borderwidth=3, relief=RIDGE)
    label5.grid(row=11, column=0, columnspan=8, rowspan=1, padx=2, pady=2, sticky=W+N)

    label5_1 = Button(frame2, image = result_img2, command=lambda:show_image(error_img_path, 'Error Analysis', 750, 800), height=280, width=30, bg="#95AC28", borderwidth=3, relief=RIDGE)
    label5_1.grid(row=0, column=0, columnspan=3, rowspan=1, padx=2, pady=2, sticky=E+W+S+N)
    label5_2 = Label(frame2, font=("aria",15,'bold'),text="ERRORS", bg="#95AC28", fg="#042E04", height=1, width=30, borderwidth=3, relief=RIDGE)
    label5_2.grid(row=1, column=0, columnspan=3, rowspan=1, padx=2, pady=2, sticky=W+N)

    label6 = Button(frame2, image = result_img3,  command=lambda:show_image(graph_img_path, 'Performance Graph', 750, 1100),  height=280, width=30, bg="#95AC28", borderwidth=3, relief=RIDGE)
    label6.grid(row=2, column=0, columnspan=3, rowspan=1, padx=2, pady=2, sticky=E+W+S+N)    
    label8_2 = Label(frame2, font=("aria",15,'bold'),text="PERFORMANCE GRAPH", bg="#95AC28", fg="#042E04", height=1, width=30, borderwidth=3, relief=RIDGE)
    label8_2.grid(row=3, column=0, columnspan=3, rowspan=1, padx=2, pady=2, sticky=W+N)

    pred_img = Image.open(relative_to_assets("button_9.png"))  
    pred_button = ImageTk.PhotoImage(pred_img, master=window)
    button_predict = Button(window,
    image=pred_button,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=lambda: predict_perf(army_no, name, rank),
    relief="flat"
    )
    button_predict.place(x=scr_width-375,y=scr_height-75,width=300,height=75)

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
