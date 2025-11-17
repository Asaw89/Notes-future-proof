from notes import read_note

def test_read_note_returns_content():
    result = read_note('test-notes/sample-note-1.md')
    
    # Check that it has both keys
    assert 'metadata' in result
    assert 'content' in result
    
    # Check that content exists and starts with the expected text
    assert result['content'].startswith('# Data Structures Overview')