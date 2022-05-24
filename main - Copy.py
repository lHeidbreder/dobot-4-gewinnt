import sys, time, asyncio
sys.path.append('./lib')
sys.path.append('./src')

from wrapper import DobotWrapper


if __name__ == '__main__':
    bot = DobotWrapper("COM6",False,False)
    time.sleep(3)
    bot2 = DobotWrapper("COM7",False,False)
    time.sleep(3)

    if not (bot.connect() and bot2.connect()):
        print(4711)
        exit(4711)
       
    asyncio.ensure_future(bot.moveRight(80))
    asyncio.ensure_future(bot2.moveLeft(80))


    loop = asyncio.get_event_loop()
    loop.run_forever()

    time.sleep(9)
    print(bot.getConnectionState())