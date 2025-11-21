import sys
import os
import yaml
from Configurator import ROOT_FOLDER
from datetime import datetime


#still being used in Notebook.search_notes(line 95)
#Still being used in Notebook.get_stats(line 119)

#read_notes returns a dictionary with the meta data

def read_note(n): #This function reads a note file and separates it into two parts: the information ABOUT the note, and the actual note content
    with open(n, 'r') as file:
        content = file.read()
#We grab piece 1 (the metadata) and piece 2 (the content). We use .strip() to remove any extra spaces or blank lines from the content.
    parts = content.split('---')
    yaml_part = parts[1]
    content_part = parts[2].strip() #

    metadata = yaml.safe_load(yaml_part)

    return {
        'metadata': metadata,
        'content': content_part
    }


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
        full_content = '---\n' + yaml_string + '---\n\n' + self.content #We construct the contents together like Lego Blocks. Kris suggested '---' to make YAMLs look nice.

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
                result = read_note(f'{self.notes_folder}/{file}')
                title = result['metadata'].get('title', '').lower()
                tags = result['metadata'].get('tags', [])
                tags_string = ' '.join(tags).lower()
                content = result['content'].lower()

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
                result = read_note(f'{self.notes_folder}/{file}')
                tags = result['metadata'].get('tags', [])
                all_tags.extend(tags)
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

    def collect_note_input(self):
        filename = input('Enter note filename:')
        title = input('Enter title:')
        content = input('Enter note content:')
        tags_input = input('Enter tags(comma-separated, or press Enter to skip):')
        author = input('Enter author (or press Enter to skip): ').strip() or None
        status = input('Enter status(or press Enter to skip): ').strip() or None
        priority = input('Enter priority(or press Enter to skip): ').strip() or None

        if tags_input.strip():  # split by commas and clean up spaces around each tag
            tags = [tag.strip() for tag in tags_input.split(',')]
        else:
            tags = []
        return filename, title, content, tags,author, status, priority

    def display_menu(self):
        print("\n=== Notes Manager ===")
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
        print("\nYour notes:")
        for file in files:
            print(f"  - {file}")
        input("\nPress Enter to return to menu...")

    def handle_create(self):
        filename, title, content, tags, author, status, priority = self.collect_note_input()

        # Create a Note object
        note = Note(title, content, tags, author, status, priority)
        note.save(filename)

        print(f"\nNote '{filename}.note' created successfully!")
        input("\nPress Enter to return to menu...")

    def handle_read(self):
        files = self.notebook.list_notes()#Stored in files List
        if not files: #if there are no notes
            print("\nNo notes found!")
            input("\nPress Enter to return to menu...")
        else:
            print("\nAvailable notes:")
            for i, file in enumerate(files, 1): #gives us each file number
                print(f"  {i}. {file}")

            note_choice = input("\nEnter note number to read: ") #user inputs choice
            try:
                index = int(note_choice) - 1 #convert the string into an integer
                if 0 <= index < len(files):
                    note = self.notebook.get_note(files[index])
                    print(f"\n--- {note.title} ---")
                    print(f"Created: {note.created}")
                    print(f"Tags: {note.tags}")
                    print(f"\n{note.content}")
                    input("\nPress Enter to return to menu...")
                else:
                    print("\nInvalid note number!")
                    input("\nPress Enter to return to menu...")
            except ValueError: #validate the numbers
                print("\nPlease enter a valid number!")
                input("\nPress Enter to return to menu...")

    def handle_edit(self):
        files = self.notebook.list_notes()
        if not files: #if no files found
            print("\nNo notes found!")
            input("\nPress Enter to return to menu...")
        else:
            print("\nAvailable notes:")
            for i, file in enumerate(files, 1): #gives file numbers
                print(f"  {i}. {file}")

            note_choice = input("\nEnter note number to edit: ")
            try:
                index = int(note_choice) - 1
                if 0 <= index < len(files):
                    filename = files[index].replace('.note', '')

                    # Load the note using Note class
                    note = self.notebook.get_note(files[index])

                    # Show the current content
                    print(f"\nCurrent title: {note.title}")
                    print(f"Current content: {note.content[:50]}...")
                    print(f"Current tags: {note.tags}")

                    # Get the new values
                    new_title = input("\nEnter new title (or press Enter to keep current): ")
                    new_content = input("Enter new content (or press Enter to keep current): ")
                    new_tags = input("Enter new tags (comma-separated, or press Enter to keep current): ")

                    # Parse input
                    title = new_title if new_title.strip() else None
                    content = new_content if new_content.strip() else None
                    tags = [tag.strip() for tag in new_tags.split(',')] if new_tags.strip() else None

                    # Update and save
                    note.update(title=title, content=content, tags=tags)
                    note.save(filename)
                    print(f"\nNote '{filename}.note' updated successfully!")
                else:
                    print("\nInvalid note number!")
            except ValueError:
                print("\nPlease enter a valid number!")
            input("\nPress Enter to return to menu...")

    def handle_search(self):
        query = input("\nEnter search term: ")
        results = self.notebook.search_notes(query)

        if not results:
            print(f"\nNo notes found matching '{query}'")
        else:
            print(f"\nFound {len(results)} note(s) matching '{query}':")
            for i, file in enumerate(results,1):
                print(f"  {i}. {file}")
            print("\What would you like to do?")
            print("1. Read note")
            print("2. Edit note")
            print("3. Return to main menu")

            action = input("n\Select an option (1-3):")

            if action == '1': #Reads the note from result
                note_choice=input("\nEnter note number to read:")
                try:
                    index=int(note_choice)-1
                    if 0 <= index < len(results):
                        note = self.notebook.get_note(results[index])
                        print(f"---{note.title}---")
                        print(f"created;{note.created}")
                        print(f"Tags:{note.tags}")
                        print(f"{note.content}")
                    else:
                        print("\nInvalid note number")
                except ValueError:
                    print("\nPlease enter a valid number")

            elif action == '2':#Edit a note from result
                note_choice=input("Enter note number to edit:")
                try:
                    index=int(note_choice)-1
                    if 0 <= index < len(results):
                        filename = results[index].replace('.note', '')
                        note = self.notebook.get_note(results[index])
                        print(f"Current title:{note.title}")
                        print(f"Current content:{note.content[:50]}...")#[:50 is for the preview]
                        print(f"Current tags: {note.tags}")

                        new_title = input("\nEnter new title (or press Enter to keep current): ")
                        new_content = input("Enter new content (or press Enter to keep current): ")
                        new_tags = input("Enter new tags (comma-separated, or press Enter to keep current): ")


                        title = new_title if new_title.strip() else None
                        content = new_content if new_content.strip() else None
                        tags = [tag.strip() for tag in new_tags.split(',')] if new_tags.strip() else None

                        note.update(title=title, content=content, tags=tags)
                        note.save(filename)
                        print(f"\nNote '{filename}.note' updated successfully!")
                    else:
                        print("\nInvalid note number!")
                except ValueError:
                    print("\nPlease enter a valid number!")
            input("\nPress Enter to return to menu...")




    def handle_delete(self):
        files = self.notebook.list_notes()
        if not files: #If no files are found
            print("\nNo notes found!")
            input("\nPress Enter to return to menu...")
        else:
            print("\nAvailable notes:")
            for i, file in enumerate(files, 1):#Gives us the file number
                print(f"  {i}. {file}")

            note_choice = input("\nEnter note number to delete: ")
            try:
                index = int(note_choice) - 1 #finds the note number
                if 0 <= index < len(files): #convert and adjust, because indexes
                    filename = files[index].replace('.note', '') #Removes the note extension
                    confirm = input(f"Are you sure you want to delete '{filename}.note'? (y/n): ")
                    if confirm.lower() == 'y':#add .lower so user can type in whatever they want.
                        self.notebook.delete_note(filename)#Actually removes the file
                        print(f"\nNote '{filename}.note' deleted successfully!")
                    else:
                        print("\nDeletion cancelled.")
                else:
                    print("\nInvalid note number!")
            except ValueError:#make sure the user enters in the right numbers
                print("\nPlease enter a valid number!")
            input("\nPress Enter to return to menu...")

    def handle_stats(self):
        stats = self.notebook.get_stats()
        print("\n===Note Statistics===")
        print(f"Total Notes: {stats['total_notes']}")
        print(f"Unique tags: {stats['total_tags']}")
        if stats['all_tags']:
            print(f"All tags used: {','.join(set(stats['all_tags']))}")
        input("\nPress Enter to return to menu...")

    def handle_help(self):
        print("\n=== Notes Manager Help ===")
        print("Welcome to the Notes App")
        print("\nAvailable commands:")
        print("  1. List notes   - View all your notes")
        print("  2. Create note  - Create a new note")
        print("  3. Read note    - Display a specific note")
        print("  4. Edit note    - Modify an existing note")
        print("  5. Search notes - Finds a note")
        print("  6. Delete note  - Removes a note")
        print("  7. Stats        - Views statistics")
        print("  8. Help         - Show this help")
        print("  9. Exit         - Quit the application")
        input("\nPress Enter to return to menu...")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nSelect an option (1-9): ")#Handles User inputs

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
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid option. Please choose 1-9.")

if __name__ == '__main__':
    notebook = Notebook(ROOT_FOLDER)#calls back to the configurator
    app = Application(notebook)#Creates the new instance with __int__
    app.run()






