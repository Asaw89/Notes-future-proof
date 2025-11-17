import sys

def help_mesg():
    help_string = 'Notes know hows to "help"'
    print(help_string)

def list_files():
    print("all the files")
    # get all the filenames from the CWD
    # print them out

def read_note(n):
    pass

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'help':
            help_mesg()
        elif cmd == 'list':
            list_files()
        elif cmd == 'read':
            # get noteid
            # open noteid.note
            # print out
            noteid = ''
            read_note(noteid)    
    else:
        print("please provide a command.")
    
    print(sys.argv)

if __name__ == '__main__':
    main()