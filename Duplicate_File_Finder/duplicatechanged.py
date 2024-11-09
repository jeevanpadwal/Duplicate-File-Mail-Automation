import os
import shutil
import send2trash
import matplotlib.pyplot as plt
from PIL import Image, ImageTk ########################################image processing
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv


class EmailInputDialog:
    def __init__(self, master, on_submit):
        self.top = Toplevel(master)
        self.top.title("Enter Recipient Email(s)")
        self.top.geometry("400x200")

        #############################################################################
        self.top.grid_rowconfigure(0, weight=1)  # Top padding
        self.top.grid_rowconfigure(1, weight=1)  # Label
        self.top.grid_rowconfigure(2, weight=1)  # Entry
        self.top.grid_rowconfigure(3, weight=1)  # Submit button
        self.top.grid_rowconfigure(4, weight=1)  # Bottom padding
        self.top.grid_columnconfigure(0, weight=1)###########################################################

        
        label = Label(self.top, text="Enter recipient email(s) separated by commas:", font=("Arial", 14))
        label.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.email_entry = Entry(self.top, font=("Arial", 14), width=40)
        self.email_entry.grid(row=2, column=0, padx=10, pady=10, sticky="n")

        submit_button = Button(self.top, text="Submit", command=self.submit, font=("Arial", 14), bg="#10B981", fg="white")
        submit_button.grid(row=3, column=0, pady=10)

        self.on_submit = on_submit



    def submit(self):
        emails = self.email_entry.get().strip()
        if emails:
            self.on_submit(emails)
            self.top.destroy()
        else:
            messagebox.showwarning("Error", "Please enter at least one recipient email.")

