import sys
import psutil


# ------------------------------------------------------
# 01 : Process Information
# ------------------------------------------------------

def ProcessInfo(ProcessName):

    Found = False

    for proc in psutil.process_iter():

        try:

            info = proc.as_dict(
                attrs=["pid", "name", "username", "status"]
            )

            if info["name"] is not None:

                if info["name"].lower() == ProcessName.lower():

                    Found = True

                    print("----------------------------------------")
                    print("Process Name :", info["name"])
                    print("Process ID   :", info["pid"])
                    print("Username     :", info["username"])
                    print("Status       :", info["status"])
                    print("----------------------------------------")

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):

            continue


    if Found == False:

        print("Process is not running")


# ------------------------------------------------------
# 02 : Main Function
# ------------------------------------------------------

def main():

    if len(sys.argv) != 2:

        print("Invalid Number of Arguments")
        print("Usage : python ProcInfo.py ProcessName")
        return

    ProcessName = sys.argv[1]

    ProcessInfo(ProcessName)


# ------------------------------------------------------
# Starter
# ------------------------------------------------------

if __name__ == "__main__":
    main()