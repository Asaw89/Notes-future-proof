import sys
import os
import yaml
from datetime import datetime


def help_mesg():
    help_string = 'Notes know hows to "help"'
    print(help_string)

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
    print("all the files")
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

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'help':
            help_mesg()
        elif cmd == 'list notes':
            list_files()
        elif cmd == 'read note':
            # get noteid
            # open noteid.note
            # print out
            noteid = ''
            read_note(noteid)
        elif cmd == 'delete note':
            list_files.remove()
    else:
        print("please provide a command.")

    print(sys.argv)

if __name__ == '__main__':
    main()