#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
import copy, random
from testfwk import create_config, run_test
from grid_control.backends import WMS
from grid_control.backends.broker_base import Broker
from python_compat import sorted


random.shuffle = lambda x: x.sort()
random.sample = lambda x, n: sorted(x)[:n]

req_base = [(WMS.WALLTIME, 123), (WMS.CPUTIME, 134), (WMS.MEMORY, 321), (WMS.CPUS, 3)]
queues_base = {
	'long1': {WMS.CPUTIME: 432000},
	'long2': {WMS.CPUTIME: 432000},
}

def create_broker(name, config_dict, items):
	random.seed(123)
	config = create_config(config_dict={'broker': config_dict})
	broker = config.get_composited_plugin('option', name, 'MultiBroker', cls=Broker, pargs=('items',),
		pkwargs={'req_type': WMS.BACKEND, 'discovery_fun': lambda: copy.deepcopy(items) or None})
	return broker

def check_req(broker, req_list, req_out=[]):
	if not broker.enabled():
		value = list(req_list)
	else:
		value = list(broker.process(list(req_list)))
	if value == req_list + req_out:
		return True
	print("REFERENCE: %s" % (req_list + req_out))
	print("PROCESSED: %s" % value)
	for (req_type, req_value) in value:
		if req_type == WMS.BACKEND:
			print("BACKEND: %s" % req_value)

def check_single_req(broker, req_list, req_out):
	value = list(broker.process(list(req_list)))
	if value == req_out:
		return True
	print("REFERENCE: %s" % req_out)
	print("PROCESSED: %s" % value)

class Test_Broker_FilterBroker:
	"""
	>>> broker = create_broker('FilterBroker', {}, {})
	>>> check_req(broker, req_base, [])
	True
	>>> broker = create_broker('FilterBroker', {}, queues_base)
	>>> check_req(broker, req_base, [])
	True

	>>> broker = create_broker('FilterBroker', {'items': 'a b c'}, {})
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', 'b', 'c'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'a -b -c'}, {})
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', '-b', '-c'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'a b c'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', 'b', 'c'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'a -b -c'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', '-b', '-c'])])
	True

	>>> broker = create_broker('FilterBroker', {'items': '-long1'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['-long1'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': '-long1'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['-long1'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': '-long1 -long2'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['-long1', '-long2'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': '-long1 -long2'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['-long1', '-long2'])])
	True

	>>> broker = create_broker('FilterBroker', {'items': 'long1 long2'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1', 'long2'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'long2 long1'}, {})
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long2', 'long1'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'long1 long2'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1', 'long2'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'long2 long1'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long2', 'long1'])])
	True

	>>> broker = create_broker('FilterBroker', {'items': 'long1 -long2 long3'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1', '-long2', 'long3'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'long1 -long2 long3'}, {})
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1', '-long2', 'long3'])])
	True
	>>> broker = create_broker('FilterBroker', {'items': 'long1 -long2 long3'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1', '-long2', 'long3'])])
	True
	"""

class Test_RandomLimitBroker:
	"""
	>>> broker = create_broker('FilterBroker RandomBroker LimitBroker', {'items': 'a b c', 'items entries': '0'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', 'b', 'c'])])
	True
	>>> broker = create_broker('FilterBroker RandomBroker LimitBroker', {'items': 'a b c', 'items entries': '2'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', 'b'])])
	True
	>>> broker = create_broker('FilterBroker RandomBroker LimitBroker', {'items': 'a b c', 'items entries': '2', 'items randomize': 'True'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', 'b'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a', 'b'])])
	True
	>>> broker = create_broker('FilterBroker RandomBroker LimitBroker', {'items': 'a b c', 'items randomize': 'True'}, None)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['a'])])
	True
	"""

