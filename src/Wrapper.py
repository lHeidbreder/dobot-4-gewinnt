from importlib import import_module

class Wrapper:
	DobotAPI = None
	__DobotID = -1
	__isConnected = False

	def __init__(self, playerID: int, comPort: str):
		self.__DobotID = playerID

		if playerID == 0:
			self.DobotDLL = import_module('Dobot0DLLType')
		else:
			self.DobotDLL = import_module('Dobot1DLLType')
		
		#Dobot konfigurieren
		CON_STR1 = {
			self.DobotDLL.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
			self.DobotDLL.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
			self.DobotDLL.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

		self.DobotAPI = self.DobotDLL.load() #Dll laden und Verwendung des CDLL Objekts
		
		#Verbindung zu Dobot herstellen
		self.__isConnected = self.DobotDLL.ConnectDobot(self.DobotAPI, comPort, 115200)[0]

		print("Connect status of dobot", playerID, CON_STR1[self.__isConnected])

		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Setting up Command Queue")
			self.DobotDLL.SetQueuedCmdClear(self.DobotAPI)                        #Clean Command Queued
			self.DobotDLL.SetQueuedCmdStartExec(self.DobotAPI)                    #Befehlswarteschlange starten

			#print("Setting up line mode")
			#self.DobotDLL.SetDeviceWithL(self.DobotAPI, True)   #Danach kommt ein bool(?) als param


	def Home(self):
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Homing...")    
			self.DobotDLL.SetHOMEParams(self.DobotAPI, 250, 0, 50, 0, isQueued = 1)
			self.DobotDLL.SetHOMECmd(self.DobotAPI, 0, isQueued = 1)

			self.WaitForMotionComplete()
		
		else:
			print("Dobot not connected! Can't home.")


	def MoveTo(self, x: int, y: int, z: int, r: int):
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Moving Dobot", self.__DobotID, "to coordinates", x, y, z, r)

			#TODO add move command
			self.DobotDLL.SetPTPCmdEx(self.DobotDLL, 0, x, y, z, r, isQueued=1)

			self.WaitForMotionComplete()
		
		else:
			print("Dobot not conncted! Can't move.")


	def MoveToInLine(self, x: int, y: int, z: int, r: int):
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Moving Dobot", self.__DobotID, "in a straight line to", x, y, z, r)

			# TODO add move command
			print("Command not implemented")

			self.WaitForMotionComplete()
		
		else:
			print("Dobot not conncted! Can't move.")


	def WaitForMotionComplete(self):
		while (not self.DobotDLL.GetQueuedCmdMotionFinish(self.DobotAPI)[0]):
			print("Waiting for Dobot", self.__DobotID, "... Current 1: ", self.DobotDLL.GetQueuedCmdCurrentIndex(self.DobotAPI))
			self.DobotDLL.dSleep(200)
		pass


	def Disconnect(self):    
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			self.DobotDLL.DisconnectDobot(self.DobotAPI)
			print("Successfully disconnected Dobot", self.__DobotID)
		
		else:
			print("Dobot not conncted! Can't disconnect.")