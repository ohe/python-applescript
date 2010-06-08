# Copyright (c) 2010 Olivier Hervieu <olivier.hervieu@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""
Installation script for the python-applescript module.
"""

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, Extension
import sys, glob

sys.path.append('python')
import version as info

version = info.__version__
url = info.__url__
dl_url = info.__dl_url__
author = info.__author__
author_email = info.__authoremail__

long_description = '''
python-applescript is an extension to execute applescript commands on OS X.
'''

classifiers = """Development Status :: 3 - Alpha
License :: OSI Approved :: BSD License
Operating System :: MacOS :: MacOS X
Programming Language :: C
Programming Language :: Python
Topic :: Utilities
Topic :: Software Development :: Libraries""".split('\n')

pa_src = glob.glob('src/*.c')
pa_inc = glob.glob('src/*.h')
pa_incdir = None
pa_lib = None
pa_libdir = None
pa_link_args = ['-framework', 'Carbon']

module = Extension('applescript.applescript',
                    sources = pa_src,
                    depends = pa_inc,
                    include_dirs = pa_incdir,
                    library_dirs = pa_libdir,
                    libraries = pa_lib,
                    extra_link_args = pa_link_args)

setup(name='python-applescript',
      version=version,
      packages    = ['applescript'],
      package_dir = { 'applescript' : 'python'},
      description = 'python extension for applescript',
      author=author,
      author_email=author_email,
      url=url,
      download_url='%s/python-applescript-%s.tar.gz' % (dl_url, version),
      ext_modules = [module],
      license = 'MIT',
      platforms = ['MacOS X'],
      long_description = long_description,
      classifiers=classifiers)