class Test_Broker_CoverageBroker:
	"""
	>>> broker = create_broker('CoverageBroker', {}, {})
	>>> check_req(broker, req_base, [(WMS.BACKEND, None)])
	True

	>>> broker = create_broker('CoverageBroker', {}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long2'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True

	>>> broker = create_broker('FilterBroker CoverageBroker', {'items': 'ekpplus001 ekpplus002 ekpplus003 ekpplus004'}, {})
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['ekpplus001'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['ekpplus002'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['ekpplus003'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['ekpplus004'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['ekpplus001'])])
	True

	>>> broker = create_broker('FilterBroker CoverageBroker', {'items': 'long1 -long2 long3'}, {})
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long3'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True

	>>> broker = create_broker('CoverageBroker', {'items': 'long1 long2 long3'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long2'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True

	>>> broker = create_broker('FilterBroker CoverageBroker', {'items': 'long1 long2 long3'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long2'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long3'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True

	>>> broker = create_broker('FilterBroker CoverageBroker', {'items': 'long1 long3'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long3'])])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, ['long1'])])
	True

	>>> broker = create_broker('FilterBroker CoverageBroker', {'items': '-long2'}, queues_base)
	>>> check_req(broker, req_base, [(WMS.BACKEND, None)])
	True
	>>> check_req(broker, req_base, [(WMS.BACKEND, None)])
	True
	"""

req0 = []
req1 = [(WMS.WALLTIME, 423), (WMS.CPUTIME, 234), (WMS.MEMORY, 321), (WMS.CPUS, 3)]
req2 = [(WMS.WALLTIME, 42300), (WMS.CPUTIME, 23400), (WMS.MEMORY, 321), (WMS.CPUS, 3)]
req3 = [(WMS.WALLTIME, 122300), (WMS.CPUTIME, 93400), (WMS.MEMORY, 321), (WMS.CPUS, 3)]
req4 = [(WMS.WALLTIME, 1223000), (WMS.CPUTIME, 934000), (WMS.MEMORY, 321), (WMS.CPUS, 3)]
req4 = [(WMS.WALLTIME, 1223000), (WMS.CPUTIME, 934000), (WMS.MEMORY, 321), (WMS.CPUS, 3)]
req5 = [(WMS.STORAGE, None)]
req6 = [(WMS.STORAGE, [])]
req7 = [(WMS.STORAGE, ['a', 'b', 'c'])]

queues1 = {
	'longl': {WMS.CPUTIME: 432000},
	'longs': {WMS.CPUTIME: 430000},
}
queues2 = {
	'long1': {WMS.WALLTIME: 987, WMS.CPUTIME: 123},
	'long2': {WMS.WALLTIME: 123, WMS.CPUTIME: 987},
}
queues3 = {
	'medium': {WMS.WALLTIME: 86700, WMS.CPUTIME: 28740},
	'long': {WMS.CPUTIME: 432000},
	'infinite': {},
	'short': {WMS.WALLTIME: 11100, WMS.CPUTIME: 3600},
	'io_only': {WMS.CPUTIME: 432000},
	'test': {WMS.WALLTIME: 86700, WMS.CPUTIME: 28740}
}
queues4 = {
	'q_all1': {},
	'q_all2': {WMS.STORAGE: None},
	'q_ab': {WMS.STORAGE: ['a', 'b']},
	'q_cd': {WMS.STORAGE: ['c', 'd']},
	'q_xy': {WMS.STORAGE: ['x', 'y']},
}

class Test_Broker_StorageBroker:
	"""
	>>> broker = create_broker('StorageBroker', {'items storage access': '1 2 3\\na=>x\\nb=>y -z'}, [])
	>>> check_req(broker, req0)
	True
	>>> check_req(broker, req5)
	True
	>>> check_req(broker, req6)
	True
	>>> check_req(broker, req7, [(WMS.BACKEND, ['x', 'y', '-z', '1', '2', '3'])])
	True
	"""

