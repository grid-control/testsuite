#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
from grid_control.config.config_entry import ConfigContainer, ConfigEntry
from grid_control.config.cview_base import SimpleConfigView


def create_hcv(cur={}, old=None, print_dict=True):
	if print_dict:
		print('cur = %r\nold = %r' % (cur, old))
	def fill(container, values):
		for key in values or {}:
			if values[key] is not None:
				container.append(ConfigEntry('x', key, values[key], '=', 'x'))

	container_cur = ConfigContainer('cur')
	fill(container_cur, cur)
	container_old = ConfigContainer('old')
	fill(container_old, old)
	if old == None:
		container_old.enabled = False
	hcv = SimpleConfigView('view', container_old, container_cur)
	hcv._get_section = lambda *args, **kwargs: 'x'
	hcv._get_section_key = lambda x: x
	return hcv
