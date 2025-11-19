from notes import read_note, list_files, save_note, delete_note, get_stats, edit_note

def test_list_files_returns_note_files():
    files = list_files()

    # Check that it returns a list
    assert isinstance(files, list)

    # Check that it found at least one .note file
    assert len(files) > 0

    # Check that all files end with .note
    for file in files:
        assert file.endswith('.note')

def test_save_note_creates_file_with_yaml():
    # Save a new note
    save_note('test-note', 'My Test Note', 'This is test content', ['testing', 'example'])

    # Read it back
    result = read_note('notes/test-note.note')

    # Verify the metadata
    assert result['metadata']['title'] == 'My Test Note'
    assert result['metadata']['tags'] == ['testing', 'example']
    assert result['content'] == 'This is test content'

def test_delete_note_removes_file():
    # First, create a test note
    save_note('temp-delete-test', 'Delete Test', 'This will be deleted', [])

    # Verify it exists
    files = list_files()
    assert 'temp-delete-test.note' in files

    # Delete it
    delete_note('temp-delete-test')

    # Verify it's gone
    files = list_files()
    assert 'temp-delete-test.note' not in files

def test_stats_returns_note_count():
    stats = get_stats()

    # Check that it returns a dictionary with stats
    assert 'total_notes' in stats
    assert isinstance(stats['total_notes'], int)
    assert stats['total_notes'] >= 0

def test_edit_note_updates_content():
    # Create a test note
    save_note('edit-test', 'Original Title', 'Original content', ['test'])

    # Edit it
    edit_note('edit-test', title='Updated Title', content='New content', tags=['updated'])

    # Read it back
    result = read_note('notes/edit-test.note')

    # Verify changes
    assert result['metadata']['title'] == 'Updated Title'
    assert result['content'] == 'New content'
    assert result['metadata']['tags'] == ['updated']