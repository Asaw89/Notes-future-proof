import sys
import os
import yaml
from Configurator import ROOT_FOLDER
from datetime import datetime


def help_message():
    help_string = 'Notes know hows to "help"'
    print(help_string)

def collect_note():#We need a way to collect information from the user to create a note.
    filename = input('Enter note filename:')
    title = input('Enter title:')
    content =input('Enter note content:')
    tags_input=input('Enter tags(comma-separated, or press Enter to skip):')

    if tags_input.strip():#split by commas and clean up spaces around each tag
        tags=[tag.strip() for tag in tags_input.split(',')]
    else:
        tags = []
    return filename,title,content,tags

def save_note(filename, title, content, tags): #We need to take the information the user gave us and save it as a properly formatted note file with YAML metadata.
    timestamp = datetime.now().isoformat() +'Z'#Use datetime to get the current time and save it to ISO format 'Z' shows UTC time
    metadata={
        'title': title,
        'created': timestamp,
        'modified': timestamp,
        'tags':tags
    }
    yaml_string = yaml.dump(metadata)#convert to YAML by going from dictionary -> YAML
    full_content = '---\n' + yaml_string + '---\n\n' + content #We construct the contents together like Lego Blocks

    with open(f'{ROOT_FOLDER}/{filename}.note', 'w') as f:#Creates the file path and Writes it
        f.write(full_content)# Writes YAML + Content

def list_files():
    files = os.listdir(ROOT_FOLDER)
    notes = [f for f in files if f.endswith('.note')]
    return notes
    # get all the filenames from the CWD
    # print them out

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

def edit_note(filename, title=None, content=None,tags=None ):#Read the existing note
    filepath = f'{ROOT_FOLDER}/{filename}.note'
    result=read_note(filepath)

    if title is not None: #update the fields
        result['metadata']['title']= title
    if content is not None:
        result['content']= content
    if tags is not None:
        result['metadata']['tags']=tags
    result['metadata']['modified']=datetime.now().isoformat() + 'Z' #updates the timestamp

    yaml_string=yaml.dump(result['metadata']) #converts to YAML and back then puts everything together like lego blocks
    full_content= '---\n' + yaml_string + '---\n\n' + result['content']

    with open(filepath, 'w') as f: #writes the new note.
        f.write(full_content)

def delete_note(filename):
    filepath = f'{ROOT_FOLDER}/{filename}.note'
    os.remove(filepath)

def get_stats():
    files = list_files()
    total_notes = len(files)

    all_tags= []
    for files in files:
        try:
            result=read_note(f'{ROOT_FOLDER}/{files}')
            tags = result['metadata'].get('tags', [])
            all_tags.extend(tags)
        except Exception:
            pass
    total_tags = len(set(all_tags))

    return {
        'total_notes': total_notes,
        'total_tags': total_tags,
        'all_tags' : all_tags
    }


def display_menu():
    print("\n=== Notes Manager ===")
    print("1. List notes")
    print("2. Create note")
    print("3. Read note")
    print('4. Edit Note')
    print("5. Delete note")
    print("6. Stats")
    print("7. Help")
    print("8. Exit")
    print("====================")

