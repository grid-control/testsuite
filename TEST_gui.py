#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), ''))
__import__('testfwk').setup(__file__)
# - prolog marker
import logging
from testfwk import TestsuiteStream, cleanup_workflow, create_config, run_test, testfwk_create_workflow, try_catch
from grid_control.gui import GUI
from grid_control.stream_base import ActivityMonitor
from grid_control.utils.activity import Activity
from grid_control.utils.thread_tools import GCEvent
from grid_control_gui.ansi import ANSI, Console
from grid_control_gui.ge_base import GUIElement


def log_stuff():
	msg_list = ['SUCCESS', 'TEST'*10, 'SUCCESS', 'DONE'] * 20
	for msg in msg_list:
		logging.getLogger().info(msg)


class Test_GUI(object):
	"""
	>>> workflow = testfwk_create_workflow({'jobs': {'jobs': 1}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---

	>>> gui = GUI.create_instance('GUI', create_config(), workflow)
	>>> gui.start_interface()
	>>> gui.end_interface()

	>>> redraw_event = GCEvent()
	>>> std_stream = TestsuiteStream(display_commands=True)
	>>> ge_base = GUIElement.create_instance('GUIElement', create_config(), 'name', workflow, redraw_event, std_stream)
	>>> try_catch(lambda: ge_base.get_height(), 'AbstractError')
	caught
	>>> try_catch(lambda: ge_base.redraw(), 'AbstractError')
	caught
	>>> span = GUIElement.create_instance('SpanGUIElement', create_config(), 'name', workflow, redraw_event, std_stream)
	>>> span.get_height()
	>>> user_log = GUIElement.create_instance('UserLogGUIElement', create_config(config_dict={'global': {'log dump': False}}), 'name', workflow, redraw_event, std_stream)
	>>> user_log.set_layout(2, 6, 30)
	>>> user_log.draw_startup()
	<erase_line><newline>
	<erase_line><newline>
	<erase_line><newline>
	<erase_line><newline>
	<erase_line><newline>
	<erase_line>
	>>> log_stuff()
	>>> user_log.redraw()
	<move:3,1>
	<bold><color_cyan>DONE<reset><reset><erase_line><newline>
	<bold><color_green>SUCCESS<reset><reset><erase_line><newline>
	TESTTESTTESTTESTTESTTESTTESTTE<reset><erase_line><newline>
	STTESTTEST<reset><erase_line><newline>
	<bold><color_green>SUCCESS<reset><reset><erase_line><newline>
	<bold><color_cyan>DONE<reset><reset><erase_line>
	>>> user_log.draw_finish()

	>>> activity_log = GUIElement.create_instance('ActivityGUIElement', create_config(config_dict={'global': {'activity interval': 0, 'activity stream': 'timed_stream'}}), 'name', workflow, redraw_event, std_stream)
	>>> activity_log.set_layout(41, 2, 30)
	>>> activity_log.draw_startup()
	<erase_line><newline>
	<erase_line>
	>>> activity_log.redraw()
	<move:42,1>
	<erase_line><newline>
	<erase_line>
	>>> activity1 = Activity('working1')
	>>> activity_log.redraw()
	<move:42,1>
	working1...<reset><erase_line><newline>
	<erase_line>
	>>> activity2 = Activity('working2')
	>>> activity_log.redraw()
	<move:42,1>
	working1...<reset><erase_line><newline>
	working2...<reset><erase_line>
	>>> activity3 = Activity('working3')
	>>> activity_log.redraw()
	<move:42,1>
	working1...<reset><erase_line><newline>
	working2...<reset><erase_line>
	>>> activity_log.set_layout(41, 3, 30)
	>>> activity_log.redraw()
	<move:42,1>
	<grayscale:250>working1...<reset><erase_line><reset><erase_line><newline>
	<grayscale:250>working2...<reset><erase_line><reset><erase_line><newline>
	<grayscale:250>working3...<reset><erase_line><reset><erase_line>
	>>> activity1.finish()
	>>> activity2.finish()
	>>> activity3.finish()
	>>> activity_log.redraw()
	>>> activity_log.draw_finish()
	"""


