#!/usr/bin/env python2
from distutils.core import setup
setup(name='obMenux',
      version='1.1.24',
      description='Openbox Menu Editor X',
      author='SDE',
      author_email='sderaut@users.noreply.github.com',
      scripts=['obmenux'],
	  py_modules=['obxmlx'],
	  data_files=[('/usr/local/share/obmenux', ['gfx/obmenux.glade', 'gfx/mnu16.png', 'gfx/mnu48.png'])]
      )

