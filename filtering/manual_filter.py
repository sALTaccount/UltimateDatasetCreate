import os
import PIL.Image as Image

import globals

image_list = []
project_dir = ''
cur_idx = 0


def init():
    global image_list
    global project_dir
    global cur_idx
    cur_idx = 0
    image_list = os.listdir(globals.PROJECT_DIRECTORY)
    image_list = [x for x in image_list if x.split('.')[-1] in globals.VALID_EXTENSIONS]
    image_list.sort()
    project_dir = globals.PROJECT_DIRECTORY


def get_cur_image():
    global cur_idx
    if not image_list:
        return None, ''
    if project_dir != globals.PROJECT_DIRECTORY:
        init()
        cur_idx = 0
    background = Image.new("RGB", globals.IMAGE_DISPLAY_RES, color=(255, 255, 255, 0))
    image = Image.open(os.path.join(project_dir, image_list[cur_idx]))
    image.thumbnail(globals.IMAGE_DISPLAY_RES)
    background.paste(image, (int((globals.IMAGE_DISPLAY_RES[0] - image.size[0]) / 2),
                             int((globals.IMAGE_DISPLAY_RES[1] - image.size[1]) / 2)))

    tag_file = os.path.join(project_dir, image_list[cur_idx].split('.')[0] + '.txt')
    if os.path.exists(tag_file):
        tags = open(tag_file, 'r').read()
    else:
        tags = ''

    return background, tags


def increment():
    global cur_idx
    if cur_idx < len(image_list) - 1:
        cur_idx += 1
        message = f"Image {cur_idx + 1} of {len(image_list)}"
    else:
        message = "Reached end of directory."
    if len(image_list) == 0:
        message = "No images in directory."
    image, tags = get_cur_image()
    return image, message, tags


def decrement():
    global cur_idx
    if cur_idx > 0:
        cur_idx -= 1
        message = f"Image {cur_idx + 1} of {len(image_list)}"
    else:
        message = "Reached beginning of directory."
    if len(image_list) == 0:
        message = "No images in directory."
    image, tags = get_cur_image()
    return image, message, tags


def delete():
    global image_list
    image_name = image_list[cur_idx]
    tags_name = image_name.split('.')[0] + '.txt'
    os.remove(os.path.join(project_dir, image_name))
    if os.path.exists(os.path.join(project_dir, tags_name)):
        os.remove(os.path.join(project_dir, tags_name))
    message = f"Deleted {image_name}"

    image_list = os.listdir(project_dir)
    image_list = [x for x in image_list if x.split('.')[-1] in globals.VALID_EXTENSIONS]

    image, tags = get_cur_image()
    return image, message, tags


def modify_tags(tags):
    tag_file = os.path.join(project_dir, image_list[cur_idx].split('.')[0] + '.txt')
    with open(tag_file, 'w') as f:
        f.write(tags)
    return f'Saved tags to {tag_file}'


def refresh():
    if not os.path.isdir(globals.PROJECT_DIRECTORY):
        return None, "Project directory doesn't exist! Set it in the config tab.", ''
    init()
    message = f"Loaded {len(image_list)} images."
    if len(image_list) == 0:
        message = "No images in directory."
    image, tags = get_cur_image()
    return image, message, tags
