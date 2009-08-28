# Copyright (c) 2009 Olivier Hervieu <olivier.hervieu@gmail.com>
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
This example creates a file named "helloworld.txt" on your desktop.
"""


import applescript

script = """set desktop_path to (path to desktop as text)
try
    set new_file to (desktop_path & "helloworkd.txt") as alias
on error
    tell application "Finder" to make new file at alias desktop_path with properties {name:"helloworld.txt", creator type:"R*ch", file type:"TEXT"}
end try"""

if __name__ == '__main__':
    try:
        applescript.launch_script(script)
    except applescript.AppleScriptError:
        print "Oups! Somethings wrong happened"
