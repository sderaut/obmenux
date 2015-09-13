#!/usr/bin/env python2
import os, sys
from distutils.core import setup

if os.path.isfile('cleaner.py') and os.path.isdir('build'):
	os.system('python2 cleaner.py clean --all') # remove previous ./build/

libdir = 'share/obmenux'
sys.path += [os.path.join(os.curdir, libdir)]

setup(name='obmenux',
      version='1.1.25',
      description='Openbox Menu Editor X',
      license='GPL',
      url='https://github.com/sderaut/obmenux',
      author='SDE',
      author_email='sderaut@users.noreply.github.com',
      scripts=['obmenux', 'pipes/obmx-xdg','pipes/obmx-dir','pipes/obmx-moz',
               'pipes/obmx-nav'],
      py_modules=['obxmlx'],
      data_files=[(libdir,
                   ['gfx/obmenux.glade', 'gfx/mnu16.png','gfx/mnu48.png'])])
