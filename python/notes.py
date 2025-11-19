import sys
import os
import yaml
from datetime import datetime


def help_message():
    help_string = 'Notes know hows to "help"'
    print(help_string)

def collect_note():
    filename = input('Enter note filename:')
    title = input('Enter title:')
    content =input('Enter note content:')
    tags_input=input('Enter tags(comma-separated, or press Enter to skip):')

    if tags_input.strip():
        tags=[tag.strip() for tag in tags_input.split(',')]
    else:
        tags = []
    return filename,title,content,tags

def save_note(filename, title, content, tags):
    timestamp = datetime.now().isoformat() +'Z'
    metadata={
        'title': title,
        'created': timestamp,
        'modified': timestamp,
        'tags':tags
    }
    yaml_string = yaml.dump(metadata)
    full_content = '---\n' + yaml_string + '---\n\n' + content

    with open(f'notes/{filename}.note', 'w') as f:
        f.write(full_content)

def list_files():
    files = os.listdir('notes')
    notes = [f for f in files if f.endswith('.note')]
    return notes
    # get all the filenames from the CWD
    # print them out

def read_note(n):
    with open(n, 'r') as file:
        content = file.read()

    parts = content.split('---')
    yaml_part = parts[1]
    content_part = parts[2].strip()  # Add .strip() here!

    metadata = yaml.safe_load(yaml_part)

    return {
        'metadata': metadata,
        'content': content_part
    }

def delete_note(filename):
    filepath = f'notes/{filename}.note'
    os.remove(filepath)

def get_stats():
    files = list_files()
    total_notes = len(files)

    all_tags= []
    for files in files:
        try:
            result=read_note(f'notes/{files}')
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
    print("4. Delete note")
    print("5. Help")
    print("6. Exit")
    print("====================")

def main():
    while True:
        display_menu()
        choice = input("\nSelect an option (1-5): ")

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
                        result = read_note(f'notes/{filename}')
                        
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

        elif choice == '5':
            # Help
            help_message()
            input("\nPress Enter to return to menu...")

        elif choice == '6':
            # Exit
            print("\nGoodbye!")
            break

if __name__ == '__main__':
    main()