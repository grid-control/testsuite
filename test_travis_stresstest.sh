#!/bin/sh

cd "$(dirname $0)/.."
export GC_WRAPPER="$1"
export GC_SCRIPT="$2"
if [ -z "$GC_SCRIPT" ]; then export GC_SCRIPT="go.py"; fi
export GC_CHECK_OUTPUT=true
echo > gc_debug_stack.log

travis_run() {
	echo "$@"
	$GC_WRAPPER "$@"
}

echo 'travis_fold:start:stress_test_basic'
travis_run $GC_SCRIPT -s -o '[jobs] continuous = False' docs/examples/ExampleS1_stresstest.conf
travis_run $GC_SCRIPT --reset INIT docs/examples/ExampleS1_stresstest.conf
travis_run $GC_SCRIPT -o '[jobs] continuous = False' docs/examples/ExampleS1_stresstest.conf
travis_run $GC_SCRIPT -o '[interactive] default = False' -d ALL docs/examples/ExampleS1_stresstest.conf
travis_run $GC_SCRIPT -G --debug docs/examples/ExampleS1_stresstest.conf --logging config=INFO --logging classloader
travis_run $GC_SCRIPT -G docs/examples/ExampleS1_stresstest.conf > test.ansi; EXITCODE=$?
if [ "$EXITCODE" != "0" ]; then cat test.ansi; fi
travis_run $GC_SCRIPT -o '[global] gui = NullGUI' docs/examples/ExampleS1_stresstest.conf --debug-trace="fun_name=xyz"
travis_run $GC_SCRIPT docs/examples/ExampleS1_stresstest.conf
diff ExampleS1_stresstest.list docs/examples/ExampleS1_stresstest.list.ref
echo 'travis_fold:end:stress_test_basic'

echo 'travis_fold:start:stress_test_cms_1'
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms1.conf
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms1.conf --help-conf
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms1.conf --help-confmin
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms1.conf -cm 1
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms1.conf
echo 'travis_fold:end:stress_test_cms_1'

echo 'travis_fold:start:stress_test_cms_2'
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms2.conf
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms2.conf -cm 1
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms2.conf
echo 'travis_fold:end:stress_test_cms_2'

echo 'travis_fold:start:stress_test_cms_3'
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms3.conf
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms3.conf -cm 1
travis_run $GC_SCRIPT docs/examples/ExampleS2_stresscms3.conf
diff ExampleS2_stresscms3.list docs/examples/ExampleS2_stresscms3.list.ref
echo 'travis_fold:end:stress_test_cms_3'
