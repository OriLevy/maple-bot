from player import Player
import time

class Key:
    # BUFFS
    WARD = '1'
    DIABOLIC = '2'
    MAPLE_WARRIOR = '3'
    
    # Skills
    SLASH = "ctrl"
    EXECUTION = "a"
    NETHER_SHIELD = "lshift"
    

class command_book:
    def __init__(self, player):
        self.player = player
    
    def ExceedExecution(self, direction, attacks=2, reps=1):
        time.sleep(0.05)
        self.player.hold(direction)
        for _ in range(reps):
            self.player.press(Key.EXECUTION, attacks)
            time.sleep(0.5)
        self.player.release(direction)
    
    def ExceedLunarSlash(self, reps=1):
        time.sleep(0.05)
        for _ in range(reps):
            self.player.press(Key.SLASH)
            time.sleep(0.5)
    
    def NetherShield(self):
        time.sleep(0.05)
        self.player.press(Key.NETHER_SHIELD)
        time.sleep(0.05)
        
        