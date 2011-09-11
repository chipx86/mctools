from optparse import OptionParser
import os
import sys

import nbt

from mctools.util.world import World


def parse_options(args):
    parser = OptionParser()
    parser.add_option('-w', '--world',
                      dest='world',
                      metavar='NAME',
                      default=None,
                      help='The name of the world')
    parser.add_option('-p', '--player',
                      dest='player',
                      metavar='NAME',
                      default=None,
                      help='The player name used to find the chunk')

    options, args = parser.parse_args(args)

    if not options.world:
        sys.stderr.write('A world must be specified.\n')
        sys.exit(1)

    return options


def main():
    options = parse_options(sys.argv[1:])

    world = World(options.world)
    player = world.get_player(options.player)

    if not player:
        sys.stderr.write('No data found for the player\n')
        sys.exit(1)

    print world.get_region_filename(player.get_chunk_pos())
