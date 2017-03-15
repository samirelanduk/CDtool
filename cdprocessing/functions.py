def clean_file(lines):
    """Takes the lines from a data file and returns a list of cleaned up lines."""
    
    return [line.decode().strip() for line in lines if line.strip()]
