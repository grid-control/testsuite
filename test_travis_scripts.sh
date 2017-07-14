#!/bin/sh

cd "$(dirname $0)/.."
export GC_WRAPPER="$1"

travis_run() {
	echo "$@"
	$GC_WRAPPER "$@"
}

echo 'travis_fold:start:scripts_dataset_nick'
travis_run ./scripts/dataset_nick.py || echo
travis_run ./scripts/dataset_nick.py /TEST/DATASET -L
travis_run ./scripts/dataset_nick.py testsuite/datasets/dataA.dbs -L
echo 'travis_fold:end:scripts_dataset_nick'

echo 'travis_fold:start:scripts_se_output_md5_list'
travis_run ./scripts/se_output_md5_list.py || echo
travis_run ./scripts/se_output_md5_list.py docs/examples/ExampleS1_stresstest.conf id:x || echo
travis_run ./scripts/se_output_md5_list.py docs/examples/ExampleS1_stresstest.conf nick:Dataset2_changed
echo 'travis_fold:end:scripts_se_output_md5_list'

echo 'travis_fold:start:scripts_parameter_info'
travis_run ./scripts/parameter_info.py || echo
travis_run ./scripts/parameter_info.py -l 'A' -p 'A=123' -j 321 -S param.gz -vvvta --parseable
travis_run ./scripts/parameter_info.py -l 'var("A")' -p 'A=123 456' -F modular --parseable
travis_run ./scripts/parameter_info.py "A B <data>" -D True -p "A=1 2 3" -p "B=x y" -lcc --logging INFO2
travis_run ./scripts/parameter_info.py docs/examples/ExampleS1_stresstest.conf -TlcLv -D docs/examples/work.ExampleS1_stresstest/datamap.tar
travis_run ./scripts/parameter_info.py 'A' -p 'A = 1 2' -ltdT -V A
travis_run ./scripts/parameter_info.py 'A' -p 'A = 3 2' -ltdT
echo 'travis_fold:end:scripts_parameter_info'

echo 'travis_fold:start:scripts_dataset_list_from'
travis_run ./scripts/dataset_list_from_gc.py || echo
travis_run ./scripts/dataset_list_from_gc.py docs/examples/ExampleS1_stresstest.conf --dump-config
travis_run ./scripts/dataset_list_from_gc.py docs/examples/ExampleS1_stresstest.conf -i OutputDirsFromConfig,JobInfoFromOutputDir,FilesFromJobInfo -d @SE_OUTPUT_FILE@
travis_run ./scripts/dataset_list_from_gc.py docs/examples/ExampleS1_stresstest.conf -s '*' -D'.:-1:' -d '@DELIMETER_DS@' -o output.dbs
travis_run ./scripts/dataset_list_from_ls.py -D '_:1:2'
echo 'travis_fold:end:scripts_dataset_list_from'

echo 'travis_fold:start:scripts_report_lumi'
travis_run ./scripts/report_lumi.py -j || echo
travis_run ./scripts/report_lumi.py -G || echo
travis_run ./scripts/report_lumi.py -G x || echo
travis_run ./scripts/report_lumi.py -F 1-2 || echo
travis_run ./scripts/report_lumi.py -J 1-2 || echo
travis_run ./scripts/report_lumi.py -GJF 123:1-123:10
travis_run ./scripts/report_lumi.py -gjep docs/examples/ExampleS2_stresscms1.conf
travis_run ./scripts/report_lumi.py -gje docs/examples/ExampleS2_stresscms2.conf
rm docs/examples/work.ExampleS2_stresscms1/output/job_0/cmssw.dbs.tar.gz
rm docs/examples/work.ExampleS2_stresscms2/datamap.tar
travis_run ./scripts/report_lumi.py -j docs/examples/ExampleS2_stresscms2.conf
echo 'travis_fold:end:scripts_report_lumi'

echo 'travis_fold:start:scripts_report'
travis_run ./scripts/report.py | echo
travis_run ./scripts/report.py docs/examples/ExampleS1_stresstest.conf -R "modern bar module trivial null lean" -T
travis_run ./scripts/report.py --report-list -T -R variables docs/examples/ExampleS2_stresscms2.conf --pivot
echo 'travis_fold:end:scripts_report'

echo 'travis_fold:start:scripts_dataset_info'
travis_run ./scripts/dataset_info.py | echo
travis_run ./scripts/dataset_info.py -QNlbfsmMOcnT 0 -C docs/examples/Example02_local.conf -S tmp testsuite/datasets/dataK.dbs testsuite/datasets/dataE.dbs
travis_run ./scripts/dataset_info.py -smM testsuite/datasets/dataE.dbs
echo 'travis_fold:end:scripts_dataset_info'

echo 'travis_fold:start:scripts_se_download'
export SE_OUTPUT_DOWNLOAD_EXEC="./scripts/se_output_download.py -T trivial --slowdown=0 --parseable"
travis_run $SE_OUTPUT_DOWNLOAD_EXEC || echo
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -m --select-se tmx
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 1,2 -m -t 2
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 1,2 -m --shuffle
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 1,2 -j
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 1,2 -j --overwrite --loop
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 1,2 -s --ignore-mark-dl
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 1,2
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf --delete --select-se tmx --ignore-mark-dl
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 3,4 --delete -t 2
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 3,4 -D -t 2
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms2.conf -J 3,4 -D
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms3.conf -J 1,2
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms3.conf -J 1,2 -D
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS2_stresscms3.conf -J 1,2 --mark-empty-fail
echo "print(__import__(\"os\").path.dirname(__import__(\"grid_control_gui\").__file__))" > locate_gui.py
export GUI_PACKAGE_DIR=$(python locate_gui.py)
mv $GUI_PACKAGE_DIR tmp_gui
travis_run $SE_OUTPUT_DOWNLOAD_EXEC docs/examples/ExampleS1_stresstest.conf -J 1,2 -j -t 2 --no-verify-md5
mv tmp_gui $GUI_PACKAGE_DIR
echo 'travis_fold:end:scripts_se_download'

echo 'travis_fold:start:scripts_plugin'
travis_run ./scripts/plugins.py || echo
travis_run ./scripts/plugins.py --parseable WMS
travis_run ./scripts/plugins.py -p WMS
travis_run ./scripts/plugins.py -c WMS
echo 'travis_fold:end:scripts_plugin'
