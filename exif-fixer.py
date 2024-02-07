from datetime import datetime
import piexif

import re
import os
import sys

date_pattern = re.compile(r"(?:(?:\b|_)(\d{4}-\d{2}-\d{2}|\d{8})(?:\b|_))")
time_pattern = re.compile(r"(?:(?:\b|_)(\d{6})(?:\b|_))")

def to_datetime(date_str, time_str):
    try:
        return datetime.strptime("{} {}".format(date_str, time_str), "%Y%m%d %H%M%S")
    except Exception as e:
        return None

def set_exif_date(filepath, date):
    exif_date = date.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict = {
        'Exif': {
            piexif.ExifIFD.DateTimeOriginal: exif_date,
            piexif.ExifIFD.DateTimeDigitized: exif_date
        }
    }
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filepath)


def main(argv):
    path = sys.argv[1] if (len(sys.argv) > 1)  else "./"
    print("Fixing photos in folder: " + path)

    allowed_files_ext = ['jpg','jpeg']
    filenames = [fn for fn in os.listdir(path) if (fn.split('.')[-1] in allowed_files_ext)]

    no_exif_files = []
    for i, filename in enumerate(filenames):
        file = "{}/{}".format(path, filename)
        exif_data = piexif.load(file)
        has_date = 'Exif' in exif_data and piexif.ExifIFD.DateTimeOriginal in exif_data['Exif']
        if (has_date == False):
            no_exif_files.append(filename)

    print(no_exif_files)
    total = len(no_exif_files)
    for i, filename in enumerate(no_exif_files):
        datetime = None
        date_matcher = date_pattern.search(filename)
        if (date_matcher is None):
            continue

        date_str = date_matcher.group(1).replace("-","")
        time_str = None
        time_matcher = time_pattern.search(filename)
        if (time_matcher is not None):
            time_str = time_matcher.group(1)
        if (time_str is not None):
            datetime = to_datetime(date_str, time_str)

        if (datetime is None):
            datetime = to_datetime(date_str, "120000")

        if (datetime is not None):
            file = "{}/{}".format(path, filename)
            set_exif_date(file, datetime)

            print("{i}/{total} - {filename} [date={date}]"
                    .format(i=i+1, total=total, filename=filename, date=datetime))

    print('\nDone!')

if __name__ == "__main__":
   main(sys.argv)
