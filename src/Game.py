import sys
import typing
from Controller import Controller
from Wrapper import Wrapper

class Game:
    def __init__(self) -> None:
        self.players = []
        self.__robots:typing.List(Wrapper) = []
        self.gamestate:typing.List(typing.List) = []

    def initialize(self) -> None:
        if (len(sys.argv) < 3):
            raise SyntaxError("Needs 2 command line arguments")

        self.players.append(Controller.getController(sys.argv[1]))
        self.players.append(Controller.getController(sys.argv[2]))
        self.__robots.append(Wrapper(0, "COM6"))
        self.__robots.append(Wrapper(1, "COM8"))

        l = []
        for i in range(7):
            l.append([])
            for j in range(6):
                l[i].append(0)

        self.gamestate = l

    def _determine_victory(self, last_col:int, last_row:int) -> int:
        #check col if necessary
        if (last_row >= 3):
            if self.gamestate[i][last_row] > 0 \
                and self.gamestate[last_col][last_row] \
                == self.gamestate[last_col][last_row-1] \
                == self.gamestate[last_col][last_row-2] \
                == self.gamestate[last_col][last_row]:
                return self.gamestate[last_col][last_row]
        
        #check row
        for i in range(4):
            if self.gamestate[i][last_row] > 0 \
                and self.gamestate[i][last_row] \
                == self.gamestate[i+1][last_row] \
                == self.gamestate[i+2][last_row] \
                == self.gamestate[i+3][last_row]:
                return self.gamestate[last_col][last_row]

        #check diagonal
        #from bottom left
        offset:int = min(last_row, last_col)
        start = last_col - offset, last_row - offset
        if (start[0] < 4 and start[1] < 4):
            for i in range(max(last_row,last_col),4):
                if self.gamestate[start[0]+i][start[1]+i] \
                    == self.gamestate[start[0]+i+1][start[1]+i+1] \
                    == self.gamestate[start[0]+i+2][start[1]+i+2] \
                    == self.gamestate[start[0]+i+3][start[1]+i+3]:
                    return self.gamestate[last_col][last_row]

        #from bottom right
        offset:int = min(last_row, last_col)
        start = last_col - offset, last_row + offset
        if (start[0] < 4 and start[1] > 2):
            for i in range(max(start[0], 6-start[1]), 4):
                if self.gamestate[start[0]+i][start[1]-i] \
                    == self.gamestate[start[0]+i+1][start[1]-i-1] \
                    == self.gamestate[start[0]+i+2][start[1]-i-2] \
                    == self.gamestate[start[0]+i+3][start[1]-i-3]:
                    return self.gamestate[last_col][last_row]

        return 0

    def run_game(self) -> None:
        victor = 0
        while victor==0:
            col:int = self.players[0].getNextTurn(1, self.gamestate)

            row = self.gamestate[col].index(0)
            self.gamestate[col][row] = 1
            self.__robots[0].MoveBlock(col, row)
            
            victor = self._determine_victory(col,row)
            if victor != 0:
                break

            col:int = self.players[1].getNextTurn(2, self.gamestate)

            row = self.gamestate[col].index(0)
            self.gamestate[col][row] = 2
            self.__robots[0].MoveBlock(col, row)
            
            victor = self._determine_victory(col,row)

        for i in len(self.players):
            self.players[i].informEnd(victor == i)