def main():
    while True: #infinite loop
        display_menu()
        choice = input("\nSelect an option (1-8): ")

        if choice == '1':
            # List notes
            files = list_files()
            print("\nYour notes:")
            for file in files:
                print(f"  - {file}")
            input("\nPress Enter to return to menu...")

        elif choice == '2':
            # Create note
            filename, title, content, tags = collect_note()
            save_note(filename, title, content, tags)
            print(f"\nNote '{filename}.note' created successfully!")
            input("\nPress Enter to return to menu...")  # Remove the result line above this!

        elif choice == '3':
            # Read note
            files = list_files()
            if not files:
                print("\nNo notes found!")
                input("\nPress Enter to return to menu...")
            else:
                print("\nAvailable notes:")
                for i, file in enumerate(files, 1):
                    print(f"  {i}. {file}")

                note_choice = input("\nEnter note number to read: ")
                try:
                    index = int(note_choice) - 1
                    if 0 <= index < len(files):
                        filename = files[index]
                        result = read_note(f'{ROOT_FOLDER}/{filename}')

                        print(f"\n--- {result['metadata']['title']} ---")
                        print(f"Created: {result['metadata']['created']}")
                        print(f"Tags: {result['metadata'].get('tags', [])}")
                        print(f"\n{result['content']}")
                        input("\nPress Enter to return to menu...")  # Add it HERE!
                    else:
                        print("\nInvalid note number!")
                        input("\nPress Enter to return to menu...")
                except ValueError:
                    print("\nPlease enter a valid number!")
                    input("\nPress Enter to return to menu...")

        elif choice == '4':
            #Edit Note
            files = list_files()
            if not files:
                print("\nNo notes found!")
                input("\nPress Enter to return to menu...")
            else:
                print("\nAvailable notes:")
                for i, file in enumerate(files, 1):
                    print(f"  {i}. {file}")
                note_choice = input("\nEnter note number to edit: ")
                try:
                    index = int(note_choice) - 1
                    if 0 <= index < len(files):
                        filename = files[index].replace('.note', '')

                        # Show current content
                        result = read_note(f'{ROOT_FOLDER}/{files[index]}')
                        print(f"\nCurrent title: {result['metadata']['title']}")
                        print(f"Current content: {result['content'][:50]}...")  # Show first 50 chars
                        print(f"Current tags: {result['metadata'].get('tags', [])}")

                        # Get new values
                        new_title = input("\nEnter new title (or press Enter to keep current): ")
                        new_content = input("Enter new content (or press Enter to keep current): ")
                        new_tags = input("Enter new tags (comma-separated, or press Enter to keep current): ")

                        #Parse Input
                        title = new_title if new_title.strip() else None
                        content = new_content if new_content.strip() else None
                        tags = [tag.strip() for tag in new_tags.split(',')] if new_tags.strip() else None

                        # Edit the note
                        edit_note(filename, title=title, content=content, tags=tags)
                        print(f"\nNote '{filename}.note' updated successfully!")
                    else:
                        print("\nInvalid note number!")
                except ValueError:
                    print("\nPlease enter a valid number!")
                input("\nPress Enter to return to menu...")


        elif choice == '5':
            # Delete note
            files = list_files()
            if not files:
                print("\nNo notes found!")
                input("\nPress Enter to return to menu...")
            else:
                print("\nAvailable notes:")
                for i, file in enumerate(files, 1):
                    print(f"  {i}. {file}")

                note_choice = input("\nEnter note number to delete: ")
                try:
                    index = int(note_choice) - 1
                    if 0 <= index < len(files):
                        filename = files[index].replace('.note', '')
                        confirm = input(f"Are you sure you want to delete '{filename}.note'? (y/n): ")
                        if confirm.lower() == 'y':
                            delete_note(filename)
                            print(f"\nNote '{filename}.note' deleted successfully!")
                        else:
                            print("\nDeletion cancelled.")
                    else:
                        print("\nInvalid note number!")
                except ValueError:
                    print("\nPlease enter a valid number!")
                input("\nPress Enter to return to menu...")

        elif choice == '6':
            #stats
            stats = get_stats()
            print("\n===Note Statistics===")
            print(f"Total Notes: {stats['total_notes']}")
            print(f"Unique tags: {stats['total_tags']}")
            if stats['all_tags']:
                print(f"All tags used: {','.join(set(stats['all_tags']))}")
            input("\nPress Enter to return to menu...")

        elif choice == '7':
            # Help
            help_message()
            input("\nPress Enter to return to menu...")

        elif choice == '8':
            # Exit
            print("\nGoodbye!")
            break

if __name__ == '__main__':
    main()