class Test_Broker_SimpleBroker:
	"""
	>>> broker = create_broker('SimpleBroker', {}, {})
	>>> check_req(broker, req0, [])
	True
	>>> check_req(broker, req1, [])
	True
	>>> check_req(broker, req2, [])
	True
	>>> check_req(broker, req3, [])
	True
	>>> check_req(broker, req4, [])
	True
	>>> check_req(broker, req5, [])
	True
	>>> check_req(broker, req6, [])
	True
	>>> check_req(broker, req7, [])
	True

	>>> broker = create_broker('SimpleBroker', {}, queues1)
	>>> check_req(broker, req0, [(WMS.BACKEND, ['longs', 'longl'])])
	True
	>>> check_req(broker, req1, [(WMS.BACKEND, ['longs', 'longl'])])
	True
	>>> check_req(broker, req2, [(WMS.BACKEND, ['longs', 'longl'])])
	True
	>>> check_req(broker, req3, [(WMS.BACKEND, ['longs', 'longl'])])
	True
	>>> check_req(broker, req4, [(WMS.BACKEND, [])])
	True
	>>> check_req(broker, req5, [(WMS.BACKEND, ['longs', 'longl'])])
	True
	>>> check_req(broker, req6, [(WMS.BACKEND, ['longs', 'longl'])])
	True
	>>> check_req(broker, req7, [(WMS.BACKEND, ['longs', 'longl'])])
	True

	>>> broker = create_broker('SimpleBroker', {}, queues2)
	>>> check_req(broker, req0, [(WMS.BACKEND, ['long2', 'long1'])])
	True
	>>> check_req(broker, req1, [(WMS.BACKEND, [])])
	True
	>>> check_req(broker, req2, [(WMS.BACKEND, [])])
	True
	>>> check_req(broker, req3, [(WMS.BACKEND, [])])
	True
	>>> check_req(broker, req4, [(WMS.BACKEND, [])])
	True
	>>> check_req(broker, req5, [(WMS.BACKEND, ['long2', 'long1'])])
	True
	>>> check_req(broker, req6, [(WMS.BACKEND, ['long2', 'long1'])])
	True
	>>> check_req(broker, req7, [(WMS.BACKEND, ['long2', 'long1'])])
	True

	>>> broker = create_broker('SimpleBroker', {}, queues3)
	>>> check_req(broker, req0, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req1, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req2, [(WMS.BACKEND, ['medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req3, [(WMS.BACKEND, ['io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req4, [(WMS.BACKEND, ['infinite'])])
	True
	>>> check_req(broker, req5, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req6, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req7, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True

	>>> broker = create_broker('FilterBroker SimpleBroker', {'items': 'medium infinite short'}, queues3)
	>>> check_req(broker, req0, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req1, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req2, [(WMS.BACKEND, ['medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req3, [(WMS.BACKEND, ['io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req4, [(WMS.BACKEND, ['infinite'])])
	True
	>>> check_req(broker, req5, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req6, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	>>> check_req(broker, req7, [(WMS.BACKEND, ['short', 'medium', 'test', 'io_only', 'long', 'infinite'])])
	True
	"""

class Test_FinalBroker:
	"""
	>>> broker = Broker.create_instance('FinalBroker', create_config(), 'test', 'test')
	>>> check_single_req(broker, [(WMS.WALLTIME, 100), (WMS.WALLTIME, 120), (WMS.WALLTIME, 110)], [(WMS.WALLTIME, 120)])
	True
	>>> check_single_req(broker, [(WMS.CPUTIME, 100), (WMS.CPUTIME, 120), (WMS.CPUTIME, 110)], [(WMS.CPUTIME, 120)])
	True
	>>> check_single_req(broker, [(WMS.MEMORY, 100), (WMS.MEMORY, 120), (WMS.MEMORY, 110)], [(WMS.MEMORY, 120)])
	True
	>>> check_single_req(broker, [(WMS.CPUS, 1), (WMS.CPUS, 2), (WMS.CPUS, 1)], [(WMS.CPUS, 2)])
	True
	>>> check_single_req(broker, [(WMS.ARRAY_SIZE, 1), (WMS.ARRAY_SIZE, 2), (WMS.ARRAY_SIZE, 1)], [(WMS.ARRAY_SIZE, 2)])
	True
	>>> check_single_req(broker, [(WMS.SITES, None), (WMS.SITES, ['C', 'D']), (WMS.SITES, []), (WMS.SITES, ['A', 'B'])], [(WMS.SITES, ['A', 'B', 'C', 'D'])])
	True
	>>> check_single_req(broker, [(WMS.QUEUES, None), (WMS.QUEUES, ['C', 'D']), (WMS.QUEUES, []), (WMS.QUEUES, ['A', 'B'])], [(WMS.QUEUES, ['A', 'B', 'C', 'D'])])
	True
	>>> check_single_req(broker, [(WMS.STORAGE, None), (WMS.STORAGE, ['C', 'D']), (WMS.STORAGE, []), (WMS.STORAGE, ['A', 'B'])], [(WMS.STORAGE, ['A', 'B', 'C', 'D'])])
	True
	"""

run_test()
