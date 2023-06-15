import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

class LoginForm():
    def __init__(self, root):
        self.root = root
        self.root.title("INICIO DE SESION")
        self.root.geometry("800x500")

        image = Image.open("aña.png")
        image = image.resize((800, 500))
        self.photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(root, image=self.photo)
        self.image_label.place(x=0, y=0)  

        self.username_entry = tk.Entry(root)
        self.username_entry.config(bg="#ffffff",width=36)
        self.username_entry.place(x=535, y=190)  

    
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.config(bg="#ffffff",width=36)
        self.password_entry.place(x=535, y=258) 

        self.login_button = tk.Button(root, text="INICIAR SESION", fg="Black", command=self.login)
        self.login_button.config(
            
            bg="#bb86fc",
            relief=tk.RAISED,
        )
        self.login_button.place(x=563, y=310)
        self.login_button.config(width=22,bd=0)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "Usu" and password == "123":
            messagebox.showinfo("Inicio de sesión exitoso", "Muy Bien :v")
            subprocess.Popen(["python", "proyecto.py"])  
            self.root.destroy() 
        else:
            messagebox.showerror("Eror", "Usted no es el propietario de este programa")

root = tk.Tk()
root.resizable(False,False)
login_form = LoginForm(root)
root.mainloop()