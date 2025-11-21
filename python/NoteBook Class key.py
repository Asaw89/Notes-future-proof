Accessing the notebook key:
* self.notebook = the Notebook object (stored in __init__)
* self.notebook.list_notes() = get list of note files
* self.notebook.get_note(filename) = get a specific Note object
* self.notebook.search_notes(query) = search for notes
* self.notebook.delete_note(filename) = delete a note
* self.notebook.get_stats() = get statistics

Calling your own Application methods:
* self.display_menu() = show the menu
* self.collect_note_input() = get input from user
* self.handle_list() = call the list handler
* self.handle_create() = call the create handler
* (etc. for all handlers)
In the Notebook class:
Accessing the folder path:
* self.notes_folder = the folder path string
Calling your own Notebook methods:
* self.list_notes() = call list_notes on yourself
In the Note class:

Accessing note data:
* self.title = the note's title
* self.content = the note's content
* self.tags = the note's tags
* self.created = creation timestamp
* self.modified = modification timestamp
