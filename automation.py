import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def file_renamer():
    folder = input("Enter folder path for renaming: ").strip()
    if not os.path.exists(folder):
        print("❌ Folder not found.")
        return
    prefix = input("Enter base filename prefix (e.g. document): ").strip()
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for index, filename in enumerate(sorted(files), start=1):
        _, ext = os.path.splitext(filename)
        old_path = os.path.join(folder, filename)
        new_name = f"{prefix}_{index}{ext}"
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} --> {new_name}")
    print("✅ All files renamed successfully!")

def data_extractor():
    file_path = input("Enter path to text file containing data: ").strip()
    if not os.path.exists(file_path):
        print("❌ File not found.")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    phone_regex = r"(?:\+91[\s-]?)?[6-9]\d{9}\b"

    emails = set(re.findall(email_regex, text))
    phones = set(re.findall(phone_regex, text))

    with open("emails.txt", "w") as f:
        f.write("\n".join(sorted(emails)))
    with open("phones.txt", "w") as f:
        f.write("\n".join(sorted(phones)))

    print(f"✅ Extracted {len(emails)} emails -> saved in emails.txt")
    print(f"✅ Extracted {len(phones)} phones -> saved in phones.txt")

def email_automation():
    sender = input("Enter sender email: ").strip()
    password = input("Enter Gmail App Password: ").strip()
    receiver = input("Enter receiver email: ").strip()
    subject = input("Enter subject: ").strip()
    message = input("Enter message body: ").strip()

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    while True:
        print("\n==========================================")
        print("      AUTOMATION SCRIPT PACK MENU         ")
        print("==========================================")
        print("1. Batch File Renamer")
        print("2. Regex Data Extractor (Emails & Phones)")
        print("3. Email Automation (SMTP)")
        print("4. Exit")
        print("------------------------------------------")
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1": file_renamer()
        elif choice == "2": data_extractor()
        elif choice == "3": email_automation()
        elif choice == "4": break

if __name__ == "__main__":
    main()
