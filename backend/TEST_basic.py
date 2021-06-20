#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
import os, shutil, logging
from testfwk import create_config, run_test, testfwk_remove_files, try_catch
from grid_control.backends.backend_tools import BackendDiscovery, BackendExecutor, ProcessCreator, ProcessCreatorViaArguments, ProcessCreatorViaStdin, unpack_wildcard_tar
from grid_control.utils.process_base import LocalProcess
from python_compat import sorted


class DummyExecutor(BackendExecutor):
	def __init__(self):
		BackendExecutor.__init__(self, create_config())

	def test(self, proc):
		proc.status(timeout=10)
		self._filter_proc_log(logging.getLogger(), proc, msg='logging', blacklist=['abc'], discard_list=['xyz'])
		return proc

class Test_Base:
	"""
	>>> dummy = shutil.copyfile('../work.jobdb/output.job_1/GC_WC_base.tar.gz', '../work.jobdb/output.job_1/GC_WC.tar.gz')
	>>> sorted(os.listdir('../work.jobdb/output.job_1/'))
	['GC_WC.tar.gz', 'GC_WC_base.tar.gz', 'gc.fail.gz', 'gc.stdout', 'gc.test.gz', 'job.info']
	>>> unpack_wildcard_tar(logging.getLogger(), '../work.jobdb/output.job_1/')
	>>> sorted(os.listdir('../work.jobdb/output.job_1/'))
	['GC_WC_base.tar.gz', 'gc.fail.gz', 'gc.stdout', 'gc.test.gz', 'job.info', 'output.job_2']
	>>> testfwk_remove_files(['../work.jobdb/output.job_1/output.job_2/*', '../work.jobdb/output.job_1/output.job_2'])

	>>> unpack_wildcard_tar(logging.getLogger(), '../work.jobdb/output.job_4/')
	0000-00-00 00:00:00 - root:ERROR - Can't unpack output files contained in ../work.jobdb/output.job_4/GC_WC.tar.gz

	>>> try_catch(BackendDiscovery(create_config()).discover, 'AbstractError')
	caught
	>>> try_catch(lambda: ProcessCreator(create_config()).create_proc([]), 'AbstractError')
	caught
	>>> try_catch(lambda: ProcessCreatorViaArguments(create_config()).create_proc([]), 'AbstractError')
	caught
	>>> try_catch(lambda: ProcessCreatorViaStdin(create_config()).create_proc([]), 'AbstractError')
	caught

	>>> de = DummyExecutor()
	>>> de.test(LocalProcess('../bin/my_echo', 123, 'xyz'))
	LocalProcess(cmd = ../bin/my_echo, args = ['123', 'xyz'], status = 123, stdin log = '', stdout log = '', stderr log = 'xyz\\n')
	>>> de.test(LocalProcess('../bin/my_echo', 123, 'abc'))
	LocalProcess(cmd = ../bin/my_echo, args = ['123', 'abc'], status = 123, stdin log = '', stdout log = '', stderr log = 'abc\\n')
	>>> de.test(LocalProcess('../bin/my_echo', 123, 'abc', 'def'))
	logging
	LocalProcess(cmd = ../bin/my_echo, args = ['123', 'abc', 'def'], status = 123, stdin log = '', stdout log = '', stderr log = 'abc\\ndef\\n')
	>>> de.test(LocalProcess('../bin/my_echo', 123, 'abc', 'def', 'xyz'))
	LocalProcess(cmd = ../bin/my_echo, args = ['123', 'abc', 'def', 'xyz'], status = 123, stdin log = '', stdout log = '', stderr log = 'abc\\ndef\\nxyz\\n')
	"""

run_test()
