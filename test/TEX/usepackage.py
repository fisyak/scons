#!/usr/bin/env python
#
# MIT License
#
# Copyright The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r"""
Validate that we can set the LATEX string to our own utility, that
the produced .dvi, .aux and .log files get removed by the -c option,
and that we can use this to wrap calls to the real latex utility.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

latex = test.where_is('latex')

if not latex:
    test.skip_test("could not find 'latex'; skipping test\n")

test.write('SConstruct', """
import os

_ = DefaultEnvironment(tools=[])
foo = Environment()
foo['TEXINPUTS'] = [ 'subdir', os.environ.get('TEXINPUTS', '') ]
foo.DVI(target = 'foo.dvi', source = 'foo.ltx')
""")

test.write('foo.ltx', r"""
\documentclass{letter}
\usepackage{bar}
\begin{document}
This is the foo.ltx file.
\end{document}
""")

test.write('bar.sty', "\n")

test.run(arguments = 'foo.dvi', stderr = None)

test.write('bar.sty', "\n\n\n")

test.not_up_to_date(arguments = 'foo.dvi', stderr = None)



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
