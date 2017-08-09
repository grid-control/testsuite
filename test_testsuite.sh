OLDPWD=$PWD
cd $(dirname $0)
SEARCH="$2"
set +e
for EXE in `find '.' | grep "$SEARCH" | grep TEST | grep -v pyc | sort | grep -v svn | grep -v scale | grep -v fuzz`; do
	grep -q ${EXE#./} test_travis_testsuite.sh || echo -n "not tested: "
	echo $1 ${EXE#./}
	$1 $EXE
done
