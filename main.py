import sys
sys.path.append('./lib')
sys.path.append('./src')

from Game import Game

if __name__=='__main__':
	game = Game()

	game.initialize()
	game.run_game()