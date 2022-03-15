# ﺏ
# Copyright [2022] Şefik Efe Altınoluk
#
# This file is a part of project Wi-Phi©
# For more details, see https://github.com/f4T1H21/Wi-Phi
#
# Licensed under the GNU GENERAL PUBLIC LICENSE Version 3.0 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/gpl-3.0.html

import uos

# Alternative of os.walk
def walk(root):
    folders = []
    files = []
    for entry in uos.ilistdir(root):
        fname = entry[0]
        ftype = entry[1]
        if ftype == int('0x4000', 16): # Is this a folder?
            folders.append(fname)
        else:
            files.append(fname)
    yield root, folders, files
    for folder in folders:
        yield from walk(root + '/' + folder)


def get_extension(path):
    if path == "":
        return None
    split = path.rsplit('.', 1)
    if len(split) == 1:
        return None
    return split[1]