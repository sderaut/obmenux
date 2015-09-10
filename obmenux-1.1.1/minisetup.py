#!/usr/bin/env python2
from distutils.core import setup
setup(name='obMenux',
      version='1.0',
      description='Openbox Menu Editor X',
      author='SDE',
      author_email='sderaut@users.noreply.github.com',
      scripts=['obmenux'],
	  py_modules=['obxmlx'],
	  data_files=[('/usr/local/share/obmenux', ['obmenux.glade', 'icons/mnu16.png', 'icons/mnu48.png'])]
      )

