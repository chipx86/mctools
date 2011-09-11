from optparse import OptionParser
import os
import sys

import nbt

from mctools.util.data import BLOCK_IDS
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
    parser.add_option('-r', '--region-file',
                      dest='region_file',
                      metavar='FILENAME',
                      default=None,
                      help='The region filename used')

    options, args = parser.parse_args(args)

    if not options.world:
        sys.stderr.write('A world must be specified.\n')
        sys.exit(1)

    return options


def main():
    options = parse_options(sys.argv[1:])

    world = World(options.world)

    if options.region_file:
        region = world.get_region(filename=options.region_file)
    else:
        player = world.get_player(options.player)

        if not player:
            sys.stderr.write('No data found for the player\n')
            sys.exit(1)

        region = world.get_region(pos=player.get_chunk_pos())

    found_entities = []

    for chunk in region.chunks:
        if chunk:
            nbt_data = chunk['nbt']
            entities = nbt_data['Level']['Entities']
            #print nbt_data.pretty_tree()

            for entity in entities.tags:
                if entity['id'].value == 2:
                    print 'XXX'

                found_entities.append(entity)

            if 'Blocks' in nbt_data['Level']:
                blocks_data = nbt_data['Level']['Blocks'].value
                extra_data = nbt_data['Level']['Data'].value

                for i, block_id in enumerate(blocks_data):
                    block_id = ord(block_id)

#                    if i == 0 and ord(extra_data[i]) != 0: # AIR
#                        print ord(extra_data[i])

#                    if block_id not in BLOCK_IDS:
#                        print block_id
                    #print BLOCK_IDS.get(block_id, 'Unknown (%s)' % block_id)

    return
    for entity in found_entities:
        entity_id = entity['id'].value

        if 'Item' in entity:
            item_id = entity['Item']['id'].value
            if 1 or item_id not in BLOCK_IDS:
                item_count = entity['Item']['Count'].value
                print '%s - %s - %s' % (entity_id, BLOCK_IDS.get(item_id, 'Unknown (%s)' % item_id), item_count)
#        else:
#            print entity_id
