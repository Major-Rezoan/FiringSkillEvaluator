
import numpy as np
import cv2
import sqlite3
from pathlib import Path
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import *
from tkinter import ttk
from similarity_finding import ssi_processing
from scan_preprocess import scan_and_preprocess
from final_calculation import calc_result
from PIL import ImageTk, Image
from datetime import date

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

today = date.today()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

fin_ld_img = []
fin_ld_img_path = []

def load_img(number, period):
    img_file='input'+str(number)+period 
    ld_img_path="input_data/"+img_file+".jpeg"
    fin_ld_img_path.append(ld_img_path)
    ld_img = Image.open(ld_img_path)

    ld_img = ld_img.resize((125,125), Image.ANTIALIAS)
    ld_img = ImageTk.PhotoImage(ld_img)
    fin_ld_img.append(ld_img)
    return ld_img

def show_image(path, no, pd):
    show_img = cv2.imread(path)
    show_img = cv2.resize(show_img, (750,750))
    if (pd == 'a'):
        period = 'After Firing'
    else:
        period = 'Before Firing'
    window_name = 'Target ' + str(no+1) + ' Input Image - ' + str(period)
    cv2.imshow(window_name,show_img)

def upload_file(frame_num,row_num,col_num,time_pd):
    f_types = [('Jpeg Files', '*.jpeg')]
    file_path = filedialog.askopenfilename(filetypes=f_types)
    upld_img=Image.open(file_path)
    upld_img_resized=upld_img.resize((125,125))
    fin_upld_img=ImageTk.PhotoImage(upld_img_resized)
    updt_row_num = row_num
    if row_num < 6:
        if (time_pd == 'b'):
            index = row_num-2
        else:
            index = row_num+2
    else:
        updt_row_num = row_num-4
        if (time_pd == 'b'):
            index = row_num+2
        else:
            index = row_num+6
    fin_ld_img[index] = fin_upld_img
    fin_ld_img_path[index] = file_path
    b2 =Button(frame_num,image=fin_ld_img[index],command=lambda:show_image(fin_ld_img_path[index],row_num-2,time_pd)) # using Button 
    b2.grid(row=updt_row_num,column=col_num)

