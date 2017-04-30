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
    correct_float_groups = filter_float_groups(float_groups)
    return correct_float_groups


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


def filter_float_groups(float_groups):
    """Takes a a bunch of number groups and returns only the longest ones with
    matching wavelengths, and with more than three values"""

    if float_groups:
        # Remove float groups shorter than the longest float group
        longest_length = len(sorted(float_groups, key=lambda k: len(k))[-1])
        correct_length_groups = [
         group for group in float_groups if len(group) == longest_length
        ]

        # Remove float groups whose first values (wavelengths) don't match the
        # first values of the first float group
        wavelengths = [
         tuple([line[0] for line in group]) for group in correct_length_groups
        ]
        wavelengths = Counter(wavelengths)
        most_common_wavelengths = wavelengths.most_common(1)[0][0]
        correct_wavelength_groups = [group for group in correct_length_groups if tuple(
         [line[0] for line in group]
        ) == most_common_wavelengths]

        # Remove float groups which don't have at least three values
        groups_at_least_three = []
        for group in correct_wavelength_groups:
            add_group = True
            for line in group:
                if len(line) < 3:
                    add_group = False
            if add_group: groups_at_least_three.append(group)
        final_groups = [[line[:3] for line in group] for group in groups_at_least_three]
        return final_groups
    else:
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
