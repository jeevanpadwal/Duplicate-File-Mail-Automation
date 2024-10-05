import os
import hashlib
from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import Tk, Label, Button, Entry, Text, filedialog, messagebox, StringVar
from tkinter.scrolledtext import ScrolledText
import time

class DuplicateFileFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate File Finder")
        self.root.geometry("700x500")
        self.root.config(bg="#F3F4F6")  # Background color
        
        self.file_path = ""
        self.duplicates = []
        self.email = StringVar()

        # UI Elements with design
        self.create_ui()

    def create_ui(self):
        # Title Label
        Label(self.root, text="Duplicate File Finder", font=("Arial", 20, "bold"),
              fg="#1F2937", bg="#F3F4F6").pack(pady=20)

        # Folder Selection Button
        Button(self.root, text="Select Folder", command=self.select_folder, font=("Arial", 12),
               bg="#10B981", fg="white", activebackground="#065F46", width=20, height=2).pack(pady=10)
        
        self.folder_label = Label(self.root, text="No folder selected", font=("Arial", 12),
                                  fg="#374151", bg="#F3F4F6")
        self.folder_label.pack(pady=5)
        
        # Email Input Label and Entry
        Label(self.root, text="Enter your email:", font=("Arial", 12), fg="#374151", bg="#F3F4F6").pack(pady=5)
        self.email_entry = Entry(self.root, textvariable=self.email, font=("Arial", 12),
                                 fg="#111827", bg="white", width=40, borderwidth=2, relief="groove")
        self.email_entry.pack(pady=5)
        
        # Find Duplicates Button
        Button(self.root, text="Find Duplicates", command=self.find_duplicates, font=("Arial", 12),
               bg="#1F2937", fg="white", activebackground="#111827", width=20, height=2).pack(pady=10)
        
        # Results Display Area
        self.result_area = ScrolledText(self.root, height=10, width=60, font=("Arial", 12),
                                        fg="#111827", bg="white", borderwidth=2, relief="groove")
        self.result_area.pack(pady=10)
        
        # Delete Duplicates Button
        Button(self.root, text="Delete Duplicates", command=self.delete_duplicates, font=("Arial", 12),
               bg="#EF4444", fg="white", activebackground="#B91C1C", width=20, height=2).pack(pady=10)

    def select_folder(self):
        self.file_path = filedialog.askdirectory(title="Select a folder")
        if self.file_path:
            self.folder_label.config(text=f"Selected Folder: {self.file_path}", fg="#10B981")
        else:
            self.folder_label.config(text="No folder selected", fg="#EF4444")

    def find_duplicates(self):
        if not self.file_path:
            messagebox.showwarning("Error", "Please select a folder first")
            return
        
        self.duplicates = self.get_duplicates(self.file_path)
        
        self.result_area.delete(1.0, "end")
        if self.duplicates:
            self.result_area.insert("end", f"Found {len(self.duplicates)} duplicate files:\n", "highlight")
            for file in self.duplicates:
                self.result_area.insert("end", f"{file}\n")
        else:
            self.result_area.insert("end", "No duplicate files found")

        self.email = self.email_entry.get()
        if self.email:
            log_dir = self.generate_log(self.duplicates)
            self.send_email(log_dir, self.email)

    def get_duplicates(self, dir_name):
        list_of_files = os.walk(dir_name)
        unique_files = {}
        duplicates = []
        
        for root, folders, files in list_of_files:
            for file in files:
                file_path = Path(os.path.join(root, file))
                hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                
                if hash_file not in unique_files:
                    unique_files[hash_file] = file_path
                else:
                    duplicates.append(file_path)

        return duplicates

    def generate_log(self, duplicates, log_dir="Duplicate"):
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        
        log_path = os.path.join(log_dir, f"Log_{int(time.time())}.txt")
        with open(log_path, 'w') as fd:
            fd.write("Duplicate Files:\n")
            for file in duplicates:
                fd.write(f"{file}\n")
        
        return log_path

    def send_email(self, log_dir, email):
        fromaddr = "youremail@gmail.com"
        toaddr = email
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Duplicate File Names"
        
        body = "Dear User,\nPlease find the attached log of duplicate files.\n"
        msg.attach(MIMEText(body, 'plain'))
        
        attachment = open(log_dir, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename= {log_dir}")
        msg.attach(p)

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromaddr, "your-app-password")
            s.sendmail(fromaddr, toaddr, msg.as_string())
            s.quit()
            messagebox.showinfo("Success", "Email sent with the log file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def delete_duplicates(self):
        if not self.duplicates:
            messagebox.showwarning("Error", "No duplicate files found to delete")
            return

        confirm = messagebox.askyesno("Delete Duplicates", "Are you sure you want to delete the duplicate files?")
        if confirm:
            for file in self.duplicates:
                os.remove(file)
            self.result_area.insert("end", "\nDuplicate files deleted successfully", "highlight")
        else:
            self.result_area.insert("end", "\nDuplicate file deletion canceled")

# Main execution
if __name__ == "__main__":
    root = Tk()
    app = DuplicateFileFinder(root)
    root.mainloop()
