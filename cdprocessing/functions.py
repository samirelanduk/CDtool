def clean_file(lines):
    """Takes the lines from a data file and returns a list of cleaned up lines."""

    return [line.decode().strip() for line in lines if line.strip()]


def extract_series(lines):
    """Takes the lines from a datafile and identifies the actual series lines
    within it."""
    
    # What are all the lines which begin with a number?
    lines_that_start_with_numbers = []
    for index, line in enumerate(lines):
        try:
            float(line.split()[0])
            lines_that_start_with_numbers.append(index)
        except ValueError:
            pass

    # Cluster these line numbers into consecutive chunks
    cluster = []
    clusters = []
    for index, line_num in enumerate(lines_that_start_with_numbers[:-1]):
        cluster.append(line_num)
        if lines_that_start_with_numbers[index + 1] > line_num + 1:
            clusters.append(cluster)
            cluster = []
    cluster.append(lines_that_start_with_numbers[-1])
    clusters.append(cluster)

    # Which is the biggest cluster?
    cluster = sorted(clusters, key=lambda k: len(k))[-1]

    # Should a header be extracted?
    chunk_count = len(lines[cluster[0]].split())
    if cluster[0] != 0:
        header_line = lines[cluster[0] - 1]
        if len(header_line.split()) == chunk_count:
            cluster = [cluster[0] - 1] + cluster

    # Get the corresponding lines and return
    lines = [lines[index] for index in cluster]
    return lines


def get_wavelengths(lines):
    """Takes the file lines corresponding to a CD scan, and extracts the
    wavelengths from it as a list of floats."""

    wavelengths = []
    for line in lines:
        try:
            wavelengths.append(float(line.split()[0]))
        except ValueError:
            pass
    return wavelengths
