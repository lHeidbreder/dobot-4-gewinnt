# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 07:36:39 2020
@author: Digital Hub
"""

#Bibliothek importieren
import DobotDllType as dobot1 #impotieren der Ausführbefehle in "DobotD11Type"

#Dobot konfigurieren
CON_STR1 = {
    dobot1.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dobot1.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dobot1.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

api1 = dobot1.load() #Dll laden und Verwendung des CDLL Objekts

#Verbindung zu Dobot herstellen
state1 = dobot1.ConnectDobot(api1, "COM7", 115200)[0] #!Achten Sie bei dem Betrieb mehrerer DOBOT auf den richtigen seriellen Port!

print("Connect status of 1:",CON_STR1[state1])

if (state1 == dobot1.DobotConnect.DobotConnect_NoError):
    print("Setting up Command Queue")
    dobot1.SetQueuedCmdClear(api1)                        #Clean Command Queued
    dobot1.SetQueuedCmdStartExec(api1)                    #Befehlswarteschlange starten
    dobot1.SetPTPCmdEx(api1, 0, 193,  0,  23, -0.264, 1)      #optional Jump-Befehl zur absoluten Koordinate zu Beginn
    dobot1.dSleep(100)                                   #Verzögerungszeit wird benötigt, um Befehl auszuführen
    
    print("Homing")
    dobot1.SetHOMEParams(api1, 250, 0, 50, 0, isQueued = 1)
    dobot1.SetHOMECmd(api1, 0, isQueued = 1)
    
    while (not dobot1.GetQueuedCmdMotionFinish(api1)[0]):
        print("Waiting... Current 1: ", dobot1.GetQueuedCmdCurrentIndex(api1))
        dobot1.dSleep(200)

    #HIER CODE SCHREIBEN

dobot1.DisconnectDobot(api1)      #Verbindung zum Roboter trennen
print("Disconnectet - Dobot programm stopped")