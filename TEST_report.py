#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), ''))
__import__('testfwk').setup(__file__)
# - prolog marker
import time
from testfwk import cleanup_workflow, create_config, run_test, testfwk_create_workflow, testfwk_remove_files, try_catch
from grid_control.report import Report
from grid_control_gui.ansi import ANSI
from grid_control_gui.report_colorbar import JobProgressBar
from python_compat import BytesBuffer


class TestImageReport(Report.get_class('ImageReport')):
	def show_report(self, job_db, jobnum_list):
		buffer = BytesBuffer()
		self._show_image('test.png', buffer)
		buffer.close()


def test_report(name, *args, **kwargs):
	job_db = args[0]
	config = kwargs.get('config') or create_config()
	report = Report.create_instance(name, config, 'test', *args)
	report.show_report(job_db, job_db.get_job_list())
	return report


class Test_Report(object):
	"""
	>>> workflow = testfwk_create_workflow({'jobs': {'jobs': 1}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> try_catch(lambda: Report.create_instance('Report', create_config(), 'test', workflow.job_manager.job_db).show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list()), 'AbstractError', 'is an abstract function')
	caught

	>>> tmp = test_report('BasicHeaderReport', workflow.job_manager.job_db)
	-----------------------------------------------------------------
	REPORT SUMMARY:
	---------------

	>>> tmp = test_report('BasicHeaderReport', workflow.job_manager.job_db, workflow.task)
	-----------------------------------------------------------------
	REPORT SUMMARY:                          unnamed / GC0000000000
	---------------

	>>> workflow = testfwk_create_workflow({'jobs': {'jobs': 1}, 'global': {'config id': 'very long and descriptive config name'}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> tmp = test_report('BasicHeaderReport', workflow.job_manager.job_db, workflow.task)
	-----------------------------------------------------------------
	REPORT SUMMARY:             very long and descriptive config name
	---------------

	>>> workflow = testfwk_create_workflow({'jobs': {'jobs': 1}, 'global': {'config id': 'incredibly and way too long and descriptive config name'}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> tmp = test_report('BasicHeaderReport', workflow.job_manager.job_db, workflow.task)
	-----------------------------------------------------------------
	REPORT SUMMARY:                                    GC0000000000
	---------------

	>>> TestImageReport(create_config(), 'image', workflow.job_manager.job_db).show_report(workflow.job_manager.job_db, [])
	>>> testfwk_remove_files(['test.png'])

	>>> tmp = test_report('ColorBarReport', workflow.job_manager.job_db, workflow.task)
	[                                                               ]
	>>> tmp = test_report('ColorBarReport', workflow.job_manager.job_db, workflow.task, config=create_config(config_dict={'global': {'report bar show numbers': 'True'}}))
	[                                       ] (    0|   0|   0|   0 )
	>>> jpb1 = JobProgressBar()
	>>> jpb2 = JobProgressBar(jobs_on_finish=True)
	>>> jpb3 = JobProgressBar(display_text=False, jobs_on_finish=True)
	>>> jpb2.update(100)
	>>> ANSI.strip_fmt(str(jpb3))
	'[                        ]'
	>>> ANSI.strip_fmt(str(jpb1))
	'[] (    0|   0|   0|   0 )'
	>>> jpb1.update(100)
	>>> ANSI.strip_fmt(str(jpb1))
	'[] (       finished      )'
	>>> ANSI.strip_fmt(str(jpb2))
	'[] (  100 |   finished   )'

	>>> tmp = Report.create_instance('LeanReport', create_config(), 'test', workflow.job_manager.job_db, workflow.task)
	>>> tmp._start_time = time.time() - 60 * 60
	>>> tmp.show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list())
	            1        0         0        0 / SUCCESS      0   0.0%
	  1h00   INIT > QUEUED > RUNNING >   DONE | [>        0%        ]
	       100.0%   100.0%    100.0%   100.0% \ FAILING      0   0.0%
	>>> tmp._start_time = time.time() - 24 * 60 * 60
	>>> tmp.show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list())
	            1        0         0        0 / SUCCESS      0   0.0%
	  1d00   INIT > QUEUED > RUNNING >   DONE | [>        0%        ]
	       100.0%   100.0%    100.0%   100.0% \ FAILING      0   0.0%

	>>> workflow = testfwk_create_workflow({'parameters': {'parameters': 'A B', 'A': '1 2', 'B': 'W X Y Z'}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> tmp = Report.create_instance('ModernReport', create_config(config_dict={'global': {'report categories max': 4}}), 'test', workflow.job_manager.job_db, workflow.task)
	>>> tmp.show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list())
	B = W (2 subtasks)
	[                                                               ]
	B = X (2 subtasks)
	[                                                               ]
	B = Y (2 subtasks)
	[                                                               ]
	B = Z (2 subtasks)
	[                                                               ]

	>>> workflow = testfwk_create_workflow({'parameters': {'parameters': 'A B', 'A': '1 2', 'B': 'X Y Z'}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> tmp = Report.create_instance('ModernReport', create_config(config_dict={'global': {'report categories max': 4}}), 'test', workflow.job_manager.job_db, workflow.task)
	>>> tmp.show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list())
	A = 1, B = X
	[                                                               ]
	A = 1, B = Y
	[                                                               ]
	A = 1, B = Z
	[                                                               ]
	Remaining subtasks (3 subtasks)
	[                                                               ]

	>>> workflow = testfwk_create_workflow({'parameters': {'parameters': 'A B', 'A': '1 2', 'B': 'X Y Z'}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> tmp = Report.create_instance('ModernReport', create_config(config_dict={'global': {'report categories max': 2}}), 'test', workflow.job_manager.job_db, workflow.task)
	>>> tmp.show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list())
	A = 1 (3 subtasks)
	[                                                               ]
	A = 2 (3 subtasks)
	[                                                               ]

	>>> workflow = testfwk_create_workflow({'parameters': {'parameters': 'A B', 'A': '1 2', 'B': 'X Y Z'}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> tmp = Report.create_instance('ModernReport', create_config(config_dict={'global': {'report categories max': 3}}), 'test', workflow.job_manager.job_db, workflow.task)
	>>> tmp.show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list())
	B = X (2 subtasks)
	[                                                               ]
	B = Y (2 subtasks)
	[                                                               ]
	B = Z (2 subtasks)
	[                                                               ]

	>>> workflow = testfwk_create_workflow({'parameters': {'parameters': 'A (B, C)', 'A': '1 2', 'B': 'X Y Z', 'C': '1 2 3'}})
	Current task ID: GC0000000000
	Task started on: 0000-00-00
	Using batch system: ---
	>>> tmp = Report.create_instance('ModernReport', create_config(config_dict={'global': {'report categories max': 3}}), 'test', workflow.job_manager.job_db, workflow.task)
	>>> tmp.show_report(workflow.job_manager.job_db, workflow.job_manager.job_db.get_job_list())
	B = X (2 subtasks)
	[                                                               ]
	B = Y (2 subtasks)
	[                                                               ]
	B = Z (2 subtasks)
	[                                                               ]
	"""

run_test(cleanup_fun=cleanup_workflow)
