import importlib
from genericpath import *
from os.path import basename, splitext, join
from os import listdir
from pathlib import Path
import traceback
import inspect

REQUIRED_COMMANDS = ['key', 'command_book']

class CommandLoader:
    def __init__(self, p):
        self.player = p
    
    def get_available_command_books(self):
        path = join('resources', 'command_books')
        available_books = [f for f in listdir(path) if isfile(join(path, f))]
        available_books_dir = {index + 1: available_books[index] for index in range(len(available_books))}
        
        for index in available_books_dir:
            print(f"({index}):         {available_books_dir[index]}")
        
        selected_book = None
        while True:
            try:
                selected_book = available_books_dir[int(input("Select command book: "))]
                break
            except:
                print("invalid selection!")
        
        return(str(Path(join('resources', 'command_books', selected_book)).resolve()))
        
    
    def load_command_book(self):
        # TODO - ask for user input
        file = self.get_available_command_books()
        # make sure provided file is a python file
        ext = splitext(file)[1]
        if ext != ".py":
            # not a python file
            print(f"ERROR '{ext}' is not a supported file extension for a command book.")
            return False
        
        new_cb = {}
        # import desired command book file
        module_name = splitext(basename(file))[0]
        target_file = '.'.join(['resources', 'command_books', module_name])
        try:
            module = importlib.import_module(target_file)
            module = importlib.reload(module)
        except ImportError: # display errors while loading requested command book
            print(' !  Errors during compilation:\n')
            for line in traceback.format_exc().split('\n'):
                line = line.rstrip()
                if line:
                    print(' ' * 4 + line)
            print(f"\n !  Command book '{module_name}' was not loaded")
            return False
        
        # Populate the new command book
        for name, command in inspect.getmembers(module, inspect.isclass):
            new_cb[name.lower()] = command
        
        for i in REQUIRED_COMMANDS:
            if i not in new_cb.keys():
                print(f"ERROR      command book is missing required command '{i}'")
                return False
            
        # return the command book moudle iniated with the player Object
        return(module.command_book(self.player))
    