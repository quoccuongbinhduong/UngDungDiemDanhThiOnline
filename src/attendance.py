from tkinter import *
from tkinter import ttk
import cv2
import  os
import  csv
from PIL import Image, ImageTk
from  tkinter import  messagebox
import mysql.connector
from tkinter import filedialog
mydata=[]


class Attandance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x650+0+0")
        self.root.title("Báo cáo điểm danh")
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

        # hinh 1

        img = Image.open(r"D:\CuongDoAn\DoAn\image\hinh giao dien.jpg")
        img = img.resize((1250, 650), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=1250, height=650)

        title_lbl = Label(f_lbl, text="Báo cáo điểm danh",
                          font=("time new roman", 30, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1250, height=45)

        main_frame = Frame(f_lbl, bd=2, bg="white")
        main_frame.place(x=2, y=50, width=1240, height=590)

        # bảng bên trái
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Quản lý báo cáo",
                                font=("times new roman", 12, "bold"))
        left_frame.place(x=4, y=4, width=610, height=580)

        # Thông tin sinh viên
        class_student_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin sinh viên",
                                         font=("times new roman", 12, "bold"))
        class_student_frame.place(x=4, y=160, width=600, height=350)
        # Thông tin sinh viên
        studentId_label = Label(class_student_frame, text="Mã số SV:", font=("times new roman", 12, "bold"), bg="white")
        studentId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        studentId_entry = ttk.Entry(class_student_frame, width=20,
                                    font=("times new roman", 12, "bold"),textvariable=self.var_maSV)
        studentId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)
        # Họ và tên sinh viên
        studentName_label = Label(class_student_frame, text="Họ tên:", font=("times new roman", 12, "bold"), bg="white")
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        studentName_entry = ttk.Entry(class_student_frame,  width=20,textvariable=self.var_HoTen,
                                      font=("times new roman", 12, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Lớp
        # Class_label = Label(class_student_frame, text="Mã môn học:", font=("times new roman", 12, "bold"), bg="white")
        # Class_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        # Class_entry = ttk.Entry(class_student_frame,  width=20,textvariable=self.var_MaMH,
        #                         font=("times new roman", 12, "bold"))
        # Class_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # # Tên giáo viên
        # teacher_label = Label(class_student_frame, text="Tên giáo viên:", font=("times new roman", 12, "bold"),
        #                       bg="white")
        # teacher_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        # teacher_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_teacher,
        #                           font=("times new roman", 12, "bold"))
        # teacher_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # # Tên giáo viên
        # teacher_label = Label(class_student_frame, text="Tên giáo viên:", font=("times new roman", 12, "bold"),
        #                       bg="white")
        # teacher_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        # teacher_entry = ttk.Entry(class_student_frame, width=20,
        #                           font=("times new roman", 12, "bold"))
        # teacher_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # #Thời gian
        # time_label = Label(class_student_frame, text="Thời gian:", font=("times new roman", 12, "bold"),
        #                       bg="white")
        # time_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        # time_entry = ttk.Entry(class_student_frame, width=20 ,textvariable=self.var_time,
        #                           font=("times new roman", 12, "bold"))
        # time_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Ngày
        # date_label = Label(class_student_frame, text="Ngày:", font=("times new roman", 12, "bold"),
        #                    bg="white")
        # date_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        # date_entry = ttk.Entry(class_student_frame, width=20 ,textvariable=self.var_date,
        #                        font=("times new roman", 12, "bold"))
        # date_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        Gender_label = Label(class_student_frame, text="Tham dự:", font=("times new roman", 12, "bold"), bg="white")
        Gender_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        Gender_combo = ttk.Combobox(class_student_frame, width=10,textvariable=self.var_ThamGia,
                                    font=("times new roman", 12, "bold"), state="readonly")
        Gender_combo['values'] = ("Co", "Khong", "Bo tiet")
        Gender_combo.current(0)
        Gender_combo.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # button frame
        btn_frame = Frame(left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=500, width=715, height=35)

        save_btn = Button(btn_frame, text="Import csv",command= self.importCsv, width=14, font=("time new roman", 13, "bold"), bg="blue",
                          fg="white")
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Export csv",command=self.exportCsv, width=14, font=("time new roman", 13, "bold"), bg="blue",
                            fg="white")
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Delete", width=14, font=("time new roman", 13, "bold"), bg="blue",
                            fg="white")
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Làm mới", width=14, command=self.reset_data(), font=("time new roman", 13, "bold"), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3)

        # bảng bên phải
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Danh sách báo cáo",
                                 font=("times new roman", 12, "bold"))
        right_frame.place(x=620, y=4, width=610, height=580)
        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=5, width=595, height=520)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable =  ttk.Treeview(table_frame,
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
        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)
    def fetchData(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END,values=i)
    def importCsv(self):
        global mydata
        mydata.clear()
        fln= filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),
                                        parent=self.root)
        with open(fln, encoding="utf-8") as myfile:
            csvread = csv.reader(myfile, delimiter =",")
            # headers = next(csvread)
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)
    def exportCsv(self):
        # try:
            if len(mydata)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất ra",parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV",
                                         filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),
                                         parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    print(i)
                    exp_write.writerow(i)
                messagebox.showinfo("Xuất dữ liệu","Xuất dữ liệu  thành công")
        # except Exception as es:
        #     messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)
    def get_cursor(self, event=""):
        curses_row= self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(curses_row)
        row=content["values"]
        self.var_maSV.set(row[0])
        self.var_HoTen.set(row[1])
        # self.var_department.set(row[2])
        # self.var_teacher.set(row[3])

        self.var_ThamGia.set(row[8])

    def reset_data(self):

        self.var_maSV.set("")
        self.var_HoTen.set("")
        # self.var_department.set("")
        # self.var_teacher.set("")
        # self.var_time.set("")
        # self.var_date.set("")
        self.var_ThamGia.set("")

if __name__ == '__main__':
    root = Tk()
    obj = Attandance(root)
    root.mainloop()
