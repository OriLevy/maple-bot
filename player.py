from interception.stroke import key_stroke
from config import ScanCodes, GeneralKeyBindigs
import time

# Scancodes for arrow and alphanumeric/modifier keys should be separated. They have different key-states.
SC_DECIMAL_ARROW = {k.lower(): v for k, v in ScanCodes.SC_DECIMAL_ARROW.items()}

SC_DECIMAL = {k.lower(): v for k, v in ScanCodes.SC_DECIMAL.items()}

# Change these to your own settings.
JUMP_KEY = GeneralKeyBindigs.jump_key
ROPE_LIFT_KEY = GeneralKeyBindigs.rope_lift_key


class Player:
    def __init__(self, context, device, game):
        self.game = game
        # interception
        self.context = context
        self.device = device

    def release_all(self):
        for key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        for key in SC_DECIMAL:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def press(self, key, repeat=1):
        """
        Mimics a human key-press.
        Delay between down-stroke and up-stroke was tested to be around 50 ms.
        """
        key = key.lower()
        for _ in range(repeat):
            if key in SC_DECIMAL_ARROW:
                self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
                time.sleep(0.05)
                self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
            else:
                self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))
                time.sleep(0.05)
                self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def release(self, key):
        key = key.lower()
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def hold(self, key):
        key = key.lower()
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))

    def go_to(self, target):
        """
        Attempts to move player to a specific (x, y) location on the screen.
        """
        # TODO - work on fine tune controls 
        while True:
            player_location = self.game.get_player_location()
            if player_location is None:
                continue

            x1, y1 = player_location
            x2, y2 = target

            """
            There are delays between taking a screenshot, processing the image, sending the key press, and game server ping.
            Player should be within 2 pixels of x-destination and 7 pixels of y-destination.
            """
            if abs(x1 - x2) < 2:
                # Player has reached target x-destination, release all held keys.
                self.release_all()
                if abs(y2 - y1) < 7:
                    # Player has reached target y-destination, release all held keys.
                    self.release_all()
                    break
                # Player is above target y-position.
                elif y1 < y2:
                    self.hold("DOWN")
                    self.press(JUMP_KEY)
                # Player is below target y-position.
                else:
                    # if target is high up - use rope lift instead of attempting to jump
                    # only if jump rope key is configured
                    if y1 - y2 > 30 and GeneralKeyBindigs.rope_lift_key != None:
                        # use rope lift - TODO
                        self.press(GeneralKeyBindigs.rope_lift_key, 1)
                    else:
                        # first release directional keys
                        for i in ["left", "right"]:
                            self.release(i)
                        # UP JUMP
                        self.press(GeneralKeyBindigs.jump_key)
                        self.hold("up")
                        self.press(GeneralKeyBindigs.jump_key)
                        self.release("up")
                # Delay for player falling down or jumping up.
                time.sleep(1)
            else:
                # Player is to the left of target x-position.
                if x1 < x2:
                    self.hold("RIGHT")
                # Player is to the right of target x-position.
                else:
                    self.hold("LEFT")
                if abs(x2 - x1) > 30:
                    self.press(JUMP_KEY)
                    self.press(JUMP_KEY)
