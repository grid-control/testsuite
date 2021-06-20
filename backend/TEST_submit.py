#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
import os, logging
from testfwk import create_config, run_test, testfwk_set_path, try_catch
from grid_control.backends import WMS
from grid_control.backends.aspect_submit import LocalSubmitWithProcess
from python_compat import sorted


testfwk_set_path('../bin')

def test_submit(plugin, exec_fn, src, req_list=None, **kwargs):
	for option in list(kwargs):
		if '_' in option:
			kwargs[option.replace('_', ' ')] = kwargs.pop(option)
	config = create_config(config_dict={'global': kwargs or {}})
	executor = LocalSubmitWithProcess.create_instance(plugin, config, exec_fn)
	executor.setup(logging.getLogger())
	os.environ['GC_TEST_FILE'] = src
	print(executor.get_array_key_list())
	print(executor._get_submit_arguments('GC000000000000', 'GC00000000.0',
		'/bin/hostname', req_list or [], '/dev/stdout', '/dev/stderr'))
	print(repr(executor.submit('GC000000000000', 'GC00000000.0',
		'/bin/hostname', req_list or [], '/dev/stdout', '/dev/stderr')))

req_list_1 = sorted({
	WMS.WN: ['site1', 'site2'],
	WMS.QUEUES: ['localqueue', 'localqueue1'],
	WMS.SOFTWARE: 'my-software-tag',
}.items())

req_list_2 = sorted({
	WMS.MEMORY: 1234,
	WMS.CPUTIME: 456,
	WMS.WALLTIME: 789,
}.items())

req_list_3 = sorted({
	WMS.QUEUES: ['localqueue', 'localqueue1'],
	WMS.ARRAY_SIZE: 1,
}.items())

req_list_4 = sorted({
	WMS.WN: ['site1', 'site2'],
	WMS.ARRAY_SIZE: 2,
}.items())

software_req_map = '-l TEST=DEFAULT\nmy-software-tag => -l TEST=MYREQ'

class Test_Base:
	"""
	>>> try_catch(lambda: test_submit('LocalSubmitWithProcess', '/bin/sh', '/dev/null'), 'AbstractError', '_get_submit_arguments is an abstract function')
	None
	caught
	"""

class Test_ARC:
	"""
	"""

class Test_Condor:
	"""
	"""

class Test_CREAM:
	"""
	"""

class Test_GliteWMS:
	"""
	"""

class Test_GridEngine:
	"""
	>>> test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit1')
	['SGE_TASK_ID']
	['-r', 'n', '-notify', '-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'424992'
	>>> test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit1', project_name='myproject')
	['SGE_TASK_ID']
	['-r', 'n', '-notify', '-P', 'myproject', '-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'424992'
	>>> test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit1', req_list_1, software_requirement_map=software_req_map)
	['SGE_TASK_ID']
	['-r', 'n', '-notify', '-q', 'localqueue@site1,localqueue@site2', '-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-l', 'TEST=MYREQ', '/bin/hostname']
	'424992'
	>>> test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit1', req_list_2, software_requirement_map=software_req_map)
	['SGE_TASK_ID']
	['-r', 'n', '-notify', '-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-l', 'TEST=DEFAULT', '-l', 's_rt=00:13:09', '-l', 'h_cpu=00:07:36', '-l', 'h_vmem=1234M', '/bin/hostname']
	'424992'
	>>> test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit1', req_list_2)
	['SGE_TASK_ID']
	['-r', 'n', '-notify', '-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-l', 's_rt=00:13:09', '-l', 'h_cpu=00:07:36', '-l', 'h_vmem=1234M', '/bin/hostname']
	'424992'
	>>> test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit1', req_list_3)
	['SGE_TASK_ID']
	['-r', 'n', '-notify', '-q', 'localqueue', '-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'424992'
	>>> try_catch(lambda: test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit1', req_list_4), 'ConfigError', 'Please also specify queue when selecting nodes')
	['SGE_TASK_ID']
	caught
	>>> test_submit('GridEngineSubmit', 'qsub', 'test.GridEngine.submit2')
	['SGE_TASK_ID']
	['-r', 'n', '-notify', '-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	Unable to parse wms id: 'FAIL'
	None
	"""

class Test_Host:
	"""
	>>> test_submit('HostSubmit', 'gc-wrapper-host', 'test.Host.submit')
	None
	['/dev/stdout', '/dev/stderr', '/bin/hostname']
	'12345'
	>>> test_submit('HostSubmit', 'gc-wrapper-host', 'test.Host.submit', req_list_1)
	None
	['/dev/stdout', '/dev/stderr', '/bin/hostname']
	'12345'
	>>> test_submit('HostSubmit', 'gc-wrapper-host', 'test.Host.submit', req_list_2)
	None
	['/dev/stdout', '/dev/stderr', '/bin/hostname']
	'12345'
	>>> test_submit('HostSubmit', 'gc-wrapper-host', 'test.Host.submit', req_list_3)
	None
	['/dev/stdout', '/dev/stderr', '/bin/hostname']
	'12345'
	>>> test_submit('HostSubmit', 'gc-wrapper-host', 'test.Host.submit', req_list_4)
	None
	['/dev/stdout', '/dev/stderr', '/bin/hostname']
	'12345'
	"""

