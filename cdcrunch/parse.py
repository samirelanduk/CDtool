"""Contains for functions for parsing CD data files."""

def get_data_blocks(file_lines):
    """Takes the lines of a django file objecy and breaks it into sections
    composed entirely of space separated numbers."""

    data_blocks, data_block = [], []
    split_file_lines = [line.split() for line in file_lines]
    for line in split_file_lines:
        try:
            chunks = [float(chunk) for chunk in line]
            data_block.append(chunks)
        except ValueError:
            if data_block:
                data_blocks.append(data_block)
                data_block = []
    if data_block: data_blocks.append(data_block)
    return data_blocks


def remove_short_data_blocks(data_blocks):
    """Takes a list of data blocks, identifies the longest one, and removes
    groups shorter than that."""

    if data_blocks:
        longest_length = len(sorted(data_blocks, key=lambda k: len(k))[-1])
        return [group for group in data_blocks if len(group) == longest_length]
    return []
