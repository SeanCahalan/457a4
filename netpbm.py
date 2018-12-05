# A new version of netpbm for CISC/CMPE 457 due to seek() bugs in the
# original netpbm.py on Windows.
#
# This handles only P5 and P6 formats and does not handle comments in
# the image file.

import sys
import numpy as np


# Read an image.  'f' is an open file descriptor.   Returns a numpy array of uint8.

def imread( f ):

    ptype, xdim, ydim, max_val = read_header(f)

    if max_val != 255:
        sys.stderr.write( 'Can only handle 8-bit-per-channel images\n' )
        sys.exit(1)

    if ptype not in ['P5','P6']:
        sys.stderr.write( 'Can only handle P5 and P6 images\n' )
        sys.exit(1)

    img = np.fromfile( f, dtype='uint8' )

    size = xdim * ydim * (1 if ptype == 'P5' else 3)

    if img.shape[0] != size:
        sys.stderr.write( 'Image has %d bytes, but %d were expected.\n' % (img.shape[0], size) )
        sys.exit(1)

    if ptype == 'P5':
        return img.reshape( ydim, xdim )
    else:
        return img.reshape( ydim, xdim, 3 )


def read_header(f):

    ptype   = read_to_whitespace(f)
    xdim    = int(read_to_whitespace(f))
    ydim    = int(read_to_whitespace(f))
    max_val = int(read_to_whitespace(f))

    return ptype, xdim, ydim, max_val


def read_to_whitespace(f):

    data = ''

    chr = f.read(1)
    while chr not in [' ', '\n', '\t', '\v']:
        data += chr
        chr = f.read(1)

    if chr == '\r': # get LF after a CR-LF
        chr = f.read(1)

    return data


# Write an image.  'f' is an open file descriptor.  'img' in a numpy array of uint8.

def imsave( f, img ):

    ptype = ( 'P5' if len(img.shape) == 2 else 'P6' )
    f.write( '%s %d %d %d\n' % (ptype, img.shape[1], img.shape[0], 255) )
    img.reshape( np.prod(img.shape) ).tofile( f )

    
def test():
    for fn in ['barbara.pnm','cortex.pnm','crest.pnm','mandrill.pnm','noise.pnm']:
        img = imread( 'images/' + fn )
        imwrite( 'images/' + fn + '.out', img )
        print fn, img.shape, len(img.shape), np.prod( img.shape )
