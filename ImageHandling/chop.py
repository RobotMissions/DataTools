#!/usr/bin/env python3


# How to use: chop.py -i input-image.jpg
#
# It will create a directory under the cwd named input-image (the name
# of the image without extension) and put 9 tiles of the original
# picture.  The script figures out how big the picture is, divides the
# picture in three horizontally and three vertically, and chops the
# picture into those 9 tiles called t0.ext - t8.ext The script can
# handle the image formats that imagemagick can handle as it calls
# imagemagick to do the work.

import argparse
import logging
import os.path
import os
import re
import subprocess
import sys


# sample output from identify command:
#     buttercups-1.jpg JPEG 3024x4032 3024x4032+0+0 8-bit sRGB 3.058MB 0.000u 0:00.000
# the first token is the file name
# second - image type
# third - dimensions
# fourth - geometry
# and there are a few more
def get_dimensions(infile):
    width = 0
    height = 0
    command = ['identify', '-format', 'w %[fx:w] h %[fx:h]\n', infile]
    ident_output = subprocess.check_output(command).decode('ascii')
    rex=re.compile(r'w ([0-9]+) h ([0-9]+)')
    mo = rex.search(ident_output)
    if mo:
        width = mo.group(1)
        height = mo.group(2)
    else:
        raise Exception('Cannot get image dimensions')
    return int(width), int(height)

# convert buttercups-2.jpg -crop 3x3@ +repage t%d.jpg
# montage -mode concatenate -tile 3x t[0-8].jpg out.jpg
def do_crop(args):
    '''Divide picture into 9 tiles named t0.jpg - t8.jpg'''
    args.logger.debug('input:  args.infile')
    width, height = get_dimensions(args.infile)
    args.logger.debug('picture {} dimensions are w {} h {}'.format(
        args.infile, width, height))

    basename, ext = os.path.splitext(args.infile)
    args.logger.debug('{}  {}'.format(basename, ext))

    try:
        os.mkdir(basename)
    except FileExistsError as fee:
        args.logger.exception('cannot create directory for tiles')
        raise

    command = ['convert', args.infile, '-crop', '3x3@', '+repage',
               os.path.join(basename, 't%d{}'.format(ext))]
    crop_output = subprocess.check_output(command).decode('ascii')
    args.logger.debug('CCC:  {}'.format(' '.join(command)))

def setup_logger(args):
    logger = logging.getLogger('chop.py')
    logger.myloglevel = args.verbosity
    logger.setLevel(logger.myloglevel)
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logger.myloglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    args.logger = logger

def handle_args_and_create_logger():
    parser = argparse.ArgumentParser(description='Chop an image into 9 tiles (3x3).')
    parser.add_argument('-i', '--infile', default=None,
                        help='input filename (default stdin)')
    parser.add_argument('-v', '--verbosity', default='ERROR',
                        help='verbosity of logging:  DEBUG,INFO,WARNING,*ERROR,CRITICAL')
    args = parser.parse_args()
    setup_logger(args)
    return args

if '__main__' == __name__:
    args = handle_args_and_create_logger()
    do_crop(args)
