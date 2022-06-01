from importlib import import_module

class Wrapper:
	DobotAPI = None
	__DobotID = -1
	__rowAmount = 7
	__isConnected = False

	__moveHeight = 125
	__homeX = 60
	__homeY = -240
	__homeZ = 0
	__cubeZ = -52.2505

	__xCoordinatesOfColumns = {
		0: 200,
		1: 200,
		2: 200,
		3: 200,
		4: 200,
		5: 200,
		6: 200
	}
	__yCorrdinatesOfColumns_mirrored = {
		0: 220,
		1: 100,
		2: 40,
		3: 0,
		4: -40,
		5: -100,
		6: -220
	}
	__zCoordinatesOfColumns = {
		0: -50,
		1: -25,
		2: 0,
		3: 25,
		4: 50,
		5: 75,
		6: 100
	}

	def __init__(self, playerID: int, comPort: str):
		self.__yCorrdinatesOfColumns = {
		0: -220,
		1: -100,
		2: -40,
		3: 0,
		4: 40,
		5: 100,
		6: 220
		}

		self.__DobotID = playerID

		if playerID == 0:
			self.DobotDLL = import_module('Dobot0DLLType')
		else:
			self.DobotDLL = import_module('Dobot1DLLType')
			#Update dictionary to have mirrored y values
			self.__yCorrdinatesOfColumns.update(self.__yCorrdinatesOfColumns_mirrored)

		#Dobot konfigurieren
		CON_STR1 = {
			self.DobotDLL.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
			self.DobotDLL.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
			self.DobotDLL.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

		self.DobotAPI = self.DobotDLL.load()

		#Verbindung zu Dobot herstellen
		self.__isConnected = self.DobotDLL.ConnectDobot(self.DobotAPI, comPort, 115200)[0]
		print("Connect status of dobot", playerID, CON_STR1[self.__isConnected])

		#Test for successfull connection
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Setting up Command Queue")
			#Clean Command Queued
			self.DobotDLL.SetQueuedCmdClear(self.DobotAPI)
			#Befehlswarteschlange starten
			self.DobotDLL.SetQueuedCmdStartExec(self.DobotAPI)
			#Bring Dobot to starting position
#			self.Home()
			self.MoveTo(self.__homeX, self.__homeY, self.__homeZ)
		pass


	def Home(self):
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Homing...")    
			self.DobotDLL.SetHOMEParams(self.DobotAPI, 250, 0, 50, 0, isQueued = 1)
			self.DobotDLL.SetHOMECmd(self.DobotAPI, 0, isQueued = 1)
			self.WaitForMotionComplete()
		else:
			print("Dobot not connected! Can't home.")
		pass


	def MoveTo(self, x: int, y: int, z: int, r=0):
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Moving Dobot", self.__DobotID, "to coordinates", x, y, z, r)
			self.DobotDLL.SetPTPCmdEx(self.DobotAPI, 1, x, y, z, r, isQueued=1)
			self.WaitForMotionComplete()
		else:
			print("Dobot not conncted! Can't move.")
		pass


	def MoveToInLine(self, x: int, y: int, z: int, r: int):
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			print("Moving Dobot", self.__DobotID, "in a straight line to", x, y, z, r)
			self.DobotDLL.SetPTPCmdEx(self.DobotDLL, 2, x, y, z, r, isQueued=1)
			self.WaitForMotionComplete()
		else:
			print("Dobot not conncted! Can't move.")
		pass
	

	def SetSuckState(self, state: bool) -> None:
		if (self.__isConnected == self.DobotDLL.DobotConnect.DobotConnect_NoError):
			conv_state = 0
			if (state):
				conv_state = 1
			self.DobotDLL.SetEndEffectorSuctionCupEx(self.DobotAPI, 1, conv_state)
		else:
			print("Dobot not conncted! Can't set suck state.")
		pass


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
		pass


	def MoveBlock(self, row: int, height: int):
		#Pick up cube
		self.MoveTo(self.__homeX, self.__homeY, self.__cubeZ)
		self.SetSuckState(True)
		self.MoveTo(self.__homeX, self.__homeY, self.__moveHeight)

		#Move cube to the row
		pointTupel = self.__getPointCoordinates(row, height)
		x_mm = pointTupel[0]
		y_mm = pointTupel[1]
		z_mm = pointTupel[2]
		self.MoveTo(x_mm, y_mm, self.__moveHeight)
		self.MoveTo(x_mm, y_mm, z_mm)
		self.SetSuckState(False)
		self.MoveTo(x_mm, y_mm, self.__moveHeight)

		#Move back to home position
		self.MoveTo(self.__homeX, self.__homeY, self.__moveHeight)
		self.MoveTo(self.__homeX, self.__homeY, self.__homeZ)
		pass


	def __getPointCoordinates(self, row: int, height: int) -> (int, int, int):
		x_mm = self.__xCoordinatesOfColumns.get(row)
		y_mm = self.__yCorrdinatesOfColumns.get(row)
		z_mm = self.__zCoordinatesOfColumns.get(height)
		return (x_mm, y_mm, z_mm)