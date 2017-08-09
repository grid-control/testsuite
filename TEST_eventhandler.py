#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), ''))
__import__('testfwk').setup(__file__)
# - prolog marker
import logging
from testfwk import TestsuiteStream, create_config, run_test, str_dict_testsuite, testfwk_create_workflow
from grid_control.event_base import LocalEventHandler, MultiLocalEventHandler, MultiRemoteEventHandler, RemoteEventHandler
from grid_control.event_basic import CompatEventHandlerManager
from grid_control.job_db import Job


class TestLocalEventHandler(LocalEventHandler):
	def _display(self, args):
		print(repr(args))

	def on_job_state_change(self, task, job_db_len, jobnum, job_obj, old_state, new_state, reason=None):
		self._display(['on_job_state_change', job_db_len, jobnum,
			Job.enum2str(old_state), Job.enum2str(new_state), reason])

	def on_job_submit(self, task, wms, job_obj, jobnum):
		self._display(['on_job_submit', jobnum, Job.enum2str(job_obj.state)])

	def on_job_update(self, task, wms, job_obj, jobnum, data):
		self._display(['on_job_update', jobnum, Job.enum2str(job_obj.state), data])

	def on_job_output(self, task, wms, job_obj, jobnum, exit_code):
		self._display(['on_job_output', jobnum, Job.enum2str(job_obj.state), exit_code])

	def on_task_finish(self, task, job_len):
		self._display(['on_task_finish', job_len])

	def on_workflow_finish(self):
		self._display(['on_workflow_finish'])


class TestRemoteEventHandler(RemoteEventHandler):
	def get_script(self):
		return ['mon.test1.sh', 'mon.test2.sh']

	def get_mon_env_dict(self):
		return {'key': 'value'}

	def get_file_list(self):
		return ['mon.support.dat']


class Test_LocalEventHandler:
	"""
	>>> config = create_config(config_dict={'global': {'event log show wms': True}})
	>>> workflow = testfwk_create_workflow({'jobs': {'jobs': 1}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> m1 = TestLocalEventHandler(config, 'm1')
	>>> m2 = LocalEventHandler(config, 'm2')
	>>> m = MultiLocalEventHandler(config, 'mon', [m1, m2])
	>>> m.on_job_state_change(workflow.task, 123, 12, Job(), Job.DONE, Job.SUCCESS, 'status update')
	['on_job_state_change', 123, 12, 'DONE', 'SUCCESS', 'status update']
	>>> m.on_job_submit(workflow.task, None, Job(), 123)
	['on_job_submit', 123, 'INIT']
	>>> m.on_job_update(workflow.task, None, Job(), 123, {'key': 'value'})
	['on_job_update', 123, 'INIT', {'key': 'value'}]
	>>> m.on_job_output(workflow.task, None, Job(), 123, 321)
	['on_job_output', 123, 'INIT', 321]
	>>> m.on_task_finish(workflow.task, 42)
	['on_task_finish', 42]
	>>> m.on_workflow_finish()
	['on_workflow_finish']

	>>> bleh = LocalEventHandler.create_instance('BasicLogEventHandler', config, 'bleh')
	>>> job = Job()
	>>> job.assign_id('WMS.HOST.1234')
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.DONE, Job.SUCCESS, 'reason')
	0000-00-00 00:00:00 - Job 12  state changed from DONE to SUCCESS (reason) (WMS:HOST)
	>>> job.set('runtime', 123)
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.DONE, Job.SUCCESS, 'reason')
	0000-00-00 00:00:00 - Job 12  state changed from DONE to SUCCESS (reason) (WMS:HOST) (runtime 0h 02min 03sec)
	>>> job.attempt = 1
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.SUBMITTED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to SUBMITTED (WMS:HOST)
	>>> job.attempt = 2
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.SUBMITTED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to SUBMITTED (WMS:HOST) (retry #1)
	>>> job.attempt = 43
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.SUBMITTED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to SUBMITTED (WMS:HOST) (retry #42)
	>>> job.set('QUEUE', 'somequeue')
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.QUEUED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to QUEUED (WMS:HOST) (somequeue)
	>>> job.set('SITE', 'somesite')
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.QUEUED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to QUEUED (WMS:HOST) (somesite/somequeue)
	>>> job.set('reason', 'walltime')
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.ABORTED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to ABORTED (WMS:HOST) (walltime)
	>>> job.set('retcode', 101)
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.FAILED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to FAILED (WMS:HOST) (error code: 101 - somesite/somequeue - runtime 0h 02min 03sec)
	>>> logging.getLogger('jobs').setLevel(logging.DEBUG)
	>>> bleh.on_job_state_change(workflow.task, 123, 12, job, Job.INIT, Job.FAILED)
	0000-00-00 00:00:00 - Job 12  state changed from INIT to FAILED (WMS:HOST) (error code: 101 - file not found - somesite/somequeue - runtime 0h 02min 03sec)
	>>> logging.getLogger('jobs').setLevel(logging.INFO)
	"""


class Test_RemoteEventHandler:
	"""
	>>> config = create_config()
	>>> m1 = TestRemoteEventHandler(config, 'm1')
	>>> m2 = RemoteEventHandler(config, 'm2')
	>>> m = MultiRemoteEventHandler(config, 'mon', [m1, m2])
	>>> m.get_script()
	['mon.test1.sh', 'mon.test2.sh']
	>>> print(str_dict_testsuite(m.get_mon_env_dict()))
	{'GC_MONITORING': 'mon.test1.sh mon.test2.sh', 'key': 'value'}
	>>> m.get_file_list()
	['mon.support.dat', 'mon.test1.sh', 'mon.test2.sh']
	"""


class Test_CompatEventHandler:
	"""
	>>> config = create_config()
	>>> tmp = CompatEventHandlerManager(config)
	>>> config.write(TestsuiteStream(), print_default=False)
	[jobs!]
	local event handler += scripts
	-----

	>>> config = create_config(config_dict={'global': {'monitor': 'dashboard scripts'}})
	>>> tmp = CompatEventHandlerManager(config)
	>>> config.write(TestsuiteStream(), print_default=False)
	[backend!]
	remote event handler += dashboard
	-----
	[global]
	monitor =
	  dashboard
	  scripts
	-----
	[jobs!]
	local event handler += dashboard
	local event handler += scripts
	-----
	"""

run_test()
