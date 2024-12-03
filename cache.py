from datetime import datetime as d
import json

# self.date = d.now("%d/%m/Y %H:%M:%S")

class Cache:
    def __init__(self):
        with open("./cache.json", "r+") as fileHandle:
            content = fileHandle.read()
            content_lenght = len(content)

            if(content_lenght < 2):
                fileHandle.write("{}")
                self.object = {}
            else:
                self.object = json.loads(content)
    def __verifyProcessObject(self, procName):
        if procName not in self.object:
            self.object[procName] = {
                "hours": 0,
                "minutes": 0,
                "seconds": 0,
                "sessions": []
            }

    def __calculateEveryTimeUnit(self, seconds):
        time = {
            "minutes": seconds / 60,
            "hours": seconds / 3600
        }
        return time
    
    def __saveCache(self):
        with open("./cache.json", "w") as fileHandle:
            json_obj = json.dumps(self.object, indent = 4)
            fileHandle.write(json_obj)

    def GetProcSessions(self, procName):
        self.__verifyProcessObject(procName)
        return self.object[procName]["sessions"]

    def GetSessionsOfAllProcess(self):
        sessions = {}

        for procName, processInfo in self.object.items():
            sessions[procName] = processInfo["sessions"]

        return sessions


    def NewSession(self, procName, seconds):
        self.__verifyProcessObject(procName)
        time = self.__calculateEveryTimeUnit(seconds)
        date = d.now().strftime("%d/%m/%Y %H:%M:%S")

        currentProcObj = self.object[procName]

        currentProcObj["hours"] = currentProcObj["hours"] + time["hours"] # Ore totali
        currentProcObj["minutes"] = currentProcObj["minutes"] + time["minutes"] # Ore totali
        currentProcObj["seconds"] = currentProcObj["seconds"] + seconds # Ore totali

        self.object[procName] = currentProcObj

        self.object[procName]["sessions"].append({
            "hours": time["hours"],
            "minutes": time["minutes"],
            "seconds": seconds,
            "date": date
        })

        self.__saveCache()