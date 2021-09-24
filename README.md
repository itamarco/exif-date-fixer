# exif-date-fixer
Restoring missing photo's exif date from the photo name

## usage:
```
pip install piexif
python exif-fixer.py ./path/to/photos/folder
```

## what is it good for?
Photos galeries are using the "creation date" field in the exif metadata in order to sort/display photos.
Eif fields may be missing. It happens for instance when downloading photos from Whatsapp.

This sciprt try to infer the date from the file name- 
e.g.
"WA-20212309-1303-C1.jpg" file name implies that the photo was taken on 23/9/2021 13:03.
