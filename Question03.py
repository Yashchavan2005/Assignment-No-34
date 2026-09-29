import sys
import os
import psutil
import time


# ------------------------------------------------------
# 01 : Process Information
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

    if not os.path.exists(FolderName):

        os.mkdir(FolderName)

    elif not os.path.isdir(FolderName):

        print("Given name is not a directory")
        return


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


# ------------------------------------------------------
# 03 : Main Function
# ------------------------------------------------------

def main():

    if len(sys.argv) != 2:

        print("Usage : python ProcInfoLog.py Demo")
        return

    FolderName = sys.argv[1]

    CreateLog(FolderName)


# ------------------------------------------------------
# Starter
# ------------------------------------------------------

if __name__ == "__main__":
    main()