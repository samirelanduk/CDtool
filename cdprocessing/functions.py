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


def float_groups_to_series(float_groups):
    """Gets the largest float group and assumes it is a series."""

    return sorted(float_groups, key=len)[-1]


def extract_wavelengths(series):
    """Takes the wavelengths from a series of lines."""

    return [float(line.split()[0]) for line in series]
