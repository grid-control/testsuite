#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), ''))
__import__('testfwk').setup(__file__)
# - prolog marker
import logging
from testfwk import create_config, run_test, testfwk_remove_files, try_catch
from hpfwk import Plugin


config_dict = {'jobs': {'wall time': '1'}, 'global': {'executable': 'TEST_task.py', 'task date': '2099-01-01'}}
config = create_config(config_dict=config_dict)

class Test_JobName:
	"""
	>>> task = Plugin.create_instance('UserTask', config, 'mytask')
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	>>> try_catch(lambda: Plugin.create_instance('JobNamePlugin', config).get_name(task, 'GC00', 12), 'AbstractError', 'is an abstract function')
	caught
	>>> logging.getLogger().warning(Plugin.create_instance('DefaultJobName', config).get_name(task, 'GC00', 12))
	GC00.12
	>>> Plugin.create_instance('ConfigurableJobName', create_config(config_dict={'global': {'job name': '@GC_TASK_DATE@ job_@GC_JOB_ID@'}})).get_name(task, 'GC00', 12)
	'2099-01-01 job_12'
	>>> try_catch(lambda: Plugin.create_instance('ConfigurableJobName', create_config(config_dict={'global': {'job name': '@GC_UNKNOWN@'}})).get_name(task, 'GC00', 12), 'ConfigError', 'references unknown variables')
	caught
	"""

class Test_Task:
	"""
	>>> task1 = Plugin.create_instance('TaskModule', config, 'mytask')
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	>>> try_catch(task1.get_command, 'AbstractError', 'is an abstract function')
	caught
	"""

run_test(cleanup_fun=lambda: testfwk_remove_files(['work/params.dat.gz', 'work/params.map.gz', 'work']))
