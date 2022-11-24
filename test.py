from os import listdir
from os.path import isfile, join
from pathlib import Path

def get_available_command():
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
        

print(get_available_command())
