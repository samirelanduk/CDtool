from math import sqrt
from collections import Counter
from inferi import Series

def extract_all_series(django_file):
    """Takes a Django file object and extracts all the CD scans from it. This
    will be a list of scans, with each scan being a list of wavelength
    measurments, with each measurment being of the form
    [wavelength, cd, cd_error]."""

    raw_lines = list(django_file)
    file_lines = [line.decode().strip() for line in raw_lines if line.strip()]
    float_groups = get_float_groups(file_lines)
    filtered_groups = remove_short_float_groups(float_groups)
    filtered_groups = remove_incorrect_wavelengths(filtered_groups)
    filtered_groups = remove_short_lines(filtered_groups)
    stripped_groups = strip_float_groups(filtered_groups)
    return stripped_groups


def get_float_groups(file_lines):
    """Takes the lines of a django files and breaks it into sections composed
    entirely of space separated numbers."""

    float_groups, float_group = [], []
    split_file_lines = [line.split() for line in file_lines]
    for line in split_file_lines:
        try:
            chunks = [float(chunk) for chunk in line]
            float_group.append(chunks)
        except ValueError:
            if float_group:
                float_groups.append(float_group)
                float_group = []
    if float_group: float_groups.append(float_group)
    return float_groups


def remove_short_float_groups(float_groups):
    """Takes a list of float groups, identifies the longest one, and removes
    groups shorter than that."""

    if float_groups:
        longest_length = len(sorted(float_groups, key=lambda k: len(k))[-1])
        return [group for group in float_groups if len(group) == longest_length]
    return []


def remove_incorrect_wavelengths(float_groups):
    """Takes a list of float groups, identifies the wavelength set that is most
    common (the first number on each line assumed to be wavelength) and removes
    the groups which don't match."""

    if float_groups:
        wavelengths = [tuple([line[0] for line in group]) for group in float_groups]
        wavelengths = Counter(wavelengths)
        correct_wavelengths = list(wavelengths.most_common(1)[0][0])
        return [
         g for g in float_groups if [line[0] for line in g] == correct_wavelengths
        ]
    return []


def remove_short_lines(float_groups):
    """Takes a list of float groups and removes those with fewer than three
    values per line."""

    return [g for g in float_groups if len([
     line for line in g if len(line) >= 3
    ]) == len(g)]


def strip_float_groups(float_groups):
    """Takes a list of float groups, works out which column is the error, and
    removes every value on every line apart from wavelength, cd, cd_error.

    The function will start by assuming the third column is an error column. It
    will decide a column is not an error column if it finds any negative numbers
    in that column, or any numbers greater than 100. It will also discard a
    column if it is entirely zero. It will go through each subsequent column,
    using the same criteria, until it finds one that looks ok.

    If no columns match, an error of zero is used."""

    if float_groups:
        error_col = 2
        while error_col > 0:
            still_good = True
            non_zero = False
            for group in float_groups:
                for line in group:
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
                if not still_good: break # The group is no good
            # All groups have now been checked
            if not non_zero:
                error_col += 1
                still_good = False
            if still_good: break

        groups = [[line[:2] + [
         line[error_col] if error_col > 0 else 0
        ] for line in g] for g in float_groups]
        return groups
    return []


def average_series(series):
    """Takes the series output by extract_all_series and averages them. A single
    scan is produced and returned. This scan will be a list of wavelength
    measurements, with each measurment taking the form
    [wavelength average_cd, standard_error."""

    wavelengths = [line[0] for line in series[0]]
    average = []
    for index, wavelength in enumerate(wavelengths):
        measurements = Series(*[s[index][1] for s in series], sample=False)
        mean = measurements.mean()
        error = series[0][index][2] if len(series) == 1 else \
         measurements.standard_deviation()

        average.append([wavelength, mean, error])
    return average


def get_file_name(title):
    """Takes an experiment title and turns it into a filename."""

    return title.lower().replace(" ", "_") if title else ""