def input_image_page(window, relative_to_assets, Army_No_This_Session, unit):
    scr_height = window.winfo_screenheight()
    scr_width = window.winfo_screenwidth()
    unit = unit

    def insertIntoDatabase(Army_No_This_Session,indl_groups, indl_errors):
        conn = sqlite3.connect('firingevaluator.db')
        cur = conn.cursor()
        for i in range(0,len(Army_No_This_Session)):
            cur.execute("INSERT INTO firingInfo VALUES(?,?,?,?)",(Army_No_This_Session[i], today, indl_groups[i], indl_errors[i]))
        conn.commit()
        conn.close()

    def nextPage():
        canvas.destroy()
        button_1.destroy()
        frame1.destroy()
        frame2.destroy()

        scanned_image_before, scanned_image_after = scan_and_preprocess(fin_ld_img_path)
        ssi_images, ssi_processed_masks = ssi_processing(scanned_image_before, scanned_image_after)
        indl_groups, indl_errors = calc_result(ssi_images, ssi_processed_masks)
        
        insertIntoDatabase(Army_No_This_Session,indl_groups, indl_errors)
        
        from window3_1 import progress_page
        progress_page(window, relative_to_assets, Army_No_This_Session, indl_groups, unit)

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
    file=relative_to_assets("button_6.png"))
    button_1 = Button(
    image=button_image_1,
    borderwidth=0.25,
    bg="#B4D177",
    highlightthickness=2,
    command=nextPage,
    relief="flat"
    )
    button_1.place(
    x=scr_width-320,
    y=scr_height-160.0
    )


    frame1=Frame(window, bd=2, bg="#95AC28", height=scr_height-200, width=scr_width-400, relief=RAISED)
    frame1.pack(side=LEFT, padx=(125,2),pady=(60,100))
    frame1.pack_propagate(0)

    No1=StringVar()
    No2=StringVar()
    No3=StringVar()
    No4=StringVar()
    No5=StringVar()
    No6=StringVar()
    No7=StringVar()
    No8=StringVar()

    lbl_No0=Label(frame1,font=("aria",20,'bold'),text="Before Firing   ", bg="#95AC28", fg="#042E04")
    lbl_No0.grid(row=1,column=1, columnspan=2, padx=5, pady=5)
    lbl_No0=Label(frame1,font=("aria",20,'bold'),text="After Firing     ", bg="#95AC28", fg="#042E04")
    lbl_No0.grid(row=1,column=3, columnspan=2, padx=5, pady=5)
    lbl_No1=Label(frame1,font=("aria",20,'bold'),text="Target No-1", bg="#95AC28", width=12,fg="#042E04")
    lbl_No1.grid(row=2,column=0, padx=5, pady=5)
    lbl_No2=Label(frame1,font=("aria",20,'bold'),text="Target No-2", bg="#95AC28", width=12,fg="#042E04")
    lbl_No2.grid(row=3,column=0, padx=5, pady=5)
    lbl_No3=Label(frame1,font=("aria",20,'bold'),text="Target No-3", bg="#95AC28", width=12,fg="#042E04")
    lbl_No3.grid(row=4,column=0, padx=5, pady=5)
    lbl_No4=Label(frame1,font=("aria",20,'bold'),text="Target No-4", bg="#95AC28", width=12,fg="#042E04")
    lbl_No4.grid(row=5,column=0, padx=5, pady=5)

    upload_img = Image.open(relative_to_assets("upload.png"))
    upload_img = upload_img.resize((42,42), Image.ANTIALIAS)
    upload_img = ImageTk.PhotoImage(upload_img)

    left_ld_img1 = load_img(1,'b')
    left_loaded_img_1=Button(frame1,image=fin_ld_img[0],command=lambda:show_image(fin_ld_img_path[0],0,'b'))
    left_loaded_img_1.grid(row=2,column=1)
    left_loaded_img_1_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,2,1,'b'),relief="flat")
    left_loaded_img_1_upbt.grid(row=2,column=2,padx=5)

    left_ld_img2 = load_img(2,'b')
    left_loaded_img_2=Button(frame1,image=fin_ld_img[1],command=lambda:show_image(fin_ld_img_path[1],1,'b'))
    left_loaded_img_2.grid(row=3,column=1)
    left_loaded_img_2_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,3,1,'b'),relief="flat")
    left_loaded_img_2_upbt.grid(row=3,column=2)

    left_ld_img3 = load_img(3,'b')
    left_loaded_img_3=Button(frame1,image=fin_ld_img[2],command=lambda:show_image(fin_ld_img_path[2],2,'b'))
    left_loaded_img_3.grid(row=4,column=1)
    left_loaded_img_3_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,4,1,'b'),relief="flat")
    left_loaded_img_3_upbt.grid(row=4,column=2)

    left_ld_img4 = load_img(4,'b')
    left_loaded_img_4=Button(frame1,image=fin_ld_img[3],command=lambda:show_image(fin_ld_img_path[3],3,'b'))
    left_loaded_img_4.grid(row=5,column=1)
    left_loaded_img_4_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,5,1,'b'),relief="flat")
    left_loaded_img_4_upbt.grid(row=5,column=2)

    Name1=StringVar()
    Name2=StringVar()
    Name3=StringVar()
    Name4=StringVar()
    Name5=StringVar()
    Name6=StringVar()
    Name7=StringVar()
    Name8=StringVar()
    
    right_ld_img1 = load_img(1,'a')
    right_loaded_img_1=Button(frame1,image=fin_ld_img[4],command=lambda:show_image(fin_ld_img_path[4],0,'a'))
    right_loaded_img_1.grid(row=2,column=3)
    right_loaded_img_1_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,2,3,'a'),relief="flat")
    right_loaded_img_1_upbt.grid(row=2,column=4)

    right_ld_img2 = load_img(2,'a')
    right_loaded_img_2=Button(frame1,image=fin_ld_img[5],command=lambda:show_image(fin_ld_img_path[5],1,'a'))
    right_loaded_img_2.grid(row=3,column=3)
    right_loaded_img_2_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,3,3,'a'),relief="flat")
    right_loaded_img_2_upbt.grid(row=3,column=4)

    right_ld_img3 = load_img(3,'a')
    right_loaded_img_3=Button(frame1,image=fin_ld_img[6],command=lambda:show_image(fin_ld_img_path[6],2,'a'))
    right_loaded_img_3.grid(row=4,column=3)
    right_loaded_img_3_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,4,3,'a'),relief="flat")
    right_loaded_img_3_upbt.grid(row=4,column=4)

    right_ld_img4 = load_img(4,'a')
    right_loaded_img_4=Button(frame1,image=fin_ld_img[7],command=lambda:show_image(fin_ld_img_path[7],3,'a'))
    right_loaded_img_4.grid(row=5,column=3)
    right_loaded_img_4_upbt=Button(frame1,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame1,5,3,'a'),relief="flat")
    right_loaded_img_4_upbt.grid(row=5,column=4)



    frame2=Frame(window, bd=2, bg="#95AC28", height=scr_height-200, width=scr_width-400, relief=RAISED)
    frame2.pack(side=RIGHT, padx=(1,125),pady=(60,100))
    frame2.pack_propagate(0)

    lbl_No0=Label(frame2,font=("aria",20,'bold'),text="Before Firing   ", bg="#95AC28", fg="#042E04")
    lbl_No0.grid(row=1,column=1, columnspan=2, padx=5, pady=5)
    lbl_No0=Label(frame2,font=("aria",20,'bold'),text="After Firing     ", bg="#95AC28", fg="#042E04")
    lbl_No0.grid(row=1,column=3, columnspan=2, padx=5, pady=5)
    lbl_No5=Label(frame2,font=("aria",20,'bold'),text="Target No-5", bg="#95AC28", width=12,fg="#042E04")
    lbl_No5.grid(row=2,column=0, padx=5, pady=5)
    lbl_No6=Label(frame2,font=("aria",20,'bold'),text="Target No-6", bg="#95AC28", width=12,fg="#042E04")
    lbl_No6.grid(row=3,column=0, padx=5, pady=5)
    lbl_No7=Label(frame2,font=("aria",20,'bold'),text="Target No-7", bg="#95AC28", width=12,fg="#042E04")
    lbl_No7.grid(row=4,column=0, padx=5, pady=5)
    lbl_No8=Label(frame2,font=("aria",20,'bold'),text="Target No-8", bg="#95AC28", width=12,fg="#042E04")
    lbl_No8.grid(row=5,column=0, padx=5, pady=5)
    
    left_ld_img5 = load_img(5,'b')
    left_loaded_img_5=Button(frame2,image=fin_ld_img[8],command=lambda:show_image(fin_ld_img_path[8],4,'b'))
    left_loaded_img_5.grid(row=2,column=1)
    left_loaded_img_5_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,6,1,'b'),relief="flat")
    left_loaded_img_5_upbt.grid(row=2,column=2)

    left_ld_img6 = load_img(6,'b')
    left_loaded_img_6=Button(frame2,image=fin_ld_img[9],command=lambda:show_image(fin_ld_img_path[9],5,'b'))
    left_loaded_img_6.grid(row=3,column=1)
    left_loaded_img_6_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,7,1,'b'),relief="flat")
    left_loaded_img_6_upbt.grid(row=3,column=2)

    left_ld_img7 = load_img(7,'b')
    left_loaded_img_7=Button(frame2,image=fin_ld_img[10],command=lambda:show_image(fin_ld_img_path[10],6,'b'))
    left_loaded_img_7.grid(row=4,column=1)
    left_loaded_img_7_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,8,1,'b'),relief="flat")
    left_loaded_img_7_upbt.grid(row=4,column=2)

    left_ld_img8 = load_img(8,'b')
    left_loaded_img_8=Button(frame2,image=fin_ld_img[11],command=lambda:show_image(fin_ld_img_path[11],7,'b'))
    left_loaded_img_8.grid(row=5,column=1)
    left_loaded_img_8_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,9,1,'b'),relief="flat")
    left_loaded_img_8_upbt.grid(row=5,column=2)

    right_ld_img5 = load_img(5,'a')
    right_loaded_img_5=Button(frame2,image=fin_ld_img[12],command=lambda:show_image(fin_ld_img_path[12],4,'a'))
    right_loaded_img_5.grid(row=2,column=3)
    right_loaded_img_5_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,6,3,'a'),relief="flat")
    right_loaded_img_5_upbt.grid(row=2,column=4)

    right_ld_img6 = load_img(6,'a')
    right_loaded_img_6=Button(frame2,image=fin_ld_img[13],command=lambda:show_image(fin_ld_img_path[13],5,'a'))
    right_loaded_img_6.grid(row=3,column=3)
    right_loaded_img_6_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,7,3,'a'),relief="flat")
    right_loaded_img_6_upbt.grid(row=3,column=4)

    right_ld_img7 = load_img(7,'a')
    right_loaded_img_7=Button(frame2,image=fin_ld_img[14],command=lambda:show_image(fin_ld_img_path[14],6,'a'))
    right_loaded_img_7.grid(row=4,column=3)
    right_loaded_img_7_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,8,3,'a'),relief="flat")
    right_loaded_img_7_upbt.grid(row=4,column=4)

    right_ld_img8 = load_img(8,'a')
    right_loaded_img_8=Button(frame2,image=fin_ld_img[15],command=lambda:show_image(fin_ld_img_path[15],7,'a'))
    right_loaded_img_8.grid(row=5,column=3)
    right_loaded_img_8_upbt=Button(frame2,image=upload_img,bg="#B4D177",height=40,width=40,command=lambda:upload_file(frame2,9,3,'a'),relief="flat")
    right_loaded_img_8_upbt.grid(row=5,column=4)


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

    window.mainloop()
    return window
