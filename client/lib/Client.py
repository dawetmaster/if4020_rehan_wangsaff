import tkinter as tk
from tkinter import simpledialog, filedialog as fd
from .Database import Database
from .E2EE import E2EE
import hashlib

class RegisterDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Pendaftaran Akun")

        tk.Label(master, text="Nama Pengguna:",anchor='w').grid(row=0, column=0, padx=10, pady=5,sticky='w')
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Kata Sandi:",anchor='w').grid(row=1, column=0, padx=10, pady=5,sticky='w')
        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Konfirmasi Kata Sandi:",anchor='w').grid(row=2, column=0, padx=10, pady=5,sticky='w')
        self.entry_confirm_password = tk.Entry(master, show='*')
        self.entry_confirm_password.grid(row=2, column=1, padx=10, pady=5)
        # Fokuskan input pertama ke username
        return self.entry_username 

    def apply(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        self.confirm_password = self.entry_confirm_password.get()
class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Halaman Masuk")

        tk.Label(master, text="Nama Pengguna:",anchor='w').grid(row=0, column=0, padx=10, pady=5,sticky='w')
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Kata Sandi:",anchor='w').grid(row=1, column=0, padx=10, pady=5,sticky='w')
        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        # Fokuskan input pertama ke username
        return self.entry_username 

    def apply(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

class KeyDialog(tk.Toplevel):
    def __init__(self, parent, public_key, private_key,ds_public_key,ds_private_key,user_name):
        super().__init__(parent)
        self.title("Informasi Kunci")
        self.geometry("400x200")

        # E2EE Key
        e2ee_frame = tk.Frame(self, relief=tk.GROOVE,bd=2)
        e2ee_frame.pack(expand=True,fill=tk.X)
        tk.Label(e2ee_frame, text="Kunci E2EE", font=("Arial", 16),justify='center').pack(pady=(10, 0))
        # Public Key
        tk.Label(e2ee_frame, text="Kunci Publik:").pack(pady=(10, 0),anchor='w')
        tk.Label(e2ee_frame, text=str(public_key)).pack(pady=(0, 10),anchor='w')
        tk.Button(e2ee_frame, text="Unduh Kunci Publik", command=self.download_public_key).pack(pady=(0, 10),anchor='center')
        # Private Key
        tk.Label(e2ee_frame, text="Kunci Privat:").pack(pady=(10, 0),anchor='w')
        tk.Label(e2ee_frame, text=str(private_key)).pack(pady=(0, 10),anchor='w')
        tk.Button(e2ee_frame, text="Unduh Kunci Privat", command=self.download_private_key).pack(pady=(0, 10),anchor='center')

        self.public_key = public_key
        self.private_key = private_key

        # Digital Signature Key
        ds_frame = tk.Frame(self, relief=tk.GROOVE,bd=2)
        ds_frame.pack(expand=True,fill=tk.X)
        tk.Label(ds_frame, text="Kunci Digital Signature", font=("Arial", 16)).pack(pady=(10, 0))
        # Public Key
        tk.Label(ds_frame, text="Kunci Publik:").pack(pady=(10, 0))
        tk.Label(ds_frame, text=str(ds_public_key)).pack(pady=(0, 10))
        tk.Button(ds_frame, text="Unduh Kunci Publik", command=self.download_ds_public_key).pack(pady=(0, 10))

        # Private Key
        tk.Label(ds_frame, text="Kunci Privat:").pack(pady=(10, 0))
        tk.Label(ds_frame, text=str(ds_private_key)).pack(pady=(0, 10))
        tk.Button(ds_frame, text="Unduh Kunci Privat", command=self.download_ds_private_key).pack(pady=(0, 10))

        self.ds_public_key = ds_public_key
        self.ds_private_key = ds_private_key

        self.user_name = user_name


    def download_public_key(self):
        try:
            with open(f"keys/{self.user_name}.ecpub", "x") as f:
                f.write(f"{self.user_name}::{self.public_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}.ecpub] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}.ecpub]")

    def download_private_key(self):
        try:
            with open(f"keys/{self.user_name}.ecprv", "x") as f:
                f.write(f"{self.user_name}::{self.private_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}.ecprv] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}.ecprv]")

    def download_ds_public_key(self):
        try:
            with open(f"keys/{self.user_name}.scpub", "x") as f:
                f.write(f"{self.user_name}::{self.ds_public_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}.scpub] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}.scpub]")

    def download_ds_private_key(self):
        try:
            with open(f"keys/{self.user_name}.scprv", "x") as f:
                f.write(f"{self.user_name}::{self.ds_private_key}")
        except FileExistsError:
            tk.messagebox.showwarning("File Sudah Ada", f"Kunci sudah ada di  [keys/{self.user_name}.scprv] ", icon='warning')
        else:
            tk.messagebox.showinfo("Pengunduhan Sukses", f"Kunci berhasil disimpan di [keys/{self.user_name}.scprv]")

class Client(tk.Tk):
    def __init__(self,port:int):
        super().__init__()

        # Atur window
        self.title("Wangsaff ©")
        self.geometry("1000x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.start_page = StartPage(self)
        self.chat_page = ChatPage(self,port)

        self.show_page(self.start_page)

    def show_page(self, page):
        page.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self)
        container.grid(row=0, column=0)
        
        # Big Label for title
        self.title_label = tk.Label(
            container, text="Wangsaff ©", font=("Arial", 24), pady=10)
        self.title_label.pack()
        
        # Author credit
        self.author_label = tk.Label(
            container, text="by Rehan Wangsaff team", font=("Arial", 12), pady=10)
        self.author_label.pack()

        # Frame untuk memasukkan kunci private dirinya dan kunci publik lawan bicaranya disusun vertikal dan diakhiri tombol "Hubungkan". Frame memiliki border dan label memasukkan kunci publik dan entri berada pada baris yang sama, begitupun yang kunci privat
        self.connect_frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
        self.connect_frame.pack(pady=10)
        
        self.connect_label = tk.Label(
            self.connect_frame, text="Kunci Publik Lawan Bicara:", font=("Arial", 12), anchor='w')
        self.connect_label.grid(row=0, column=0, sticky='w')
        self.public_entry = tk.Entry(self.connect_frame, font=("Arial", 12))
        self.public_entry.grid(row=0, column=1)
        
        self.connect_button = tk.Button(
            self.connect_frame, text="Pilih Kunci Publik", font=("Arial", 12), bd=4, command=self.select_public_key)
        self.connect_button.grid(row=0, column=2)
        
        self.connect_label = tk.Label(
            self.connect_frame, text="Kunci Privat Anda:", font=("Arial", 12), anchor='w')
        self.connect_label.grid(row=1, column=0, sticky='w')
        self.private_entry = tk.Entry(self.connect_frame, font=("Arial", 12))
        self.private_entry.grid(row=1, column=1)
        
        self.connect_button = tk.Button(
            self.connect_frame, text="Pilih Kunci Privat", font=("Arial", 12), bd=4, command=self.select_private_key)
        self.connect_button.grid(row=1, column=2)
        
        self.connect_frame.grid_rowconfigure(2, minsize=50)
        
        self.connect_button = tk.Button(
            self.connect_frame, text="Hubungkan", font=("Arial", 12), bd=4, command=self.open_chat)
        self.connect_button.grid(row=2, column=0, columnspan=2)
        
        # Tombol untuk mengakses kunci pengguna
        self.register_login_frame = tk.Frame(container, bd=2, relief=tk.GROOVE)
        self.register_login_frame.pack(pady=10)
        self.register_button = tk.Button(
            self.register_login_frame, text="Daftar", font=("Arial", 12), bd=4, command=self.register_user)
        self.register_button.grid(row=0, column=0)
        self.register_login_frame.grid_columnconfigure(1, minsize=50)
        self.login_button = tk.Button(
            self.register_login_frame, text="Masuk", font=("Arial", 12), bd=4, command=self.login)
        self.login_button.grid(row=0, column=1)

    def open_chat(self):
        # Bikin dialog konfirmasi "Apakah kunci yang Anda masukkan sudah benar?"
        confirm = tk.messagebox.askyesno("Konfirmasi", "Apakah kunci yang Anda masukkan sudah benar?")
        if not confirm:
            return
        # Baca entry kunci privat dan publik.
        public_key = self.public_entry.get()
        private_key = self.private_entry.get()
        # Jika salah satu kosong, tampilkan pesan error
        if not public_key or not private_key:
            tk.messagebox.showerror("Error", "Kunci Publik dan Privat Harus Diisi!")
            return
        # init chat
        self.master.chat_page.init_chat(public_key,private_key)
        # Buka chat window
        self.master.show_page(self.master.chat_page)

    def register_user(self):
        dialog = RegisterDialog(self)
        if dialog.username and dialog.password and dialog.confirm_password:
            if dialog.password != dialog.confirm_password:
                tk.messagebox.showerror("Error", "Kata Sandi Tidak Cocok!")
            else:
                Database.add_user(dialog.username, hashlib.sha256(dialog.password.encode()).hexdigest())
                tk.messagebox.showinfo("Sukses", "Pendaftaran berhasil!\nSilahkan Masuk Untuk Melihat Kunci Anda.")
        else:
            tk.messagebox.showerror("Error", "Semua Kolom Harus Diisi!")

    def login(self):
        dialog = LoginDialog(self)
        # cari user
        user = Database.search_user_by_credential(dialog.username, dialog.password)
        if user:
            # Bikin dialog yang menampilkan kunci pengguna beserta tombol untuk mengunduh kunci
            # TODO kunci buat digital signature
            KeyDialog(self, user[3], user[4], "", "", user[1])
        else:
            tk.messagebox.showerror("Error", "Username atau kata sandi salah!")

    def select_public_key(self):
        file_path = fd.askopenfilename(title="Pilih Kunci Publik")
        if not file_path:
            return 
        with open(file_path, "r") as f:
            self.public_entry.insert(0, f.read())

    def select_private_key(self):
        file_path = fd.askopenfilename(title="Pilih Kunci Privat")
        if not file_path:
            return
        with open(file_path, "r") as f:
            self.private_entry.insert(0, f.read())

class ChatPage(tk.Frame):
    def __init__(self, parent, port: int):
        super().__init__(parent)
        self.port = port
        # grid semua elemen
        self.grid(row=0, column=0, sticky='nsew')
        # Buat chat screen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Buat PanedWindow untuk memisahkan chat screen dan message box
        paned_window = tk.PanedWindow(self, orient=tk.VERTICAL)
        paned_window.grid(row=0, column=0, sticky='nsew')
        
        # frame untuk chat screen
        top_frame = tk.Frame(paned_window)
        paned_window.add(top_frame, stretch='always')
        paned_window.paneconfig(top_frame, height=300)  # Tinggi chat screen
        
        # frame untuk message box
        bottom_frame = tk.Frame(paned_window)
        paned_window.add(bottom_frame)

        # Atur scrollbar
        chat_display_frame = tk.Frame(top_frame)
        chat_display_frame.pack(fill=tk.BOTH, expand=True)
        chat_display_scrollbar = tk.Scrollbar(chat_display_frame)
        self.chat_display = tk.Text(chat_display_frame, state='disabled', width=50, height=10, yscrollcommand=chat_display_scrollbar.set)
        chat_display_scrollbar.config(command=self.chat_display.yview)
        chat_display_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

        # Message box buat entry dan tombol terkait
        self.message_entry = tk.Entry(bottom_frame, width=50)
        self.message_entry.pack(pady=5)
        tk.Button(bottom_frame, text="Send", command=self.send_message).pack(pady=5)
        tk.Button(bottom_frame, text="Back", command=self.back_to_start).pack(pady=20)

    def init_chat(self,public_key:str,private_key:str):
        tmp = public_key.split("::")
        self.chatmate = tmp[0]
        if len(tmp)<2:
            self.public_key = tmp[0]
        else:
            self.public_key = tmp[1]
        tmp = private_key.split("::")
        if len(tmp)<2:
            self.private_key = tmp[0]
        else:
            self.private_key = tmp[1]

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Simpan ke database
            Database.add_message(self.port,E2EE.encrypt(message.encode(),self.public_key))
            # Cetak Pesan
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"You: {message}\n")

            # Tombol buat melihat dan verifikasi signature
            view_button = tk.Button(self.chat_display, text="Lihat Signature", command=self.view_signature)
            verify_button = tk.Button(self.chat_display, text="Verifikasi Signature", command=self.verify_signature)

            # Tambahkan tombol ke display
            self.chat_display.window_create(tk.END, window=view_button)
            self.chat_display.window_create(tk.END, window=verify_button)
            self.chat_display.insert(tk.END, "\n")

            # Hapus teks di message box
            self.chat_display.config(state='disabled')
            self.message_entry.delete(0, tk.END)

    def back_to_start(self):
        self.master.show_page(self.master.start_page)

    def verify_signature(self):
        tk.messagebox.showinfo("Verification", "The signature is valid.")

    def view_signature(self):
        tk.messagebox.showinfo("Pake Nanya")