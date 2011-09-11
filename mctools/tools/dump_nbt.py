import os
import sys

import nbt


def main():
    for filename in sys.argv[1:]:
        nbt_file = nbt.NBTFile(filename, 'rb')

        print nbt_file.pretty_tree()
