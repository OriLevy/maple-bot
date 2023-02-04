"""
listens for keyboard events to start and stop the routine
"""
from pynput import keyboard

class KeyboardListener:
    key_bindings = {
        'start/stop' : keyboard.Key.f10,
        'eme_stop' : keyboard.Key.f12
    }
    def __init__(self, player=None):
        self.player = player
        self.enabled = False
        self.listener = keyboard.Listener(on_press=self._main)
    
    def start(self):
        print("Started Keyboard Listener")
        self.listener.start()
    
    def _main(self, key):
        if key == self.key_bindings['start/stop']:
                if self.enabled:
                    # release all keys before stopping
                    self.player.release_all()
                
                self.enabled = not self.enabled
                self.print_state(str(self.enabled))
        
        elif key == self.key_bindings['eme_stop']:
            self.player.release_all()
            exit()
    
    @staticmethod
    def print_state(state: str):
        print("#####################")
        print(f"####  {state.upper()} ####")
        print("#####################")
        