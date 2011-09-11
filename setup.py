#!/usr/bin/env python
#
# setup.py -- Installation for mctools.
#
# Copyright (C) 2011 Christian Hammond
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.test import test


PACKAGE_NAME = 'MCTools'


setup(name=PACKAGE_NAME,
      version="0.4.0",
      license="MIT",
      description="Command line tools for working with Minecraft files",
      entry_points = {
          'console_scripts': [
              'mc-get-region-file = mctools.tools.get_region_file:main',
              'mc-list-entities = mctools.tools.list_entities:main',
              'mc-dump-nbt = mctools.tools.dump_nbt:main',
              'mc-dump-region = mctools.tools.dump_region:main',
          ],
      },
      install_requires=[
          'NBT',
      ],
      packages=find_packages(),
      include_package_data=True,
      maintainer="Christian Hammond",
      maintainer_email="chipx86@chipx86.com",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Utilities",
      ]
)
