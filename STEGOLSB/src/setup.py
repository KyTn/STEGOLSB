from distutils.core import setup
import py2exe

data = [('images', ['C:\src/images/no-image.png'])]
setup(console=['GUI.py'],data_files = data)