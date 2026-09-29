import sys
import os
import psutil
import time
import smtplib

from email.message import EmailMessage


# ------------------------------------------------------
# 01 : Process Scan
# ------------------------------------------------------

def ProcessScan():

    ListProcess = []

    for proc in psutil.process_iter():

        try:

            info = proc.as_dict(
                attrs=["pid", "name", "username"]
            )

            ListProcess.append(info)

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):

            continue

    return ListProcess


# ------------------------------------------------------
# 02 : Create Log File
# ------------------------------------------------------

def CreateLog(FolderName):

    if os.path.exists(FolderName):

        if not os.path.isdir(FolderName):

            print("Given name exists but it is not a directory")
            return None

    else:

        os.mkdir(FolderName)

        print("Directory created successfully")


    Timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    FileName = os.path.join(
        FolderName,
        "Marvellous_%s.log" % Timestamp
    )


    fobj = open(FileName, "w")

    Border = "-" * 50

    fobj.write(Border + "\n")
    fobj.write("     MARVELLOUS PROCESS LOGGER\n")
    fobj.write(Border + "\n")

    fobj.write(
        "Log File Created At : " +
        Timestamp + "\n"
    )

    fobj.write(Border + "\n\n")


    # Get Running Processes

    Data = ProcessScan()


    # Write Process Information

    for info in Data:

        fobj.write(
            "Process Name : " +
            str(info["name"]) + "\n"
        )

        fobj.write(
            "PID          : " +
            str(info["pid"]) + "\n"
        )

        fobj.write(
            "Username     : " +
            str(info["username"]) + "\n"
        )

        fobj.write(Border + "\n")


    fobj.close()

    print("Log file created successfully")
    print("Log File :", FileName)

    return FileName


# ------------------------------------------------------
# 03 : Send Log File Through Email
# ------------------------------------------------------

def SendMail(FileName, ReceiverEmail):

    SenderEmail = "YOUR_EMAIL@gmail.com"
    AppPassword = "YOUR_APP_PASSWORD"


    Message = EmailMessage()

    Message["From"] = SenderEmail
    Message["To"] = ReceiverEmail
    Message["Subject"] = "Marvellous Process Log"

    Message.set_content(
        "Please find attached the Process Log File."
    )


    # Attach Log File

    with open(FileName, "rb") as fobj:

        FileData = fobj.read()


    Message.add_attachment(
        FileData,
        maintype="text",
        subtype="plain",
        filename=os.path.basename(FileName)
    )


    # Connect Gmail SMTP Server

    try:

        Server = smtplib.SMTP("smtp.gmail.com", 587)

        Server.starttls()

        Server.login(
            SenderEmail,
            AppPassword
        )

        Server.send_message(Message)

        Server.quit()

        print("Email sent successfully")


    except Exception as E:

        print("Unable to send email")
        print("Error :", E)


# ------------------------------------------------------
# 04 : Main Function
# ------------------------------------------------------

def main():

    if len(sys.argv) != 3:

        print(
            "Usage : python ProcInfoLog.py "
            "DirectoryName EmailID"
        )

        return


    FolderName = sys.argv[1]

    ReceiverEmail = sys.argv[2]


    # Create Log

    FileName = CreateLog(FolderName)


    if FileName is not None:

        # Send Log

        SendMail(
            FileName,
            ReceiverEmail
        )


# ------------------------------------------------------
# Starter
# ------------------------------------------------------

if __name__ == "__main__":
    main()