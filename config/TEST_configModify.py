#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
from testfwk import create_config, run_test, testfwk_remove_files, try_catch
from testfwk_config import create_hcv
from grid_control.config.cinterface_typed import SimpleConfigInterface


def test_get_plugin(cur, old=None, old_dict=None, cur_dict=None, **kwargs):
	old_dict = old_dict or {}
	cur_dict = cur_dict or {}
	old_dict['key'] = old
	cur_dict['key'] = cur
	hcv = create_hcv(cur_dict, old_dict, print_dict=False)
	config = SimpleConfigInterface(hcv)
	return config.get_plugin('key', **kwargs)

class Test_Config:
	"""
	>>> testfwk_remove_files(['work.test_mod/*', 'work.test_mod'])
	>>> config1 = create_config('test_mod.conf')
	>>> print(config1.get('key1', 'k1_def'))
	k1_v1
	k1_v2
	>>> print(config1.get('key2', 'k2_def'))
	k2_def
	k2_v1
	>>> config1_a = config1.change_view(set_sections=['mod', 'section'])
	>>> tmp = config1_a.set('key3', 'k3_v2', '+=')
	>>> print(config1_a.get('key3', 'k3_def'))
	k3_v1
	k3_def
	k3_v2

	>>> config1.factory.freeze()
	>>> try_catch(lambda: config1_a.set('key  fail', 'value'), 'APIError', 'Config container is read-only')
	caught

	>>> config2 = create_config('test_mod.conf')
	>>> print(config2.get('key1', 'k1_def'))
	k1_v1
	k1_v2
	>>> print(config2.get('key2', 'k2_def'))
	k2_def
	k2_v1
	>>> config2_a = config2.change_view(set_sections=['mod', 'section'])
	>>> tmp = config2_a.set('key3', 'k3_v2', '+=')
	>>> print(config2_a.get('key3', 'k3_def'))
	k3_v1
	k3_def
	k3_v2

	>>> testfwk_remove_files(['work.test_mod/*', 'work.test_mod'])

	>>> test_get_plugin('id', pargs=('1-3',))
	<id:1-3>
	>>> test_get_plugin('IDSelector', pargs=('1-3',))
	<id:1-3>
	>>> test_get_plugin('IDSelector', 'IDSelector', pargs=('1-3',))
	<id:1-3>
	>>> test_get_plugin('id', 'id', pargs=('1-3',))
	<id:1-3>
	>>> test_get_plugin('IDSelector', 'id', pargs=('1-3',))
	<id:1-3>
	>>> test_get_plugin('id', 'IDSelector', pargs=('1-3',))
	<id:1-3>
	>>> test_get_plugin('id', 'state', pargs=('1-3',), on_change=None)
	<id:1-3>
	>>> try_catch(lambda: test_get_plugin('id', 'state', pargs=('1-3',)), 'ConfigError', 'possible to change')
	caught

	>>> test_get_plugin('shell', pargs=('1-3', 'key'), cls='Matcher')
	ShellStyleMatcher(case sensitive = 'key')
	>>> test_get_plugin('ShellStyleMatcher', pargs=('1-3', 'key'), cls='Matcher')
	ShellStyleMatcher(case sensitive = 'key')
	>>> test_get_plugin('ShellStyleMatcher', 'shell', pargs=('1-3', 'key'), cls='Matcher')
	ShellStyleMatcher(case sensitive = 'key')
	>>> test_get_plugin('shell', 'ShellStylematcher', pargs=('1-3', 'key'), cls='Matcher')
	ShellStyleMatcher(case sensitive = 'key')
	>>> test_get_plugin('shell', 'blackwhite', pargs=('1-3', 'key'), cls='Matcher', on_change=None)
	ShellStyleMatcher(case sensitive = 'key')
	>>> try_catch(lambda: test_get_plugin('shell', 'blackwhite', pargs=('1-3', 'key'), cls='Matcher'), 'ConfigError', 'possible to change')
	caught
	"""

run_test()
