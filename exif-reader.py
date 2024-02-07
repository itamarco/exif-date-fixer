import piexif


def get_exif_data(image_path):
    # Load EXIF data from the image
    exif_dict = piexif.load(image_path)

    # The EXIF data is stored in various groups (0th, Exif, GPS, 1st, etc.)
    # We'll focus on '0th', 'Exif', and 'GPS' groups for this example
    exif_groups = ['0th', 'Exif', 'GPS']

    # Create a dictionary to store readable EXIF data
    readable_exif = {}

    for group in exif_groups:
        group_data = exif_dict.get(group)
        if group_data:
            readable_exif[group] = {}
            for tag, value in group_data.items():
                # Convert the tag ID to a readable tag name
                tag_name = piexif.TAGS[group][tag]["name"]
                readable_exif[group][tag_name] = value

    return readable_exif


# Replace 'your_image.jpg' with the path to your image file
image_path = ''
exif = get_exif_data(image_path)

# Print the EXIF data
for group, group_data in exif.items():
    print(f"{group} Group:")
    for tag, value in group_data.items():
        print(f"  {tag}: {value}")
