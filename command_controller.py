import importlib
from genericpath import *
from os.path import basename, splitext, join
from os import listdir, mkdir
from pathlib import Path
import traceback
import inspect
import csv

REQUIRED_COMMANDS = ['key', 'command_book']

class CommandLoader:
    def __init__(self, p):
        self.player = p
        self.module_name = None

    def get_available_routines_and_select(self):
        # return the complete file path of the selected routine
        # will allow user to choose between routines within a folder
        # that matches the loaded command book
        path = join('resources', 'routines', self.module_name)
        available_routines = None
        try:
            available_routines = [f for f in listdir(path) if isfile(join(path, f))]
        except FileNotFoundError:
            # the specified dir doesn't exist. this probably means that the seleceted command book has no
            # routines available for it.
            # force the creation of the requsted dir and continue.
            mkdir(path)
        if not available_routines:
            # no routines available for the selected command book
            print(f"ERROR      selected command book {self.module_name} has no routines.")
            exit()
        available_routines_dir = {index + 1: available_routines[index] for index in range(len(available_routines))}
        for index in available_routines_dir:
            print(f"({index}):         {available_routines_dir[index]}")
        
        selected_routine = None
        while True:
            try:
                selected_routine = available_routines_dir[int(input("Select command book: "))]
                break
            except:
                print("invalid selection!")
        
        return(str(Path(join('resources', 'routines', self.module_name, selected_routine)).resolve()))


    def build_routine(self):
        file = self.get_available_routines_and_select()
        # make sure provided file is a csv file
        ext = splitext(file)[1]
        if ext != ".csv":
            # not a python file
            print(f"ERROR '{ext}' is not a supported file extension for a routine.")
            return False
        routine = []
        with open(file, "r") as r_file:
            csvreader = csv.reader(r_file)
            for row in csvreader:
                # if any white spaces were loaded - remove them
                while "" in row:
                    row.remove("")
                
                new_command = ""
                # begin analysing new command
                # first index will always indicate the type of the command
                if row[0] == "*":
                    # this is a new point to move too
                    # TODO - make sure index 1 and 2 contain numrical values
                    new_command += f"p.go_to(({row[1]}, {row[2]}))"
                
                elif row[0] == "#":
                    # this is a comment - ignore line
                    continue

                elif row[0] == "-":
                    # this is an action to perform
                    new_command += f"commands.{row[1]}("
                    command_params = row[2:] # paramters to pass to the command function
                    for param in command_params:
                        new_command += f"{param}, "
                    new_command = new_command[:len(new_command) - 2] + ")"
                
                else:
                    print(f"ERROR  while loading routine - unkown command type {row[0]}")
                routine.append(new_command)
            r_file.close()

        return(routine)
    
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
        
        # set module name to the selected command_book name
        self.module_name = selected_book[:selected_book.index(".py")]
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
    