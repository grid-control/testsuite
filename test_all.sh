#!/bin/bash

cd "$(dirname $0)/.."
export GC_WRAPPER="$1"
export GC_SCRIPT="$2"
export GC_RESULT=0

./testsuite/test_travis_testsuite.sh "$GC_WRAPPER"
EXITCODE="$?"
if [ "$EXITCODE" = "0" ]; then
	echo "TESTSUITE - ok";
else
	echo "TESTSUITE - FAILED";
	export GC_RESULT=1
fi
if [ -n "$TRAVIS" ]; then
	bash <(curl -s https://codecov.io/bash) -c -F testsuite || echo "Codecov did not collect coverage reports"
fi

./testsuite/test_travis_stresstest.sh "$GC_WRAPPER" "$GC_SCRIPT"
EXITCODE="$?"
if [ "$EXITCODE" = "0" ]; then
	echo "STRESSTEST - ok";
else
	echo "STRESSTEST - FAILED";
	export GC_RESULT=1
fi
if [ -n "$TRAVIS" ]; then
	bash <(curl -s https://codecov.io/bash) -c -F stresstest || echo "Codecov did not collect coverage reports"
fi

./testsuite/test_travis_scripts.sh "$GC_WRAPPER"
EXITCODE="$?"
if [ "$EXITCODE" = "0" ]; then
	echo "SCRIPTS - ok";
else
	echo "SCRIPTS - FAILED";
	export GC_RESULT=1
fi
if [ -n "$TRAVIS" ]; then
	bash <(curl -s https://codecov.io/bash) -c -F scripts || echo "Codecov did not collect coverage reports"
fi

exit $GC_RESULT
