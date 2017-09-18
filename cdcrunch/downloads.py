from datetime import datetime
import json
from time import tzname
from cdtool import version

DATA_FILE = """CDtool {}
Date generated: {}
Time generated: {}

Wavelength (nm)   Absorbance   Absorbance Error
"""


def produce_filename(name):
    """Takes an experiment name and returns a valid filename."""

    name = name.lower() if name else "cdresults"
    replacements = {" ": "_", ":": "-", "@": "-"}
    for char in replacements:
        name = name.replace(char, replacements[char])
    return name + ".dat"


def series_to_file(series):
    """Takes a series string sent from the frontend, converts it into a dict,
    and produces the string of a download file from it."""

    series = json.loads(series.replace("'", '"'))
    date = datetime.now().strftime("%d %B, %Y (%A)")
    time = datetime.now().strftime("%H:%M:%S ({})").format(tzname[0])
    lines = ["{:.1f}         {:10.4f}   {:10.4f}".format(
     cd[0],
     cd[1],
     abs(error[1] - error[2]) / 2
    ) for cd, error in zip(series["series"][::-1], series["error"][::-1])]
    return DATA_FILE.format(version, date, time) + "\n".join(lines)
