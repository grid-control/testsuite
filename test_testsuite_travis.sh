#!/bin/sh

WRAPPER="$1"

echo 'travis_fold:start:testsuite_backend'
$WRAPPER ./testsuite/backend/TEST_backend.py
$WRAPPER ./testsuite/backend/TEST_basic.py
$WRAPPER ./testsuite/backend/TEST_broker.py
$WRAPPER ./testsuite/backend/TEST_cancel.py
$WRAPPER ./testsuite/backend/TEST_discover.py
$WRAPPER ./testsuite/backend/TEST_jdl.py
$WRAPPER ./testsuite/backend/TEST_proxy.py
$WRAPPER ./testsuite/backend/TEST_status.py
$WRAPPER ./testsuite/backend/TEST_submit.py
echo 'travis_fold:end:testsuite_backend'

echo 'travis_fold:start:testsuite_cms'
$WRAPPER ./testsuite/cms/TEST_cms_cert.py
$WRAPPER ./testsuite/cms/TEST_cmssw.py
$WRAPPER ./testsuite/cms/TEST_cmssw_scanner.py
$WRAPPER ./testsuite/cms/TEST_lumifilter.py
$WRAPPER ./testsuite/cms/TEST_lumiproc.py
$WRAPPER ./testsuite/cms/TEST_lumitools.py
$WRAPPER ./testsuite/cms/TEST_provider_cms.py
$WRAPPER ./testsuite/cms/TEST_provider_das.py
$WRAPPER ./testsuite/cms/TEST_sitedb.py
echo 'travis_fold:end:testsuite_cms'

echo 'travis_fold:start:testsuite_config'
$WRAPPER ./testsuite/config/TEST_configAPI1.py
$WRAPPER ./testsuite/config/TEST_configAPI2.py
$WRAPPER ./testsuite/config/TEST_configAPI3.py
$WRAPPER ./testsuite/config/TEST_configAPI4.py
$WRAPPER ./testsuite/config/TEST_configContainer.py
$WRAPPER ./testsuite/config/TEST_configHandlers.py
$WRAPPER ./testsuite/config/TEST_configModify.py
$WRAPPER ./testsuite/config/TEST_configParser.py
$WRAPPER ./testsuite/config/TEST_config.py
$WRAPPER ./testsuite/config/TEST_configTyped.py
$WRAPPER ./testsuite/config/TEST_configView.py
$WRAPPER ./testsuite/config/TEST_interactive.py
$WRAPPER ./testsuite/config/TEST_matcher.py
echo 'travis_fold:end:testsuite_config'

echo 'travis_fold:start:testsuite_datasets'
$WRAPPER ./testsuite/datasets/TEST_dataresync1.py
$WRAPPER ./testsuite/datasets/TEST_dataresync2.py
$WRAPPER ./testsuite/datasets/TEST_dataresync3.py
$WRAPPER ./testsuite/datasets/TEST_dataresync4.py
$WRAPPER ./testsuite/datasets/TEST_dataresync5.py
$WRAPPER ./testsuite/datasets/TEST_dataresync_meta.py
$WRAPPER ./testsuite/datasets/TEST_dataresync_reorder.py
$WRAPPER ./testsuite/datasets/TEST_processor.py
$WRAPPER ./testsuite/datasets/TEST_provider.py
$WRAPPER ./testsuite/datasets/TEST_scanner.py
$WRAPPER ./testsuite/datasets/TEST_splitterio.py
$WRAPPER ./testsuite/datasets/TEST_splitter.py
echo 'travis_fold:end:testsuite_datasets'

echo 'travis_fold:start:testsuite_parameters'
$WRAPPER ./testsuite/parameters/TEST_config_param.py
$WRAPPER ./testsuite/parameters/TEST_padapter1.py
$WRAPPER ./testsuite/parameters/TEST_padapter.py
$WRAPPER ./testsuite/parameters/TEST_pfactory.py
$WRAPPER ./testsuite/parameters/TEST_pproc.py
$WRAPPER ./testsuite/parameters/TEST_psource.py
echo 'travis_fold:end:testsuite_parameters'

echo 'travis_fold:start:testsuite_basic'
$WRAPPER ./testsuite/TEST_activity.py
$WRAPPER ./testsuite/TEST_debug.py
$WRAPPER ./testsuite/TEST_eventhandler.py
$WRAPPER ./testsuite/TEST_exception.py
$WRAPPER ./testsuite/TEST_go.py
$WRAPPER ./testsuite/TEST_gui.py
$WRAPPER ./testsuite/TEST_jobdb.py
$WRAPPER ./testsuite/TEST_jobselector.py
$WRAPPER ./testsuite/TEST_logging.py
$WRAPPER ./testsuite/TEST_output_processor.py
$WRAPPER ./testsuite/TEST_plugins.py
$WRAPPER ./testsuite/TEST_process.py
$WRAPPER ./testsuite/TEST_report.py
$WRAPPER ./testsuite/TEST_task.py
$WRAPPER ./testsuite/TEST_taskresync.py
$WRAPPER ./testsuite/TEST_utils.py
$WRAPPER ./testsuite/TEST_webservice.py
echo 'travis_fold:end:testsuite_basic'

echo 'travis_fold:start:testsuite_ansi'
export GC_TERM=dumb; $WRAPPER ./testsuite/TEST_ansi.py
export GC_TERM=gc_color16; $WRAPPER ./testsuite/TEST_ansi.py
export GC_TERM=gc_color256; $WRAPPER ./testsuite/TEST_ansi.py
echo 'travis_fold:end:testsuite_ansi'
