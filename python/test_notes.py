from notes import read_note, list_files

def test_read_note_returns_content():
    result = read_note('test-notes/sample-note-1.md')

    # Check that it has both keys
    assert 'metadata' in result
    assert 'content' in result

    # Check that content exists and starts with the expected text
    assert result['content'].startswith('# Data Structures Overview')

def test_list_files_returns_note_files():
    files = list_files()

    # Check that it returns a list
    assert isinstance(files, list)

    # Check that it found at least one .note file
    assert len(files) > 0

    # Check that all files end with .note
    for file in files:
        assert file.endswith('.note')