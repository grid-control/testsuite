#!/usr/bin/env python

import os, sys


class MKDIR(object):
	def __init__(self, lfn_prefix, can_parent, on_noargs):
		from optparse import OptionParser
		parser = OptionParser()
		self._lfn_prefix = lfn_prefix
		self._on_noargs = on_noargs
		if can_parent:
			parser.add_option('-p', dest='parents', action='store_true', default=False)
		(opts, args) = parser.parse_args()
		self._can_parent = can_parent
		self._base_dn = '/home/fred/grid-control.git/testsuite/se-tools/dummy'
		sys.exit(self._handle_base(opts, args))

	def _handle(self, opts, local_path, lfn):
		pass

	def _handle_base(self, opts, args, parents=False):
		if not self._can_parent:
			opts.parents = False
		if self._on_noargs and not args:
			sys.stderr.write(self._on_noargs[1])
			return self._on_noargs[0]
		local_path = args[0].replace(self._lfn_prefix, self._base_dn)
		return self._handle(opts, local_path, args[0])

	def _mkdir(self, opts, local_path):
		mkdir_fun = os.mkdir
		if opts.parents:
			mkdir_fun = os.makedirs
		mkdir_fun(local_path)
