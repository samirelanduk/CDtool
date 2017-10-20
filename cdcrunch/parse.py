"""Contains for functions for parsing CD data files."""

from collections import Counter
from inferi import Dataset, Variable
from imagipy import Color
from .exceptions import *

def files_to_sample(files, baseline=None, name=""):
    """Takes a list of files, and optionally a list of baseline files. It then
    turns them into a sample dict."""

    sample = None
    if baseline:
        sample = files_to_two_component_sample(files, baseline)
    else:
        sample = files_to_one_component_sample(files)
    sample["name"] = name
    return sample



def files_to_one_component_sample(files):
    """Takes a list of files, (with no baselines). It then turns them into a
    sample dict (minus the name)."""

    scans = files_to_scans(files)
    if len(scans) == 0:
        raise NoScansError
    elif len(scans) == 1:
        return scan_to_dict(scans[0], linewidth=2, color="#16A085")
    elif len(scans) > 1:
        average = average_scans(*scans)
        sample = scan_to_dict(average, linewidth=2, color="#16A085")
        colors = generate_colors(len(scans))
        sample["scans"] = [scan_to_dict(
         scan, linewidth=1, color=color
        ) for scan, color in zip(scans, colors)]
        return sample


def files_to_two_component_sample(raw_files, baseline_files):
    """Takes a list of raw files, and a list of baseline files. It then turns
    them into a sample dict (minus the name)."""

    raw_scans = files_to_scans(raw_files)
    baseline_scans = files_to_scans(baseline_files)
    if not raw_scans and not baseline_scans:
        raise NoScansError
    elif not raw_scans:
        raise NoMinuendScansError
    elif not baseline_scans:
        raise NoSubtrahendScansError
    raw = raw_scans[0] if len(raw_scans) == 1 else average_scans(*raw_scans)
    subtracted = subtract_components(raw, baseline_scans[0])
    sample = scan_to_dict(subtracted, linewidth=2, color="#16A085")
    raw_component = scan_to_dict(raw, linewidth=1.5, color="#137864")
    baseline_component = scan_to_dict(baseline_scans[0], linewidth=1.5, color="#A0D6FA")
    if len(raw_scans) > 1:
        colors = generate_colors(len(raw_scans))
        raw_component["scans"] = [scan_to_dict(
         scan, linewidth=1, color=color
        ) for scan, color in zip(raw_scans, colors)]
    sample["components"] = [raw_component, baseline_component]
    return sample


def files_to_scans(files):
    """Takes a list of scans and returns all the scans it finds in them as a
    single list."""

    scans = []
    for f in files:
        scans += file_to_scans(f)
    return scans


def file_to_scans(django_file):
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


def generate_colors(n):
    """Generates n colors, starting with six basic colours and mutating them."""

    colors = [
     Color.RED, Color.BLUE, Color.ORANGE,
     Color.PURPLE, Color.GREEN, Color.BROWN
    ]
    color_len = len(colors)
    while n > len(colors):
        colors.append(colors[-color_len].mutate())
    return [color.hex() for color in colors][:n]


def average_scans(*scans):
    """Takes some Datasets and produces a Dataset which has the wavelength
    column of the first Dataset and the averaged CD column of all of them."""

    averaged_cd = Variable.average(*[
     scan.variables()[1] for scan in scans
    ], sd_err=True)
    return Dataset(scans[0].variables()[0], averaged_cd)


def subtract_components(component1, component2):
    """Takes two Datasets and subtracts one from the other."""

    subtracted_cd = component1.variables()[1] - component2.variables()[1]
    return Dataset(component1.variables()[0], subtracted_cd)


def scan_to_dict(scan, linewidth=1, color="#000000"):
    """Takes a scan Dataset and turns into a JSON-valid dict."""

    wav, cd = scan.variables()
    return {
     "series": [[x, round(y, 8)] for x, y in zip(wav, cd)][::-1],
     "error": [[
      x, *[round(val, 8) for val in y.error_range()]
     ] for x, y in zip(wav, cd.values(error=True))][::-1],
     "linewidth": linewidth,
     "color": color,
     "scans": [],
     "components": []
    }
