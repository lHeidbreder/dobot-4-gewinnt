# Vier Gewinnt Minimax
from ast import Pass
from pickle import NONE
from typing import List
from random import randint
import copy
import PySimpleGUI as sg



class Controller:
  def __init__(self):
    pass
  
  @staticmethod
  def getController(name:str):
    if name == 'ai':
      raise NotImplementedError('There is no AIController implemented yet')
    return GUIController(name)

  def getName(self) -> str:
    '''Return this Controller's name'''
    raise NotImplementedError()
  
  def getNextTurn() -> int:
    '''Return a column index where to put the next block'''
    raise NotImplementedError()


class AIController(Controller):

  WIN_POINTS:int = 100
  LOSS_POINTS:int = -100
  
  def __init__(self):
    super()
    self._name = 'AI' #TODO: make random
  
  def getName(self):
    return self._name
  
  def getNextTurn(self, gamestate:List[List[int]], controller_id:int) -> int:
    '''Return a column index where to put the next block'''
    column:int = 0
    best_value:int = AIController.LOSS_POINTS
    for i in range(len(gamestate)):
      newstate = copy.deepcopy(gamestate)
      newstate[i].append(controller_id)
      value = self._getTurnViability(newstate, controller_id)
    
      # if this is a winning move, just do it
      if value == AIController.WIN_POINTS:
        return i
    
      # if this is better than the previous best, it becomes the best
      print(value)
      if value > best_value:
          best_value = value
          column = i
  
    return column

  def _getTurnViability(self, gamestate:List[List[int]], controller_id: int, search_depth:int = 1) -> int:
    '''Return a value between WIN_POINTS and LOSS_POINTS representing the given turn's viability'''
    rtn:int = randint(AIController.LOSS_POINTS, AIController.WIN_POINTS) #0
    #rtn:int = test() #FS Lib connection
    
    #TODO: do work
    return rtn


class GUIController(Controller):
  

  def __init__(self, name):
    super()
    self.name = name
    self.window = Window.Instance()
  
  def getName(self) -> str:
    return self._name
  
  def getNextTurn(self, playerId, gamestate: List[List[int]]) -> int:
    #TODO
    self.window.updateState(gamestate)
    return self.window.WaitButtonClicked(playerId)
  
  def informEnd(self, victor):
    sg.Popup('Der Gewinner ist' + str(victor), title = "Spielende")
    self.window.close()
    

class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)  

@Singleton
class Window:
  gameboard = []
  def __init__(self):
    self.window = self.__initWindow()

  def __initWindow(self) -> sg.Window:
    
    buttons = []
    for i in range(7):
      buttons.append(sg.Button(str(i), size=(2,None)))
    for i in range(6):
      self.gameboard.append([])
      for j in range(7):
        self.gameboard[i].append(sg.Text(size=(2,None),pad=7, background_color= "white", key = "Field"))
    layout = [[self.gameboard], [buttons]]
    
    return sg.Window("Game", layout, finalize=True)

  def updateState(self, gamestate: List[List[int]]):
    color_map = {0:"white", 1:"blue", 2:"red"}
    for i in range(len(self.gameboard)):
      for j in range(len(self.gameboard[i])):
        self.gameboard[5-i][j].update(background_color = color_map[gamestate[j][i]])


  def WaitButtonClicked(self, playerId) -> int:
    color_map = {1:"blue", 2:"red"}
    column = 0
    while True:             # Event Loop
      event, values = self.window.Read()
      for i in range(7):
        if event == str(i):
          column = i
          for j in range(6):
            if self.gameboard[5-j][i].Widget['background'] == "white":
              self.gameboard[5-j][i].update(background_color= color_map[playerId])
              break
          break
      if event == sg.WIN_CLOSED:
        self.window.close()
        break
      return column

    #for l in state:
     # print(l)