#!/bin/sh

cd "$(dirname $0)/.."
export GC_WRAPPER="$1"
export GC_RESULT=0

run_test() {
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
run_test ./testsuite/backend/TEST_backend.py
run_test ./testsuite/backend/TEST_basic.py
run_test ./testsuite/backend/TEST_cancel.py
run_test ./testsuite/backend/TEST_discover.py
run_test ./testsuite/backend/TEST_jdl.py
run_test ./testsuite/backend/TEST_proxy.py
run_test ./testsuite/backend/TEST_status.py
echo '##[endgroup]'

echo '##[group]testsuite_cms'
run_test ./testsuite/cms/TEST_cms_cert.py
run_test ./testsuite/cms/TEST_cmssw.py
run_test ./testsuite/cms/TEST_cmssw_scanner.py
run_test ./testsuite/cms/TEST_lumifilter.py
run_test ./testsuite/cms/TEST_lumiproc.py
run_test ./testsuite/cms/TEST_lumitools.py
# run_test ./testsuite/cms/TEST_provider_cms.py
# run_test ./testsuite/cms/TEST_provider_das.py
# run_test ./testsuite/cms/TEST_sitedb.py
echo '##[endgroup]'

echo '##[group]testsuite_config'
run_test ./testsuite/config/TEST_configAPI1.py
run_test ./testsuite/config/TEST_configAPI2.py
run_test ./testsuite/config/TEST_configAPI3.py
run_test ./testsuite/config/TEST_configAPI4.py
run_test ./testsuite/config/TEST_configContainer.py
run_test ./testsuite/config/TEST_configHandlers.py
run_test ./testsuite/config/TEST_configModify.py
run_test ./testsuite/config/TEST_configParser.py
run_test ./testsuite/config/TEST_config.py
run_test ./testsuite/config/TEST_configTyped.py
run_test ./testsuite/config/TEST_configView.py
run_test ./testsuite/config/TEST_interactive.py
run_test ./testsuite/config/TEST_matcher.py
echo '##[endgroup]'

echo '##[group]testsuite_datasets'
run_test ./testsuite/datasets/TEST_dataresync1.py
run_test ./testsuite/datasets/TEST_dataresync2.py
run_test ./testsuite/datasets/TEST_dataresync3.py
run_test ./testsuite/datasets/TEST_dataresync4.py
run_test ./testsuite/datasets/TEST_dataresync5.py
run_test ./testsuite/datasets/TEST_dataresync_meta.py
run_test ./testsuite/datasets/TEST_dataresync_reorder.py
run_test ./testsuite/datasets/TEST_processor.py
run_test ./testsuite/datasets/TEST_provider.py
run_test ./testsuite/datasets/TEST_scanner.py
run_test ./testsuite/datasets/TEST_splitterio.py
run_test ./testsuite/datasets/TEST_splitter.py
echo '##[endgroup]'

echo '##[group]testsuite_parameters'
run_test ./testsuite/parameters/TEST_config_param.py
run_test ./testsuite/parameters/TEST_padapter1.py
run_test ./testsuite/parameters/TEST_padapter.py
run_test ./testsuite/parameters/TEST_pfactory.py
run_test ./testsuite/parameters/TEST_pproc.py
run_test ./testsuite/parameters/TEST_psource.py
echo '##[endgroup]'

echo '##[group]testsuite_basic'
run_test ./testsuite/TEST_activity.py
run_test ./testsuite/TEST_debug.py
run_test ./testsuite/TEST_eventhandler.py
run_test ./testsuite/TEST_exception.py
run_test ./testsuite/TEST_go.py
run_test ./testsuite/TEST_gui.py
run_test ./testsuite/TEST_jobdb.py
run_test ./testsuite/TEST_jobselector.py
run_test ./testsuite/TEST_logging.py
run_test ./testsuite/TEST_output_processor.py
run_test ./testsuite/TEST_plugins.py
run_test ./testsuite/TEST_process.py
run_test ./testsuite/TEST_report.py
run_test ./testsuite/TEST_task.py
run_test ./testsuite/TEST_taskresync.py
run_test ./testsuite/TEST_utils.py
run_test ./testsuite/TEST_webservice.py
echo '##[endgroup]'

echo '##[group]testsuite_ansi'
export GC_TERM=dumb; run_test ./testsuite/TEST_ansi.py
export GC_TERM=gc_color16; run_test ./testsuite/TEST_ansi.py
export GC_TERM=gc_color256; run_test ./testsuite/TEST_ansi.py
echo '##[endgroup]'

exit $GC_RESULT
