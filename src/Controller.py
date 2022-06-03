# Vier Gewinnt Minimax
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
    self.window.__updateState(gamestate)
    return self.window.WaitButtonClicked(playerId)

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
  gameboard = [[]]
  def __init__(self):
    self.window = self.__initWindow()

  def __initWindow(self) -> sg.Window:
    textFields = []
    c0 = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []
    buttons = []
    for i in range(7):
      buttons.append(sg.Button(str(i), size=(2,None), key = "buttons"))
    for i in range(7):
      textFields.append(sg.Text(str(0), size=(2,None),pad=7, key = "text"))
    column = [textFields]
    for i in range(7):
      c0.append(sg.Text(size=(2,None),pad=7, background_color= "white", key = "Field"))
      c1.append(sg.Text(size=(2,None),pad=7, background_color= "white", key = "Field"))
      c2.append(sg.Text(size=(2,None),pad=7, background_color= "white", key = "Field"))
      c3.append(sg.Text(size=(2,None),pad=7, background_color= "white", key = "Field"))
      c4.append(sg.Text(size=(2,None),pad=7, background_color= "white", key = "Field"))
      c5.append(sg.Text(size=(2,None),pad=7, background_color= "white", key = "Field"))

    gameboard = [c5,c4,c3,c2,c1,c0]
    layout = [[gameboard], [buttons], [sg.Column(column, vertical_alignment='left', justification='left',  k='-C-')],[sg.Button("exit", size=(3,None))]]
    
    return sg.Window("Game", layout, finalize=True)

  def __updateState(self, gamestate: List[List[int]]):
    color_map = {0:"white", 1:"blue", 2:"red"}
    for i in range(6):
      for j in range(7):
        self.gameboard[i][j].update(background_color= color_map[gamestate[i][j]])


  def WaitButtonClicked(self, playerId) -> int:
    color_map = {1:"blue", 2:"red"}
    column = 0
    while True:             # Event Loop
      event, values = self.window.Read()
      for j in range(7):
        if event == str(j):
          column = j
          #print(i)    #wrapper Move Methode hier
          self.textFields[j](str(int(self.textFields[j].get()) + 1))
          for i in range(6):
            if self.gameboard[5-i][j].Widget['background'] == "white":
              self.gameboard[5-i][j].update(background_color= color_map[playerId])
              break
          break
      if event == sg.WIN_CLOSED or event == "exit":
        break
      return column

    #for l in state:
     # print(l)