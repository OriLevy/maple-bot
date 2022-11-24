from player import Player
import time

class Key:
    # BUFFS
    CALL_OF_CYGNUS = '1'
    GLORY_OF_THE_GUARDIANS = '2'
    SPEED_INFUSION = '3'
    
    # Skills
    SOLAR = "ctrl"
    EQUNIOX = "lshift"
    

class command_book:
    def __init__(self, player):
        self.player = player
    
    def SolarSlashLunaDivide(self, direction, attacks=2, reps=1):
        time.sleep(0.05)
        self.player.hold(direction)
        for _ in range(reps):
            self.player.press(Key.SOLAR)
            time.sleep(0.5)
        self.player.release(direction)

    def EquinoxSlash(self, direction):
        time.sleep(0.05)
        self.player.hold(direction)
        self.player.press(Key.SOLAR, 3)
        self.player.release(direction)
        