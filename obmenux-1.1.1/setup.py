#!/usr/bin/env python2
import os, sys, glob
from distutils.core import setup

libdir = 'share/obmenux'
sys.path += [os.path.join(os.curdir, libdir)]

setup(name='obMenux',
      version='1.1.1',
      description='Openbox Menu Editor X',
      license='GPL',
      url='https://github.com/sderaut/obmenux',
      author='SDE',
      author_email='sderaut@users.noreply.github.com',
      scripts=['obmenux', 'pipes/obmx-xdg','pipes/obmx-dir','pipes/obmx-moz','pipes/obmx-nav'],
      py_modules=['obxmlx'],
      data_files=[(libdir, ['obmenux.glade', 'icons/mnu16.png','icons/mnu48.png'])]
      )
