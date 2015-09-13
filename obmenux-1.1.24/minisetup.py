#!/usr/bin/env python2
from distutils.core import setup
import os

if os.path.isfile('cleaner.py') and os.path.isdir('build'):
	os.system('python2 cleaner.py clean --all') # remove previous ./build/

setup(name='obmenux',
      version='1.1.25',
      description='Openbox Menu Editor X',
      author='SDE',
      author_email='sderaut@users.noreply.github.com',
      scripts=['obmenux'],
	  py_modules=['obxmlx'],
	  data_files=[('/usr/local/share/obmenux',
	               ['gfx/obmenux.glade', 'gfx/mnu16.png', 'gfx/mnu48.png'])])
