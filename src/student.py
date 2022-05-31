from tkinter import *
from tkinter import ttk

import cv2
from PIL import Image, ImageTk
from  tkinter import  messagebox
import mysql.connector


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x650+0+0")
        self.root.title("Hệ thống nhận điểm danh nhận diện khuôn mặt")

        self.var_maSV = StringVar()
        self.var_HoTen = StringVar()
        self.var_Lop = StringVar()
        self.var_GioiTinh = StringVar()
        self.var_Email = StringVar()
        self.var_SDT = StringVar()
        self.var_DiaChi = StringVar()
        self.var_NgaySinh = StringVar()
        img = Image.open(r"D:\CuongDoAn\DoAn\image\hinh giao dien.jpg")
        img = img.resize((1250, 650), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=1250, height=650)

        title_lbl = Label(f_lbl, text="Chi tiết thông tin sinh viên",
                          font=("time new roman", 30, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1250, height=45)
        main_frame =Frame(f_lbl, bd=2, bg="white")
        main_frame.place(x=2,y=50, width=1240, height=590)

        # bảng bên trái
        left_frame =LabelFrame(main_frame, bd=2,bg="white", relief=RIDGE, text="Thông tin sinh viên",font=("times new roman",12,"bold"))
        left_frame.place(x=4,y= 4, width=600, height=580)

        # left_img = Image.open(r"image\hinh giao dien.jpg")
        # left_img = left_img.resize((600, 580), Image.ANTIALIAS)
        # self.photoleft_img = ImageTk.PhotoImage(left_img)
        # left_imgBR = Label(self.root, image=self.photoleft_img)
        # left_imgBR.place(x=18, y=80, width=585, height=550)

        # # Khóa học
        # current_course_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin môn học",
        #                         font=("times new roman", 12, "bold"))
        # current_course_frame.place(x=4, y=4, width=590, height=150)
        # dep_label=Label(current_course_frame, text="Mã môn học:",font=("times new roman",12,"bold"),bg="white")
        # dep_label.grid(row=0, column=0,pady=10)

        # dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_MaMH,font=("times new roman",12,"bold"),state="readonly")
        # dep_combo['values']=("Chọn mã môn học","HM123", "PTUDDD123")
        # dep_combo.current(0)
        # dep_combo.grid(row=0,column=1,padx=2,pady=10, sticky=W)
        #
        # #năm học
        # year_label = Label(current_course_frame, text="Năm học:", font=("times new roman", 12, "bold"), bg="white")
        # year_label.grid(row=1, column=0, pady=10,sticky=W)
        #
        # year_combo = ttk.Combobox(current_course_frame,textvariable=self.var_NamHoc, font=("times new roman", 12, "bold"), state="readonly")
        # year_combo['values'] = ("Chọn năm học", "2021-2022", "2022-2023")
        # year_combo.current(0)
        # year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        #Khóa học
        # course_label = Label(current_course_frame, text="Môn học:", font=("times new roman", 12, "bold"), bg="white")
        # course_label.grid(row=0, column=2, pady=10)
        #
        # course_combo = ttk.Combobox(current_course_frame,textvariable=self.var_MonHoc , font=("times new roman", 12, "bold"), state="readonly")
        # course_combo['values'] = ("Chọn môn học", "Học máy", "Phát triển ứng dụng duy động")
        # course_combo.current(0)
        # course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)
        #
        # # Học kì
        # semester_label = Label(current_course_frame, text="Học kỳ:", font=("times new roman", 12, "bold"), bg="white")
        # semester_label.grid(row=1, column=2, pady=10,sticky=W)
        #
        # semester_combo = ttk.Combobox(current_course_frame,textvariable=self.var_HocKy, font=("times new roman", 12, "bold"), state="readonly")
        # semester_combo['values'] = ("Chọn học kỳ", "HK1", "HK2", "HK3")
        # semester_combo.current(0)
        # semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        # Thông tin sinh viên
        class_student_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin sinh viên",
                                          font=("times new roman", 12, "bold"))
        class_student_frame.place(x=4, y=160, width=590, height=350)
        # Thông tin sinh viên
        studentId_label = Label(class_student_frame, text="Mã số SV:", font=("times new roman", 12, "bold"), bg="white")
        studentId_label.grid(row=0, column=0,padx =10, pady=5, sticky=W)
        studentId_entry =ttk.Entry(class_student_frame,textvariable=self.var_maSV,width = 20, font=("times new roman", 12, "bold"))
        studentId_entry.grid(row=0, column=1,padx =10, pady=5, sticky=W)
        # Họ và tên sinh viên
        studentName_label = Label(class_student_frame, text="Họ tên:", font=("times new roman", 12, "bold"), bg="white")
        studentName_label.grid(row=0, column=2,padx =10, pady=5, sticky=W)
        studentName_entry = ttk.Entry(class_student_frame,textvariable=self.var_HoTen, width=20, font=("times new roman", 12, "bold"))
        studentName_entry.grid(row=0, column=3,padx =10, pady=5, sticky=W)

        # Lớp
        Class_label = Label(class_student_frame, text="Lớp:", font=("times new roman", 12, "bold"), bg="white")
        Class_label.grid(row=1, column=0,padx =10, pady=5, sticky=W)
        Class_entry = ttk.Entry(class_student_frame,textvariable=self.var_Lop, width=20, font=("times new roman", 12, "bold"))
        Class_entry.grid(row=1, column=1,padx =10, pady=5, sticky=W)

        # Giới tính
        Gender_label = Label(class_student_frame, text="Giới tính:", font=("times new roman", 12, "bold"), bg="white")
        Gender_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        Gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_GioiTinh,width=10,
                                      font=("times new roman", 12, "bold"), state="readonly")
        Gender_combo['values'] = ("Nam", "Nu", "Khac")
        Gender_combo.current(0)
        Gender_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Email
        Email_label = Label(class_student_frame, text="Email:", font=("times new roman", 12, "bold"),
                                    bg="white")
        Email_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        Email_entry = ttk.Entry(class_student_frame,textvariable=self.var_Email, width=20, font=("times new roman", 12, "bold"))
        Email_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Số điện thoại
        Phone_label = Label(class_student_frame, text="Số điện thoại:", font=("times new roman", 12, "bold"),
                                   bg="white")
        Phone_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        Phone_entry = ttk.Entry(class_student_frame,textvariable=self.var_SDT, width=20, font=("times new roman", 12, "bold"))
        Phone_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Địa chỉ
        Address_label = Label(class_student_frame, text="Địa chỉ:", font=("times new roman", 12, "bold"),
                                   bg="white")
        Address_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        Address_entry = ttk.Entry(class_student_frame,textvariable=self.var_DiaChi, width=20, font=("times new roman", 12, "bold"))
        Address_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Tên giáo viên
        teacher_label = Label(class_student_frame, text="Ngày sinh:", font=("times new roman", 12, "bold"),
                                   bg="white")
        teacher_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        teacher_entry = ttk.Entry(class_student_frame,textvariable=self.var_NgaySinh, width=20, font=("times new roman", 12, "bold"))
        teacher_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # self.var_radio1=StringVar()
        # radiobtn1=ttk.Radiobutton(class_student_frame, variable=self.var_radio1,text="Lấy mẫu ảnh.", value="Yes")
        # radiobtn1.grid(row=4,column=0)
        #
        # radiobtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="Không lấy mẫu ảnh.", value="No")
        # radiobtn2.grid(row=4, column=1)

        #Khung các nút
        btn_frame =Frame(class_student_frame,bd=2, relief=RIDGE,bg="white")
        btn_frame.place(x=3, y=180,width=580, height=130)

        #nút lưu
        save_btn=Button(btn_frame,command=self.add_data,text="Lưu",width=15,font=("times new roman", 12, "bold"),
                                   bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        # Nút cập nhập
        update_btn = Button(btn_frame,command=self.update_data, text="Cập nhập", width=15, font=("times new roman", 12, "bold"),
                          bg="blue", fg="white")
        update_btn.grid(row=0, column=1)

        # nút xóa
        delete_btn = Button(btn_frame, text="Xóa",command=self.delete_data, width=15, font=("times new roman", 12, "bold"),
                          bg="blue", fg="white")
        delete_btn.grid(row=0, column=2)

        # nút cài lại
        reset_btn = Button(btn_frame, text="Cài lại", command=self.reset_data, width=15, font=("times new roman", 12, "bold"),
                          bg="blue", fg="white")
        reset_btn.grid(row=0, column=3)

        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=3, y=250, width=580, height=35)

        # nút lưu
        take_photo_btn = Button(btn_frame1, text="Thu thập hình",command=self.generate_dataset, width=35, font=("times new roman", 12, "bold"),
                          bg="blue", fg="white")
        take_photo_btn.grid(row=0, column=0)

        # nút lưu
        update_photo_btn = Button(btn_frame1, text="Cập nhập lại hình", width=35, font=("times new roman", 12, "bold"),
                                bg="blue", fg="white")
        update_photo_btn.grid(row=0, column=1)

        # bảng bên phải
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin sinh viên",
                                font=("times new roman", 12, "bold"))
        right_frame.place(x=620, y=4, width=610, height=580)

        #hệ thống tìm kiếm
        seach_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Tìm kiếm",
                                 font=("times new roman", 12, "bold"))
        seach_frame.place(x=625, y=30, width=600, height=80)

        # seach_label = Label(seach_frame, text="Tìm kiếm", width=15, font=("times new roman", 15, "bold"),
        #                    bg="red", fg="white")
        # seach_label.grid(row=0, column=0)

        # seach_combo = ttk.Combobox(seach_frame, font=("times new roman", 12, "bold"), state="readonly")
        # seach_combo['values'] = ("Chọn mã sinh viên", "1824801040009", "cuskk")
        # seach_combo.current(0)
        # seach_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
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
        self.student_table=ttk.Treeview(table_frame,column=("MaSV","HoTen", "NgaySinh","GioiTinh","Lop","Email","SDT","DiaChi"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        self.student_table.heading("MaSV", text="Mã sinh viên")
        self.student_table.heading("HoTen", text="Họ tên sinh viên")
        self.student_table.heading("Lop", text="Mã Lớp")
        self.student_table.heading("GioiTinh", text="Giới tính")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("SDT", text="Số điện thoại")
        self.student_table.heading("DiaChi", text="Địa chỉ")
        self.student_table.heading("NgaySinh", text="Ngày sinh")

        self.student_table["show"]="headings"
        self.student_table.column("MaSV", width=100)
        self.student_table.column("HoTen", width=100)
        self.student_table.column("Lop", width=100)
        self.student_table.column("GioiTinh", width=100)
        self.student_table.column("Email", width=100)
        self.student_table.column("SDT", width=100)
        self.student_table.column("DiaChi", width=100)
        self.student_table.column("NgaySinh", width=100)
        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

    def add_data(self):
        if self.var_HoTen.get() == "" or self.var_maSV.get() == "":
            messagebox.showerror("Error","Tất cả các trường là bắt buộc", parent=self.root)
        else:
            # messagebox.showinfo("Lưu thành công",)
            try:

                conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                               database="face")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s)",(

                                                                self.var_maSV.get(),
                                                                self.var_HoTen.get(),
                                                                self.var_NgaySinh.get(),
                                                                self.var_GioiTinh.get(),
                                                                self.var_Lop.get(),
                                                                self.var_Email.get(),
                                                                self.var_SDT.get(),
                                                                self.var_DiaChi.get(),
                                  ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Thành công", "Sinh viên đã được lưu thành công",parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Vì: {str(es)}",parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                       database="face")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data= my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END, values=i)
            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        self.var_maSV.set(data[0])
        self.var_HoTen.set(data[1])
        self.var_Lop.set(data[4])
        self.var_GioiTinh.set(data[3])
        self.var_Email.set(data[5])
        self.var_SDT.set(data[6])
        self.var_DiaChi.set(data[7])
        self.var_NgaySinh.set(data[2])
    def update_data(self):

        if self.var_HoTen.get() == "" or self.var_maSV.get() == "":
            messagebox.showerror("Error", "Tất cả các trường là bắt buộc", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                               database="face")
                my_cursor = conn.cursor()
                Update =messagebox.askyesno("Cập nhập","Bạn có muốn cập nhập hay không?",parent=self.root)
                if Update>0:

                    my_cursor.execute("update student set HocKy=%s,HoTen=%s,Lop=%s,GioiTinh=%s,Email=%s,SDT=%s,DiaChi=%s,NgaySinh=%s where MaSV=%s",(

                                                                self.var_HoTen.get(),
                                                                self.var_Lop.get(),
                                                                self.var_GioiTinh.get(),
                                                                self.var_Email.get(),
                                                                self.var_SDT.get(),
                                                                self.var_DiaChi.get(),
                                                                self.var_NgaySinh.get(),
                                                                self.var_maSV.get(),))

                else:
                    if not Update:
                        return
                messagebox.showinfo("Thành Công","Cập nhập thông tin thành công",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_maSV.get()=="":
            messagebox.showerror("Error","Mã sinh viên không tồn tại!",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                               database="face")
                my_cursor = conn.cursor()
                detele= messagebox.askyesno("Xóa sinh viên","Bạn có muốn cóa xinh viên này không?",parent=self.root)
                if detele>0:

                    sql="delete from student where MaSV=%s"
                    val = (self.var_maSV.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not detele:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Xóa","Xóa sinh viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)

    def reset_data(self):

        self.var_maSV.set("")
        self.var_HoTen.set(""),
        self.var_Lop.set(""),
        self.var_GioiTinh.set("Nam"),
        self.var_Email.set(""),
        self.var_SDT.set(""),
        self.var_DiaChi.set(""),
        self.var_NgaySinh.set(""),

    #Tạo tập dữ liệu
    def generate_dataset(self):
        if self.var_HoTen.get() == "" or self.var_maSV.get() == "":
            messagebox.showerror("Error", "Tất cả các trường là bắt buộc", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                               database="face")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                myersult = my_cursor.fetchall()
                id=0
                for x in myersult:
                    # id+=1
                    # my_cursor.execute(
                    #     "update student set HoTen=%s,Lop=%s,GioiTinh=%s,Email=%s,SDT=%s,DiaChi=%s,NgaySinh=%s where MaSV=%s",
                    #     (
                    #         self.var_HoTen.get(),
                    #         self.var_Lop.get(),
                    #         self.var_GioiTinh.get(),
                    #         self.var_Email.get(),
                    #         self.var_SDT.get(),
                    #         self.var_DiaChi.get(),
                    #         self.var_NgaySinh.get(),
                    #         self.var_maSV.get()))
                    # conn.commit()
                    # self.fetch_data()
                    # self.reset_data()
                    # conn.close()

                    #can them cat khuôn mặt từ hình
                    face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                    def  face_cropped(img):
                        gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
                        faces = face_classifier.detectMultiScale(gray,1.3,5)
                        for (x,y,w,h) in faces:
                            face_cropped=img[y:y+h,x:x+w]
                            return face_cropped
                    cap=cv2.VideoCapture(0)
                    img_id=0
                    while True:
                        ret, my_frame =cap.read()
                        if face_cropped(my_frame) is not None:
                            img_id+=1
                            face= cv2.resize(face_cropped(my_frame),(450,450))
                            face = cv2.cvtColor(face, cv2.COLOR_BGR2HLS)
                            file_name_path ="Dataset/FaceData/raw/"+str(id)+"."+str(img_id)+".jpg"
                            cv2.imwrite((file_name_path),face)
                            cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                            cv2.imshow("Cắt khuôn mặt", face)
                        if cv2.waitKey(1)==13 or int(img_id)==20:
                            break

                    cap.release()
                    cv2.destroyAllWindows()
                    messagebox.showinfo("Thành công","Thêm thành công hình ảnh")
            except Exception as es:
                messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)


if __name__=="__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()