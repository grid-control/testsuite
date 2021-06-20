#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
from testfwk import create_config, run_test, testfwk_remove_files, testfwk_set_path, try_catch
from grid_control.backends import WMS
from grid_control.backends.storage import StorageManager
from grid_control.job_db import Job


def create_wms(name):
	wms = WMS.create_instance('Host', create_config(), name)
	return (wms, wms.get_access_token(None))

def display_jobs(wms, gc_id_list):
	for (gc_id, job_state, job_info) in wms.check_jobs(gc_id_list):
		print('%s %s' % (gc_id, Job.enum2str(job_state)))

class Test_Storage:
	"""
	>>> sm = StorageManager(create_config(), 'test', 'se', 'se output')
	>>> sm.do_transfer([])
	>>> sm.get_dependency_list()
	[]
	>>> sm.get_process([])
	(';', [])
	>>> sm_sb = StorageManager.create_instance('LocalSBStorageManager', create_config(), 'test', 'sb', 'sb output')
	>>> try_catch(lambda: sm_sb.do_transfer([('desc', '/tmp/GC_TEST_FILE', 'GC_TEST_FILE')]), 'StorageError', 'Unable to transfer desc')
	caught

	>>> sm_se1 = StorageManager.create_instance('SEStorageManager', create_config(), 'test', 'se', 'se output')
	>>> sm_se1.get_dependency_list()
	[]
	>>> try_catch(lambda: sm_se1.do_transfer([('dest', 'dummy', 'dummy')]), 'ConfigError', 'transferred because se output')
	caught

	>>> se_config = create_config(config_dict={'storage': {'se path': 'srm://host/dir'}})
	>>> se_config.get('access token', '')
	''
	>>> sm_se2 = StorageManager.create_instance('SEStorageManager', se_config, 'test', 'se', 'se output')
	>>> se_config.get('access token', '')
	'\\nVomsProxy'
	>>> sm_se2.get_dependency_list()
	['glite']
	"""

class Test_WMS:
	"""
	>>> wms = WMS.create_instance('WMS', create_config(), 'wms')
	>>> try_catch(lambda: wms.can_submit(60, True), 'AbstractError', 'is an abstract function')
	caught
	>>> try_catch(lambda: wms.get_access_token(None), 'AbstractError', 'is an abstract function')
	caught
	>>> try_catch(lambda: wms.deploy_task(task=None, transfer_se=None, transfer_sb=None), 'AbstractError', 'is an abstract function')
	caught
	>>> try_catch(lambda: wms.submit_jobs([100, 200], task=None), 'AbstractError', 'is an abstract function')
	caught
	>>> try_catch(lambda: wms.check_jobs(['WMSID.HOST.100', 'WMSID.HOST.200']), 'AbstractError', 'is an abstract function')
	caught
	>>> try_catch(lambda: wms.cancel_jobs(['WMSID.HOST.100', 'WMSID.HOST.200']), 'AbstractError', 'is an abstract function')
	caught
	>>> try_catch(lambda: wms.retrieve_jobs(['WMSID.HOST.100', 'WMSID.HOST.200']), 'AbstractError', 'is an abstract function')
	caught
	"""

class Test_MultiWMS:
	"""
	>>> testfwk_remove_files(['work/*', 'work'])
	>>> (h1, at1) = create_wms('HOST1')
	Using batch system: ---
	>>> (h2, at2) = create_wms('HOST2')
	Using batch system: ---
	>>> (h3, at3) = create_wms('HOST3')
	Using batch system: ---

	>>> hm = WMS.create_instance('MultiWMS', create_config(), 'multiwms', [h1, h2, h3])
	>>> (at1 == at2, at1 == at3)
	(False, False)
	>>> hm.get_access_token('WMSID.HOST1.123') == at1
	True
	>>> hm.get_access_token('WMSID.HOST2.123') == at2
	True
	>>> hm.get_access_token('WMSID.HOST3.123') == at3
	True
	>>> hm.get_access_token('WMSID.HOSTx.123') == at1
	True
	>>> display_jobs(h1, ['WMSID.HOST1.100000', 'WMSID.HOST1.200000'])
	WMSID.HOST1.100000 DONE
	WMSID.HOST1.200000 DONE

	>>> display_jobs(hm, ['WMSID.HOST1.100000', 'WMSID.HOST1.200000', 'WMSID.HOST2.300000', 'WMSID.HOST3.400000', 'WMSID.HOST2.500000', 'WMSID.HOST3.600000'])
	WMSID.HOST1.100000 DONE
	WMSID.HOST1.200000 DONE
	WMSID.HOST2.300000 DONE
	WMSID.HOST2.500000 DONE
	WMSID.HOST3.400000 DONE
	WMSID.HOST3.600000 DONE

	>>> testfwk_remove_files(['work/*', 'work'])
	"""

class Test_Local:
	"""
	>>> try_catch(lambda: WMS.create_instance('Local', create_config(), 'wms'), 'BackendError', 'No valid local backend found')
	caught
	>>> testfwk_set_path('../bin')
	>>> wms = WMS.create_instance('Local', create_config(config_dict={'global': {'wms': 'host'}}), 'wms')
	Using batch system: ---
	"""


run_test()
