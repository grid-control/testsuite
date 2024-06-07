#!/bin/sh

cd "$(dirname $0)/.."
export GC_WRAPPER="$1"
export GC_RESULT=0

travis_run() {
	echo "Running $@"
	$GC_WRAPPER "$@"
	EXITCODE="$?"
	if [ "$EXITCODE" = "0" ]; then
		echo "$@ - ok";
	else
		echo "$@ - test failed with $EXITCODE";
		GC_RESULT=1
	fi
}

echo '##[group]testsuite_backend'
travis_run ./testsuite/backend/TEST_backend.py
travis_run ./testsuite/backend/TEST_basic.py
travis_run ./testsuite/backend/TEST_cancel.py
travis_run ./testsuite/backend/TEST_discover.py
travis_run ./testsuite/backend/TEST_jdl.py
travis_run ./testsuite/backend/TEST_proxy.py
travis_run ./testsuite/backend/TEST_status.py
echo '##[endgroup]'

echo '##[group]testsuite_cms'
travis_run ./testsuite/cms/TEST_cms_cert.py
travis_run ./testsuite/cms/TEST_cmssw.py
travis_run ./testsuite/cms/TEST_cmssw_scanner.py
travis_run ./testsuite/cms/TEST_lumifilter.py
travis_run ./testsuite/cms/TEST_lumiproc.py
travis_run ./testsuite/cms/TEST_lumitools.py
# travis_run ./testsuite/cms/TEST_provider_cms.py
# travis_run ./testsuite/cms/TEST_provider_das.py
# travis_run ./testsuite/cms/TEST_sitedb.py
echo '##[endgroup]'

echo '##[group]testsuite_config'
travis_run ./testsuite/config/TEST_configAPI1.py
travis_run ./testsuite/config/TEST_configAPI2.py
travis_run ./testsuite/config/TEST_configAPI3.py
travis_run ./testsuite/config/TEST_configAPI4.py
travis_run ./testsuite/config/TEST_configContainer.py
travis_run ./testsuite/config/TEST_configHandlers.py
travis_run ./testsuite/config/TEST_configModify.py
travis_run ./testsuite/config/TEST_configParser.py
travis_run ./testsuite/config/TEST_config.py
travis_run ./testsuite/config/TEST_configTyped.py
travis_run ./testsuite/config/TEST_configView.py
travis_run ./testsuite/config/TEST_interactive.py
travis_run ./testsuite/config/TEST_matcher.py
echo '##[endgroup]'

echo '##[group]testsuite_datasets'
travis_run ./testsuite/datasets/TEST_dataresync1.py
travis_run ./testsuite/datasets/TEST_dataresync2.py
travis_run ./testsuite/datasets/TEST_dataresync3.py
travis_run ./testsuite/datasets/TEST_dataresync4.py
travis_run ./testsuite/datasets/TEST_dataresync5.py
travis_run ./testsuite/datasets/TEST_dataresync_meta.py
travis_run ./testsuite/datasets/TEST_dataresync_reorder.py
travis_run ./testsuite/datasets/TEST_processor.py
travis_run ./testsuite/datasets/TEST_provider.py
travis_run ./testsuite/datasets/TEST_scanner.py
travis_run ./testsuite/datasets/TEST_splitterio.py
travis_run ./testsuite/datasets/TEST_splitter.py
echo '##[endgroup]'

echo '##[group]testsuite_parameters'
travis_run ./testsuite/parameters/TEST_config_param.py
travis_run ./testsuite/parameters/TEST_padapter1.py
travis_run ./testsuite/parameters/TEST_padapter.py
travis_run ./testsuite/parameters/TEST_pfactory.py
travis_run ./testsuite/parameters/TEST_pproc.py
travis_run ./testsuite/parameters/TEST_psource.py
echo '##[endgroup]'

echo '##[group]testsuite_basic'
travis_run ./testsuite/TEST_activity.py
travis_run ./testsuite/TEST_debug.py
travis_run ./testsuite/TEST_eventhandler.py
travis_run ./testsuite/TEST_exception.py
travis_run ./testsuite/TEST_go.py
travis_run ./testsuite/TEST_gui.py
travis_run ./testsuite/TEST_jobdb.py
travis_run ./testsuite/TEST_jobselector.py
travis_run ./testsuite/TEST_logging.py
travis_run ./testsuite/TEST_output_processor.py
travis_run ./testsuite/TEST_plugins.py
travis_run ./testsuite/TEST_process.py
travis_run ./testsuite/TEST_report.py
travis_run ./testsuite/TEST_task.py
travis_run ./testsuite/TEST_taskresync.py
travis_run ./testsuite/TEST_utils.py
travis_run ./testsuite/TEST_webservice.py
echo '##[endgroup]'

echo '##[group]testsuite_ansi'
export GC_TERM=dumb; travis_run ./testsuite/TEST_ansi.py
export GC_TERM=gc_color16; travis_run ./testsuite/TEST_ansi.py
export GC_TERM=gc_color256; travis_run ./testsuite/TEST_ansi.py
echo '##[endgroup]'

exit $GC_RESULT
