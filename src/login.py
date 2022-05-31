from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from main import Face_Recognition_System
def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()
class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        self.var_DangNhap = StringVar()
        self.var_MatKhau = StringVar()
        self.var_MatKhau_1 = StringVar()
        self.var_MatKhau_2 = StringVar()
        self.bg=ImageTk.PhotoImage(file=r"D:\CuongDoAn\DoAn\image\login.jpg")
        #
        # lbl_bg=Label(self.root, image=self.bg)
        # lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame=Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=450)

        img1=Image.open(r"D:\CuongDoAn\DoAn\image\iconuser.jpg")
        img1=img1.resize((100, 100), Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(self.root, image=self.photoimage1, bg="black", borderwidth=0)
        lblimg1.place(x=730, y=175, width=97, height=97)

        get_str=Label(frame, text="ĐĂNG NHẬP", font=("time new roman", 20, "bold"), fg="white", bg="black")
        get_str.place(x=95, y=100)

        #label
        username=lbl=Label(frame, text="Tên đăng nhập", font=("time new roman", 15, "bold"), fg="white", bg="black")
        username.place(x=70, y=155)

        self.txtuser=ttk.Entry(frame, font=("time new roman", 15, "bold"),textvariable=self.var_DangNhap)
        self.txtuser.place(x=40, y=180, width=270)

        password = lbl = Label(frame, text="Mật khẩu", font=("time new roman", 15, "bold"), fg="white", bg="black")
        password.place(x=70, y=225)

        self.txtpass = ttk.Entry(frame,textvariable=self.var_MatKhau, font=("time new roman", 15, "bold"))
        self.txtpass.place(x=40, y=250, width=270)

        # =============Icon Image================
        img2 = Image.open(r"D:\CuongDoAn\DoAn\image\iconuser.jpg")
        img2 = img2.resize((25, 25), Image.ANTIALIAS)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        lblimg1 = Label(image=self.photoimage2, bg="black")
        lblimg1.place(x=650, y=323, width=25, height=25)

        img3 = Image.open(r"D:\CuongDoAn\DoAn\image\iconpassword.jpg")
        img3 = img3.resize((25, 25), Image.ANTIALIAS)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        lblimg1 = Label(image=self.photoimage3, bg="black")
        lblimg1.place(x=650, y=395, width=25, height=25)

        #loginbutton
        loginbtn=Button(frame, command=self.login, text="Đăng nhập", font=("time new roman", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="red", activeforeground="white", activebackground="red" )
        loginbtn.place(x=110, y=300, width=150, height=35)

        # #registerbutton
        # registerbtn = Button(frame, text="Đăng Ký", font=("time new roman", 10, "bold"), borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
        # registerbtn.place(x=15, y=350, width=120, height=160)

        #forgetpassbtn
        registerbtn = Button(frame, text="Quên mật khẩu?",command=self.forgot_password_window, font=("time new roman", 10, "bold"), borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
        registerbtn.place(x=10, y=300, width=120, height=160)
    # def rigister_window(self):
    #     self.new_window=Toplevel(self.root)
    #     self.app=
    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error", "all field required")
        elif self.txtuser.get()=="kapu" and self.txtpass.get()=="ashu":
            messagebox.showinfo("Thành công!" "Chào mừng bạn đến với hệ thống điểm danh")
        else:
            conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                           database="face")
            # messagebox.showerror("Không hợp lệ!", "Tên đăng nhập hoặc mật khẩu không hợp lệ")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from teacher where MaGV=%s and MK=%s",(
                self.var_DangNhap.get(),
                self.var_MatKhau.get()
            ))
            row=my_cursor.fetchone()
            print(row)
            if row==0:
                messagebox.showerror("Error","Tên đăng nhập & mật khẩu không tồn tại")
            else:
                self.root3 = Toplevel()
                self.app=Face_Recognition_System(self.root3)
                self.var_DangNhap=""
                self.var_MatKhau=""
            conn.commit()
            conn.close()
    def reset_pass(self):
        if self.txtpass_1.get() != self.txtpass_2.get():
            messagebox.showerror("Lỗi","Mật khẩu không khớp")
        else:
            conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                           database="face")

            my_cursor = conn.cursor()
            query = ("update teacher set mk=%s")
            value = (self.txtpass_2.get())
            my_cursor.execute(query, value)
            conn.commit()
            conn.close()


    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Vui lòng nhập tên đăng nhập")
        else:
            conn = mysql.connector.connect(host="127.0.0.1", port="3307", username="root", password="root",
                                           database="face")
            # messagebox.showerror("Không hợp lệ!", "Tên đăng nhập hoặc mật khẩu không hợp lệ")
            my_cursor = conn.cursor()
            query=("select * from teacher where MaGV=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Nhập đúng tên đăng nhập")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Quên mật khẩu")
                self.root2.geometry("340x450+610+170")
                l=Label(self.root2,text ="Quên mật khẩu",font=("times new roman",20,"bold"),fg="red",bg="white")
                l.place(x=0,y=10,relwidth=1)
                password_1 = lbl = Label( self.root2,text="Nhập mật khẩu", font=("time new roman", 15, "bold"), fg="white",
                                       bg="black")
                password_1.place(x=70, y=155)

                self.txtpass_1 = ttk.Entry( self.root2,font=("time new roman", 15, "bold"), textvariable=self.var_MatKhau_1)
                self.txtpass_1.place(x=40, y=180, width=270)

                password_2 = lbl = Label(self.root2,text="Nhập lại mật khẩu", font=("time new roman", 15, "bold"), fg="white",
                                       bg="black")
                password_2.place(x=70, y=225)

                self.txtpass_2 = ttk.Entry(self.root2,textvariable=self.var_MatKhau_2, font=("time new roman", 15, "bold"))
                self.txtpass_2.place(x=40, y=250, width=270)
                btn=Button(self.root2,command=self.reset_pass,text="Cập nhập",font=("time new roman", 15, "bold"), fg="white",
                                       bg="green")
                btn.place(x=100,y=290)


if __name__ == '__main__':
    main()