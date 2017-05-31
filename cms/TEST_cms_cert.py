#!/usr/bin/env python
__import__('sys').path.append(__import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
__import__('testfwk').setup(__file__)
# - prolog marker
import os, getpass
from testfwk import create_config, function_factory, run_test, testfwk_remove_files, testfwk_set_path, try_catch
from grid_control.backends import AccessToken
from grid_control_cms.access_cms import get_cms_cert


class Test_CMSCert(object):
	"""
	>>> testfwk_remove_files(['testfwk_timeleft'])
	>>> os.environ['PATH'] = '/bin'
	>>> os.environ['X509_USER_PROXY'] = ''

	>>> get_cms_cert(ignore_errors=True)
	>>> try_catch(get_cms_cert, 'CMSAuthenticationException', 'Unable to find grid environment')
	caught

	>>> testfwk_set_path('../bin')
	>>> config = create_config(config_dict={'access': {'ignore warnings': True}})
	>>> token = AccessToken.create_instance('VomsAccessToken', config, 'cms-proxy')
	>>> token.can_submit(5*60, True)
	True
	>>> get_cms_cert(config, ignore_errors=False)
	'/usr/users/stober/.globus/proxy.grid'

	>>> testfwk_set_path('../cms')
	>>> getpass.getpass = function_factory('cat123', '01:00:00')

	>>> try_catch(lambda: get_cms_cert(config, ignore_errors=False), 'CMSAuthenticationException', 'Newly created grid proxy is also invalid')
	The grid proxy has expired or is invalid!
	(('Please enter proxy password: ',), {})
	caught

	>>> get_cms_cert(config, ignore_errors=False)
	The grid proxy has expired or is invalid!
	(('Please enter proxy password: ',), {})
	'/usr/users/stober/.globus/proxy.grid'

	>>> testfwk_remove_files(['testfwk_timeleft'])
	"""

run_test()