class Test_JMS:
	"""
	>>> test_submit('JMSSubmit', 'job_submit', 'test.JMS.submit')
	None
	['-J', 'GC00000000.0', '-p', 1, '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'121195'
	>>> test_submit('JMSSubmit', 'job_submit', 'test.JMS.submit', req_list_1)
	None
	['-J', 'GC00000000.0', '-p', 1, '-o', '/dev/stdout', '-e', '/dev/stderr', '-c', 'localqueue', '/bin/hostname']
	'121195'
	>>> test_submit('JMSSubmit', 'job_submit', 'test.JMS.submit', req_list_2)
	None
	['-J', 'GC00000000.0', '-p', 1, '-o', '/dev/stdout', '-e', '/dev/stderr', '-T', 14, '-t', 8, '-m', 1234, '/bin/hostname']
	'121195'
	>>> test_submit('JMSSubmit', 'job_submit', 'test.JMS.submit', req_list_3)
	None
	['-J', 'GC00000000.0', '-p', 1, '-o', '/dev/stdout', '-e', '/dev/stderr', '-c', 'localqueue', '/bin/hostname']
	'121195'
	>>> test_submit('JMSSubmit', 'job_submit', 'test.JMS.submit', req_list_4)
	None
	['-J', 'GC00000000.0', '-p', 1, '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'121195'
	"""

class Test_LSF:
	"""
	>>> test_submit('LSFSubmit', 'bsub', 'test.LSF.submit')
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'34020017'
	>>> test_submit('LSFSubmit', 'bsub', 'test.LSF.submit', req_list_1)
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-q', 'localqueue,localqueue1', '/bin/hostname']
	'34020017'
	>>> test_submit('LSFSubmit', 'bsub', 'test.LSF.submit', req_list_2)
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-W', 14, '-c', 8, '/bin/hostname']
	'34020017'
	>>> test_submit('LSFSubmit', 'bsub', 'test.LSF.submit', req_list_3)
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-q', 'localqueue,localqueue1', '/bin/hostname']
	'34020017'
	>>> test_submit('LSFSubmit', 'bsub', 'test.LSF.submit', req_list_4)
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'34020017'
	"""

class Test_PBS:
	"""
	>>> test_submit('PBSSubmit', 'qsub', 'test.PBS.submit')
	None
	['-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'1667161'
	>>> test_submit('PBSSubmit', 'qsub', 'test.PBS.submit', shell='/bin/ash', account='myaccount')
	None
	['-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-P', 'myaccount', '-S', '/bin/ash', '/bin/hostname']
	'1667161'
	>>> test_submit('PBSSubmit', 'qsub', 'test.PBS.submit', req_list_1, software_requirement_map=software_req_map)
	None
	['-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-l', 'TEST=MYREQ', '-q', 'localqueue', '-l', 'host=site1+site2', '/bin/hostname']
	'1667161'
	>>> test_submit('PBSSubmit', 'qsub', 'test.PBS.submit', req_list_2, software_requirement_map=software_req_map)
	None
	['-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-l', 'TEST=DEFAULT', '-l', 'pvmem=1234mb', '/bin/hostname']
	'1667161'
	>>> test_submit('PBSSubmit', 'qsub', 'test.PBS.submit', req_list_2)
	None
	['-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-l', 'pvmem=1234mb', '/bin/hostname']
	'1667161'
	>>> test_submit('PBSSubmit', 'qsub', 'test.PBS.submit', req_list_3)
	None
	['-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-q', 'localqueue', '/bin/hostname']
	'1667161'
	>>> test_submit('PBSSubmit', 'qsub', 'test.PBS.submit', req_list_4)
	None
	['-N', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-l', 'host=site1+site2', '-t', 2, '/bin/hostname']
	'1667161'
	"""

class Test_SLURM:
	"""
	>>> test_submit('SLURMSubmit', 'sbatch', 'test.SLURM.submit')
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'121195'
	>>> test_submit('SLURMSubmit', 'sbatch', 'test.SLURM.submit', req_list_1)
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '-p', 'localqueue', '/bin/hostname']
	'121195'
	>>> test_submit('SLURMSubmit', 'sbatch', 'test.SLURM.submit', req_list_2)
	None
	['-J', 'GC00000000.0', '-o', '/dev/stdout', '-e', '/dev/stderr', '/bin/hostname']
	'121195'
	"""

run_test()
