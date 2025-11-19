import sys
import os
import yaml
from datetime import datetime


def help_mesg():
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
    full_content = '---\n' + yaml_string + '---n\n' + content

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

def display_menu():
    print("\n=== Notes Manager ===")
    print("1. List notes")
    print("2. Create note")
    print("3. Read note")
    print("4. Delete note")
    print("5. Exit")
    print("====================")

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'help':
            help_mesg()
        elif cmd == 'list':
            files = list_files()
            for file in files:
                print(file)
        elif cmd == 'read note':
            # get noteid
            # open noteid.note
            # print out
            noteid = ''
            read_note(noteid)
        elif cmd == 'delete note':
            list_files.remove()
        elif cmd == 'create':
            filename, title, content, tags = collect_note()
            save_note(filename,title,content,tags)
            print(f"Note '{filename}.note' created")
    else:
        print("please provide a command.")



if __name__ == '__main__':
    main()