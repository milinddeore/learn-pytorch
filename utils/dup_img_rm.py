# -*- coding:utf8 -*-
# !/usr/bin/env python
#
# Columbus https://mycolumbus.xyz
# The MIT License (MIT)
#
# Written by Milind Deore <tomdeore@gmail.com>, Jan 2020


# If you want to extract images from a video an use them for training model,
# this post (https://medium.com/@tomdeore/convert-video-to-images-61ab3cea30a8) would
# help you capture images out of a video. Often such video has may duplicates. Following
# code help you find and remove those duplicate files.

import os
import shutil
import argparse
from imagededup.methods import PHash

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, required=True, help="path of folder, for duplicated trashing")
args = parser.parse_args()

def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


if __name__ == "__main__":
    path = args.path
    del_list = []

    phasher = PHash()
    encodings = phasher.encode_images(image_dir=path)
    duplicates = phasher.find_duplicates(encoding_map=encodings)

    for k,v in duplicates.items():
        if len(v) and (k not in del_list):
            for fname in v:
                del_list.append(fname)

    print('Deleting Duplicates :\n{0}'.format(del_list))

    for dl in del_list:
        remove(path + dl)
