set -e
cd ..
export WRAPPER="$1"
export SE_OUTPUT_DOWNLOAD_EXEC="./scripts/se_output_download.py -T trivial --slowdown=0"
cat .travis.yml | grep script -A 1000 | cut -d "-" -f 2- | grep WRAPPER | grep scripts | while read ENTRY; do
	echo "========================================="
	echo $ENTRY
	eval $ENTRY
done