class DuplicateFileFinder:
    def __init__(self):
        self.root = TkinterDnD.Tk()  ############# Initialize TkinterDnD for drag-and-drop
        self.root.title("Duplicate File Finder")
        self.root.geometry("700x600")
        self.file_path = ""
        self.duplicates = []

        
        self.create_ui()

    def create_ui(self):
        #############                      Folder selection                      ############################
        self.folder_label = Label(self.root, text="Drag and drop a folder or select it manually:", font=("Arial", 12))
        self.folder_label.pack(pady=10)

        self.select_folder_button = Button(self.root, text="Select Folder", command=self.browse_folder, font=("Arial", 12),
                                           bg="#4CAF50", fg="white", width=20, height=2)
        self.select_folder_button.pack(pady=10)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_folder)  ######################           Drag-and-drop functionality         #####################

        
        self.result_area = Text(self.root, height=10, font=("Arial", 12))
        self.result_area.pack(pady=10)

        #################    Buttons     ####################
        Button(self.root, text="Find Duplicates", command=self.find_duplicates, font=("Arial", 12),
               bg="#1F2937", fg="white", width=20, height=2).pack(pady=10)

        Button(self.root, text="Isolate Duplicates", command=self.isolate_duplicates, font=("Arial", 12),
               bg="#FBBF24", fg="white", width=20, height=2).pack(pady=10)

        Button(self.root, text="Delete Duplicates", command=self.delete_duplicates, font=("Arial", 12),
               bg="#DC2626", fg="white", width=20, height=2).pack(pady=10)

        Button(self.root, text="Export to CSV", command=self.export_to_csv, font=("Arial", 12),
               bg="#1D4ED8", fg="white", width=20, height=2).pack(pady=10)

        Button(self.root, text="Send Report via Email", command=self.open_email_dialog, font=("Arial", 12),
               bg="#10B981", fg="white", width=20, height=2).pack(pady=10)

    def browse_folder(self):
        self.file_path = filedialog.askdirectory()
        if self.file_path:
            self.folder_label.config(text=f"Selected Folder: {self.file_path}", fg="#10B981")
    
    def drop_folder(self, event):
        self.file_path = event.data
        self.folder_label.config(text=f"Selected Folder: {self.file_path}", fg="#10B981")

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
            
            ############ Generate file type chart(pie chart)##########
            self.generate_file_type_chart(self.duplicates)
            
        else:
            self.result_area.insert("end", "No duplicate files found")

    def get_duplicates(self, folder):
        file_hashes = {}
        duplicates = []
        allowed_extensions = {'.txt', '.jpg', '.png', '.docx'}  ##################### allowed file types ############
    
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in allowed_extensions:  ################ Checks if the file extension is allowedd    #####################
                    filepath = os.path.join(root, file)
                    file_hash = self.get_file_hash(filepath)
                    if file_hash in file_hashes:
                        duplicates.append(filepath)
                    else:
                        file_hashes[file_hash] = filepath
        return duplicates

    def get_file_hash(self, file_path):
        return hash(os.path.getsize(file_path))

    def generate_file_type_chart(self, duplicates):
        file_type_count = {}
        
        for file in duplicates:
            file_extension = os.path.splitext(file)[1]
            if file_extension in file_type_count:
                file_type_count[file_extension] += 1
            else:
                file_type_count[file_extension] = 1

        labels = file_type_count.keys()
        sizes = file_type_count.values()
        
        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
        plt.axis('equal')
        plt.title("Duplicate File Type Distribution")
        plt.show()

    def isolate_duplicates(self):
        isolation_folder = os.path.join(self.file_path, "Isolated_Duplicates")
        if not os.path.exists(isolation_folder):
            os.makedirs(isolation_folder)
        
        for file in self.duplicates:
            shutil.move(file, isolation_folder)
        
        messagebox.showinfo("Isolation", "Duplicate files moved to isolation folder")
        self.result_area.insert("end", "\nDuplicate files moved to isolation successfully", "highlight")

    def delete_duplicates(self):
        if not self.duplicates:
            messagebox.showwarning("Error", "No duplicate files found to delete")
            return

        confirm = messagebox.askyesno("Delete Duplicates", "Are you sure you want to delete the duplicate files?")
        if confirm:
            self.show_disk_space()

            for file in self.duplicates:
                os.remove(file)

            self.result_area.insert("end", "\nDuplicate files deleted successfully", "highlight")
            self.show_disk_space()
        else:
            self.result_area.insert("end", "\nDuplicate file deletion canceled")

    def show_disk_space(self):
        total, used, free = shutil.disk_usage(self.file_path)
        used_percentage = (used / total) * 100
        free_percentage = (free / total) * 100

        self.result_area.insert("end", f"Disk Space: {used_percentage:.2f}% Used, {free_percentage:.2f}% Free\n")

    def export_to_csv(self):
        if not self.duplicates:
            messagebox.showwarning("Warning", "No duplicates found to export.")
            return

        log_file = self.generate_log(self.duplicates)
        if log_file:
            messagebox.showinfo("CSV Export", f"Duplicate files exported to {log_file}")

    def generate_log(self, duplicates):
        log_file = os.path.join(self.file_path, "duplicate_log.csv")
        try:
            with open(log_file, "w", newline='') as log:
                writer = csv.writer(log)
                writer.writerow(['Duplicate Files'])
                for file in duplicates:
                    writer.writerow([file])
            return log_file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate log file: {str(e)}")
            return None
        
    def open_email_dialog(self):
        EmailInputDialog(self.root, self.send_email_report)

    def send_email_report(self, emails):
        recipient_emails = [email.strip() for email in emails.split(",")]

        try:
            ########### Email setup  ##############
            sender_email = "supercoin2002@gmail.com"
            password = "*****************"
            log_file = self.generate_log(self.duplicates)  ################## Generates log for email #################
            subject = "Duplicate Files Report"
            body = "Please find the attached duplicate files report."

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ", ".join(recipient_emails)
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            #################                  Attaches the log file                ###################
            with open(log_file, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(log_file)}')
                msg.attach(part)

            ################              Sending email         ###################
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient_emails, msg.as_string())

            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def run(self):
        self.root.mainloop()

class LoginWindow:
    def __init__(self):
        self.login_root = Tk()
        self.login_root.title("Login Page")
        self.login_root.geometry("400x300")
        self.username = StringVar()
        self.password = StringVar()

        self.create_login_ui()

    def create_login_ui(self):
        Label(self.login_root, text="Login", font=("Arial", 24)).pack(pady=20)
        
        Label(self.login_root, text="Username:", font=("Arial", 12)).pack(pady=5)
        Entry(self.login_root, textvariable=self.username, font=("Arial", 12)).pack(pady=5)

        Label(self.login_root, text="Password:", font=("Arial", 12)).pack(pady=5)
        Entry(self.login_root, textvariable=self.password, font=("Arial", 12), show="*").pack(pady=5)

        Button(self.login_root, text="Login", command=self.authenticate, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

    def authenticate(self):
        
        if self.username.get() == "11" and self.password.get() == "22":
            self.login_root.destroy()
            self.start_application()
        else:
            messagebox.showwarning("Login Failed", "Incorrect username or password")

    def start_application(self):
        app = DuplicateFileFinder()
        app.run()

if __name__ == "__main__":
    LoginWindow().login_root.mainloop()
