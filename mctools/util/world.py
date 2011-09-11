from StringIO import StringIO
import math
import os
import struct
import sys
import zlib

import nbt


class World(object):
    def __init__(self, name):
        self.world_dir = os.path.join(os.path.expanduser('~'), '.minecraft',
                                      'saves', name)

        self.level_filename = os.path.join(self.world_dir, 'level.dat')
        self.level_nbt = nbt.NBTFile(self.level_filename, 'rb')

    def get_player(self, name=None):
        nbt_data = None
        player_file = None

        if name:
            player_file = os.path.join(self.world_dir, 'players', name + '.dat')

            if os.path.exists(player_file):
                nbt_data = nbt.NBTFile(player_file, 'rb')
        elif 'Player' in self.level_nbt['Data']:
            nbt_data = self.level_nbt['Data']['Player']

        if nbt_data:
            return Player(player_file, nbt_data, name)

        return None

    def get_region_filename(self, pos):
        local_x = math.floor(pos[0] / 32)
        local_z = math.floor(pos[2] / 32)

        return os.path.join(self.world_dir, 'region',
                            'r.%d.%d.mcr' % (local_x, local_z))

    def get_region(self, filename=None, pos=None):
        if filename:
            return Region(filename)
        elif pos:
            return Region(self.get_region_filename(pos))
        else:
            return None


class Region(object):
    def __init__(self, filename):
        self.filename = filename
        self.locations = []
        self.timestamps = []
        self.chunks = []

        fp = open(self.filename, 'rb')
        data = fp.read()
        fp.close()

        locations = data[:4096]
        timestamps = data[4096:8192]
        chunks = data[8192:]

        for i in range(0, 4096, 4):
            loc_data = struct.unpack('>ib', '\00' + data[i:i+4])
            self.locations.append(loc_data)

        assert len(self.locations) == 1024

        for i in range(4096, 8192, 4):
            timestamp_data = struct.unpack('>i', data[i:i+4])
            self.timestamps.append(timestamp_data)

        assert len(self.timestamps) == 1024

        for loc, sector_count in self.locations:
            if loc != 0:
                loc = loc * 4096
                length, compression_type = struct.unpack('>ib', data[loc:loc+5])
                loc += 5
                compressed_data = data[loc:loc+length]

                if compression_type == 1:
                    # gzip
                    string_io = StringIO(compressed_data)
                    nbt_file = nbt.NBTFile(buffer=string_io)
                elif compression_type == 2:
                    # zlib
                    uncompressed = zlib.decompress(compressed_data)
                    string_io = StringIO(uncompressed)
                    nbt_file = nbt.NBTFile(buffer=string_io)
                    self.chunks.append({
                        'length': length,
                        'compression_type': compression_type,
                        'nbt': nbt_file,
                    })
                    #print nbt_file.pretty_tree()
                else:
                    sys.stderr.write('Unknown compression type %d' %
                                     compression_type)


class Player(object):
    def __init__(self, player_file, nbt, name=None):
        self.player_file = player_file
        self.nbt = nbt
        self.name = name

    def get_pos(self):
        pos = self.nbt['Pos'].tags

        return pos[0].value, pos[1].value, pos[2].value

    def get_chunk_pos(self):
        pos = self.get_pos()

        return pos[0] / 8, pos[1] / 8, pos[2] / 8
