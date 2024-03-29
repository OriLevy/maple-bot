import time
import random
from rune_solver import find_arrow_directions
from interception import *
from game import Game
from player import Player
from config import PetSettings, GeneralKeyBindigs, StartStopControl
from command_controller import CommandLoader
import itertools
from event_listener import KeyboardListener


def bind(context):
    context.set_filter(interception.is_keyboard, interception_filter_key_state.INTERCEPTION_FILTER_KEY_ALL.value)
    print("Click any key on your keyboard.")
    device = None
    while True:
        device = context.wait()
        if interception.is_keyboard(device):
            print(f"Bound to keyboard: {context.get_HWID(device)}.")
            c.set_filter(interception.is_keyboard, 0)
            break
    return device

def solve_rune(g, p, target):
    """
    Given the (x, y) location of a rune, the bot will attempt to move the player to the rune and solve it.
    """
    while True:
        print("Pathing towards rune...")
        p.go_to(target)
        # Activate the rune.
        time.sleep(1)
        p.press(GeneralKeyBindigs.interact_key)
        # Take a picture of the rune.
        time.sleep(1)
        img = g.get_rune_image()
        print("Attempting to solve rune...")
        directions = find_arrow_directions(img)
        print(f"directions : {directions}")

        if len(directions) == 4:
            print(f"Directions: {directions}.")
            for d, _ in directions:
                p.press(d)

            # The player dot will be blocking the rune dot, attempt to move left/right to unblock it.
            p.hold("LEFT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("LEFT")

            p.hold("RIGHT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("RIGHT")

            rune_location = g.get_rune_location()
            if rune_location is None:
                print("Rune has been solved.")
                break
            else:
                print("Trying again...")
        
        else:
            print("could not solve rune.")


if __name__ == "__main__":
    # This setup is required for Interception to mimic your keyboard.
    c = interception()
    d = bind(c)
    g = Game((5, 60, 180, 130))
    p = Player(c, d, g)
    cl = CommandLoader(p)
    commands = cl.load_command_book()
    routine = cl.build_routine()
    keyboard_listener = KeyboardListener(p)
    keyboard_listener.start()

    last_fed = time.time()
    for command in itertools.cycle(routine):
        if keyboard_listener.enabled:
            #print(g.get_player_location())
            # main bot body
            other_player_location = g.get_other_location()
            if other_player_location > 0:
                print("A player has entered your map.")

            rune_location = g.get_rune_location()
            if rune_location is not None:
                print("A rune has appeared.")
                solve_rune(g, p, rune_location)
            
            if PetSettings.autofeed and time.time() - last_fed > 600 / PetSettings.num_of_pets:
                p.press(PetSettings.petfood_key)

            #print(g.get_player_location())
            eval(command)
        
        
        
        
        
        

        
        
        
        

    
