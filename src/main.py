import tkinter.messagebox
from tkinter import *
from PIL import  Image,ImageTk
from student import Student
import os
import csv
from tkinter import filedialog
import subprocess
from  tkinter import  messagebox
from attendance import  Attandance
from GDvideo import Video
from tkinter.messagebox import showinfo
class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1250x650+0+0")
        self.root.title("Hệ thống nhận điểm danh nhận diện khuôn mặt")

        img = Image.open(r"D:\CuongDoAn\DoAn\image\hinh giao dien.jpg")
        img = img.resize((1250,650), Image.ANTIALIAS)
        self.photoimg= ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0,y=0,width = 1250, height=650)

        title_lbl =Label(f_lbl,text="Hệ thống điểm danh bằng nhận diện khuôn mặt", font=("time new roman",30,"bold"), bg="white", fg="red")
        title_lbl.place(x=0,y=0, width = 1250, height=45)

        # Nút quản lý sinh viên
        img1 = Image.open(r"D:\CuongDoAn\DoAn\image/thong_tinsv.jpg")
        img1 = img1.resize((220, 220), Image.ANTIALIAS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        # Hiện thị hình + nút
        b1 = Button(f_lbl, image=self.photoimg1, command=self.student_details,cursor="hand2")
        b1.place(x=50,y=350, width=220,height=220)
        # Hiện thị chữ trên nút
        b1_1 =Button(f_lbl,text="Chi tiết sinh viên", command=self.student_details,cursor="hand2",font=("time new roman",15,"bold"), bg="darkblue", fg="white")
        b1_1.place(x=50,y=550,width=220, height=40)

        # Nút
        img2 = Image.open(r"D:\CuongDoAn\DoAn\image\nhan-dien-khuon-mat-khong.jpg")
        img2 = img2.resize((220, 220), Image.ANTIALIAS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        # Hiện thị hình + nút
        b1 = Button(f_lbl, image=self.photoimg2, cursor="hand2",command=self.face)
        b1.place(x=350, y=100, width=220, height=220)
        # Hiện thị chữ trên nút
        b1_1 = Button(f_lbl, text="Nhận diện bằng camera",command=self.face, cursor="hand2", font=("time new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=350, y=300, width=220, height=40)

        # Nút thống kê có mặt

        img3 = Image.open(r"D:\CuongDoAn\DoAn\image\\OIP.jpg")
        img3 = img3.resize((220, 220), Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        # Hiện thị hình + nút
        b1 = Button(f_lbl, image=self.photoimg3, cursor="hand2", command=self.thongKe)
        b1.place(x=480, y=350, width=220, height=220)
        # Hiện thị chữ trên nút
        b1_1 = Button(f_lbl, text="Thống kê", cursor="hand2",command=self.thongKe, font=("time new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=480, y=550, width=220, height=40)

        # Nút hỗ trợ
        # img4 = Image.open(r"image\\help.png")
        # img4 = img4.resize((220, 220), Image.ANTIALIAS)
        # self.photoimg4 = ImageTk.PhotoImage(img4)
        # Hiện thị hình + nút
        # b1 = Button(f_lbl, image=self.photoimg4, cursor="hand2")
        # b1.place(x=950, y=100, width=220, height=220)
        # # Hiện thị chữ trên nút
        # b1_1 = Button(f_lbl, text="Hỗ trợ", cursor="hand2", font=("time new roman", 15, "bold"),
        #               bg="darkblue", fg="white")
        # b1_1.place(x=950, y=300, width=220, height=40)

        # # Nút huấn luyện
        # img5 = Image.open(r"image/trainning.png")
        # img5 = img5.resize((220, 220), Image.ANTIALIAS)
        # self.photoimg5 = ImageTk.PhotoImage(img5)
        # # Hiện thị hình + nút
        # b1 = Button(f_lbl, image=self.photoimg5, cursor="hand2", command=self.train)
        # b1.place(x=50, y=350, width=220, height=220)
        # # Hiện thị chữ trên nút
        # b1_1 = Button(f_lbl, text="Huấn luyện",command=self.train, cursor="hand2", font=("time new roman", 15, "bold"),
        #               bg="darkblue", fg="white")
        # b1_1.place(x=50, y=550, width=220, height=40)

        # # Toàn bộ hình ảnh
        # img6 = Image.open(r"image/sv.jpg")
        # img6 = img6.resize((220, 220), Image.ANTIALIAS)
        # self.photoimg6 = ImageTk.PhotoImage(img6)
        # # Hiện thị hình + nút
        # b1 = Button(f_lbl, image=self.photoimg6, cursor="hand2", command=self.open_img,)
        # b1.place(x=350, y=350, width=220, height=220)
        # # Hiện thị chữ trên nút
        # b1_1 = Button(f_lbl, text="Hình ảnh",command=self.open_img, cursor="hand2", font=("time new roman", 15, "bold"),
        #               bg="darkblue", fg="white")
        # b1_1.place(x=350, y=550, width=220, height=40)

        # Nhận diện bằng video
        img7 = Image.open(r"D:\CuongDoAn\DoAn\image/video.jpg")
        img7 = img7.resize((220, 220), Image.ANTIALIAS)
        self.photoimg7 = ImageTk.PhotoImage(img7)
        # Hiện thị hình + nút
        b1 = Button(f_lbl, image=self.photoimg7, cursor="hand2",command=self.video)
        b1.place(x=650, y=100, width=220, height=220)
        # Hiện thị chữ trên nút
        b1_1 = Button(f_lbl, text="Nhận diện bằng video", cursor="hand2", command=self.video, font=("time new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=650, y=300, width=220, height=40)

        # Thoát chương trình
        img8 = Image.open(r"D:\CuongDoAn\DoAn\image/ex.jpg")
        img8 = img8.resize((220, 220), Image.ANTIALIAS)
        self.photoimg8 = ImageTk.PhotoImage(img8)
        # Hiện thị hình + nút
        b1 = Button(f_lbl, image=self.photoimg8, cursor="hand2", command=self.exit)
        b1.place(x=950, y=350, width=220, height=220)
        # Hiện thị chữ trên nút
        b1_1 = Button(f_lbl, text="Thoát", cursor="hand2", font=("time new roman", 15, "bold"), command=self.exit,
                      bg="darkblue", fg="white")
        b1_1.place(x=950, y=550, width=220, height=40)
    def student_details(self):#Chuyển hướng quản ly sinh viên
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)
    def open_img(self):
        global mydata
        os.startfile("video")
        # mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Cho Video",
                                         filetypes=(("File video", "*.mp4"), ("All File", "*.*")),
                                         parent=self.root)

        showinfo(
            title='Selected File',
            message=fln
        )
        # with open(fln, encoding="utf-8") as myfile:
        #     csvread = csv.reader(myfile, delimiter=",")
        #     # headers = next(csvread)
        #     for i in csvread:
        #         mydata.append(i)
        #     self.fetchData(mydata)
        # os.startfile("Dataset")
    def train(self):
        try:
            messagebox.showinfo("Huấn luyện", "Bấm OK để tiến hành thực hiện. Bộ dữ liệu đang được huấn luyện vui lòng chờ!! ")
            argv = ['python',
                    'src/classifier.py',
                    'TRAIN',
                    'Dataset/FaceData/processed',
                    'Models/20180402-114759.pb',
                    'Models/facemodel.pkl',
                    '--batch_size', '1000']
            subprocess.call(argv)
            messagebox.showinfo("Thành công", "Huấn luyện thành công!!")
        except Exception as es:
            messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)
    def face(self):
        try:
            Toplevel(self.root)
            # messagebox.showinfo("Hướng dẫn", "Bấm 'q' để kết thúc.")
            argv = ['python',
                    'face_rec_cam.py']
            subprocess.call(argv)
            messagebox.showinfo("Thành công", "Nhận diện thành công!!")
        except Exception as es:
            messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)
    def video(self):
        # try:
        #     # mydata.clear()
        #     fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Cho Video",
        #                                      filetypes=(("File video", "*.mp4"), ("All File", "*.*")),
        #                                      parent=self.root)
        #     # showinfo(
        #     #     title='Selected File',
        #     #     message=fln
        #     # )
        #     try:
        #         # self.new_window = Toplevel(self.root)
        #         # messagebox.showinfo("Hướng dẫn", "Bấm 'q' để kết thúc.")
        #         argv = ['python',
        #                 'src/face_rec.py',
        #                 '--path',
        #                 fln]
        #         subprocess.call(argv)
        #         messagebox.showinfo("Thành công", "Nhận diện thành công!!")
        #     except Exception as es:
        #         pass
        # except Exception as es:
        #     messagebox.showerror("Error", f"Vì: {str(es)}", parent=self.root)
        self.new_window = Toplevel(self.root)
        self.app = Video(self.new_window)

    def thongKe(self):

        self.new_window = Toplevel(self.root)
        self.app = Attandance(self.new_window)

    def exit(self):
        self.exit=tkinter.messagebox.askyesno("Nhận diện khuôn mặt","Bạn có muốn thoát chương trình không?",parent=self.root)
        if self.exit>0:
            self.root.destroy()
        else:
            return
    # def time():
    #     string = strftime("%H:%M:%S %p")
    #     lbl.confi
if __name__=="__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()