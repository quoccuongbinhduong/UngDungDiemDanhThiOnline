from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import csv
import subprocess
from PIL import Image, ImageTk
import mysql.connector
from  tkinter import  messagebox
import tensorflow as tf

import facenet
import mysql.connector
import pickle
import align.detect_face
import numpy as np
import cv2
import collections
import  imutils
from datetime import datetime
mydata=[]

class Video:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x650+0+0")
        self.root.title("Hệ thống nhận điểm danh nhận diện khuôn mặt")

        self.var_MaMH = StringVar()
        self.var_MonHoc = StringVar()
        self.var_NamHoc = StringVar()
        self.var_HocKy = StringVar()
        self.var_maSV = StringVar()
        self.var_HoTen = StringVar()
        self.var_Lop = StringVar()
        self.var_GioiTinh = StringVar()
        self.var_NgaySinh = StringVar()
        self.var_ThamGia = StringVar()

        img = Image.open(r"D:\CuongDoAn\DoAn\image\hinh giao dien.jpg")
        img = img.resize((1250, 650), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=1250, height=650)

        title_lbl = Label(f_lbl, text="Nhận diện bằng video",
                          font=("time new roman", 30, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1250, height=45)

        main_frame =Frame(f_lbl, bd=2, bg="white")
        main_frame.place(x=2,y=50, width=1240, height=590)

        # bảng bên trái
        self.left_frame =LabelFrame(main_frame, bd=2,bg="white", relief=RIDGE, text="Thông tin sinh viên",font=("times new roman",12,"bold"))
        self.left_frame.place(x=4,y= 4, width=600, height=580)

        # Khóa học
        current_course_frame = LabelFrame(self.left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin môn học",
                                font=("times new roman", 12, "bold"))
        current_course_frame.place(x=4, y=4, width=590, height=150)
        dep_label=Label(current_course_frame, text="Mã môn học:",font=("times new roman",12,"bold"),bg="white")
        dep_label.grid(row=0, column=0,pady=10)

        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_MaMH,font=("times new roman",12,"bold"),state="readonly")
        dep_combo['values']=("Chọn mã môn học","TI102", "TI264","TI210","TI210")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10, sticky=W)

        #năm học
        year_label = Label(current_course_frame, text="Năm học:", font=("times new roman", 12, "bold"), bg="white")
        year_label.grid(row=1, column=0, pady=10,sticky=W)

        year_combo = ttk.Combobox(current_course_frame,textvariable=self.var_NamHoc, font=("times new roman", 12, "bold"), state="readonly")
        year_combo['values'] = ("Chọn năm học", "2021-2022", "2022-2023", "2023-2024")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        #Khóa học
        course_label = Label(current_course_frame, text="Môn học:", font=("times new roman", 12, "bold"), bg="white")
        course_label.grid(row=0, column=2, pady=10)

        course_combo = ttk.Combobox(current_course_frame,textvariable=self.var_MonHoc , font=("times new roman", 12, "bold"), state="readonly")
        course_combo['values'] = ("Chọn môn học", "Hoc May", "Quan tri mang may tinh", "Phan tich du lieu lon","internet of things")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # Học kì
        semester_label = Label(current_course_frame, text="Học kỳ:", font=("times new roman", 12, "bold"), bg="white")
        semester_label.grid(row=1, column=2, pady=10,sticky=W)

        semester_combo = ttk.Combobox(current_course_frame,textvariable=self.var_HocKy, font=("times new roman", 12, "bold"), state="readonly")
        semester_combo['values'] = ("Chọn học kỳ", "HK1", "HK2", "HK3")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        # Thông tin sinh viên

        class_student_frame = LabelFrame(self.left_frame, bd=2, bg="white", relief=RIDGE, text="Nhận diện",
                                          font=("times new roman", 12, "bold"))
        class_student_frame.place(x=3, y=160, width=590, height=350)

        self.class_video = Label(class_student_frame)
        self.class_video.place(x=0, y=0, width=580, height=340)
        # video
        self.class_video1= Label(self.class_video)
        self.class_video1.pack()

        # Thông tin sinh viên

        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=3, y=280, width=580, height=35)

        # nút bắt đầu nhận Diện
        start_face_btn = Button(btn_frame1, text="Nhận diện",command=self.video, width=35, font=("times new roman", 12, "bold"),
                          bg="blue", fg="white")
        start_face_btn.grid(row=0, column=0)

        # nút lưu
        end_face_btn = Button(btn_frame1, text="Kết thúc nhận diện",command=self.end,width=35, font=("times new roman", 12, "bold"),
                                bg="blue", fg="white")
        end_face_btn.grid(row=0, column=1)
        # _btn = Button(btn_frame1, text="Kết thúc nhận diện", command=self.add_data, width=35,
        #                       font=("times new roman", 12, "bold"),
        #                       bg="blue", fg="white")
        # end_face_btn.grid(row=0, column=2)
        # end_face_btn = Button(btn_frame1, text="Kết thúc nhận diện", command=self.add_data, width=35,
        #                       font=("times new roman", 12, "bold"),
        #                       bg="blue", fg="white")
        # end_face_btn.grid(row=0, column=3

        # bảng bên phải
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Báo cáo",
                                font=("times new roman", 12, "bold"))
        right_frame.place(x=620, y=4, width=610, height=580)

        #hệ thống tìm kiếm
        seach_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Tìm kiếm",
                                 font=("times new roman", 12, "bold"))
        seach_frame.place(x=625, y=30, width=600, height=80)

        # seach_label = Label(seach_frame, text="Tìm kiếm", width=15, font=("times new roman", 15, "bold"),
        #                    bg="red", fg="white")
        # seach_label.grid(row=0, column=0)

        seach_combo = ttk.Combobox(seach_frame, font=("times new roman", 12, "bold"), state="readonly")
        seach_combo['values'] = ("Chọn năm học", "hkjll", "cuskk")
        seach_combo.current(0)
        seach_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        seach_btn = Button(seach_frame, text="Tìm kiếm", width=10, font=("times new roman", 12, "bold"),
                                bg="blue", fg="white")

        seach_entry = ttk.Entry(seach_frame, width=20, font=("times new roman", 12, "bold"))
        seach_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        seach_btn.grid(row=0, column=3, padx=5, pady=5, sticky=W)

        showAll_btn = Button(seach_frame, text="Tất cả", width=10, font=("times new roman", 12, "bold"),
                           bg="blue", fg="white")
        showAll_btn.grid(row=0, column=4, padx=5, pady=5, sticky=W)

        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=90, width=600, height=400)
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
        self.student_table=ttk.Treeview(table_frame,column=("MaMH","MonHoc","NamHoc","HocKy","MaSV"
                                                            ,"HoTen","Lop","GioiTinh","NgaySinh","ThamGia"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        btn_frame = Frame(self.left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=500, width=715, height=35)

        save_btn = Button(btn_frame, text="Import csv", command=self.importCsv, width=29,
                          font=("time new roman", 13, "bold"), bg="blue",
                          fg="white")
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Export csv", command=self.exportCsv, width=29,
                            font=("time new roman", 13, "bold"), bg="blue",
                            fg="white")
        update_btn.grid(row=0, column=1)

        # bảng bên phải
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Danh sách báo cáo",
                                 font=("times new roman", 12, "bold"))
        right_frame.place(x=620, y=4, width=610, height=580)
        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=5, width=595, height=520)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(table_frame,
                                                  column=(
                                                  "id", "name", "department","MonHoc", "NamHoc","HocKy", "time", "date", "attendance","tile"),
                                                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id", text="MaSV")
        self.AttendanceReportTable.heading("name", text="Tên Sinh Viên")
        self.AttendanceReportTable.heading("department", text="Mã môn học")
        self.AttendanceReportTable.heading("MonHoc", text="Môn học")
        self.AttendanceReportTable.heading("NamHoc", text="Năm học")
        self.AttendanceReportTable.heading("HocKy", text="Học kỳ")
        self.AttendanceReportTable.heading("time", text="Thời Gian")
        self.AttendanceReportTable.heading("date", text="Ngày")
        self.AttendanceReportTable.heading("attendance", text="Tham dự")
        self.AttendanceReportTable.heading("tile", text="Tỉ lệ")

        self.AttendanceReportTable["show"] = "headings"
        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("department", width=100)
        self.AttendanceReportTable.column("MonHoc", width=100)
        self.AttendanceReportTable.column("NamHoc", width=100)
        self.AttendanceReportTable.column("HocKy", width=100)
        self.AttendanceReportTable.column("time", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)
        self.AttendanceReportTable.column("tile", width=100)

        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)

    def fetchData(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("", END, values=i)

    def fetch_data(self):
        conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                       database="face")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from report")
        data= my_cursor.fetchall()
        if len(data)!=0:
            self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
            for i in data:

                self.AttendanceReportTable.insert("",END, values=i)

            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        cursor_focus=self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(cursor_focus)
        data=content["values"]
        # self.var_MaMH.set(data[2])
        # self.var_MonHoc.set(data[1])
        # self.var_NamHoc.set(data[2])
        # self.var_HocKy.set(data[3])
        # print(data[0])
        # self.var_maSV.set(data[0])
        # self.var_HoTen.set(data[1])
        # self.var_Lop.set(data[6])
        # self.var_GioiTinh.set(data[7])



    def update_data(self):

        if self.var_MaMH.get() == "Chọn mã môn học" or self.var_HoTen.get() == "" or self.var_maSV.get() == "":
            messagebox.showerror("Error", "Tất cả các trường là bắt buộc", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                               database="face")
                my_cursor = conn.cursor()
                Update =messagebox.askyesno("Cập nhập","Bạn có muốn cập nhập hay không?",parent=self.root)
                if Update>0:

                    my_cursor.execute("update student set MaMH=%s, MonHoc=%s, NamHoc=%s,HocKy=%s,HoTen=%s,Lop=%s,GioiTinh=%s,Email=%s,SDT=%s,DiaChi=%s,TenGV=%s,Hinh=%s where MaSV=%s",(
                                                                self.var_MaMH.get(),
                                                                self.var_MonHoc.get(),
                                                                self.var_NamHoc.get(),
                                                                self.var_HocKy.get(),

                                                                self.var_HoTen.get(),
                                                                self.var_Lop.get(),
                                                                self.var_GioiTinh.get(),

                                                                self.var_maSV.get(),))

                else:
                    if not Update:
                        return
                messagebox.showinfo("Thành Công","Cập nhập thông tin thành công",parent=self.root)
                conn.commit()
                # self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)

    #Tạo tập dữ liệu
    def generate_dataset(self):
        if self.var_MaMH.get() == "Chọn mã môn học" or self.var_HoTen.get() == "" or self.var_maSV.get() == "":
            messagebox.showerror("Error", "Tất cả các trường là bắt buộc", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                               database="face")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                myersult = my_cursor.fetchall()
                for x in myersult:

                    my_cursor.execute(
                        "update student set MaMH=%s, MonHoc=%s, NamHoc=%s,HocKy=%s,HoTen=%s,Lop=%s,GioiTinh=%s,Email=%s,SDT=%s,DiaChi=%s,TenGV=%s,Hinh=%s where MaSV=%s",
                        (
                            self.var_MaMH.get(),
                            self.var_MonHoc.get(),
                            self.var_NamHoc.get(),
                            self.var_HocKy.get(),

                            self.var_HoTen.get(),
                            self.var_Lop.get(),
                            self.var_GioiTinh.get(),
                            self.var_maSV.get()))
                    conn.commit()
                    # self.fetch_data()
                    # self.reset_data()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)

    def importCsv(self):
        global mydata
        mydata.clear()
        fln= filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),
                                        parent=self.root)
        with open(fln, encoding="utf-8") as myfile:
            csvread = csv.reader(myfile, delimiter =",")
            # headers = next(csvread)
            for i in csvread:
                i.append(self.var_MaMH.get())
                i.append(self.var_MonHoc.get())
                i.append(self.var_NamHoc.get())
                i.append(self.var_HocKy.get())
                mydata.append(i)
            self.fetchData(mydata)

    def add_data(self):

        if self.var_MaMH.get()== "Chọn mã môn học":
            messagebox.showerror("Error","Tất cả các trường là bắt buộc", parent=self.root)
        else:
            # messagebox.showinfo("Lưu thành công",)
            try:
                conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                               database="face")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "delete from report")
                for i in mydata:

                    my_cursor.execute("INSERT INTO report (MaMH, MonHoc, NamHoc, HocKy, MaSV, HoTen) "
                                                            "values(%s,%s,%s,%s,%s,%s)",(
                                                                    i[2],
                                                                    i[3],
                                                                    i[4],
                                                                    i[5],
                                                                    i[0],
                                                                    i[1]
                                      ))
                    conn.commit()
                self.fetch_data()
                conn.close()
                # messagebox.showinfo("Thành công", "Sinh viên đã được lưu thành công",parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Vì: {str(es)}",parent=self.root)
    def exportCsv(self):
        try:
            conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                           database="face")
            my_cursor = conn.cursor()
            my_cursor.execute("select * from report")
            mydata = my_cursor.fetchall()
            if len(mydata)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất ra",parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV",
                                         filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),
                                         parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Xuất dữ liệu","Xuất dữ liệu  thành công")
        except Exception as es:
            messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)
    def end(self):
        return 1
    def video(self):
        # try:
            # mydata.clear()
            self.add_data()
            # try:

            if self.var_MaMH.get() == "Chọn mã môn học":
                messagebox.showerror("Error", "Tất cả các trường là bắt buộc", parent=self.root)
            else:
                fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Cho Video",
                                                 filetypes=(("File video", "*.mp4"), ("All File", "*.*")),
                                                 parent=self.root)
                # print(fln)
                # Cai dat cac tham so can thiet
                MINSIZE = 20
                THRESHOLD = [0.6, 0.7, 0.7]
                FACTOR = 0.709
                IMAGE_SIZE = 182
                INPUT_IMAGE_SIZE = 160
                CLASSIFIER_PATH = 'D:/CuongDoAn/DoAn/Models/facemodel.pkl'
                VIDEO_PATH = fln
                FACENET_MODEL_PATH = 'D:/CuongDoAn/DoAn/Models/20180402-114759.pb'
                # Load model da train de nhan dien khuon mat - thuc chat la classifier
                with open(CLASSIFIER_PATH, 'rb') as file:
                    model, class_names = pickle.load(file)
                print("Custom Classifier, Successfully loaded")
                conn = mysql.connector.connect(host="127.0.0.1", port="3307",
                                               username="root",
                                               password="root",
                                               database="face")
                my_cursor = conn.cursor()

                with tf.Graph().as_default():
                    # Cai dat GPU neu co
                    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
                    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
                    with sess.as_default():
                        # Load model MTCNN phat hien khuon mat
                        print('Loading feature extraction model')
                        facenet.load_model(FACENET_MODEL_PATH)
                        # Lay tensor input va output
                        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                        embedding_size = embeddings.get_shape()[1]
                        # Cai dat cac mang con
                        pnet, rnet, onet = align.detect_face.create_mtcnn(sess, "align")
                        people_detected = set()
                        person_detected = collections.Counter()
                        # Lay hinh anh tu file video
                        cap = cv2.VideoCapture(VIDEO_PATH)
                        while (cap.isOpened()):
                            # Doc tung frame
                            ret, frame = cap.read()
                            frame = imutils.resize(frame, width=1300, height=700)
                            frame = cv2.flip(frame, 1)
                            # player = tkvideo(r"D:\CuongDoAn\DoAn\video\test1.mp4", self.class_video1, loop=1,
                            #                  size=(450, 300))
                            # player.play()
                            # Phat hien khuon mat, tra ve vi tri trong bounding_boxes
                            bounding_boxes, _ = align.detect_face.detect_face(frame, MINSIZE, pnet, rnet, onet,
                                                                              THRESHOLD,
                                                                              FACTOR)
                            faces_found = bounding_boxes.shape[0]
                            try:
                            # Neu co it nhat 1 khuon mat trong frame
                                if faces_found > 0:
                                    det = bounding_boxes[:, 0:4]
                                    bb = np.zeros((faces_found, 4), dtype=np.int32)
                                    for i in range(faces_found):
                                        bb[i][0] = det[i][0]
                                        bb[i][1] = det[i][1]
                                        bb[i][2] = det[i][2]
                                        bb[i][3] = det[i][3]
                                        # Cat phan khuon mat tim duoc
                                        cropped = frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :]
                                        scaled = cv2.resize(cropped, (INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE),
                                                            interpolation=cv2.INTER_CUBIC)
                                        scaled = facenet.prewhiten(scaled)
                                        scaled_reshape = scaled.reshape(-1, INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE, 3)
                                        feed_dict = {images_placeholder: scaled_reshape, phase_train_placeholder: False}
                                        emb_array = sess.run(embeddings, feed_dict=feed_dict)
                                        # Dua vao model de classifier
                                        predictions = model.predict_proba(emb_array)
                                        best_class_indices = np.argmax(predictions, axis=1)
                                        best_class_probabilities = predictions[
                                            np.arange(len(best_class_indices)), best_class_indices]
                                        # Lay ra ten va ty le % cua class co ty le cao nhat
                                        best_name = class_names[best_class_indices[0]]
                                        print("Name: {}, Probability: {}".format(best_name, best_class_probabilities))
                                        # Ve khung mau xanh quanh khuon mat
                                        cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)
                                        text_x = bb[i][0]
                                        text_y = bb[i][3] + 20
                                        # Neu ty le nhan dang > 0.5 thi hien thi ten
                                        if best_class_probabilities > 0.6:
                                            # my_cursor.execute(
                                            #     "select HoTen from student where HoTen like '" + str(best_name) + "'")
                                            # n =my_cursor.fetchone()
                                            # n = "+".join(n)
                                            # print(n)
                                            my_cursor.execute(
                                                "select MaSV from student where HoTen like '" + str(best_name) + "'")
                                            m = my_cursor.fetchone()
                                            m = "+".join(m)  
                                            print(m)
                                            now = datetime.now()
                                            d1 = now.strftime("%d/%m/%Y")
                                            dtString = now.strftime("%H:%M:%S")
                                            name = class_names[best_class_indices[0]]
                                            if self.var_MaMH.get() == "Chọn mã môn học":
                                                messagebox.showerror("Error", "Tất cả các trường là bắt buộc")
                                            else:
                                                # messagebox.showinfo("Lưu thành công",)

                                                my_cursor.execute(
                                                    "update report set Gio=%s,Ngay=%s,ThamGia=%s,TiLe=%s where MaSV=%s", (
                                                        dtString,
                                                        d1,
                                                        "Co",
                                                        str(best_class_probabilities[0]),
                                                        str(m)
                                                    )


                                                )
                                                # print(str(m))

                                                conn.commit()
                                                self.fetch_data()

                                                # messagebox.showinfo("Thành công", "Sinh viên đã được lưu thành công")

                                        else:
                                            # Con neu <=0.5 thi hien thi Unknow
                                            name = "Nguoi la"
                                        # Viet text len tren frame
                                        cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                    1, (255, 255, 255), thickness=1, lineType=2)
                                        cv2.putText(frame, str(round(best_class_probabilities[0], 3)),
                                                    (text_x, text_y + 17),
                                                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                    1, (255, 255, 255), thickness=1, lineType=2)
                                        person_detected[best_name] += 1
                                cv2.imshow('Nhan Dien', frame)
                                if cv2.waitKey(1) & 0xFF == ord('q') or self.end == 1:
                                    break
                            except:
                                pass
                            # Hien thi frame len man hinh


                    cap.release()
                    cv2.destroyAllWindows()
                conn.close()

                messagebox.showinfo("Thành công", "Nhận diện thành công!!")
            # except Exception as es:
            #     pass
        # except Exception as es:
        #     messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)
if __name__=="__main__":
    root = Tk()
    obj = Video(root)
    root.mainloop()