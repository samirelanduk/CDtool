from math import sqrt
from inferi import Series

def clean_file(lines):
    """Takes the lines from a data file and returns a list of cleaned up lines."""

    return [line.decode().strip() for line in lines if line.strip()]


def get_float_groups(lines):
    """Takes data lines and identifies the sections that begin with numbers."""
    float_groups = []
    float_group = []
    for line in lines:
        elements = line.split()
        try:
            float(elements[0])
            float_group.append(line)
        except ValueError:
            if float_group:
                float_groups.append(float_group)
                float_group = []
    if float_group: float_groups.append(float_group)
    return float_groups


def float_groups_to_big_series(float_groups):
    """Gets the largest float group and assumes it is a series."""

    return sorted(float_groups, key=len)[-1]


def float_groups_to_extra_series(float_groups, big_series):
    """Looks through float groups for ones which might be further scans of a
    given float group."""

    potential_series = [group for group in float_groups if group != big_series]
    start_floats = [float(line.split()[0]) for line in big_series]
    series = []
    for group in potential_series:
        group_floats = [float(line.split()[0]) for line in group]
        if group_floats == start_floats:
            series.append(group)
    return series


def extract_wavelengths(series):
    """Takes the wavelengths from a series of lines."""

    return [float(line.split()[0]) for line in series]


def extract_absorbances(series):
    """Gets the wavelengths and absorbances from a series of lines."""

    if len(series) == 1:
        return [[float(line.split()[0]), float(line.split()[1]), 0] for line in series[0]]
    else:
        absorbances = []
        for index, line in enumerate(series[0]):
            wavelength = float(line.split()[0])
            measurements = Series(*[float(s[index].split()[1]) for s in series])
            average_absorbance = measurements.mean()
            error = measurements.standard_deviation() / sqrt(len(measurements))
            absorbances.append([wavelength, average_absorbance, error])
        return absorbances
