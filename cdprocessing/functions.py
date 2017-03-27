from math import sqrt
from collections import Counter
from inferi import Series

def extract_all_series(django_file):
    """Takes a Django file object and extracts all the CD scans from it."""

    raw_lines = list(django_file)
    file_lines = [line.decode().strip() for line in raw_lines if line.strip()]
    float_groups = get_float_groups(file_lines)
    correct_float_groups = filter_float_groups(float_groups)
    return correct_float_groups


def get_float_groups(file_lines):
    float_groups, float_group = [], []
    split_file_lines = [line.split() for line in file_lines]
    for line in split_file_lines:
        try:
            first, second = float(line[0]), float(line[1])
            float_group.append([first, second])
        except ValueError:
            if float_group:
                float_groups.append(float_group)
                float_group = []
    if float_group: float_groups.append(float_group)
    return float_groups


def filter_float_groups(float_groups):
    longest_length = len(sorted(float_groups, key=lambda k: len(k))[-1])
    correct_length_groups = [
     group for group in float_groups if len(group) == longest_length
    ]
    wavelengths = [
     tuple([line[0] for line in group]) for group in correct_length_groups
    ]
    wavelengths = Counter(wavelengths)
    most_common_wavelengths = wavelengths.most_common(1)[0][0]
    correct_wavelength_groups = [group for group in correct_length_groups if tuple(
     [line[0] for line in group]
    ) == most_common_wavelengths]
    return correct_wavelength_groups


def average_series(series):
    wavelengths = [line[0] for line in series[0]]
    average = []
    for index, wavelength in enumerate(wavelengths):
        measurements = Series(*[s[index][1] for s in series])
        mean = measurements.mean()
        error = 0 if len(series) == 1 else \
         measurements.standard_deviation() / sqrt(len(series))
        max_, min_ = mean - error, mean + error

        average.append([wavelength, mean, error, max_, min_])
    return average
