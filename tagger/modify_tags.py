import os

import globals


def add(text):
    for file in os.listdir(globals.PROJECT_DIRECTORY):
        if file.endswith('.txt'):
            with open(globals.PROJECT_DIRECTORY + '/' + file, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(text + content)
                f.close()


def remove(text):
    for file in os.listdir(globals.PROJECT_DIRECTORY):
        if file.endswith('.txt'):
            with open(globals.PROJECT_DIRECTORY + '/' + file, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(content.replace(text, ''))
                f.close()
