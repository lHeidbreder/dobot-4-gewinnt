import sys
sys.path.append('./lib')
sys.path.append('./src')

from src.Wrapper import Wrapper

Dobot1 = Wrapper(0, "COM6")
Dobot2 = Wrapper(1, "COM7")

Dobot1.Disconnect()