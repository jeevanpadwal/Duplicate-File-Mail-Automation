# Duplicate File Finder
A user-friendly desktop application to find and delete duplicate files from any selected folder and send a report via email.

![Jeevan Padwal](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image001.png)

## Features
- **Folder Selection**: Easily browse and select a folder to scan for duplicate files.
- **Duplicate Detection**: Uses MD5 hash algorithm to detect duplicate files with precision.
- **Email Log**: Automatically sends an email containing a log of all duplicate files detected.
- **File Deletion**: Safely delete duplicate files from your folder with a confirmation dialog.
- **Log Generation**: Generates a detailed log file for each execution with a timestamp.

## Tech Stack
- **Language**: Python
- **Libraries**:
  - `tkinter` for building the graphical user interface.
  - `hashlib` for file hashing (MD5).
  - `smtplib` for sending emails.
  - `pathlib`, `os` for file handling.
  - `ScrolledText` for handling large text areas.

## Screenshots
### Main Application Interface
![Main Application Interface](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image002.png)

### Folder Selection
![Folder Selection](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image004.png)

### Duplicate Files Display
![Duplicate Files Display](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image006.png)

## How to Install
- Clone the repository or download the project files:
    ```bash
    git clone https://github.com/username/duplicate-file-finder.git
    ```
- Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
- Ensure you have a valid Gmail account to use for sending the email log. Update the sender email and app password in the script.

## Usage
- Run the application:
    ```bash
    python duplicate_file_finder.py
    ```
- Select a folder: Click the "Select Folder" button and choose a directory to scan for duplicate files.

![Folder Selection](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image008.png)

- Find Duplicates: Click "Find Duplicates" to start scanning the selected folder. A log will display the duplicate files found.

![Find Duplicates](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image009.png)

- Email Log: If you've entered an email, a log file with duplicates will be sent to your inbox.

![Email Log](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image010.png)

- Delete Duplicates: Click "Delete Duplicates" to remove the files from your system. A confirmation will be asked before deletion.

![Delete Duplicates](https://raw.githubusercontent.com/jeevanpadwal/Duplicate-File-Mail-Automation/refs/heads/main/Images/image012.png)

## Log Files
The program generates a log file after every scan and places it in the Logs directory with a timestamp. This log contains all duplicate file paths.

Example of a log file name:
```
Log_1633024802.txt
```
## Email Configuration
You need to configure your Gmail account to allow access via third-party apps (this is necessary for the `smtplib` library to send the email):

- Set your Gmail account to allow less secure apps or generate an App Password if using 2FA.

In the script, update the following lines with your email and app password:

```python
fromaddr = "youremail@gmail.com"
s.login(fromaddr, "your-app-password")
```
## Contribution
- Fork the repository.
- Create a new branch:
  ```bash
   git checkout -b feature-branch
  ```
- Commit your changes:
  ```bash
   git commit -m "Add some feature"
  ```
- Push to the branch:
  ```bash
   git push origin feature-branch
  ```
- Create a pull request.

