#!/bin/bash

cd "$(dirname $0)/.."
export GC_WRAPPER="$1"
export GC_SCRIPT="$2"

./testsuite/test_travis_testsuite.sh "$GC_WRAPPER"
if [ -n "$TRAVIS" ]; then
	bash <(curl -s https://codecov.io/bash) -c -F testsuite || echo "Codecov did not collect coverage reports"
fi

./testsuite/test_travis_stresstest.sh "$GC_WRAPPER" "$GC_SCRIPT"
if [ -n "$TRAVIS" ]; then
	bash <(curl -s https://codecov.io/bash) -c -F stresstest || echo "Codecov did not collect coverage reports"
fi

./testsuite/test_travis_scripts.sh "$GC_WRAPPER"
if [ -n "$TRAVIS" ]; then
	bash <(curl -s https://codecov.io/bash) -c -F scripts || echo "Codecov did not collect coverage reports"
fi
