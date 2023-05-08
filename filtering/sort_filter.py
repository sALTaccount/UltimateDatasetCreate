import os

import globals


def remove(sort_type, amount):
    files = os.listdir(globals.PROJECT_DIRECTORY)
    images = [file for file in files if file.split('.')[-1] in globals.VALID_EXTENSIONS]
    if sort_type == "Name":
        images.sort(reverse=True)
    if amount < 1:
        to_remove = images[int(len(images) * (1 - amount)):]
    else:
        to_remove = images[int(len(images) - amount):]
    for file in to_remove:
        os.remove(os.path.join(globals.PROJECT_DIRECTORY, file))
        if os.path.isfile(os.path.join(globals.PROJECT_DIRECTORY, file.split('.')[0] + '.txt')):
            os.remove(os.path.join(globals.PROJECT_DIRECTORY, file.split('.')[0] + '.txt'))
    return f"Removed {len(to_remove)} images."
