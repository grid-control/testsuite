#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), ''))
__import__('testfwk').setup(__file__, None)
# - prolog marker
import os
from testfwk import TestsuiteStream, run_test
from grid_control_gui.ansi import ANSI


def display():
	TestsuiteStream(True).write(ANSI.color_grayscale(0.5) + 'TEST' + ANSI.reset)

if os.environ.get('GC_TERM') == 'dumb':
	class Test_ANSI(object):
		"""
		>>> display()
		TEST
		"""

elif os.environ.get('GC_TERM') == 'gc_color16':
	class Test_ANSI(object):
		"""
		>>> display()
		<reset><color_white>TEST<reset>
		"""

elif os.environ.get('GC_TERM') == 'gc_color256':
	class Test_ANSI(object):
		"""
		>>> display()
		<grayscale:243>TEST<reset>
		"""

run_test()
