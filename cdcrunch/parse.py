"""Contains for functions for parsing CD data files."""

from collections import Counter

def get_data_blocks(file_lines):
    """Takes the lines of a django file object and breaks it into sections
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


def remove_short_lines(data_blocks):
    """Takes a list of data blocks and removes those with fewer than three
    values per line."""

    return [b for b in data_blocks if len([
     line for line in b if len(line) >= 3
    ]) == len(b)]


def strip_data_blocks(data_blocks):
    """Takes a list of daya blocks, works out which column is the error, and
    removes every value on every line apart from wavelength, cd, cd_error.
    The function will start by assuming the third column is an error column. It
    will decide a column is not an error column if it finds any negative numbers
    in that column, or any numbers greater than 100. It will also discard a
    column if it is entirely zero. It will go through each subsequent column,
    using the same criteria, until it finds one that looks ok.
    If no columns match, an error of zero is used."""

    if data_blocks:
        error_col = 2
        while error_col > 0:
            still_good = True
            non_zero = False
            for block in data_blocks:
                for line in block:
                    if error_col > len(line) - 1:
                        error_col = -1
                        still_good = False
                        break
                    if line[error_col] < 0 or line[error_col] > 100:
                        error_col += 1
                        still_good = False
                        break
                    if line[error_col] != 0:
                        non_zero = True
                    if not still_good: break # The line is no good
                if not still_good: break # The block is no good
            # All blocks have now been checked
            if not non_zero:
                error_col += 1
                still_good = False
            if still_good: break
        blocks = [[line[:2] + [
         line[error_col] if error_col > 0 else 0
        ] for line in b] for b in data_blocks]
        return blocks
    return []
