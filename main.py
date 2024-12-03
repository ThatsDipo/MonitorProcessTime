import psutil
import time
import json
from cache import Cache

newCache = Cache()

def monitorProcess(target_name):
    seconds = 0

    while True:
        process_names = [p.info['name'] for p in psutil.process_iter(['name'])]

        if target_name in process_names:
            seconds = seconds + 1
            time.sleep(1)
        else:
            return seconds
        
def ShowMenu():
    print("==== Menù ====")
    print("[1] Monitora il tempo di un processo")
    print("[2] Lista delle sessioni di un processo")
    print("[3] Lista completa delle sessioni di tutti i processi")

    option = int(input("> "))

    if(option == 1):
        proc_name = input("Nome processo: ")
        seconds = monitorProcess(proc_name)
        minutes = seconds / 60
        hours = minutes / 60

        if(seconds > 0):
            newCache.NewSession(proc_name, seconds)
            print("Hai chiuso il processo")
            print(f"Tempo nel processo (secondi): {seconds}")

            if(seconds >= 60):
                print(f"Tempo nel processo (minuti): {minutes}")

            if(minutes >= 60):
                print(f"Tempo nel processo (ore): {hours}")
        else:
            print("Processo non trovato...")
    elif(option == 2):
        proc_name = input("Nome processo: ")
        sessions = newCache.GetProcSessions(proc_name)

        if(len(sessions) > 0):
            print(f"\n==== Lista sessioni di {proc_name} ====")

            for session in sessions:
                print(f"| Date: {session["date"]} | Seconds: {round(session["seconds"])} | Minutes: {round(session["minutes"])} | Hours: {round(session["hours"])} |")
        else:
            print("Non ci sono sessioni registrate su questo processo...")

        print("\n")
    elif(option == 3):
        print("\n")

        allSessions = newCache.GetSessionsOfAllProcess()

        if(len(allSessions) > 0):
            for procName, sessions in allSessions.items():
                if(len(sessions) > 0):
                    print(f"\n==== Lista sessioni di {procName} ====")
                    for session in sessions:
                        print(f"| Date: {session["date"]} | Seconds: {round(session["seconds"])} | Minutes: {round(session["minutes"])} | Hours: {round(session["hours"])} |")
                else:
                    print(f"Non ci sono sessioni registrate sul processo {procName}...")
        else:
            print("Non ci sono sessioni registrate su nessuno dei processi registrati...")

        print("\n")


    ShowMenu()

ShowMenu()