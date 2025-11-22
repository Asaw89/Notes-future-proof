import sys
import os
import yaml
import tempfile
import subprocess
from Configurator import ROOT_FOLDER
from collections import Counter
from datetime import datetime


class Note():
    def __init__(self, title, content, tags=None, author=None, status=None, priority=None):#constructor
        self.title = title
        self.content = content
        self.tags = tags if tags else []
        self.author = author
        self.status= status
        self.priority = priority
        self.created = datetime.now().isoformat() + 'Z'
        self.modified = datetime.now().isoformat() + 'Z'

    def save(self,filename): #We need to take the information the user gave us and save it as a properly formatted note file with YAML metadata.
        self.modified = datetime.now().isoformat() + 'Z'#Use datetime to get the current time and save it to ISO format 'Z' shows UTC time
        metadata = {
            'title': self.title,
            'created': self.created,
            'modified': self.modified,
            'tags': self.tags
            }
        yaml_string = yaml.dump(metadata)#convert to YAML by going from dictionary -> YAML
        full_content = '---' + yaml_string + '---' + self.content #We construct the contents together like Lego Blocks. Kris suggested '---' to make YAMLs look nice.

        with open(f'{ROOT_FOLDER}/{filename}.note', 'w') as f:#Creates the file path and Writes it
            f.write(full_content)# Writes YAML + Content

    @classmethod #Needed, because load _note does not use a regular "method".It CREATES a new Note Instance from FILE
    def load_note(cls,filepath):#This function reads a note file and separates it into two parts: the information ABOUT the note, and the actual note content
        with open(filepath, 'r') as file:
            content = file.read() #We grab piece 1 (the metadata) and piece 2 (the content). We use .strip() to remove any extra spaces or blank lines from the content.
            parts = content.split('---')#splits the content into pieces
            yaml_part = parts[1]#the meta data between the dashes
            content_part = parts[2].strip()#displays the actual content

            metadata = yaml.safe_load(yaml_part)#Converts YAML text into a python Dictionary, so python can read the file.

            note = cls(#cls = "the class itself" a "note factory"
                title = metadata['title'],
                content = content_part,
                tags = metadata.get('tags', []),
                author=metadata.get('author'),
                status=metadata.get('status'),
                priority=metadata.get('priority')

    )

        note.created = metadata['created']
        note.modified = metadata ['modified']

        return note

    def update(self,title=None, content=None,tags=None ):#update note fields
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        if tags is not None:
            self.tags=tags

        self.modified = datetime.now().isoformat() + 'Z'

    def to_dict(self): #Return note as a dictionary
        return {
        'metadata': {
            'title': self.title,
            'created': self.created,
            'modified': self.modified,
            'tags': self.tags,
            'author': self.author,
            'status': self.status,
            'priority': self.priority
        },
        'content': self.content
    }

class Notebook():

    def __init__(self, notes_folder): #constructor
        self.notes_folder = notes_folder

    def list_notes(self):
        files = os.listdir(self.notes_folder)
        notes = [f for f in files if f.endswith('.note')]
        return notes

    def get_note(self, filename):
        filepath = f'{self.notes_folder}/{filename}'
        return Note.load_note(filepath)

    def search_notes(self, query):
        files = self.list_notes()
        matching_files = []
        query_words = query.lower().split() #split query into individual keywords

        for file in files:
            try:
                note = Note.load_note(f'{self.notes_folder}/{file}')

                title=note.title.lower()
                tags_string=''.join(note.tags).lower()
                content=note.content.lower()

                searchable_text = f"{title} {tags_string} {content}" #searchable keywords

                found=False
                for word in query_words:
                    if word in searchable_text:
                        found=True
                        break
                if found:
                    matching_files.append(file)
            except Exception:
                pass

        return matching_files

    def delete_note(self, filename):
        filepath = f'{self.notes_folder}/{filename}.note'
        os.remove(filepath)

    def get_stats(self):
        files = self.list_notes()
        total_notes = len(files)
        all_tags = []

        for file in files:
            try:
                note = Note.load_note(f'{self.notes_folder}/{file}')
                all_tags.extend(note.tags)
            except Exception:
                pass

        total_tags = len(set(all_tags))

        return {
            'total_notes': total_notes,
            'total_tags': total_tags,
            'all_tags': all_tags
        }

