import os
import sys

import nbt

from mctools.util.world import Region


def main():
    for filename in sys.argv[1:]:
        region = Region(filename)

        for chunk in region.chunks:
            if chunk:
                print chunk['nbt'].pretty_tree()
