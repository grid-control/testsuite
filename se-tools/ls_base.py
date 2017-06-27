#!/usr/bin/env python

import os, sys


class LS(object):
	def __init__(self, lfn_prefix, fmt_dir, fmt_file):
		from optparse import OptionParser
		parser = OptionParser()
		self._setup_opts(parser)
		(opts, args) = parser.parse_args()
		self._base_dn = '/home/fred/grid-control.git/testsuite/se-tools/dummy'
		self._lfn_prefix = lfn_prefix
		self._turl_prefix = ''
		self._name_key = None
		self._fmt = '%(name)s\n'
		self._fmt_dir = fmt_dir
		self._fmt_file = fmt_file
		sys.exit(self._handle(opts, args))

	def _display_dir_content(self, opts, local_path):
		for fn in os.listdir(local_path):
			self._out(os.path.join(local_path, fn))

	def _err(self, fmt, local_fn):
		sys.stderr.write(self._fmt_entry(local_fn, fmt))

	def _fmt_entry(self, local_fn, fmt=None):
		tmp = {
			'lfn_prefix': self._lfn_prefix,
			'basename': os.path.basename(local_fn),
			'lfn': local_fn.replace(self._base_dn, self._lfn_prefix),
			'turl': local_fn.replace(self._base_dn, self._turl_prefix + self._lfn_prefix),
		}
		tmp['name'] = tmp.get(self._name_key)
		if os.path.isfile(local_fn):
			tmp['size'] = os.path.getsize(local_fn)
			tmp.update(self._fmt_file)
		else:
			tmp['size'] = 0
			tmp.update(self._fmt_dir)
		return (fmt or self._fmt) % tmp

	def _handle(self, opts, args):
		pass

	def _out(self, local_fn):
		sys.stdout.write(self._fmt_entry(local_fn))

	def _setup_opts(self, parser):
		parser.add_option('-l', dest='is_long', action='store_true', default=False)
		parser.add_option('-d', dest='dont_enter_dir', action='store_true', default=False)
