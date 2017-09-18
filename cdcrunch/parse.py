"""Contains for functions for parsing CD data files."""

from collections import Counter
from inferi import Dataset, Variable

def extract_scans(django_file):
    """Takes a django file object and returns the scans it contains as inferi
    Dataset objects."""

    lines = file_to_lines(django_file)
    potential_blocks = extract_data_blocks(lines)
    len_filtered_blocks = remove_short_data_blocks(potential_blocks)
    wav_filtered_blocks = remove_incorrect_wavelengths(len_filtered_blocks)
    line_filtered_blocks = remove_short_lines(wav_filtered_blocks)
    stripped_blocks = strip_data_blocks(line_filtered_blocks)
    datasets = [block_to_dataset(block) for block in stripped_blocks]
    return datasets


def file_to_lines(django_file):
    """Takes an uploaded file, and breaks into lines. The lines will be stripped
    at both ends, and decoded from bytes to strings. If the file is a binary
    file, an empty list will be returned."""

    lines = list(django_file)
    try:
        lines = [line.strip().decode() for line in lines if line.strip()]
    except UnicodeDecodeError: return []
    return lines


def extract_data_blocks(file_lines):
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
        longest_length = max([len(block) for block in data_blocks])
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
    """Takes a list of data blocks, decides which column is the error column,
    and discards all other columns. If no columns look likely, errors of 0 are
    used."""

    if not data_blocks: return []
    cd_column, other_columns = [], [[] for val in data_blocks[0][0][2:]]
    for block in data_blocks:
        cd_column += [line[1] for line in block]
        for row in block:
            for index, value in enumerate(row[2:]):
                other_columns[index].append(value)
    checks = [is_possible_error_column(col, cd_column) for col in other_columns]
    try:
        error_col_number = checks.index(True) + 2
    except ValueError: error_col_number = -1
    for block in data_blocks:
        for row in block:
            for index in range(len(row)):
                if index > 1 and index != error_col_number:
                    row[index] = None
            while None in row: row.remove(None)
            if len(row) == 2: row.append(0)
    return data_blocks



def is_possible_error_column(column, absorbance):
    """Checks if a column could be an error column based on the CD values."""

    if set(column) == set([0]): return False
    delta_abs = max(absorbance) - min(absorbance)
    for val in column:
        if val < 0 or val > delta_abs * 2:
            return False
    return True


def block_to_dataset(data_block):
    """Turns a data block into an inferi Dataset, with a Variable for wavelength
    and a Variable for CD absorbance."""

    wavelength = Variable(*[line[0] for line in data_block])
    cd = Variable(
     *[line[1] for line in data_block],
     error=[line[2] for line in data_block]
    )
    return Dataset(wavelength, cd)


def dataset_to_dict(dataset, linewidth=1, color="#000000", name=""):
    """Takes a scan Dataset and turns into a JSON-valid dict."""

    wav, cd = dataset.variables()
    return {
     "series": [[x, y] for x, y in zip(wav, cd)][::-1],
     "error": [[
      x, *[round(val, 8) for val in y.error_range()]
     ] for x, y in zip(wav, cd.values(error=True))][::-1],
     "linewidth": linewidth,
     "color": color,
     "name": name
    }
