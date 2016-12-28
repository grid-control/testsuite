#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
import os, shutil, logging
from testfwk import create_config, run_test, testfwk_remove_files, try_catch
from grid_control.backends.backend_tools import BackendDiscovery, BackendExecutor, ProcessCreator, ProcessCreatorViaArguments, ProcessCreatorViaStdin, unpack_wildcard_tar
from grid_control.utils.process_base import LocalProcess
from python_compat import sorted


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

	"""

run_test()
