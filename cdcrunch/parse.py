"""Contains for functions for parsing CD data files."""

from collections import Counter

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


def remove_incorrect_wavelengths(data_blocks):
    """Takes a list of data blocks, identifies the wavelength set that is most
    common (the first number on each line assumed to be wavelength) and removes
    the blocks which don't match."""

    if data_blocks:
        wavelengths = [tuple([l[0] for l in block]) for block in data_blocks]
        wavelengths = Counter(wavelengths)
        correct_wavelengths = list(wavelengths.most_common(1)[0][0])
        return [
         b  for b in data_blocks if [l[0] for l in b] == correct_wavelengths
        ]
    return []
