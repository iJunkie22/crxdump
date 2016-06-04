#!/usr/bin/env python
from __future__ import print_function
import os
import struct
import sys
import zipfile
import os.path


def main(args):
    if len(args) != 2:  # Print usage and abort
        print('Usage', args[0], '<filename.crx>')
        sys.exit(1)

    crx_fn = os.path.abspath(args[1])
    crx_dir = crx_fn + '_dump'

    if not os.path.isdir(crx_dir):
        os.mkdir(crx_dir)

    assert os.path.exists(crx_dir)

    with open(crx_fn, 'rb') as f:
        assert (f.read(4) == 'Cr24')
        version = struct.unpack('I', f.read(4))[0]
        key_size = struct.unpack('I', f.read(4))[0]
        sig_size = struct.unpack('I', f.read(4))[0]
        key = f.read(key_size)
        sig = f.read(sig_size)

        print('PKZip starts at', f.tell())
        zf = zipfile.ZipFile(f)

        print()
        print(os.path.basename(crx_dir))
        print('\t' + '\n\t'.join(zf.namelist()))

        for fn in zf.namelist():
            p1, sep, p2 = str(fn).rpartition('/')
            if p1 != '' and not os.path.isdir(os.path.join(crx_dir, p1)):
                os.mkdir(os.path.join(crx_dir, p1))

            if p2 == '':    # This was only a directory name
                continue

            with open(os.path.join(crx_dir, p1, p2), 'wb') as outfile:
                outfile.write(zf.read(fn))

if __name__ == "__main__":
    main(sys.argv)