class Test_Stream(object):
	"""
	>>> std_stream = TestsuiteStream()
	>>> activity = Activity('work ongoing')
	>>> try_catch(lambda: ActivityMonitor.create_instance('ActivityMonitor', create_config(), std_stream).write('Hallo'), 'AbstractError', 'is an abstract function')
	caught
	>>> stream1 = ActivityMonitor.create_instance('null', create_config())
	>>> stream1.write('Hallo\\n')
	>>> stream1.write('Welt\\n')
	>>> stream1.flush()

	>>> std_stream = TestsuiteStream(display_commands=True)
	>>> stream2 = ActivityMonitor.create_instance('single_stream', create_config(), std_stream)
	>>> stream2.write('Hallo\\n')
	Hallo<newline>
	work ongoing...
	>>> stream2.write('Welt\\n')
	-----
	-----
	Welt<newline>
	work ongoing...
	>>> stream2.flush()

	>>> Console.getmaxyx()  # default
	(24, 80)
	>>> stream3 = ActivityMonitor.create_instance('multi_stream', create_config(config_dict={'global': {'activity fold fraction': 0.1}}), std_stream)
	>>> stream3.write('Hallo\\n')
	Hallo<erase_line><newline>
	<erase_line><newline>
	<wrap_off>
	<erase_line><grayscale:255>work ongoing...<reset><newline>
	<erase_down><move_up:2><wrap_on>

	>>> stream3.write('Welt\\n')
	Welt<erase_line><newline>
	<erase_line><newline>
	<wrap_off>
	<erase_line><grayscale:255>work ongoing...<reset><newline>
	<erase_down><move_up:2><wrap_on>

	>>> activity1 = Activity('nested work ongoing', name='a1')
	>>> activity2 = Activity('nested nested work ongoing')
	>>> activity3 = Activity('nested nested nested work ongoing')
	>>> stream3.write('')
	<newline>
	<wrap_off>
	<erase_line><grayscale:255>work ongoing...<reset><newline>
	<erase_line>  <grayscale:250>nested work ongoing...<reset><newline>
	<erase_down><move_up:3><wrap_on>

	>>> stream3 = ActivityMonitor.create_instance('multi_stream', create_config(config_dict={'global': {'activity fold fraction': 0.5}}), std_stream)
	>>> stream3.write('')
	<newline>
	<wrap_off>
	<erase_line><grayscale:255>work ongoing...<reset><newline>
	<erase_line>  <grayscale:250>nested work ongoing...<reset><newline>
	<erase_line>    <grayscale:245>nested nested work ongoing...<reset><newline>
	<erase_line>      <grayscale:241>nested nested nested work ongoing...<reset><newline>
	<erase_down><move_up:5><wrap_on>

	>>> activity2x = Activity('2nd nested nested work ongoing', parent='a1')
	>>> stream3.write('')
	<newline>
	<wrap_off>
	<erase_line><grayscale:255>work ongoing...<reset><newline>
	<erase_line>  <grayscale:250>nested work ongoing...<reset><newline>
	<erase_line>    <grayscale:245>nested nested work ongoing...<reset><newline>
	<erase_line>      <grayscale:241>nested nested nested work ongoing...<reset><newline>
	<erase_line>    <grayscale:245>2nd nested nested work ongoing...<reset><newline>
	<erase_down><move_up:6><wrap_on>

	>>> stream4 = ActivityMonitor.create_instance('multi_stream', create_config(config_dict={'global': {'activity fold fraction': 0.2}}), std_stream)
	>>> stream4.write('')
	<newline>
	<wrap_off>
	<erase_line><grayscale:255>work ongoing...<reset><newline>
	<erase_line>  <grayscale:250>nested work ongoing...<reset><newline>
	<erase_line>    <grayscale:245>nested nested work ongoing...<reset><newline>
	<erase_line>    <grayscale:245>2nd nested nested work ongoing...<reset><newline>
	<erase_down><move_up:5><wrap_on>

	>>> activity.finish()
	"""

class Test_ANSI(object):
	"""
	>>> tmp = '\x1b[0m\x1b[34mHello\x1b[0m'
	>>> ANSI.strip_fmt(tmp)
	'Hello'
	"""

run_test(cleanup_fun=cleanup_workflow)