class Application():

    def __init__(self, notebook): #Constructor
        self.notebook = notebook

    def create_note_input(self): #Create a temporary file with a random name, file ends with.txt. Put a helpful comment in the file so its not empty
        filename= input('Enter note filename:')
        title= input('Enter title:')

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write("# Enter your note content below (you can delete this line)")

        print("Opening nano for content entry...")#Opens up before nano
        print("Instructions:")
        print("  - Type your note content")
        print("  - Save: Ctrl+O, then press Enter")
        print("  - Exit: Ctrl+X")
        input("Press Enter when ready")

        subprocess.call(['nano', temp_path])#runs another program(nano) from Python. Command:"nano/tmp/tmpxyz123.txt"

        with open(temp_path,'r') as f:
            content=f.read().strip()

        os.remove(temp_path)

        tags_input=input('Enter tags (comma-separated, or press enter to skip):')
        author = input('Enter author (or press Enter to skip):').strip() or None #the .strip() or None is used to add optional variables
        status = input('Enter status (or press Enter to skip):').strip() or None
        priority = input('Enter priority(or press Enter to skip):').strip() or None

        if tags_input.strip():#Parse the tags
            tags = [tag.strip() for tag in tags_input.split(',')]
        else:
            tags = []

        return filename, title, content, tags, author, status, priority

    def display_menu(self):
        print("==== Notes Manager ====")
        print("1. List notes")
        print("2. Create note")
        print("3. Go to note")
        print("4. Edit note")
        print("5. Search note")
        print("6. Delete note")
        print("7. Stats")
        print("8. Help")
        print("9. Exit")
        print("====================")

    def handle_list(self):  # Separate method
        files = self.notebook.list_notes()  # Use self.notebook
        files.sort(key=str.lower) #key= tells sort: "Before comparing, transform each item using this function"
        print("Your notes:")
        for file in files:
            print(f"  - {file}")
        input("Press Enter to return to menu...")

    def handle_create(self):
        filename, title, content, tags, author, status, priority = self.create_note_input()

        # Create a Note object
        note = Note(title, content, tags, author, status, priority)
        note.save(filename)

        print(f"Note '{filename}.note' created successfully!")
        input("Press Enter to return to menu...")

    def handle_read(self):
        files = self.notebook.list_notes()#Stored in files List
        files.sort(key=str.lower) #sorts the files alphabetically
        if not files: #if there are no notes
            print("No notes found!")
            input("Press Enter to return to menu...")
        else:
            print("Available notes:")
            for i, file in enumerate(files, 1): #gives us each file number
                print(f"  {i}. {file}")

            note_choice = input("Enter note number to read: ") #user inputs choice
            try:
                index = int(note_choice) - 1 #convert the string into an integer
                if 0 <= index < len(files):
                    note = self.notebook.get_note(files[index])
                    print(f"--- {note.title} ---")
                    print(f"Created: {note.created}")
                    print(f"Tags: {note.tags}")
                    print(f"{note.content}")
                    input("Press Enter to return to menu...")
                else:
                    print("Invalid note number!")
                    input("Press Enter to return to menu...")
            except ValueError: #validate the numbers
                print("Please enter a valid number!")
                input("Press Enter to return to menu...")

    def handle_edit(self):
        files = self.notebook.list_notes()
        files.sort(key=str.lower) #key= tells sort: "Before comparing, transform each item using this function"
        if not files:
            print("No notes found!")
            input("Press Enter to return to menu...")
        else:
            print("Available notes:")
            for i, file in enumerate(files, 1):
                print(f"  {i}. {file}")

            note_choice = input("Enter note number to edit: ")
            try:
                index = int(note_choice) - 1
                if 0 <= index < len(files):
                    filepath = f'{self.notebook.notes_folder}/{files[index]}'

                # Open the actual file in nano
                    print(f"Opening {files[index]} in nano...")
                    print("Instructions:")
                    print("  - Edit your note content")
                    print("  - Save: Ctrl+O, then press Enter")
                    print("  - Exit: Ctrl+X")
                    input("Press Enter when ready")
                    subprocess.call(['nano', filepath])

                    print(f"Note '{files[index]}' updated successfully!")
                else:
                    print("Invalid note number!")
            except ValueError:
                print("Please enter a valid number!")
        input("Press Enter to return to menu...")

    def handle_search(self):
        query = input("Enter search term: ")
        results = self.notebook.search_notes(query)
        results.sort(key=str.lower) #key= tells sort: "Before comparing, transform each item using this function"

        if not results:
            print(f"No notes found matching '{query}'")
        else:
            print(f"Found {len(results)} note(s) matching '{query}':")
            for i, file in enumerate(results,1):
                print(f"  {i}. {file}")
            print("What would you like to do?")
            print("1. Read note")
            print("2. Edit note")
            print("3. Return to main menu")

            action = input("Select an option (1-3):")

            if action == '1': #Reads the note from result
                note_choice=input("Enter note number to read:")
                try:
                    index=int(note_choice)-1
                    if 0 <= index < len(results):
                        note = self.notebook.get_note(results[index])
                        print(f"---{note.title}---")
                        print(f"created;{note.created}")
                        print(f"Tags:{note.tags}")
                        print(f"{note.content}")
                    else:
                        print("Invalid note number")
                except ValueError:
                    print("Please enter a valid number")

            elif action == '2':  # Edit a note from results
                note_choice = input("Enter note number to edit: ")
                try:
                    index = int(note_choice) - 1
                    if 0 <= index < len(results):
                        filepath = f'{self.notebook.notes_folder}/{results[index]}'
                        print(f"Opening {results[index]} in nano...")
                        print("Instructions:")
                        print("  - Edit your note content")
                        print("  - Save: Ctrl+O, then press Enter")
                        print("  - Exit: Ctrl+X")
                        input("Press Enter when ready")
                        subprocess.call(['nano', filepath])

                        print(f"Note '{results[index]}' updated successfully!")
                    else:
                        print("Invalid note number!")
                except ValueError:
                    print("Please enter a valid number!")



    def handle_delete(self):
        files = self.notebook.list_notes()
        files.sort(key=str.lower) #key= tells sort: "Before comparing, transform each item using this function"
        if not files: #If no files are found
            print("No notes found!")
            input("Press Enter to return to menu...")
        else:
            print("Available notes:")
            for i, file in enumerate(files, 1):#Gives us the file number
                print(f"  {i}. {file}")

            note_choice = input("Enter note number to delete: ")
            try:
                index = int(note_choice) - 1 #finds the note number
                if 0 <= index < len(files): #convert and adjust, because indexes
                    filename = files[index].replace('.note', '') #Removes the note extension
                    confirm = input(f"Are you sure you want to delete '{filename}.note'? (y/n): ")
                    if confirm.lower() == 'y':#add .lower so user can type in whatever they want.
                        self.notebook.delete_note(filename)#Actually removes the file
                        print(f"Note '{filename}.note' deleted successfully!")
                    else:
                        print("Deletion cancelled.")
                else:
                    print("Invalid note number!")
            except ValueError:#make sure the user enters in the right numbers
                print("Please enter a valid number!")
            input("Press Enter to return to menu...")

    def handle_stats(self):
        stats = self.notebook.get_stats()
        print("===Note Statistics===")
        print(f"Total Notes: {stats['total_notes']}")
        print(f"Unique tags: {stats['total_tags']}")
        if stats['all_tags']:
            tag_counts = Counter(stats['all_tags'])
            top_tags = tag_counts.most_common(10)
            print("Top 10 most used tags:")
            for tag, count in top_tags:
                print(f' {tag}: {count} notes')

        input("Press Enter to return to menu...")

    def handle_help(self):
        print("=== Notes Manager Help ===")
        print("Welcome to the Notes App")
        print("Available commands:")
        print("  1. List notes   - View all your notes")
        print("  2. Create note  - Create a new note")
        print("  3. Read note    - Display a specific note")
        print("  4. Edit note    - Modify an existing note")
        print("  5. Search notes - Finds a note")
        print("  6. Delete note  - Removes a note")
        print("  7. Stats        - Views statistics")
        print("  8. Help         - Show this help")
        print("  9. Exit         - Quit the application")
        input("Press Enter to return to menu...")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select an option (1-9): ")#Handles User inputs

            if choice == '1':
                self.handle_list()
            elif choice == '2':
                self.handle_create()
            elif choice == '3':
                self.handle_read()
            elif choice == '4':
                self.handle_edit()
            elif choice == '5':
                self.handle_search()
            elif choice == '6':
                self.handle_delete()
            elif choice == '7':
                self.handle_stats()
            elif choice == '8':
                self.handle_help()
            elif choice == '9':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-9.")

if __name__ == '__main__':
    notebook = Notebook(ROOT_FOLDER)#calls back to the configurator
    app = Application(notebook)#Creates the new instance with __int__
    app.run()






